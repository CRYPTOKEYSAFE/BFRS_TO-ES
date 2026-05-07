# 3d MED BN Doctrine Digest, 10 Documents

Apex Omega: facts only. Each section names the source, binding rules,
ratified decisions, defects, open TBDs, prior work done, and any
explicit don't-do directives.

## 1. CLAUDE.md (root)

Purpose. Project-level operating rules for the BFR audit / pipeline
effort. Binding methodology pointer to APEX_OMEGA.pdf, "if anything
conflicts, Apex Omega wins."

Binding rules.

- Apex Omega 9 non-negotiables: facts only; verify line/block/ref;
  current authoritative sources only; mark TBD pending source on
  unverifiable items; time-stamp citations; three-bucket fact
  separation (regulatory / program-practice / external); numbers
  traceable to a cited source; plain prose, lead with answer; no em
  dash, no en dash, no double-hyphen-as-em-dash, no asterisk bold,
  no dash separators for emphasis.
- Anti-patterns: speculation, stale citations, TFSMS as authoritative
  without ASR reconciliation, ERC vs PRV conflation, AI hedging,
  decorative content.
- Quality-check rituals before any deliverable: back-test, pressure-test,
  confirm publication status, verify primary sources, recalc spreadsheets
  zero error tokens, TFSMS-ASR reconciliation gate.
- Definition of done, 10 acceptance items: cosmetic per STYLE_GUIDE
  + Apex Omega 4-color palette; recalc clean (zero #REF!, #DIV/0!,
  #NAME?, #VALUE!, #N/A); every CCN sheet computes; roll-up integrity
  (every CCN flows once, no drops, no doubles); all cross-refs resolve,
  no external links; TFSMS gate green; personnel summaries; equipment
  summaries; GSF/GSY consistency; audit-traceable inline citations.
- Terminology lock: MCB Camp Butler / MCIPAC; never MCBJ, MCBB, or
  COMMARCORBASESJAPAN.
- Source workbooks never modified.
- Branch policy: per-session claude/* branch; never push main.

Defects surfaced. CLB-4 SW BFR rolls up only 4 visible CCN sheets to
14,299 GSF; 6 CCN sheets hidden and broken (14312, 14326, 21710, 21730,
44112, 45110). 156 of CLB-4's billets excluded from admin count, no
medical CCN. Pipeline NOTE column empty across the repo (Layer 2 broken).
TFSMS_UNRECONCILED gate at TFSMS_Loading!$D$19 was structurally broken
(merged cell incapable of holding value); now repaired.

Don't-do. Never treat TFSMS as authoritative without ASR reconciliation.
No IFERROR(...,"") top-level masking. No external links. No restricted-
range lookups. No 2017-era template residue. No emojis or decorative
content.

## 2. audit/PIPELINE.md

Purpose. Six-layer unit-agnostic pipeline contract spec.

Binding contract.

- Layer 1, three TO&E source formats: A (per-co TFSMS export),
  B (BFR-embedded TO/TE), C (Master MEF wide TFSMS), D (TFSMS / ASR
  PDF). All four must be ingestable; PDF needs page/table/row
  citation and TBD pending [page] when low-confidence.
- Layer 2, NOTE column carries CCN+suffix tag like 21710o, 44112w,
  14345a. Suffix vocabulary: o=office (>=E-6/officer, 120 SF/PN);
  c=cubicle (<=E-5, 60 SF/PN); w=warehouse worker (60 SF/PN, /3);
  rs/cs/ds/ws/shf/ms=section staffing; a=armory work-area; bare CCN
  on TE rows; 1=personal effects entitlement. Observed, not
  authoritative; FC 2-000-05N Appendix tables are the source of truth.
- Layer 3, classification rules from
  (BIC, Billet Description, Alpha Grade, BMOS, PMOS, MCC) -> NOTE tag.
- Layer 4, Format B in-workbook TO/TE schema. TO header on row 3:
  LINE | NOTE | CCN | CCN Description | UIC | Rec CD | BIC | Billet
  Description | Alpha Grade | BMOS | PMOS | chargeability cols.
  TE header on row 1: ROW | NOTE | CCN | CCN Description | CCN 21451
  Equipment Type | UIC | TAMCN Short | TAMCN | Nomenclature | TAM
  Stat | U/I | Rdy | Ind Qty | Org Qty | Unit T/E | L Ft | W Ft |
  H Ft | Volume Ea | Volume Total.
- Layer 5, stable lookup contracts. Full-column refs ('TO'!$B:$B),
  named-range constants (NTG=1.33, NSF_PER_OFFICE=120,
  NSF_PER_CUBICLE=60), no IFERROR top-level masking, no restricted
  ranges, traceable to one rolled-up cell per sheet.
- Layer 6, validation harness binding contract: (1) schema check,
  (2) NOTE coverage every TO row matches `^\d{4,5}[a-z]{0,4}$` and
  every TE row matches `^\d{4,5}$`; (3) NOTE-CCN consistency;
  (4) CCN-sheet-to-NOTE-vocab; (5) roll-up integrity (UNIT_ROLLUP H
  cells = each CCN's TOTAL REQUIREMENT, no #REF!/#N/A); (6) billet
  accounting (TO billet count = sum across CCN sheets, no double, no
  orphan); (7) equipment accounting (every TAMCN exactly one CCN or
  explicit zero).

Operational modes. Update-existing (BFR + new T/O&E -> updated BFR
plus diff report); Generate-new (T/O&E + metadata -> fresh BFR);
Audit-existing (BFR -> forensic findings + repair plan).

Defects. Layer 1 holds. Layer 2 broken across repo (NOTE column
empty). Layer 3 undocumented. Layer 4 partial. Layer 5 broken in
legacy CCN sheets. Layer 6 did not exist at PIPELINE.md writing
(now exists per HANDOFF as pipeline/validate.py at 8 PASS / 0 FAIL).

## 3. audit/FINDINGS.md

Purpose. Round-1 forensic findings on CLB-4 SW BFR, plus Round-3
gate finding 9 / 9b.

Findings still applicable to 3d MED BN.

- All BFRs descend from a 2017 NAVFAC MIDLANT template (Brunson, J,
  CIV); 9 years of accumulated debt.
- Defined-name pollution pattern: junk literals, #REF!, #N/A, test
  garbage; the 3d Med Bn benchmark has 44 names with similar junk
  including _lAQUETTAaRMORY, gfhgfhgf, Amroy, ghgghhg, mt.
- External-link contamination is structural for non-CLB-4 BFRs.
- Wrong-unit residue in mission statements is the rule, not the
  exception.

Ratified decisions. Round-3 gate fix (Sec 9b, 2026-04-30): Option A1
unmerge B19:O19; gate at D19 holds three-state formula
=IF(O37=0,"PENDING - ASR not yet provided", IF(O17=O37,"FALSE -
RECONCILED", "TRUE - UNRECONCILED")); ASR data section rows 26-37;
per-bucket diagnostic rows 39-51; PN_* family at row 37 mirrors
TFSMS_* at row 17; recalc verified 5,553 cells, zero error tokens;
fullCalcOnLoad=True set.

Don't-do. No silent fixes; structural changes need methodology-owner
direction.

## 4. audit/STYLE_GUIDE.md

Purpose. Binding cosmetic specification, extracted from the four
rebuilt clean CCN sheets in CLB-4 SW BFR (14345, 21451, 21455, 61072).

Sheet canvas (verbatim).

- Page orientation portrait, scale 84 percent, paper Letter (1),
  fit-to-page unset, print area $A$1:$AF$<last> typically $AF$36 or
  $AF$37, margins L=0.75 R=0.5 T=0.75 B=0.5 hdr=0.0 ftr=0.3.
- Footer odd-left: `\r# DISTRIBUTION: DoD COMMUNITY ONLY`. Header
  empty. Freeze panes none.
- Default row height 12.75. Default col width none (all explicit).
  Base col width 8. Sheet width 32 columns A-AF.

Column widths. A = 2.81640625 (left gutter narrow); B-AF default ~8;
AG, AH = 9.1796875 hidden by design.

Row heights. Rows 1-2 = 15.75 (title banner merged A1:AF2); row 3 =
30.75 (Installation/Tenant); row 4 = 14.5 (UICs/Planning Area);
row 5 = 15.75 (CCN/Nomenclature); row 6 = 28.5 (section banner);
row 7 = 14.5 (column headers); rows 8-35 = 12.75-15.75 (body);
row 37 = 12.75 (TOTAL REQUIREMENT).

Theme tints / fills.

- Title banner A1:AF2 = no fill (white).
- Section header banner A6:AF6 = theme=1, tint=-0.1499984740745262
  (~ light grey 15 percent darker than white).
- Sub-header / label cells (A7, A15, AB15, AB16) = same tint solid.
- Column-header cells (V7, Y7, AB7) = theme=1,
  tint=-0.0499893185216834 solid (~ very light grey 5 percent).
- Body cells = no fill.
- All borders thin, color indexed=64 (auto/black).

Fonts.

- Title A1: Calibri 16 bold, h=center, v=center.
- Section header A6: Calibri 11 bold, h=left, v=center, wrap.
- Sub-headers (A3, A4, A5, M3, M4, M5): Calibri 11 bold.
- Right-side labels (R3, F4, R4) populated unit data: Arial 10
  (paste-in convention; preserve).
- Column headers (V7, Y7, AB7): Calibri 10 bold, h=center.
- Body labels (A8 onward): Calibri 10, h=left, wrap=True.
- Body values (V8, Y8, AB8 onward): Calibri 10, h=center.
- TOTAL REQUIREMENT label (A37): Calibri 11 bold, top border thin.
- TOTAL REQUIREMENT value (H37): Calibri 10, h=center, v=center, wrap.
- Unit label (L37): Calibri 11 bold, top border thin.

Number formats. Counts and factors = General; subtotals = General or
#,##0; final GSF = #,##0; H37 = `#,##0\ "GSF"` or `#,##0\ "GSY"` for
yard CCNs (14312, 21455, 45110).

Merge skeleton (every CCN sheet, invariant).

```
A1:AF2    title banner ("BASIC FACILITY REQUIREMENTS WORKSHEET")
A3:E3     "Installation:" label
F3:L3     installation name
M3:Q3     "Tenant:" label
R3:X3     tenant unit name
A4:E4     "Installation UIC:" label
F4:L4     UIC value
M4:Q4     "Tenant UIC:" label
R4:X4     UIC value
Y4:AD4    "Planning Area: <area>"
A5:B5     "CCN:" label
C5:L5     CCN value
M5:Q5     "Nomenclature:" label
R5:AF5    CCN nomenclature
A6:AF6    section banner ("SPACE REQUIREMENT ANALYSIS, CCN xxxxx, UFC 2-000-05N ...")
A7:U7     sub-banner / column-block header
V7:X7, Y7:AA7, AB7:AF7   three numeric column headers (SF/Person, Count, NSF)
A8:U8 ... A15:AA15, A16:U16   body label spans + subtotal/total rows
AB15:AF15, AB16:AF16    value cells
A37:G37   "TOTAL REQUIREMENT:" merged
H37:K37   total value cell
L37:N37   unit label (GSF / GSY)
```

Apex Omega 4-color cell-role palette (verified verbatim from
STYLE_GUIDE).

| Role | Fill | Use |
|---|---|---|
| INPUT | #FFF8DC (cream) | TFSMS counts, vehicle counts, override flags, project metadata |
| CALC | #EAF3F4 (light teal) | NSF subtotals, factor multiplications, lookup results |
| OUTPUT | #DCE7C8 (light green) | Per-CCN GSF total, UNIT_ROLLUP H cells, TOTAL REQUIREMENT |
| WARNING / REVIEW | #F8E2D6 (light orange) | TFSMS-unreconciled flag, missing-loading flag, override-active flag |

Font discipline: Calibri or Arial only (no display fonts in body).

Don't-do. No bright tab colors (CLB-4 clean sheets all tab_color=None;
hidden broken sheets use FFFF0000, never adopt that). No
IFERROR(...,"") masking. No restricted-range lookups. No external
links. No defined names with #REF! or #N/A. No 2017-era template
residue.

## 5. audit/BFR_GENERATOR_NOTES.md

Purpose. Annotated tour of BFR_Generator_FC2-000-05N.xlsx, the
methodology + math reference.

Binding named-range API. Cover (PROJ_TITLE, INSTALLATION, BLDG_NO,
REGION, TENANT_UNIT, UIC, PLANNER, PROJ_DATE, PROG_FY at Cover!$D$6:$D$14).
TFSMS_* family at TFSMS_Loading!$D-$O$17 with TFSMS_TOTAL at $O$17 and
TFSMS_UNRECONCILED at $D$19. PN_OFF / PN_ENL / PN_CIV / PN_CTR /
PN_TOTAL / PN_MIL on Personnel!$C$28-$C$33. Okinawa adjustments
Okinawa_Navy_ACF (FY26 = 2.34 per UFS 3-701-01 Tbl 4-1),
Okinawa_Sust_ACF=2.1, Esc_Factor=1.0, Contingency=1.05, SIOH (per FY),
PD_Factor=1.09 (1.13 medical), HF TBD. BFR_CCN / BFR_NAME / BFR_UM /
BFR_REQ / BFR_OVR / BFR_NOTE on BFR_Calculator rows 7-20; CCN_TABLE on
CCN_Library!$C$6:$I$1100.

Decisions ratified. CCN_Library expanded 2026-04-28 to 1,060 entries
(1,059 from FC 2-000-05N Appendix A canonical extract source date
2019-06-27 plus 23 originally curated rows; 1 curated CCN
"143 13 Operational Vehicle/Equipment Canopy" preserved as net-new
since absent from 2019 catalog). Curated planning factors overlay
canonical title where both exist.

CCN format. `<3-digit-prefix> <2-digit-suffix>` space-separated
(`143 11`); CLB-4 SW sheet names use no space (`14311`); generator
must handle both.

Reconciliation gate. TFSMS_UNRECONCILED at TFSMS_Loading!$D$19 is THE
gate; render WARNING fill (#F8E2D6) when TRUE; final-output sheet
must refuse to display clean total while gate is TRUE, instead show
"TBD, pending ASR reconciliation".

## 6. audit/3DMEDBN_BASING_BRIEF.md

Purpose. Strategic basing summary for 3d Med Bn (all sources at
repo root; CG signed letter, Tabs A/B/C, MCIPAC endorsement docx,
email).

Key facts. Tenant 3d Medical Bn UIC M13020; Echelon II MCIPAC;
installation MCB Camp Butler, Okinawa. Subordinate UICs M28261 (H&S),
M28263 (Surg A), M28262 (Surg B). CG signed letter 2 Feb 2026:
711 personnel, consolidate at Camp Kinser. MT/UT and MSTC have
already physically moved to Kinser; rest of unit still at Camp
Foster. CG endorsement names buildings: 107 BN HQ co-use, 300 MSTC,
613 MT/UT, 400 armory bay, 1225 BEQ, 508 supply.

Three-doc reconciliation. Tab B v9 (Mar 25) = Surg Co B only,
Foster preferred, 180 PN. Tab C MCBB GF (Aug 25) = Surg Co B only,
Foster COA1, 181 PN. CG signed letter (Feb 26) = entire 3d Med Bn,
Camp Kinser, 711 PN. CG letter supersedes earlier Foster-leaning
analysis.

Open items needing person, not agent. TFSMS export for full 3d Med
Bn (or specifically Surg B as first worked example). Site walk of
Bldgs 107/300/613/400/1225/508 on Camp Kinser. Confirmation of right
Auto Org Shop CCN for medical-BN ground equipment (FC 2-000-05N
Series 200 narrative review). Engineer assigned per Kenji's
"(1) Planner and (1) Engineer" sizing.

Don't-do. Strategic basing is upstream of BFR; do not wait on
basing to scaffold the 3d Med Bn unit profile. 21410 "Combat
Vehicle Maintenance Shop" is questionable for medical battalion;
hold at confidence=low, render engineering-study warning, do not
silently fill (Apex Omega rule 4).

## 7. audit/3DMEDBN_BFR_REPAIR_PLAN.md

Purpose. Repair plan for `M67400-FO-M13020 3D MED BN-22NOV2024.xlsx`.

Cosmetic preservation. Same playbook as CLB-4; cosmetic stays as
is; only broken structure / cross-refs touched. Calibri 16/12/11/10;
green tabs (FF00B050) on visible CCN sheets; red tabs (FFFF0000) on
hidden broken sheets and UNIT_ROLLUP. A1 banner text retained.

Findings F1-F9.

- F1 (CRITICAL). UNIT_ROLLUP excludes 4 hidden CCN sheets (14312,
  21451, 21710, 45110); same defect as CLB-4 round 1.
- F2 (CRITICAL). 3,303 #N/A and 1 #VALUE! cached, root cause
  external [5]CCN! / [5]TAMCN! VLOOKUP residue.
- F3 (CRITICAL). Five external links: BULK_Storage_4 UNC, renel.douyon
  desktop, 1st MED BN M11020 May 2018, 2 LAAD MCICOM URL,
  flankspeed M13020 2029 TO E CUT.
- F4 (CRITICAL). 44 defined names; 28 #REF!, 2 #N/A, 14 junk
  literals; literal-as-value names EWC, HQ, TableName, TAOC, _Order1.
- F5 (CRITICAL). Personnel reconciliation: ASR 609 vs CG signed
  letter 711.
- F6 (CRITICAL). Mystery Surg Co C reference on sheet 45110 row 39
  (M28275); ASR has only Surg A (M28263) and Surg B (M28262).
- F7 (MAJOR). TO column 7 BIC encoding inconsistent.
- F8 (MAJOR). Surg Co B TFSMS export still shows Hawaii address.
- F9 (MAJOR). MISSION STATEMENT 306 rows + one #VALUE!.

Ratified user decisions D1-D6 (verbatim).

- D1. Personnel total. RESOLVED 2026-05-05: canonical planning total
  is 711 (CG signed letter, matching the HTML). The 609 ASR figure
  is the BIC-only structure number and is presented as a footnote
  inside the BFR for traceability. The 102-person delta (711 minus
  609) is most likely civilians, contractors, USN augmentees, or
  other non-BIC personnel that ASR does not carry. The BFR will not
  silently reconcile to 609; the cover and headline numbers use 711,
  with the ASR breakout cited.
- D2. Surg Co C. Confirm strip M28275 and Surg Co C references from
  the four hidden sheets during repair. (Per investigation findings,
  Surg Co C is not 3d MED BN, it is Camp Lejeune template residue.)
- D3. External links replacement strategy. Internal CCN_Library
  sheet (10 rows, internal scope) replaces `[5]CCN!` lookups; option
  (a) refined per Phase B ratified work.
- D4. Hidden CCN sheets treatment. Repair-and-unhide in place
  (preferred per CLB-4 lessons); not deleted, not left hidden.
- D5. Locator_Deck. Extract to separate workbook
  (`audit/reports/3dmedbn/locator_deck_extract.xlsx`) and remove
  from the BFR (orphan, referenced by no other sheet, 608 rows of
  hand-built TAMCN/location/PAL/QUAD data).
- D6. Phase ordering. A -> B -> C -> D -> E (structural triage,
  structural fixes, data reconciliation, validator, foundational-
  document delivery).

Don't-do explicit (Sec.6).

- Will not alter cosmetic of any green-tabbed CCN sheet.
- Will not change CCN sheet calc logic without FC citation.
- Will not delete hidden CCN sheets; repaired or rolled in.
- Will not silently fill TBD-pending items.
- Will not change personnel numbers in TO without TFSMS / ASR reconciliation.

Open items in plan. Phase D validator pass and Phase E foundational-
document delivery; Phase C-bis P2 (CCN 14312 = 0 GSF VLOOKUP IFERROR
fallback returns string "0" not number 0).

## 8. audit/3DMEDBN_BFR_INVESTIGATION_FINDINGS.md

Purpose. Forensic answers to user-asked Q1-Q5 before any repair.

Findings.

- Q1. Surg Co C is NOT 3d MED BN; it is Camp Lejeune template
  residue (2nd MED BN at M67001). Lineage: 2nd MED BN (Lejeune
  M67001) -> 1st MED BN (Pendleton M11020) on 04 MAY 2018 -> 3d MED
  BN (MCB Camp Butler M67400) on 22 NOV 2024. M28271/72/73/75 are
  the 2nd Med Bn UIC block, never relevant to 1st or 3d MED BN.
- Q2. Hidden CCN sheets are doctrinally relevant topics (14312
  laydown, 21451 auto org, 21710 comms maint marginal, 45110 open
  storage) but data inside each is wrong (wrong UICs, three of four
  still labeled MCB Camp Lejeune). Two repair options: rebuild with
  3d MED BN UICs (M28261, M28262, M28263), OR remove and let
  pipeline regenerate later.
- Q3. Dead VLOOKUPs total 3,307: 1,959 to `[5]CCN!$C$7:$D$1098` and
  1,348 to `[5]TAMCN!`. External target `M13020 2029 TO E CUT.xlsx`
  on flankspeed SharePoint. Repair: replace with internal
  CCN_Library and TAMCN_Library sheets sourced from
  audit/CCN_VOCABULARY.json (1,060 ratified CCNs).
- Q4. Locator_Deck is a 608-row orphan; referenced by zero
  formulas anywhere; keep / trim / remove all break nothing.
- Q5. Five external links; only link 5 ever carried live data; all
  five must be severed.

## 9. audit/3DMEDBN_PHASE_C_SCOPE.md

Purpose. Per-row retag mapping for Phase C, 170 rows, FC-cited.
Document does not edit BFR; awaiting per-bucket ratification.

FC source rows (current as of dates).

- 21820 Construction/Weight Handling Equipment Shop, FC 200-series
  16 May 2025 p.199; covers utility shops at HQBn / FSR / FMF
  Engineer Bn. 3d MED BN is none of these.
- 14312 Operational Vehicle Laydown Area, FC 100-series 11 Feb 2026
  p.189; matches towable gensets, towable pumps, ISO-container
  batch plants.
- 44112 Storage of Air or Ground Organic Units MC, FC 400-series
  19 Nov 2025 p.46; catch-all for unit organic storage.
- 45110 Open Storage Area, FC 400-series 19 Nov 2025 p.50; outdoor
  uncovered, sized in SY.
- 14345 Armory, FC 100-series 11 Feb 2026 p.205.
- 21451 Automotive Organizational Shop, FC 200-series 16 May 2025
  p.188.

Buckets pending ratification.

- A. 36 rows currently 21820, proposed retag 8 to 14312
  (genset/pump/containerized batch plant) and 28 to 44112
  (ECU/water tank/power dist panel/field bath/water purification/
  tool kit/analyzer).
- B. 129 rows currently `CSP` (TFSMS source-sheet placeholder, not
  a real CCN). Four policies: B-i all-44112; B-ii split (12 to
  14345, 7 to 45110, 110 to 44112) closest to FC convention; B-iii
  remove; B-iv defer with footnote. Agent's read is B-ii but will
  not commit without ratification.
- C. 5 rows cleared from #N/A; nomenclature-based retags: row 379
  E02122B MR PDO -> 14345; row 401 M00112B mod kit -> 21451; row
  426 C00102F small arms carrier -> 14345; row 461 E02012M
  suppressor -> 14345; row 478 C02182B decon kit -> 44112.
- D. 3 TFSMS COE TAMCNs missing per surg co. C00392B water filter
  add to TE qty 180 with CCN 44112; C02222F helmet ECH correctly
  absent and document; C02472Z M50 mask TBD pending verification of
  whether 3d MED BN COE TSC is `CBRN EQP COE`.
- E (downstream). After retags, 14312 picks up 8 first real TE
  rows; 45110 may pick up 7 from B-ii; UNIT_ROLLUP recomputes via
  fullCalcOnLoad.

Open TBDs. ERAA acronym TBD pending source. C02472Z M50 mask
chargeability TBD pending COE TSC verification. Phase C bucket A
36-row retag carries SME confirmation footnote (3d MED BN buildings
do not include a 21820-style utility shop).

Don't-do. Will not retag any of 170 rows without per-bucket choice;
will not delete TE rows (B-iii); will not add C00392B / C02472Z
without confirmation; will not silently fill ERAA/TSC.

## 10. audit/HANDOFF_NEXT_SESSION.md

Purpose. Self-contained primer for next session, repository state at
handoff.

Already done (do not redo).

- Validator pipeline/validate.py: 8 PASS / 0 FAIL on the BFR.
- LibreOffice headless recalc + GSF reconciliation (commit cd5738f).
- CG signed letter OCR'd this session (711 PN confirmed).
- Violations 1 and 3 partial close; Violation 3 corrected to Camp
  Kinser primary source.
- Strip placeholder narratives, match sheet convention.
- Reverted corrupt recalc; HANDOFF document added.
- CCN_Library 10-row internal sheet built (replaces external `[5]CCN!`).
- Locator_Deck extracted to separate workbook and removed from BFR.
- Cosmetic fingerprint preserved per STYLE_GUIDE.
- Apex Omega 4-color palette in use.

Per-CCN GSF state at handoff (post-recalc).

```
CCN     TOTAL                STATUS
14312       0.00 GSF         BROKEN, fix required
14345    6,110.08 GSF        OK
17110       0.00 GSF         DESIGN STUB (rolls to 17120)
17120    2,815.45 GSF        OK
21451    1,129.00 GSF        PARTIAL, equipment side returns 0
21710      583.32 GSF        PARTIAL, officers count 0
44112   46,182.74 GSF        OK
45110        8.89 GSF        BROKEN, factor and chain wrong
61072   69,875.00 GSF        QUESTIONABLE, sweeps clinical at admin rate
61073       0.00 GSF         CRITICAL, 574 billets routed, hardcoded zero
SUM    126,704.48 GSF        unreliable; defensible portion ~56,000 GSF
```

Open Apex Omega violations.

- Violation 1, PARTIAL. TE row 507 H&S C00392B FILTER WATER PURIFI
  qty 180 was same-battalion mirror of Surg A and Surg B; H&S TFSMS
  does not exist and will not exist; whole H&S TE side is 198
  inherited 2017 NAVFAC MIDLANT template rows; re-source all 198 is
  the real fix.
- Violation 2, OPEN. 574 clinical platoon billets routed to CCN
  61073 holding literal 0 in H40, and ALSO captured by 61072 rows
  27-29 at BN HQ admin rate of 162.5 SF per Marine inflating 61072
  to 69,875 SF. Fix: add FC Series 500 medical CCN to CCN_Library
  (likely 53010 Dispensary / Outpatient Clinic; verify against
  fc_2_000_05n_500series_03_17_2023.pdf), reroute clinical billets
  out of 61073 NOTE into the new Series 500 NOTE, remove the 61072
  sweep on those Marines.
- Violation 3, CLOSED. MISSION STATEMENT B208/B210/B211 now match
  postal-block convention (UNIT 38445 / FPO AP 963734500 /
  Country JP).
- Violation 4, OPEN. CG signed letter OCR'd; 711 PN confirmed; BFR
  has 710; reconcile 1-billet gap. Workspace requirement is in CG
  letter enclosure (2) "Proposed Facilities Layout" not directly
  identified in repo; candidates POM26 PDF, Tab B brief.

Per-CCN repair priority. P1 CCN 61073 = 0 with 574 billets routed;
P2 CCN 14312 = 0 (VLOOKUP IFERROR returns string "0" not 0); P3
CCN 45110 = 8.89 (R29 chain returns 0; verify 0.11111 SF-to-SY
conversion); P4 CCN 21451 equipment side = 0 (M28 = AB173 chain);
P5 CCN 21710 = 583 SF (officers count returns 0); P6 CCN 61072 =
69,875 SF (after Violation 2 fix should drop to ~6,337.5 SF for
39 BN admin Marines).

User's durable directives this session.

- 711 people in BN per CG signed letter (verified).
- "Every single tab the GSF everything must add up, not AI
  placeholder crap." No zero TOTALs masquerading as design, no
  bracketed TBDs in cell text, no unit-conversion bugs.
- "We are not stuck on where the unit is at right now ... we need
  the BFR correct so we can right size the unit into the proper
  facilities." BFR is a requirements doc, not a status tracker; do
  not put relocation narrative in MISSION STATEMENT.
- "No placeholder crap." Strip TBD-pending bracketed text from
  cells; flag in audit logs and commit messages, not in workbook.
- H&S TFSMS does not exist and will not exist; do not wait on it.
- Use ruflo for structural / multi-step work in next session.
- Stop chasing locations; BFR is the overarching document.
- Do not ask 90 questions at session start.

Don't-do. Never push to main. Do not run LibreOffice
-convert-to xlsx on the active BFR (corrupts for Excel even though
openpyxl reads it). Do not paper over a non-live ruflo by claiming
it works.

What to do first (no questions). (1) Run validator confirm 8 PASS /
0 FAIL; (2) read 44_gsf_findings.txt; (3) read
45_cg_letter_findings.txt; (4) start Violation 2 (Series 500 medical
CCN; FC citation before adding sheet); (5) work P2-P6 per priority;
(6) Violation 4 back-test against 711 PN.
