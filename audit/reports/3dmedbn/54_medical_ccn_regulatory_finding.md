# 3d MED BN BFR clinical CCN sizing, regulatory finding

Date: 2026-05-06
Branch: claude/apex-omega-audit-repair-gG9mM
Source for this finding: deep-research review by user using Claude
Sonnet 4.6 Thinking, citing FC 2-000-05N Series 500 (v.500.20231703,
17 March 2023) and DHA SPC Chapter 110 (15 December 2022).

================================================================
Doctrinal-correct path for 3d Med Bn clinical CCN sizing
================================================================

The 547 clinical billets currently misrouted to CCN 61073 (Co HQ
Admin = 0 SF) cannot be sized from any single public unclassified
table. FC 2-000-05N Series 500 explicitly delegates the sizing
authority for medical facilities. This delegation is the binding
regulatory path.

FC 2-000-05N Section 500-1 GENERAL, verbatim:

  "The Office of the Assistant Secretary of Defense Health Affairs
  (OASD (HA)) has primary responsibility for establishing functional
  space criteria and standards for medical facility programs
  necessary to fulfill the Secretary of Defense's responsibilities.
  The medical program is funded by the Assistant Secretary of
  Defense, Health Affairs (OASD (HA)); which provides annual
  programming guidance, performs defense-wide health care facility
  planning, project programming, reviews and adjusts projects for
  scope and cost. Using the OASD (HA) criteria, the Office of the
  Navy Surgeon General (BUMED) programs all medical projects for
  the Navy."

FC 2-000-05N Section 500-2 POLICY, verbatim:

  "The BUMED Echelon 3 command Project Officers will develop
  explicit planning documents for future year projects, including
  a Healthcare Requirements Analyses (HCRA), Economic Analyses
  (EA), Construction cost analyses, Make-versus-Buy Analysis, and
  Program for Design. Each medical MILCON project is unique and
  circumstances may warrant modification to the guidelines
  provided. The analyses will normally require the assistance of
  outside contractors."

For 3d Med Bn at MCB Camp Butler (MCIPAC), the BUMED Echelon 3
command of record is Naval Medicine West (NMW). The BFR cannot
independently size the medical CCNs.

================================================================
Per-CCN status, doctrinally correct
================================================================

CCN 53010 DISPENSARY AND OUTPATIENT CLINIC
  FC 2-000-05N Series 500 (v.500.20231703, 17 March 2023, p.6)
  GENERAL section verbatim, complete: "53010-1 GENERAL. Free
  Standing Clinic, outpatient clinic, which occupies a building
  or part of a building, but is not physically located with a
  hospital or medical center that provides routine and emergency
  care to authorized personnel."
  Sizing methodology in FC: NONE (definition only).
  BFR entry: TBD pending BUMED NMW HCRA + Program for Design,
  per FC 2-000-05N Section 500-2.

CCN 55010 PRIMARY CARE CLINIC
  FC 2-000-05N Series 500 v.500.20231703, p.12, verbatim:
  "55010-1 GENERAL. A primary care clinic provides the office,
  examination and treatment space for 'primary care managers'..."
  Sizing methodology in FC: NONE (definition only).
  BFR entry: TBD pending BUMED NMW HCRA.

CCN 55020 AMBULATORY CARE CENTER
  FC 2-000-05N Series 500 v.500.20231703, p.12, verbatim:
  "55020-1 GENERAL. A health care facility capable of performing
  outpatient surgical procedures and other medical treatment, not
  requiring extensive patient convalescence or overnight
  observation."
  Sizing methodology in FC: NONE (definition only).
  BFR entry: TBD pending BUMED NMW HCRA.

CCN 54010 DENTAL CLINIC
  Status: NOT APPLICABLE to 3d Med Bn.
  Reason: zero dental officers and zero dental staff in 3d Med Bn
  T/O. The 27 billets carrying Navy NEC L31A in the BFR's TO sheet
  are MEDICAL LABORATORY TECHNICIANS (BMOS L31A description "MED
  LAB TECH"), not dental personnel. The Navy NEC L3 series spans
  multiple medical specialties; L31A specifically is medical
  laboratory technology, not dental. Dental services for 3d MLG
  units at MCB Camp Butler are presumably administered by 3d
  Dental Battalion (separate unit, separate UIC, not 3d Med Bn).
  CCN 54010 should not appear in this BFR.

  This corrects the prior session's classification rule
  navy_nec_l3_dental that mapped any L3-prefixed NEC to CCN
  54010. The rule should be split: L31A -> medical lab (NCS
  53020 Medical Laboratory or rolled into 53010), L0xx hospital
  corpsman -> 53010 dispensary, etc. Specific dental NECs to be
  re-examined in audit/CLASSIFICATION_RULES.yaml.

================================================================
DHA SPC Chapter 110 applicability
================================================================

DHA Space Planning Criteria (SPC) chapters cover military
Medical Treatment Facilities (MTFs). Chapter 110 verbatim:

  "The purpose of this document is to outline how Space Planning
  documents are organized in order to facilitate planning,
  programming, and budgeting for DHA military Medical Treatment
  Facilities (MTFs)."

SEPS access restriction, verbatim: "SEPS is a proprietary tool
and requests for a DoD SEPS user account are limited to planners
supporting DHA facility projects or on other criteria established
by DHA-FE, CSM."

3d Med Bn is a Marine Corps operational unit, NOT a DHA-managed
MTF. DHA SPC chapters and SEPS are not directly applicable as a
BFR sizing tool for this unit unless NMW or NAVFAC Medical
Facilities Program Office certifies their use for an operational
USMC medical battalion garrison facility.

This is a binding constraint. Apex Omega rule 4: do not silently
adopt DHA SPC factors as if they were authorized for this BFR.

================================================================
Net-to-gross factors for use after net area is established
================================================================

FC 2-000-05N Table 500-1 (verbatim):

  Department Type                    Net/Gross Ratio
  Primary Care/Family Practice       1.35
  Emergency Services                 1.35
  Specialty Surgical Clinics         1.35
  Preventive/Occupational Medicine   1.35
  Dental Clinics                     1.35
  Surgery                            1.60
  Pathology                          1.25

FC 2-000-05N Table 500-2 building-level gross factors for Medical
and Dental Clinics, verbatim:

  Mechanical                         13.5%
  Electrical                          2.0%
  Circulation                        14.0%
  Half Areas                          1.5%

These factors apply AFTER net area is established through DHA
SPC/SEPS or HCRA, not as a substitute for it.

================================================================
Recommended action for the BFR
================================================================

1. Re-route the 547 clinical billets from CCN 61073 NOTE column
   to a new CCN 53010 NOTE column (Layer 2 reclassification).

2. Add CCN 53010 to CCN_Library and add a 53010 sheet to the
   workbook with TOTAL REQUIREMENT cell holding "TBD pending
   BUMED NMW HCRA per FC 2-000-05N Section 500-2".

3. Cite FC 2-000-05N Section 500-1 and 500-2 verbatim on the
   53010 sheet's footer.

4. Cite Table 500-1 and Table 500-2 net-to-gross factors in the
   sheet body for application post-HCRA.

5. UNIT_ROLLUP entry for 53010 carries the TBD value, not 0.

6. DD Form 1391 derivation deferred until HCRA is in hand.

================================================================
Apex Omega application
================================================================

Rule 1, facts only: every cited number above traceable to FC
2-000-05N Series 500 v.500.20231703 with page numbers, or to
DHA SPC Chapter 110 (15 December 2022). No invented sizing.

Rule 4, TBD where unverifiable: medical CCN sizes are honestly
marked TBD pending BUMED HCRA. The BFR is not silently filled
with a guessed number.

Rule 5, time-stamp at point of citation: FC 2-000-05N Series 500
current as of 17 March 2023. DHA SPC Chapter 110 current as of
15 December 2022. CG signed letter current as of 2 February 2026.

Rule 7, numbers traceable: zero invented numbers in this finding.
The 547 clinical billet count derives from BFR's own TO sheet
walked under deterministic UIC + section keyword filter.
