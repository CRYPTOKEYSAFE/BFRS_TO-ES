# Exhaustive clinical-CCN sweep, every primary source in the repo

Date: 2026-05-07
Branch: claude/apex-omega-audit-repair-gG9mM
Trigger: user direction "deploy ruflo multiple agents to read....I cannot
believe there is unanswerable...you are not looking at every reference."
Method: 9 parallel reading agents, each scoped to one or two source
clusters, total coverage of every file in the repository that could
plausibly carry a clinical-facility SF figure or methodology.

================================================================
The question
================================================================

Is there ANY usable square-foot figure or quantitative methodology
for sizing 3d Med Bn's Role 2 garrison clinical footprint (547
clinical billets across H&S Co + Surg Co A + Surg Co B) anywhere
in this repository?

================================================================
Sources searched, by agent
================================================================

A1 (CLB-4 BFRs):
  SW_M29030_CLB4_BFR_2026-NWPCW167400L021.xlsx
  FO_M29030_CLB 4_FINAL BFR.xlsx
  Result: Zero. The SW workbook's 61072 sheet A8 carries text only:
  "Medical / BAS billets (34) - medical facility CCN required". The
  same gap as 3d Med Bn, no SF figure.

A2 (Tab A / Tab B / Tab C basing package):
  Tab A endorsement letters, Tab B Decision Brief v2, Tab C basing
  assessment Aug 2025 PPTX.
  Result: Zero clinical SF. Tab C slide 20 cites "Existing HI BFR,
  2024" and "Surg Co A existing BFR, 2023" as the source of the
  Surg Co B figures, but the clinical figure is silent. Tab A page
  6 Section 5 quotes 7,056 NSF total office space for 180 BICs
  (39.2 NSF/BIC) - this is total office, not clinical.

A3 (3d MED BN BFR + 2 backups):
  M67400-FO-M13020 3D MED BN-22NOV2024.xlsx (current, post-Phase B)
  M67400-FO-M13020 3D MED BN-22NOV2024.preB-backup.xlsx
  M67400-FO-M13020 3D MED BN-22NOV2024.preExtLinkPurge-backup.xlsx
  Result: Zero clinical CCN sheet exists in any of the three
  workbooks. CRITICAL BREADCRUMB found in preB-backup: 34 TO rows
  tagged "MTF" (Medical Treatment Facility) covering PSYCHIATRIST,
  CLIN PSYCH, BEHAVIORAL HLTH TECH, EMERG MED SPEC, FLD MED TECH;
  135 TO rows tagged "BUMED?" (with question mark, prior author
  uncertainty) covering GEN SGN, ORTHOPEDIC SGN, ANESTHESIOLOGIST,
  CC NRS, SURFACE IDC, FLD MED TECH. 169 billets total. Phase B
  repair overwrote these annotations to "61073" (Co HQ Admin) when
  the external lookup couldn't resolve. The original tagging
  knowledge was lost. Independent confirmation that prior authors
  also concluded BUMED owns the sizing.

A4 (POM26 PDF + M67400 BFR PDF):
  E_BFR_F_PRC_BU26-5836R_POM26_20260228_2_OF_2.pdf
  M67400-FO-M13020 3D MED BN-22NOV2024.pdf
  Result: Zero. The "1 of 2" companion to the POM26 file is missing
  from the repo and may have carried the figure. The 3d Med Bn PDF
  (60 pages) tags clinical billets `#N/A` CCN; structurally
  incomplete with respect to its own Role 2 mission.

A5 (Six Kinser building schedules + AE PLUS PDFs + 3d Med Bn
    Footprint Jan 2026 PDF/PPTX):
  107_KI_Schedule.xlsx, 300_KI_Schedule.xlsx, 350_KI_Compound_
  Schedule.xlsx, 400_KI_schedule.xlsx, 508_KI_Schedule.xlsx,
  613_KI_Schedule.xlsx, plus six AE PLUS floor plan PDFs, plus
  3D MED BN Footprint (as of Jan 2026) PDF and PPTX.
  Result: Zero medical-CCN rooms across all 6 Kinser buildings.
  Zero medical-keyword rooms in AE PLUS floor plans. Footprint
  document tracks IT counts (workstations, phones), not facility
  area. Only one clinical-tagged room: FOS-5717 Room 216 "Clinic
  Ops, BN Surgeon" (admin office for the Bn Surgeon, no SF).

A6 (BFR_Generator workbook):
  BFR_Generator_FC2-000-05N.xlsx
  Result: All 13 medical CCN entries (530-10 through 550-30)
  carry name-only placeholders. Default Factor, Factor Notes, NTG
  columns are all empty for every medical CCN. No worked example
  in BFR_Calculator for any 530xx/540xx/550xx CCN. PD_Factor 1.09
  hardcoded; "1.13 medical" exists as text annotation only, no
  conditional override.

A7 (2031 Master TO&E + 3d Med Bn Footprint):
  2031 Master TO&E v1.1 - 20250411.xlsx
  3D MED BN Footprint PDF/PPTX (re-read)
  Result: Master TO&E TE_3 sheet CCN column is 100% empty across
  all 19,001 rows. Medical-keyword equipment rows exist (AMAL kits,
  THEATER MEDICAL INF, X-RAY APPARATUS) but they are equipment
  TAMCNs, not facility tags.

A8 (TFSMS files + audit/* directory + BFR's MISSION STATEMENT
    sheet):
  M28262_3dMedSurgB.xlsx, M28263_3dMedSurgA.xlsx, all audit/*.md /
  audit/*.json / audit/*.yaml / audit/reports/* files, the BFR's
  embedded MISSION STATEMENT sheet (3 TFSMS Unit TO&E Reports for
  M28261, M28263, M28262).
  Result: Zero clinical SF data in TFSMS files (they are personnel
  + equipment authorization sources, not facility sources). The
  PLANNING_FACTORS.json correctly captured zero-factor status for
  53010, 53020, 53025, 53030, 53060, 53070, 55010, 55020 and full
  factor tables for 54010 (Dental). MISSION STATEMENT sheet
  contains three signed Mission Statements verbatim (FEB 3 2021
  Eric M. Smith, DC CD&I) but no SF figure.

A9 (FC 2-000-05N Series 500 exhaustive end-to-end):
  fc_2_000_05n_500series_03_17_2023.pdf (16 pages, full read)
  fc_2_000_05n_400series_11_19_2025.pdf (medical cross-reference
  scan)
  Result: Definitive doctrinal answer. FC 2-000-05N has zero
  quantitative methodology for sizing an operational USMC medical
  battalion clinic, BAS, or any non-DHA-MTF outpatient clinic.
  Section 500-1 delegates to OASD(HA); Section 500-2 requires
  BUMED Echelon 3 HCRA + Program for Design. Tables 500-1 and
  500-2 provide net-to-gross conversion ratios and building-level
  grossing percentages but presuppose net area is established
  elsewhere. Tables 53045-1 (Veterinary), 54010-1 to -4 (Dental),
  55030-1 (Alcohol Rehab) are the only quantitative tools in the
  500 Series. None apply to 53010 or to a Marine medical battalion
  Role 2 clinical footprint.

================================================================
The 61074 Garrison Aid Station finding (and why it does not solve
the problem)
================================================================

Agent A8 surfaced CCN 61074 GARRISON AID STATION, MARINE CORPS in
FC 2-000-05N Series 600 (v.600.20230302, pages 38-39). It is the
only FC 2-000-05N CCN with a Marine-Corps-specific clinical NSF
factor table. Table 61074-1 verbatim factors:

  Reception Area / Admin Area / Medical Records:
    Reception Desk            64 NSF per workspace
    Waiting & Form Writing    10 NSF per patient
    History Station           40 NSF per station
    Medical Officer Office   100 NSF per workspace (private)
    IDC Office                65 NSF per workspace (semi-private)

  Administrative Support Space:
    Office Equipment          45 NSF average
    Computer Support          60 NSF average
    Records Storage Movable   25 NSF average
    Records Workroom         200 NSF for up to 800 Marines
                              + 25 NSF per additional 100 Marines
    Reference Bookshelves      8 NSF per bookshelf
    Restrooms                 25 NSF per Exam Room (min 2 private)

  Patient Areas:
    Exam Room                100 NSF per physician
    Treatment Room           150 NSF
    Nourishment Center       100 NSF

  Clinic Support:
    Clean Utility            120 NSF
    Soiled Utility            90 NSF
    Equipment Storage        100 NSF average
    Janitor Closet            50 NSF
    Low Volume Pharmacy       50 NSF

  Deployment Storage:
    Deployment Storage     1,000 NSF

  Gross Floor Area: NSF * 1.35 NTG (FC 61074-3)

CRITICAL SCOPE EXCLUSION verbatim from FC 61074-1:

  "Garrison Aid Stations do not take the place of clinics
  maintained by BUMED, but rather provide the first echelon of
  basic medical care in a fixed facility. Access to higher
  echelons of care (including laboratory, radiological, or
  surgical services) shall be provided at BUMED facilities rather
  than the facility detailed here."

3d Med Bn provides Role 2 surgical, laboratory, radiological care.
The unit is itself the higher-echelon BUMED capability that 61074
explicitly redirects to. Therefore CCN 61074 is structurally NOT
the right CCN for 3d Med Bn's Role 2 garrison footprint.

CCN 61074 might apply to a BAS function within H&S Co providing
Role 1 first-echelon care to 3d Med Bn's own personnel, but that
is not the 547-clinical-billet question. The 547 clinical billets
are providing Role 2 to III MEF, not Role 1 to themselves.

================================================================
What the answer actually is
================================================================

After an exhaustive sweep of every primary source in the repo:

  1. There is no usable clinical SF figure for 3d Med Bn's Role 2
     mission anywhere in this repository.

  2. FC 2-000-05N has no quantitative methodology for sizing a
     Marine Corps Medical Battalion's Role 2 garrison clinic.
     Series 500 delegates the entire methodology to OASD(HA) and
     BUMED. Series 600's CCN 61074 is Role 1 only and explicitly
     excludes Role 2 services.

  3. Project-practice documents (Tab A, B, C, the basing package,
     POM26, footprint, building schedules) collectively confirm
     the gap. Tab C cites "Existing HI BFR 2024" and "Surg Co A
     existing BFR 2023" as the source of the Surg Co B figures,
     but the clinical figure is not in those Tabs and the source
     documents are not in the repo.

  4. The preB-backup of the BFR carried prior authors' explicit
     "MTF" and "BUMED?" annotations on 169 billets, independently
     reaching the same conclusion (this is BUMED's call). Phase B
     repair overwrote those annotations to 61073 (admin) without
     resolving the underlying gap.

  5. The user's external deep research (Claude Sonnet 4.6
     Thinking) confirmed verbatim from FC 2-000-05N Series 500
     and DHA SPC Chapter 110: clinical sizing for non-DHA-MTF
     operational units like 3d Med Bn flows through BUMED
     Echelon 3 (Naval Medicine West for MCIPAC) HCRA + Program
     for Design.

  6. DHA SPC Chapter 302 (PCMH Freestanding) provides interim
     workload-driven formulas (~1,863 encounters/room/year), but
     SPC use and SEPS access are restricted to DHA-managed MTF
     projects. 3d Med Bn is NOT a DHA MTF.

================================================================
What this means for the BFR
================================================================

The 53010 (or equivalent Role 2 CCN) TOTAL REQUIREMENT cell in
the 3d Med Bn BFR must be marked TBD pending BUMED NMW HCRA per
FC 2-000-05N Section 500-2. The cell's footer should cite Section
500-1 and 500-2 verbatim, and apply Table 500-1 NTG 1.35 + Table
500-2 building grossing 13.5/2.0/14.0/1.5 only after net area is
established by HCRA.

This is the doctrinally correct, Apex-Omega-rule-4 compliant,
facts-only answer. The BFR is not silently filled with a guessed
or extrapolated number; it is honestly marked TBD with the
regulatory path that resolves the gap.

If the user obtains "Existing HI BFR 2024" (Surg Co B's previous
Hawaii BFR) or "Surg Co A existing BFR 2023" from MCIPAC G-5 or
Naval Medicine West, the existing figures in those documents
become the authoritative input. Until then, TBD.

================================================================
Apex Omega application
================================================================

Rule 1 (facts only): every claim above traceable to a specific
agent's verbatim extraction from a specific file with citation.

Rule 4 (TBD where unverifiable): clinical CCN sizing honestly
marked TBD pending BUMED NMW HCRA. Not silently filled.

Rule 6 (three-bucket separation): regulatory facts (FC 2-000-05N,
DHA SPC) separated from program-practice facts (Tab A/B/C, POM26,
footprint) and from external benchmarks (none used).

Rule 7 (numbers traceable): zero invented numbers. Every figure
cited is reproducible from the original source with the agent's
extraction script.

Rule 9 (read everything): nine agents executed in parallel,
covering 100% of the repo's potentially-relevant primary sources.
The conclusion is not from omission.
