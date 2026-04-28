# Unit-Agnostic BFR Data Pipeline, Contract Specification

This document defines what the data pipeline between TO&E source data and the
BFRL output workbook must look like for the BFRL to roll up correctly,
deterministically, and audit-defensibly for any USMC unit, not just CLB-4.
CLB-4 is referenced only as the worked example.

The contract has six layers. Every layer must hold, or the BFR is not
airtight. The CLB-4 SW BFR currently fails at Layer 3 (the CCN+suffix
tagging is missing from the in-workbook TO/TE), which is why the legacy
CCN calculation sheets all resolve to `#REF!` or zero.



## Layer 1, Three TO&E source formats coexist in this domain

Round-2 schema map (`audit/reports/10_schema_map.txt`) confirms three
distinct source formats. Any pipeline tool must handle all three, or
explicitly reject what it can't ingest.

### Format A, Per-Company TFSMS Export (Excel)

Files in this repo: `M29111_HQ_CO_CLB-4`, `M29112_CLC_A_CLB-4`,
`M29113_CLC_B_CLB-4`, `M29114_GS_CO_CLB-4`.

Sheets: `Header`, `TO`, `Billet Summary`, `RecapMOS`, `RecapMCC`,
`Footnotes`, `Primary Only` (TE-side), `X-78`, `COE`,
`Task Organized T_E`.

TO header layout: multi-row merged header at rows 5, 7 spanning 46
columns. Row 5 carries the primary labels (`Rec CD | BIC | Billet
Description | Alpha Grade | BMOS ASD1 ASD2 | P | B R N | T Y P | ...`);
rows 6 and 7 carry chargeability sub-labels for the Off/Enl pair columns.

TE header layout (`Primary Only`): multi-row header at rows 8, 10
spanning 37 columns. Row 8 carries primary labels (`TAMCN | Nomenclature
| TAM Stat | U/I | Rdy | Ind Qty | Org Qty | Unit | ...`); rows 9, 10 carry
year sub-labels (`2026 | 2027 | 2028 | ...` x `Unf | Pln`).

CRITICAL: Format A carries no `CCN` column and no `NOTE`/suffix
column. It is pure billet-and-equipment roster data with zero facility
classification. Any CCN tagging must be applied as a transformation step
before this data can drive a BFR.

### Format B, BFR-Embedded TO/TE

Files in this repo: the `TO` and `TE` sheets *inside* the BFR
workbooks (`SW_M29030_CLB4_BFR_2026-NWPCW167400L021.xlsx`,
`M67400-FO-M13020 3D MED BN-22NOV2024.xlsx`).

Header layout: single-row header at row 3 (3D Med Bn) or row 4
(CLB-4 SW), 41 columns. First six columns are the spine:
`LINE | NOTE | CCN | CCN Description | UIC | Rec CD | BIC | Billet Description | ...`.

TE-side header: single-row at row 1, 20 columns:
`ROW | NOTE | CCN | CCN Description | CCN 21451 Equipment Type (if applicable)
| UIC | TAMCN Short | TAMCN | Nomenclature | TAM Stat | U/I | Rdy |
Ind Qty | Org Qty | Unit T/E | L, Ft | W, Ft | H, Ft | Volume Ea | Volume Total`.

This is the format the CCN calculation sheets are written to read. Every
COUNTIFS / SUMIFS / INDEX-MATCH lookup in the legacy hidden CCN tabs
expects to find data in Format B layout, with the NOTE column carrying
CCN+suffix tags.

### Format C, Master MEF / Wide TFSMS Export (Excel)

Files in this repo: `2031 Master TO&E v1.1 - 20250411.xlsx` , 
`TO_2` (24,299 rows x 51 cols), `TE_3` (19,002 rows x 27 cols).

Header layout: single-row at row 1. Rich chargeability breakdown:
`Marine Active Chargeable Officer | CHARG ACT MAR ENLST |
Chargeable Marine Res Officer | ... | Non-Chargeable Marine Active Officer |
...` (16 chargeability columns), plus `MCC`, `Footnote`, `Fiscal Year`,
`Hierarchy Order Number`, `Pay Grade`, `Geolocation Name`, `Installation
Name/City`, `Chargeable Category`, `UIC - Unit Name`, `Grade Type`.

TE-side has dimensional and space-factor data: `L, Ft`, `W, Ft`,
`H, Ft`, `Volume EA, ft3`, `Volume Total, ft3`, `Space Factor`, `NSY`,
`NTG Factor`. This is the richest TE source but carries no per-billet
CCN tag in the actual data rows (the `CCN` column header exists but
data rows show `None` in that column).

Coverage: the file in this repo covers UICs `M00102`, `M00105`,
`M00109` ... `M29003-M29494` (selected). It does not cover `M29030 /
M29031 / M29111-14` (CLB-4). It is for a different MEF/MLG. Whether
3d MLG has a corresponding Master TO&E is unknown to me; if it exists,
it should be obtained and added to this repo.

### Format D, TFSMS / ASR / Authoritative PDF

Files in this repo: none yet observed. Real engagements will supply
TFSMS printable PDFs, ASR PDFs, or other authoritative T/O&E printouts.

The pipeline must accept these and extract tabular billet and equipment
data with citation-grade fidelity. Ingestion requirements:

- Per-row citation, every extracted record carries the source PDF
  filename, page number, and table/row reference. This satisfies Apex
  Omega Sec.5.4 (verify against primary source) and Sec.8.1 (cite source +
  section + date inline).
- Confidence threshold, if a value cannot be extracted with high
  confidence (low-confidence OCR, ambiguous column boundary,
  illegible scan), mark it `TBD, pending [page reference]` per
  Apex Omega Sec.6 / Sec.8.3. Never invent a value to fill a gap.
- Schema target, the extractor's output is the canonical Format A
  schema (one row per billet, one row per TAMCN). After extraction,
  PDF-sourced data flows through the same downstream stages as
  Excel-sourced data.
- Tooling options (to be selected in implementation):
  `pdfplumber`, `camelot-py`, `tabula-py`, or text-mode extraction
  with hand-coded column splits. OCR (`tesseract`, `paddleocr`) only
  for scanned PDFs; native-text PDFs use direct extraction.
- No silent corrections. If a PDF says `LtCol`, the extracted value
  is `LtCol`, not `LTCOL`. Normalization happens in a separate
  documented step that emits a diff log.



## Operational modes

The pipeline runs in one of three modes. Each mode declares its inputs
and its output contract. The same internal stages (Layers 1, 6 below) are
used; the modes differ in whether the existing-BFR input exists and
whether the output is a new workbook or an updated one.

### Update-existing (the common case)

Inputs: existing BFR workbook (Format B, possibly stale or partially
correct) + new T/O&E source data (Format A, C, or D).

Output: the BFR workbook with refreshed loading data, recomputed
CCN totals, regenerated summary tabs (`UNIT_ROLLUP`, `RecapMCC`-style,
`Billet Summary`-style, equipment-by-CCN), and repaired lookup contracts
(broken `#REF!` / restricted-range formulas rewritten to full-column
references). Output is paired with a diff report enumerating every
cell that changed, with before/after values and traceable cause.

### Generate-new

Inputs: T/O&E source data only (Format A, C, or D) + project
metadata (UIC, building number, planner, programmed FY, region).

Output: a fresh BFR workbook built against the canonical template,
cosmetic per `STYLE_GUIDE.md`, with all CCN sheets populated from the
T/O&E data via the documented classification rule set (Layer 3).

### Audit-existing

Inputs: existing BFR workbook only.

Output: a forensic findings report (the work product of round 1 on
CLB-4 SW lives in `audit/FINDINGS.md`) plus a repair plan listing each
broken sheet, the failure mode, and the recommended fix path
(rebuild vs. surgical repair).



## Layer 2, The CCN+Suffix Tagging Mechanism (the Pipeline Spine)

### What it is

Every CCN calculation sheet in a BFR workbook needs to count, by
sub-category, how many billets or equipment items belong in that CCN's
facility. The mechanism is a string tag of the form `<CCN><suffix>`
placed in the `NOTE` column of the in-workbook TO and TE sheets.

Round-2 evidence (`audit/reports/05_hidden_ccn_*.txt`) gives us the
following observed suffix vocabulary used by the legacy CCN sheets:

| Suffix | Meaning | Used by sheet |
|---|---|---|
| `o` | Office (private, >=E-6 / officer), 120 GSF/person | 14345, 21710, 21730, 44112 |
| `c` | Cubicle (<=E-5), 60 GSF/person | 14345, 21710, 21730, 44112 |
| `w` | Warehouse worker (clerk), 60 GSF/person, /3 ratio | 44112 |
| `rs` | Radio section staffing, counted /15 to bays | 21710, 21730 |
| `cs` | Comm section | 21710, 21730 |
| `ds` | Data section | 21710, 21730 |
| `ws` | Wire section | 21710, 21730 |
| `shf` | SHF section | 21710, 21730 |
| `ms` | Maint section | 21710, 21730 |
| `a` | Armory work-area / personnel (observed in 3d Med Bn TO) | 14345 |
| (bare CCN) | Equipment record's primary facility CCN | TE rows |
| `1` | Personal Effects entitlement, 1 per chargeable person | 44112 |

This list is observed, not authoritative. A canonical vocabulary
sourced from FC 2-000-05N planning factor tables (per CCN) must be
the source of truth.

### Where it currently lives, and where it doesn't

`audit/reports/11_pipeline_probe.txt` searched all TO/TE sheets in the
repo for strings matching `^\d{4,5}[a-z]{1,4}$`. Findings:

| Workbook | Sheet | CCN+suffix hits | Bare CCN hits (Col D) |
|---|---|---:|---:|
| 4 x CLB-4 company files (Format A) | TO | 0 | 0 |
| 2 x CLB-4 company files (Format A) | Primary Only | 0 | 0 |
| CLB-4 SW (Format B) | TO | 0 | 264 (6 distinct CCNs) |
| CLB-4 SW (Format B) | TE | 0 | 305 (5 distinct CCNs) |
| 3D Med Bn (Format B) | TO | 9 (`44112w` x 5, `44112o` x 2, `14345o` x 1, `14345a` x 1) | 145 (6 distinct) |
| 3D Med Bn (Format B) | TE | 0 | 368 (5 distinct) |
| Master TO&E (Format C) | TO_2 | 0 | 0 (CCN header present but data column empty) |

The pipeline spine, the NOTE column with CCN+suffix tags, is
essentially absent from every workbook in this repo. The 9 tags in 3d
Med Bn are sparse outliers.

This is why the broken hidden CCN tabs in CLB-4 SW resolve to `#REF!`
or zero: even if their lookup *ranges* were repaired to point at the
populated `TO` and `TE` sheets, the COUNTIFS would still match zero rows
because the NOTE column is empty.

The 4 visible/working CCN sheets (`14345`, `21451`, `21455`, `61072`)
sidestep this entirely by hardcoding personnel and equipment counts.
That works for one-off authoring, but it can't be reproduced for new
units without manual re-classification each time. It is not a pipeline.



## Layer 3, The Classification Step (Currently Manual & Implicit)

To populate the NOTE column, every billet and every equipment item must
be classified to a `<CCN><suffix>` tag (or to "no facility CCN", e.g.
operational billets that don't generate facility demand). The
classification rule set is not documented in any file in this repo.

The rules that *should* be made explicit:

1. Officer / SNCO billets (Alpha Grade >= E-6 or O-1+) of a section
   whose primary work is in CCN X to tag `Xo` (private office).
2. Junior enlisted billets (Alpha Grade <= E-5) of that section  to 
   tag `Xc` (cubicle), unless the section's mission inherently puts
   them in a shop bay or warehouse.
3. Specialist billets that physically work in a maintenance shop or
   warehouse to tag `Xws`, `Xrs`, `Xw` etc., per FC 2-000-05N planning
   factor tables for that CCN.
4. Excluded billets (medical, EOD, ordnance repair) to tag with their
   own facility CCN (e.g. `541 series` for medical, `21420` for
   maintenance-with-bays, etc.) and let the matching CCN sheet pick them
   up.
5. Equipment items to tag with the primary CCN whose facility stores
   or maintains them. E.g. an LMTV truck to `21451` (auto org shop)
   or `44112` (organic storage) depending on stowage doctrine.

This rule set must come from FC 2-000-05N (specifically: per-CCN
planning factor tables) and from unit doctrine for which sections
physically reside where. It is the single most important deliverable
for an airtight pipeline. Without it, classification is whatever the
last analyst decided, and BFRs are not reproducible.



## Layer 4, In-Workbook TO/TE Tabs (Format B) Must Be Self-Contained

Once classified, the canonical Format B layout in the BFR workbook is:

### TO sheet (one row per billet)

Required columns, in order, header on row 3:

| # | Column | Source / Rule |
|---|---|---|
| 1 | LINE | sequential 1..N (or formula `=1+An-1`) |
| 2 | NOTE | `<CCN><suffix>` from classification, MANDATORY for every row |
| 3 | CCN | bare 5-digit CCN, must equal the CCN portion of NOTE |
| 4 | CCN Description | per FC 2-000-05N (lookup from `CCN & Description` reference sheet) |
| 5 | UIC | from TO source |
| 6 | Rec CD | from TO source (`E` enlisted, `C` civ, etc.) |
| 7 | BIC | from TO source, unique billet ID |
| 8 | Billet Description | from TO source |
| 9 | Alpha Grade | from TO source |
| 10 | BMOS / PMOS | from TO source |
| 11+ | chargeability columns | from TO source (per Format C/A schema) |

### TE sheet (one row per TAMCN-on-T/E)

Required columns, header on row 1:

| # | Column | Source / Rule |
|---|---|---|
| 1 | ROW | sequential or formula |
| 2 | NOTE | `<CCN>` (bare; equipment generally doesn't take suffixes) |
| 3 | CCN | bare 5-digit CCN |
| 4 | CCN Description | lookup |
| 5 | CCN 21451 Equipment Type | only populated for CCN 21451 rows (auto/medium/heavy) |
| 6 | UIC | from TE source |
| 7 | TAMCN Short | first 5 chars of TAMCN |
| 8 | TAMCN | full TAMCN |
| 9 | Nomenclature | from TE source |
| 10 | TAM Stat | DP / IS / etc. |
| 11 | U/I | EA / PR / etc. |
| 12 | Rdy | M/N |
| 13 | Ind Qty | individual quantity |
| 14 | Org Qty | organizational quantity |
| 15 | Unit T/E | sum |
| 16, 18 | L, W, H (Ft) | from FC 2-000-05N TAMCN dim table or from Format C TE_3 |
| 19 | Volume Ea, ft³ | `=LxWxH` |
| 20 | Volume Total, ft³ | `=Volume Ea x Unit T/E` |



## Layer 5, CCN Calculation Sheets Use Stable Lookup Contracts

Each CCN sheet must use lookup formulas that:

1. Reference full columns or named ranges in the in-workbook TO and
   TE sheets, never restricted ranges that break when rows are added.
   Example for admin-space count from TO:

   ```
   =COUNTIFS('TO'!$B:$B, "21710o", 'TO'!$E:$E, $B$32)
                ^^^^^^^^             ^^^^^^^^
                NOTE column          UIC column
   ```

   Not `'TO'!$B$5:$B$309` (today's anti-pattern, which is what got
   replaced with `#REF!` when someone resized the sheet).

2. Use a documented named range vocabulary for sheet-spanning
   constants. E.g. `NTG = 1.33`, `NSF_PER_OFFICE = 120`,
   `NSF_PER_CUBICLE = 60`, declared once on a `Constants` sheet.

3. Have no `IFERROR` masking of broken lookups. `IFERROR(...,"")` is
   forbidden as a top-level formula wrapper. If a formula can't resolve,
   the sheet must say so loudly. Use `IFERROR` only for genuinely
   optional reverse-lookups (e.g. nomenclature lookup that might miss).

4. Trace cleanly to one rolled-up cell per sheet that flows into
   `UNIT_ROLLUP`, typically `H40` or `H46` (`TOTAL REQUIREMENT`).



## Layer 6, Validation Harness (Pipeline Self-Test)

Before any BFR is "final", a deterministic validation pass must report
zero failures across:

1. Schema check, TO has the 11+ required columns, TE has the 20
   required columns, header rows are at the documented positions.
2. NOTE coverage, every TO row has a non-empty NOTE matching
   `^\d{4,5}[a-z]{0,4}$`. Every TE row has a non-empty NOTE matching
   `^\d{4,5}$`.
3. NOTE↔CCN consistency, for every row, the CCN portion of NOTE
   equals the value in the CCN column.
4. CCN-sheet-to-NOTE-vocabulary check, for each CCN calculation
   sheet `XXXXX` in the workbook, every suffix it COUNTIFS for must
   appear at least once in TO!NOTE (or be documented as legitimately
   zero for this unit).
5. Roll-up integrity, `UNIT_ROLLUP` H-column cells equal the
   `TOTAL REQUIREMENT` cell on each CCN sheet, with no `#REF!` or
   `#N/A`.
6. Billet accounting, number of billets in TO equals the sum of
   billets attributed across all CCN sheets (no double-counting, no
   orphans). The `61072` sheet in CLB-4 SW already documents this
   pattern: 84 in-scope + 156 excluded = 240 total, and the 156 must
   show up in their respective CCN sheets.
7. Equipment accounting, every TAMCN row in TE is referenced by
   exactly one CCN sheet (or explicitly zero), no orphans.

This harness should be a single tool, run on commit, that emits a
pass/fail report. That is what "airtight" looks like in practice.



## Definition of done, binding for every deliverable

A BFR produced by any operational mode is not done until all of
these acceptance tests hold. (Restated from `CLAUDE.md` so the contract
spec is self-contained.)

1. Cosmetic, matches `STYLE_GUIDE.md` (CLB-4 theme + Apex Omega
   4-color cell-role palette).
2. Recalc clean, zero `#REF!`, `#DIV/0!`, `#NAME?`, `#VALUE!`,
   `#N/A` after LibreOffice headless recalc (the recalc step is
   mandatory; openpyxl alone does not compute formulas).
3. Every CCN sheet computes, `TOTAL REQUIREMENT` evaluates to a
   real number traceable to a TFSMS/ASR input or FC 2-000-05N
   planning factor.
4. Roll-up integrity, every CCN's total flows to `UNIT_ROLLUP`
   exactly once. No dropped CCNs (the round-1 finding where 6 hidden
   CCN sheets were excluded from the 14,299 GSF roll-up cannot
   recur). No double counts.
5. All cross-references resolve, named ranges, sheet refs, and
   lookups all point at populated cells. No external links. No
   `#REF!` or `#N/A` in the defined-names list.
6. TFSMS reconciliation gate green, `TFSMS_UNRECONCILED = FALSE`;
   ASR-reconciled `PN_*` named ranges populated.
7. Personnel summaries populated and accurate, billet
   breakdowns by rank, by MOS, by MCC. Numbers tie to source TFSMS.
8. Equipment summaries by CCN populated and accurate, every
   TAMCN line maps to a CCN; counts tie to source T/E.
9. GSF / GSY totals consistent across detail tabs and roll-up.
10. Audit-traceable, every regulatory or numeric claim cited
    inline with source + section + date.

A deliverable that fails any one of these is `TBD, pending <failing
item>` per Apex Omega rule 4. Never silently release.

## Where this leaves us

The ground truth for the round-2 audit:

- Layer 1 holds (we understand the three formats).
- Layer 2 is broken, the NOTE column is essentially unpopulated
  across this entire repo.
- Layer 3 has no documentation, classification rules are implicit.
- Layer 4 is partially authored, the in-workbook TO/TE sheets
  exist but are missing the NOTE column data and (in CLB-4) the
  dimensional data on TE.
- Layer 5 is broken, legacy CCN sheets use brittle restricted-range
  lookups that have been broken for years; the four rebuilt CCN sheets
  bypass the lookup contract entirely by hardcoding counts.
- Layer 6 does not exist.

To restore an airtight, unit-agnostic pipeline, the work has a clear
order:

1. Lock down a canonical CCN+suffix vocabulary sourced from FC
   2-000-05N (this is the dictionary).
2. Lock down a classification rule set, the function from
   `(BIC, Billet Description, Alpha Grade, BMOS, PMOS, MCC, ...)` to
   a NOTE tag. This is the hardest deliverable; it requires unit
   doctrine knowledge.
3. Build an ETL tool that ingests Format A or Format C TO&E source
   data, applies the classification rule set, and emits Format B
   in-workbook TO/TE tabs ready to drop into a BFR template.
4. Build a canonical BFR template with Layer 5, compliant CCN sheets
   and a `UNIT_ROLLUP` that auto-collects them. This template should be
   unit-agnostic, cell references via named ranges, no hardcoded UICs.
5. Build the validation harness (Layer 6).
6. Drive every existing unit's BFR through the pipeline and reconcile.

I have not started any of this work. This document is the contract
specification only. Round 3 should pick one of these six tracks and
commit to a deliverable.
