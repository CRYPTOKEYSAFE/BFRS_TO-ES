# H&S C00392B FILTER WATER PURIFI deletion readme

Date: 2026-05-06
Branch: claude/apex-omega-audit-repair-gG9mM
File modified: M67400-FO-M13020 3D MED BN-22NOV2024.xlsx
Backup: M67400-FO-M13020 3D MED BN-22NOV2024.preTabCBackfill-backup.xlsx

## What was deleted

TE row 507, the H&S Co (M28261) entry for TAMCN C00392B FILTER
WATER PURIFI-41207. The row was physically deleted via
`ws.delete_rows(507, 1)`. TE max_row went from 2251 to 2250.

The Surg A and Surg B entries for the same TAMCN (TE rows 505 and
506, qty 180 each) were RETAINED. Those entries are supported by
the surgical companies' own TFSMS COE rules (per skill Track 10b
bucket D ratification, commit 42b1428).

## Why

Apex Omega Violation 1, declared in skill Track 10e self-audit:
the prior session derived a qty 180 for the H&S Co C00392B by
"mirroring" the same-battalion Surg A and Surg B allocation. That
was a guess. The 2031 Master TO&E v1.1 (dated 2025-04-11) was
queried as a primary source and returned ZERO hits for TAMCN
C00392B under any UIC across all 19,001 data rows of TE_3.

Per Apex Omega rule 4 (omit if not verifiable, never guess to
fill a gap), the unsupported H&S row was removed. If H&S Co
acquires this filter at any qty, an authoritative T/E entry must
be the basis, not an inter-company mirror.

## User direction

User message 2026-05-06: "You can delete it and put a read me in
somewhere; that is the best."

## Effect on validator

Validator post-deletion: 8 PASS / 0 FAIL (was 8 PASS / 0 FAIL
with the row in place; the row was attributed to CCN 44112 but
carried no quantity that affected GSF totals downstream).

## Reversal

If the H&S Filter Water Purifier turns out to be a real T/E
allocation, restore from
M67400-FO-M13020 3D MED BN-22NOV2024.preTabCBackfill-backup.xlsx
TE row 507, then re-source the qty from a primary T/E document.
