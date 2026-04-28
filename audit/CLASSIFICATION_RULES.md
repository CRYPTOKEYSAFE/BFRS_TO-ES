# Layer 3 Classification Rules

This document defines the function that maps each billet in a unit's
T/O&E to a NOTE tag of the form `<CCN><suffix>`. The NOTE tag drives
the COUNTIFS lookups inside CCN calculation sheets and is the spine
of the BFR pipeline (see `audit/PIPELINE.md`, Layers 2 and 3).

Status: STARTER. The general-pattern rules below come from the
observed suffix vocabulary in CLB-4 SW BFR and 3d Med Bn BFR
(`audit/reports/11_pipeline_probe.txt`), restated in plain prose.
SME-specific rule rows (BMOS to facility CCN) are placeholders marked
TBD pending FC 2-000-05N planning-factor tables and unit-type doctrine
input. Apex Omega rule 4 applies: do not silently fill TBD rows.

## Inputs

A billet record from a Format A or Format C T/O&E source carries:

| Field | Meaning |
|---|---|
| BIC | Billet Identification Code (unique per billet within a unit) |
| Billet Description | Plain-text role title |
| Alpha Grade | E-1 to E-9, W-1 to W-5, O-1 to O-10, etc. |
| BMOS | Billet MOS (the MOS the billet is coded for) |
| PMOS | Primary MOS (the MOS the assigned Marine actually holds) |
| MCC | Marine Corps Command code |
| UIC | Unit Identification Code (parent unit) |

The classifier consumes these six fields plus optional unit-context
inputs (unit type, parent UIC, region) and emits a single NOTE tag
plus a confidence flag.

## Output

A NOTE tag matches the regex `^\d{4,5}[a-z]{0,4}$`:

| Tag form | Example | Meaning |
|---|---|---|
| `<CCN><suffix>` | `21710o` | This billet generates demand on CCN 21710 in role "o" (private office) |
| `<CCN>` | `14345` | TE row only. Equipment record's primary facility CCN |
| (none) | | Excluded from BFR demand. Billet is mobile or shipboard or otherwise non-facility-loading |

## Suffix vocabulary

Observed in CLB-4 and 3d Med Bn. Must be ratified against
FC 2-000-05N before being treated as canonical.

| Suffix | Meaning | Loading factor (observed) |
|---|---|---|
| `o` | Office, private. Officer (O-1 to O-10) or SNCO (E-6 and above) | 120 GSF / person |
| `c` | Cubicle. Junior enlisted (E-5 and below) and most NCOs in admin sections | 60 GSF / person |
| `w` | Warehouse worker | 60 GSF / person, divide by 3 |
| `rs` | Radio section | divide by 15 to get bay count |
| `cs` | Comm section | divide by 15 |
| `ds` | Data section | divide by 15 |
| `ws` | Wire section | divide by 15 |
| `shf` | SHF section | divide by 15 |
| `ms` | Maintenance section | divide by 15 |
| `a` | Armory work area | 1.25 GSF / item |
| `1` | Personal effects entitlement | 1 unit / chargeable person |
| (bare) | Equipment record's primary facility CCN | TE rows only |

The 120 / 60 / divide-by-N values are CLB-4-extracted and need to be
verified against the current FC 2-000-05N edition for each
facility type. Different facility CCNs may use different per-person
or per-section ratios.

## General-pattern rules

These three apply to every unit's billets unless a specific BMOS or
section-residency rule overrides them:

1. Officer or SNCO (Alpha Grade pay grade O-1 or higher, or E-6 or
   higher) of an admin or HQ section: tag `<admin_CCN>o`. Default
   admin_CCN is `61072` for Marine battalion / squadron HQs; other
   unit types have their own admin CCN per FC 2-000-05N.
2. Junior enlisted (Alpha Grade E-1 to E-5) of an admin or HQ
   section: tag `<admin_CCN>c`.
3. Equipment items in TE: tag with the CCN whose facility stores or
   maintains the equipment (auto-org-shop CCN 21451 for organic
   vehicles, open-storage CCN 45110 for laydown, etc.).

## Section-residency rules

These override the general-pattern rules when a billet's BMOS or
Billet Description identifies it as physically working in a non-admin
facility:

| If BMOS in | And section is | Tag | Source / TBD |
|---|---|---|---|
| 0481, 0491 (Logistics) | Auto Org Shop | `<auto_org_CCN>` based | TBD pending FC 2-000-05N Series 200 ratification |
| 3500 series (Motor T) | Auto Org Shop | `<auto_org_CCN>` based | TBD |
| 0600 series (Comm) | Comm Maint Shop | `21710` plus suffix `rs/cs/ds/ws/shf/ms` per sub-section | TBD |
| 0800 series (Field Artillery) | Ammo / ordnance | TBD | TBD |
| 1300 series (Engineer) | Field Maint Shop | `21730` plus suffix | TBD |
| 1800 series (Tank / AAV) | Field Maint Shop | `21730` plus suffix | TBD |
| 2300 series (EOD) | EOD Facility | `14326` based | TBD pending FC 2-000-05N Series 100 EOD table |
| 2800 series (Data / Comm) | Data section | `21710ds` | TBD |
| 3000 series (Supply) | Warehouse | `44112w` or admin per role | TBD |
| 3400 series (Finance) | Admin | general-pattern rules apply | TBD |
| 4400 series (Legal) | Admin | general-pattern rules apply | TBD |
| 5500 series (Music) | Special facility | TBD | TBD |
| 5800 series (MP / Corrections) | MP / brig CCN | TBD | TBD |
| 5900 series (Electronic Maint) | Comm/Elec Maint Shop | `21710` plus suffix | TBD |
| 6000-6500 series (Aviation Maint) | Aviation hangar / shop | TBD pending FC 2-000-05N Series 200 aviation CCNs | TBD |
| 6500-6700 series (Aviation Ord) | Aviation ordnance | TBD | TBD |
| 7200 series (Air Control) | ATC tower / control bldg | `141 70` | TBD |
| 8000 series (Medical) | Medical / dental | `54xxx` series | TBD pending FC 2-000-05N Series 500 medical CCNs |

Every TBD row in this table is `TBD pending [FC 2-000-05N table id]`
per Apex Omega rule 4 and rule 7. The classifier emits an
`unclassified` result when a billet matches no rule, with
human-readable text identifying the BMOS, Alpha Grade, and Billet
Description. Unclassified billets are not silently dropped; they
appear in the validator's billet-accounting check (Check 7) as
orphans and must be resolved before release.

## Per-unit overrides

Each unit profile may supply a `classification_overrides.yaml`
mapping specific BMOS or Billet Description patterns to NOTE tags.
This is how a unit-specific exception (e.g., a CLB-attached EOD
detachment vs. an organic EOD platoon) is handled without modifying
the doctrine table.

## Output schema (audit/CLASSIFICATION_RULES.yaml)

```yaml
provenance:
  authority: "FC 2-000-05N (Marine Corps BFR), unit-type doctrine,
              MOS Manual MCO 1200.18"
  ratified_against: "TBD pending FC 2-000-05N Series 100 / 200 PDF
                     extraction (audit/extract_planning_factors.py)"
  source_date: "TBD"
rules:
  - id: officer_admin_default
    when:
      alpha_grade_min: "O-1"
      section: "admin_or_hq"
    tag_template: "{admin_ccn}o"
    confidence: high
    citation: "Observed in CLB-4 SW BFR 61072; ratify against FC
               2-000-05N admin facility table"
  - id: snco_admin_default
    when:
      alpha_grade_min: "E-6"
      section: "admin_or_hq"
    tag_template: "{admin_ccn}o"
    confidence: high
    citation: "Observed in CLB-4 SW BFR 61072; ratify against FC
               2-000-05N admin facility table"
  - id: junior_enlisted_admin
    when:
      alpha_grade_max: "E-5"
      section: "admin_or_hq"
    tag_template: "{admin_ccn}c"
    confidence: high
  - id: bmos_0600_comm
    when:
      bmos_prefix: "06"
    tag_template: "21710{section_suffix}"
    confidence: low
    citation: "TBD pending FC 2-000-05N Series 200 comm/elec
               maintenance shop table"
  # ... more rules
unclassified_disposition:
  emit: orphan
  message: "billet does not match any rule; SME review required"
```

## Pipeline contract

A future `pipeline/classify.py` will:

1. Load `audit/CLASSIFICATION_RULES.yaml`.
2. For each billet in a Format A or Format C T/O&E:
   a. Apply per-unit overrides first.
   b. Apply BMOS section-residency rules.
   c. Apply general-pattern rules.
   d. If no rule matches, emit `unclassified` with the row reference.
3. For each TAMCN row in the equipment side:
   a. Look up primary facility CCN per FC 2-000-05N TAMCN dimensional
      table (currently `audit/CCN_VOCABULARY.json` carries CCN names
      but not TAMCN to CCN mappings; that is its own scaffold).
   b. Emit bare CCN tag.
4. Write the resulting NOTE column into the in-workbook TO and TE
   sheets (Format B).
5. The validator (`pipeline/validate.py`, Checks 2, 3, 7, 8) gates
   the result.

The classifier itself is pure: same inputs always produce the same
NOTE tag. Doctrine changes go through the rule table, not the code.

## What this commit ships

The doctrine schema and a starter rule table. No automated
classification yet. Per Apex Omega rule 4, every doctrine-specific
rule row is marked TBD pending FC 2-000-05N ratification and unit
doctrine SME review. The schema is stable enough that the rule table
can be filled in and the classifier built against it without
schema churn.

## Next concrete actions

1. Pull FC 2-000-05N Series 100 and 200 PDFs into the repo.
2. Run `audit/extract_planning_factors.py` to produce the per-CCN
   factor table.
3. Author the BMOS to facility CCN doctrine table by joining the MOS
   Manual (MCO 1200.18) against the FC 2-000-05N planning factor
   tables.
4. Replace TBD rows in `audit/CLASSIFICATION_RULES.yaml` with cited
   rule rows.
5. Build `pipeline/classify.py`.
6. Wire the classifier into the pipeline so generated BFRs carry a
   populated NOTE column.
