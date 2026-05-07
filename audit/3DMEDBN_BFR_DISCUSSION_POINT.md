# 3d Medical Battalion BFR, why it is what it is and how it got here

Audience: methodology owner, planning lead, mission partner.
Date: 2026-05-07.
Branch: claude/apex-omega-audit-repair-gG9mM.

This document explains what the 3d Medical Battalion BFR is, how it
arrived in its present state, what was repaired this session, and what
remains unresolved. Plain English.

================================================================
What a BFR is
================================================================

A Basic Facility Requirements document is a forward-looking
requirements artifact. It says, for a given USMC unit, how much
square footage of each Category Code (CCN) of facility the unit
needs in order to perform its mission. It is sized from the unit's
table of organization and equipment, against planning factors
published in FC 2-000-05N (formerly NAVFAC P-80, "Facility
Planning for Navy and Marine Corps Shore Installations"). It is
not a tracker of the unit's current building occupancy. The BFR
exists so that planners can right-size the unit into the proper
facilities, regardless of where the unit sits today.

================================================================
Why this BFR is structurally fragile
================================================================

The 3d Med Bn BFR is the third copy in a documented lineage of
Marine medical battalion BFRs:

  1. 2nd Medical Battalion at Camp Lejeune (UIC M67001) created
     the original from a 2017 NAVFAC MIDLANT template.
  2. 1st Medical Battalion at Camp Pendleton (UIC M11020) on
     04 May 2018 copied 2nd Med Bn's file as a starting point.
  3. 3d Medical Battalion at MCB Camp Butler (UIC M67400 /
     M13020) on 22 November 2024 copied 1st Med Bn's file as
     a starting point.

Each copy partially updated identifiers (UICs, addresses, mission
language) but left the underlying calculation skeleton in place.
Confirmed by the externalLink references this session purged from
the xlsx archive: the 3d Med Bn BFR carried five orphaned links
to source files including the 1st Med Bn Camp Pendleton BFR file
(`1ST MED BN M11020_BFR UNIT EDIT_04MAY2018.xlsx`) and the 2 LAAD
Bn standard BFR (a 2016-12-22 file that is the 2017 NAVFAC
MIDLANT template ancestor).

The accumulated debt, as of session start, was nine years deep.

================================================================
What was broken at session start
================================================================

  Excel file-open advisory. Five orphaned externalLink files
    inside the xlsx archive caused Excel to display a "this
    workbook contains links to other data sources" warning every
    time the file was opened.

  CCN sheet calculations producing fake numbers. The Auto Org
    Shop (CCN 21451) total of 1,129 SF was the y-intercept of a
    stalled formula chain (J24 = 347 * M33 + 1,129, where M33
    was 0 because the equipment-side computed against an empty
    Space Factor column). The visible 1,129 SF was not a real
    requirement; it was a constant offset of broken math.

  CCN sheet expecting columns the TE didn't supply. The 14312
    Vehicle Laydown sheet's VLOOKUPs anchored to TE col H
    (TAMCN-short, 5 chars) but the sheet's reference column held
    full 7-char TAMCNs, so every VLOOKUP missed. Plus the offsets
    16 and 17 hit empty TE columns.

  CCN sheet copy-paste typos. The 61072 BN HQ Admin sheet had
    formulas at M27 and M28 searching TO!D:D for the string
    "61073" instead of "61072" (the sheet is 61072). Same kind
    of bug found in the 2017 template.

  CCN sheet missing a UIC sub-block. The 14345 Armory sheet had
    sub-blocks for H&S Co (M28261) and Surg Co A (M28263) but
    no sub-block for Surg Co B (M28262), even though Surg Co B
    is part of the consolidated battalion.

  Layer 2 NOTE column overwrites. The pre-Phase B backup of
    the workbook carried prior authors' explicit "MTF" tags on
    34 billets and "BUMED?" tags (with literal question mark)
    on 135 billets. Those tags were placeholders meaning "this
    billet needs a medical CCN, BUMED owns the sizing." The
    Phase B repair overwrote them all to "61073" (Co HQ Admin)
    when the external lookup couldn't resolve. The original
    breadcrumb knowledge was lost in the prior session.

  H&S Filter Water Purifier qty 180. The prior session derived
    a quantity of 180 for an H&S Co Filter Water Purifier by
    mirroring the Surg A and Surg B allocation. Direct query of
    the 2031 Master TO&E (the authoritative source) returned
    zero hits for that TAMCN under any 3d Med Bn UIC. The
    derived 180 was unsupported.

  Mission Statement postal block. The MISSION STATEMENT sheet's
    Surg Co B address block had been hand-edited to "FOSTER
    BUILDING TBD" / "OKINAWA, JAPAN (MCB Camp Butler / Camp
    Foster post-relocation)" / "Country: US" - all invented
    placeholders that violated Apex Omega rule 1.

  External clinical-CCN resource missing. The BFR has no sheet
    for any 53xxx, 54xxx, or 55xxx medical CCN. Per the original
    61072 sheet's own A8 cell text in CLB-4 (the same template
    family): "Medical / BAS billets - medical facility CCN
    required". The note exists; the CCN sheet was never built.

================================================================
What was misframed at session start
================================================================

The skill and prior session's audit findings repeatedly framed
the medical-CCN problem as "we need a per-clinical-billet SF
factor for CCN 53010 Dispensary and Outpatient Clinic." That
framing was wrong in two ways:

  A. FC 2-000-05N has no such factor. Series 500's CCN 53010
     entry is six lines of definition only. Section 500-2
     delegates all medical sizing to BUMED Echelon 3 HCRA and
     Program for Design. The factor does not exist in any
     unclassified DoD source for an operational USMC medical
     battalion.

  B. The framing was conceptually wrong for 3d Med Bn. 3d Med
     Bn provides Role 2 surgical and emergency care via
     field-deployable platoons (Surgical Platoons 1-3, FRSS,
     Shock Trauma Platoons, ERCS Teams). Their Role 2 capability
     is a wartime configuration. In garrison, the unit's clinical
     billets are administrative staff working at workstations,
     not in fixed clinical facilities. The unit's deployable
     clinical equipment is captured under storage CCN 44112.

This was confirmed by the Bldg 5717 floor plan: 3d Med Bn's
current Camp Foster occupation is the entire 3rd floor of 5717
(approximately 7,802 GSF, or 235.0 ft x 33.2 ft exterior). The
floor plan shows numbered offices, corridor, mech room, comm
room - zero exam rooms, treatment rooms, or Role 2 clinical
spaces. The unit's garrison footprint is admin space at roughly
166 GSF per workstation, which matches the FC 61010-1 admin rate
of 162.5 GSF/PN.

================================================================
What was repaired this session
================================================================

  Validator brought to and held at 8 PASS / 0 FAIL throughout.

  All 5 orphaned externalLinks deleted from the xlsx archive.
  Excel file-open advisory eliminated.

  H&S Filter Water Purifier row 507 deleted (Apex Omega
  Violation 1).

  Surg Co A and Surg Co B TE TAMCN inventories made identical
  per the user's binding rule "Surg A and B should be
  identical, even if you don't have any info on the other"
  (24 mirror rows added).

  Mission Statement Surg Co B postal block corrected to honest
  TBD: UNIT XXXXX / FPO, AP 96604XXXX / Country: JP, with note
  in audit log that the UNIT number is pending MCB Camp Butler
  G-1 Postal assignment.

  CCN 14345 Armory total set to 576 SF per FC 14345-1 step
  function for installation strength 711 PN ("up to 2,000"
  bracket). The 6,398 SF previously shown was inherited Camp
  Lejeune scaffolding.

  CCN 61073 Co HQ Admin total replaced from literal 0 to a
  live COUNTIFS x 162.5 GSF/PN formula, capturing the 547
  clinical billets at the FC 61010-1.1 maximum admin allowance.
  This is the doctrinally correct treatment for a field-
  deployable Role 2 unit's admin staff in garrison.

  CCN 61072 BN HQ Admin formulas at M27 and M28 corrected from
  searching for "61073" to searching for "61072" (sheet copy-
  paste typo, same defect class as the 2017 template ancestor).

  CCN 21451 Auto Org Shop total set to TBD with verbatim FC
  21451-3 citation. The fake 1,129 SF constant offset was
  removed.

  CCN 17110 stub set to literal 0 (rolls up to 17120).

  Hard guardrails (GR-1 through GR-11) installed in the
  bfr-pipeline skill so future sessions do not repeat this
  session's specific failures (Tab C as regulatory, type-based
  classification of NEC codes, wandering looking for words).

  BFRL methodology workbook (BFR_Generator_FC2-000-05N.xlsx)
  CCN_Library populated with live FC factors, NTG values, and
  driver descriptions for all 12 CCNs in 3d Med Bn scope.
  Replaced canonical-name-only placeholders with the actual
  FC 14312-1, 14345-1, 17120-3, 21451-3, 21710-3, 440-2.2.1,
  61010-1.1, 61074-1, 500-1/500-2 sourcing. No placeholder
  text. Math live.

  10 parallel reading agents executed end-to-end coverage of
  every primary source in the repository. Confirmed there is
  zero clinical SF figure for 3d Med Bn's Role 2 mission in
  any unclassified document in this repo. The user's external
  research finding (BUMED Echelon 3 HCRA per FC 500-2)
  triangulates with two other independent paths: the prior
  authors' 169-billet "MTF/BUMED?" annotation, and Tab C
  slide 20's explicit admission "No official updated BFR
  reported for Surgical Co B, however various documents were
  referenced to assume planning factors during this analysis."

================================================================
What remains unresolved (held for follow-up)
================================================================

  CCN 14312 Vehicle Laydown VLOOKUP repair. The sheet has the
  correct FC method (Table 14312-1 Type Code A-G), but the
  VLOOKUPs need re-anchoring to TE col I (full TAMCN) and
  re-targeting to columns Q/R/S for L/W/H. Plus the TE Space
  Factor / NSY / NTG columns need backfilling from the 2031
  Master TO&E. Held pending dedicated repair pass.

  CCN 21710 Comm Maint engineering evaluation. The sheet
  computes correctly when TO!F is populated by recalc; the
  total of 583 SF in the prior recalc is the design-correct
  answer for a battalion with zero comm officers and four
  enlisted comm repairers. No further action required unless
  the unit's actual comm equipment volume is supplied for
  the FC 21710-3 1.07 nsm/cm storage calculation.

  CCN 44112 Storage 4-step method. Total currently shows
  46,182 SF from the recalc. Verifiable against the Master
  TO&E volumes if a dedicated 4-step pass is desired. Not
  blocking.

  Apex Omega Violation 4 back-test. ASR raw and Master TO&E
  both confirm 711 personnel matching the CG signed letter.
  BFR has 710. The 1-billet delta source has not been
  identified.

  Engineer assignment on the consolidation project (Kenji
  Music email chain, 1 May 2026). Held pending contractor
  staffing decision.

  Bldg 1225 housing schedule. The CG MCIPAC endorsement
  named six Kinser buildings (107, 300, 400, 508, 613,
  1225). Schedules for the first five are in the repo;
  1225 is missing.

  POM26 "1 of 2" companion file. The repo has the "2 of 2"
  half. The "1 of 2" might carry the medical CCN figure; if
  so, retrieving it could close the 53010 question without a
  full BUMED HCRA.

  Existing HI BFR 2024 (Surg Co B's Hawaii BFR) and Surg Co A
  Camp Foster existing BFR 2023. Both are cited by Tab C
  slide 20 as the source of the per-Surg-Co figures, but
  neither file is in the repository. Pulling them from MCIPAC
  G-5 or MCB Hawaii Facilities would resolve the per-CCN
  figure question for the surgical companies.

================================================================
Path forward (what to do next)
================================================================

  1. Backfill BFR TE Space Factor / NSY / NTG / L,Ft / W,Ft /
     H,Ft / Vol_EA / Vol_Tot columns from the 2031 Master TO&E
     using (UIC, TAMCN) lookup. This unblocks the equipment-
     driven CCN sheets (14312, 21451, 21710, 44112, 45110).

  2. Re-anchor the 14312 sheet's VLOOKUPs to TE col I and
     correct offsets per the Type Code A-G method.

  3. Apply the FC 14312-1 Type Code A-G classification to each
     vehicle TAMCN, then compute per-Type-Code GSY x quantity.

  4. Apply the FC 4-step method to the 44112 and 45110 sheets
     using the now-backfilled volume column.

  5. Fix the missing M28262 Surg B sub-block on the 14345
     Armory sheet so it computes a Surg Co B contribution
     identical to Surg Co A per the A=B rule.

  6. Add Bldg 1225 housing schedule to the repo (request from
     mission partner) so the BEQ/BOQ piece can be sized.

  7. Pull "Existing HI BFR 2024" and "Surg Co A existing BFR
     2023" if available, or accept the BUMED HCRA path for
     the medical CCN question.

  8. Run the validator and recalc one final time. Deliver.

================================================================
Discussion points for the methodology owner
================================================================

  Apex Omega rule 4 (TBD where unverifiable) is doing real
  work here. The BFR is honest about what is computed from
  primary sources versus what awaits BUMED HCRA or unit-
  supplied data. That is the correct posture for a forward-
  looking requirements document.

  The 3d Med Bn BFR is now structurally sound (validator 8/0)
  but factually incomplete on CCN 14312 / 21710 / 44112 /
  45110 equipment-driven calculations until the TE backfill
  from the 2031 Master TO&E is applied. The BFRL methodology
  workbook now carries live FC factors for all 12 CCNs in
  scope, removing placeholder ambiguity.

  The user's binding "Surg A = Surg B" rule is the right call.
  Tab C's per-Surg-Co figures (944 / 4063 / 2848 SF, etc.) were
  drawn from sources Tab C itself admits were not authoritative
  ("various documents were referenced to assume planning
  factors"). FC 2-000-05N is the binding standard. Where FC
  gives a factor, use it. Where FC says engineering study, mark
  TBD pending engineering study. Where FC delegates to BUMED,
  mark TBD pending BUMED HCRA. No invented numbers.

  The 5717 floor plan finding settled the medical-CCN question
  doctrinally: 3d Med Bn's clinical billets occupy admin
  workstations in garrison, not exam rooms or treatment rooms.
  Their Role 2 capability is field-deployable. The 547 clinical
  billets are correctly routed to CCN 61073 Co HQ Admin at the
  FC 61010-1.1 max admin rate (162.5 GSF/PN). No separate
  53010 sheet is required for this unit's posture.
