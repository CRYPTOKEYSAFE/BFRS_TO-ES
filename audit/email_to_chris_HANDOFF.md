Subject: 3d Med Bn BFR, handoff while I'm out

Chris,

Quick context, then the meat. I'm out next week and I want you to be able to pick this up. The bottom line is I owe you a draft BFR for 3d Medical Battalion and I don't have a finished one to hand over. The work is partially done and the file is in much better shape than the one we inherited, but every time I went to drive a number to ground I uncovered another doctrinal question that needs a real answer, not a guess. I'd rather hand you the questions and what I've already worked out than hand you a number I made up. I hate it, but it's the only honest move.

All the documents are in the 3d MLG MS Teams channel. That is the live source. If you want any of them mirrored, tell me.

What the BFR is supposed to do, in case it helps to restate. The BFR states the unit's rated facility space, broken out by category code (CCN), rolled up to a unit total. It does not assign people to buildings. It does not say "these 39 work here, these 547 work there." It says: under FC 2-000-05N, given the unit's TO&E and operating posture, the unit rates X amount of armory, Y amount of admin, Z amount of equipment storage, and so on, and the unit total comes out to W gross square feet. A planner downstream takes the BFR and overlays it onto buildings. The BFR is the requirements document, not the building plan.

The reference documents I have been working from. All in Teams.

  FC 2-000-05N. The 200-in. Series 100 was published 11 Feb 2026 and sets the methodology baseline. Series 500 covers medical CCNs. Series 600 covers admin (61072 etc.). Series 200 covers maintenance and shop functions. All eight series PDFs plus Appendix A are in the channel.

  3DMLG_ASR.xlsx. The Active Strength Report. It carries 609 BICs split 250 H&S + 179 Surg A + 180 Surg B. This is the authority for billet count, and per FC reconciliation rules the BFR cannot release until ASR ties out against TFSMS.

  The CG-signed strategic basing letter, dated 2 Feb 2026, signed K. G. Collins, CG 3d MLG, addressed to DC I&L Facilities and Services Division via III MEF and MARFORPAC. It cites 711 PN consolidating to Camp Kinser plus Surgical Co B returning from MCBH Kaneohe Bay. The letter directs a strategic basing action. It is not a facility-planning math source. It is a sanity check on head count.

  3D MED BN Footprint (as of Jan 2026), Camps FOSTER and KINSER. Room-by-room layout of where the unit sits today. Useful for grounding the math against actual occupancy at Bldg 5717, Bldg 215, Bldg 5628, and the Kinser pieces.

  M28261 H&S Co, M28263 Surg Co A, M28262 Surg Co B per-company TFSMS files. Source of the TO&E billet detail per company.

  The current BFR file: M67400-FO-M13020 3D MED BN-22NOV2024.xlsx.

History of the BFR file. This is part of why this work has been hard. The file did not start clean.

In 2017, Naval Facilities Engineering Command Mid-Atlantic (NAVFAC MIDLANT) issued a BFR template for 2nd Medical Battalion at Camp Lejeune (UIC M67001). The template was authored by James Brunson at NAVFAC MIDLANT. Around May 2018 that template was copied for 1st Medical Battalion at Camp Pendleton (UIC M11020). On 22 November 2024 it was copied again to stand up 3d Medical Battalion (UIC M13020 / M67400). Each copy carried forward the original 2017 cell layout, formula structure, defined names, lookup ranges, and external links to the prior installation's SharePoint. By the time the file landed on my desk it had nine years of accumulated debt in it.

Specifically, the things I found and fixed in the current file:

  The installation field across multiple sheets still said Camp Lejeune. I corrected it to MCB Camp Butler.

  Five external links pointed at SharePoint folders on Pendleton (1st Med Bn's BFR) and FlankSpeed (a fabricated reference to a 2029 TFSMS export that does not exist). All five severed via zip surgery so the file no longer pops the "this file has links to other data sources" warning when opened.

  The template carried four hidden CCN sheets (14312 vehicle laydown, 21451 auto org shop, 21710 comm/electronic maintenance, 45110 open storage) referencing 2nd Med Bn's UIC structure (M28271 / M28272 / M28273 / M28275) including a phantom Surg Co C that does not exist in 3d Med Bn. The Surg Co C ghost is eliminated from the visible work; the hidden sheets still need their UIC sub-blocks rebuilt to reflect 3d Med Bn (M28261 H&S, M28263 Surg A, M28262 Surg B).

  The 61072 admin sheet had a copy-paste bug where the COUNTIFS formula was searching for the string "61073" while sitting on the "61072" sheet. Fixed.

  The 14345 armory sheet was double-counting. Now reads 576 GSF per FC 14345-1 step function for 711 PN strength bracket.

  The 17110 stub now reads literal 0 per FC redirect to 17120.

  The methodology workbook (BFR_Generator_FC2-000-05N.xlsx) was scrubbed: fonts standardized, CCN_Library populated with verbatim FC factors per CCN, named-range API for Okinawa adjustments verified.

Where the file stands today.

  Validator runs 8 PASS, 0 FAIL. Schema is clean. NOTE coverage is 100 percent of tagged rows. No #REF!, #DIV/0!, #NAME?, #VALUE!, or #N/A error tokens anywhere in the workbook. External links: zero. Defined names: clean.

  Sheets: 15 total, 11 visible, 4 hidden. The visible CCN sheets are 14345, 17110, 17120, 44112, 61072, 61073. The hidden ones are 14312, 21451, 21710, 45110.

CCN by CCN status.

  14345 Armory. 576 GSF. Real number, FC-derived.
  17110 Education stub. 0 GSF. Correct, rolls to 17120.
  17120 Applied Instruction. 1,197 GSF. Real, FC chain produces it.
  44112 Storage of Air or Ground Organic Units. 46,182 GSF. FC chain produces it from TE volumes. The multi-tier constants for 44112c (climate-controlled) and 44112w (weather-tight) are unpopulated and need verification before signing.
  45110 Open Storage. 8.89 SY. Real but the SUMIFS criterion uses a literal "(none)" placeholder that needs cleaning.
  61072 BN HQ Admin. Currently 5,494 GSF from a prior FC 61010 weighted methodology run that was based on a category split I now think was wrong. Needs to be rederived from real billet category counts after the 102-PN delta is resolved (see below).
  61073 Co HQ. Literal 0 stub.
  14312 Operational Vehicle Laydown. TBD pending hidden-sheet UIC restructure and TE volume backfill.
  21451 Auto Organizational Shop. TBD. Two cells (F24 and J24) carry undocumented regression formulas with no FC citation that I could find. Reverted from a prior fabricated 1,129 GSF value.
  21710 Comm/Electronic Maint Shop. 583 GSF, FC chain produces it. Some orphan blocks need attention.

Personnel attribution. 710 of 1,324 TO rows are NOTE-tagged with a CCN. The remainder is unattributed because TO billet description quality varies and the prior session ran out of clock.

Equipment attribution. 506 TE rows, 506 attributed. The TE volume columns (Space Factor, NSY, NTG, L, W, H, Vol_EA, Vol_Tot) are mostly unpopulated, which blocks the equipment-driven CCN math from running cleanly.

The ASR-versus-CG-letter delta. The 102 PN. This is the biggest open question.

ASR carries 609 BICs (250 H&S + 179 Surg A + 180 Surg B). CG letter cites 711 PN. The delta is 102 PN. The plausible composition is civilian government employees (GS), contractors (CTR), and USN augmentees including Navy MD and DO officers, Navy hospital corpsmen attached, and Independent Duty Corpsmen. I do not know where any of those 102 sit physically. I do not know whether they rate space at 3d Med Bn or at the base medical clinic at USNH Okinawa or at a Branch Health Clinic. Until we know, the BFR cannot reconcile and the TFSMS reconciliation gate stays in PENDING. If you can pull a list from S-1 or BUMED Augmentation Branch (or whoever owns the augmentee tasking for 3d Med Bn at MCIPAC), the BFR can run to ground.

The methodology between Surg A and Surg B. By standing direction from leadership, Surgical Company A and Surgical Company B are doctrinally identical. They mirror each other in the BFR. They have the same TO structure (HQ Plt + 3 Surgical Plts + Ambulance Plt), the same TAMCN inventory of organic equipment for Role 2 deployment, and they rate identical garrison space. We pulled Surg A's actual room layout at Foster Bldg 5717 3rd Floor (CO, XO, SEL, LPO, OPS, three Plt Cdrs, ERC rooms, supply, conference room, two heads, mech rooms, comm room) and that becomes the model for Surg B's allocation at Kinser. Where Surg B currently shows Hawaii postal data (UIC M28262, AAC M29018, BOX 63062 Kaneohe), the BFR shows it but flags the postal block as TBD pending MCB Camp Butler G-1 Postal assignment after physical relocation.

Why FC Series 500 keeps coming up and what I think it actually says. FC Series 500 governs medical facilities. For Dispensary / Outpatient Clinic (53010), Primary Care Clinic (55010), and Ambulatory Care Center (55020), FC 500-2 directs that BUMED Echelon 3 Project Officers (for MCIPAC, that is Naval Medicine West) develop a Healthcare Requirements Analysis to size the clinical net area. Then the BFR applies Net-to-Gross 1.35 plus building grossing factors to land on GSF. FC does not give a closed-form factor per clinical billet. Only Dental Clinic (54010) has closed-form factors in FC, and 3d Med Bn has zero dental billets, so 54010 is not in scope.

That is the textbook regulatory finding. The practical reality is more useful. Once I read the footprint document carefully, in 559 lines of room data the only clinical-function hit is one room: Bldg 5717 room 216, BN Surgeon Clinic Ops, two workstations. There is no surgical suite, no exam rooms, no x-ray, no pharmacy, no ward in 3d Med Bn's occupied space. The unit is expeditionary. The surgical companies deploy and run Role 2 in the field on organic equipment. The clinical billets owned by 3d Med Bn TO&E who do fixed-clinic work do that work at the base medical clinic, which is USNH Okinawa or a BHC. Naval Hospital Okinawa owns its own BFR; 3d Med Bn does not claim that space.

What this means for the BFR: 3d Med Bn at garrison rates space mostly for admin, training, and storage, with a small dispensary (53010) for the BN Surgeon clinic-coordination cell. The CCNs are:

  61072 BN HQ Admin, sized to actual admin staff plus the un-deployed company head count, weighted by FC 61010 categories (Cat A 120 NSF private office, Cat B 64 NSF semi-private, Cat C 48 NSF shared, Cat D clinical at clinic rate, Cat E field-deployable at storage rate).
  17120 Applied Instruction, sized to MSTC training requirements.
  44112 Storage of Air or Ground Organic Units, sized to Role 2 organic equipment volume.
  14345 Armory, sized to weapon density per FC 14345-1.
  14312 Vehicle Laydown, 21451 Auto Org Shop, 21710 Comm/Electronic, 45110 Open Storage, sized to TE.
  53010 Dispensary, a small CCN sized to the BN Surgeon clinic-coordination cell only. This is the only Series 500 CCN the unit needs at garrison, and it does not need a BUMED HCRA at this scope because it is a coordination cell, not a clinical service.

Net-to-gross factors, in case anyone asks "why doesn't the math add up to the building". FC 2-000-05N bakes the un-usable space (corridors, stairwells, walls, mechanical rooms, electrical rooms, half-areas, restrooms, lobbies) into the rated GSF via Net-to-Gross factors that range from about 1.19 to 1.71 depending on function. NTG 1.40 is typical for admin. NTG 1.35 is typical for medical. The BFR's rated GSF is gross, not net. No unit ever occupies 100 percent of its BFR; that is by design.

Open questions for you to think through. I would rather flag these than guess. None of them are blockers in the sense of "can't do anything"; all of them shape the final numbers, and any answer is better than a fabrication.

  1. The 102-PN delta. Where do these people work, do they rate space at 3d Med Bn or at another facility, and how should they be split between H&S, Surg A, Surg B for billet attribution? S-1 or the BUMED Augmentation Branch should have the augmentee detail.

  2. CCN 53010 scope. We need to add a small 53010 sheet for the BN Surgeon clinic-coordination cell. Is the right scope just room 216 (BN Surgeon, 2 WS), or does it include Combat Stress (rooms 213-214, 2 WS) and Preventive Medicine (rooms 201-212, about 12 WS)? Different totals, different dispensary CCN size.

  3. Hidden CCN sheets. Three options for the four hidden sheets: full restructure (rebuild UIC sub-blocks to M28261 + M28263 + M28262 mirrored, unhide, bring into rollup), formula-fix only (repair lookup ranges in place, leave structure inherited), or delete and rebuild from a clean template. I lean toward full restructure but it is the longest road.

  4. Cover sheet metadata. Planner of record name and title. Programmed FY (FY26?). Project name or number. The repo references E_BFR_F_PRC_BU26-5836R_POM26 which suggests POM26 project BU26-5836R is the right number. Confirm. Region default is Okinawa for ACF / SIOH / PD / Contingency multipliers in the BFRL; that should be correct but worth a sanity check.

  5. Master TO&E backfill source. The TE volume columns are unpopulated. The reference data lives in M28261 / M28262 / M28263 per-company files plus the Master TO&E (which is dated 2025-04-11 and does not cover 3d Med Bn directly per its file metadata) plus FRMS v2.7.accdb. We need a definitive pull source for TAMCN dimensions. If you have a fresh TAMCN catalog cut, that is the cleanest path.

  6. Surg Co B postal block. The MISSION STATEMENT page carries TBD pending MCB Camp Butler G-1 Postal assignment. Do you have the assignment, or do we leave it TBD with a footnote citing G-1 Postal as the source action.

  7. Definition of done. The acceptance criteria has 10 items. The BFR is partial-green / partial-amber as of HEAD 3596107 on the working branch. Acceptable to release as a draft with explicit TBDs, or do we hold until everything is green.

  8. Dimensioned floor plan. The footprint document we have shows rooms by number with workstation counts but no measured square footage. If a CAD-quality dimensioned floor plan for Bldg 5717 (and the Kinser target buildings 107, 300, 400, 508, 613) exists, it lets us cross-check FC-derived SF against measured.

  9. CLB-4 cross-audit. CLB-4 is in the same repo as a teaching example (the format and methodology pattern). The corrected methodology in this session might apply to CLB-4 too, but I held off touching it. Worth doing in the same engineering pass or freeze CLB-4 and stay focused on 3d Med Bn.

What you have to work with right now. The current file is M67400-FO-M13020 3D MED BN-22NOV2024.xlsx. It opens cleanly, validates 8/0, has a clean cosmetic palette on the visible sheets, and produces real numbers for 14345, 17110, 17120, 44112, 21710, and 45110. It carries TBDs on 14312, 21451, 61072 (pending the 102-PN delta), 61073, and the unit total. The methodology workbook BFR_Generator_FC2-000-05N.xlsx has the FC factors loaded and the named-range API live for Okinawa. The audit folder in the repo has a project state document (audit/PROJECT_STATE_2026-05-07.md) that maps every CCN, every defect class, and every open question in one place if you want a deeper drill.

I'm sorry this is not a finished draft BFR. I went into the work expecting to produce one. The unit is small on paper, but every step toward a real number surfaced a doctrinal question I could not honestly answer without input. I would rather hand you a clean partial with the open questions enumerated than a finished draft full of fabricated numbers, because we both know the latter would not survive review.

If you want me to walk through any piece live before I'm out, let me know.

Best,
[your name]
