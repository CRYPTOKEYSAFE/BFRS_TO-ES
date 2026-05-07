# Apex Omega handoff, 3d MED BN BFR audit and repair

Paste this as the priming message of the next Claude Code session.
Self-contained, no clarifying questions required.

================================================================
Binding methodology
================================================================

Apex Omega rules govern every output. Read APEX_OMEGA.pdf and
CLAUDE.md at repo root before any deliverable. Non-negotiables:
facts only, no speculation, verify line by line, current
authoritative sources only, mark TBD pending source where you
cannot verify, no em dashes / en dashes / asterisk bold / dash
separators, plain prose, lead with the answer, no preamble.

================================================================
Unit identity (do not ask)
================================================================

Tenant: 3d Medical Battalion. UIC M13020.
Echelon II: MCIPAC. Installation: MCB Camp Butler, Okinawa.
Subordinate companies: M28261 H&S, M28263 Surg A, M28262 Surg B.
Surg B is administratively in the BFR. CG signed letter dated
2 Feb 2026 confirms 711 personnel and consolidation at Camp
Kinser; MT/UT and MSTC have already physically moved to Kinser,
the rest of the unit is still at Camp Foster. Current correct
nomenclature is MCB Camp Butler with MCIPAC as the Echelon II.

================================================================
Repository state at handoff
================================================================

Repo: cryptokeysafe/bfrs_to-es
Working dir: /home/user/BFRS_TO-ES
Active branch (this session): claude/usmc-bfr-audit-repair-0YYwt
Last commit: 9553f7d (revert corrupt recalc + add this handoff)
Prior commits this session, in order:
  0d358e9 hook fix: CLAUDE_PROJECT_DIR default + ruflo first
  54e2668 hook simplify: tighten comments, drop subshell
  2cf9c80 violations 1 and 3 partial close
  3bdb87f violation 3 corrected (Camp Kinser primary source)
  9f4ceef strip placeholder narratives, match sheet convention
  cd5738f LibreOffice headless recalc + GSF reconciliation
  c3a6c7c CG signed letter OCR
  9553f7d revert corrupt recalc, add HANDOFF_NEXT_SESSION.md

Next session: harness will assign a fresh claude/* branch name.
Base it from claude/usmc-bfr-audit-repair-0YYwt (the branch above)
since main is behind. Either:
  git checkout -b <new-branch> origin/claude/usmc-bfr-audit-repair-0YYwt
or merge claude/usmc-bfr-audit-repair-0YYwt into the new branch on
first action. Never push to main.

================================================================
Authoritative BFR file
================================================================

M67400-FO-M13020 3D MED BN-22NOV2024.xlsx at repo root.
GitHub (this branch):
  https://github.com/cryptokeysafe/bfrs_to-es/blob/claude/usmc-bfr-audit-repair-0YYwt/M67400-FO-M13020%203D%20MED%20BN-22NOV2024.xlsx
GitHub (raw download):
  https://github.com/cryptokeysafe/bfrs_to-es/raw/claude/usmc-bfr-audit-repair-0YYwt/M67400-FO-M13020%203D%20MED%20BN-22NOV2024.xlsx

This file is the reverted (pre-recalc) version. Cached TOTAL
values are None until opened in Excel; fullCalcOnLoad=True is
set so Excel will recalc on open. Do not run LibreOffice
-convert-to xlsx on this file; that round-trip corrupts the
workbook for Excel even though openpyxl reads the output.

Backup (do not modify): M67400-FO-M13020 3D MED BN-22NOV2024.preB-backup.xlsx
GitHub:
  https://github.com/cryptokeysafe/bfrs_to-es/blob/claude/usmc-bfr-audit-repair-0YYwt/M67400-FO-M13020%203D%20MED%20BN-22NOV2024.preB-backup.xlsx

================================================================
Validator state
================================================================

Run: python3 pipeline/validate.py "M67400-FO-M13020 3D MED BN-22NOV2024.xlsx"
Last result: 8 PASS / 0 FAIL.
Validator checks format only (schema, NOTE coverage, error tokens,
roll-up integrity). It does not verify factual accuracy or doctrinal
correctness.

================================================================
Per-CCN GSF state, post-recalc
================================================================

  CCN     TOTAL                  STATUS
  -----   --------------------   ----------------------------------
  14312       0.00 GSF           BROKEN, fix required
  14345    6,110.08 GSF          OK
  17110       0.00 GSF           DESIGN STUB (rolls into 17120)
  17120    2,815.45 GSF          OK
  21451    1,129.00 GSF          PARTIAL, equipment side returns 0
  21710      583.32 GSF          PARTIAL, officers count 0
  44112   46,182.74 GSF          OK
  45110        8.89 GSF          BROKEN, factor and chain wrong
  61072   69,875.00 GSF          QUESTIONABLE, sweeps clinical at admin rate
  61073       0.00 GSF           CRITICAL, 574 billets routed here, hardcoded zero
  -----   --------------------
  SUM    126,704.48 GSF          unreliable; defensible portion approx 56,000 GSF

Full chain dump: audit/reports/3dmedbn/44_gsf_audit_full.txt
Per-defect findings: audit/reports/3dmedbn/44_gsf_findings.txt

================================================================
Open Apex Omega violations (carried from commit 9a01d01)
================================================================

Violation 1, PARTIAL.
  TE row 507 H&S C00392B FILTER WATER PURIFI qty 180 was a
  same-battalion mirror of Surg A and Surg B. There is no H&S
  TFSMS export and there is not going to be one. The whole H&S
  TE side is 198 inherited rows from the 2017 NAVFAC MIDLANT
  template baseline, not a primary 3d Med Bn source. Re-source
  all 198 rows is the real fix.

Violation 2, OPEN.
  574 clinical platoon billets are routed to CCN 61073 (Co HQ
  Admin) which holds the literal value 0 in H40 = 0 SF. They
  are also captured by 61072 rows 27-29 at the BN HQ admin rate
  of 162.5 SF per Marine, inflating 61072 to 69,875 SF (430
  Marines worth of admin space for an admin staff of 39).
  Fix: add an FC Series 500 medical CCN to CCN_Library
  (likely 53010 Dispensary / Outpatient Clinic; verify against
  fc_2_000_05n_500series_03_17_2023.pdf), re-route the 574
  clinical billets out of 61073 NOTE into the new Series 500
  NOTE, and remove the 61072 sweep on those Marines.

Violation 3, CLOSED.
  MISSION STATEMENT B208 / B210 / B211 now match the sheet's
  postal-block convention (UNIT 38445 / FPO, AP 963734500 /
  Country: JP). Surg B routes to the battalion HQ FPO since
  it is consolidating into 3d Med Bn facilities at Camp Butler.

Violation 4, OPEN.
  CG signed letter primary source extracted this session
  (audit/reports/3dmedbn/45_cg_letter_findings.txt). 711
  personnel confirmed; BFR has 710. Reconcile the 1-billet gap.
  Workspace requirement is in CG letter enclosure (2) "Proposed
  Facilities Layout" which is not directly identified in the
  repo by name. Candidates: POM26 PDF, Tab B decision brief.
  Until that document is in hand, the GSF back-test is per-
  doctrine sanity only (162.5 SF admin Marine, 90 SF junior
  enlisted, 120 SF officer); CCN 14312 / 45110 / 21451 / 21710
  defects from violation 4 work overlap with the per-CCN
  defects above.

================================================================
Per-CCN repair items (priority order)
================================================================

P1 (do first): CCN 61073 = 0 with 574 billets routed.
  Either approach acceptable, structural ratification needed:
    Option A: add FC Series 500 medical CCN sheet, re-route
      classifier rule 7 (UIC M28263 / M28262 default 61073)
      to route clinical-section billets to the new CCN.
    Option B: replace 61073 H40 = 0 with a real COUNTIFS x SF
      formula matching the 61072 pattern, accepting that admin
      rates are not the right doctrinal rate for clinical
      platoons (this is a stop-gap, not a real fix).

P2: CCN 14312 = 0 GSF. VLOOKUP IFERROR fallback is "0" (string)
  not 0 (number); chain collapses. Verify TE rows tagged 14312
  populate cols T/U/V/W (length/width/height/volume); fix the
  IFERROR fallback to a number.

P3: CCN 45110 = 8.89 GSF. R29 chain returns 0 (F29 = M42 = 0).
  R32 = 80 from R30 or R31 outside the chain; identify source.
  Confirm 0.11111 is intentional SF to SY conversion.

P4: CCN 21451 equipment side = 0. M28 = AB173 chain returns 0;
  determine why and repair.

P5: CCN 21710 = 583 SF. Officers count returns 0. Connect H&S
  radio/electronics TE rows to the equipment-driven half.

P6: CCN 61072 = 69,875 SF. After violation 2 fix, the M27/M28/
  M29 rows (clinical sweep) should produce 0; only P26 (39 BN
  admin Marines x 162.5 = 6,337.5 SF) should remain.

H&S T/E re-source: 198 rows of inherited M28261 equipment lack
  a primary source. Either obtain a 3d Med Bn Master TO&E
  extract for H&S or accept the inherited values with explicit
  documentation that they descend from the 2017 NAVFAC MIDLANT
  template via 2nd Med Bn.

================================================================
Source documents in repo (do not re-discover)
================================================================

Methodology and FC source:
  APEX_OMEGA.pdf                                binding briefing
  fc_2_000_05n_100series_02_11_2026.pdf         current
  fc_2_000_05n_200series_05_16_2025.pdf         current
  fc_2_000_05n_300series_03_02_2023.pdf         (training, not used)
  fc_2_000_05n_400series_11_19_2025.pdf         current
  fc_2_000_05n_500series_03_17_2023.pdf         MEDICAL, needed for Violation 2
  fc_2_000_05n_600series_03_02_2023.pdf         current
  fc_2_000_05n_700series_11_19_2025.pdf         current
  fc_2_000_05n_800series_03_31_2025.pdf         current
  fc_2_000_05n_appendixa.pdf                    1060-CCN vocabulary
  BFR_Generator_FC2-000-05N.xlsx                methodology workbook

Unit-data sources for 3d MED BN:
  M28262_3dMedSurgB.xlsx                        Surg B TFSMS, structure 02/03/2026
  M28263_3dMedSurgA.xlsx                        Surg A TFSMS, structure 02/03/2026
  3DMLG_ASR.xlsx                                master ASR; sheet "3D MED BN"
                                                 has 206 rows, BIC structure
                                                 only, no equipment columns
  H&S TFSMS                                     DOES NOT EXIST in repo, will
                                                 not exist; H&S TE side is
                                                 inherited template residue

Reference / context:
  M67400-FO-M13020 3D MED BN-22NOV2024.pdf      pre-repair PDF render of older BFR
  3d Med Bn Strat Basing Req CG SIGNED (004).pdf
                                                 OCR'd this session, 711 confirmed
                                                 enclosure (2) "Proposed Facilities
                                                 Layout" not directly identified
  Tab A - Endorsement Letters                   Surg B endorsement chain
  Tab B - Bravo Surgical Decision Brief         possibly CG letter encl (1)
  Tab C - Basing Assessment Aug 2025            input document
  CG Endorsement Surg Co B G-5 Basing Action v1.docx
                                                 paragraph 19 names Camp Kinser
                                                 buildings: 107 BN HQ co-use,
                                                 300 MSTC, 613 MT/UT, 400 armory
                                                 bay, 1225 housing, 508 supply
  3D MED BN Footprint as of Jan 2026 .pdf/.pptx current state, FOS-215, FOS-5717,
                                                 FOS-5628, KIN-300; reference only
  E_BFR_F_PRC_BU26-5836R_POM26_20260228_2_OF_2.pdf
                                                 POM26 part 2 of 2; possibly
                                                 contains proposed facility
                                                 layout for Violation 4 back-test
  RE_ CG MCIPAC Endorsement Request.pdf         email thread context
  FW_ CG MCIPAC Endorsement Request 2026-04-30.eml

Worked example (NOT this unit, cosmetic reference only):
  SW_M29030_CLB4_BFR_2026-NWPCW167400L021.xlsx
                                                 CLB-4 BFR with 4 clean rebuilt
                                                 CCN sheets (14345, 21451,
                                                 21455, 61072); typography
                                                 source per audit/STYLE_GUIDE.md

================================================================
Pipeline and audit infrastructure (already authored)
================================================================

  pipeline/validate.py                  Layer 6 validation harness
  audit/CLASSIFICATION_RULES.yaml       Layer 3 BMOS-to-CCN rule table
  audit/UNIT_TYPE_DEFAULTS.yaml         per-unit-type admin_ccn defaults
  audit/PIPELINE.md                     six-layer contract spec
  audit/FINDINGS.md                     round 1-2 forensic findings
  audit/STYLE_GUIDE.md                  cosmetic discipline rules
  audit/PLANNING_FACTORS.{yaml,json}    extracted FC factors
  audit/CCN_VOCABULARY.json             1060 CCNs from FC Appendix A

Skill: .claude/skills/bfr-pipeline/SKILL.md (Track 10e covers
prior session; this session's tracks not yet appended).

================================================================
Diff and audit log artifacts from this session
================================================================

  audit/reports/3dmedbn/41_violations_1_and_3_diff.txt
  audit/reports/3dmedbn/41_validator_post_violations_1_3.txt
  audit/reports/3dmedbn/42_kinser_correction_diff.txt
  audit/reports/3dmedbn/42_validator_post_kinser_correction.txt
  audit/reports/3dmedbn/43_strip_placeholders_diff.txt
  audit/reports/3dmedbn/43_validator_no_placeholders.txt
  audit/reports/3dmedbn/44_gsf_audit_full.txt
  audit/reports/3dmedbn/44_gsf_findings.txt
  audit/reports/3dmedbn/45_cg_letter_findings.txt
  audit/reports/3dmedbn/45_cg_signed_letter_ocr_p1.txt
  audit/reports/3dmedbn/45_cg_signed_letter_ocr_p2.txt

================================================================
Sandbox environment (do not re-install)
================================================================

Already installed in this sandbox:
  python3 + openpyxl + et-xmlfile
  poppler-utils (pdftotext, pdftoppm)
  tesseract-ocr
  libreoffice-calc (headless recalc works)
  pdfplumber installed but cryptography binding broken; use
    pdftoppm + tesseract for image-only PDFs instead
  ruflo binary at /opt/node22/bin/ruflo v3.7.0-alpha.7

If you start in a fresh sandbox, the session-start hook (fixed
this session) will install ruflo on its own. If openpyxl is
missing, pip install openpyxl.

================================================================
Ruflo activation
================================================================

The .mcp.json at repo root registers ruflo via 'npx -y
ruflo@latest mcp start' so it auto-downloads on session start
even without the global binary. The hook fix
(.claude/hooks/session-start.sh) installs the binary globally
to make startup faster.

Verification at session start:
  bash -c 'echo CLAUDE_CODE_REMOTE=$CLAUDE_CODE_REMOTE; which ruflo; ruflo -version'
  Expected: CLAUDE_CODE_REMOTE=true, /opt/node22/bin/ruflo,
            ruflo v3.7.0-alpha.7

If 'mcp__ruflo__*' tools appear in the deferred-tool list, ruflo
is live and you can use its agent orchestration. If they do not
appear, restart the session once and they should appear on the
second start. Do not paper over a non-live ruflo by claiming it
works; report and continue without it.

================================================================
What to do first (no questions)
================================================================

1. Run the validator to confirm 8 PASS / 0 FAIL still.
2. Open audit/reports/3dmedbn/44_gsf_findings.txt for the per-CCN
   GSF defect list.
3. Open audit/reports/3dmedbn/45_cg_letter_findings.txt for the
   CG signed letter primary source.
4. Start with Violation 2: read fc_2_000_05n_500series_03_17_2023.pdf,
   identify the right Series 500 CCN(s) for an MLG medical
   battalion clinical platoon (likely 53010 Dispensary / Outpatient
   Clinic), and propose the structural change. The user has
   directed that structural changes need ratification, so
   propose with FC citation before adding the sheet.
5. After Violation 2, work through P2 (14312), P3 (45110), P4
   (21451), P5 (21710), P6 (61072) per the priority list above.
6. After all CCN math is repaired, do Violation 4 back-test
   against the CG letter (711 personnel) and against any GSF
   data found in the POM26 PDF or Tab B brief. If the user
   supplies CG letter enclosure (2) "Proposed Facilities Layout",
   that is the gold back-test source.

================================================================
Things the user has said this session, durable
================================================================

  - 711 people in the BN per CG signed letter (verified).
  - "every single tab the GSF everything must add up, not AI
    placeholder crap" (no zero TOTALs masquerading as design,
    no bracketed TBDs in cell text, no unit-conversion bugs).
  - "we are not stuck on where the unit is at right now ... we
    need the BFR correct so we can right size the unit into the
    proper facilities" (BFR is a requirements doc, not a status
    tracker; do not put relocation narrative in MISSION STATEMENT).
  - "no placeholder crap" (strip TBD-pending bracketed text from
    cells; flag in audit logs and commit messages, not in the
    workbook itself).
  - H&S TFSMS does not exist and will not exist; do not wait on it.
  - Use ruflo for the structural / multi-step work in next session.
  - Stop chasing locations; the BFR is the overarching document.
  - Do not ask 90 questions at session start.

End of handoff.
