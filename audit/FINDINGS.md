# CLB-4 BFR Audit — Forensic Findings (Round 1)

**Audit date:** 2026-04-28
**Files audited:** all `.xlsx` in repository root
**Method:** structural inventory via openpyxl (`audit/inventory.py`, `audit/sheet_dump.py`, `audit/file_metadata.py`); no workbook has been modified.

---

## 1. Authoritative file determination

| File | Internal `modified` | Status |
|---|---|---|
| `SW_M29030_CLB4_BFR_2026-NWPCW167400L021.xlsx` | 2026-02-28 01:25:46 | **AUTHORITATIVE** |
| `SW_M29030_CLB4_BFR_2026.xlsx` | 2026-02-28 01:23:55 | duplicate, 1m51s earlier, structurally identical |
| `FO_M29030_CLB 4_FINAL BFR.xlsx` | 2025-05-06 07:34:41 | **STALE — do not use** (almost a year old) |

Provenance: every BFR file (including the 3D Med Bn benchmark) was originally `created` 2017-03-06 by `Brunson, James J CIV NAVFAC MIDLANT, AM`. Every CLB-4 BFR in this repo descends from the same 2017 NAVFAC MIDLANT template.

## 2. Authoritative file is materially incomplete

`UNIT_ROLLUP` sums **only 4 visible CCNs** for a CLB:

| CCN | Description | GSF |
|---|---|---:|
| 14345 | Armory | 413 |
| 21451 | Auto Organization Shop | 2,315 |
| 21455 | Vehicle Wash Platform | 3,192 |
| 61072 | Battalion HQ Admin | 8,379 |
| | **Total** | **14,299** |

Six additional CCN tabs exist **in the workbook but are hidden**, and every one of them is broken:

| CCN | Description | State | Failure mode |
|---|---|---|---|
| 14312 | Operational Vehicle Laydown | hidden | Per-TAMCN lookups all `#REF!`; `IFERROR` masks to `""`; rolls up as 0 |
| 14326 | MC EOD Platoon Facility | hidden | Loud `#REF!` errors; mission text is for **Engineering Support Bn**, not CLB |
| 21710 | Comms / Elec Maintenance Shop | hidden | All `COUNTIFS`/`SUMIFS` against `#REF!`; rolls up as `#REF!` |
| 21730 | Field Maintenance Shop (Comms/Elecs) | hidden | Same lookup breakage **AND** lookup strings still reference `"21710o"` etc. — the sheet was copy-pasted from 21710 and the search keys were never updated to `21730*` |
| 44112 | Storage of Air or Ground Organic Units | hidden | Warehouse / admin / personal-effects sections all `#REF!`; only the hardcoded "Support Space" section computes (1,388.52 NSF) |
| 45110 | Open Storage Area | hidden | All container counts (`SUMIFS` against TAMCN) are `#REF!` |

The own `61072` sheet documents that **156 CLB-4 billets are "EXCLUDED FROM THIS CCN" and require separate facility CCNs**:

> Medical / BAS billets (34) — medical facility CCN required
> EOD Section billets (13) — EOD facility CCN required
> Specialist shop billets (99) — maintenance shop CCN(s) required
> Ordnance repair billets (10) — ordnance shop CCN required

Those required CCN sheets are exactly the ones that exist-but-are-hidden-and-broken (14326 EOD, 21710/21730 maint shops, plus a missing medical CCN entirely). **The BFR currently captures admin space for 84 of CLB-4's billets and zero space for the other 156.**

Implication: a defensible CLB BFR is typically tens of thousands of GSF beyond the 14,299 currently rolled up. The current artifact is a partial rebuild left in mid-state with the broken legacy sheets buried out of sight.

## 3. Visible CCN tabs are clean rebuilds

Sheets `14345`, `21451`, `21455`, and `61072` were rebuilt from scratch — 30–37 rows each, hardcoded counts, simple multiplication formulas, zero `#REF!`, explicit FC 2-000-05N table citations in the labels. Whoever built these did good work; they just stopped after four CCNs.

The hidden tabs are the original 2017 NAVFAC MIDLANT template structure (80–180 rows each, complex multi-page layouts driven by `COUNTIFS`/`SUMIFS`/`INDEX-MATCH` against the `TO` and `TE` sheets) — and those lookup ranges were destroyed at some point and replaced with `#REF!`.

## 4. Workbook hygiene problems persist across all BFRs

**Defined-name pollution** in the authoritative SW_:

```
a, Comment, CostCode, d, DDD, delete1, GDSGSDG, ghhghg, gsg, Hello,
HELLO1, heloo, new, oc, Ordnance, sds, TE_2, TE_3, TE_orignial, te_table, x
```

21 of 29 defined names are `#REF!` or `#N/A` — including a typo (`TE_orignial`), names that are obviously test garbage (`Hello`, `gsg`, `heloo`, `DDD`, `ghhghg`, `GDSGSDG`), and names that suggest cross-template paste history (`Ordnance`, `CostCode`).

The 3d Med Bn benchmark is **worse**: 44 defined names, with additional garbage (`_lAQUETTAaRMORY`, `gfhgfhgf`, `Amroy`, `ghgghhg`, `mt`).

**External links** — `FO_` (stale) and `3D MED BN` both reach outside the workbook. The authoritative SW_ is clean (0 external links).

| Workbook | External link targets |
|---|---|
| `FO_M29030 ... FINAL BFR` | `\\naeanrfkfs43\BULK_Storage_4\...` (UNC), 2 SharePoint URLs to `M00146-MS-M19885-20161222.xlsx` (a 2 LAAD template) |
| `SW_M29030 ... NWPCW167400L021` | (none) ✓ |
| `M67400 3D MED BN` | same UNC; `C:\Users\renel.douyon\Desktop\Copy of 19Marine Air Support Squadron_advocate review (002).xlsx` (someone's local desktop); `\\mcuspndlfs44\CPEN_GF\...\1ST MED BN M11020_BFR UNIT EDIT_04MAY2018.xlsx` (Camp Pendleton 1st Med Bn 2018 BFR); 2 LAAD SharePoint URL; one legitimate-looking flankspeed link to `M13020 2029 TO E CUT.xlsx` |

**Wrong-unit residue** in mission statements:
- CLB-4 SW_: Mission Statement carries `UNIT 38440 / UTC 9VCBF` and `UNIT 38420 / UTC UWLAB` — neither is CLB-4.
- 3D Med Bn: Mission Statement carries `UNIT 38445`, `UNIT 38448`, with `MCBH BOX 63062 / KANEOHE BAY HI 96863` — that's a Hawaii unit, **not** Okinawa-based 3D Med Bn.
- Defined names `EWC = "M00873"`, `HQ = "M00871"`, `TAOC = "M00872"` in CLB-4 SW_ are MCC codes for an unrelated unit family (M008xx range).

## 5. Two company files are openpyxl round-trip artifacts

| File | Last modified | By |
|---|---|---|
| `M29111_HQ_CO_CLB-4.xlsx` | 2026-02-26 08:11:04 | `Potter CTR Anthony L` ✓ |
| `M29112_CLC_A_CLB-4.xlsx` | 2026-02-26 08:18:11 | `Potter CTR Anthony L` ✓ |
| `M29113_CLC_B_CLB-4.xlsx` | **2026-04-28 08:00:16** (upload day) | `creator: openpyxl` ⚠ |
| `M29114_GS_CO_CLB-4.xlsx` | **2026-04-28 08:00:16** (upload day) | `creator: openpyxl` ⚠ |

Mitigation: all four files are pure-data exports (0 formulas, 0 data validations, 0 conditional formats, 0 defined names, 0 external links), so a passive read-then-write through openpyxl does not put the data values at risk. Cell values, sheet structure, and merged-cell counts are consistent between the touched and untouched pairs. Damage risk is **low for downstream data extraction** but should be flagged for the record.

## 6. The "Master TO&E" file does NOT cover CLB-4

`2031 Master TO&E v1.1 - 20250411.xlsx` is a clean two-sheet data dump — `TO_2` (24,299 billet rows), `TE_3` (19,002 equipment rows), zero formulas, zero links. **But it covers a different MLG.**

UICs present in the file (M29* range only): `M29003, M29004, M29006, M29011-14, M29017, M29022-27, M29041, M29047, M29091-94, M29101-04, M29106, M29491-94`.

UICs **NOT present**: `M29030` (CLB-4 parent), `M29031`, `M29111`, `M29112`, `M29113`, `M29114`. CLB-4 is not in this Master TO&E.

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

1. **Reconcile the `61072` excluded-billet count against the four company TO sheets.** The 61072 sheet says 84 in-scope + 156 excluded = 240 billets. Cross-check that against M29111 + M29112 + M29113 + M29114 TO data. If those add up, we have a defensible billet baseline; if not, the 61072 admin number is also wrong.
2. **Build a CCN coverage matrix** — for every CCN tagged in the four company TO sheets, mark whether the CLB-4 SW_ workbook covers it (visible & calculated vs. hidden & broken vs. missing entirely). This produces the "BFR is missing X SF" finding in defensible form.
3. **Repair vs. rebuild decision per hidden CCN.** For each of the 6 broken hidden tabs, choose:
   - rebuild as a clean hardcoded sheet (matches the 14345/21451/21455/61072 pattern), or
   - repair the `INDEX/MATCH/COUNTIFS` ranges to point at the current `TO` and `TE` sheet structure.
   Rebuild is faster and produces auditable artifacts; repair preserves automation but requires understanding the original 2017 lookup contract.
4. **Cleanse defined names.** Remove all `#REF!` / `#N/A` defined names and the test garbage. This is purely hygienic but improves auditability.
5. **Replace template-residue mission text and MCC defined names** with CLB-4 / 3d MLG values.
6. **Decide on the openpyxl-touched company files.** If known-clean original copies of `M29113` and `M29114` exist somewhere, swap them in. Otherwise document the touched state and proceed.

No workbook has been edited. All evidence is in `audit/reports/`.
