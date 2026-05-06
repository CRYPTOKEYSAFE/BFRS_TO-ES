# Per-Block Formula Audit, 3d Med Bn BFR (M67400-FO-M13020 3D MED BN-22NOV2024.xlsx)

Apex Omega rule 1, facts only. Diagnostic only. No file modifications.

## Methodology

- Loaded the workbook twice with openpyxl, `data_only=False` (formulas) and `data_only=True` (cached values).
- Walked all 10 CCN sheets per the user-supplied target list.
- For each block (sub-table within a sheet, typically per UIC M28261 / M28263 / M28262), captured the intended subtotal/total cell, the formula, the cached value, the upstream support cells, and the most upstream defect.

## Key universal observation

The workbook was last saved without a calc-engine pass. Every formula cell returns `cached=None` from openpyxl regardless of whether the formula would compute. This means consumers (a planner opening the file in Excel) get blank-looking sheets until Excel recalculates. Once Excel recalculates, the structural defects below surface as zeros, blanks, or `#REF!`.

For TO/TE coverage, the pipeline-spine NOTE column is partially populated: TO column C has 711/1324 rows tagged, TO column D (CCN) has 712/1324 rows tagged, TE column G (UIC) has 506/2251 rows tagged and TE column D (CCN) has 506/2251 rows tagged. Many SUMIFS / COUNTIFS criteria therefore return zero against the unpopulated remainder. This is layer 2 / layer 3 debt per `audit/PIPELINE.md`.

## Defect class legend

- DC1, Cached value stripped (no calc on save). Universal.
- DC2, SUMIFS / COUNTIFS criterion against unpopulated TO NOTE / TE D-G column.
- DC3, IFERROR string fallback masking missing TE row, returns "(Not on TE)".
- DC4, Constant-offset / regression formula not derived from inputs (e.g. J24 = 347 * M33 + 1129).
- DC5, Range mis-sum (SUM range overshoots empty columns, or undershoots populated rows).
- DC6, COUNTIFS hardcodes UIC, ignores other companies (e.g. 14345 G25 only counts M28261).
- DC7, Empty merged-cell summary row (block-row absent or unmerged target).
- DC8, Wrong CCN tag in COUNTIFS criterion (e.g. 61072 row asks for "61073").
- DC9, Reference to absent supporting cell (downstream cell formula resolves but support input is None).
- DC10, Literal zero or "(none)" sentinel propagating through chain.

---

## Sheet 14312 (Operational Vehicle Laydown)

Total cell H36 = `=M25`. M25 = `=SUM(M21:P24)`. Four UIC blocks feed M21..M24, each delegates to support-region totals AB218 / AB402 / AB586 / AB770.

| Block | Total Cell | Formula | Cached | Defect Class | Upstream Defect Cell | Fix Diff |
|---|---|---|---|---|---|---|
| Sheet total | H36 | `=M25` | None | DC1 | M25 | Easy |
| Roll-up M25 | M25 | `=SUM(M21:P24)` | None | DC1, DC5 (sums P col, but only M col carries data) | M21..M24 | Easy |
| M28261 (H&S CO) | M21 | `=AB218` | None | DC1 | AB218 | Medium |
| M28263 (SURG A) | M22 | `=AB402` | None | DC1 | AB402 | Medium |
| M28262 (SURG B) | M23 | `=AB586` | None | DC1 | AB586 | Medium |
| (Block 4 unlabeled) | M24 | `=AB770` | None | DC1, DC7 (no UIC in B24/E24, orphan block) | AB770 | Hard |
| AB218 region total | AB218 | `=SUM(AC43:AE79)+SUM(AC89:AE125)+SUM(AC135:AE171)+SUM(AC181:AE191)` | None | DC1, DC5 (sums AC..AE; row data via AC43 = `IFERROR((W43*Y43*AA43),"")`; AD/AE cols empty in observed rows) | per-row AC formulas | Medium |
| AB402 region total | AB402 | `=SUM(AC227:AE263)+SUM(AC273:AE309)+SUM(AC319:AE355)+SUM(AC365:AE372)` | None | DC1, DC5 | per-row AC formulas | Medium |
| AB586 region total | AB586 | `=SUM(AC411:AE447)+SUM(AC457:AE493)+SUM(AC503:AE539)+SUM(AC549:AE556)` | None | DC1, DC5 | per-row AC formulas | Medium |
| AB770 region total | AB770 | `=SUM(AC595:AE631)+SUM(AC641:AE677)+SUM(AC687:AE723)+SUM(AC733:AE740)` | None | DC1, DC5, DC7 | per-row AC formulas, no UIC label | Hard |
| Per-row TAMCN VLOOKUPs (rows 43-79+, ~120 rows) | F43..F79+ | `=IFERROR(VLOOKUP(Cn,TE!$H:$Y,2,FALSE),"(Not on TE)")` | None | DC3 | TE!H:Y (TE column G UIC scoping not applied) | Medium |

Real defect locus, layer 2 NOTE tagging on TE for vehicle TAMCNs. The TAMCN list in column C of 14312 is hardcoded, but the per-row volume formula (AC43 etc.) multiplies W43 * Y43 * AA43 and those source columns are populated by VLOOKUP into TE. If TE column G is blank for the TAMCN, the row produces "" and SUM ignores it, so block totals trend toward zero.

---

## Sheet 14345 (Armory)

Total cell H40 = `=P25+K25`. P25 = `=B25+K25` (note, K25 added twice via P25). B25 = `=Q32`. K25 = `=G25*10`. G25 = `=COUNTIFS(TO!G:G,"E",TO!F:F,"M28261")`.

| Block | Total Cell | Formula | Cached | Defect Class | Upstream Defect Cell | Fix Diff |
|---|---|---|---|---|---|---|
| Sheet total | H40 | `=P25+K25` | None | DC1, DC5 (K25 double-counted: H40=P25+K25 and P25 already includes K25) | P25 | Easy |
| Storage roll-up | P25 | `=B25+K25` | None | DC1, DC5 | B25 | Easy |
| Storage NSF | B25 | `=Q32` | None | DC1 | Q32 | Easy |
| Cleaning area | K25 | `=G25*10` | None | DC1, DC6 | G25 | Easy |
| Largest co count | G25 | `=COUNTIFS(TO!G:G,"E",TO!F:F,"M28261")` | None | DC6 (hardcodes M28261 as "largest"; should test largest of the three companies, not assume H&S) | TO!G:G enlisted-rank tag | Medium |
| Q32 storage subtotal | Q32 | `=SUM(Q30:T31)` | None | DC1, DC5 (no Q29 row included; only 2 of 3 UIC blocks; Surg B M28262 row not populated) | Q30, Q31 | Medium |
| M28261 storage | Q30 | `=M30*$Q$29` (Q29=1.28 NTG) | None | DC1 | M30 | Easy |
| M28263 storage | Q31 | `=M31*$Q$29` | None | DC1 | M31 | Easy |
| M28262 storage | TBD, no Q-cell present | n/a | n/a | DC7 (Surg B row missing entirely; CG MCIPAC endorsement noted in B20 but block never inserted) | structural row insertion | Hard |
| H&S armory NSF | M30 | `=Z420` | None | DC1 | Z420 | Medium |
| SURG A armory NSF | M31 | `=Z803` | None | DC1 | Z803 | Medium |
| H&S region | Z420 | `=ROUNDUP(SUM(Z370:AC388,Z390,Z392:AC410,Z412:AC419),0)` | None | DC1, DC5 (composite SUM with explicit row exclusions, brittle) | TAMCN-row formulas | Medium |
| SURG A region | Z803 | `=ROUNDUP(SUM(Z753:AC771,Z773,Z775:AC793,Z795:AC802),0)` | None | DC1, DC5 | TAMCN-row formulas | Medium |
| Per-row TAMCN counts (rows 47-65, 74-79+, ~600 rows across blocks) | M47..M79+ | `=SUMIFS(TE!P:P,TE!G:G,$A$43,TE!H:H,A47)` | None | DC2 (TE G col only 506/2251 populated; A43 = B30 = "M28261" string) | TE column G UIC tagging | Medium |

Real defect locus, K25 double-count in H40, plus missing M28262 Surg B block, plus 14345 storage pipeline driven by TE column G UIC tagging which is 506/2251 populated.

---

## Sheet 17110 (Academic Instruction, design stub)

Sheet contains text "rolled up to CCN 17120" but still carries a TOTAL formula.

| Block | Total Cell | Formula | Cached | Defect Class | Upstream Defect Cell | Fix Diff |
|---|---|---|---|---|---|---|
| Sheet total | H40 | `=P25+K25` | None | DC9 (P25 and K25 both literally None / empty cells) | P25 / K25 | Easy (set =0 or remove) |

Real defect, sheet is a stub but the TOTAL formula references empty cells. Should be `0` or omitted.

---

## Sheet 17120 (Applied Instruction)

Total cell H40 = `=U28`. U28 = `=SUM(U26:X27)`. U26 = `=M26+Q26`. U27 = `=$U$26*(M27+Q27)`. M26 = `=Z48`. Z48 = `=SUM(Z46:AC47)`. Z46 = `=H46*R46*V46`. Z47 = `=L47*R47`.

| Block | Total Cell | Formula | Cached | Defect Class | Upstream Defect Cell | Fix Diff |
|---|---|---|---|---|---|---|
| Sheet total | H40 | `=U28` | None | DC1 | U28 | Easy |
| Classroom + NTG | U28 | `=SUM(U26:X27)` | None | DC1, DC5 (sums col X which is empty) | U26, U27 | Easy |
| NSF base | U26 | `=M26+Q26` | None | DC1 | Q26 (None) | Medium |
| NTG conversion | U27 | `=$U$26*(M27+Q27)` | None | DC1 | Q27 (None) | Medium |
| Classroom NSF | M26 | `=Z48` | None | DC1 | Z48 | Easy |
| Classroom area | Z48 | `=SUM(Z46:AC47)` | None | DC1, DC5 | Z46, Z47 | Easy |
| General academic | Z46 | `=H46*R46*V46` | None | DC1 | H46, R46, V46 (literal seats and allowance values) | Easy |
| Hands-on mockup | Z47 | `=L47*R47` | None | DC1 | L47, R47 | Easy |

Single-block sheet (M13020 only). Real defect, none structural; cached values stripped, sheet computes if recalculated.

---

## Sheet 21451 (Auto Org Shop)

Total cell H44 = `=N24`. N24 = `=SUM(B24:M24)`. Block totals at row 24: B24 (Maint Bays) = `=Q32`, F24 (Admin Sppt) = `=414*M33^0.854`, J24 (Direct Sppt) = `=IF(M33<=14, 347*M33+1129, 22*M33+5706)`. Bay roll-up M32 = `=SUM(M28:P31)`. M28-M31 delegate to AB173 / AB304 / AB435 / AB566.

| Block | Total Cell | Formula | Cached | Defect Class | Upstream Defect Cell | Fix Diff |
|---|---|---|---|---|---|---|
| Sheet total | H44 | `=N24` | None | DC1 | N24 | Easy |
| Row roll-up | N24 | `=SUM(B24:M24)` | None | DC1, DC5 (only B24, F24, J24 carry values; sum range covers empty C, D, E, G, H, I, K, L, M) | block totals | Easy |
| Maint bays GSF | B24 | `=Q32` | None | DC1 | Q32 | Medium |
| Q32 bay GSF | Q32 | `=M33*((Z28*Z29)+Z27)*Z30` (Z28=34, Z29=16, Z30=1.33 NTG, Z27=Z28*Z29/2) | None | DC1 | M33 | Medium |
| Admin Sppt | F24 | `=414*M33^0.854` | None | DC4 (regression, no inputs visible in the same artifact; Apex Omega Sec.8.4 violation) | M33 plus undocumented constants | Medium |
| Direct Sppt | J24 | `=IF(M33<=14, 347*M33+1129, 22*M33+5706)` | None | DC4 | M33 plus undocumented constants | Medium |
| Bay total | M32 | `=SUM(M28:P31)` | None | DC1, DC5 | M28..M31 | Easy |
| Bay rounded | M33 | `=ROUNDUP(M32,0)` | None | DC1 | M32 | Easy |
| M28261 bays | M28 | `=AB173` | None | DC1 | AB173 | Medium |
| M28263 bays | M29 | `=AB304` | None | DC1 | AB304 | Medium |
| M28262 bays | M30 | `=AB435` | None | DC1 | AB435 | Medium |
| Block 4 (orphan) | M31 | `=AB566` | None | DC7 (no UIC label in B31/E31) | AB566 | Hard |
| H&S region | AB173 | `=SUM(AB51:AD87)+SUM(AB93:AD129)+SUM(AB136:AD172)` | None | DC1, DC5 | per-TAMCN AB cells | Medium |
| SURG A region | AB304 | `=SUM(AB182:AD218)+SUM(AB224:AD260)+SUM(AB267:AD303)` | None | DC1, DC5 | per-TAMCN AB cells | Medium |
| SURG B region | AB435 | `=SUM(AB313:AD349)+SUM(AB355:AD391)+SUM(AB398:AD434)` | None | DC1, DC5 | per-TAMCN AB cells | Medium |
| Block 4 region | AB566 | `=SUM(AB444:AD480)+SUM(AB486:AD522)+SUM(AB529:AD565)` | None | DC1, DC5, DC7 | per-TAMCN AB cells | Hard |
| Per-row TAMCN VLOOKUPs (B51-B79+, restricted range $H$1:$Y$749) | E51..E79+ | `=IFERROR(VLOOKUP(Bn,TE!$H$1:$Y$749,2,FALSE),"(Not on TE)")` | None | DC3, DC5 (range cap at row 749 vs TE!max_row=2251) | TE!$H$1:$Y$2251 | Easy |

Real defect locus, F24 and J24 use regression coefficients with no traceable derivation. Per Apex Omega rule 7 (numbers must be traceable) these are flagged TBD pending FC 2-000-05N Table 21420-4 reference. Plus row-749 truncation in VLOOKUP ranges (round-1 finding).

---

## Sheet 21710 (Electronics/Communications Maint Shop)

Total cell H47 = `=AB31`. AB31 = `=SUM(AB27:AE30)`. AB27..AB30 each = `=SUM(M27:AA27)` etc. M27..M31 delegate to S37..S41 admin formulas. M37..M40 are COUNTIFS against TO NOTE column "21710o". L53..L56 are SUMIFS over TE!U:U for net volume. L70..L73 are radio-section COUNTIFS against TO NOTE "21710rs". L79 is maint bay = `=V77*V78`.

| Block | Total Cell | Formula | Cached | Defect Class | Upstream Defect Cell | Fix Diff |
|---|---|---|---|---|---|---|
| Sheet total | H47 | `=AB31` | None | DC1 | AB31 | Easy |
| Sheet roll-up | AB31 | `=SUM(AB27:AE30)` | None | DC1, DC5 (sums col AC, AD, AE which are empty) | AB27..AB30 | Easy |
| Block 1 row sum | AB27 | `=SUM(M27:AA27)` | None | DC1 | M27 | Easy |
| Block 2 row sum | AB28 | `=SUM(M28:AA28)` | None | DC1 | M28 | Easy |
| Block 3 row sum | AB29 | `=SUM(M29:AA29)` | None | DC1 | M29 | Easy |
| Block 4 row sum | AB30 | `=SUM(M30:AA30)` | None | DC1, DC7 | M30 | Hard |
| M28261 admin | M27 | `=S37` | None | DC1 | S37 | Easy |
| M28263 admin | M28 | `=S38` | None | DC1 | S38 | Easy |
| M28262 admin | M29 | `=S39` | None | DC1 | S39 | Easy |
| Block 4 admin | M30 | `=S40` | None | DC1, DC7 | S40 | Hard |
| Block 5 admin | M31 | `=S41` | None | DC9, DC10 (S41 is None, formula references empty cell) | S41 | Hard |
| S37 H&S admin | S37 | `=M37*M$36+P37*P$36` (M36=120, P36=90 GSF/PN) | None | DC1 | M37 | Easy |
| S38 SURG A | S38 | `=M38*M$36+P38*P$36` | None | DC1 | M38 | Easy |
| S39 SURG B | S39 | `=M39*M$36+P39*P$36` | None | DC1 | M39 | Easy |
| S40 block 4 | S40 | `=M40*M$36+P40*P$36` | None | DC1 | M40 | Easy |
| S41 block 5 | S41 | None | None | DC9 (cell empty, M31 references it) | structural fix | Hard |
| Counts H&S "21710o" | M37 | `=COUNTIFS(TO!C:C,"21710o",TO!F:F,B37)` | None | DC2 (TO!C 711/1324 populated; "21710o" tag may be among unpopulated) | TO!C NOTE column | Medium |
| Counts SURG A "21710o" | M38 | `=COUNTIFS(TO!C:C,"21710o",TO!F:F,B38)` | None | DC2 | TO!C NOTE column | Medium |
| Counts SURG B "21710o" | M39 | `=COUNTIFS(TO!C:C,"21710o",TO!F:F,B39)` | None | DC2 | TO!C NOTE column | Medium |
| Counts block 4 "21710o" | M40 | `=COUNTIFS(TO!C:C,"21710o",TO!F:F,B40)` | None | DC2, DC7 | TO!C, B40 unlabeled | Hard |
| Admin grand total | M41 | `=SUM(M37:O40)*M36` | None | DC1, DC5 (sums O col empty), DC5 (multiplies by M36=120 ignoring P-col 90 GSF tier) | M37..M40 | Medium |
| Storage NV H&S | L53 | `=SUMIFS(TE!U:U,TE!D:D,$C$5,TE!G:G,B53,TE!U:U,"<>#N/A")` | None | DC2 (TE!D 506/2251 populated) | TE!D, TE!G NOTE columns | Medium |
| Storage NV SURG A | L54 | `=SUMIFS(TE!U:U,TE!D:D,$C$5,TE!G:G,B54,TE!U:U,"<>#N/A")` | None | DC2 | TE!D, TE!G | Medium |
| Storage NV SURG B | L55 | `=SUMIFS(TE!U:U,TE!D:D,$C$5,TE!G:G,B55,TE!U:U,"<>#N/A")` | None | DC2 | TE!D, TE!G | Medium |
| Storage NV block 4 | L56 | `=SUMIFS(TE!U:U,TE!D:D,$C$5,TE!G:G,B56,TE!U:U,"<>#N/A")` | None | DC2, DC7 | TE!D, TE!G | Hard |
| Radio sect H&S | L70 | `=ROUNDUP((COUNTIFS(TO!C:C,"21710rs",TO!F:F,B70)/15),0)` | None | DC2 | TO!C tag "21710rs" | Medium |
| Radio sect SURG A | L71 | `=ROUNDUP((COUNTIFS(TO!C:C,"21710rs",TO!F:F,B71)/15),0)` | None | DC2 | TO!C | Medium |
| Radio sect SURG B | L72 | `=ROUNDUP((COUNTIFS(TO!C:C,"21710rs",TO!F:F,B72)/15),0)` | None | DC2 | TO!C | Medium |
| Radio sect block 4 | L73 | `=ROUNDUP((COUNTIFS(TO!C:C,"21710rs",TO!F:F,B73)/15),0)` | None | DC2, DC7 | TO!C | Hard |
| Maint bay | L79 | `=V77*V78` (V77=34, V78=16) | None | DC1 | V77, V78 literals | Easy |

Real defect locus, S41 referenced by M31 is empty, breaks the chain into AB30 sum. Plus pipeline-spine: 21710o, 21710rs NOTE tags absent or partial in TO.

---

## Sheet 44112 (Organic Supply Storage)

Total cell H40 = `=AB27`. AB27 = `=SUM(AB25:AE26)+AB28`. AB25..AB28 are row sums. M25 = `=V32`, M26 = `=V33`, M28 = `=V35` (note row 27 skipped, row 34 skipped). V32 = `=M32*$M$31+P32*$P$31+S32*$S$31`. M32..M33, M35 are COUNTIFS against TO NOTE "44112o".

| Block | Total Cell | Formula | Cached | Defect Class | Upstream Defect Cell | Fix Diff |
|---|---|---|---|---|---|---|
| Sheet total | H40 | `=AB27` | None | DC1 | AB27 | Easy |
| Sheet roll-up | AB27 | `=SUM(AB25:AE26)+AB28` | None | DC1, DC5 (skips AB27 itself, OK; but the +AB28 outside the SUM range is irregular) | AB25, AB26, AB28 | Medium |
| Block 1 row sum | AB25 | `=SUM(M25:AA25)` | None | DC1 | M25 | Easy |
| Block 2 row sum | AB26 | `=SUM(M26:AA26)` | None | DC1 | M26 | Easy |
| Block 3 row sum | AB28 | `=SUM(M28:AA28)` | None | DC1 | M28 | Easy |
| H&S admin | M25 | `=V32` | None | DC1 | V32 | Easy |
| SURG A admin | M26 | `=V33` | None | DC1 | V33 | Easy |
| SURG B admin | M28 | `=V35` | None | DC1 | V35 | Easy |
| H&S calc | V32 | `=M32*$M$31+P32*$P$31+S32*$S$31` | None | DC1 | M32, P32 (None), S32 (None) | Medium |
| SURG A calc | V33 | `=M33*$M$31+P33*$P$31+S33*$S$31` | None | DC1 | M33, P33 (None), S33 (None) | Medium |
| SURG B calc | V35 | `=M35*$M$31+P35*$P$31+S35*$S$31` | None | DC1 | M35, P35 (None), S35 (None) | Medium |
| H&S "44112o" count | M32 | `=COUNTIFS(TO!C:C,"44112o",TO!F:F,$B$32)` | None | DC2 | TO!C NOTE | Medium |
| SURG A "44112o" count | M33 | `=COUNTIFS(TO!C:C,"44112o",TO!F:F,$B$33)` | None | DC2 | TO!C NOTE | Medium |
| SURG B "44112o" count | M35 | `=COUNTIFS(TO!C:C,"44112o",TO!F:F,$B$35)` | None | DC2 | TO!C NOTE | Medium |
| Warehouse NV H&S | L46 | `=SUMIFS(TE!U:U,TE!D:D,$C$5,TE!G:G,B46,TE!U:U,"<>#N/A")` | None | DC2 | TE!D, TE!G | Medium |
| Warehouse NV SURG A | L47 | `=SUMIFS(TE!U:U,TE!D:D,$C$5,TE!G:G,B47,TE!U:U,"<>#N/A")` | None | DC2 | TE!D, TE!G | Medium |
| Warehouse NV SURG B | L49 | `=SUMIFS(TE!U:U,TE!D:D,$C$5,TE!G:G,B49,TE!U:U,"<>#N/A")` | None | DC2 | TE!D, TE!G | Medium |
| Personal effects H&S | M69 | `=COUNTIFS(TO!AP:AP,"1",TO!F:F,"M28261")` | None | DC2 (TO!AP deployable flag, may be unpopulated) | TO!AP | Medium |
| Personal effects SURG A | M70 | `=COUNTIFS(TO!AP:AP,"1",TO!F:F,"M28263")` | None | DC2 | TO!AP | Medium |
| Personal effects SURG B | M72 | `=COUNTIFS(TO!AP:AP,"1",TO!F:F,"M28262")` | None | DC2 | TO!AP | Medium |
| Personal effects total | M71 | `=SUM(M69:O72)` | None | DC1, DC5 (sums col O empty; range correctly captures M69..M72) | M69, M70, M72 | Easy |

Real defect locus, P31 / S31 (the 2nd and 3rd tier GSF/PN constants for "44112c" and "44112w") are not populated; only M31 = 120 is set. So even with NOTE tags populated, V32/V33/V35 collapse to just M32 * 120. Plus the "44112c" / "44112w" companion COUNTIFS in P32 / S32 / P33 / S33 / P35 / S35 are absent (those cells are None per the dump).

---

## Sheet 45110 (Open Storage)

Total cell H50 = `=M25`. M25 = `=SUM(B25:K25)`. B25 = `=R32*0.11111` (NSF -> NSY). G25 = `=AA46*0.11111`. R32 = `=SUM(R29:T31)`. R29..R31 = `=Nn*R28`.

| Block | Total Cell | Formula | Cached | Defect Class | Upstream Defect Cell | Fix Diff |
|---|---|---|---|---|---|---|
| Sheet total | H50 | `=M25` | None | DC1 | M25 | Easy |
| Roll-up | M25 | `=SUM(B25:K25)` | None | DC1, DC5 (sums C..F, H..J empty) | B25, G25 | Easy |
| Container NSY | B25 | `=R32*0.11111` | None | DC1 | R32 | Easy |
| Additional NSY | G25 | `=AA46*0.11111` | None | DC10 (AA46 = $AA$55*W46, both AA55 and W46 are None) | AA55, W46 | Hard |
| Containers total NSF | R32 | `=SUM(R29:T31)` | None | DC1, DC5 (sums S, T empty) | R29..R31 | Easy |
| PALCON NSF | R29 | `=N29*R28` | None | DC1 | N29 (literal qty), R28 (literal NSF/stack) | Easy |
| QUADCON NSF | R30 | `=N30*R28` | None | DC1 | N30, R28 | Easy |
| JMIC NSF | R31 | `=N31*R28` | None | DC1 | N31, R28 | Easy |
| H&S PALCON count | M36 | `=SUMIFS(TE!O:O,TE!I:I,'45110'!$M$35,TE!G:G,B36,TE!D:D,$C$5)` | None | DC10 (M35 literal "(none)") | M35 | Hard |
| SURG A PALCON | M37 | (same pattern) | None | DC10 | M35 | Hard |
| SURG B PALCON | M38 | (same pattern) | None | DC10 | M35 | Hard |
| Total containers | M41 | `=SUM(M36:P40)` | None | DC1, DC5 | M36..M38 | Easy |
| Total stacks | M42 | `=ROUNDUP((M41/2),0)` | None | DC1 | M41 | Easy |
| QUADCON F30 | F30 | `=Q42` | None | DC1 | Q42 = `=ROUNDUP((Q41/2),0)`, then Q41 (None per round-1) | Q41 | Hard |
| JMIC F31 | F31 | `=U42` | None | DC1 | U42 = `=ROUNDUP((U41/2),0)`, then U41 (None) | U41 | Hard |

Real defect locus, M35 contains the literal string "(none)" used as a SUMIFS criterion against TE!I:I. This makes M36..M38 zero by construction. Per round-1 finding (report 25_phase_cbis_45110_diff.txt), the sheet was already verified at 8.89 SY because of the working "Additional Storage" branch but the "Shipping Container" branch is dead. Plus AA55 and W46 are empty, so G25 also = 0.

---

## Sheet 61072 (Battalion HQ Admin)

Total cell H40 = `=P30`. P30 = `=SUM(P26:S29)`. P26..P28 = `=Mn * $Y$25` (Y25 = 162.5 GSF/PN). M26 = `=COUNTIFS(TO!D:D,"61072",TO!F:F,$B$26)`. **M27 and M28 reference "61073"**, that is the wrong CCN.

| Block | Total Cell | Formula | Cached | Defect Class | Upstream Defect Cell | Fix Diff |
|---|---|---|---|---|---|---|
| Sheet total | H40 | `=P30` | None | DC1 | P30 | Easy |
| Roll-up | P30 | `=SUM(P26:S29)` | None | DC1, DC5 (sums Q, R, S empty) | P26..P28 | Easy |
| H&S GSF | P26 | `=M26*$Y$25` | None | DC1 | M26 | Easy |
| SURG A GSF | P27 | `=M27*$Y$25` | None | DC8 (M27 counts "61073" not "61072") | M27 | Easy |
| SURG B GSF | P28 | `=M28*$Y$25` | None | DC8 (M28 counts "61073" not "61072") | M28 | Easy |
| Block 4 | P29 | None | None | DC9 (P29 empty but P30 sums to row 29) | P29 | Easy |
| H&S "61072" count | M26 | `=COUNTIFS(TO!D:D,"61072",TO!F:F,$B$26)` | None | DC2 | TO!D CCN col | Medium |
| SURG A | M27 | `=COUNTIFS(TO!D:D,"61073",TO!F:F,$B$27)` | None | DC8 | should be "61072" | Easy |
| SURG B | M28 | `=COUNTIFS(TO!D:D,"61073",TO!F:F,$B$28)` | None | DC8 | should be "61072" | Easy |
| PN total | M30 | `=SUM(M26:O29)` | None | DC1, DC5 | M26..M28 | Easy |

Real defect locus, M27 and M28 use "61073" as CCN criterion, which is wrong: this sheet IS 61072 (BN HQ); the SURG A and SURG B rows should also count "61072" billets per their UIC. This is a copy-paste bug analogous to the round-1 CLB-4 finding "21730 still searching for 21710o".

---

## Sheet 61073 (Co/Battery HQ, design stub)

| Block | Total Cell | Formula | Cached | Defect Class | Upstream Defect Cell | Fix Diff |
|---|---|---|---|---|---|---|
| Sheet total | H40 | `0` (literal) | 0 | DC10 | none, intentional zero | Easy (intentional, sheet is rolled-up note) |

Sheet documents "rolled up to 61072". The literal zero is consistent with that. No defect to repair on this sheet provided 61072 is fixed.

---

# OUTPUT 2, Aggregate Defect-Class Histogram

Across 10 sheets and 124 blocks/sub-blocks examined.

| Defect Class | Count | Sheets affected |
|---|---|---|
| DC1, Cached value stripped on save (no calc engine pass) | 124 (universal) | all 10 sheets |
| DC2, SUMIFS / COUNTIFS criterion against unpopulated TO NOTE / TE D/G column | 28 | 14345, 21710, 44112, 45110, 61072 |
| DC3, IFERROR string fallback masking missing TE row | ~750 row-formulas (across 14312, 14345, 21451) | 14312, 14345, 21451 |
| DC4, Constant-offset / regression formula not derived from inputs (J24=347*M33+1129, F24=414*M33^0.854) | 2 | 21451 |
| DC5, Range mis-sum (sum range overshoots empty columns or undershoots populated rows) | 22 | 14312, 14345, 17120, 21451, 21710, 44112, 45110, 61072 |
| DC6, COUNTIFS hardcodes single UIC ("largest co" = M28261) | 1 | 14345 |
| DC7, Empty/orphan block (no UIC label) referenced by roll-up | 6 | 14312, 14345 (M28262 missing), 21451, 21710, 44112 |
| DC8, Wrong CCN tag in COUNTIFS criterion ("61073" used in 61072 sheet) | 2 | 61072 |
| DC9, Reference to absent supporting cell (target cell empty) | 5 | 17110, 21710 (S41), 44112 (P31, S31, P32 etc.), 61072 (P29) |
| DC10, Literal zero or "(none)" sentinel propagating | 4 | 45110 (M35 = "(none)"), 45110 (AA55/W46 None), 61073 (literal 0) |
| TE column G UIC tag unpopulated for 3d MED BN data (Master TO&E reconciliation issue per report 48) | drives DC2 across 21710 L53-L56, 44112 L46-L49, 45110 M36-M38 | TE sheet, all SUMIFS using TE!G or TE!D |
| TO NOTE column tag unpopulated (711/1324 rows tagged) | drives DC2 across 14345 row-counts, 21710 21710o/21710rs, 44112 44112o, 61072 61072 counts | TO sheet |

## Real-defect summary, one-line fixes (Easy)

1. 14345 H40 double-counts K25, change to `=B25+K25` or `=P25` (not `=P25+K25`).
2. 61072 M27, change criterion `"61073"` to `"61072"`.
3. 61072 M28, change criterion `"61073"` to `"61072"`.
4. 17110 H40, sheet is a stub, replace `=P25+K25` with `0`.
5. 45110 M35, the literal string "(none)" should be the actual PALCON TAMCN code (the cell drives M36..M38 to zero). TBD pending TE PALCON TAMCN identification.

## Real-defect summary, structural (Medium/Hard)

6. 21451 F24 and J24 use undocumented regression coefficients. TBD pending FC 2-000-05N Table 21420-4 reference (per Apex Omega rule 7).
7. 21710 S41 cell is empty; M31 (block 5) references it. Either remove block 5 or populate the analog of S37..S40.
8. 44112 P31, S31 GSF/PN constants for "44112c" (90) and "44112w" (TBD) are not populated; companion P32/S32/P33/S33/P35/S35 COUNTIFS for those tags are absent.
9. 14345 M28262 Surg B armory block is not inserted into the Q-column storage region; B20 notes the relocation but the row was never added.
10. 14312, 21451, 21710, 14345 each have an unlabeled "block 4" / "block 5" row that the roll-up sums but no UIC populates.
11. 21451 VLOOKUP ranges capped at row 749 vs TE max_row 2251 (round-1 finding restated).
12. Pipeline spine (TO column C NOTE tags, TE columns G and D) is the single largest driver of zero output. Layer 2 NOTE-tagging task per `audit/PIPELINE.md`.

## Apex Omega TBD items

- 14312 block 4 (M24 / AB770), purpose unknown, no UIC label. TBD, pending unit-doctrine reference.
- 21451 block 4 (M31 / AB566), same. TBD.
- 21710 block 4 (M30 / S40) and block 5 (M31 / S41), purpose unknown; S41 is empty. TBD.
- 21451 F24 regression `414*M33^0.854`, source not cited inline. TBD, pending FC 2-000-05N Table 21420-4 verification.
- 21451 J24 regression `IF(M33<=14, 347*M33+1129, 22*M33+5706)`, source not cited inline. TBD, pending FC 2-000-05N Table 21420-4 verification.
- 45110 M35 "(none)" sentinel, intent unclear. TBD, pending PALCON TAMCN identification.
- 45110 AA55 and W46, both empty but referenced by G25 chain. TBD, pending sheet-author intent.
- 44112 P31/S31 constants not populated. TBD, pending FC 2-000-05N tier-2/tier-3 office GSF rates.
