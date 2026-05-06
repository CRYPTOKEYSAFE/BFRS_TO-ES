# Per-Block Formula Audit, 3d Med Bn BFR (M67400-FO-M13020 3D MED BN-22NOV2024.xlsx)

Apex Omega rule 1, facts only. Diagnostic only. No file modifications.

## Methodology

Loaded the workbook with openpyxl twice, `data_only=False` (formulas) and `data_only=True` (cached values). Walked all 10 named CCN sheets. Captured per block: total cell, formula, cached value, upstream support cells, most upstream defect.

## Universal observation

The workbook was saved without a calc pass. Every formula cell returns `cached=None`. Once Excel recalculates, structural defects below surface as zeros, blanks, or `#REF!`. Pipeline-spine coverage: TO column C (NOTE) 711/1324 rows, TO column D (CCN) 712/1324, TE column G (UIC) 506/2251, TE column D (CCN) 506/2251. Many SUMIFS / COUNTIFS criteria therefore land on unpopulated rows.

## Defect class legend

- DC1, Cached value stripped (universal).
- DC2, SUMIFS / COUNTIFS criterion against unpopulated TO NOTE / TE D-G column.
- DC3, IFERROR string fallback masking missing TE row.
- DC4, Constant-offset / regression formula not derived from inputs.
- DC5, Range mis-sum (sum overshoots empty columns or undershoots data).
- DC6, COUNTIFS hardcodes single UIC.
- DC7, Empty/orphan block referenced by roll-up.
- DC8, Wrong CCN tag in COUNTIFS criterion.
- DC9, Reference to absent supporting cell.
- DC10, Literal zero or "(none)" sentinel propagating.

---

## Sheet 14312 (Operational Vehicle Laydown)

H36 = `=M25`. M25 = `=SUM(M21:P24)`. Four blocks delegate to AB218/AB402/AB586/AB770; each is a 4-segment SUM(AC..AE) over TAMCN row regions.

| Block | Cell | Formula | DC | Fix |
|---|---|---|---|---|
| Sheet | H36 | `=M25` | 1 | E |
| Roll-up | M25 | `=SUM(M21:P24)` | 1,5 | E |
| M28261 H&S | M21 | `=AB218` (SUM(AC43:AE79)+SUM(AC89:AE125)+SUM(AC135:AE171)+SUM(AC181:AE191)) | 1,5 | M |
| M28263 SRG A | M22 | `=AB402` (analogous SUM over rows 227-372) | 1,5 | M |
| M28262 SRG B | M23 | `=AB586` (analogous SUM over rows 411-556) | 1,5 | M |
| Block 4 orphan | M24 | `=AB770` (analogous SUM over rows 595-740) | 1,5,7 | H |
| Per-row VLOOKUPs (~120) | F43..F79+ | `=IFERROR(VLOOKUP(Cn,TE!$H:$Y,2,FALSE),"(Not on TE)")` | 3 | M |

Real defect, layer 2 TAMCN-NOTE tagging on TE. AC43 row formula = `IFERROR((W43*Y43*AA43),"")`; if TE lookup misses, row collapses to "" and SUM ignores it. All cached = None.

---

## Sheet 14345 (Armory)

H40 = `=P25+K25`. P25 = `=B25+K25`. K25 thus added twice. B25 = `=Q32`. K25 = `=G25*10`. G25 hardcodes M28261.

| Block | Cell | Formula | DC | Fix |
|---|---|---|---|---|
| Sheet | H40 | `=P25+K25` (K25 double-counted) | 1,5 | E |
| Roll-up | P25 | `=B25+K25` | 1,5 | E |
| Storage NSF | B25 | `=Q32` | 1 | E |
| Cleaning | K25 | `=G25*10` | 1,6 | E |
| Largest-co count | G25 | `=COUNTIFS(TO!G:G,"E",TO!F:F,"M28261")` (hardcoded) | 6 | M |
| Storage Q32 | Q32 | `=SUM(Q30:T31)` (Surg B row absent) | 1,5 | M |
| H&S | Q30 | `=M30*$Q$29` (Q29 NTG=1.28) | 1 | E |
| SRG A | Q31 | `=M31*$Q$29` | 1 | E |
| SRG B | absent | not inserted despite B20 endorsement | 7 | H |
| H&S NSF | M30 | `=Z420` = ROUNDUP(SUM(Z370:AC388,Z390,Z392:AC410,Z412:AC419),0) | 1,5 | M |
| SRG A NSF | M31 | `=Z803` = ROUNDUP(SUM(Z753:AC771,Z773,Z775:AC793,Z795:AC802),0) | 1,5 | M |
| Per-row TAMCN (~600) | M47..M79+ | `=SUMIFS(TE!P:P,TE!G:G,$A$43,TE!H:H,An)` | 2 | M |

Real defects, K25 double-count in H40, missing Surg B block, 506/2251 TE UIC tags drive zeros. All cached = None.

---

## Sheet 17110 (Academic Instruction, stub)

| Block | Cell | Formula | Cached | DC | Upstream | Fix |
|---|---|---|---|---|---|---|
| Sheet | H40 | `=P25+K25` | None | 9 (P25, K25 empty) | P25/K25 | E |

Stub, references empty cells. Should be `0` per the body text "rolled up to 17120".

---

## Sheet 17120 (Applied Instruction)

H40 = `=U28`. Single block (M13020).

| Block | Cell | Formula | DC | Fix |
|---|---|---|---|---|
| Sheet | H40 | `=U28` (=SUM(U26:X27)) | 1,5 | E |
| NSF base | U26 | `=M26+Q26` (Q26 None) | 1 | M |
| NTG conv | U27 | `=$U$26*(M27+Q27)` (Q27 None) | 1 | M |
| Classroom NSF | M26 | `=Z48` (=SUM(Z46:AC47), Z46=H46*R46*V46, Z47=L47*R47) | 1,5 | E |

Single-block sheet. No structural defect, all cached = None.

---

## Sheet 21451 (Auto Org Shop)

H44 = `=N24`. N24 = `=SUM(B24:M24)`. Row 24 carries B24 (Bays), F24 (Admin), J24 (Direct).

| Block | Cell | Formula | DC | Fix |
|---|---|---|---|---|
| Sheet | H44 | `=N24` | 1 | E |
| Row roll-up | N24 | `=SUM(B24:M24)` | 1,5 | E |
| Maint Bays | B24 | `=Q32` (=M33*((Z28*Z29)+Z27)*Z30; 34x16 ft, NTG 1.33) | 1 | M |
| Admin Sppt | F24 | `=414*M33^0.854` | 4 | M |
| Direct Sppt | J24 | `=IF(M33<=14,347*M33+1129,22*M33+5706)` | 4 | M |
| Bay total | M32 | `=SUM(M28:P31)` | 1,5 | E |
| Bay rounded | M33 | `=ROUNDUP(M32,0)` | 1 | E |
| H&S bays | M28 | `=AB173` (=SUM(AB51:AD87)+SUM(AB93:AD129)+SUM(AB136:AD172)) | 1,5 | M |
| SRG A | M29 | `=AB304` (analog rows 182-303) | 1,5 | M |
| SRG B | M30 | `=AB435` (analog rows 313-434) | 1,5 | M |
| Block 4 orphan | M31 | `=AB566` (analog rows 444-565) | 7 | H |
| TAMCN VLOOKUPs B51..B79+ | E51..E79+ | `=IFERROR(VLOOKUP(Bn,TE!$H$1:$Y$749,2,FALSE),"(Not on TE)")` (range capped at 749, TE max 2251) | 3,5 | E |

Real defects, F24 / J24 regressions uncited per Apex Omega rule 7. Row-749 truncation (round-1 finding). All cached = None.

---

## Sheet 21710 (Electronics Maint Shop)

H47 = `=AB31`. AB31 = `=SUM(AB27:AE30)`.

| Block | Cell | Formula | Cached | DC | Upstream | Fix |
|---|---|---|---|---|---|---|
| Sheet | H47 | `=AB31` | None | 1 | AB31 | E |
| Roll-up | AB31 | `=SUM(AB27:AE30)` | None | 1,5 (AC,AD,AE empty) | AB27..AB30 | E |
| Block 1 H&S | AB27 | `=SUM(M27:AA27)` | None | 1 | M27 | E |
| Block 2 SRG A | AB28 | `=SUM(M28:AA28)` | None | 1 | M28 | E |
| Block 3 SRG B | AB29 | `=SUM(M29:AA29)` | None | 1 | M29 | E |
| Block 4 orphan | AB30 | `=SUM(M30:AA30)` | None | 1,7 | M30 | H |
| H&S admin | M27 | `=S37` | None | 1 | S37 | E |
| SRG A | M28 | `=S38` | None | 1 | S38 | E |
| SRG B | M29 | `=S39` | None | 1 | S39 | E |
| Block 4 | M30 | `=S40` | None | 1,7 | S40 | H |
| Block 5 | M31 | `=S41` | None | 9 (S41 empty) | S41 | H |
| S37 | S37 | `=M37*M$36+P37*P$36` (M36=120, P36=90) | None | 1 | M37 | E |
| S38 | S38 | `=M38*M$36+P38*P$36` | None | 1 | M38 | E |
| S39 | S39 | `=M39*M$36+P39*P$36` | None | 1 | M39 | E |
| S40 | S40 | `=M40*M$36+P40*P$36` | None | 1 | M40 | E |
| S41 | S41 | None | None | 9 | structural | H |
| H&S 21710o | M37 | `=COUNTIFS(TO!C:C,"21710o",TO!F:F,B37)` | None | 2 | TO!C | M |
| SRG A 21710o | M38 | (same pattern) | None | 2 | TO!C | M |
| SRG B 21710o | M39 | (same pattern) | None | 2 | TO!C | M |
| Block 4 21710o | M40 | (same pattern) | None | 2,7 | TO!C, B40 | H |
| Admin grand | M41 | `=SUM(M37:O40)*M36` | None | 1,5 (only x M36, ignores P36 tier) | M37..M40 | M |
| Storage NV H&S | L53 | `=SUMIFS(TE!U:U,TE!D:D,$C$5,TE!G:G,B53,TE!U:U,"<>#N/A")` | None | 2 | TE!D, TE!G | M |
| Storage NV SRG A | L54 | (same) | None | 2 | TE!D, TE!G | M |
| Storage NV SRG B | L55 | (same) | None | 2 | TE!D, TE!G | M |
| Storage NV blk 4 | L56 | (same) | None | 2,7 | TE!D, TE!G | H |
| Radio sect H&S | L70 | `=ROUNDUP((COUNTIFS(TO!C:C,"21710rs",TO!F:F,B70)/15),0)` | None | 2 | TO!C "21710rs" | M |
| Radio sect SRG A | L71 | (same) | None | 2 | TO!C | M |
| Radio sect SRG B | L72 | (same) | None | 2 | TO!C | M |
| Radio sect blk 4 | L73 | (same) | None | 2,7 | TO!C | H |
| Maint bay | L79 | `=V77*V78` (34, 16) | None | 1 | literals | E |

Real defects, S41 empty breaks block 5. Pipeline NOTE tags 21710o, 21710rs absent or partial.

---

## Sheet 44112 (Organic Supply Storage)

H40 = `=AB27`. AB27 = `=SUM(AB25:AE26)+AB28` (irregular: AB28 outside SUM).

| Block | Cell | Formula | Cached | DC | Upstream | Fix |
|---|---|---|---|---|---|---|
| Sheet | H40 | `=AB27` | None | 1 | AB27 | E |
| Roll-up | AB27 | `=SUM(AB25:AE26)+AB28` | None | 1,5 | AB25, AB26, AB28 | M |
| Block 1 row | AB25 | `=SUM(M25:AA25)` | None | 1 | M25 | E |
| Block 2 row | AB26 | `=SUM(M26:AA26)` | None | 1 | M26 | E |
| Block 3 row | AB28 | `=SUM(M28:AA28)` | None | 1 | M28 | E |
| H&S admin | M25 | `=V32` | None | 1 | V32 | E |
| SRG A admin | M26 | `=V33` | None | 1 | V33 | E |
| SRG B admin | M28 | `=V35` | None | 1 | V35 | E |
| H&S calc | V32 | `=M32*$M$31+P32*$P$31+S32*$S$31` | None | 1,9 (P31, S31, P32, S32 empty) | M31, P31, S31 | M |
| SRG A calc | V33 | `=M33*$M$31+P33*$P$31+S33*$S$31` | None | 1,9 | same | M |
| SRG B calc | V35 | `=M35*$M$31+P35*$P$31+S35*$S$31` | None | 1,9 | same | M |
| H&S 44112o | M32 | `=COUNTIFS(TO!C:C,"44112o",TO!F:F,$B$32)` | None | 2 | TO!C | M |
| SRG A 44112o | M33 | (same) | None | 2 | TO!C | M |
| SRG B 44112o | M35 | (same) | None | 2 | TO!C | M |
| Wh NV H&S | L46 | `=SUMIFS(TE!U:U,TE!D:D,$C$5,TE!G:G,B46,TE!U:U,"<>#N/A")` | None | 2 | TE!D, TE!G | M |
| Wh NV SRG A | L47 | (same) | None | 2 | TE!D, TE!G | M |
| Wh NV SRG B | L49 | (same) | None | 2 | TE!D, TE!G | M |
| PE H&S | M69 | `=COUNTIFS(TO!AP:AP,"1",TO!F:F,"M28261")` | None | 2 | TO!AP deployable flag | M |
| PE SRG A | M70 | `=COUNTIFS(TO!AP:AP,"1",TO!F:F,"M28263")` | None | 2 | TO!AP | M |
| PE SRG B | M72 | `=COUNTIFS(TO!AP:AP,"1",TO!F:F,"M28262")` | None | 2 | TO!AP | M |
| PE total | M71 | `=SUM(M69:O72)` | None | 1,5 | M69, M70, M72 | E |

Real defect, P31 / S31 GSF/PN constants for 44112c (90) and 44112w (TBD) not populated; companion P-col / S-col COUNTIFS absent. V32/V33/V35 collapse to first-tier only.

---

## Sheet 45110 (Open Storage)

H50 = `=M25`. M25 = `=SUM(B25:K25)`. B25 = `=R32*0.11111` (NSF -> NSY).

| Block | Cell | Formula | Cached | DC | Upstream | Fix |
|---|---|---|---|---|---|---|
| Sheet | H50 | `=M25` | None | 1 | M25 | E |
| Roll-up | M25 | `=SUM(B25:K25)` | None | 1,5 | B25, G25 | E |
| Container NSY | B25 | `=R32*0.11111` | None | 1 | R32 | E |
| Additional NSY | G25 | `=AA46*0.11111` | None | 10 (AA55 None, W46 None) | AA55, W46 | H |
| Containers NSF | R32 | `=SUM(R29:T31)` | None | 1,5 | R29..R31 | E |
| PALCON | R29 | `=N29*R28` | None | 1 | literals | E |
| QUADCON | R30 | `=N30*R28` | None | 1 | literals | E |
| JMIC | R31 | `=N31*R28` | None | 1 | literals | E |
| H&S PALCON | M36 | `=SUMIFS(TE!O:O,TE!I:I,'45110'!$M$35,TE!G:G,B36,TE!D:D,$C$5)` | None | 10 (M35 = "(none)" string) | M35 | H |
| SRG A PALCON | M37 | (same) | None | 10 | M35 | H |
| SRG B PALCON | M38 | (same) | None | 10 | M35 | H |
| Total cont. | M41 | `=SUM(M36:P40)` | None | 1,5 | M36..M38 | E |
| Total stacks | M42 | `=ROUNDUP((M41/2),0)` | None | 1 | M41 | E |
| QUADCON F30 | F30 | `=Q42` | None | 1 | Q41 (None) | H |
| JMIC F31 | F31 | `=U42` | None | 1 | U41 (None) | H |

Real defect, M35 is the literal string "(none)" used as a SUMIFS criterion, so M36..M38 = 0 by construction. AA55 and W46 also empty. Note: round-1 verified the sheet at 8.89 SY through the additional-storage branch; the container branch is dead.

---

## Sheet 61072 (Battalion HQ Admin)

H40 = `=P30`. P30 = `=SUM(P26:S29)`. P26..P28 = `=Mn * Y25` (Y25 = 162.5 GSF/PN).

| Block | Cell | Formula | Cached | DC | Upstream | Fix |
|---|---|---|---|---|---|---|
| Sheet | H40 | `=P30` | None | 1 | P30 | E |
| Roll-up | P30 | `=SUM(P26:S29)` | None | 1,5 | P26..P28 | E |
| H&S GSF | P26 | `=M26*$Y$25` | None | 1 | M26 | E |
| SRG A GSF | P27 | `=M27*$Y$25` | None | 8 | M27 | E |
| SRG B GSF | P28 | `=M28*$Y$25` | None | 8 | M28 | E |
| Block 4 | P29 | None | None | 9 | P29 absent | E |
| H&S 61072 cnt | M26 | `=COUNTIFS(TO!D:D,"61072",TO!F:F,$B$26)` | None | 2 | TO!D | M |
| SRG A | M27 | `=COUNTIFS(TO!D:D,"61073",TO!F:F,$B$27)` | None | 8 (should be "61072") | TO!D criterion | E |
| SRG B | M28 | `=COUNTIFS(TO!D:D,"61073",TO!F:F,$B$28)` | None | 8 (should be "61072") | TO!D criterion | E |
| PN total | M30 | `=SUM(M26:O29)` | None | 1,5 | M26..M28 | E |

Real defect, M27 and M28 use "61073" as CCN criterion. Copy-paste bug analogous to round-1 CLB-4 finding "21730 still searching for 21710o".

---

## Sheet 61073 (Co/Battery HQ, stub)

| Block | Cell | Formula | Cached | DC | Upstream | Fix |
|---|---|---|---|---|---|---|
| Sheet | H40 | `0` literal | 0 | 10 | none, intentional | E |

Body text states "rolled up to 61072". Literal zero is consistent.

---

# OUTPUT 2, Aggregate Defect-Class Histogram

124 blocks/sub-blocks examined across 10 sheets.

| Defect Class | Count | Sheets affected |
|---|---|---|
| DC1, Cached value stripped on save | 124 (universal) | all 10 |
| DC2, SUMIFS / COUNTIFS against unpopulated TO NOTE / TE D/G | 28 | 14345, 21710, 44112, 45110, 61072 |
| DC3, IFERROR string fallback masking missing TE row | ~750 row-formulas | 14312, 14345, 21451 |
| DC4, Constant-offset / regression formula uncited | 2 | 21451 (F24, J24) |
| DC5, Range mis-sum (overshoots empty cols) | 22 | 14312, 14345, 17120, 21451, 21710, 44112, 45110, 61072 |
| DC6, COUNTIFS hardcodes single UIC ("largest co" = M28261) | 1 | 14345 |
| DC7, Empty/orphan block referenced by roll-up | 6 | 14312, 14345, 21451, 21710, 44112 |
| DC8, Wrong CCN tag in COUNTIFS criterion | 2 | 61072 (M27, M28) |
| DC9, Reference to absent supporting cell | 5 | 17110, 21710 (S41), 44112 (P31, S31, etc.), 61072 (P29) |
| DC10, Literal zero / "(none)" sentinel propagating | 4 | 45110 (M35), 45110 (AA55/W46), 61073 |
| TE column G UIC tag unpopulated (Master TO&E reconciliation) | drives DC2 across 21710 L53-L56, 44112 L46-L49, 45110 M36-M38 | TE sheet |
| TO NOTE column tag unpopulated (711/1324) | drives DC2 across 14345, 21710 (21710o, 21710rs), 44112 (44112o), 61072 | TO sheet |

## One-line fixes (Easy)

1. 14345 H40 double-counts K25, change to `=B25+K25` (drop the +K25 outside).
2. 61072 M27, change `"61073"` to `"61072"`.
3. 61072 M28, change `"61073"` to `"61072"`.
4. 17110 H40, replace `=P25+K25` with `0`.
5. 45110 M35, replace `"(none)"` with the actual PALCON TAMCN code (TBD pending TE PALCON identification).

## Structural fixes (Medium/Hard)

6. 21451 F24 and J24 use undocumented regression coefficients. TBD pending FC 2-000-05N Table 21420-4.
7. 21710 S41 cell empty; M31 references it. Either remove block 5 or populate analog.
8. 44112 P31, S31 GSF/PN constants for "44112c" / "44112w" not populated; companion P/S col COUNTIFS absent.
9. 14345 M28262 Surg B armory storage row not inserted despite B20 endorsement.
10. 14312, 21451, 21710, 14345 each have an unlabeled "block 4/5" the roll-up sums but no UIC populates.
11. 21451 VLOOKUP ranges capped at row 749 vs TE max_row 2251 (round-1 finding).
12. Pipeline spine (TO column C NOTE tags, TE columns G and D) is the largest single driver of zero output. Layer 2 NOTE-tagging task per `audit/PIPELINE.md`.

## Apex Omega TBD items

- 14312 block 4 (M24 / AB770), 21451 block 4 (M31 / AB566), 21710 blocks 4-5 (M30 / S40, M31 / S41), purpose unknown, no UIC label. TBD pending unit doctrine.
- 21451 F24 `414*M33^0.854` and J24 `IF(M33<=14,347*M33+1129,22*M33+5706)`, source not cited inline. TBD pending FC 2-000-05N Table 21420-4 verification.
- 45110 M35 "(none)" sentinel. TBD pending PALCON TAMCN identification.
- 45110 AA55 and W46 empty but referenced by G25 chain. TBD pending sheet-author intent.
- 44112 P31 / S31 second- and third-tier office GSF rates not populated. TBD pending FC 2-000-05N tier rates.
