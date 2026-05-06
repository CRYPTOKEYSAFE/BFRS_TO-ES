# 3d MED BN BFR Investigation Findings (no edits, forensic only)

This document answers the three open questions the user asked
before any repair work begins. Sources cited inline.

## Q1. Where does Surg Co C come from?

**Finding: it is not 3d MED BN.** It is template residue from a
Camp Lejeune medical battalion BFR.

Evidence:

- The four hidden CCN sheets (14312, 21451, 21710, 45110) each
  list the same four subordinate UICs and labels:

  | UIC | Label |
  |---|---|
  | M28271 | H&S Co |
  | M28272 | Surgical Co A |
  | M28273 | Surgical Co B |
  | M28275 | Surgical Co C |

- 3d MED BN's actual current UICs per the ASR
  (`3DMLG_ASR.xlsx`, sheet `3D MED BN`, row 6 to row 207) are:

  | UIC | Label | FY26 BIC count |
  |---|---|---|
  | M28261 | H&S Co | 250 |
  | M28262 | Surgical Co B (currently in Hawaii, returning) | 180 |
  | M28263 | Surgical Co A (currently on Okinawa) | 179 |

  Total 609 BICs. No M28271, M28272, M28273, or M28275 exist
  for 3d MED BN. No Surg Co C exists.

- Three of the four hidden sheets still list the installation as
  Camp Lejeune (`audit/reports/3dmedbn/09_hidden_sheets_deepdive.txt`):

  | Sheet | Installation | Installation UIC |
  |---|---|---|
  | 14312 | MCB Camp Butler | M67400 |
  | 21451 | MCB Camp Lejeune | M67001 |
  | 21710 | MCB Camp Lejeune | M67001 |
  | 45110 | MCB Camp Lejeune | M67001 |

  Camp Lejeune is the East Coast home of 2nd Medical Battalion.
  M67001 is the Camp Lejeune installation UIC. M67400 is MCB
  Camp Butler.

- The workbook's external link 3 points at
  `\\mcuspndlfs44\CPEN_GF\cpen_pwd\IR TEAM OASIS\BFR\1stMED BN BFR 2025\1ST MED BN M11020_BFR UNIT EDIT_04MAY2018.xlsx`.
  That is 1st Medical Battalion's BFR at Camp Pendleton from
  May 2018.

**Lineage reconstructed: this BFR is the third copy in a chain.**

```
2nd MED BN (Lejeune, M67001)
    -> 1st MED BN (Pendleton, M11020) on 04 MAY 2018
        -> 3d MED BN (MCB Camp Butler, M67400) on 22 NOV 2024
```

Each copy partially updated identifiers. Sheet 14312 got its
installation field flipped to MCB Camp Butler / M67400 in the
3d MED BN copy. Sheets 21451, 21710, and 45110 never got
touched, so they still say MCB Camp Lejeune. None of the hidden
sheets had their subordinate UIC tables updated; they all still
reference M28271/72/73/75 with a Surg Co C, which is the
2nd Med Bn structure that was never relevant to 1st Med Bn or
3d MED BN.

**Recommendation: Surg Co C and the M2827x UIC block can be
removed from this BFR with confidence. They have nothing to do
with 3d MED BN.** The repair work is to either rebuild the four
hidden CCN sheets with 3d MED BN's correct UICs (M28261,
M28262, M28263), or remove them entirely if the underlying CCN
calculations are not needed for 3d MED BN.

## Q2. Do the hidden CCN sheets pertain to 3d MED BN?

**Finding: the topics yes; the data no.**

The four hidden CCN sheets each cover a category that 3d MED BN
plausibly needs:

| CCN | Topic | Doctrinal relevance to 3d MED BN |
|---|---|---|
| 14312 | Operational Vehicle Laydown Area | Yes. 3d MED BN has tactical vehicles (M997 ambulances, JLTV ambulances, MTVRs, JLTVs, trailers, generators) per Tab A page 16. They need a laydown area. |
| 21451 | Automotive Organizational Shop | Yes. The Motor T and Utilities section needs maintenance space. |
| 21710 | Electronic / Communications Maintenance Shop | Marginal. Depends on whether 3d MED BN has enough comm equipment to justify its own shop, or whether it shares with H&S Co support. |
| 45110 | Open Storage Area | Yes. Class VIII storage and shipping container laydown. |

So the topics are valid. The data inside each sheet is wrong. It
references the 2nd / 1st MED BN UIC structure, not 3d MED BN.

**Two repair options:**

A. **Rebuild each hidden sheet** with 3d MED BN's actual UICs
   (M28261, M28262, M28263), corrected installation field
   (MCB Camp Butler / M67400), corrected subordinate row
   labels (H&S Co, Surg Co A, Surg Co B; no Surg Co C), and
   recalculated TAMCN pulls from the TE tab. Then unhide them
   and add UNIT_ROLLUP rows so they flow to the total. This
   matches the CLB-4 round-1 recommendation in
   `audit/FINDINGS.md`.

B. **Remove the hidden sheets entirely** from this BFR. If those
   CCNs are needed downstream, the existing BFR pipeline
   (`pipeline/template.py`, `pipeline/etl.py`) can regenerate
   them clean from the 3d MED BN TFSMS exports plus
   `audit/CCN_VOCABULARY.json` plus `audit/PLANNING_FACTORS.json`.

Either way, the current hidden sheets are not foundational data
and should not be kept as is.

## Q3. The dead VLOOKUPs in the TO and TE sheets

**Finding: 3,307 dead VLOOKUPs across two external sheets.**

Counts (`audit/reports/3dmedbn/11_dead_vlookups.txt`):

| Target | Formulas |
|---|---|
| `[5]CCN!$C$7:$D$1098` | 1,959 |
| `[5]TAMCN!` | 1,348 |
| **Total** | **3,307** |

The `[5]` external file is referenced in
`xl/externalLinks/externalLink5.xml.rels` and points at:

```
https://flankspeed-my.sharepoint-mil.us/.../
  MCB Camp Butler MCIPAC FRP FY23/SV#5/Team D - DY EA/
  TO&E/TO E CUT/M13020 2029 TO E CUT.xlsx
```

That is 3d MED BN's own FY29 TFSMS T/O&E cut, stored on
FlankSpeed SharePoint as a working artifact for the FY23 FRP
team. The exposed sheets in that external file are:

```
TO calc, TE calc, Locator_Deck, EQUIP, CCN, MOS, TAMCN, CSP,
TO values, TE values, Camp Lejeune
```

(Note the residual `Camp Lejeune` sheet name on the FY29 TO&E
cut. The Camp Lejeune lineage reaches into the SharePoint
artifacts too.)

**What the VLOOKUPs do:**

- `=VLOOKUP(D5,[5]CCN!$C$7:$D$1098,2,FALSE)` (TO sheet, column E)
  takes the CCN code in column D and returns the CCN
  description from the external CCN reference table.
- The TE sheet uses `[5]TAMCN!` to pull TAMCN descriptions for
  each equipment row.

**Why they are dead:** the external file is not open and not in
the package. Excel cannot resolve the lookup, so every cell
returns `#N/A` and stays cached as `#N/A` across the 3,303
error tokens documented in
`audit/reports/3dmedbn/02_bfr_error_tokens.txt`.

**Repair option:** Replace `[5]CCN!` with an internal sheet
(call it `CCN_Library`) populated from
`audit/CCN_VOCABULARY.json` (1,060 ratified CCNs already in the
repo). Replace `[5]TAMCN!` with a similar internal `TAMCN_Library`
sheet. The internal library can be built from the methodology
workbook (`BFR_Generator_FC2-000-05N.xlsx`) which already has a
CCN library, plus the TAMCN descriptions can come from the
3d MED BN TFSMS exports themselves (each row already has the
TAMCN description in the equipment data). Doing this fix:
- Severs the external dependency (closes finding F3).
- Drops `#N/A` count from 3,303 to near zero (closes finding F2).
- Makes the BFR self-contained and recalc-clean per Apex Omega
  Sec.5.5.

## Q4. Locator_Deck sheet

**Finding: 608-row orphan sheet, referenced by no other sheet
in the workbook.** (`audit/reports/3dmedbn/10_locator_deck.txt`)

Content: an inventory of TAMCNs / NSNs / nomenclature with
location codes like `FRONT CAGE`, `FRONT DECK`, and PAL/QUAD
serial numbers (PRC 036199 etc). Looks like a hand-built
equipment-location tracker, not a BFR calculation input.

The sheet has no references coming in (zero formulas in any
other sheet mention `Locator_Deck`).

**Recommendation: keep, trim, or remove is a low-impact call.**
Removing it cleans up the workbook and breaks nothing. Keeping
it preserves whatever historical equipment-location data the
unit captured. Either way, this is not a foundational BFR
component and does not contribute to any CCN total.

## Q5. The other four external links

For completeness, the workbook has five external link
references (`externalLink1.xml.rels` through
`externalLink5.xml.rels`):

| # | Target | Used for | Status |
|---|---|---|---|
| 1 | `\\naeanrfkfs43\BULK_Storage_4\Users\p0047813\...\Master Asset (2).xls` | Personal file in p0047813's Outlook temp folder | Dead. Never accessible from a current workstation. |
| 2 | `C:\Users\renel.douyon\Desktop\Copy of 19Marine Air Support Squadron_advocate review (002).xlsx` | Wrong unit (MASS, not 3d MED BN) | Dead. Should never have been linked. |
| 3 | `\\mcuspndlfs44\CPEN_GF\cpen_pwd\IR TEAM OASIS\BFR\1stMED BN BFR 2025\1ST MED BN M11020_BFR UNIT EDIT_04MAY2018.xlsx` | The 1st Med Bn ancestor BFR | Dead. The template lineage reference. |
| 4 | `https://mcicom.usmc.mil/MCICOM_IR_OPT/Standard BFRs/2 LAAD/M00146-MS-M19885-20161222.xlsx` | 2 LAAD reference BFR (Dec 2016) | Dead. Unrelated unit. |
| 5 | `https://flankspeed-my.sharepoint-mil.us/.../M13020 2029 TO E CUT.xlsx` | 3d MED BN FY29 TFSMS T/O&E cut | Dead. The CCN and TAMCN library source. |

Only link 5 ever contributed live data. All five should be
severed during the repair.

## Summary of the answers

1. **Surg Co C is not 3d MED BN.** Template residue from a Camp
   Lejeune medical battalion BFR.

2. **The hidden CCN sheets do not pertain to 3d MED BN as
   currently constituted.** The CCN topics are doctrinally
   relevant; the data inside each sheet references the wrong
   unit's UIC structure and (in three of four cases) wrong
   installation. Either rebuild with 3d MED BN data or remove.

3. **The dead VLOOKUPs were pulling CCN and TAMCN descriptions
   from a 3d MED BN FY29 TO&E cut on FlankSpeed SharePoint.**
   Concept is correct (a description lookup); the implementation
   is broken because of the external dependency. Fix is to
   internalize the CCN and TAMCN libraries.

4. **Locator_Deck is an orphan working sheet.** Referenced by
   nothing. Keep, trim, or remove all break nothing.

5. **All five external links are dead.** Only one (link 5) ever
   carried live data.

## What I will do next, only after the user authorizes

I will not change anything until the user reads these findings
and tells me what to do with each item.

The decisions to take, restated cleanly:

- **D2 (Surg Co C):** confirm we strip M28275 and Surg Co C
  references from the four hidden sheets during repair.
- **D4a (hidden sheets):** rebuild with 3d MED BN UICs, or
  remove and let the pipeline regenerate clean later?
- **D5 (Locator_Deck):** keep, trim, or remove?
- **D3 (dead VLOOKUPs):** confirm the internal-library
  replacement strategy (CCN_Library and TAMCN_Library sheets
  copied from the methodology workbook plus the TFSMS exports).
- **D6 (phasing):** still open.
