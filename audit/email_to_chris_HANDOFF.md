Subject: 3d Med Bn BFR, handoff while I'm out

Chris,

Bottom line first. I'm out next week and I owe you a draft BFR for 3d Medical Battalion that I do not have ready. The work is partway done. The file is in much better shape than the one we inherited, but every time I tried to pin a number down I uncovered another question that needs a real answer instead of a guess. I would rather hand you the questions and what I worked out than hand you a number I made up.

Everything I have been working from is in the 3d MLG MS Teams channel. That is the live source. If anything is missing on your side, tell me and I will mirror it.

What the BFR is supposed to do, in case it helps to restate. The BFR states the unit's rated facility space, broken out by CCN, rolled up to a unit total. It does not assign people to buildings. It says: under FC 2-000-05N, given the unit's TO&E and operating posture, the unit rates X amount of armory, Y amount of admin, Z amount of equipment storage, and so on, and the unit total comes out to W gross square feet. A planner downstream takes the BFR and decides which building gets which function.

What I have been pulling from. All in Teams.

  FC 2-000-05N. The 200-in. Series 100 was published 11 Feb 2026 and sets the methodology baseline. Series 500 is the medical chapter. Series 600 covers admin (61072 in particular). All eight series PDFs plus Appendix A are in the channel.

  3DMLG_ASR.xlsx. The Active Strength Report. It carries 609 BICs broken out 250 H&S, 179 Surg A, 180 Surg B.

  The CG signed strategic basing letter, dated 2 Feb 2026, signed by K. G. Collins, CG 3d MLG. Cites 711 PN consolidating to Camp Kinser plus Surgical Co B returning from MCBH Kaneohe Bay.

  The January 2026 footprint document for Foster and Kinser, room by room.

  M28261 H&S, M28263 Surg A, M28262 Surg B per-company TFSMS files.

  The current BFR file: M67400-FO-M13020 3D MED BN-22NOV2024.xlsx.

History of this BFR file, because it explains why the work has been harder than it should have been. The file did not start clean. In 2017, NAVFAC Mid-Atlantic issued a BFR template for 2nd Medical Battalion at Camp Lejeune. Around May 2018 that template was copied for 1st Medical Battalion at Camp Pendleton. On 22 November 2024 it was copied again for 3d Medical Battalion. Each copy carried forward the original layout, the formulas, and the live links back to the prior installation's SharePoint. By the time the file landed in front of me it had nine years of accumulated debt riding inside it.

Things I found and fixed in this round.

  The installation field on multiple sheets still said Camp Lejeune. Corrected to MCB Camp Butler.

  Five live links to other files (Pendleton SharePoint, plus one fake link to a 2029 TFSMS export that does not exist) were severed. The file no longer pops the "this file has links to other data sources" warning when you open it.

  The template carried four hidden sheets (vehicle laydown, auto org shop, comm/electronic maintenance, open storage) that referenced 2nd Med Bn UICs including a phantom Surg Co C that does not exist in 3d Med Bn. The Surg Co C ghost is gone from the visible work; the four hidden sheets still need their UIC sub-blocks rebuilt to reflect 3d Med Bn (M28261 H&S, M28263 Surg A, M28262 Surg B).

  The 61072 admin sheet had a copy-paste bug where the formula was searching for the wrong CCN string. Fixed.

  The 14345 armory sheet was double-counting. It now reads 576 GSF per FC 14345-1 for the 711-PN strength bracket.

  The methodology workbook (BFR_Generator_FC2-000-05N.xlsx, the BFRL) was scrubbed. The CCN library is populated with verbatim FC factors per CCN. Okinawa adjustment factors are live.

Where the BFR file is today. It opens cleanly. No error cells (no #REF!, no #DIV/0!, no #N/A). No broken links. No rogue references.

Visible CCN sheets: 14345 (Armory), 17110 (Education stub), 17120 (Applied Instruction), 44112 (Storage of Air or Ground Organic Units), 61072 (BN HQ Admin), 61073 (Co HQ stub). Hidden sheets: 14312 (Vehicle Laydown), 21451 (Auto Org Shop), 21710 (Comm/Electronic Maintenance), 45110 (Open Storage).

CCN by CCN, where each one stands:

  14345 Armory. 576 GSF. Real, FC-derived.
  17110 Education. 0 GSF stub. Correct, rolls to 17120.
  17120 Applied Instruction. 1,197 GSF. Real, FC produces it.
  44112 Storage. 46,182 GSF from TE volumes. The constants for the climate-controlled and weather-tight tiers need verification before sign.
  45110 Open Storage. 8.89 SY, real but a dead criterion needs cleanup.
  61072 BN HQ Admin. Currently 5,494 GSF. Needs to be rederived once the 102-PN delta below is resolved.
  61073 Co HQ. 0 GSF stub.
  14312 and 21451 are TBD. The hidden sheets need their UIC sub-blocks rebuilt before they can compute honestly.
  21710 Comm/Electronic. 583 GSF. Some orphan blocks need attention.

Personnel attribution. 710 of 1,324 TO rows are tagged to a CCN. The rest is untagged because the billet description quality on TO varies, and I ran out of clock to push it the rest of the way.

Equipment attribution. All 506 TE rows are tagged, but the volume columns are mostly unpopulated, which blocks the equipment-driven CCN math.

The 102-PN delta. This is the biggest open question.

ASR shows 609 BICs (250 H&S + 179 Surg A + 180 Surg B). CG letter cites 711 PN. The delta is 102 PN. Plausible composition is GS civilians, contractors, and USN augmentees (Navy MD/DO officers, hospital corpsmen attached, IDCs). I do not know where any of those 102 sit physically. I do not know whether they rate space at 3d Med Bn or at the base medical clinic at USNH Okinawa. Until we know, the BFR cannot reconcile against the ASR. If you can pull augmentee detail from S-1 or the BUMED Augmentation Branch, the BFR can run to ground.

Surg A and Surg B mirror methodology. By standing direction, Surgical Company A and Surgical Company B are doctrinally identical and mirror each other in the BFR. They have the same TO structure (HQ Plt + 3 Surgical Plts + Ambulance Plt), the same Role 2 organic equipment, and they rate identical garrison space. We pulled Surg A's actual room layout at Foster Bldg 5717 3rd Floor (CO, XO, SEL, LPO, OPS, three Plt Cdrs, ERC rooms, supply, conference room, two heads, mech rooms, comm room) and that becomes the model for Surg B's allocation at Kinser. Where Surg B still shows Hawaii postal data, the BFR shows it but flags the postal block as TBD pending G-1 Postal assignment after the physical relocation.

Why FC Series 500 keeps coming up, and what I think it actually means here. FC Series 500 governs medical facilities. For Dispensary (53010), Primary Care Clinic (55010), and Ambulatory Care (55020), FC 500-2 directs that BUMED Echelon 3 Project Officers (for MCIPAC, that is Naval Medicine West) develop a Healthcare Requirements Analysis to size the clinical net area, and then the BFR applies grossing factors. FC does not give a per-billet number for clinical space. Only Dental Clinic (54010) has closed-form factors in FC, and 3d Med Bn has zero dental billets, so 54010 is not in scope.

That is the textbook position. The practical reality is more useful here. Once I read the footprint document carefully, in 559 lines of room data the only clinical-function hit is one room: Bldg 5717 room 216, BN Surgeon Clinic Ops, two workstations. There is no surgical suite, no exam rooms, no x-ray, no pharmacy, no ward in 3d Med Bn's occupied space. The unit is expeditionary. The surgical companies deploy and run Role 2 in the field on organic equipment. The clinical billets owned by 3d Med Bn TO&E who do fixed-clinic work do that work at the base medical clinic, which is USNH Okinawa or a Branch Health Clinic. USNH Okinawa owns its own BFR; 3d Med Bn does not claim that space.

What that means for the BFR. 3d Med Bn at garrison rates space for admin, training, and storage, with a small dispensary (53010) for the BN Surgeon coordination cell. The CCNs are 61072 admin (sized to actual admin staff plus the un-deployed company head count, weighted by FC 61010 categories), 17120 training (MSTC), 44112 storage (Role 2 organic equipment), 14345 armory, 14312 vehicle laydown, 21451 auto org shop, 21710 comm/electronic, 45110 open storage, and 53010 small dispensary. That is it.

A note on net-to-gross in case it comes up. FC bakes the unusable space (corridors, stairwells, walls, mechanical rooms, electrical rooms, restrooms, lobbies, half-areas) into the rated GSF through Net-to-Gross factors that run from about 1.19 to 1.71 depending on function. Roughly 1.40 for admin and 1.35 for medical. The BFR's number is gross, not net. No unit ever occupies 100 percent of its BFR; that is by design.

Open questions for you to think through. None are show-stoppers; all of them shape the final numbers.

  1. The 102-PN delta. Where do these people work, do they rate space at 3d Med Bn or at another facility, and how should they split between H&S, Surg A, Surg B for billet attribution. S-1 or BUMED Augmentation Branch should have it.

  2. CCN 53010 scope. We need to add a small 53010 sheet for the BN Surgeon clinic-coordination cell. Is the right scope just room 216 (BN Surgeon, two workstations), or does it include Combat Stress (rooms 213-214) and Preventive Medicine (rooms 201-212). Different numbers depending on the answer.

  3. The four hidden CCN sheets. They need to be brought into 3d Med Bn shape. Three options: full rebuild (UIC sub-blocks reset to M28261, M28263, M28262 mirrored, then unhide and roll up), formula-fix in place (repair the lookups but leave the 2nd Med Bn skeleton), or delete and start fresh. I lean toward full rebuild but it is the longest road.

  4. Cover sheet metadata. Planner of record (name and title), programmed FY (FY26?), project name or number. The Teams channel has a POM26 package referencing project BU26-5836R; confirm that is the right number. Region defaults to Okinawa for the adjustment factors.

  5. Master TO&E backfill. The TE volume columns are unpopulated. The reference data lives in the per-company TFSMS files plus the Master TO&E plus the FRMS database. We need a definitive pull source for TAMCN dimensions. A fresh TAMCN catalog cut would be the cleanest.

  6. Surg Co B postal block. Currently TBD pending G-1 Postal assignment after physical relocation. Either we get the assignment now, or it stays TBD with a footnote.

  7. Dimensioned floor plan. The footprint document shows rooms by number with workstation counts but no measured square footage. If a CAD-quality floor plan for Bldg 5717 and the Kinser target buildings (107, 300, 400, 508, 613) exists somewhere, we can cross-check the FC-derived numbers against measured.

What you have to work with right now. The current BFR file is M67400-FO-M13020 3D MED BN-22NOV2024.xlsx. It opens cleanly, runs without errors, has a clean look on the visible sheets, and produces real numbers for 14345, 17110, 17120, 44112, 21710, 45110. It has TBDs on 14312, 21451, 61072 (pending the 102-PN delta), 61073, and the unit total. The methodology workbook (BFR_Generator_FC2-000-05N.xlsx) has the FC factors loaded and the Okinawa adjustments live.

I am sorry this is not a finished draft. I went into the work expecting to produce one. The unit is small on paper, but every step toward a real number surfaced a question I could not answer without input. I would rather hand you a clean partial with the open questions enumerated than a finished draft full of fabricated numbers. We both know the second one would not survive review.

If you want me to walk through any piece live before I am out, let me know.

Best,
[your name]
