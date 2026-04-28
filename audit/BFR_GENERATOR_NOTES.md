# BFR_Generator_FC2-000-05N.xlsx, Annotated Tour

This document is a structural reference for the methodology workbook
`BFR_Generator_FC2-000-05N.xlsx` (uploaded by the owner on
2026-04-28). It applies Apex Omega via TFSMS-to-ASR reconciliation gates
and FC 2-000-05N Series 100 enforcement. It is the methodology +
math reference. CLB-4 SW BFR is one observed example unit (there is
no gold standard in this domain); see `STYLE_GUIDE.md` for the cosmetic
typography extracted from it. Structural patterns derive from
FC 2-000-05N planning factor tables plus unit doctrine, not from any
single example unit.

Source evidence: `audit/reports/14_BFR_Generator.inventory.txt`.



## Sheet roster

| # | Sheet | Purpose |
|---|---|---|
| 0 | `Cover` | Project metadata: title, UIC, building no., installation, region, tenant unit, planner, project date, programmed FY. Authority list (FC, MCO, UFC, UFS) cited in references block. (No DD 1391 field, DD 1391s are downstream MILCON project documents informed by the BFR but not part of it.) |
| 1 | `TFSMS_Loading` | TFSMS RecapMCC raw input, by personnel category. Carries the `TFSMS_UNRECONCILED` flag at `D19`, the gate. |
| 2 | `Personnel` | ASR-reconciled personnel loading. Final `PN_*` named ranges flow from this sheet. References *FC 2-000-05N Sec.61010-3* (personnel loading authority). |
| 3 | `BFR_Calculator` | Per-CCN row-driven BFR. One row per CCN; columns: CCN, Description, UoM, Loading, Factor, Required, Override, NOTE. Vectorized via `BFR_*` named ranges. |
| 4 | `Inventory` | Inventory-vs-required comparison (gap analysis), keyed off `BFR_Calculator` row indices. |
| 5 | `Okinawa_Adj` | Okinawa-specific adjustments: MILCON ACF, Sustainment ACF, Escalation, Contingency, SIOH, PD Factor, ATFP / seismic / typhoon checklist (with `TBD` placeholders for unverified items per Apex Omega rule 4). |
| 6 | `BFR_Summary` | Final per-CCN summary. Pulls Loading/Factor/Required from `Inventory`, applies Okinawa adjustments, emits the final SF (or SY) by CCN. |
| 7 | `CCN_Library` | The canonical CCN dictionary. Columns: CCN, Facility Name, UoM, Default Factor, Factor Notes, NTG, Driver Description. Expanded 2026-04-28 (Layer 5) to 1,060 entries, 1,059 from the FC 2-000-05N Appendix A canonical extract (`audit/CCN_VOCABULARY.json`, source date 2019-06-27) merged with the 23 originally curated rows; one curated CCN ("143 13 Operational Vehicle/Equipment Canopy") is preserved as net-new since it is not present in the 2019 generation of the catalog. Curated planning factors (Default Factor, Factor Notes, NTG, Driver Description) overlay the canonical title where both exist. |



## Named-range API (the contract surface)

A generator that produces a BFR workbook in this lineage must
preserve these names and their cell coordinates so downstream formulas
work. They are the public API.

### Cover-sheet metadata

| Name | Cell | Meaning |
|---|---|---|
| `PROJ_TITLE` | `Cover!$D$6` | Project title |
| `INSTALLATION` | `Cover!$D$7` | Installation (e.g. MCB Camp Butler) |
| `BLDG_NO` | `Cover!$D$8` | Building number |
| `REGION` | `Cover!$D$9` | Region (e.g. Okinawa, Japan) |
| `TENANT_UNIT` | `Cover!$D$10` | Tenant unit name |
| `UIC` | `Cover!$D$11` | UIC |
| `PLANNER` | `Cover!$D$12` | Planner |
| `PROJ_DATE` | `Cover!$D$13` | Project date |
| `PROG_FY` | `Cover!$D$14` | Programmed FY |

### TFSMS raw inputs (per personnel category)

| Name | Cell | Meaning |
|---|---|---|
| `TFSMS_MAR_OFF` | `TFSMS_Loading!$D$17` | Marine Officer billets |
| `TFSMS_MAR_ENL` | `TFSMS_Loading!$E$17` | Marine Enlisted billets |
| `TFSMS_NAV_OFF` | `TFSMS_Loading!$F$17` | Navy Officer billets |
| `TFSMS_NAV_ENL` | `TFSMS_Loading!$G$17` | Navy Enlisted billets |
| `TFSMS_OS_OFF` | `TFSMS_Loading!$H$17` | Other Services Officer billets |
| `TFSMS_OS_ENL` | `TFSMS_Loading!$I$17` | Other Services Enlisted billets |
| `TFSMS_RES_OFF` | `TFSMS_Loading!$J$17` | Reserve Officer billets |
| `TFSMS_RES_ENL` | `TFSMS_Loading!$K$17` | Reserve Enlisted billets |
| `TFSMS_CIV` | `TFSMS_Loading!$L$17` | Civilian billets |
| `TFSMS_CTR` | `TFSMS_Loading!$M$17` | Contractor billets |
| `TFSMS_NC` | `TFSMS_Loading!$N$17` | Non-chargeable billets |
| `TFSMS_TOTAL` | `TFSMS_Loading!$O$17` | TFSMS row total |
| `TFSMS_UNRECONCILED` | `TFSMS_Loading!$D$19` | Reconciliation gate flag. When `TRUE`, the BFR is not releasable. Apex Omega Sec.6 anti-pattern: never treat TFSMS as authoritative without ASR reconciliation. |

### ASR-reconciled personnel (Personnel sheet)

| Name | Cell | Meaning |
|---|---|---|
| `PN_OFF` | `Personnel!$C$28` | Officers (reconciled) |
| `PN_ENL` | `Personnel!$C$29` | Enlisted (reconciled) |
| `PN_CIV` | `Personnel!$C$30` | Civilians (reconciled) |
| `PN_CTR` | `Personnel!$C$31` | Contractors (reconciled) |
| `PN_TOTAL` | `Personnel!$C$32` | Total PN for BFR loading |
| `PN_MIL` | `Personnel!$C$33` | Military total (Off + Enl) |

These flow into `BFR_Calculator` Loading column (col E). Sample:
`'BFR_Calculator'!E11 = =PN_MIL` for CCN `143 45` (Armory),
`'BFR_Calculator'!E18 = =PN_TOTAL` for CCN `179 60`.

### Okinawa adjustment factors

| Name | Cell | Default | Source |
|---|---|---|---|
| `Okinawa_Navy_ACF` | `Okinawa_Adj!$C$7` | (per FY) | UFS 3-701-01 Table 4-1 (FY26 = 2.34 per Apex Omega briefing) |
| `Okinawa_Sust_ACF` | `Okinawa_Adj!$C$8` | 2.1 | UFS 3-701-01 Sec.3-3 (Sustainment ACF) |
| `Esc_Factor` | `Okinawa_Adj!$C$9` | 1.0 | UFS 3-730-01 Table 2, set per program FY |
| `Contingency` | `Okinawa_Adj!$C$10` | 1.05 | UFS 3-730-01 OCONUS contingency |
| `SIOH` | `Okinawa_Adj!$C$11` | (per FY) | Supervision, Inspection, and Overhead |
| `PD_Factor` | `Okinawa_Adj!$C$12` | 1.09 | UFS 3-701-01 Eq 3-1 (1.09 standard, 1.13 medical) |
| `HF` | `Okinawa_Adj!$C$13` | (TBD) | Hazard / typhoon factor (verify per project) |

### BFR Calculator vectors

| Name | Range | Meaning |
|---|---|---|
| `BFR_CCN` | `BFR_Calculator!$B$7:$B$20` | CCN identifier per row (format `143 11`, `171 10`, etc.), current cap is 14 active rows; per-unit projects with more CCNs use the Track B template generator instead |
| `BFR_NAME` | `BFR_Calculator!$C$7:$C$20` | Looked up from `CCN_TABLE` |
| `BFR_UM` | `BFR_Calculator!$D$7:$D$20` | Unit of measure (SF / SY) |
| `BFR_REQ` | `BFR_Calculator!$H$7:$H$20` | Computed required quantity |
| `BFR_OVR` | `BFR_Calculator!$I$7:$I$20` | Override (if planner overrides the calc) |
| `BFR_NOTE` | `BFR_Calculator!$J$7:$J$20` | Per-row note / justification |
| `CCN_TABLE` | `CCN_Library!$C$6:$I$1100` | The lookup library, expanded 2026-04-28 (Layer 5) to cover the 1,060-CCN merged dictionary plus headroom |



## CCN Library (FC 2-000-05N keyed dictionary, observed entries)

Format: `<3-digit-prefix> <2-digit-suffix>` (space-separated; e.g.
`143 11`, not `14311`). Sheet names in the CLB-4 SW workbook use no
space (`14345`, `21451`); the library uses spaces. Generator must
handle both.

| CCN | Name | UoM | Default factor / NTG | Loading basis |
|---|---|---|---|---|
| `141 70` | Air Traffic Control Tower | SF | 2956 SF base, NTG 1.1 | Each tower |
| `143 10` | Emergency Vehicle Garage | SF | NTG 1.05 | Sum of vehicle plan-areas + 3 ft clearance/side |
| `143 11` | Operational Vehicle Garage | SF | NTG 1.2 | Per Table 14311-1 (Type A 108 NSF ... Type G 888 NSF) + 250 SF mech rm |
| `143 12` | Operational Vehicle Laydown Area | SY | NTG 1.0 | Per Table 14312-1 (Type A 19 GSY ... Type G 99 GSY) |
| `143 13` | Operational Vehicle/Equipment Canopy | SF | NTG 1.0 | Vehicle/equip area + circulation (drip line) |
| `143 24` | Marine Corps EOD Facility | SF | 7000 SF + 204 SF Haz/Flam, NTG 1.0 | Each EOD facility |
| `143 26` | Marine Corps EOD Company Facility | SF | NTG 1.4 | NSF per function x NTG (Admin 1,910 SF; classrooms via 171 10) |
| `143 45` | Armory | SF | NTG 1.0 | Per Table 14345-1 (1, 2K strength: 576 GSF; >10K: +0.1 SF/PN). Loading = `PN_MIL` |
| `143 46` | Marine Barracks - General Purpose | SF | NTG 1.0 | Per Table 14346-1 (1, 50: 75 GSF/PN; 201+: +30 GSF/PN) |
| `143 47` | Alert Force Building | SF | NTG 1.0 | Engineering analysis |
| `171 10` | Academic Instruction Building | SF | 45 GSF/student, NTG 1.33 | Per Table 17110-1 |
| `171 15` | Navy/Marine Corps Reserve Training | SF | NTG 1.3 | NOSC Space Program Spreadsheet (Tables 17115-1...9) |
| `171 20` | (continues, full dump in inventory report) | | | |
| `171 50` | | | | |
| `173 10` | | | | |
| `173 11` | | | | |
| `179 60` | | | | Loading = `PN_TOTAL`, factor = `1/125` |

(The library covers rows 6 through 28 of `CCN_Library`. Full enumeration
will be added when the canonical FC 2-000-05N CCN vocabulary is
extracted in the next round.)



## Reconciliation gate (the most important methodology element)

`TFSMS_UNRECONCILED` at `TFSMS_Loading!$D$19` is the gate. The
generator should:

1. Compute it as `=NOT(<sum of reconciled categories on Personnel> = <sum of TFSMS categories>)` or equivalent invariant.
2. Render it with the Apex Omega WARNING fill (`#F8E2D6`) when `TRUE`.
3. Have any final-output sheet refuse to display a clean total while
   `TFSMS_UNRECONCILED = TRUE`, instead, show
   `"TBD, pending ASR reconciliation"` per Apex Omega rule 4.

This is the operational implementation of Apex Omega Sec.5.6:
*"TFSMS RecapMCC personnel data must be reconciled against the unit's
authoritative ASR / T/O&E before a BFR can be released."*



## Synthesis, how this maps to the unit-agnostic pipeline

| Layer (per `PIPELINE.md`) | BFR Generator implementation |
|---|---|
| 1. Source format awareness | `TFSMS_Loading` accepts Format A/C raw counts directly |
| 2. CCN+suffix tagging | Bypassed, the BFR Generator uses row-per-CCN with `Loading` from named ranges, not COUNTIFS-on-NOTE. This is the cleaner approach for top-level summary. |
| 3. Classification rules | Embedded in the `Loading` formula per CCN row (e.g. `=PN_MIL` for armory; `=PN_TOTAL/125` for one-stall-per-125-PN heads) |
| 4. In-workbook TO/TE schema | Not present, the BFR Generator summarizes; it does not carry the TO/TE roster. The pipeline will need to attach Format-B TO/TE if the user wants per-billet traceability beyond the named-range loading. |
| 5. Stable lookup contracts | Compliant, uses `VLOOKUP` against `CCN_TABLE` named range, no restricted ranges. `IFERROR(...,"")` is used but only on the lookup's "name" column, not on the math; the math itself surfaces `#REF!` / `#DIV/0!` if inputs are missing. |
| 6. Validation harness | Partial, `TFSMS_UNRECONCILED` flag is the seed; full harness (schema check, NOTE coverage, roll-up integrity) still to build. |

The two reference workbooks are complementary, not redundant:

- BFR Generator = methodology, math, named-range API, Okinawa
  adjustments, reconciliation gate.
- CLB-4 SW = cosmetic, multi-section CCN-tab structure with
  per-billet traceability via TO/TE.

A merged generator should produce, per BFR project:

1. A summary workbook in BFR Generator form (Cover + TFSMS_Loading +
   Personnel + BFR_Calculator + Okinawa_Adj + BFR_Summary + CCN_Library)
  , for high-level deliverable.
2. A detail workbook (or detail tabs in the same workbook) in
   CLB-4-SW form (one CCN tab per CCN with multi-section calc and
   per-billet TO/TE backing), for audit traceability.
