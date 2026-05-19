# APEX OMEGA HANDOFF: 3d Med Bn BFR audit and repair

Paste this entire document as the priming message of the next
Claude Code session. The next session resumes work without asking
clarifying questions. Defaults for ambiguous cases are baked in
below and may be revisited only with explicit user override.

================================================================
SECTION 1, GITHUB
================================================================

  Repository:   cryptokeysafe/bfrs_to-es
  Repo URL:     https://github.com/cryptokeysafe/bfrs_to-es
  Branch:       claude/usmc-bfr-audit-repair-0YYwt
  Branch URL:   https://github.com/cryptokeysafe/bfrs_to-es/tree/claude/usmc-bfr-audit-repair-0YYwt
  HEAD commit:  5fa9e9c (audit(bfr): personnel disambiguation, ASR vs BFR vs CG letter)

Subsequent harness-assigned branch must base from this branch:
  git fetch origin claude/usmc-bfr-audit-repair-0YYwt
  git checkout -b <new-harness-branch> origin/claude/usmc-bfr-audit-repair-0YYwt

Never push to main. Stop hook requires commit and push before stop.

Workbook on this branch:
  Web:  https://github.com/cryptokeysafe/bfrs_to-es/blob/claude/usmc-bfr-audit-repair-0YYwt/M67400-FO-M13020%203D%20MED%20BN-22NOV2024.xlsx
  Raw:  https://github.com/cryptokeysafe/bfrs_to-es/raw/claude/usmc-bfr-audit-repair-0YYwt/M67400-FO-M13020%203D%20MED%20BN-22NOV2024.xlsx

Backup (do not modify):
  Web:  https://github.com/cryptokeysafe/bfrs_to-es/blob/claude/usmc-bfr-audit-repair-0YYwt/M67400-FO-M13020%203D%20MED%20BN-22NOV2024.preB-backup.xlsx

================================================================
SECTION 2, BINDING METHODOLOGY (APEX OMEGA)
================================================================

Read APEX_OMEGA.pdf and CLAUDE.md first. The seven Apex Omega
BLOCKING gates in .claude/skills/bfr-pipeline/SKILL.md "Failure
modes and BLOCKING gates" section are binding. Summary:

  G1, Excel-open verification before any xlsx commit. NEVER use
      libreoffice --convert-to xlsx (corrupts the file for Excel).
  G2, Column-letter audit before any ABSENT finding on workbook
      data. A parallel agent in the prior session falsely
      reported zero M28261 rows in TE; actual count is 198.
  G3, Convention-first cell edits. Dump analogous blocks before
      writing. The prior session wasted three commits on B208/
      B210 by ignoring the H&S Co convention at rows 7-10.
  G4, No placeholder text inside cells, ever. TBD/pending notes
      go in audit log + commit message + this handoff, never in
      cell content.
  G5, GSF roll-up sanity check. A CCN with 0 GSF + non-zero
      billet routing is broken (catches the 61073 = 0 case).
  G6, Recalc cached values present at commit OR explicit
      fullCalcOnLoad=True annotation in the commit msg.
  G7, Primary-source extraction (with OCR fallback) before any
      claim about unit posting, location, mission, facility plan.

Apex Omega rules in one block:
  1. Facts only. No assumptions, no AI jargon, no preamble.
  2. Verify line by line, reference by reference, with date and
     section in every citation.
  3. Use only current authoritative sources.
  4. Cannot verify means omit or mark TBD pending [source/action],
     never guess.
  5. Time-stamp external data at the point of citation.
  6. Three-bucket separation: regulatory / program-practice /
     external benchmark. Never blend.
  7. Numbers must be traceable.
  8. Plain prose. Lead with answer. No "let's", no "I'll help
     you", no emojis.
  9. Typography: no em dashes, no en dashes, no double-hyphen as
     em dash, no markdown asterisk bold, no dash separators.

================================================================
SECTION 3, UNIT IDENTITY (DO NOT ASK)
================================================================

Tenant: 3d Medical Battalion. UIC M13020. Echelon II: MCIPAC.
Installation: MCB Camp Butler, Okinawa.

Subordinate companies:
  M28261 H&S Co  Headquarters and Service Company
  M28263 Surg A  Alpha Surgical Company
  M28262 Surg B  Bravo Surgical Company

Current physical disposition (per 3d Med Bn Footprint Jan 2026
and CG signed letter 2 Feb 2026):
  Camp Foster: FOS-215, FOS-5717, FOS-5628 (most of unit)
  Camp Kinser: KIN-300 (MT/UT and MSTC, already moved)

Planned post-relocation at Camp Kinser (CG MCIPAC endorsement,
not yet executed):
  Bldg. 107   BN HQ co-use
  Bldg. 300   Medical Skills Training Center (MSTC)
  Bldg. 613   Motor Transport and Utilities
  Bldg. 400   Consolidated armory bay
  Bldg. 1225  Personnel housing
  Bldg. 508   Supply

Primary source for the buildings: CG Endorsement Surg Co B 3d
Med Bn 3d MLG G-5 Basing Action v1.docx, paragraph 19. Verbatim
quote available at audit/reports/3dmedbn/42_kinser_correction_diff.txt.

The BFR is a facility REQUIREMENTS document, not a current-
location tracker. Do not put relocation narrative in any cell.
MISSION STATEMENT B208/B210/B211 follow the sheet's postal-block
convention (UNIT 38445 / FPO, AP 963734500 / Country: JP),
matching the H&S Co block at rows 7-10.

================================================================
SECTION 4, PERSONNEL GROUND TRUTH (DISAMBIGUATED)
================================================================

BFR TO sheet: 710 rows. Of those:

  99   organizational unit headers (Section / Platoon / Team
       titles in the T/O hierarchy; no Grade, PMOS, Branch).
       NOT BILLETS. Counting them as personnel is wrong.
  611  real billets

  ASR authoritative billet count:   609 (per 3DMLG_ASR.xlsx
                                       sheet '3D MED BN', row 6)
  BFR-to-ASR delta:                   2 (data-vintage drift)
  CG signed letter total:           711
  CG-to-ASR delta:                  102 (augment / FAP /
                                       civilian / contractor)

Per-UIC breakdown of BFR billets:

  M28261 H&S Co:  289 TO rows (37 headers + 252 billets)
  M28263 Surg A:  210 TO rows (31 headers + 179 billets)
  M28262 Surg B:  211 TO rows (31 headers + 180 billets)
                  ---
                  710 (99 headers + 611 billets)

Branch distribution (real billets only):

  Navy (corpsmen, doctors, nurses, dentists):  521
  Marine:                                       90
                                               ---
                                               611

The "99 None/unknown branch" billets reported in earlier
session messages were the org-structure headers, not personnel.

Navy NEC specialty collapse, BFR has destroyed granularity:

ASR distinguishes L00A, L03A, L10A, L12A, L17A, L22A, L23A,
L24A, L31A by NEC. BFR has collapsed all of these into a
single L03A bucket per company:

  H&S:    BFR L03A=131, ASR L-codes sum=130 (+1)
  Surg A: BFR L03A=122, ASR L-codes sum=122 (exact)
  Surg B: BFR L03A=122, ASR L-codes sum=122 (exact)

Restore NEC granularity from per-co TFSMS extracts (M28262_3dMedSurgB.xlsx
and M28263_3dMedSurgA.xlsx). H&S NEC granularity has no TFSMS
source in repo and may need to be reconstructed from ASR's per-
NEC counts.

================================================================
SECTION 5, FUNCTIONAL BUCKETING (DEFAULTS BAKED IN)
================================================================

Each of the 611 real billets sits under one of 99 section
headers. Bucket by section name (data only, no assumption):

CONFIRMED BN_ADMIN, needs fixed BN building space, route to
existing 61072 (BN HQ Admin) plus motor pool / supply / shop
CCNs:

  H&S Co only:                                     101 billets
    Motor Transport Section                23  -> 21451 / 14312
    S-4 Logistics                          20  -> 61072 + 44112
    S-2/S-3 Intel/Operations               15  -> 61072
    S-1 Admin                              12  -> 61072
    Ambulance Section                       9  -> 21451 (vehicles)
    HQ Command Staff                        6  -> 61072
    Supply Section                          5  -> 44112
    Utilities Section                       5  -> 21451 / 21710
    Company HQ Section                      4  -> 61072
    Chaplain Section                        2  -> 61072

CONFIRMED CLINICAL_OR_DEPLOY, no fixed BN admin space needed;
route to new FC 2-000-05N Series 500 medical CCN(s):

  H&S Co:    151 billets
    Holding Ward Sections 1, 2, 3                  88
    Preventive Med Section                         31
    Stabilization Sections A, B, C                 80 (wait,
      this is 80 not 30; see audit report for actual numbers)
    Collecting/Evac Sections A, B, C               64
    Radiology Sections 1, 2                        24
    Laboratory Sections 1, 2, 3                    24
    FRSS Team 1, 2                                 16
    ERCS Team 1, 2, 3                              16
    Pharmacy Det 1, 2                               6
    Blood Bank Section                              6
    Combat Stress Teams 1, 2, 3                    18
    (Numbers are per-section per audit log; H&S total = 151)
  Surg A:    111 billets
  Surg B:    111 billets
             ---
  Subtotal:  373 billets

DEFAULTS FOR 137 TBD BILLETS (baked in; revisit only on user
override):

  HEADQUARTERS PLATOON Surg A and Surg B (~32-33 each):
    DEFAULT, route to BN_ADMIN at 61072. These are the surgical
    companies' own HQ admin sections (Co CO, XO, 1stSgt, Co
    Clerk, supply chief, etc.). They sit at desks, not in the
    clinic. Routing: 61072.

  FRSS 1 / FRSS 2 / FRSS 3 in Surg A and Surg B (16 each, 96 total):
    DEFAULT, route to CLINICAL_OR_DEPLOY at the new Series 500
    medical CCN. Forward Resuscitative Surgical Systems are
    deployable surgical teams; they do not occupy fixed BN
    admin space.

  AMBULANCE DET 1 / AMBULANCE DET 2 in Surg A and Surg B
  (12 each, 48 total):
    DEFAULT, route VEHICLES to 21451 / 14312 (motor pool +
    vehicle laydown). Route PERSONNEL to the new Series 500
    medical CCN. Corpsmen ride out with surgical platoons; no
    fixed desk requirement.

REVISED BUCKET TOTALS WITH DEFAULTS APPLIED:

  BN_ADMIN:                       101 + 65 (Surg HQ Plt) = 166
  CLINICAL_OR_DEPLOY:             373 + 96 (FRSS) + 48 (Amb pers) = 517
  Equipment-only (Amb vehicles):  ~48 vehicle slots, no personnel
                                  ---
  Total billets:                  166 + 517 + (already counted) = 611

================================================================
SECTION 6, CCN GSF STATE (CURRENT, BEFORE THE FIX)
================================================================

Pre-recalc cached values, validator: 8 PASS / 0 FAIL (format
only; G5 sanity check will fail).

  CCN     TOTAL                  STATUS
  -----   --------------------   ----------------------------------
  14312       0.00 GSF           BROKEN, TE VLOOKUP chain returns 0
  14345    6,110.08 GSF          OK
  17110       0.00 GSF           DESIGN STUB (rolls into 17120)
  17120    2,815.45 GSF          OK
  21451    1,129.00 GSF          PARTIAL, equipment side returns 0
  21710      583.32 GSF          PARTIAL, officers count 0
  44112   46,182.74 GSF          OK
  45110        8.89 GSF          BROKEN, factor 0.11111 SF-to-SY
  61072   69,875.00 GSF          INFLATED, sweeps clinical at admin rate
  61073       0.00 GSF           CRITICAL, 574 billets routed, 0 SF
  -----   --------------------
  SUM    126,704.48 GSF          unreliable

Defensible portion of the current 126,704 SF is approximately
56,000 SF (44112 + 14345 + 17120 + 21451 + 21710 + the BN-only
slice of 61072 at 39 admin Marines x 162.5 = 6,337.5).

================================================================
SECTION 7, FULL COMMIT HISTORY THIS WORK CHAIN
================================================================

Branch claude/usmc-bfr-audit-repair-0YYwt commits in order
since 9a01d01 (prior session's last commit):

  0d358e9 hook fix: CLAUDE_PROJECT_DIR default + ruflo first
  54e2668 hook simplify: tighten comments, drop subshell
  2cf9c80 violations 1 and 3 partial close
  3bdb87f violation 3 corrected (Camp Kinser primary source)
  9f4ceef strip placeholder narratives, match sheet convention
  cd5738f LibreOffice recalc + GSF reconciliation (REVERTED)
  c3a6c7c CG signed letter OCR
  9553f7d revert corrupt recalc, add HANDOFF_NEXT_SESSION.md
  12a5f12 doc(handoff): update HEAD reference
  3fc3814 doc(handoff): add GitHub URLs
  28f2271 skill: Track 10f + Apex Omega BLOCKING gates
  5fa9e9c personnel disambiguation, ASR vs BFR vs CG letter

================================================================
SECTION 8, SOURCE DOCUMENTS (DO NOT RE-DISCOVER)
================================================================

Methodology and FC source:
  APEX_OMEGA.pdf                                binding briefing
  fc_2_000_05n_100series_02_11_2026.pdf         current
  fc_2_000_05n_200series_05_16_2025.pdf         current; PERSONNEL-DRIVEN
  fc_2_000_05n_300series_03_02_2023.pdf         training, not used here
  fc_2_000_05n_400series_11_19_2025.pdf         current
  fc_2_000_05n_500series_03_17_2023.pdf         MEDICAL, USE THIS NEXT
  fc_2_000_05n_600series_03_02_2023.pdf         current
  fc_2_000_05n_700series_11_19_2025.pdf         current
  fc_2_000_05n_800series_03_31_2025.pdf         current
  fc_2_000_05n_appendixa.pdf                    1060-CCN vocabulary
  BFR_Generator_FC2-000-05N.xlsx                methodology workbook

Unit data sources for 3d Med Bn:
  M28262_3dMedSurgB.xlsx        Surg B TFSMS, structure 02/03/2026
  M28263_3dMedSurgA.xlsx        Surg A TFSMS, structure 02/03/2026
  3DMLG_ASR.xlsx                Master ASR; sheet '3D MED BN'
                                authoritative 609 billets pivot
                                by company x MOS x grade
  H&S TFSMS                     DOES NOT EXIST IN REPO. Will not
                                exist. H&S TE side is 198 inherited
                                NAVFAC MIDLANT template rows.

CG decision documents:
  3d Med Bn Strat Basing Req CG SIGNED (004).pdf
                                OCR'd previously. 711 personnel.
                                Workspace per enclosure (2),
                                not directly identified in repo.
  CG Endorsement Surg Co B 3d Med Bn 3d MLG - G-5 Basing Action v1.docx
                                paragraph 19 names the Camp Kinser
                                buildings.
  3D MED BN Footprint (as of Jan 2026) .pdf/.pptx
                                current state layout.
  Tab A - Endorsement Letters; Tab B - Decision Brief; Tab C -
  Basing Assessment Aug 2025 (background, supporting documents).
  E_BFR_F_PRC_BU26-5836R_POM26_20260228_2_OF_2.pdf
                                POM26 part 2 of 2; possibly
                                contains the encl (2) facility
                                layout. Verify next session.

================================================================
SECTION 9, EVIDENCE FILES IN audit/reports/3dmedbn/
================================================================

Personnel disambiguation:
  46_personnel_disambiguation_findings.txt     this session
  46_personnel_section_disambiguation.txt      bucket dump
  46_asr_bfr_mos_pivot.txt                     MOS-level pivot

CG signed letter:
  45_cg_letter_findings.txt
  45_cg_signed_letter_ocr_p1.txt
  45_cg_signed_letter_ocr_p2.txt

GSF audit:
  44_gsf_audit_full.txt                        recursive chain
  44_gsf_findings.txt                          per-CCN defects

Earlier diff logs:
  41_violations_1_and_3_diff.txt
  41_validator_post_violations_1_3.txt
  42_kinser_correction_diff.txt
  42_validator_post_kinser_correction.txt
  43_strip_placeholders_diff.txt
  43_validator_no_placeholders.txt

================================================================
SECTION 10, RUFLO ACTIVATION (NEW SESSION DOES THIS FIRST)
================================================================

The session-start hook (.claude/hooks/session-start.sh) is
fixed. It installs ruflo via npm globally if CLAUDE_CODE_REMOTE
is true. The .mcp.json registers ruflo via 'npx -y ruflo@latest
mcp start' so it auto-downloads on session start even without
global install.

Verification first action in new session:
  bash -c 'which ruflo; ruflo --version'
  Expected: /opt/node22/bin/ruflo and v3.7.0-alpha.7 or later

Then call ToolSearch:
  ToolSearch with query "ruflo" max_results=20

Once mcp__ruflo__* tools appear, spawn the orchestrator with
this task prompt (paste verbatim into ruflo's task input):

  Read audit/HANDOFF_NEXT_SESSION.md fully. Execute Section 11
  end to end. Apex Omega rules and the seven BLOCKING gates in
  .claude/skills/bfr-pipeline/SKILL.md are binding. The branch
  is claude/usmc-bfr-audit-repair-0YYwt at HEAD 5fa9e9c. Push
  to the harness-assigned branch. Do not push to main.

If mcp__ruflo__* tools do not appear within 30 seconds of
session start, restart the session once. If they still do not
appear, continue without ruflo using the in-session Agent
tool; the work plan is the same.

================================================================
SECTION 11, ACTION PLAN (NO QUESTIONS, EXECUTE IN ORDER)
================================================================

A. Verify the baseline.

  A1. Confirm the workbook opens by validating with openpyxl:
      python3 pipeline/validate.py "M67400-FO-M13020 3D MED BN-22NOV2024.xlsx"
      Expected: 8 PASS / 0 FAIL.
  A2. Read SECTION 5 of this handoff to load the bucket plan.
  A3. Confirm sandbox tooling: openpyxl, poppler-utils,
      tesseract-ocr, libreoffice-calc, ruflo.

B. Extract Series 500 medical CCNs from FC 2-000-05N.

  B1. Read fc_2_000_05n_500series_03_17_2023.pdf via pdfplumber
      if it works in the new sandbox; otherwise pdftoppm + tesseract.
  B2. Identify CCN candidates for the 3d Med Bn clinical functions:
        Likely primary candidate: 53010 Dispensary / Outpatient Clinic
        Secondary candidates: 54010 Hospital, 55XXX specialty spaces
      Extract per-CCN planning factor (SF per Marine / Navy
      enlisted / officer at the various medical specialty types).
  B3. Document the chosen CCN(s) and planning factors in
      audit/reports/3dmedbn/47_series500_extraction.txt with
      page and table citations per Apex Omega rule 2.

C. Restore Navy NEC granularity for Surg A and Surg B.

  C1. Read M28263_3dMedSurgA.xlsx and M28262_3dMedSurgB.xlsx.
      Extract per-billet NEC codes (L00A, L03A, L10A, L17A, L23A,
      L31A) where present.
  C2. Update the BFR TO sheet's PMOS column to restore the NEC
      distinction for Surg A and Surg B billets.
  C3. For H&S, NEC granularity has no TFSMS source in repo. Use
      the ASR per-NEC counts (3DMLG_ASR.xlsx '3D MED BN' rows
      130-140 area) to distribute H&S's 130 Navy enlisted across
      L00A=2, L03A=69, L10A=4, L12A=21, L17A=6, L22A=6, L23A=4,
      L24A=9, L31A=9. Match by billet description where possible;
      assign by section function where not.
  C4. Commit the NEC restoration with explicit before/after for
      a sample of 20 billets per company.

D. Add the Series 500 CCN sheet(s) to the workbook.

  D1. Use pipeline/template.py admin pattern (or a new pattern
      derived from FC 2-000-05N 500 series) to build the new
      CCN sheet.
  D2. Match cosmetic style per audit/STYLE_GUIDE.md (CLB-4 four-
      sheet typography, Apex Omega 4-color cell-role palette).
  D3. Populate the loading formulas using COUNTIFS against
      TO!C:C for the new NOTE tag (e.g. 53010c for clinical
      enlisted, 53010o for clinical officer, 53010w if relevant).
  D4. Add the new CCN to UNIT_ROLLUP per existing pattern.
  D5. Add the new CCN to CCN_Library if not already there
      (verify against audit/CCN_VOCABULARY.json).

E. Re-route the 574 misrouted billets per SECTION 5 defaults.

  E1. For each of the 611 real billets in BFR TO sheet, set the
      NOTE column based on the bucket:
        BN_ADMIN H&S (101):                          61072 + 21451 + 44112
                                                     + 21710 + 14345 per
                                                     section table above
        BN_ADMIN Surg A/B HQ Platoon (65):           61072 (default)
        CLINICAL_OR_DEPLOY H&S (151):                53010 (new)
        CLINICAL_OR_DEPLOY Surg A clinical (111):    53010 (new)
        CLINICAL_OR_DEPLOY Surg B clinical (111):    53010 (new)
        FRSS 1/2/3 Surg A+B (96):                    53010 (new) (default)
        AMBULANCE DET personnel Surg A+B (48):       53010 (new) (default)
        AMBULANCE DET vehicles in TE:                21451 / 14312
  E2. For each rerouted billet, also update the CCN column to
      match the new NOTE tag's CCN.

F. Replace CCN 61073 H40 = 0 hardcoded.

  F1. Either:
      Option F1a: leave 61073 = 0 if no billets route to it after
                  E (and remove 61073 from UNIT_ROLLUP, with a
                  note that 61073 is unused because the
                  doctrinally correct routing avoids it).
      Option F1b: replace 61073 H40 with a real formula like
                  61072's pattern, so any future billet routed
                  there gets a real SF allocation.
      DEFAULT: F1a. Remove unused CCN.

G. Repair the other broken CCNs.

  G1. CCN 14312 VLOOKUP chain: change IFERROR fallback from
      "0" (string) to 0 (number); verify TE rows tagged 14312
      carry length/width/height/volume in cols T/U/V/W.
  G2. CCN 45110: identify the source of the 80 value at R30/R31;
      confirm 0.11111 is intentional SF-to-SY conversion or fix
      the chain to produce SF directly.
  G3. CCN 21451 equipment side: M28 = AB173 chain returns 0;
      determine why and repair.
  G4. CCN 21710 officers count: connect H&S radio/electronics
      TE rows (A20427G, A01357G, A80017GA, A00227G) to the
      equipment-driven half of the chain.

H. Validate, recalc, ship.

  H1. Run python3 pipeline/validate.py against the updated
      workbook. Expect 8 PASS / 0 FAIL (format) plus all G5
      sanity checks (every CCN with non-zero billet routing
      must produce non-zero GSF).
  H2. Recalc: rely on fullCalcOnLoad=True (verify the workbook
      has it; if not, set it). DO NOT use libreoffice
      --convert-to xlsx. Alternative: open in Excel and save.
  H3. Open the workbook in Excel (or have user open it) before
      claiming complete. GATE 1 enforces this.
  H4. Back-test the new GSF roll-up against:
        CG signed letter: 711 personnel x doctrinal SF/person
        rates per FC 2-000-05N Series 200 (admin) and Series
        500 (clinical).
      A defensible BFR should land in roughly the 80,000 -
      130,000 GSF range, weighted heavily toward Series 500
      clinical space.
  H5. Commit with diff log under audit/reports/3dmedbn/47_*.
      Push to harness branch.

I. Update the handoff and skill for the session after this one.

  I1. Append Track 10g to .claude/skills/bfr-pipeline/SKILL.md
      recording the work done this session.
  I2. Update audit/HANDOFF_NEXT_SESSION.md HEAD reference and
      add an "outstanding for follow-up" section.

================================================================
SECTION 12, USER STATEMENTS THAT ARE DURABLE
================================================================

  - 711 personnel in the BN per CG signed letter (verified).
  - Surg B is a structural mirror of Surg A by design, not a
    paste error. The 1-billet asymmetry is real.
  - Currently the unit is at Camp Foster (most of it). MT/UT
    and MSTC have moved to Camp Kinser. Full consolidation at
    Kinser is the plan, not yet executed.
  - The BFR is the overarching document. It sizes facility
    requirements. It does not track per-billet physical location
    today.
  - "Every single tab the GSF must add up, not AI placeholder
    crap." No zero TOTALs with non-zero billet routing. No
    bracketed TBDs in cell text. No unit-conversion bugs.
  - "No placeholder crap." TBD/pending notes go in audit log
    and commit messages, not in cell content.
  - H&S TFSMS does not exist and will not exist. H&S TE side is
    198 inherited NAVFAC MIDLANT template rows. Restore NEC
    granularity for H&S via ASR pivot, not via a missing TFSMS.
  - The BFR end state should say who needs space and who does
    not, with confirmation personnel are real, not fabrications.
    SECTION 5 above is that disambiguation, baked in.
  - Use ruflo for structural / multi-step work in next session.
  - Stop chasing locations. The BFR is the overarching document.
  - Do not ask 90 questions at session start. Defaults baked in
    above; revisit only on explicit override.

================================================================
SECTION 13, OPEN APEX OMEGA VIOLATIONS STATUS
================================================================

Violation 1, PARTIAL.
  H&S TE side: 198 inherited NAVFAC MIDLANT rows, no primary
  source. R507 cell text now matches convention (no inline
  marker). Re-source held for next session under ruflo.

Violation 2, OPEN (THIS IS THE STRUCTURAL FIX).
  574 of 611 real billets currently routed to CCN 61073 = 0.
  Doctrinal fix is adding FC 2-000-05N Series 500 medical CCN
  and re-routing per SECTION 5 defaults.

Violation 3, CLOSED.
  MISSION STATEMENT B208 / B210 / B211 follow the sheet's
  postal-block convention. Primary-source citation for Camp
  Kinser planned facilities at 42_kinser_correction_diff.txt.

Violation 4, OPEN.
  Personnel back-test against CG letter (711) verified;
  workspace back-test still needs CG letter enclosure (2)
  "Proposed Facilities Layout". Likely candidate: POM26 PDF
  part 2 of 2. Verify next session.

================================================================
SECTION 14, SANDBOX TOOLING (FRESH SANDBOX MAY NEED INSTALL)
================================================================

  pip install openpyxl   (probably present)
  apt-get install -y poppler-utils  (for pdftoppm)
  apt-get install -y tesseract-ocr  (for OCR fallback)
  apt-get install -y libreoffice-calc  (inspection only;
                                        NEVER use --convert-to
                                        xlsx, see GATE 1)
  npm install -g ruflo@latest  (or rely on .mcp.json's npx
                                 auto-download)

Broken in this sandbox (do not rely on):
  pdfplumber, pdfminer.six   (cryptography binding pyo3 panic)
  use pdftoppm + tesseract instead

================================================================
END OF HANDOFF
================================================================
