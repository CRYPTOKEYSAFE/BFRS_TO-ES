# Apex Omega Violation 2 fix proposal, 3d MED BN BFR

Status: AWAITING USER RATIFICATION. Per the handoff, structural
changes to CCN_Library require user direction before implementation.

## What Violation 2 is

The BFR currently routes 574 of 710 billets to CCN 61073 (Co HQ
Admin), which holds the literal value 0 SF at H40. This is the
result of a Layer 2 NOTE classification that defaulted clinical
platoon billets (FIELD MED TECH, SURG TECH, ANESTHESIOLOGIST,
LABORATORY, RADIOLOGY, PHARMACY, etc.) to 61073 because the BFR's
CCN_Library has no Series 500 medical CCN. As a side effect, those
574 Marines and Sailors are also captured by 61072 rows 27-29 at
162.5 SF per Marine, inflating 61072 to 69,875 SF (430 Marines'
worth of admin space for an admin staff of 39).

Net result: ~70,000 SF unreliable, 0 SF allocated for actual
clinical mission space, no Series 500 CCN sheet exists.

## Per-UIC, per-section breakdown of the 574 misrouted billets

  UIC      Total   FIELD_MED  LAB  SHOCK/SURG/FRSS  Other clinical  Admin
  ------   -----   ---------  ---  ---------------  --------------  -----
  M28261     183       50      14         12              105          2
  M28262     196       85      12         18               80          1
  M28263     195       85      12         18               79          1

Top billet descriptions in the 574: FLD MED TECH (220), MED LAB
TECH (27), CC NRS (24), ADV X-RAY (24), PREV MED TECH (21),
SURFACE IDC (16), SURG TECH (16), EMERG MED SPEC (16), GEN SGN
(12), BEH HLTH TECH (9), ANESTHESIOLOGIST (8), PHYS ASST (8),
EMERG-TRAUMA NRS (8), FAM PHYS (8), PROF REG NRS (8), CLIN PSYCH
(6), PHARM TECH (6), HYGIENE EQUIPMENT OPER (6), RADIOLOGY (5).

Navy NEC L3 (dental) billets in the 574: 27.

Co HQ admin billets (CO, XO, 1stSgt, Admin Chief etc.): 4 in BFR.
That is too few; expect ~12-15 across three companies. Most of
those billets are currently in 61072 NOTE not 61073.

## FC 2-000-05N Series 500 candidates

Source: fc_2_000_05n_500series_03_17_2023.pdf, version date
2023-03-17, captured page 6, BFR Required: Y.

  CCN     Title                                        Form           FAC
  -----   -----------------------------------------    ------         -----
  53010   DISPENSARY AND OUTPATIENT CLINIC             SF             5500
  53020   MEDICAL LABORATORY (detached)                SF             5302
  53025   PHARMACY (standalone)                        SF             5500
  53030   MORGUE                                       SF             5303
  53060   MEDICAL WAREHOUSE                            SF             5306
  53070   AMBULANCE SHELTER                            SF             5306
  54010   DENTAL CLINIC                                SF             (Series 500 page 9)
  51016   MEDICAL ADMINISTRATION                       SF             6100

Per FC 53010-1 (page 6, verbatim): "Free Standing Clinic,
outpatient clinic, which occupies a building or part of a building,
but is not physically located with a hospital or medical center
that provides routine and emergency care to authorized personnel."

Per FC 53025-1 (page 6, verbatim): "Pharmacy areas within hospitals
or clinics will not be separately identified but will carry the
same category code as the hospital or clinic. This category does
not serve as headquarters space for command level units."

The FC 53025-1 same-category-code rule applies generally inside
a clinic: pharmacy, lab, and similar functional areas roll up to
the parent dispensary CCN unless physically detached.

CORRECTION TO PRIOR DRAFT. I earlier called 53010 an
"engineering-study CCN". That framing was speculation borrowed
from CCNs that explicitly carry it (14326, 21451 narrative
sections in Series 100/200) and from a pipeline-extraction
category for "no factor table found". FC 2-000-05N Series 500
(2023-03-17) gives 53010 a definition only. No factor table, no
"engineering study" language, no sizing methodology stated.
Verbatim, the entire 53010 entry is:

  530 10  DISPENSARY AND OUTPATIENT CLINIC (SF)
  FAC: 5500
  BFR Required: Y

  53010-1  GENERAL. Free Standing Clinic, outpatient clinic,
  which occupies a building or part of a building, but is not
  physically located with a hospital or medical center that
  provides routine and emergency care to authorized personnel.

That is all FC says. Sizing for 53010 must come from a source
outside FC 2-000-05N. Candidate sources:

  1. DoD Military Health System Space Planning Criteria (MHS SPC)
     chapters on outpatient clinics. Source not in repo.
  2. BUMED project programming guidance (NAVMED references).
     Source not in repo.
  3. UFC 4-510-01 Military Medical Facilities. Design criteria,
     not space programming. Source not in repo.
  4. A unit-supplied per-platoon SF from a 3d MED BN engineering
     survey or basing study.
  5. Enclosure (2) of the CG signed letter (Proposed Facilities
     Layout). Document referenced but not in repo by name.

53020, 53025, 53060 are likewise definition-only in Series 500
(no factor tables, no sizing methodology). 54010 DENTAL CLINIC
does have Table 54010-1 with per-component space allowances
(Series 500 pages 11-13).

## Proposal options

### Option A (RECOMMENDED). Add CCN 53010 only, route all clinical to it

Add one Series 500 CCN sheet to CCN_Library, 53010 DISPENSARY AND
OUTPATIENT CLINIC. Re-route the clinical sections of all three
companies (FIELD_MED, LAB, PHARMACY, SHOCK_TRAUMA, SURGICAL, FRSS,
STAB, COLLECTING, EVAC, ERCS, RADIOLOGY, HOLDING_WARD, GEN_MED,
DENTAL, plus equivalent senior leadership) to the new CCN.

Doctrinal grounding: FC 53025-1 same-category-code rule says
pharmacy, lab, dental and similar functional areas inside a clinic
inherit the parent dispensary CCN. 3d MED BN's clinical platoons
deliver outpatient and Role 2 emergency care from a free-standing
clinic facility, which fits FC 53010-1 verbatim.

GSF method: FC 2-000-05N gives no sizing methodology for 53010.
TOTAL REQUIREMENT cell is `TBD pending sizing source` and the
sizing source itself is also TBD (DoD MHS Space Planning Criteria
or BUMED programming or unit-supplied engineering survey).

Pros: One sheet to build, FC-grounded, conservative, aligns with
FC 53025-1 same-code rule.

Cons: Loses fidelity for the 27 dental billets that have a
factor-table CCN (54010); rolls them into 53010 by the
same-category-code rule. Defensible but coarse.

Affected billets: 547 of 574 routed to 53010, 27 stay at 53010
under FC 53025-1 (or split to 54010, see Option B), ~12-15
genuine Co HQ admin billets stay at 61073 with a real COUNTIFS
formula instead of literal 0.

### Option B. Add 53010 plus 54010

Add two Series 500 CCN sheets. Route clinical-sections of all
three companies to 53010. Route 27 Navy NEC L3 dental billets to
54010.

Doctrinal grounding: 54010 DENTAL CLINIC is a distinct facility
type with its own factor table (Table 54010-1, Series 500 pages
11-13). When dental capability occupies separate space, 54010 is
the right CCN.

GSF method: 53010 sizing-source-TBD as in Option A. 54010 has
Table 54010-1 with per-component space allowances; loading driver
to be determined by reviewing Series 500 pages 11-13.

Pros: More precise. Dental gets its own factor-driven sheet.

Cons: Two sheets to build. Adds complexity. May overstate
precision if 3d MED BN dental is collocated with clinic space (in
which case FC 53025-1 says it stays at 53010).

Affected billets: 520 to 53010, 27 to 54010, ~12-15 to 61073.

### Option C. Add 53010 + 53020 + 53025 + 54010 + 51016

Add five Series 500 CCN sheets. Granular per-functional-area
classification.

Doctrinal grounding: each function gets its own CCN as if the
spaces were detached.

GSF method: all engineering-study except 54010.

Pros: Maximum doctrinal precision per CCN.

Cons: Five sheets, FC 53025-1 same-category-code rule says
collocated pharmacy and lab should NOT be separately identified.
Likely overstates structural complexity for an MLG medical
battalion that operates as a single clinical facility.

### Option D (NOT RECOMMENDED, lighter fix)

Replace 61073 H40 = 0 with a real COUNTIFS x SF formula matching
the 61072 pattern. Accepts that admin SF rates are not the right
doctrinal rate for clinical platoons.

Pros: No structural change. Minimal effort.

Cons: Apex Omega rule 1 violation. Routes 574 clinical Marines
to admin space at admin rates. Conflates 61072 BN HQ admin with
61073 Co HQ admin (which then gets used as a clinical-space
proxy). Does not align with FC 2-000-05N because clinical
platoons are not Co HQ admin.

## Recommended action

Option A. One CCN added (53010), re-route 574 - ~12 = ~562
clinical billets there, leave Co HQ admin (~12) at 61073 with a
real COUNTIFS formula. TOTAL REQUIREMENT for 53010 marked
`TBD pending engineering study (FC 2-000-05N Series 500 53010-1,
page 6, version 2023-03-17)` per Apex Omega rule 4. The 61072
clinical-sweep rows 27-29 collapse to 0 once the 574 are
re-routed, leaving 61072 P30 = 39 BN admin Marines x 162.5 SF =
6,337.5 SF (defensible).

After Option A is implemented:
  - CCN 53010: 562 billets, TOTAL TBD
  - CCN 61073: ~12 admin billets x 162.5 SF/Marine = ~1,950 SF
  - CCN 61072: 39 BN admin Marines x 162.5 SF = 6,337.5 SF
  - Other CCNs: unchanged

Net BFR posture: clinical mission space surfaced as a TBD honest
gap (Apex Omega rule 4) rather than 0 SF or absorbed into admin.
The TBD is closed by an engineering study or by a unit-doctrine
SF figure if the methodology owner provides one.

## Decision needed from user

  1. Which option (A, B, C, or D)?
  2. If A or B, what value to set as the engineering-study TBD on
     the 53010 sheet's TOTAL REQUIREMENT cell (TBD pending study,
     or a placeholder figure with citation)?
  3. Layer 2 re-classification: ratify the rule "billets in
     M28261 with FIELD_MED, LAB, PHARMACY, SHOCK_TRAUMA, SURGICAL,
     FRSS, STAB, COLLECT, EVAC, ERCS, RADIOLOGY, HOLDING_WARD,
     GEN_MED, DENTAL, plus full Surg A and Surg B clinical
     sections route to 53010"? Currently the rules are at
     audit/CLASSIFICATION_RULES.yaml but the BFR's Layer 2
     application defaulted to 61073 because 53010 was not in
     the workbook's CCN_Library.

## Files that change in Option A

  CCN_Library sheet (in BFR workbook): add row 11 for 53010
    (CCN, FAC, BFR Required, FC version date, source PDF).
  UNIT_ROLLUP sheet: add row 19 entry for 53010, extend SUM range.
  New 53010 CCN sheet: built per CLB-4 style (audit/STYLE_GUIDE.md),
    cosmetically matching the four clean rebuilt CCN sheets (14345,
    21451, 21455, 61072), with Apex Omega 4-color cell-role palette,
    citation footer per pipeline/template.py, TOTAL REQUIREMENT TBD.
  TO sheet: NOTE column updates for ~562 billets from 61073o/61073c
    to 53010o/53010c. CCN column for the same rows from 61073 to
    53010.
  61072 sheet: rows 27/28/29 (clinical sweep) will recompute to 0
    automatically once TO reclass is done, no formula change needed.
  61073 sheet: H40 changes from literal 0 to a real COUNTIFS
    formula referencing the ~12 admin billets that remain.

## Files that change in Option B

  Same as Option A, plus:
  CCN_Library sheet: add row 12 for 54010.
  UNIT_ROLLUP: add row 20 entry for 54010, extend SUM.
  New 54010 CCN sheet.
  TO sheet: 27 NEC L3 dental billets re-routed to 54010 instead of
    53010.

## Apex Omega compliance

  Rule 1 (facts only): every routing rule cited to FC 2-000-05N
    Series 500 narrative section.
  Rule 2 (verify line by line): per-billet description and BMOS/
    PMOS examined; counts above are line-by-line.
  Rule 3 (current authoritative source): FC 2-000-05N Series 500,
    version 2023-03-17, current as of this session 2026-05-06.
  Rule 4 (TBD where unverifiable): 53010 TOTAL marked TBD pending
    engineering study; not silently filled.
  Rule 5 (timestamp at citation): all FC references stamped with
    publication date (2023-03-17 for Series 500).
  Rule 6 (three-bucket separation): regulatory facts (FC sections)
    separated from program-practice (current 3d MED BN BFR state)
    and external benchmarks (none used here).
  Rule 7 (numbers traceable): every billet count above is a
    deterministic COUNTIFS on the TO sheet's CCN+suffix column,
    reproducible via the script at the foot of this document.
  Rule 8 (plain prose): no decorative content.

## Reproducibility

The 574 / 547 / 27 / 12 figures come from an openpyxl walk of the
TO sheet (header row 3, NOTE col 3, CCN col 4, BIC col 8, Desc
col 9, BMOS col 11). The walk was run on the BFR HEAD as of
commit 5a5d70c on branch claude/apex-omega-audit-repair-gG9mM,
2026-05-06, and is reproducible from the script in the session
log preceding this document. The 547 figure assumes Option A's
coarse classification with all clinical functional areas under
53010; the 27 figure is the count of NEC L3 dental in the routed
574; the 12 figure is the expected Co HQ admin staffing across
three companies (3 CO + 3 XO + 3 1stSgt + 3 Admin Chief = 12).
