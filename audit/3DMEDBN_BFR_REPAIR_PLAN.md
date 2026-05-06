# 3d MED BN BFR Repair Plan

Source workbook: `M67400-FO-M13020 3D MED BN-22NOV2024.xlsx`
Audit reports: `audit/reports/3dmedbn/`
Methodology: Apex Omega (facts only, every claim sourced inline, no
silent fixes).

## 1. What this BFR is

A 3d Medical Battalion Basic Facility Requirements workbook dated
22 Nov 2024. Naming convention `M67400-FO-M13020` follows the same
project-prefix / unit-UIC pattern as CLB-4's
`FO_M29030_CLB 4_FINAL BFR.xlsx`. M13020 is the 3d MED BN UIC.

Cosmetic fingerprint matches the CLB-4 BFR:
- Calibri font, sizes 16 (workbook title), 12 (totals), 11
  (section labels), 10 (data)
- Visible CCN sheets carry green tab color (FF00B050)
- Hidden / broken CCN sheets carry red tab color (FFFF0000)
- UNIT_ROLLUP carries red tab (top-level workbook entry point)
- Same merged-cell skeleton, same A1 banner text "BASIC FACILITY
  REQUIREMENTS WORKSHEET"

This means the repair work follows the same playbook as CLB-4 and
the cosmetic stays exactly as is. Only broken structure and broken
cross-references get touched.

## 2. Sheet inventory (15 sheets)

| Sheet | State | Tab | Role |
|---|---|---|---|
| UNIT_ROLLUP | visible | red | top-level rollup |
| MISSION STATEMENT | visible | none | mission text |
| TO | visible | none | personnel table of organization |
| TE | visible | none | table of equipment |
| Locator_Deck | visible | none | TAMCN/location lookup |
| 14312 | hidden | red | Operational Vehicle Laydown Area |
| 14345 | visible | green | Armory |
| 17110 | visible | green | Academic Instruction Building (stub, rolled to 17120) |
| 17120 | visible | green | Applied Instruction Building |
| 21451 | hidden | red | Automotive Organizational Shop |
| 21710 | hidden | red | Electronic / Communications Maintenance Shop |
| 44112 | visible | green | Storage of Air or Ground Organic Units, USMC |
| 45110 | hidden | red | Open Storage Area |
| 61072 | visible | green | Battalion / Squadron HQ, MC |
| 61073 | visible | green | Company / Battery HQ, MC (stub, rolled to 61072) |

**This is the same defect pattern as CLB-4 SW BFR (see
`audit/FINDINGS.md`):** the visible green sheets are clean rebuilds;
the hidden red sheets are 2017 NAVFAC MIDLANT template residue with
broken lookups, IFERROR masking, and external-link contamination.

## 3. Findings by severity

### CRITICAL (blocks foundational document status)

#### F1. UNIT_ROLLUP excludes hidden CCN sheets

UNIT_ROLLUP has 6 CCN rows and references only the visible green
sheets:
- 14345 Armory
- 17110 Academic Instruction (rolled to 17120)
- 17120 Applied Instruction Building
- 44112 Storage of Air or Ground Organic Units
- 61072 Battalion HQ
- 61073 Company HQ (rolled to 61072)

The four hidden CCN sheets (14312, 21451, 21710, 45110) exist with
calculations, are referenced in the TO and TE NOTE columns, but do
not flow to UNIT_ROLLUP. This is the same finding as CLB-4 round 1:
hidden CCN sheets dropped from the rollup, total understated.

Source: `audit/reports/3dmedbn/01_bfr_inventory.txt`, UNIT_ROLLUP
section showing 6 ccn-like rows; hidden sheets 14312/21451/21710/
45110 confirmed present.

#### F2. 3,303 #N/A and 1 #VALUE! cached error tokens

| Sheet | #N/A | #VALUE! |
|---|---|---|
| TO | 466 | 0 |
| TE | 2,837 | 0 |
| MISSION STATEMENT | 0 | 1 |

Root cause: TO and TE rely on VLOOKUP into external file
references (`[5]CCN!$C$7:$D$1098` style). Source:
`audit/reports/3dmedbn/02_bfr_error_tokens.txt`.

Per Apex Omega Sec.5.5: zero error tokens after recalc is required
before the BFR is releasable. This is the second-largest blocker.

#### F3. Five external-link contaminations

Per `audit/reports/3dmedbn/01_bfr_inventory.txt`:
- `\\naeanrfkfs43\BULK_Storage_4\Users\p0047813\...\Master Asset (2).xls`
- `C:\Users\renel.douyon\Desktop\Copy of 19Marine Air Support Squadron_advocate review (002).xlsx`
- `\\mcuspndlfs44\CPEN_GF\cpen_pwd\IR TEAM OASIS\BFR\1stMED BN BFR 2025\1ST MED BN M11020_BFR UNIT EDIT_04MAY2018.xlsx`
- `https://mcicom.usmc.mil/MCICOM_IR_OPT/Standard BFRs/2 LAAD/M00146-MS-M19885-20161222.xlsx`
- `https://flankspeed-my.sharepoint-mil.us/...M13020 2029 TO E CUT.xlsx`

The 2018 1st MED BN BFR link confirms this workbook descends from
the 1st MED BN BFR template (Camp Pendleton, May 2018). Same
template lineage as CLB-4 traces back to 2017 NAVFAC MIDLANT.

Per `audit/PIPELINE.md` Layer 5: "no external links" is a contract
requirement. All five must be severed.

#### F4. 44 defined names; 28 broken (`#REF!`), 2 `#N/A`, 14 junk literals

The defined-names list is corrupt:

Garbage names: `_lAQUETTAaRMORY`, `gfhgfhgf`, `ghgghhg`, `Hello`,
`HELLO1`, `heloo`, `dd`, `DDD`, `delete1`, `gsg`, `mt`, `oc`, `sds`,
`x`, `a`, `d`, `new`, `Amroy`, `Ordnance`, `GDSGSDG`, `IN_ins`,
`TE_2`, `TE_3`, `TE_orignial`, `te_table`, `_17120Ne`, `_17120new`,
`_17945`, `_2145NEW`, `_21451_UIC`, `_21451New`, `_21451NewTab`,
`_MY`, `Recover`, `CostCode`.

Literal-as-value names (these store strings, not refs):
- `EWC` -> `'M00873'`
- `HQ` -> `'M00871'`
- `TableName` -> `'Dummy'`
- `TAOC` -> `'M00872'`
- `_Order1` -> `'255'`

External-file refs:
- `Recover` -> `[1]Macro1!$A$206`
- `UIC_HQ` -> `'[3]14312'!$C$51`
- `UIC_HS` -> `'[4]14312'!$C$96`

Per Apex Omega Sec.5: zero `#REF!` and zero `#N/A` in defined names
is required before release.

#### F5. Personnel reconciliation discrepancy: ASR 609 vs CG signed letter 711

ASR (`3DMLG_ASR.xlsx`, sheet `3D MED BN`) FY26 BICs:
- H&S Co 3d MED BN: 250
- Surg Co A 3d MED BN: 179
- Surg Co B 3d MED BN: 180
- **Total: 609** (sheet R207 Grand Total = 609)

CG 3d MLG signed letter dated 2 Feb 26 para 5a: Personnel 711.

Delta: 102 personnel unexplained. Possible sources:
- Civilians or contractors (ASR is BIC-only)
- 1CP grouping (ASR shows "1CP" = 429 separately, possibly a sub-
  count of the 609 not adding to 711 either)
- USN augmentees not in ASR
- Forward-looking force structure additions

Source: `audit/reports/3dmedbn/03_asr_3dmedbn.txt` and
`audit/reports/3dmedbn/04_asr_unit_breakdown.txt`.

This must be reconciled before the TFSMS gate at
`TFSMS_Loading!D19` can be set to FALSE - RECONCILED in the
methodology workbook. The BFR currently has no `TFSMS_Loading`
sheet; that comes from `BFR_Generator_FC2-000-05N.xlsx`.

#### F6. Mystery Surg Co C reference (UIC M28275)

Sheet 45110 row 39 references `M28275 SURGICAL CO C`. The ASR
shows only Surg Co A (M28263) and Surg Co B (M28262) under
3d MED BN. UICs M28271/M28272/M28273 also appear in the 45110
sheet but do not appear in the ASR.

Either:
- Surg Co C was deactivated and M28275 is stale
- M28275 is a different unit altogether
- These are pre-restructure aliases

Needs SME verification before any line on the 45110 sheet can be
trusted.

### MAJOR (must fix; not foundational blockers)

#### F7. TO column 7 BIC encoding inconsistent

The TO sheet has 1325 rows. Initial inventory pulled 145 CCN-like
rows. The BIC column (col 7 in MCTOFD layout) was not detectable by
the simple regex audit; the BIC values appear in column-positions
that vary across rows. This needs a per-column header walk before
any reconciliation can proceed.

Source: `audit/reports/3dmedbn/05_toe_inventory.txt` showed BIC
prefix counts came back empty because the column heuristic missed.

#### F8. Surg Co B TFSMS export still shows Hawaii address

`M28262_3dMedSurgB.xlsx` Header R11: "MCBH BOX 63062, KANEOHE BAY,
HI 96863." Structure data current as of 02/03/2026.

Per the G-5 30 Apr 26 note, the unit has physically relocated. The
TFSMS structure data has not been updated to reflect this. Until
TFSMS is updated, the BFR's address fields and any UIC-to-location
joins that key off TFSMS will reflect the pre-move state.

This is a TFSMS data freshness issue, not a workbook bug. Worth
noting in the foundational document so the reader knows the
address line is stale.

#### F9. MISSION STATEMENT sheet contains 306 rows and one #VALUE!

The 306-row Mission Statement is heavy. CLB-4 keeps mission text
in the Header sheet of the per-company TFSMS export. The single
`#VALUE!` will render in any printout. Worth trimming and fixing
the formula.

### MINOR (cosmetic / hygiene)

- Locator_Deck has 608 rows. Looks like a TAMCN-to-room/location
  lookup table; not part of the canonical BFR template per CLB-4.
  Confirm whether this is needed for 3d MED BN's specific use
  case or if it can be retired.
- Print areas defined on most sheets but not all (17110, 21451,
  61072, 61073 missing print_area). Set them so printouts are
  consistent.
- Sheet 61072 col_max reports 16384 (the worksheet has data
  written into a cell beyond column AF that Excel widened the
  used range for). Trim.

## 4. What the foundational document needs (Definition of Done)

Per `CLAUDE.md` "Definition of done" plus Kenji RE email 1 May 26:

1. UNIT_ROLLUP includes every CCN sheet that is referenced in the
   TO or TE NOTE columns. No silent drops.
2. Zero `#REF!`, `#DIV/0!`, `#NAME?`, `#VALUE!`, and zero
   unintended `#N/A` after LibreOffice headless recalc.
3. Every CCN sheet's TOTAL REQUIREMENT cell is a real number
   traceable through formulas back to a TO/TE input cell or a
   documented FC 2-000-05N planning factor.
4. No external links (the five identified must be severed).
5. Zero `#REF!` and zero `#N/A` in defined names; junk names
   removed.
6. TFSMS reconciliation gate (`TFSMS_Loading!D19` in the
   methodology workbook) reads `FALSE - RECONCILED` once ASR /
   TFSMS counts are pasted in. Requires F5 reconciliation first.
7. Cosmetic fingerprint preserved: green tabs on visible sheets
   stay green, font remains Calibri at established sizes, A1
   banner text retained, no decorative changes.
8. Mission Statement on the Header tab of each company TFSMS
   export remains the source of truth; the BFR's MISSION STATEMENT
   sheet trimmed to a single page summary that points back to the
   TFSMS exports.

## 5. Recommended repair sequence

Layered, with explicit gates between layers. Each layer is a
single commit so it can be reviewed in isolation.

### Phase A: structural triage (no formula changes)

A1. Audit deeper: dump every formula in the TO sheet for column
    7 (BIC) so we know which columns hold BIC. Dump every CCN
    sheet's TOTAL REQUIREMENT formula path. Output:
    `audit/reports/3dmedbn/08_formula_paths.txt`.

A2. Snapshot the cosmetic fingerprint (fonts, fills, borders,
    merge patterns) of the green-tabbed sheets so we have a
    reference to validate against post-edits. Output:
    `audit/reports/3dmedbn/09_cosmetic_fingerprint.txt`.

A3. Resolve F5 personnel reconciliation question with the user:
    is the canonical 3d MED BN total 609 (ASR), 711 (CG signed
    letter), or some third number? Document the resolution.

A4. Resolve F6 Surg Co C question: is M28275 still a real entity,
    or stale? If stale, mark the 45110 sheet rows for cleanup.

### Phase B: structural fixes (no cosmetic changes)

B1. Sever all five external links. For TO and TE, replace external
    `[5]CCN!` lookups with internal references, either to a new
    `CCN_Library` sheet copied in from the methodology workbook,
    or to `audit/CCN_VOCABULARY.json` exported as a sheet.

B2. Clean up defined names: delete the 28 `#REF!` entries, 2
    `#N/A`, 14 junk literals. Keep only well-formed names that
    actually resolve. Document the deletions in
    `audit/reports/3dmedbn/10_named_names_cleanup.txt`.

B3. Add UNIT_ROLLUP rows for the four hidden CCN sheets (14312,
    21451, 21710, 45110) and unhide them, OR document in the
    rollup why they are excluded. The cosmetic stays the same;
    only the rollup table grows.

B4. Re-run the LibreOffice headless recalc check. Target: zero
    `#REF!`, zero `#DIV/0!`, zero `#NAME?`, zero `#VALUE!`. The
    `#N/A` counts should drop to zero where they were caused by
    severed external links.

### Phase C: data reconciliation

C1. Walk the TO sheet against the M28262 (Surg B), M28263 (Surg
    A), and M28261 (H&S) TFSMS exports. Confirm BIC counts match.
    Surface mismatches as `audit/reports/3dmedbn/11_to_recon.txt`.

C2. Walk the TE sheet against the company T/O&E equipment lines.
    Surface TAMCN orphans (TE rows whose TAMCN does not map to
    any CCN per `audit/TAMCN_CCN_MAP.yaml`). Output:
    `audit/reports/3dmedbn/12_te_recon.txt`.

C3. Run the reconciliation gate: paste TFSMS counts and ASR
    counts into the methodology workbook
    (`BFR_Generator_FC2-000-05N.xlsx`) at the documented
    `TFSMS_Loading` rows. Confirm `D19` reads `FALSE -
    RECONCILED`. Capture screenshot.

### Phase D: validator pass

D1. Run `pipeline/validate.py` against the repaired BFR. Target:
    8 PASS / 0 FAIL.

D2. Capture report at
    `audit/reports/3dmedbn/13_validator.txt`.

### Phase E: foundational-document delivery

E1. Update `audit/3DMEDBN_BASING_BRIEF.md` to point at the
    repaired BFR as the authoritative requirement set for the
    Kinser walk and SOW development.

E2. Update `.claude/skills/bfr-pipeline/SKILL.md` Track DONE entry
    capturing the repair work, file hashes, and validator state.

E3. Commit and push to the work branch.

## 6. What I will NOT do without explicit user approval

Per Apex Omega and per the user's standing direction:

- I will not alter the cosmetic of any green-tabbed CCN sheet.
- I will not change CCN sheet calculation logic without
  documenting why and citing FC 2-000-05N section.
- I will not delete the hidden CCN sheets. They are repaired or
  brought into the rollup; not deleted.
- I will not silently fill `TBD pending` items per Apex Omega
  rule 4.
- I will not change personnel numbers in the TO without
  reconciling against TFSMS and ASR per F5.

## 7. Decisions needed from the user before Phase A starts

D1. **Personnel total (F5 resolution).** RESOLVED per user direction
    2026-05-05: canonical planning total is 711 (CG signed letter,
    matching the HTML). The 609 ASR figure is the BIC-only structure
    number and is presented as a footnote inside the BFR for
    traceability. The 102-person delta (711 minus 609) is most
    likely civilians, contractors, USN augmentees, or other non-BIC
    personnel that ASR does not carry. The BFR will not silently
    reconcile to 609; the cover and headline numbers use 711, with
    the ASR breakout cited.

D2. **Surg Co C (F6 resolution).** Does M28275 still exist as a
    real unit? If not, is the 45110 sheet's reference to Surg Co
    C historical, or is it an error to remove?

D3. **External links (F3) replacement strategy.** Replace the
    `[5]CCN!` external lookup with:
    - (a) a new internal `CCN_Library` sheet copied from
      `BFR_Generator_FC2-000-05N.xlsx`, or
    - (b) a new internal sheet built from
      `audit/CCN_VOCABULARY.json`, or
    - (c) something else?

D4. **Hidden CCN sheets (F1) treatment.** For 14312, 21451,
    21710, 45110:
    - (a) repair and unhide (preferred per CLB-4 lessons), or
    - (b) bring rollup links in but leave hidden, or
    - (c) document why excluded?

D5. **Locator_Deck sheet retention.** Keep, trim, or remove?

D6. **Phase ordering.** Is the sequence A -> B -> C -> D -> E
    the order you want, or do you want C (data reconciliation)
    earlier so we know the personnel and equipment ground truth
    before structural fixes?

Once D2 through D6 are answered, Phase A starts. D1 is closed.
