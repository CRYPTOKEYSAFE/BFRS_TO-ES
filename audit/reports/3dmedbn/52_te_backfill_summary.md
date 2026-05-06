# 3d MED BN BFR TE Backfill Mapping Summary

Source mapping: 2031 Master TO&E v1.1 (2025-04-11), sheet TE_3,
filtered to UICs M28261, M28262, M28263 (3d MED BN).
BFR target: M67400-FO-M13020 3D MED BN-22NOV2024.xlsx, sheet TE (read-only).

Apex Omega rule 7: every backfill value below is reproducible by
looking up (UIC, TAMCN) in the 2031 Master TO&E TE_3 sheet.
Apex Omega rule 4: rows that do not resolve are marked UNMATCHED
or UIC-MATCHED-TAMCN-MISMATCH and carry no proposed backfill values.

## Headline finding

Two of the eight columns the BFR's CCN sheets need are NOT recoverable
from the 2031 Master TO&E TE_3, because TE_3 itself does not carry
them. Specifically:

- Space Factor (TE_3 col 22): blank for all 19,001 data rows.
- NTG Factor (TE_3 col 25): blank for all 19,001 data rows.

The remaining six columns are recoverable for most rows:

- L, Ft / W, Ft / H, Ft / Volume EA / Volume Total: populated for 464 of
  the 506 3d MED BN rows in TE_3 (~91.7%).
- NSY: populated for 439 of the 506 3d MED BN rows (~86.8%).

Implication: a TAMCN-keyed lookup against TE_3 cannot, by itself,
supply the Space Factor and NTG Factor that CCN 21451 and CCN 14312
require. Those two factors must come from a different authoritative
source (FC 2-000-05N planning factor tables, or a separate engineering
data source). Per Apex Omega rule 4, those columns are TBD pending
identification of that source.

## Match-class counts

- Total BFR TE TAMCN-bearing rows: 506
- MATCHED: 502
- TAMCN-MATCHED-IN-OTHER-UIC: 0
- UIC-MATCHED-TAMCN-MISMATCH: 4
- UNMATCHED: 0

## Master TO&E coverage stats

- Master TO&E rows loaded for 3d MED BN UICs: 506
- Unique (UIC, TAMCN) keys in master subset: 506
- Distinct TAMCNs across the three UICs: 216

## Unmatched TAMCNs (UNMATCHED bucket)

None.

## UIC-MATCHED-TAMCN-MISMATCH bucket

BFR row's UIC is one of the three 3d MED BN UICs, but the TAMCN
does not appear under that UIC (or any 3d MED BN UIC) in the 2031
Master TO&E. Likely causes: (a) post-2031-cut TAMCN added to the
unit, (b) BFR data-entry error, (c) TAMCN reclassification between
the Master TO&E vintage and the 2024 BFR. SME review required.

### UIC M28261 (2 TAMCNs)

- B00497B
- C00392B

### UIC M28262 (1 TAMCNs)

- C00392B

### UIC M28263 (1 TAMCNs)

- C00392B


## TAMCN-MATCHED-IN-OTHER-UIC examples

None.

## Apex Omega Violation 1 verification: C00392B FILTER WATER PURIFI

- Rows for TAMCN C00392B in entire 2031 Master TO&E TE_3: 0
- Rows for TAMCN C00392B under 3d MED BN UICs (M28261/M28262/M28263): 0

FINDING: TAMCN C00392B FILTER WATER PURIFI does NOT appear under
any 3d MED BN UIC (M28261, M28262, M28263) in the 2031 Master TO&E
v1.1 (2025-04-11). It does not appear under any UIC in the entire
TE_3 sheet (zero hits in 19,001 data rows). The BFR's TE sheet does
carry C00392B for all three 3d MED BN UICs (BFR TE rows 505, 506,
507) but with no quantity or dimensional data, and the 2031 Master
TO&E does not corroborate any of it.

Per Apex Omega rule 4, the previously derived qty 180 is unsupported
by this primary source and is TBD pending an authoritative T/E that
explicitly carries C00392B for 3d MED BN (e.g., the unit's ASR or a
more recent TFSMS export that includes this line item).

## Per-CCN backfill counts

Counts of BFR TE rows whose backfill from the 2031 Master TO&E
yields a non-blank Space Factor or non-blank NSY+NTG, by CCN tag
on the BFR TE row.

| CCN | BFR TE rows | rows with Space Factor | rows with NSY+NTG |
|---|---:|---:|---:|
| 14312 | 8 | 0 | 0 |
| 14345 | 126 | 0 | 0 |
| 21451 | 47 | 0 | 0 |
| 21710 | 75 | 0 | 0 |
| 44112 | 249 | 0 | 0 |
| 45110 | 1 | 0 | 0 |

## CCN-specific feasibility

- CCN 21451 has 47 BFR TE rows tagged. Of those,
  0 carry a Space Factor sourced from the 2031 Master TO&E.
  Space Factor is blank for every row of TE_3, so the 2031 Master TO&E
  cannot supply this column. Backfill is NOT sufficient for CCN 21451
  to compute; Space Factor must come from FC 2-000-05N planning factor
  tables for vehicle-equipment occupancy, or from another engineering
  authority. TBD pending source identification.

- CCN 14312 has 8 BFR TE rows tagged. Of those,
  7 carry NSY from the 2031 Master TO&E, and
  0 carry NTG Factor. NTG Factor is blank for every
  row of TE_3, so the 2031 Master TO&E cannot supply this column.
  Backfill is partial: NSY is recoverable but NTG is not. CCN 14312
  cannot compute on this backfill alone. NTG Factor TBD pending
  identification of an authoritative armory-storage planning source.

## Method

1. Master TO&E TE_3 was streamed and filtered to rows whose UIC was
   M28261, M28262, or M28263. Each row was indexed under (UIC, TAMCN).
2. The BFR's TE sheet (sheet name 'TE') was opened read-only. Each
   row with a non-blank TAMCN (column 9) was emitted to the CSV.
3. Match priority:
   a. Exact (UIC, TAMCN) hit -> MATCHED, backfill from that record.
   b. TAMCN exists under a different 3d MED BN UIC -> 
      TAMCN-MATCHED-IN-OTHER-UIC; dimensional/factor backfill carried
      from the sibling record (these fields are TAMCN-intrinsic).
   c. BFR UIC is in {M28261, M28262, M28263} but TAMCN absent in
      master subset -> UIC-MATCHED-TAMCN-MISMATCH, no backfill.
   d. Otherwise -> UNMATCHED, no backfill.
4. Outputs: CSV (one row per BFR TE row) and this summary.

## Files

- /home/user/BFRS_TO-ES/audit/reports/3dmedbn/52_te_backfill_mapping.csv
- /home/user/BFRS_TO-ES/audit/reports/3dmedbn/52_te_backfill_summary.md
