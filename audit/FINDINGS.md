# CLB-4 BFR Audit, Forensic Findings (Round 1)

Audit date: 2026-04-28
Files audited: all `.xlsx` in repository root
Method: structural inventory via openpyxl (`audit/inventory.py`, `audit/sheet_dump.py`, `audit/file_metadata.py`); no workbook has been modified.



## 1. Authoritative file determination

| File | Internal `modified` | Status |
|---|---|---|
| `SW_M29030_CLB4_BFR_2026-NWPCW167400L021.xlsx` | 2026-02-28 01:25:46 | AUTHORITATIVE |
| `SW_M29030_CLB4_BFR_2026.xlsx` | 2026-02-28 01:23:55 | duplicate, 1m51s earlier, structurally identical |
| `FO_M29030_CLB 4_FINAL BFR.xlsx` | 2025-05-06 07:34:41 | STALE, do not use (almost a year old) |

Provenance: every BFR file (including the 3D Med Bn benchmark) was originally `created` 2017-03-06 by `Brunson, James J CIV NAVFAC MIDLANT, AM`. Every CLB-4 BFR in this repo descends from the same 2017 NAVFAC MIDLANT template.

## 2. Authoritative file is materially incomplete

`UNIT_ROLLUP` sums only 4 visible CCNs for a CLB:

| CCN | Description | GSF |
|---|---|---:|
| 14345 | Armory | 413 |
| 21451 | Auto Organization Shop | 2,315 |
| 21455 | Vehicle Wash Platform | 3,192 |
| 61072 | Battalion HQ Admin | 8,379 |
| | Total | 14,299 |

Six additional CCN tabs exist in the workbook but are hidden, and every one of them is broken:

| CCN | Description | State | Failure mode |
|---|---|---|---|
| 14312 | Operational Vehicle Laydown | hidden | Per-TAMCN lookups all `#REF!`; `IFERROR` masks to `""`; rolls up as 0 |
| 14326 | MC EOD Platoon Facility | hidden | Loud `#REF!` errors; mission text is for Engineering Support Bn, not CLB |
| 21710 | Comms / Elec Maintenance Shop | hidden | All `COUNTIFS`/`SUMIFS` against `#REF!`; rolls up as `#REF!` |
| 21730 | Field Maintenance Shop (Comms/Elecs) | hidden | Same lookup breakage AND lookup strings still reference `"21710o"` etc., the sheet was copy-pasted from 21710 and the search keys were never updated to `21730*` |
| 44112 | Storage of Air or Ground Organic Units | hidden | Warehouse / admin / personal-effects sections all `#REF!`; only the hardcoded "Support Space" section computes (1,388.52 NSF) |
| 45110 | Open Storage Area | hidden | All container counts (`SUMIFS` against TAMCN) are `#REF!` |

The own `61072` sheet documents that 156 CLB-4 billets are "EXCLUDED FROM THIS CCN" and require separate facility CCNs:

> Medical / BAS billets (34), medical facility CCN required
> EOD Section billets (13), EOD facility CCN required
> Specialist shop billets (99), maintenance shop CCN(s) required
> Ordnance repair billets (10), ordnance shop CCN required

Those required CCN sheets are exactly the ones that exist-but-are-hidden-and-broken (14326 EOD, 21710/21730 maint shops, plus a missing medical CCN entirely). The BFR currently captures admin space for 84 of CLB-4's billets and zero space for the other 156.

Implication: a defensible CLB BFR is typically tens of thousands of GSF beyond the 14,299 currently rolled up. The current artifact is a partial rebuild left in mid-state with the broken legacy sheets buried out of sight.

## 3. Visible CCN tabs are clean rebuilds

Sheets `14345`, `21451`, `21455`, and `61072` were rebuilt from scratch, 30, 37 rows each, hardcoded counts, simple multiplication formulas, zero `#REF!`, explicit FC 2-000-05N table citations in the labels. Whoever built these did good work; they just stopped after four CCNs.

The hidden tabs are the original 2017 NAVFAC MIDLANT template structure (80, 180 rows each, complex multi-page layouts driven by `COUNTIFS`/`SUMIFS`/`INDEX-MATCH` against the `TO` and `TE` sheets), and those lookup ranges were destroyed at some point and replaced with `#REF!`.

## 4. Workbook hygiene problems persist across all BFRs

Defined-name pollution in the authoritative SW_:

```
a, Comment, CostCode, d, DDD, delete1, GDSGSDG, ghhghg, gsg, Hello,
HELLO1, heloo, new, oc, Ordnance, sds, TE_2, TE_3, TE_orignial, te_table, x
```

21 of 29 defined names are `#REF!` or `#N/A`, including a typo (`TE_orignial`), names that are obviously test garbage (`Hello`, `gsg`, `heloo`, `DDD`, `ghhghg`, `GDSGSDG`), and names that suggest cross-template paste history (`Ordnance`, `CostCode`).

The 3d Med Bn benchmark is worse: 44 defined names, with additional garbage (`_lAQUETTAaRMORY`, `gfhgfhgf`, `Amroy`, `ghgghhg`, `mt`).

External links, `FO_` (stale) and `3D MED BN` both reach outside the workbook. The authoritative SW_ is clean (0 external links).

| Workbook | External link targets |
|---|---|
| `FO_M29030 ... FINAL BFR` | `\\naeanrfkfs43\BULK_Storage_4\...` (UNC), 2 SharePoint URLs to `M00146-MS-M19885-20161222.xlsx` (a 2 LAAD template) |
| `SW_M29030 ... NWPCW167400L021` | (none) [ok] |
| `M67400 3D MED BN` | same UNC; `C:\Users\renel.douyon\Desktop\Copy of 19Marine Air Support Squadron_advocate review (002).xlsx` (someone's local desktop); `\\mcuspndlfs44\CPEN_GF\...\1ST MED BN M11020_BFR UNIT EDIT_04MAY2018.xlsx` (Camp Pendleton 1st Med Bn 2018 BFR); 2 LAAD SharePoint URL; one legitimate-looking flankspeed link to `M13020 2029 TO E CUT.xlsx` |

Wrong-unit residue in mission statements:
- CLB-4 SW_: Mission Statement carries `UNIT 38440 / UTC 9VCBF` and `UNIT 38420 / UTC UWLAB`, neither is CLB-4.
- 3D Med Bn: Mission Statement carries `UNIT 38445`, `UNIT 38448`, with `MCBH BOX 63062 / KANEOHE BAY HI 96863`, that's a Hawaii unit, not Okinawa-based 3D Med Bn.
- Defined names `EWC = "M00873"`, `HQ = "M00871"`, `TAOC = "M00872"` in CLB-4 SW_ are MCC codes for an unrelated unit family (M008xx range).

## 5. Two company files are openpyxl round-trip artifacts

| File | Last modified | By |
|---|---|---|
| `M29111_HQ_CO_CLB-4.xlsx` | 2026-02-26 08:11:04 | `Potter CTR Anthony L` [ok] |
| `M29112_CLC_A_CLB-4.xlsx` | 2026-02-26 08:18:11 | `Potter CTR Anthony L` [ok] |
| `M29113_CLC_B_CLB-4.xlsx` | 2026-04-28 08:00:16 (upload day) | `creator: openpyxl` ⚠ |
| `M29114_GS_CO_CLB-4.xlsx` | 2026-04-28 08:00:16 (upload day) | `creator: openpyxl` ⚠ |

Mitigation: all four files are pure-data exports (0 formulas, 0 data validations, 0 conditional formats, 0 defined names, 0 external links), so a passive read-then-write through openpyxl does not put the data values at risk. Cell values, sheet structure, and merged-cell counts are consistent between the touched and untouched pairs. Damage risk is low for downstream data extraction but should be flagged for the record.

## 6. The "Master TO&E" file does NOT cover CLB-4

`2031 Master TO&E v1.1 - 20250411.xlsx` is a clean two-sheet data dump, `TO_2` (24,299 billet rows), `TE_3` (19,002 equipment rows), zero formulas, zero links. But it covers a different MLG.

UICs present in the file (M29* range only): `M29003, M29004, M29006, M29011-14, M29017, M29022-27, M29041, M29047, M29091-94, M29101-04, M29106, M29491-94`.

UICs NOT present: `M29030` (CLB-4 parent), `M29031`, `M29111`, `M29112`, `M29113`, `M29114`. CLB-4 is not in this Master TO&E.

Source-of-truth TO&E data for CLB-4 in this repo lives in the four `M2911x` company workbooks (HQ / CLC A / CLC B / GS Co), which contain `TO`, `Billet Summary`, `RecapMOS`, `RecapMCC`, `Primary Only` (TE), and `COE` sheets per company.

The 7.9 MB Master TO&E is potentially useful as a wider 3d MLG (or 1st MLG, depending on what those UICs are) reference dataset, but it cannot be used to load or validate CLB-4's BFR.

## 7. What is NOT in the repo that we may need

- "1 of 2" companion to `E_BFR_F_PRC_BU26-5836R_POM26_20260228_2_OF_2.pdf` (POM26 package).
- INFADS extract for CLB-4 facilities at MCB Camp Butler (existing real-property assets to compare against BFR-rated demand).
- The actual MCTOFD or MTOMS-T export for `M29030 / M29111-14`. The four company files appear to be filtered exports of this data.
- A clean reference BFR template (the 3d Med Bn file is the closest in this repo and is itself problematic).
- FC 2-000-05N most recent series PDFs (Feb 2026 release) for cross-checking planning factors.

## 8. Recommended next steps (not yet executed)

In the order I'd run them, pending direction from you:

1. Reconcile the `61072` excluded-billet count against the four company TO sheets. The 61072 sheet says 84 in-scope + 156 excluded = 240 billets. Cross-check that against M29111 + M29112 + M29113 + M29114 TO data. If those add up, we have a defensible billet baseline; if not, the 61072 admin number is also wrong.
2. Build a CCN coverage matrix, for every CCN tagged in the four company TO sheets, mark whether the CLB-4 SW_ workbook covers it (visible & calculated vs. hidden & broken vs. missing entirely). This produces the "BFR is missing X SF" finding in defensible form.
3. Repair vs. rebuild decision per hidden CCN. For each of the 6 broken hidden tabs, choose:
   - rebuild as a clean hardcoded sheet (matches the 14345/21451/21455/61072 pattern), or
   - repair the `INDEX/MATCH/COUNTIFS` ranges to point at the current `TO` and `TE` sheet structure.
   Rebuild is faster and produces auditable artifacts; repair preserves automation but requires understanding the original 2017 lookup contract.
4. Cleanse defined names. Remove all `#REF!` / `#N/A` defined names and the test garbage. This is purely hygienic but improves auditability.
5. Replace template-residue mission text and MCC defined names with CLB-4 / 3d MLG values.
6. Decide on the openpyxl-touched company files. If known-clean original copies of `M29113` and `M29114` exist somewhere, swap them in. Otherwise document the touched state and proceed.

No workbook has been edited. All evidence is in `audit/reports/`.

## 9. TFSMS_UNRECONCILED gate is structurally broken (Round 3 finding)

Audit date: 2026-04-28. Surfaced during baseline-audit pass on the
methodology workbook BFR_Generator_FC2-000-05N.xlsx.

Apex Omega Sec.5.6 and CLAUDE.md both treat the TFSMS_UNRECONCILED
flag as the operational reconciliation gate; "must read FALSE before
any BFR is releasable; never bypass." The skill and CLAUDE.md both
locate the flag at TFSMS_Loading!$D$19.

The named range TFSMS_UNRECONCILED resolves to TFSMS_Loading!$D$19
correctly. The cell at $D$19 holds no value and no formula. It
cannot hold a value at its current coordinate because the entire
row $B$19:$O$19 is a single merged range, the only writable cell of
which is $B$19. $B$19 holds the label string "Reconciliation Gate".

Consequences:
1. The gate never reads FALSE, so per the binding semantic ("must
   read FALSE before releasable") no BFR generated against this
   methodology workbook can be released today. Definition of Done
   item 6 in CLAUDE.md is failing for every unit.
2. The gate also never reads TRUE, so it does not actually GATE
   anything; downstream sheets that reference it see a blank, which
   in Excel is treated as FALSE in boolean contexts. The system
   silently passes when it should be loudly failing.
3. The named range was authored pointing at a coordinate that is
   structurally incapable of holding a value, suggesting either the
   merge was added after the named range, or the named range was
   added without verifying the target cell's mergeability.

Repair options for the methodology owner. This audit does not
choose between them; per Apex Omega rule 4, the structural change
to the methodology workbook requires methodology-owner direction.

Option A. Unmerge B19:O19. Restore the label "Reconciliation Gate"
in B19. Author the gate formula in D19 (e.g.,
`=IF(AND(TFSMS_TOTAL>0, SUM(<ASR-PN-named-ranges>)>0,
TFSMS_TOTAL=<ASR-PN-total>), FALSE, TRUE)` or similar; the formula
must compare TFSMS personnel totals (named range TFSMS_TOTAL at
TFSMS_Loading!$O$17) against the unit's ASR-reconciled personnel
totals. Add explicit row-level breakdown cells (E19, F19, G19...)
showing per-bucket reconciliation status if desired.

Option B. Leave the merge in place. Move the named range
TFSMS_UNRECONCILED to a different unmerged cell on the sheet
(e.g., a new row 25 with a labeled value cell). Author the gate
formula there. Update CLAUDE.md and the skill to reflect the new
coordinate.

In either option, the formula's exact comparison logic depends on
which PN_* named ranges represent the ASR-reconciled personnel
totals for the unit; the BFR_Generator_FC2-000-05N.xlsx sheet
inventory does not currently expose those named ranges, only the
TFSMS_* family at TFSMS_Loading!$D$17:$O$17. The methodology owner
must specify the ASR-side named ranges before the gate formula can
be authored without speculation.

This audit does NOT silently fix the workbook. The defect is
documented here and surfaced for methodology-owner direction.

## 9b. TFSMS_UNRECONCILED gate repaired (Round 3 follow-up, 2026-04-30)

Methodology owner directed: Option A1 (unmerge B19:O19) plus a
three-state gate that supports the user's stated workflow
("sometimes I have ASR, sometimes I don't").

Repair shipped:

  Cell B19:C19 (merged) holds the label "Reconciliation Gate".
  Cell D19:O19 (merged) holds the formula
    =IF(O37=0,"PENDING - ASR not yet provided",
        IF(O17=O37,"FALSE - RECONCILED",
                   "TRUE - UNRECONCILED"))
  Conditional formatting on D19:
    contains "FALSE" -> green fill (BFR releasable)
    contains "TRUE"  -> red fill (BFR held; per-bucket diagnostic)
    default          -> yellow (PENDING)
  Cell comment documents the three states plus Apex Omega Sec.5.6
  authority.

ASR data entry section added at TFSMS_Loading rows 26-37:
  Row 26: section heading
  Row 27: "Per-UIC ASR Loading" sub-header
  Row 28: column-group headers (Marine Active, Navy Active, etc.)
  Row 29: column sub-headers (UIC, Unit Name, Off, Enl, ...)
  Rows 30-36: 7 ASR data entry rows (mirror of TFSMS rows 9-15)
  Row 37: ASR UNIT TOTAL (mirror of TFSMS row 17)

Per-bucket reconciliation diagnostic at TFSMS_Loading rows 39-51:
  Row 39: section heading
  Row 40: column headers (Bucket, TFSMS, ASR, Delta, Status)
  Rows 41-51: one row per personnel bucket showing TFSMS count,
              ASR count, delta, and per-bucket status
              (PENDING / OK / MISMATCH) with conditional fill.

Named ranges:
  TFSMS_UNRECONCILED rebound to TFSMS_Loading!$D$19 (now live)
  PN_MAR_OFF, PN_MAR_ENL, PN_NAV_OFF, PN_NAV_ENL, PN_OS_OFF,
  PN_OS_ENL, PN_RES_OFF, PN_RES_ENL, PN_CIV, PN_CTR, PN_NC,
  PN_TOTAL all point at the corresponding cells in row 37.
  Parallel to the TFSMS_* family at row 17.

Recalc verification: 5,553 cells; zero error tokens
(#REF!, #DIV/0!, #NAME?, #VALUE!) via Python `formulas` package.
fullCalcOnLoad=True set on the workbook so Excel and LibreOffice
recompute on open.

Workflow per the methodology owner:

  1. Paste TFSMS counts into rows 9-15 (existing). Totals roll up
     to row 17 automatically. Gate at D19 reads
     "PENDING - ASR not yet provided" because the ASR section is
     empty. BFR planning work can proceed.
  2. When ASR data is available, paste it into rows 30-36 with
     the same UIC sequence. Totals roll up to row 37. Gate at D19
     turns green ("FALSE - RECONCILED") if TFSMS = ASR, red
     ("TRUE - UNRECONCILED") if not.
  3. If red, the per-bucket diagnostic at rows 41-51 shows which
     bucket is off. User adjusts either side until each bucket
     reads "OK".
  4. Definition of Done item 6 ("TFSMS_UNRECONCILED = FALSE") is
     satisfied only in the green / RECONCILED state. Apex Omega
     Sec.5.6 binding.

Finding 9 (the structural defect) is closed by this commit.
