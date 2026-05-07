# APEX OMEGA handoff, session 2026-05-06

Paste this as the priming message of the next Claude Code session
working on the 3d MED BN BFR.

================================================================
Binding methodology
================================================================

Apex Omega rules govern every output. Read APEX_OMEGA.pdf,
CLAUDE.md, and the bfr-pipeline skill at
.claude/skills/bfr-pipeline/SKILL.md (BEFORE STARTING WORK; the
"Hard guardrails" section at top is non-negotiable).

Non-negotiables: facts only, no speculation, verify line by line,
current authoritative sources only, mark TBD pending source where
you cannot verify, no em dashes / en dashes / asterisk bold,
plain prose, lead with the answer, no preamble.

================================================================
Source hierarchy (do NOT blend)
================================================================

REGULATORY (binding):
  FC 2-000-05N Series 100, 200, 400, 500, 600, 700, 800
    (Series 300 not on the critical path).
  MCO 11000.12.
  UFS 3-701-01.
  UFC 4-510-01 (medical facility design).
  Future: MIL-HDBK-1191; BUMED instruction series for medical.

AUTHORITATIVE PRIMARY SOURCE:
  3DMLG_ASR.xlsx (3d Marine Logistics Group ASR, dated 02/03/2026)
    -> 3D MED BN tab and Page1 raw billet roster.
  2031 Master TO&E v1.1 - 20250411.xlsx (TFSMS-format,
    ASD-published, FY2031 cut)
    -> covers M28261, M28262, M28263 with full L/W/H/Vol/NSY data.
  BFR_Generator_FC2-000-05N.xlsx (BFRL methodology workbook with
    Okinawa adjustments).
  BFR's own MISSION STATEMENT sheet (embedded TFSMS Unit TO&E
    Reports for M28261, M28263, M28262).
  CG signed letter (3d Med Bn Strat Basing Req CG SIGNED, 2 Feb
    2026) -> 711 PN canonical.
  M28262_3dMedSurgB.xlsx, M28263_3dMedSurgA.xlsx
    (TFSMS exports, structure as of 02/03/2026).

PROGRAM-PRACTICE (sanity-check only, NOT authoritative):
  Tab A endorsement letters.
  Tab B 3d MLG Bravo Surgical Decision Brief.
  Tab C basing assessment Surg Co B Aug 2025.
    NOTE: Tab C is scoped to Surg Co B only at Camp Foster.
    The 944 SF / 2,848 SF / 4,063 SF figures are project-practice,
    NOT regulatory. Do NOT use as binding sizing inputs.
  CG MCIPAC Endorsement Request.docx (April 2026 draft).
  3D MED BN Footprint PDF/PPTX.
  Six Kinser building schedules / AE PLUS PDFs.

EXTERNAL BENCHMARK:
  GAO-20-195G, AACE Recommended Practices, JED Cost Guide, JDDG.

================================================================
Unit identity (do not ask)
================================================================

Tenant: 3d Medical Battalion. UIC M13020.
Echelon II: MCIPAC. Installation: MCB Camp Butler, Okinawa.
Subordinate companies:
  M28261 H&S Company       : 288 billets per Master TO&E,
                             290 raw / 250 chargeable per ASR.
  M28263 Surgical Company A: 210 billets per Master TO&E and ASR.
  M28262 Surgical Company B: 211 billets per Master TO&E and ASR.
  Total                    : 711 PN per CG signed letter (raw
                             ASR), 609 per ASR pivot
                             (chargeable BIC).

USER-RATIFIED RULE (BINDING): Surg A and Surg B are doctrinally
identical even when only one has data. "Surg A and B should be
identical, even if you don't have any info on the other...they
are identical on paper."

================================================================
Repository state at handoff
================================================================

Repo: cryptokeysafe/bfrs_to-es
Working dir: /home/user/BFRS_TO-ES
Active branch: claude/apex-omega-audit-repair-gG9mM (this session)
Last commit before handoff write: 5cc3fee (Surg A=B mirror rows).
Validator: pipeline/validate.py "M67400-FO-M13020 3D MED BN-22NOV2024.xlsx"
  -> 8 PASS / 0 FAIL.

Backups:
  M67400-FO-M13020 3D MED BN-22NOV2024.preB-backup.xlsx
  M67400-FO-M13020 3D MED BN-22NOV2024.preExtLinkPurge-backup.xlsx
  M67400-FO-M13020 3D MED BN-22NOV2024.preTabCBackfill-backup.xlsx

Next session: harness will assign a fresh claude/* branch name.
Base it from claude/apex-omega-audit-repair-gG9mM.

================================================================
What is done
================================================================

1. Hook fix: settings.json now registers SessionStart hook so
   ruflo MCP loads automatically on next session start (commit
   3407bdf).

2. ExternalLinks deep purge: 5 ghost references inside the xlsx
   archive removed (xl/externalLinks/* + workbook.xml +
   _rels/workbook.xml.rels + [Content_Types].xml). Excel
   file-open advisory eliminated (commit 50a9094).

3. Apex Omega Violation 1 closed: H&S Co C00392B FILTER WATER
   PURIFI qty 180 deleted. Master TO&E confirms zero hits
   across all 19,001 rows for any 3d MED BN UIC. Surg A and
   Surg B C00392B kept (each supported by their own TFSMS
   COE rule). Readme at
   audit/reports/3dmedbn/53_c00392b_h_and_s_deletion_readme.md
   (commit ecf6725).

4. Surg A=B identicalization: 24 mirror rows added to TE (rows
   507-530) so Surg A and Surg B have identical TAMCN inventories
   across all 5 CCNs (14312, 14345, 21451, 21710, 44112). Drift
   = 0 in both directions post-fix. Commit 5cc3fee.

5. Medical CCN regulatory finding documented: clinical CCN
   sizing (53010, 55010, 55020) requires BUMED Echelon 3 (NMW for
   MCIPAC) HCRA + Program for Design per FC Section 500-2. CCN
   54010 Dental NOT APPLICABLE (no dental billets in 3d MED BN;
   the 27 NEC L31A are MEDICAL LAB TECH not dental). Tab C is
   sanity-check, not authoritative. Per audit/reports/3dmedbn/
   54_medical_ccn_regulatory_finding.md (commit 3b077e5).

6. 10 parallel reading agents executed: per-block CCN formula
   audit, doctrine docs digest, BFR_Generator workbook digest,
   TAMCN backfill mapping, FC per-CCN methodology, ASR
   reconciliation, POM26 + KI building plans, Tab A/B/C +
   footprint, APEX_OMEGA + skill + TFSMS files, CG MCIPAC
   endorsement docx. All findings in audit/reports/3dmedbn/49-54.

7. Skill updated with 11 hard guardrails (GR-1 through GR-11)
   that encode this session's specific failures and corrections.
   Track 11 entry appended to DONE list.

================================================================
What is open
================================================================

V2 Clinical CCN routing.
  574 clinical billets currently routed to CCN 61073 (literal 0
  SF in H40). Doctrinal-correct path: re-route to CCN 53010 NOTE,
  add 53010 sheet to BFR with TOTAL = "TBD pending BUMED NMW
  HCRA per FC 2-000-05N Section 500-2", cite Section 500-1 and
  500-2 verbatim. Layer 2 reclassification deferred until user
  ratifies. The user is researching external sources to find a
  per-clinical-billet SF figure as an interim placeholder.

V3 Surg B postal block.
  MISSION STATEMENT B208 currently reads "FOSTER BUILDING TBD"
  (Apex Omega rule 1 violation, invented placeholder). B210
  reads "OKINAWA, JAPAN (MCB Camp Butler / Camp Foster
  post-relocation)" (also invented). B211 reads "Country: US"
  (should be JP). Two candidate fixes pending user pick:
    Option A (per A=B rule): mirror Surg A address.
      B208 = UNIT 38448
      B210 = FPO, AP   966048448
      B211 = Country: JP
    Option B (per prior Track 10e ratification): mirror BN HQ.
      B208 = UNIT 38445
      B210 = FPO, AP   963734500
      B211 = Country: JP

V4 Back-test against CG letter 711 PN.
  Master TO&E + ASR raw confirm 711. BFR has 710. 1-billet
  delta source not identified. Investigate which UIC is short.

================================================================
The hardcoded "1,129 SF" problem
================================================================

CCN 21451 H44 visibly evaluates to 1,129 SF. Per per-block
agent: that number is the y-intercept of formula
J24 = IF(M33<=14, 347*M33+1129, 22*M33+5706) evaluated at
M33=0. The equipment-side chain returns 0 because column X
"Space Factor" looks up TE col U "Volume Total" which is empty
in the BFR TE. The 1,129 is not a real requirement; it's a
constant offset of a stalled formula.

Fix path: backfill BFR TE Space Factor column from 2031 Master
TO&E (col 22 = Space Factor populated for some TAMCNs), or
mark CCN 21451 TOTAL as "TBD pending engineering study per FC
2-000-05N 21451-3 (v.200.20250516, page 188)" if Master TO&E
Space Factor coverage is insufficient.

================================================================
The "engineering study" CCNs and their FC text verbatim
================================================================

CCN 21451 AUTOMOTIVE ORGANIZATIONAL SHOP
  FC 2-000-05N Series 200, v.200.20250516, page 188:
    "21451-3 Conduct an engineering study to determine
     requirements."
  -> BFR entry: TBD pending engineering study, FC-cited.

CCN 21710 ELECTRONICS/COMMUNICATIONS MAINTENANCE SHOP
  FC 2-000-05N Series 200, v.200.20250516, page 195:
    "21710-3 No specific criteria are provided. An engineering
     evaluation can be conducted to determine the office space
     and support area requirements... For storage area, an
     engineering evaluation can be used to determine the volume
     of material required to be stored. The standard stacking
     height for this type of material is 1.83 meters (6 feet).
     A factor of 1.07 nsm/cm is applied to the volume of
     material to determine the required net square meters
     (m2). A conversion factor of 1.65 for net square meters
     to gross square meters is appropriate."
  -> BFR entry: compute via 1.07 nsm/cm volume x 1.65 NTG
     using Master TO&E volume column for comm equipment, OR
     mark TBD pending engineering evaluation.

CCN 53010 DISPENSARY AND OUTPATIENT CLINIC
  FC 2-000-05N Series 500, v.500.20231703, page 6:
    "53010-1 GENERAL. Free Standing Clinic, outpatient clinic,
     which occupies a building or part of a building, but is
     not physically located with a hospital or medical center
     that provides routine and emergency care to authorized
     personnel."
  No factor table. No engineering-study language. Sizing flows
  to FC Section 500-2:
    "The BUMED Echelon 3 command Project Officers will develop
     explicit planning documents for future year projects,
     including a Healthcare Requirements Analyses (HCRA),
     Economic Analyses (EA)..."
  -> BFR entry: TBD pending BUMED NMW HCRA. Cite FC Section
     500-1 and 500-2 verbatim on the sheet's footer. Apply
     Table 500-1 net-to-gross 1.35 (or 1.60 for surgery, 1.25
     for pathology) at delivery.

CCN 55010, 55020. Same regulatory path as 53010.

================================================================
The CCN sheets that DO have FC factors
================================================================

CCN 14345 ARMORY (FC 100, v.100.20260211, page 205):
  Table 14345-1 step function on Installation Military Strength.
  For 711 PN: bracket "up to 2,000" = 576 SF total for the BN.
  This is BN-WIDE total, not per-co. Tab C 944 SF/co is NOT
  authoritative.

CCN 14312 OPERATIONAL VEHICLE LAYDOWN AREA (FC 100, page 189):
  Table 14312-1 Type Code A-G. For each vehicle, classify by
  length: A <10ft = 19 GSY (1.50 NTG); B 10-20ft = 32 GSY (1.75);
  C 20-30 = 46 (1.75); D 30-40 = 59 (2.00); E 40-50 = 72 (2.00);
  F 50-60 = 86 (2.25); G 60-70 = 99 (2.25).
  Compute from Master TO&E vehicles, L,Ft column.

CCN 44112 STORAGE OF AIR OR GROUND ORGANIC UNITS, MARINE CORPS
  (FC 400, page 46): redirects to FC 440-2.2.1 4-Step Method.
  Step 1 Total Cubic Feet, Step 2 Stacking Height, Step 3
  NSF = Vol/SH, Step 4 GSF = NSF x NTG factor.
  Compute from Master TO&E Volume_Total column filtered to
  organic-storage TAMCNs.

CCN 45110 OPEN STORAGE AREA (FC 400, page 50): 4-Step Method,
  default SH = 4 ft. Output unit is SY (square yards), NOT GSF.
  The L50 cell label correctly says "SY".

CCN 17120 APPLIED INSTRUCTION BUILDING (FC 100, pages 298-299):
  Broad planning factor 150 GSF per student station. The
  current sheet computes 2,815 SF; matches Tab C as
  cross-check.

CCN 61072 BATTALION/SQUADRON HEADQUARTERS, MARINE CORPS
  (FC 600, page 37): redirects to CCN 610-10 Admin BFR Generator.
  Per BFR_Generator workbook: 162.5 SF/Marine for senior admin.
  39 BN admin Marines x 162.5 = 6,338 SF.

CCN 61073 COMPANY/BATTERY HEADQUARTERS, MARINE CORPS (FC 600,
  pages 37-38): same redirect to 610-10. ~12 true Co HQ admin
  Marines x 162.5 = 1,950 SF. Clinical 574 reroutes OUT to
  CCN 53010 (V2).

================================================================
Okinawa adjustments from BFR_Generator workbook
================================================================

  Okinawa_Navy_ACF       2.34   (UFS 3-701-01 Tbl 4-1, FY26)
  Okinawa_Sust_ACF       2.10
  Esc_Factor             1.00   (update at FY release)
  Contingency            1.05
  SIOH                   1.065  (OCONUS Japan)
  PD_Factor              1.09   (1.13 for medical CCNs)
  HF                     1.00   (TBD)

Programmed cost formula:
  Programmed = Bare * Okinawa_Navy_ACF * SIOH * Contingency *
               Esc_Factor * PD_Factor * HF.

================================================================
Apex Omega anti-pattern reminder
================================================================

This session repeatedly violated:
  Rule 1 (facts only) by inventing the words "engineering study"
    for CCN 53010 when FC says nothing of the kind.
  Rule 6 (three-bucket separation) by treating Tab C as
    regulatory.
  Rule 7 (numbers traceable) by accepting the visible 1,129 SF
    on CCN 21451 without inspecting the formula chain.
  Per-instruction "read everything" by asking the user
    questions answerable from files in the repo.

The skill's GR-1 through GR-11 encode the specific corrections.
Read those before starting any work.

================================================================
Reading order for next session
================================================================

  1. .claude/skills/bfr-pipeline/SKILL.md (Hard guardrails
     section first, then everything).
  2. CLAUDE.md.
  3. APEX_OMEGA.pdf.
  4. audit/PIPELINE.md.
  5. audit/reports/3dmedbn/49_per_block_audit.md
     (defect catalog).
  6. audit/reports/3dmedbn/50_doctrine_digest.md
     (10-doc digest).
  7. audit/reports/3dmedbn/51_bfr_generator_digest.md
     (BFRL methodology).
  8. audit/reports/3dmedbn/52_te_backfill_*.{csv,md}
     (TAMCN backfill mapping from Master TO&E).
  9. audit/reports/3dmedbn/53_c00392b_h_and_s_deletion_readme.md.
  10. audit/reports/3dmedbn/54_medical_ccn_regulatory_finding.md.
  11. audit/HANDOFF_NEXT_SESSION.md (prior session handoff).
  12. THIS document, audit/HANDOFF_APEX_OMEGA_2026_05_06.md.

================================================================
First concrete action for next session (no questions)
================================================================

  1. Confirm validator 8/0 on the BFR.
  2. Get user pick on V3 Surg B postal block (A=B mirror
     vs BN HQ mirror). Apply.
  3. Apply easy CCN-sheet bug fixes from per-block audit:
     14345 H40 K25 double-count, 61072 M27/M28 wrong CCN tag,
     17110 H40 stub to literal 0, 45110 M35 "(none)" sentinel.
  4. Backfill BFR TE Space Factor / NSY / NTG / L,Ft / W,Ft /
     H,Ft / Vol_EA / Vol_Tot columns from 2031 Master TO&E
     keyed by (UIC, TAMCN).
  5. Compute FC-method totals per CCN. Write into TOTAL cells.
     Mark engineering-study CCNs TBD with FC citation.
  6. Recalc, re-validate, commit per CCN.
  7. Update SKILL.md Track 11 with progress.

End of handoff.
