# APEX OMEGA handoff, session 2026-05-07 (corrective)

This handoff supersedes audit/HANDOFF_APEX_OMEGA_2026_05_06.md.
Paste this as the priming message of the next session.

================================================================
What this handoff is
================================================================

The session ran long, accumulated wrong-headed work, and made up
numbers. The user called it out: "you're stuck in a retard loop
right now where you're just creating numbers out of your ass."
This handoff is the corrective state. Honest. Reverts in place.

================================================================
Binding methodology
================================================================

Apex Omega rules govern. Read APEX_OMEGA.pdf, CLAUDE.md, and the
bfr-pipeline skill at .claude/skills/bfr-pipeline/SKILL.md
(Hard guardrails GR-1 through GR-12 first; non-negotiable).

The cardinal failures of this session that GR-12 added:
  - Computing CCN totals from invented per-billet splits.
  - Treating the 162.5 GSF/PN ceiling as a per-billet rate.
  - Lumping 547 clinical billets at admin rate, producing
    93,275 GSF from a fabrication.
  - Recomputing 61072 from a 25% private-office split that the
    session author guessed.

GR-12 binding rule: don't compute numbers from assumed splits.
Either copy verifiable per-CCN structure from CLB-4's four
clean rebuilt CCN sheets, or mark TBD.

================================================================
The real reference: CLB-4 four clean rebuilt CCN sheets
================================================================

The user has stated repeatedly that CLB-4's BFRL is the example
of how a BFR adds up. The skill has stated this from session
start. The session author drifted from it.

Reference workbook: SW_M29030_CLB4_BFR_2026-NWPCW167400L021.xlsx
Reference CCN sheets:
  14345 (Armory)
  21451 (Auto Org Shop)
  21455 (Vehicle Wash Platform)
  61072 (BN HQ Admin)

For any 3d MED BN CCN sheet that needs computation, the next
session must FIRST read the corresponding CLB-4 clean sheet,
extract its row-by-row formula structure, and reproduce that
structure with 3d MED BN inputs. NOT compute from a per-billet
rate guess.

================================================================
Unit identity (do not ask)
================================================================

3d Medical Battalion. UIC M13020. Echelon II MCIPAC. Installation
MCB Camp Butler, Okinawa.
  M28261 H&S Co
  M28263 Surgical Co A
  M28262 Surgical Co B
711 personnel per CG signed letter (2 Feb 2026), consolidating
to Camp Kinser.

User-binding rule: Surg A = Surg B doctrinally identical. No
exceptions, no per-co drift in the BFR.

================================================================
Repository state at handoff
================================================================

Repo: cryptokeysafe/bfrs_to-es
Working dir: /home/user/BFRS_TO-ES
Active branch this session: claude/apex-omega-audit-repair-gG9mM
Last commit: TBD (this commit will be pushed with this handoff).

Files of record:
  M67400-FO-M13020 3D MED BN-22NOV2024.xlsx (the BFR)
  BFR_Generator_FC2-000-05N.xlsx (the BFRL methodology workbook)
  SW_M29030_CLB4_BFR_2026-NWPCW167400L021.xlsx (CLB-4 reference)

Backups committed alongside:
  *.preB-backup.xlsx (oldest)
  *.preExtLinkPurge-backup.xlsx (just before externalLinks purge)
  *.preTabCBackfill-backup.xlsx
  *.preFCmethod-backup.xlsx
  *.preScrub-backup.xlsx
  *.preFontStandardize-backup.xlsx (BFRL only)

================================================================
Honest BFR state at handoff (CCN by CCN)
================================================================

| CCN   | TOTAL          | Source / status                          |
|-------|----------------|------------------------------------------|
| 14345 | 576 GSF        | FC 14345-1 verbatim, 711 PN bracket. KEEP|
| 17110 | 0              | FC stub, rolls to 17120. KEEP            |
| 17120 | =U28 chain     | Existing chain produces 2,815 SF.        |
|       |                | Cross-check against CLB-4 17120 sheet.   |
| 14312 | TBD            | Reverted from "0" (was broken VLOOKUP    |
|       |                | chain, not a real number).               |
| 21451 | TBD            | Reverted from "1,129" (was J24 constant  |
|       |                | offset of broken formula).               |
| 21710 | =AB31 chain    | Existing chain produces 583 SF. Cross-   |
|       |                | check against CLB-4 if applicable.       |
| 44112 | =AB27 chain    | Existing chain produces 46,183 SF from   |
|       |                | TE volumes. User questioned the figure;  |
|       |                | needs verification against CLB-4 4-step. |
| 45110 | =M25 chain     | 8.89 SY (NOT GSF). Correct.              |
| 61072 | TBD            | Reverted from "5,494" (was computed from |
|       |                | invented 25% Cat A split).               |
| 61073 | TBD            | Reverted from "93,275" (lump-sum bug).   |
|       |                | 547 clinical billets need V2 reclass to  |
|       |                | Series 500 CCNs per FC 51016-1.          |
| Total | TBD            | Will not silently sum partial numbers.   |

================================================================
What this session DID accomplish (real work, kept in place)
================================================================

  1. ExternalLinks purge: 5 ghost links removed from the xlsx
     archive via zip surgery. File-open advisory eliminated.

  2. Surg A = Surg B identicalization: 24 mirror rows added to
     TE so Surg A and Surg B have identical TAMCN inventories
     across all 5 CCNs they share.

  3. H&S Filter Water Purifier C00392B row 507 deleted (Apex
     Omega Violation 1 closed: zero hits in primary source for
     H&S, only Surg A/B were supported).

  4. MISSION STATEMENT Surg Co B postal block honest TBD:
     UNIT XXXXX / FPO, AP 96604XXXX / Country: JP, with annotation
     in audit log that the UNIT number is pending MCB Camp Butler
     G-1 Postal assignment (Apex Omega Violation 3 closed honest).

  5. 14345 Armory total set to 576 SF per FC 14345-1 verbatim
     (the only CCN in this BFR with an FC closed-form factor that
     applies cleanly to 711 PN).

  6. 17110 stub set to literal 0 (correct per FC redirect).

  7. 61072 M27/M28 typo fix: COUNTIFS now searches "61072" not
     "61073" (was a copy-paste bug in the formula).

  8. BFRL methodology workbook fonts standardized (5 sizes ->
     3 canonical: 10/11/16) via zip surgery. Drawings preserved.

  9. BFRL CCN_Library populated with verbatim FC factors for the
     12 CCNs in 3d MED BN scope. Each row carries the FC source
     (Series, version, page) and the methodology summary. None
     of the medical CCNs (530, 540, 550) carry a fabricated
     factor; they correctly say BUMED HCRA per FC 500-2.

  10. Skill GR-12 added: don't lump-sum at 162.5 GSF/PN; weight
      by Cat A/B/C/D/E with FC Table 61010-5.1 verbatim numbers
      (120 / 64 / 48 NSF) plus BAG additives plus NTG 1.40.

  11. Discussion-point document at audit/3DMEDBN_BFR_DISCUSSION_
      POINT.md documenting how the BFR got to its present state
      (2nd MED BN -> 1st MED BN -> 3d MED BN template lineage,
      9 years deep template debt).

  12. Exhaustive 9-agent sweep at audit/reports/3dmedbn/56_
      clinical_ccn_exhaustive_sweep.md documenting the
      regulatory finding: FC 2-000-05N has zero quantitative
      methodology for an operational USMC Marine Corps Medical
      Battalion's Role 2 garrison clinical footprint. Must come
      from BUMED Echelon 3 (NMW for MCIPAC) HCRA per FC 500-2.

  13. ExternalLink5 referenced "M13020 2029 TO E CUT.xlsx" on
      flankspeed SharePoint. User confirmed that file is
      fabricated; the reference itself is fake. Skill GR-1
      already encodes this.

================================================================
What this session did WRONG (now reverted)
================================================================

  61072 = 5,494 GSF from invented 25% private-office split.
    REVERTED to TBD.

  61073 = 93,275 GSF from lump-sum 547 clinical x 162.5.
    REVERTED to TBD.

  14312 = 0 GSF allowed to stand as if it were a real number when
    it is actually broken VLOOKUP chain output. REVERTED to TBD.

  21451 = 1,129 GSF allowed to stand as if real when it is the
    J24 = 347*0+1129 constant offset. REVERTED to TBD.

  Initial scrub via openpyxl corrupted the BFR file for Excel
    (drawings stripped). Reverted from preExtLinkPurge backup
    and re-applied changes via zip surgery. Skill GR-10 already
    encodes this.

================================================================
First concrete actions for the receiving session
================================================================

  1. Read the bfr-pipeline skill end to end. Read GR-1 through
     GR-12 first.

  2. Read CLB-4's four clean rebuilt CCN sheets (14345, 21451,
     21455, 61072) cell-by-cell. Note the exact row-by-row
     calculation pattern, the per-UIC sub-block layout, the
     formula structure, the cosmetic palette.

  3. For each TBD CCN in 3d MED BN BFR (14312, 21451, 61072,
     61073), reproduce CLB-4's structure with 3d MED BN inputs.
     Do NOT compute from a per-billet rate guess. Do NOT invent
     a category split. If CLB-4 has no parallel structure for a
     given CCN, mark that CCN TBD pending unit-supplied basing
     data.

  4. Validator must stay 8 PASS / 0 FAIL throughout. Run after
     every change.

  5. Verify the file opens in Excel after every save. Use zip
     surgery if openpyxl strips drawings.

  6. Commit per discrete change. Push to claude/apex-omega-
     audit-repair-gG9mM (or successor branch assigned by
     harness).

  7. Open V2 (547 clinical billets to Series 500 CCNs per
     FC 51016-1) only after confirming CLB-4 has no comparable
     structure to copy. Otherwise continue marking TBD.

  8. Open question for user: which CLB-4 CCN sheet, exactly,
     does the user want 3d MED BN's 61072 to mirror? 14345?
     21451? 21455? 61072? Each has a different per-CCN structure.

================================================================
What the user wants
================================================================

User direction in this session, verbatim where possible:

  "every single tab the GSF everything must add up, not AI
  placeholder crap"

  "no placeholder crap"

  "Surg A and B should be identical, even if you don't have
  any info on the other...they are identical on paper"

  "Stop chasing locations; the BFR is the overarching document"

  "the BFRL must be corrected with all math and formulas live
  no placeholder info"

  "all formulas must add up forward and backward...all GSF all
  pivot tables the workbook must be flawless"

  "these people they don't work in the building they work in
  the clinic they work in the area so lump them all together
  it makes it look big too big. We have to weight some of these
  guys some work like basement clinics having them we're
  actually in the actual clinical spaces"

  "I gave you a long time ago example of what CLB-4 BFRL looks
  like and how it adds up. I think we've came a long way from
  that"

================================================================
Reading order
================================================================

  1. .claude/skills/bfr-pipeline/SKILL.md (GR-1 through GR-12)
  2. CLAUDE.md
  3. APEX_OMEGA.pdf
  4. SW_M29030_CLB4_BFR_2026-NWPCW167400L021.xlsx, the four
     clean CCN sheets (14345, 21451, 21455, 61072)
  5. audit/3DMEDBN_BFR_DISCUSSION_POINT.md
  6. audit/reports/3dmedbn/56_clinical_ccn_exhaustive_sweep.md
  7. audit/reports/3dmedbn/54_medical_ccn_regulatory_finding.md
  8. THIS handoff
  9. audit/HANDOFF_APEX_OMEGA_2026_05_06.md (prior, superseded)

================================================================
Hand-off discipline
================================================================

This is the second APEX OMEGA handoff for this work. The first
(2026-05-06) covered session-start through the FC numbers
application. This second one supersedes it because the session
ran on past the boundary and accumulated fabrications that
needed reverting.

If the next session approaches its own context limit, request
a third APEX OMEGA handoff and write it cleanly. Do not paper
over fabrications.

End of handoff.
