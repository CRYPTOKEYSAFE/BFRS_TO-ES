# BFR_Generator_FC2-000-05N.xlsx, Methodology Digest

Source file: /home/user/BFRS_TO-ES/BFR_Generator_FC2-000-05N.xlsx (133,383 bytes,
mtime 2026-05-05). Read with openpyxl 2026-05-06; formulas captured via
data_only=False, cached values absent (workbook has no Excel-side cache, so all
"v" came back None; this is normal for a workbook that has not been opened in
Excel/LibreOffice since edit). All cell references below are verified against
the file.

## Sheet roster (8 visible sheets, no hidden)

| # | Sheet | Dim | Purpose |
|---|---|---|---|
| 0 | Cover | B2:G42 | Project metadata + cell-color legend + authority list |
| 1 | TFSMS_Loading | B2:S51 | Per-UIC TFSMS paste area + ASR paste area + 3-state recon gate |
| 2 | Personnel | B2:I41 | Effective loading by category, source-switch (TFSMS vs Personnel input) |
| 3 | BFR_Calculator | B2:J33 | Per-CCN row (14 active rows) + 7-type vehicle sub-schedule |
| 4 | Inventory | B2:J20 | Required vs iNFADS existing, Surplus/Deficit, recommended action |
| 5 | Okinawa_Adj | B2:E27 | MILCON ACF, SIOH, PD, Esc, Contingency, HF + ATFP/seismic checklist |
| 6 | BFR_Summary | B2:J75 | Print-ready: project header, personnel, requirements, cost roll-up, narrative, endorsements |
| 7 | CCN_Library | B2:I1065 | 1,060 CCN rows (FC 2-000-05N Appendix A merged with 23 curated) |

## Defined-names API (52 names)

Cover metadata: PROJ_TITLE D6, INSTALLATION D7, BLDG_NO D8, REGION D9,
TENANT_UNIT D10, UIC D11, PLANNER D12, PROJ_DATE D13, PROG_FY D14.

TFSMS raw inputs (TFSMS_Loading row 17, summed from rows 8 to 15):
TFSMS_MAR_OFF D17, TFSMS_MAR_ENL E17, TFSMS_NAV_OFF F17, TFSMS_NAV_ENL G17,
TFSMS_OS_OFF H17, TFSMS_OS_ENL I17, TFSMS_RES_OFF J17, TFSMS_RES_ENL K17,
TFSMS_CIV L17, TFSMS_CTR M17, TFSMS_NC N17, TFSMS_TOTAL O17.

ASR-reconciled inputs (TFSMS_Loading row 37, summed from rows 30 to 36):
PN_MAR_OFF D37, PN_MAR_ENL E37, PN_NAV_OFF F37, PN_NAV_ENL G37,
PN_OS_OFF H37, PN_OS_ENL I37, PN_RES_OFF J37, PN_RES_ENL K37,
PN_CIV L37, PN_CTR M37, PN_NC N37, PN_TOTAL O37.

Note: PN_OFF / PN_ENL / PN_MIL point at the Personnel sheet (C28/C29/C33),
not TFSMS_Loading. Those are the source-switched effective loading values
(see Personnel sheet section).

Reconciliation gate: TFSMS_UNRECONCILED at TFSMS_Loading!D19.

Okinawa adjustments (Okinawa_Adj column C):
Okinawa_Navy_ACF C7, Okinawa_Sust_ACF C8, Esc_Factor C9, Contingency C10,
SIOH C11, PD_Factor C12, HF C13.

BFR_Calculator vectors (rows 7..20, 14 rows):
BFR_CCN B7:B20, BFR_NAME C7:C20, BFR_UM D7:D20, BFR_REQ H7:H20,
BFR_OVR I7:I20, BFR_NOTE J7:J20.

CCN library lookup: CCN_TABLE = CCN_Library!C6:I1100.

## Cover sheet, observed values

D7 "Camp Foster, Okinawa, JP". D9 "MCIPAC - 3d MLG / CLR-3".
D10 "CLB-4 (UIC M29110)". D11 "M29110 (CLB-4 - composite of M29111/12/13/14)".
References block lists FC 2-000-05N (11 Feb 2026), MCO 11000.12, MCO P11000.5x,
UFC 4-010-01, UFC 4-020-01, UFS 3-701-01, UFS 3-730-01, DoD RPCS / iNFADS.

## TFSMS_Loading three-state reconciliation gate

Cell D19 formula:
`=IF(O37=0,"PENDING - ASR not yet provided",IF(O17=O37,"FALSE - RECONCILED","TRUE - UNRECONCILED"))`

States:
1. PENDING (yellow) when no ASR has been pasted (O37 == 0).
2. FALSE - RECONCILED (green) when TFSMS total O17 equals ASR total O37; the
   BFR is releasable.
3. TRUE - UNRECONCILED (red) when O17 != O37; the BFR is not releasable.

Per-bucket diagnostics live in rows 41 to 51, columns B (label) C (TFSMS) D (ASR)
E (delta) F (status). For each personnel bucket the F-column status formula is
`=IF(<ASR>=0,"PENDING",IF(<TFSMS>=<ASR>,"OK","MISMATCH"))`. Buckets covered:
Marine Officer, Marine Enlisted, Navy Officer, Navy Enlisted, Other Service
Officer/Enlisted, Reserve/FAP Officer/Enlisted, Civilian, Contractor,
Non-Chargeable.

Rows 9 to 12 are pre-populated for the CLB-4 example with M29111 (12/60/2/11),
M29112 (3/55/0/0), M29113 (3/55/0/0), M29114 (4/79/6/17 + 3 NC). Total row 17
sums D8:D15 down each column. The user is intended to paste similar tables for
the engagement unit, then paste ASR-reconciled counts into rows 30 to 36.

## Personnel sheet

Source switch is at C4 ("TFSMS" string). Row 4 cell D4 is a warning formula:
`=IF(TFSMS_UNRECONCILED>0,"WARN "&TFSMS_UNRECONCILED&" TFSMS rows are NOT yet reconciled against the ASR ...","TFSMS data marked reconciled or not in use.")`

Rows 7 to 14 hold a manual (non-TFSMS) Personnel breakdown by staff section
(HQ/CE, S-3, S-2, S-4, S-6, Maint/MotorT, Med/Dental, Other). Columns C/D/E/F
are Officers/Enlisted/Civilians/Contractors. Total row 15 sums each column.

Effective-loading block (rows 27 to 33, the named ranges):
- C28 PN_OFF: `=IF($C$4="TFSMS",TFSMS_MAR_OFF+TFSMS_NAV_OFF+TFSMS_OS_OFF+TFSMS_RES_OFF,C15)`
- C29 PN_ENL: `=IF($C$4="TFSMS",TFSMS_MAR_ENL+TFSMS_NAV_ENL+TFSMS_OS_ENL+TFSMS_RES_ENL,D15)`
- C30 PN_CIV: `=IF($C$4="TFSMS",TFSMS_CIV,E15)` (named range PN_CIV at TFSMS_Loading!L37 supersedes; see note below)
- C31 PN_CTR: `=IF($C$4="TFSMS",TFSMS_CTR,F15)`
- C32 PN_TOTAL alias (named range points to TFSMS_Loading!O37, this cell is a parallel formula): `=IF($C$4="TFSMS",TFSMS_TOTAL,G15)`
- C33 PN_MIL: `=IF($C$4="TFSMS",TFSMS_MAR_OFF+TFSMS_MAR_ENL+TFSMS_NAV_OFF+TFSMS_NAV_ENL+TFSMS_OS_OFF+TFSMS_OS_ENL+TFSMS_RES_OFF+TFSMS_RES_ENL,C15+D15)`

Caveat: there is a named-range/cell-formula inconsistency. PN_CIV / PN_CTR /
PN_TOTAL are defined to point at TFSMS_Loading!L37/M37/O37 (ASR-reconciled
totals), while C30/C31/C32 on the Personnel sheet are formulas that read
TFSMS_CIV/TFSMS_CTR/TFSMS_TOTAL (raw TFSMS row 17). Downstream BFR_Calculator
and BFR_Summary cells use the named ranges (so they pull from row 37, the ASR
reconciled side). Personnel!C30:C32 is essentially a redundant display.

## BFR_Calculator

Header row 6: CCN | Facility Name | UM | Driver Qty | Factor | NTG | Required |
Total Required (UM) | Justification.

For each row r in 7..20: name pulls via VLOOKUP(B{r},CCN_TABLE,2,FALSE),
UoM pulls col 3, Required H{r}=`=IFERROR(E{r}*F{r}*G{r},0)`. The IFERROR is
on the multiply, suppressing #VALUE! when factor is text ("see notes").

Row mapping (CCN, driver, factor, NTG):
- r7  143 10 Emergency Vehicle Garage; E7=0, F7 blank, G7=1
- r8  143 11 Operational Vehicle Garage; E8=1, F8=`=BFR_Calculator!G33` (vehicle subschedule garage NSF total + 250 mech rm), G8=1.2
- r9  143 12 Operational Vehicle Laydown; E9=1, F9=`=BFR_Calculator!H33`, G9=1
- r10 143 24 EOD Facility; E10=1, F10=7204 (7000+204), G10=1
- r11 143 45 Armory; E11=`=PN_MIL`, F11 blank (planner enters per Table 14345-1), G11=1
- r12 143 46 Barracks; E12=0, F12 blank, G12=1
- r13 171 10 Academic Instruction; E13=0, F13=45, G13=1.33
- r14 171 20 Applied Instruction; E14=0, F14=150, G14=1.25
- r15 171 50 Indoor SA Range; E15=0, G15=1
- r16 173 10 Range Ops Bldg; G16=1
- r17 173 11 Range Support Bldg; G17=1
- r18 179 60 Parade & Drill Field; E18=`=PN_TOTAL`, F18=`=1/125`, G18=1
- r19 179 91 Confidence Course; E19=0, F19=1, G19=1
- r20 179 92 Obstacle Course; G20=1

Vehicle subschedule rows 26 to 32, types A through G, three columns: garage
NSF/EA, laydown GSY/EA, then computed totals. Per-type EA defaults:
A 108 NSF / 19 GSY, B 180/29, C 288/42, D 420/57, E 588/71, F 720/85, G 888/99.
Row 33 totals: G33=`=IF(SUM(G26:G32)=0,0,SUM(G26:G32)+250)` (adds 250 SF mech
room only when there are vehicles), H33=`=SUM(H26:H32)`.

## Inventory sheet

For each row matching BFR_Calculator (r7..r20 indexed against r7..r20):
Required E=`=IF(BFR_Calculator!I{r}="",BFR_Calculator!H{r},BFR_Calculator!I{r})`
(uses override if present, else computed). Existing F=G+H (Adequate + Inadequate).
Deficit/Surplus I=G-E (Adequate minus Required, so positive is surplus,
negative is deficit). Action J is text:
`=IF(I{r}<0,"NEW or RENOVATE - deficit of "&TEXT(ABS(I{r}),"#,##0")&" "&D{r},IF(H{r}>0,"REHAB - inadequate assets exist","NO ACTION - adequate"))`

## Okinawa_Adj, observed factor values

| Cell | Name | Value | Notes |
|---|---|---|---|
| C7 | Okinawa_Navy_ACF | 2.34 | "PAX Newsletter 3.2.1; updated annually. Applies to MILCON construction cost." |
| C8 | Okinawa_Sust_ACF | 2.1 | Sustainment ACF, UFS 3-701-01 §3-3 |
| C9 | Esc_Factor | 1 | "Set per program FY (UFS 3-730-01 Table 2). Update each FY." |
| C10 | Contingency | 1.05 | OCONUS contingency (UFS 3-730-01) |
| C11 | SIOH | 1.065 | "Supervision, Inspection & Overhead." OCONUS Japan |
| C12 | PD_Factor | 1.09 | "1.09 standard / 1.13 medical (UFS 3-701-01 Eq 3-1)" |
| C13 | HF | 1 | "1.05 if historic district." |

Direct answers to the questions asked:
- Okinawa_Navy_ACF for the workbook is 2.34 at Okinawa_Adj!C7. The cell label
  in B7 reads "MILCON Area Cost Factor (Okinawa, Navy)" and D7 cites PAX
  Newsletter 3.2.1, "updated annually." The cell does not itself say "FY26";
  the user (and the project briefing) treats 2.34 as the FY26 figure.
  Verification against current UFS 3-701-01 Table 4-1 is required at the time
  of release per Apex Omega Sec.5.5; this workbook hard-codes 2.34 and dates
  it implicitly to the workbook edit date (2026-04-28 per repo notes).
- SIOH for Okinawa is 1.065 at Okinawa_Adj!C11. No FY-specific override is
  built in; this is the OCONUS Japan SIOH used flat across all CCNs.
- ATFP / seismic / siting checklist (rows 17 to 27) is all "TBD" placeholder
  per Apex Omega rule 4. Items: UFC 4-010-01 standoff (controlled perimeter
  >=18 ft, within >=12 ft), UFC 4-020-01 DBT/LOP, UFC 4-010-01 Std 21 mass
  notification, UFC 4-023-03 progressive collapse, Japan seismic premium,
  typhoon/wind ASCE 7 + Okinawa Vult ~170 mph, host-nation FIP/SOFA,
  encroachment / IMP land-use, NEPA + Japan PA cultural survey, LEED Silver.

## Per-rank SF allowances

The methodology workbook does not embed per-rank SF allowances directly. The
admin sizing for 610 72 (Battalion HQ) and 610 73 (Company HQ) is delegated to
FC 2-000-05N rank-based tables; the workbook only carries the CCN library
descriptor and pulls SF via the planner-entered Driver Qty x Factor x NTG.
Per-rank GSF/PN values (officer, SNCO, junior enlisted) are not in this
workbook. They live in FC 2-000-05N Series 100 Tables 61072-1 and 61073-1
(extracted separately to audit/PLANNING_FACTORS.yaml). To adopt them in the
3d MED BN BFR, pull from PLANNING_FACTORS.yaml; do not invent.

## BFR_Summary cost roll-up (the per-CCN unit costs hard-coded in column F)

| CCN | $/UM | CCN | $/UM |
|---|---|---|---|
| 143 10 | 425 | 171 50 | 700 |
| 143 11 | 425 | 173 10 | 425 |
| 143 12 | 110 | 173 11 | 425 |
| 143 24 | 525 | 179 60 | 5,500 |
| 143 45 | 525 | 179 91 | 250,000 |
| 143 46 | 380 | 179 92 | 175,000 |
| 171 10 | 510 | | |
| 171 20 | 525 | | |

Per-row programmed cost J=`=G*H*I*Contingency*Esc_Factor*PD_Factor*HF` where
G=bare cost (deficit x $/UM), H=Okinawa_Navy_ACF, I=SIOH. Program total at J57
sums J43:J56. Note these unit costs are not cited; treat as placeholders and
override per UFS 3-730-01 historical cost data per project FY.

## CCN_Library schema

Header row 5, columns C through I (named range CCN_TABLE = C6:I1100, has
headroom for 35 future rows beyond the current 1,060):

| Col | Header | Meaning |
|---|---|---|
| C | CCN | 5-digit code in "NNN NN" form (space-separated, e.g. "143 11") |
| D | Facility Name | Per FC 2-000-05N Appendix A title |
| E | UM | Unit of Measure (SF, SY, AC, EA, LF) |
| F | Default Factor | Numeric or "see notes" string (planner-entered if blank) |
| G | Factor Notes / Formula | Free text, planning factor reference |
| H | NTG | Net-to-Gross ratio (numeric, multiplied into Required) |
| I | Driver Description | Plain-text driver definition |

Total populated rows: 1,060 (rows 6 through 1065). Of these, 23 are curated
with planning factors (cols F, G, H all populated), the remaining 1,037 are
canonical FC 2-000-05N Appendix A entries with only CCN, Name, UoM, and
Driver Description filled.

## Hard-coded planning factors for the requested CCNs

Quoted from CCN_Library (curated rows where present, cols D, E, F, G, H):

- 143 12 Operational Vehicle Laydown Area, SY, factor "see notes",
  notes "Per Table 14312-1 (Type A 19 GSY ... Type G 99 GSY).", NTG 1.0.
  Worked example present in BFR_Calculator r9 + vehicle subschedule rows 26..32.
- 143 45 Armory, SF, factor "see notes",
  notes "Per Table 14345-1 (1-2K strength: 576 GSF; >10K: +0.1 SF/PN).", NTG 1.0.
  Worked example present in BFR_Calculator r11; loading driver = PN_MIL.
- 214 51 (21451) AUTO ORGANIZATIONAL SHOP, SF; not curated, no factor/NTG/notes.
  Driver text only.
- 217 10 (21710) ELECNX/COMMS MAINT SHOP, SF; not curated.
- 441 12 (44112) STG AIR/GRD ORG UTS MARCOR, SF; not curated.
- 451 10 (45110) OPEN STORAGE AREA, SY; not curated.
- 530 10 (53010) DISP & OUT PATIENT CLINIC, SF; not curated.
- 540 10 (54010) DENTAL CLINIC, SF; not curated.
- 610 72 (61072) BATTLN SQUADRN HQ (MARCOR), SF; not curated.
- 610 73 (61073) COMPANY/BATTERY HQ(MARCOR), SF; not curated.

CCN 143 12 missing from the requested list (14312 corresponds to 143 12 in
this library's space-separated form). Note that the SW CLB-4 sheet name
"14312" does not match the library key "143 12"; the generator must
normalize (strip space when matching sheet to library).

Worked examples in BFR_Calculator are present for 143 10, 143 11, 143 12, 143 24,
143 45, 143 46, 171 10, 171 20, 171 50, 173 10, 173 11, 179 60, 179 91, 179 92.
There is no worked example in BFR_Calculator for any of the 21451, 21710, 44112,
45110, 53010, 54010, 61072, 61073 sheets requested. To size those CCNs for the
3d MED BN BFR, pull factors from FC 2-000-05N Appendix A directly (now extracted
to audit/CCN_VOCABULARY.json and audit/PLANNING_FACTORS.yaml).

## Adoption guidance for 3d MED BN BFR

1. Use the named-range API verbatim: PN_OFF, PN_ENL, PN_TOTAL, PN_MIL,
   Okinawa_Navy_ACF (2.34), Okinawa_Sust_ACF (2.1), SIOH (1.065),
   PD_Factor (1.09 std / 1.13 medical, set per CCN, 530 10 / 540 10 use 1.13),
   Contingency (1.05), Esc_Factor (set per FY26).
2. Implement the three-state recon gate (TFSMS_Loading!D19 logic) on the
   3d MED BN workbook so the BFR cannot release until O17 (TFSMS total)
   equals O37 (ASR total).
3. Adopt CCN_TABLE = CCN_Library!C6:I1100 lookups; do not use restricted
   ranges. Sheet-name to library-key normalization (strip space) is required.
4. For 530 10 (Dispensary/Outpatient Clinic) and 540 10 (Dental Clinic),
   override PD_Factor to 1.13 per UFS 3-701-01 Eq 3-1 (medical). The
   workbook currently uses a single PD_Factor cell for all CCNs; for medical
   facilities a per-row override is required.
5. The vehicle sub-schedule pattern (rows 25 to 33) is reusable for any unit
   with motor pool footprint, including 3d MED BN's medical vehicle laydown.
6. Per-CCN unit costs in BFR_Summary col F are placeholders ($425 SF for
   admin, $525 for armory, etc.) and must be replaced with project-specific
   estimates from a current UFS 3-730-01 historical cost reference.

## Apex Omega gaps in this workbook (TBD, pending resolution)

- ATFP / seismic / siting checklist all "TBD" (Okinawa_Adj rows 18..27).
- Per-rank SF allowances not in workbook; live in FC 2-000-05N Tables 61072-1,
  61073-1 (use audit/PLANNING_FACTORS.yaml, not invented values).
- 1,037 of 1,060 CCN library rows have no planning factor; must enrich from
  FC 2-000-05N Appendix A as needed (CLB-4 used 14 active rows; 3d MED BN's
  CCN list will hit 530 10, 540 10, 21451, 21710, 44112, 45110, 61072, 61073
  among others, which need factor backfill).
- Esc_Factor hard-coded to 1.0; must update to current FY26 escalation value
  per UFS 3-730-01 Table 2 at release.
- Personnel!C30:C32 formulas reference TFSMS row 17 (raw) while named ranges
  PN_CIV/PN_CTR/PN_TOTAL point at TFSMS_Loading row 37 (ASR-reconciled).
  This is an inconsistency; downstream consumers use the named ranges so the
  ASR-reconciled side wins, but the Personnel sheet display column is wrong
  when TFSMS != ASR. Repair before adopting.
