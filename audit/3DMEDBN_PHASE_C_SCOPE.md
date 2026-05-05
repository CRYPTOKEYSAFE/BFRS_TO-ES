# 3d MED BN BFR, Phase C scope and retag proposal

Source workbook: `M67400-FO-M13020 3D MED BN-22NOV2024.xlsx` at HEAD
98fc297 on `claude/resume-bfr-pipeline-nrRNC`.
Methodology: Apex Omega. Every retag below is grounded in FC
2-000-05N text, every quoted line traceable to PDF and page. No
guessing. Items that need SME ratification are marked
`TBD pending [source/action]`.

This document does not edit the BFR. It is the per-row mapping I
will execute in Phase C only after explicit user ratification of
each bucket.

## What changed since the handoff scope statement

The handoff stated 175 rows to retag (36+134+5). Live workbook
reads 170: 36 under 21820, 129 with literal `CSP`, 5 cleared from
former `#N/A`. The 5-row delta from 134 to 129 between the handoff
text and the live file is consistent with the B.7 commit
(fe7cba6) clearing 134 literal `#N/A` strings to live formulas
plus the 5 cleared `#N/A` in col D. Numbers below use the live
129+36+5 = 170 figure.

## FC 2-000-05N text relevant to retag candidates

### CCN 21820 CONSTRUCTION/WEIGHT HANDLING EQUIPMENT SHOP (SF)
Source: fc_2_000_05n_200series_05_16_2025.pdf p. 199, current as of
16 May 2025.

> 21820-2 Included in this category are special construction
> and utility shops for Marine Corps units. These shops are
> normally part of the Headquarters Battalion, Force Service
> Regiment, and the Fleet Marine Force (FMF) Engineer
> Battalions. Conduct an engineering study to determine
> requirements.

Implication for 3d MED BN. The category does cover utility
shops in FMF organizations, but 3d MED BN is not an Engineer
Battalion, FSR, or HQBN. The 36 rows currently tagged 21820 are
not maintenance shop floor space; they are the medical battalion's
organic utility equipment used to power and water its forward
field hospital. The category is wrong for these items at this
unit type.

### CCN 14312 OPERATIONAL VEHICLE LAYDOWN AREA (SY)
Source: fc_2_000_05n_100series_02_11_2026.pdf p. 189, current as of
11 Feb 2026.

> 14312-2 ... The equipment requiring storage can range from
> towable generator sets or light packs to large flatbed
> trailers.

Direct match for towable generator sets, towable pump units, and
ISO-container batch plants in 3d MED BN's TE.

### CCN 44112 STORAGE OF AIR OR GROUND ORGANIC UNITS, MARINE CORPS (SF)
Source: fc_2_000_05n_400series_11_19_2025.pdf p. 46, current as of
19 Nov 2025.

> 44112-1 DESCRIPTION. This category code includes general
> purpose storage facilities assigned to Marine Corps bases,
> air installations and Fleet Marine Force (FMF) units for
> organic requirements to include Division/Wing,
> Battalion/Group and Company/Squadron storage areas, Special
> Service storerooms, base shipping and receiving functions
> and any other organic storage requirements.

Catch-all for unit organic equipment storage that is not weapons
(14345) and not vehicle laydown (14312). Direct match for ECUs,
water tanks, distribution panels, bath units, water purification
units, tools, and analyzers stored under cover when not in
operational use.

### CCN 45110 OPEN STORAGE AREA (SY)
Source: fc_2_000_05n_400series_11_19_2025.pdf p. 50, current as of
19 Nov 2025.

Outdoor uncovered storage. Sized in square yards. Used for
weather-tolerant items that do not justify covered storage.

### CCN 14345 ARMORY (SF)
Source: fc_2_000_05n_100series_02_11_2026.pdf p. 205, current as of
11 Feb 2026. Already present in the BFR; canonical CLB-4 worked
example.

Holds weapons and weapons accessories. Optics, suppressors,
small-arms carriers, and helmets are typically armory-side.

### CCN 21451 AUTOMOTIVE ORGANIZATIONAL SHOP (SF)
Source: fc_2_000_05n_200series_05_16_2025.pdf p. 188.

Vehicle-side maintenance space. Vehicle modification kits and
vehicle-specific organic gear can map here.

## Bucket A. 36 rows currently tagged CCN 21820, proposed retag

The 36 rows split cleanly into two groups by FC 14312-2 versus FC
44112-1 language. My proposal is to retag per the categorization
below.

| Subgroup | Count | Items | Proposed CCN | FC citation |
|---|---|---|---|---|
| GENSET (towable/skid-mounted) | 6 | B00437B MEP-1050, B00777B MEP-1030, B07307B MEP831A, B10217B MEP-1070 (3 instances) | 14312 | 100s p.189 "towable generator sets" |
| CONTAINERIZED BATCH PLANT (ISO container) | 1 | B00667B 34240300M-1 | 14312 | 100s p.189 "long term storage of specialized vehicles and equipment" |
| PUMP UNIT SET (skid-mounted) | 1 | B16207B SL-3-00970D | 14312 | 100s p.189 "light packs to large flatbed trailers" |
| ECU / REFRIGERATION | 8 | B00087B AC (3 instances), B00497B SB541.0, B00612E CREK-M, B00757B SB531.0 (2 instances), 1 add'l B00087B variant | 44112 | 400s p.46 "any other organic storage requirements" |
| WATER TANK (rigid 3000 gal + collapsible fabric) | 7 | B21307B, B21307BB (3 instances), B21307BD (3 instances) | 44112 | 400s p.46 "Battalion/Group ... storage areas" |
| POWER DISTRIBUTION PANEL | 5 | B00277B 5KW indoor, B00287B 5KW outdoor, B00297B 15KW, B00307B 30KW, B00317B DB350MA | 44112 | 400s p.46 |
| FIELD BATH UNIT (MK64 MOD5) | 3 | B00557B (3 instances) | 44112 | 400s p.46 |
| WATER PURIFICATION | 2 | B00077B (2 instances) | 44112 | 400s p.46 |
| TOOL KIT | 2 | B00622E lineman's TK-1141, K79022B refrigeration PAC3521 | 44112 | 400s p.46 |
| ANALYZER ELECTRICAL | 1 | B70012G 434/AN | 44112 | 400s p.46 |

Total. 8 rows to 14312, 28 rows to 44112. Both target sheets are
already in the workbook with TOTAL REQUIREMENT cells feeding
UNIT_ROLLUP, so no new sheets are needed. The 14312 sheet
currently picks up zero TE rows; after this retag it will pick up
8 rows (the towable engineer items).

Open question for SME (TBD pending unit-doctrine confirmation):
3d MED BN's actual building layout at MCB Camp Butler (Foster 215,
5717, 5628; Kinser 300) does not include a 21820-style utility
shop under the unit. The above retag assumes the equipment is
stored organic-unit style, which matches the current footprint.
If 3d MED BN actually maintains a distinct Construction/Utility
shop space at any of its current buildings, some items may
legitimately stay with 21820. Confirm with unit POC.

## Bucket B. 129 rows currently tagged literal `CSP`

`CSP` is not a real CCN. It is a TFSMS source-sheet name (Combat
Service Pack / per-Marine personal equipment) that propagated into
the BFR's TE column D as a placeholder during a prior import. The
129 items are individual Marine personal load and combat gear:
body armor inserts, helmets, magazines, optics, suppressors, gas
masks, decon kits, cold-weather clothing, sleeping systems, packs,
canteens, IFAKs.

By nomenclature category (counts):

| Category | Count | Examples |
|---|---|---|
| INDIVIDUAL PERSONAL CLOTHING | 48 | spectacles, drawers, gloves, jackets, sleeping mats |
| INDIVIDUAL LOAD GEAR | 28 | field packs, pouches, canteens, intrenching tools |
| CBRN | 18 | M8 paper, decon kits, NBC glove inserts, JSGPM mask kit |
| WEAPONS AND ACCESSORIES | 12 | small arms carriers, helmets ECH, optics, magazines |
| OTHER (no clear category) | 10 | unnamed items, modular sleep system |
| FIELD SHELTER / CONTAINER | 7 | tarpaulins, JMIC collapsible containers, two-man tent |
| FABRICATION / OUTERSHELL | 4 | TACFAB tactical fabrication, APECS 3rd-gen rain shell |
| MEDICAL | 2 | IFAK individual first aid kit |

Doctrine framing. Per current TM and FM convention, individual
combat-load equipment (body armor, helmet, packs, canteens,
clothing) is issued to and carried by the Marine; it is not a
facility-driver because it does not require a building when in
use. Reserve and replacement quantities held at the unit level
are organic-unit storage and fall under 44112. Weapons and
weapons accessories not in active use are armory-side (14345).

The four reasonable retag policies for these 129 rows are listed
below. I am not recommending one without ratification because the
choice is doctrinal, not data-hygiene.

| Policy | Treatment | Effect on BFR |
|---|---|---|
| B-i. Conservative all-44112 | Tag all 129 to 44112 | 44112 GSF requirement grows by ~129 line items |
| B-ii. Split by category | 12 weapons-related to 14345; 7 shelter/container to 45110 (open storage); remaining 110 to 44112 | All three CCNs grow modestly |
| B-iii. Remove from TE | Delete the 129 rows entirely (rationale, individual Marine gear, not facility-driving) | TE shrinks to 374 rows; 44112 unchanged |
| B-iv. Defer | Leave tagged `CSP` and produce a footnote in the BFR explaining the convention | TE stays as-is; BFR must carry an explicit caveat |

My read is that B-ii is closest to FC convention and to how
CLB-4's worked-example 14345 sheet is built (the CLB-4 14345 holds
small arms accessories explicitly), but I will not commit to it
without ratification.

## Bucket C. 5 rows cleared from `#N/A`, currently CCN col D = None

| Row | UIC | TAMCN | Nomenclature | Status | Qty | Proposed CCN | Rationale |
|---|---|---|---|---|---|---|---|
| 379 | M28262 | E02122B | MID-RANGE PRECISION DAY OPTIC (MR PDO) | PL | 0 | 14345 | weapon optic, armory item |
| 401 | M28262 | M00112B | MODIFICATION KIT, VE | IS | 3 | 21451 | M-prefix vehicle modification kit |
| 426 | M28262 | C00102F | CARRIER, SMALL ARMS | IS | 180 | 14345 | small-arms carrier vest, armory-side |
| 461 | M28262 | E02012M | SUPPRESSOR, SMALL ARMS | IS | 0 | 14345 | weapon accessory, armory-side |
| 478 | M28262 | C02182B | DECONTAMINATION KIT | IS | 4 | 44112 | CBRN organic-unit gear |

All five are Surg Co B (M28262). The retag rationale is
nomenclature-based and traceable. No guessing on these five.

## Bucket D. 3 TFSMS COE TAMCNs missing per surgical co

Source documents searched:
- `M28262_3dMedSurgB.xlsx` sheets: Header, TO, Billet Summary,
  RecapMOS, RecapMCC, Footnotes, Primary Only, X-78, COE,
  Task Organized T_E (2026-02-03 export).
- `M28263_3dMedSurgA.xlsx` sheets identical.

| TAMCN | Nomenclature | Primary Only qty (per co) | COE chargeability rule | Disposition |
|---|---|---|---|---|
| C00392B | FILTER, WATER PURIFICATION (41207) | 180 (IS) | All ERAAs Excludes DMFA, WRMR, MCPPN, MPF | Add to BFR TE. Tag = 44112 (organic spare for B00077B water purification unit). |
| C02222F | HELMET, GROUND TROOP HC ECH | 0 (IS) | All Artillery/Missile/Rocket Units (no HQ Btry, no Reg); Per E00272G SBNVG; MACS ATC Marine Mobile Team | Correctly absent. 3d MED BN matches none of the COE rules. Document and close. |
| C02472Z | JOINT SERVICE GENERAL PURPOSE MASK, FIELD (M50) | 180 (PL) | All ERAAs Type Support Code (CBRN EQP COE); MARFOR HQ; MARSOC; MCESG; MCIPAC CBRN IPE COE; specific UICs | TBD pending verification: is 3d MED BN's COE TSC `CBRN EQP COE`? If yes, add at qty 180 per co with CCN 44112. |

ERAA acronym: TBD pending source. Appears in the TFSMS COE
chargeability sheet without expansion. Proceeding will require
either an ERAA glossary reference or an explicit user ratification
of whether 3d MED BN qualifies. Not a guess.

## Bucket E (downstream, not Phase C). UNIT_ROLLUP refresh

After Phase C retags, the 14312 sheet will pick up its first
real TE rows (8 from Bucket A.GENSET/PUMP/CONTAINERIZED). The
14312 TOTAL REQUIREMENT formula must be re-verified to confirm it
sums those 8 rows correctly. The 45110 sheet may pick up rows from
Bucket B.ii (7 shelter/container items) if the user selects
policy B-ii. UNIT_ROLLUP totals at R19 will recompute on file
open via fullCalcOnLoad=True.

## What I will not do without explicit ratification

- I will not retag any of the 170 rows above without your
  per-bucket choice.
- I will not delete any TE rows (Bucket B option iii).
- I will not add the C00392B or C02472Z rows to TE without
  explicit add-and-tag confirmation.
- I will not silently fill the ERAA/TSC question for C02472Z.

## Decision matrix you need to ratify

| Bucket | Decision needed |
|---|---|
| A | Approve the 8-to-14312 / 28-to-44112 mapping per the table above, OR override per item, OR ask for unit-doctrine confirmation first. |
| B | Choose B-i, B-ii, B-iii, or B-iv. |
| C | Approve all 5 row-by-row tags, or override per row. |
| D | C00392B: add to TE at qty 180 per co with CCN 44112. C02222F: leave absent and document. C02472Z: ratify ERAA/TSC question or hold. |
| order | Phase C in this session, or stop after ratification and resume next session for execution? |
