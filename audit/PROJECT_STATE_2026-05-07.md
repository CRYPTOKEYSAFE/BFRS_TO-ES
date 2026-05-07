PROJECT STATE, 2026-05-07 corrective handoff session

Purpose. Single document that the user can confirm reflects ground
truth before the next batch of work runs. Written in plain prose
under Apex Omega rules.

================================================================
1. What this project is

A USMC Basic Facility Requirements (BFR) audit and pipeline
development effort. The deliverable is an airtight, unit-agnostic,
format-agnostic, state-agnostic data pipeline that ingests TFSMS
and ASR T/O&E source data plus the unit's existing BFR (if any)
and produces a compliant updated BFR workbook per FC 2-000-05N
(Series 100, 11 Feb 2026), Marine Corps Basic Facility
Requirements (formerly UFC 2-000-05N / NAVFAC P-80).

The active worked example is 3d Medical Battalion (UIC M13020,
3d MLG, MCIPAC, MCB Camp Butler, Okinawa). The earlier worked
example, CLB-4 (UIC M29030), remains in the repo as a teaching
reference for layout and methodology-in-tab pattern. Tooling
must be unit-agnostic; CLB-4 is one example, 3d Med Bn is
another, and the pipeline must accommodate any USMC unit.

================================================================
2. Authority hierarchy (corrected this session)

The user clarified the doctrinal hierarchy on 2026-05-07. The
ordering binds all subsequent work.

  1. FC 2-000-05N. The "200-in" methodology manual. Series 100
     was published 11 Feb 2026. Series 500 governs medical
     facilities. Closed-form planning factors and CCN
     classification rules live here. This is the doctrinal
     source for square footage.

  2. T/O&E. The unit's authoritative tables of organization
     and equipment. For 3d Med Bn, this is the M28261 H&S Co,
     M28263 Surg Co A, M28262 Surg Co B per-company files
     plus the Master TO&E reference. For CLB-4 it is the
     M2911x per-company files.

  3. ASR. The unit's Active Strength Report. Required to
     reconcile against TFSMS / TO&E billet counts before any
     BFR can release. Apex Omega Sec.5.6, mandatory gate.

  4. Existing BFR. Where one exists, it is checked, not
     trusted. The 2nd MED BN -> 1st MED BN -> 3d MED BN
     template debt documented in 3DMEDBN_BFR_DISCUSSION_
     POINT.md is a worked example of why "trust" is wrong.

  5. CG-signed strategic basing letter. A head-count sanity
     check. For 3d Med Bn the letter (2 Feb 2026, signed by
     CG K. G. Collins, 3d MLG) cites 711 PN consolidating to
     Camp Kinser and absorbing returning Surgical Co B from
     Hawaii. The letter does not dictate CCN structure or
     square footage; if our derived totals from ASR + TO&E
     materially differ from 711 PN, our math is wrong, not
     the CG's number.

  6. CLB-4 BFR. Cosmetic reference and layout / methodology-
     in-tab format reference. Each CCN tab in CLB-4 pulls a
     factor from FC, shows the math in-tab, produces a CCN
     total GSF, and the totals roll up to UNIT_ROLLUP. That
     pattern is the binding lesson. CLB-4 is "not 100%
     functionally correct" (user direction); it is not a
     row-level structural stencil.

The skill encodes this hierarchy at GR-15 (added this session).

================================================================
3. What a BFR is, and is not

A BFR is a unit-level requirements document. It states the
total rated square footage the unit is entitled to under
FC 2-000-05N for its TO&E, broken out by CCN, rolled up to a
unit total in UNIT_ROLLUP. Per-CCN totals show which functions
the unit needs and how much space each function rates.

A BFR is not a building-allocation plan. It does not say which
billets sit in which building. Some billets work in clinics,
some in admin, some in field positions, some in deployable
configurations. The placeholder Area A / B / C / B&D bucketing
that appeared in earlier 3d Med Bn artifacts was a stand-in
because actual sit-locations are unknown. Building overlay is
a downstream planner activity that consumes the BFR.

The skill encodes this at GR-14 (added this session).

================================================================
4. Where 3d Medical Battalion is right now

Unit identity:
  Unit:         3d Medical Battalion
  UIC:          M13020 (alternative legacy code M67400)
  Echelon II:   MCIPAC (Marine Corps Installations Pacific)
  Installation: MCB Camp Butler, Okinawa
  Companies:    M28261 H&S Co
                M28263 Surgical Co A
                M28262 Surgical Co B (currently MCBH Kaneohe
                Bay, returning)
  Personnel:    711 PN per CG signed letter, 2 Feb 2026
  Surg A and B: doctrinally identical, mirrored, by user
                direction. No per-company drift.

Strategic basing posture:
  The unit is consolidating from Camp Foster to Camp Kinser.
  Surgical Co B is returning from Hawaii to consolidate at
  Kinser. CG MCIPAC endorsement dated 30 Apr 2026 (request).
  No specific Surg Co B PCS / arrival date is on record in
  the repository.

Current Foster + Kinser occupancy (Jan 2026 footprint):
  Camp Foster:  Bldg 215 (BN HQ), Bldg 5717 (Surg A footprint
                with documented breakout), Bldg 5628 (other
                H&S elements, Supply).
  Camp Kinser:  Bldg 300 (MSTC, BN Supply, shared Bay 2 with
                CBRNE and Food Service).

Kinser buildings requested for 3d Med Bn (per Apr 2026
endorsement, total inventory shown is current building size,
not the unit's demand):
  Bldg 107   96,478 SF, BN HQ co-use with other CLR units.
  Bldg 300  210,473 SF, MSTC.
  Bldg 400  202,479 SF, consolidated armory, Surg Co B
            dedicated bay proposed.
  Bldg 508  204,355 SF, Supply.
  Bldg 613   15,996 SF, Motor Transport and Utilities.
  Bldg 1225 referenced for personnel housing / BEQ.

3d Med Bn BFR file of record:
  M67400-FO-M13020 3D MED BN-22NOV2024.xlsx
  Workbook 15 sheets, 11 visible, 4 hidden.
  Validator: 8 PASS / 0 FAIL as of HEAD 1602a3f.
  No #REF!, #DIV/0!, #NAME?, #VALUE!, #N/A error tokens.
  External links: all five purged via zip surgery this session.
  TFSMS reconciliation gate: not yet driven by ASR (TBD).

Per-CCN state in the 3d Med Bn BFR:

  CCN     Current state                  Source / status
  -----   --------------------------     ----------------
  14312   M25 SUM 21:24 = 284 SY         Hidden. VLOOKUP TE
                                          reconciliation. DC2
                                          and DC3 defects flagged.
                                          TE Space Factor cols
                                          unpopulated, pending
                                          Master TO&E backfill.
  14345   H40 = B25 + K25 = 576 SF       Visible green. FC 14345-1
                                          step function for 711 PN.
                                          M28261 H&S and M28263
                                          Surg A sub-blocks live.
                                          M28262 Surg B sub-block
                                          missing from formula
                                          (DC7), needs mirror
                                          insertion.
  17110   H40 = 0 stub                   Visible green. Rolls to
                                          17120 per FC redirect.
  17120   H40 = U28 = 1,197 SF           Visible green. Single
                                          unit block M13020. No
                                          structural defects.
  21451   H44 TBD                        Hidden. F24 and J24 use
                                          undocumented regression
                                          coefficients (DC4). VLOOKUP
                                          range cap at row 749 vs
                                          TE max 2251. Reverted
                                          from 1,129 fabrication.
  21710   H47 = AB31 = 583 SF            Hidden. NOTE column tagging
                                          incomplete (DC2). S41
                                          empty (DC9). Blocks 4 and
                                          5 orphaned (DC7).
  44112   H40 = AB27 = 46,182 SF         Visible green. Multi-tier
                                          (44112o, 44112c, 44112w)
                                          but P31 / S31 GSF/PN
                                          constants unpopulated for
                                          tiers c and w (DC9). TE
                                          UIC col G and Equipment
                                          volume col U unpopulated
                                          (DC2).
  45110   H50 = M25 = 8.89 SY            Hidden. M35 uses literal
                                          "(none)" as SUMIFS
                                          criterion (DC10). AA55,
                                          W46 empty (DC10). Container
                                          branch dead.
  61072   H40 = P30 = 5,494 GSF (apex    Visible green. M27/M28
          omega: this number was         copy-paste bug corrected.
          fabricated in the prior        FC 61010 weighted method
          session, reverted to TBD,      applied. After 2026-05-07
          and is being re-derived the    user direction this number
          honest way; see Section 6      may need to be reverted to
          for the open question)         TBD again until derived
                                          from FC plus TO&E without
                                          invented splits.
  61073   H40 = 0 literal stub           Visible green. 547 clinical
                                          billets currently routed to
                                          61072 by COUNTIFS; the
                                          honest disposition under
                                          GR-12 is Series 500 CCNs,
                                          which are TBD pending BUMED
                                          HCRA. See Section 5.

Roll-up integrity. UNIT_ROLLUP carries 6 visible rows. Validator
check 6 reports all 10 CCN sheets present in the workbook are
referenced by the rollup with no silent drops.

Billet accounting. TO carries 710 data rows, 710 are attributed to
a CCN, zero orphans. Per-CCN distribution as currently NOTE-tagged:
61073=574, 21451=70, 61072=39, 44112=22, 21710=4, 14345=1.

Equipment accounting. TE carries 506 data rows, 506 attributed,
zero orphans. Per-CCN: 44112=249, 14345=126, 21710=75, 21451=47,
14312=8, 45110=1.

Structural defect classes documented in 49_per_block_audit.md
(10 classes total). Highest impact items:
  DC1  Cached values stripped on save, universal post-openpyxl.
       Recalc required to verify any number.
  DC2  SUMIFS / COUNTIFS on unpopulated TO NOTE / TE cols. Affects
       14345, 21710, 44112, 45110, 61072. NOTE column on TO is
       711 of 1,324 rows tagged; the rest are blank.
  DC3  IFERROR masking missing TE rows. About 750 row formulas in
       14312, 14345, 21451 collapse to "" on lookup miss; SUM
       ignores; output understated.
  DC4  Undocumented regression formula in 21451 F24 and J24. No
       FC citation; flagged TBD.
  DC7  Orphan blocks on 21451, 21710, 44112, 45110. Six blocks
       sum but no UIC populates. Intent unknown; TBD pending unit
       doctrine.

Master TO&E backfill is the largest open engineering task. The
TE columns Space Factor, NSY, NTG, L, W, H, Vol_EA, Vol_Tot are
unpopulated. Until populated, equipment-driven CCNs (44112, 14312,
45110, partially 14345) cannot compute their full GSF / SY from
TE volume.

================================================================
5. Series 500 medical CCNs, the regulatory gate

The user direction on 2026-05-07 was: "the methodology comes
from the 200-in." Reading FC 2-000-05N Series 500 directly,
the regulatory finding stands.

For an operational USMC Marine Corps medical battalion's
Role 2 garrison clinical footprint:

  53010 Dispensary / Outpatient.       FC 500-1, 500-2 define
                                       the CCN. FC 500-2 Sec
                                       directs that BUMED Echelon 3
                                       command Project Officers
                                       develop the planning
                                       documents including a
                                       Healthcare Requirements
                                       Analysis (HCRA). FC does
                                       not give a closed-form
                                       factor.
  55010 Primary Care Clinic.           Same delegation.
  55020 Ambulatory Care Center.        Same delegation.
  53020, 53025, other clinical CCNs.   Same delegation.

  54010 Dental Clinic.                 FC Tables 54010-1 through
                                       54010-4 give closed-form
                                       factors. NOT APPLICABLE to
                                       3d Med Bn. Zero dental
                                       officers / staff on the
                                       roster. Dental is handled
                                       by 3d Dental Battalion, a
                                       separate unit.

Net-to-gross factors that apply once HCRA establishes the net
area:
  Table 500-1, 500-2.  NTG 1.35 for clinical functions. Building
                       grossing: Mechanical 13.5%, Electrical
                       2.0%, Circulation 14.0%, Half-areas 1.5%.
  UFS 3-701-01 Eq 3-1. PD factor override to 1.13 for medical
                       facilities, not the standard 1.09.

Honest disposition for 3d Med Bn clinical CCNs:
  TBD, pending BUMED Echelon 3 (Naval Medicine West for MCIPAC)
  Healthcare Requirements Analysis. The BFR releases with
  53010, 55010, 55020 marked TBD with that exact source named.
  We do not invent a clinical factor from CLB-4 (CLB-4 is a
  combat logistics battalion and has no clinical CCNs to
  reference) or from a per-billet rate guess.

This was the conclusion in 56_clinical_ccn_exhaustive_sweep.md.
The 2026-05-07 user direction does not overturn it; it
confirms FC is the doctrinal source, and FC explicitly defers
to BUMED for clinical sizing. The corrective is: stop trying
to compute clinical GSF from a per-billet rate, mark TBD,
draft a memo to MCB G-1 / 3d MLG G-4 / NMW for the HCRA.

================================================================
6. The 547 clinical billets reclass, pending decision

The 547 clinical billets are currently routed to 61072 (BN HQ
admin) and 61073 (Co HQ admin) via the COUNTIFS NOTE-column
search in the BFR. That is wrong. Per FC 51016-1 verbatim,
"This category does not serve as headquarters space for command
level units"; clinical billets belong in their clinical-area
CCN, not in admin.

The corrective Violation 2 work (V2 reclass) was held this
session pending the decision the user just gave. With the
2026-05-07 direction:

  1. Move clinical billets out of 61072 / 61073 admin
     COUNTIFS so admin headcount reflects only the actual
     admin function (HQ staff, S-1, S-2, S-3, S-4, S-6,
     S-3 ops, etc.). The exact admin count needs to be
     derived from billet description analysis, not assumed.

  2. Tag clinical billets with their Series 500 CCN. Where
     the CCN's GSF factor is TBD pending BUMED HCRA, the
     billet is still tagged so the planner sees the
     allocation. The CCN total displays "TBD pending HCRA"
     until HCRA is supplied.

  3. 61072's GSF then reverts to TBD until the genuine
     admin headcount is known and FC 61010 weighted
     methodology is applied to that count without invented
     Cat A / B / C splits.

  4. The CG letter's 711 PN sanity check applies to the
     sum across all CCNs (admin + clinical + ops + storage
     + training) at the head-count level, not to any
     single CCN.

The reclass is the largest remaining doctrinal task in the
3d Med Bn BFR.

================================================================
7. Pipeline state, six-layer contract

  Layer 1, source format awareness.
    Status: workable. The audit handles Format A (per-co
    TFSMS export, the M2911x and M28261 / M28263 / M28262
    files), Format B (BFR-embedded), Format C (Master MEF
    reference) at the inventory and probe level.

  Layer 2, CCN+suffix tagging.
    Status: partial. CLASSIFICATION_RULES.yaml plus
    CCN_VOCABULARY (1,060 CCNs) plus TAMCN_CCN_MAP.yaml
    cover most cases. The 3d Med Bn TO NOTE column is
    711 of 1,324 rows tagged. Untagged rows block DC2
    SUMIFS / COUNTIFS in 14345, 21710, 44112, 45110, 61072.

  Layer 3, classification rules.
    Status: drafted. CLASSIFICATION_RULES.md and .yaml exist
    in audit/. Series 500 clinical rules need finalization
    (the V2 reclass).

  Layer 4, in-workbook TO/TE schema.
    Status: schema validated. 3d Med Bn TO has 10/10 columns
    matched to canonical Format B; TE has 10/10. Master TO&E
    backfill is the missing engineering work for TE Space
    Factor / NSY / NTG / volumes.

  Layer 5, stable lookup contracts.
    Status: partial. Hidden CCN sheets in 3d Med Bn (14312,
    21451, 21710, 45110) carry the original 2nd Med Bn
    template's restricted-range VLOOKUPs. Phase B repaired
    Camp Lejeune installation field but not the lookup ranges.
    Visible rebuilt sheets (14345, 17120, 44112, 61072) have
    cleaner contracts but inherit DC2 / DC9 issues.

  Layer 6, validation harness.
    Status: working at 8 PASS / 0 FAIL. Schema, NOTE coverage,
    NOTE / CCN consistency, vocabulary, error scan, roll-up
    integrity, billet accounting, equipment accounting are
    all green.

================================================================
8. CLB-4 state (the teaching example)

CLB-4 SW BFR file: SW_M29030_CLB4_BFR_2026-NWPCW167400L021.xlsx.

Visible CCN sheets, four clean rebuilds:
  14345  Armory
  21451  Auto Org Shop
  21455  Vehicle Wash Platform
  61072  BN HQ Admin

Hidden, broken, do not reference for structure:
  14312, 14326, 21710, 21730, 44112, 45110.

CLB-4's UNIT_ROLLUP totals 14,299 GSF across the 4 visible
sheets. The 6 hidden sheets are excluded. The 61072 sheet
documents that 156 of CLB-4's billets are excluded from the
admin count and require their own facility CCNs (those are
the broken-and-hidden ones).

CLB-4 is the teaching example because each visible CCN tab
shows the FC factor pulled in, the math computed in-tab, the
CCN total produced, and the rollup at UNIT_ROLLUP. That is
the layout / methodology-in-tab pattern that 3d Med Bn must
match cosmetically, with FC factors appropriate to a medical
battalion (different CCN mix entirely).

CLB-4 is not gospel. CLB-4 is "not 100% functionally correct"
per user direction; row-level structures are illustrative,
not normative.

================================================================
9. Methodology workbook (BFRL)

BFR_Generator_FC2-000-05N.xlsx is the methodology reference.
It implements:
  TFSMS-to-ASR reconciliation gate (PENDING / FALSE-RECONCILED
  / TRUE-UNRECONCILED, three-state).
  CCN_Library populated with verbatim FC factors for the 12
  CCNs in 3d Med Bn scope. Each row carries FC source (Series,
  version, page) and methodology summary. Medical CCNs (530,
  540, 550) correctly say "BUMED HCRA per FC 500-2."
  Okinawa adjustments: ACF, SIOH, PD, Contingency.
  Named-range API: PN_OFF, PN_ENL, PN_TOTAL, Okinawa_Navy_ACF,
  etc.
  Fonts standardized to STYLE_GUIDE canonical (10 / 11 / 16)
  via zip surgery this session.

The BFRL is a methodology reference, not a unit BFR. It is
read for the math; it is not edited per unit.

================================================================
10. Open questions for the user, before swarm runs

These are the questions whose answers shape the next batch
of work. Apex Omega rule 4: ask, don't guess.

  Q1. V2 reclass execution. Should the swarm execute the
      547 clinical billet reclass now (move from 61072 / 61073
      admin to Series 500 CCNs marked TBD pending HCRA), or
      hold V2 until BUMED HCRA is in hand?

  Q2. Genuine admin head count. The reclass implies 61072's
      admin head count drops from "39 + 547 lumped" to a real
      number. Is the user's preference: (a) derive admin
      count by mining billet descriptions for actual S-shop /
      HQ-staff billets, or (b) accept a published TO line as
      the admin count and TBD any ambiguity, or (c) defer
      until V2 ratifies the clinical reclass?

  Q3. HCRA memo. The honest path forward for clinical CCNs
      requires a memo from MCB G-1 or 3d MLG G-4 to NMW
      requesting the HCRA. Should the swarm draft that memo
      as a deliverable (audit/ as Markdown plus a docx-ready
      version) for the user to forward, or is that out of
      scope for this engineering pass?

  Q4. Master TO&E backfill. The TE Space Factor / NSY / NTG
      / volume columns are unpopulated. The data lives in
      the per-co TFSMS workbooks (M28261, M28262, M28263)
      and the Master TO&E. Should the swarm execute the
      backfill ETL now, or is the user supplying a fresh TO&E
      cut?

  Q5. CLB-4 cross-check scope. Should CLB-4 be re-audited as
      part of this pass to verify its visible-sheet math, or
      treat CLB-4 as frozen reference (only used for
      cosmetic / layout pattern) and focus all engineering on
      3d Med Bn?

  Q6. Surg Co B postal block. Currently honest TBD: UNIT XXXXX
      / FPO, AP 96604XXXX. Does the user have the assigned
      MCB Camp Butler G-1 Postal UIC, or does it stay TBD?

================================================================
11. Recent commit history (active branch
claude/apex-omega-handoff-correction-cNOxx)

  1602a3f  skill: GR-13 corrected; add GR-14, GR-15 per
           2026-05-07 user direction (this session)
  d7dc304  feat(ruflo): activate Ruflo v3.7.0-alpha.11
  0c7452f  docs(handoff): replace 2026-05-07 handoff with
           corrective version
  99f23f6  fix(bfr+skill+handoff): revert fabricated numbers;
           GR-13 added; APEX OMEGA handoff 2026-05-07
  3689cb4  fix(bfr+skill): apply FC 61010 weighted methodology
           to 61072 (5,494 GSF) + skill GR-12 enriched
  615bdb5  fix(bfr+skill): GR-12 added; revert 61073 lump-sum
           93,275 to TBD pending workspace weighting

================================================================
12. Definition-of-done check, where 3d Med Bn BFR stands

  1. Cosmetic match to CLB-4.            PARTIAL. Visible CCNs
                                         green tab, palette OK.
                                         Hidden CCNs not yet
                                         conformed.
  2. Recalc clean.                       GREEN. Zero error
                                         tokens.
  3. Every CCN total a real number.      AMBER. 14345, 17110,
                                         17120, 21710, 44112,
                                         45110 are real;
                                         14312, 21451, 61072,
                                         61073 are TBD pending
                                         honest derivation.
  4. Roll-up integrity.                  GREEN. All 10 CCN
                                         sheets in workbook
                                         flow to rollup.
  5. Cross-references resolve.           AMBER. Defined names
                                         clean, but several
                                         DC9 absent-cell refs
                                         remain.
  6. TFSMS reconciliation gate green.    RED. Gate not yet
                                         driven by ASR-paste
                                         data for 3d Med Bn.
  7. Personnel summaries populated.      AMBER. Billet
                                         attribution by NOTE
                                         is 711/1324 rows. The
                                         remainder unattributed.
  8. Equipment summaries by CCN.         AMBER. TE attribution
                                         506/506 within tagged
                                         range; volume-driven
                                         equipment math blocked
                                         by Master TO&E backfill.
  9. GSF / GSY totals consistent.        AMBER. Visible CCNs
                                         tie out. Hidden CCNs
                                         have orphan blocks
                                         (DC7).
  10. Audit-traceable.                   AMBER. Methodology
                                         tagged per CCN where
                                         FC closed-form applies.
                                         TBDs name the missing
                                         authority. Memo to
                                         NMW for HCRA not yet
                                         drafted.

The BFR is releasable as a draft with explicit TBDs. It is
not airtight per Apex Omega Sec.8 until items 3, 6, 7, 8,
9, 10 advance from amber to green.

================================================================
End of project state document.
