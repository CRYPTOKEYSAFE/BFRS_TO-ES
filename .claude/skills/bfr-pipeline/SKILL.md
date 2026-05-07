---
name: bfr-pipeline
description: USMC Basic Facility Requirements (BFR) audit and workbook generation for the BFRS_TO-ES repository, under Apex Omega methodology. Use whenever the user asks about BFR worksheets, BFRL, FC 2-000-05N planning factors, TFSMS / ASR / T/O&E ingestion, CCN classifications, the data pipeline between T/O&E source data and BFR output, the cosmetic style of generated workbooks, or any operation on the .xlsx files in this repo. Triggers include words like BFR, BFRL, CCN, TFSMS, ASR, T/O&E, FC 2-000-05N, UFC 2-000-05N, P-80, INFADS, NTG factor, GSF/GSY/NSY, ACF, SIOH, MILCON, Okinawa, MCIPAC, MCB Camp Butler, MLG/MEF/CLB unit names, Apex Omega.
---

# BFR Pipeline Skill (project-local)

Activate this skill the moment any BFR-related task is requested in this
repository. It encodes the Apex Omega methodology, the project's
contract, conventions, audit state, and binding style guide so a fresh
session does not re-derive them or drift.

## Read-first artifacts (always, in this order)

1. `APEX_OMEGA.pdf`, binding methodology briefing. Non-negotiable
   rules in Sec.2; anti-patterns in Sec.6; QC rituals in Sec.5; output
   conventions in Sec.8.
2. `CLAUDE.md`, repository overview + Apex Omega rules restated +
   working conventions.
3. `audit/PIPELINE.md`, six-layer unit-agnostic data pipeline contract.
4. `audit/BFR_GENERATOR_NOTES.md`, annotated tour of the
   `BFR_Generator_FC2-000-05N.xlsx` (methodology + math reference). The
   workbook was originally supplied as `MCBJ_BFR_Generator_FC2-000-05N.xlsx`
   and renamed in this repo per the no-MCBJ rule. Current correct
   nomenclature is MCIPAC (Marine Corps Installations Pacific) and
   MCB Camp Butler. Do not use "MCBJ", "MCBB", or
   "COMMARCORBASESJAPAN" as a place/org term.
5. `audit/STYLE_GUIDE.md`, binding cosmetic specification (CLB-4 theme
   styling + Apex Omega 4-color cell-role palette).
6. `audit/FINDINGS.md`, Round-1 forensic findings on CLB-4 plus
   Round-3 finding 9 (TFSMS_UNRECONCILED gate at TFSMS_Loading!$D$19
   is structurally broken: the cell is part of merged range B19:O19
   so it cannot hold a value at its named-range coordinate; defect
   surfaced for methodology-owner direction, not silently fixed).

## Project mental model

The end-state is a unit-agnostic ETL + generator that:

1. Ingests TO&E source data in any of four observed formats:
   - Format A (per-company MCTOFD-style export, no CCN tagging)
   - Format B (BFR-embedded TO/TE, CCN+suffix in NOTE column)
   - Format C (Master MEF/MTOMS-T-style, rich data, CCN header empty)
   - Format D (TFSMS / ASR / authoritative PDF, extract via pdfplumber
     with per-row page+table citation; low-confidence values marked
     `TBD, pending [page reference]`)
2. Classifies every billet to a `<CCN><suffix>` NOTE tag using a
   documented rule set (FC 2-000-05N planning factors + unit doctrine).
3. Emits a Format-B-compliant in-workbook TO and TE.
4. Generates CCN calculation sheets that reproduce the CLB-4
   rebuilt look exactly (per `STYLE_GUIDE.md`) and use stable lookup
   contracts (full-column refs, no IFERROR masking).
5. Validates the output against a deterministic harness (Layer 6).
6. Rolls up to a `UNIT_ROLLUP` sheet that traces every cell back
   to a CCN sheet's TOTAL REQUIREMENT cell.

## Hard guardrails (added 2026-05-06 after session-specific failures)

These guardrails encode mistakes the assistant has actually made
in this session and the corrected behavior. They override
default LLM tendencies. Read these first; everything below is
context.

GR-1 SOURCE HIERARCHY IS FIXED. DO NOT BLEND.
  - Regulatory:        FC 2-000-05N (Series 100-800), MCO 11000.12,
                       UFS 3-701-01, UFC 4-510-01, BUMED instructions.
  - Authoritative:     ASR (3DMLG_ASR.xlsx), 2031 Master TO&E v1.1,
                       BFR_Generator_FC2-000-05N.xlsx (BFRL),
                       embedded TFSMS data inside the BFR's
                       MISSION STATEMENT sheet.
  - Program-practice:  unit-supplied basing assessments (Tab B, Tab C),
                       footprint PDFs, building schedules.
  - External benchmark:GAO, AACE, JED, JDDG.
  Tab C is program-practice, NOT regulatory. Do NOT use Tab C
  GSF figures as binding sizing inputs. Tab C is a sanity-check
  reference at most. The same applies to Tab B and any briefing
  deck.

GR-2 DO NOT GUESS SIZING FACTORS.
  When FC 2-000-05N gives a factor, use it. When FC says
  "engineering study" or "engineering evaluation", that IS the
  answer; mark TBD pending engineering study and cite the FC
  section verbatim. Do not invent a factor by extrapolating from
  a sibling CCN. Do not invent the words "engineering study"
  when FC says nothing about sizing (e.g., CCN 53010 has only
  a definition; sizing flows through FC Section 500-2 to BUMED
  HCRA, not to an engineering study).

GR-3 DO NOT EXTRAPOLATE FROM TYPING.
  Do not classify a billet because its NEC/MOS/BMOS string
  matches a substring you remember. Look up the actual code
  meaning before classifying. Example failure this session: a
  classification rule mapped any Navy NEC starting with "L3" to
  CCN 54010 Dental, which routed 27 MEDICAL LABORATORY
  TECHNICIANS (BMOS L31A, billet description verbatim "MED LAB
  TECH") to a dental clinic. L3 is not dental; L31A is medical
  laboratory.

GR-4 DO NOT WANDER LOOKING FOR WORDS, NAMES, OR PLACEHOLDERS.
  When the BFR has a placeholder string ("FOSTER BUILDING TBD",
  "Camp Kinser", "Surg Co C"), the fix is not to grep for a
  substitute word. The fix is:
   1. identify the field's purpose from the surrounding TFSMS
      Unit TO&E Report context;
   2. apply the doctrinal field convention (postal block, mission
      statement, CCN library, etc.);
   3. fill from primary source or mark TBD with the regulatory
      path.

GR-5 NUMBERS COME FROM FORMULAS OR PRIMARY SOURCES. PERIOD.
  Every numeric output the assistant produces must be either
  (a) verbatim from a primary-source document with citation,
  (b) computed by an explicit formula whose inputs are
  primary-source values with citations, or (c) marked TBD with
  the source that would resolve it. Apex Omega rule 7 is binding.
  Watch out for: constant offsets in IF formulas that produce a
  defensible-looking number from zero inputs (CCN 21451 J24
  =347*M33+1129 produces 1129 when M33=0 because of the
  y-intercept; that's not a real requirement).

GR-6 THE 2031 MASTER TO&E v1.1 IS A 3D MED BN PRIMARY SOURCE.
  The skill previously stated the Master TO&E "does not cover
  CLB-4". That statement was true for CLB-4 specifically and
  was incorrectly extrapolated to mean "does not cover any
  unit". For 3d MED BN, the file contains:
    M28261 H&S Co     : 288 billets, 198 equipment lines
    M28262 Surg Co B  : 211 billets, 148 equipment lines
    M28263 Surg Co A  : 210 billets, 160 equipment lines
  with full L/W/H/Vol/NSY columns populated. This is the
  authoritative TO&E source for 3d MED BN equipment-driven CCN
  sizing. The Org_Qty column represents unit-level authorized
  total per the FY2031 cut, not per-billet instances.

GR-7 H&S TFSMS DATA EXISTS, EMBEDDED.
  The skill previously stated "H&S TFSMS does not exist and
  will not exist." That is false. The H&S Co (M28261) TFSMS
  Unit TO&E Report is embedded in the BFR's MISSION STATEMENT
  sheet starting at row 1, with the postal block, the structure
  data current as of 02/27/2023, and the FEB 3 2021 signed
  Mission Statement at row 31. Do not wait on a separate H&S
  TFSMS file; read the MISSION STATEMENT sheet.

GR-8 WHEN A USER SUPPLIES A DOCTRINAL DIRECTION, IT IS BINDING.
  Examples from this session, exact phrasing:
   - "Surg A and B should be identical, even if you don't have
     any info on the other...they are identical on paper."
     -> A=B rule binding for billets, equipment, GSF, address.
   - "Stop chasing locations; the BFR is the overarching
     document."
     -> Mission statement does not carry building numbers; BFR
        is requirements not status.
   - "No placeholder crap."
     -> Strip TBD-pending bracketed text from cells; flag in
        audit logs and commit messages, not in the workbook
        itself.
   - "We are not stuck on where the unit is at right now ... we
     need the BFR correct so we can right size the unit into
     the proper facilities."
     -> BFR is a requirements doc, not a current-state tracker.

GR-9 BEFORE ASKING ANOTHER QUESTION, READ EVERYTHING.
  This session repeatedly surfaced facts that were available in
  files the assistant hadn't read. The 2031 Master TO&E was in
  the repo from session start, but I asked the user about
  H&S sizing instead of reading it. The MISSION STATEMENT sheet
  contained H&S TFSMS data, but I asked about it instead of
  reading it. The user's binding directive is "imagine I have
  told you to read EVERYTHING." Apply it.

GR-10 THE EXTERNALLINKS PURGE MUST OUTLIVE A "RECALC".
  A LibreOffice headless recalc or any openpyxl save can
  reintroduce externalLinks/* parts inside the xlsx archive
  even when the prior session "purged" them at the formula
  level. After any save or recalc, re-verify zero entries
  under xl/externalLinks/ and zero references in xl/workbook.xml,
  xl/_rels/workbook.xml.rels, and [Content_Types].xml. Use the
  zip-surgery script at audit/reports/3dmedbn/47_external_links_purge.txt
  pattern as the canonical purge.

GR-11 SETTINGS.JSON HOOK REGISTRATION IS REQUIRED.
  A SessionStart hook script at .claude/hooks/session-start.sh
  is not executed unless registered in .claude/settings.json
  under hooks.SessionStart. The prior session "fixed" the hook
  but never registered it. Settings.json must contain the
  registration plus enableAllProjectMcpServers=true so
  .mcp.json's ruflo entry loads without per-session approval.
  See settings.json fix at commit 3407bdf.

GR-12 DO NOT LUMP-SUM BILLETS AT 162.5 GSF/PN ADMIN RATE.
  The 162.5 GSF/PN factor in FC 61010-1.1 is the MAXIMUM admin
  allowance, not a per-billet entitlement. It assumes each
  billet has dedicated admin workspace (private office or
  workstation type 1). Most clinical, technical, and field-
  deployable billets do not work in admin space; their primary
  workspace is in another CCN (clinical, lab, surgical, vehicle
  shop, or in deployable equipment). Lumping all 547 clinical
  billets in a medical battalion at 162.5 GSF each produces a
  number (93,275 SF) that overstates required garrison
  administrative space by an order of magnitude.
  Correct treatment: weight billets by primary workspace type:
    Category A (full private office, ~120 NSF): CO, XO, S-shop
      chiefs, billet leaders. Typically 10-20 billets BN-wide.
    Category B (workstation type 1, ~64 NSF): SNCOs, section
      heads, primary admin staff.
    Category C (workstation type 2, ~36-48 NSF): junior admin
      clerks who actually work at a desk daily.
    Category D (clinical / lab / surgical workspace, NOT admin):
      surgeons, anesthesiologists, surg techs, lab techs,
      radiology, pharmacy, holding ward staff. Their primary
      workspace is in a Series 500 clinical CCN, not 61073.
    Category E (field-deployable, minimal garrison): Surg Plt,
      FRSS, STP, ERCS, Ambulance Plt clinical staff. Their
      primary workspace is deployable equipment stored under
      CCN 44112; minimal garrison admin desk.
    Category F (shared / shift workspace): rotating clinical
      staff, watchstanders. One workstation per N billets.
  User direction received 2026-05-07 verbatim: "these people
  they don't work in the building they work in the clinic they
  work in the area so lump them all together it makes it look
  big too big. We have to weight some of these guys some work
  like basement clinics having them we're actually in the
  actual clinical spaces."
  Apex Omega rule 1: do not invent the per-billet rate. Either
  read the actual workspace allocation from the unit's basing
  document (which the BFR is producing), OR mark TBD pending
  workspace allocation methodology.

  AUTHORITATIVE FC 2-000-05N Series 600 v.600.20230203 numbers
  (Table 61010-5.1, p.4 + Table 61010-7.1, p.6 + Note 5):

    Private Office  120 NSF/PN (range 100-120) supervisory
    WST1             64 NSF/PN (range 48-64)   general admin
    WST2             48 NSF/PN (range 36-48)   hoteling/telework
    Admin support     8 NSF/PN
    Break room        2 NSF/PN (without kitchen)
    Conf/training NSF/PN per Table 61010-7.1A band:
      band 1-25 PN     25 NSF/PN
      band 26-50 PN    18 NSF/PN
      band 51-150 PN   15 NSF/PN
    NTG factor       1.40 if loading <50 PN; calculated otherwise.
    Ceiling          162.5 GSF/PN per FC 61010-7.1.1 verbatim
                     "shall not exceed".

  Compute pattern: NSF_workspace = sum over Cat A/B/C of (count
  x per-billet NSF). Add BAG additives (admin support + break +
  conf/training band-by-band). Apply NTG. Compare to ceiling
  (PN x 162.5); take the lesser.

  Worked example, 3d MED BN BN HQ 39 PN: 6 Cat A x 120 + 33 Cat B
  x 64 = 720 + 2112 = 2832 NSF workspace + 39 x 28 BAG = 1092 NSF
  = 3924 NSF total x 1.40 NTG = 5494 GSF. Ceiling 39 x 162.5
  = 6338 GSF. Take 5494 (within ceiling).

  Clinical billets (Category D) flow to Series 500 CCNs, NOT 610
  admin: per FC 51016-1 verbatim ("This category does not serve
  as headquarters space for command level units"), within-clinic
  admin stays in the clinic CCN. Each billet is loaded once at
  the planning area / category code where its work occurs.

  Field-deployable equipment (Category E) flows to CCN 44112
  (Storage of Air or Ground Organic Units) per FC 44112-1, sized
  by stored equipment volume not by per-billet rate.

GR-13 CLB-4 FOUR CLEAN CCN SHEETS ARE THE STRUCTURAL REFERENCE.
  When a 3d MED BN (or any unit) CCN sheet needs computation,
  the binding move is: read the corresponding CLB-4 clean
  rebuilt CCN sheet (14345 Armory, 21451 Auto Org Shop, 21455
  Vehicle Wash Platform, 61072 BN HQ Admin) cell by cell,
  extract its row-by-row formula structure, and reproduce that
  structure with the new unit's inputs. Do NOT compute from a
  per-billet rate guess. Do NOT invent a category split (e.g.,
  "25% of officers in private office"). If CLB-4 has no parallel
  structure for the CCN, mark TBD pending unit-supplied basing
  data.
  User direction received 2026-05-07 verbatim: "I gave you a
  long time ago example of what CLB-4 BFRL looks like and how
  it adds up. I think we've came a long way from that."
  This guardrail returns the work to that reference.

## Hard rules (Apex Omega override defaults)

- Facts only. No assumptions, speculation, AI jargon. Ask if unclear.
- Cite source + section + date inline for every regulatory or
  numeric claim. Format: *"FC 2-000-05N Sec.61010-3, current as of
  2026-02-11"*.
- Three-bucket separation: regulatory / program-practice / external
  benchmark. Never blend.
- Mark unverified items as `TBD, pending [source/action]`. Never
  silently fill.
- Show the math. Every derived number reproducible from inputs in
  the same artifact (formulas in Excel, equations in Markdown).
- Plain prose. Lead with the answer. No "let's", no "I'll help you",
  no preamble, no marketing tone, no emojis.
- Typography. No em dashes (U+2014). No en dashes (U+2013). No double
  hyphen used as em dash. No markdown asterisk bold. No dash separators
  used for emphasis. Hyphens within identifiers and compound words
  (FC 2-000-05N, MCB Camp Butler, NAVFAC P-72, unit-agnostic) stay.
  Markdown list bullets at line start are allowed as functional
  markers. Emphasis via sentence structure or ALL CAPS, sparingly.
- Reconciliation gate. TFSMS RecapMCC must be reconciled against
  ASR / T/O&E before any BFR is releasable. The
  `TFSMS_UNRECONCILED` flag in the BFR Generator at
  `TFSMS_Loading!$D$19` is the
  operational implementation. Never bypass.
- Recalc requirement. Every openpyxl-generated workbook must be
  recalculated by LibreOffice headless before delivery. Zero `#REF!`,
  `#DIV/0!`, `#NAME?`, `#VALUE!` after recalc.
- Unit-agnostic. CLB-4 is the worked example. Tools take a unit
  identifier or path as input.
- Cosmetic fidelity. Generated workbooks reproduce the CLB-4
  rebuilt-clean-CCN look (theme tints, fonts, fills, borders, merged
  cells, page setup, footer text) plus the Apex Omega 4-color
  cell-role palette (input `#FFF8DC`, calc `#EAF3F4`, output `#DCE7C8`,
  warning `#F8E2D6`). No "default openpyxl" output.
- Source files are read-only. Inputs in repo root are never edited.
  Outputs go under `audit/` or a clearly-named output directory.
- Branch: development branch is set per session by the Claude Code
  harness; the session-suffixed branch name appears in the harness
  instructions at session start. Push there. Never push to `main`
  without explicit instruction. Commit and push at meaningful
  milestones (the stop hook enforces this). Do not name a specific
  session-suffix in this skill; it goes stale instantly.

## Input contract (accept any format the unit hands us)

| Input | Possible formats |
|---|---|
| T/O&E source data | Excel (TFSMS per-co; Master MEF / TFSMS-style), PDF (TFSMS printable, ASR PDF, other authoritative printout) |
| Existing BFR for the unit | Excel (Format B; may be stale, partial, or mid-edit) |
| Project metadata | Manual (UIC, building no., planner, programmed FY, region), no DD 1391 field; DD 1391 is a downstream MILCON document, not a BFR field |

PDF ingestion: every extracted record carries source filename + page
+ table/row reference. Low-confidence extractions are marked
`TBD, pending [page reference]`. Tooling: `pdfplumber`, `camelot`,
`tabula-py`, or text-mode with hand-coded splits; OCR only for scanned
PDFs.

## Operational modes

- Update-existing (common case): existing BFR + new T/O&E  to 
  refreshed BFR + diff report.
- Generate-new: T/O&E only to fresh BFR built against canonical
  template.
- Audit-existing: existing BFR only to forensic findings + repair
  plan.

## Definition of done, binding acceptance test

(Full text in `CLAUDE.md` and `audit/PIPELINE.md`. Summary here:)

1. Cosmetic match to CLB-4 + Apex Omega palette.
2. Zero `#REF!`/`#DIV/0!`/`#NAME?`/`#VALUE!`/`#N/A` after LibreOffice
   headless recalc.
3. Every CCN sheet's TOTAL REQUIREMENT computes a real, traceable number.
4. Roll-up integrity, every CCN flows to UNIT_ROLLUP once, no drops,
   no double counts.
5. All cross-references resolve. No external links. No #REF!/#N/A
   defined names.
6. `TFSMS_UNRECONCILED = FALSE`; `PN_*` named ranges populated.
7. Personnel summaries (by rank/MOS/MCC) accurate.
8. Equipment summaries by CCN accurate.
9. GSF/GSY totals consistent across all sheets.
10. Inline citations for every regulatory or numeric claim.

A deliverable failing any one of these is `TBD, pending <failing item>`.

## Authoritative references (Apex Omega Sec.3), confirm currency at use

| Reference | Use |
|---|---|
| FC 2-000-05N (Series 100, 11 Feb 2026) | Marine Corps BFR (primary for this work) |
| MCO 11000.12 | Real Property Facilities Manual |
| UFS 3-701-01 | DoD Facilities Pricing Guide / ACF (Okinawa Navy ACF FY26 = 2.34) |
| UFS 3-730-01 | Economic analysis / ERC |
| UFC 3-740-05 (with Change 1) | Cost engineering policy |
| UFC 4-010-01 | DoD Minimum Antiterrorism Standards (ATFP) |
| UFC 3-310-04 | Seismic design |
| GAO-20-195G | GAO Cost Estimating Guide |
| AACE Recommended Practices | Cost-estimate class definitions |
| JED Cost Estimating Guide (Nov 2025) | Japan Engineer District cost rules |
| JDDG v9 (Apr 2025) | Japan District Design Guide |

## Pipeline-spine quick reference

The `NOTE` column in the BFR workbook's `TO` sheet carries tags of the
form `<CCN><suffix>`. Observed suffix vocabulary (not yet canonical , 
must be ratified against FC 2-000-05N):

| Suffix | Meaning |
|---|---|
| `o` | Office (>= E-6 / officer), 120 GSF/person |
| `c` | Cubicle (<= E-5), 60 GSF/person |
| `w` | Warehouse worker, 60 GSF/person, /3 ratio |
| `rs`/`cs`/`ds`/`ws`/`shf`/`ms` | Maintenance shop sections (radio/comm/data/wire/SHF/maint), counted /15 to bays |
| `a` | Armory work-area / personnel |
| (bare CCN) | Equipment record's primary facility CCN (TE rows) |
| `1` | Personal Effects entitlement, 1 per chargeable person |

CCN calculation sheets count via `COUNTIFS('TO'!$B:$B, "21710o",
'TO'!$E:$E, $B$32)` etc., `'TO'!$B:$B` is the NOTE column,
`'TO'!$E:$E` is the UIC column (per Format B schema).

## File inventory (as of round 3 merge from main)

- Apex Omega briefing: `APEX_OMEGA.pdf` (root). Read first.
- Methodology + math reference: `BFR_Generator_FC2-000-05N.xlsx`
  (root). Implements TFSMS reconciliation gate, CCN library
  (1,060 entries, Layer 5 done), Okinawa adjustments, named-range
  API. See `audit/BFR_GENERATOR_NOTES.md`.
- One observed CLB-4 BFR example (NOT a gold standard, no gold
  standard exists): `SW_M29030_CLB4_BFR_2026-NWPCW167400L021.xlsx`
  (Feb 2026). Roll-up = 14,299 GSF across 4 visible CCN sheets;
  materially incomplete per audit/FINDINGS.md. Useful for cosmetic
  typography (extracted to STYLE_GUIDE.md) and as one illustration of
  how a CLB-shaped BFR is laid out. Structural / row-level patterns
  derive from FC 2-000-05N, not from this file. Per-unit-type patterns
  (MAG, MWHS, MEU, depot, training command, etc.) are different and
  must be derived from FC 2-000-05N and doctrine for that unit type.
- Stale, do not use: `FO_M29030_CLB 4_FINAL BFR.xlsx` (May 2025).
- Clean rebuild sheets in the CLB-4 SW file (use only as a cosmetic
  example, not a structural template): `14345`, `21451`, `21455`,
  `61072`.
- Hidden broken sheets: `14312`, `14326`, `21710`, `21730`, `44112`,
  `45110`, same workbook. Lookup ranges all `#REF!`. Do not extend
  these; rebuild against the contract.
- TFSMS exports (Format A, per company):
  `M29111_HQ_CO_CLB-4.xlsx`, `M29112_CLC_A_CLB-4.xlsx`,
  `M29113_CLC_B_CLB-4.xlsx` (openpyxl-touched),
  `M29114_GS_CO_CLB-4.xlsx` (openpyxl-touched).
- Master TO&E (Format C, TFSMS-style):
  `2031 Master TO&E v1.1 - 20250411.xlsx`, does not cover CLB-4
  (covers a different MEF/MLG; M29030/M29111-14 absent).
- Canonical CCN dictionary (Layer 2):
  `audit/CCN_VOCABULARY.yaml` / `.csv` / `.json`, 1,059 distinct CCNs
  extracted from `fc_2_000_05n_appendixa.pdf` (WBDG, dated 2019-06-27).
  Provenance block in YAML records source URL, document date,
  extraction date. Re-extractor: `audit/extract_ccn_appendix_a.py`.
- Source PDF for the CCN dictionary: `fc_2_000_05n_appendixa.pdf`
  (root). Time-stamp at citation: 27-JUN-2019. Authority chain:
  FC 2-000-05N Appendix A to NAVFAC P-72 (DON Facility Category Codes).
- Per-unit-type defaults (Track 6):
  `audit/UNIT_TYPE_DEFAULTS.yaml`. Maps each USMC unit_type
  identifier (CLB, MLG_HQ, MEF_HQ, MEU_CE, MAG_HQ, MWHS,
  AVIATION_SQUADRON, RECRUIT_DEPOT, SCHOOLHOUSE, TRAINING_COMMAND,
  DEPOT, INSTALLATION_HQ, plus a `default` fallback) to a dict of
  defaults consumed by `pipeline/classify.py`. Currently the only
  field is `admin_ccn`; schema is intentionally a per-type dict so
  more fields can be added (default Okinawa ACF, default NTG, etc.)
  without breaking existing rows. CLB is confidence high
  (admin_ccn 61072, cited from observed CLB-4 SW BFR plus NAVFAC
  P-72 Category 610). Every other unit type is admin_ccn TBD,
  confidence low, pending FC 2-000-05N Series 100 ratification.
  Apex Omega rule 4: TBD or unknown unit_type causes the
  classifier to inject `{admin_ccn_TBD}` into the rule template,
  which leaves an unresolved placeholder and surfaces affected
  billets as orphans in validator Check 7. Loaded by
  `Classifier.__init__`; precedence is rule-table defaults
  (lowest, backward-compat fallback) < per-unit-type row <
  explicit unit_context overrides (highest). Unit profile must
  declare `unit_type` for the per-type row to apply (see
  `samples/clb4_profile.json` for the worked example).
- TAMCN to facility CCN doctrine table (Layer 5):
  `audit/TAMCN_CCN_MAP.yaml`. Maps each USMC TAMCN to its facility
  CCN via ordered regex rules. Schema mirrors
  `audit/CLASSIFICATION_RULES.yaml`: ordered `rules` list, each rule
  has `id` / `description` / `pattern` (regex on the upper-cased
  TAMCN) / `facility_ccn` / `confidence` (high / medium / low) /
  `citations`. Apex Omega rule 4: rules with `facility_ccn: TBD`
  are intentional and the matcher must skip them so the TAMCN
  surfaces as an orphan in `pipeline/validate.py` Check 8 instead
  of receiving a guessed CCN. A `tamcn_validator` regex at the top
  filters out non-equipment rows that leak through Format-A
  ingestion (header rows, footnote rows, date strings).
  `unmapped_disposition.do_not_silently_drop: true`.
- Pipeline package: `pipeline/`
  - `pipeline/template.py`, Layer 4 BFR generator. Produces a
    Format-B BFR for any unit profile + CCN list. Three pattern
    variants (primary_items, admin, shop_with_bays) plus default
    fallback.
  - `pipeline/validate.py`, Layer 6 validator. Eight-check pass/fail
    report against any Format-B BFR workbook (schema, NOTE
    coverage, NOTE-CCN consistency, vocabulary, cell errors,
    roll-up integrity, billet accounting, equipment accounting).
  - `pipeline/classify.py`, Layer 3 classifier. Maps a billet
    record to a NOTE tag using `audit/CLASSIFICATION_RULES.yaml`.
    Honors Apex Omega rule 4 (TBD rules emit unclassified, never
    a guessed tag).
  - `pipeline/etl.py`, end-to-end orchestrator. Reads Format-A
    T/O&E files, classifies via classify.py, populates TO and TE
    via template.py, emits run report.
- Sample inputs: `samples/clb4_profile.json`,
  `samples/clb4_ccns.json`. Worked-example unit profile and CCN list
  for CLB-4.
- Sample outputs:
  `out/CLB4_BFR_sample.xlsx` (template-only, 10 CCNs, validator
   8 PASS / 0 FAIL because TO and TE empty).
  `out/CLB4_BFR_full.xlsx` (full ETL, 359 billets and 885
   equipment rows from four company files; validator 5 PASS /
   3 FAIL with the FAILs surfacing 184 unclassified billets and
   885 unmapped equipment rows pending rule-table ratification
   plus TAMCN-to-CCN doctrine table).
- Validator reports at `audit/reports/16` (CLB-4 SW BFR),
  `audit/reports/17` (template-only sample), `audit/reports/20`
  (full ETL sample). ETL run report at `audit/reports/19`.
- Typography sweeper: `audit/strip_dashes_and_bold.py`. One-shot tool
  that removes em dashes, en dashes, and markdown bold from every
  text file in the repo. Re-run if any new content sneaks them back
  in.

## Standard tooling

Install once: `pip install openpyxl pdfplumber pypdfium2 formulas`.

Audit (read-only inspection):
```bash
python3 audit/inventory.py "<file.xlsx>"
python3 audit/sheet_dump.py "<file.xlsx>" "<sheet>" [max_row]
python3 audit/schema_map.py
python3 audit/pipeline_probe.py
python3 audit/style_extract.py "<file.xlsx>" "<sheet>" [<sheet>...]
```

Pipeline (write):
```bash
python3 audit/extract_ccn_appendix_a.py
python3 audit/expand_ccn_library.py
python3 audit/extract_planning_factors.py
python3 pipeline/classify.py --to <Format-A.xlsx> --out <classified.csv>
python3 pipeline/template.py --profile <profile.json> --ccns <ccns.json> --output <path.xlsx>
python3 pipeline/etl.py --profile <profile.json> --ccns <ccns.json> \
    --to-files <co1.xlsx> <co2.xlsx> ... --output <path.xlsx>
python3 pipeline/validate.py <workbook.xlsx> [--report <path>]
```

Single-shot end-to-end for any unit (once the BMOS rules and
TAMCN-to-CCN doctrine tables are ratified):
```bash
python3 pipeline/etl.py \
    --profile samples/<unit>_profile.json \
    --ccns samples/<unit>_ccns.json \
    --to-files <co1.xlsx> <co2.xlsx> <co3.xlsx> ... \
    --output out/<unit>_BFR_full.xlsx
python3 pipeline/validate.py out/<unit>_BFR_full.xlsx \
    --report audit/reports/NN_validate_<unit>.txt
```

Capture audit output into `audit/reports/<NN>_<name>.txt` and commit.
The report numbering convention is sequential (`01_`, `02_`, ...),
keep it.

## Work tracks, recommended order

Authored 2026-04-28. Each track is independent enough to commit as a
unit; the order is the recommended build sequence.

### DONE

- Layer 2, CCN vocabulary lock. Extracted 1,059 canonical CCNs
  from FC 2-000-05N Appendix A. Outputs: `audit/CCN_VOCABULARY.yaml`,
  `.csv`, `.json`; report `audit/reports/15_ccn_vocabulary_extraction.txt`;
  re-extractor `audit/extract_ccn_appendix_a.py`. Commit `c328a36`.
- Documentation hygiene. Dropped DD 1391 field from BFR docs and
  the methodology workbook; purged "MCBJ" and "COMMARCORBASESJAPAN"
  legacy terminology from cells; renamed workbook
  `MCBJ_BFR_Generator_FC2-000-05N.xlsx`  to 
  `BFR_Generator_FC2-000-05N.xlsx`. Commits `0a2c8cc`, `1a61265`.
- Layer 5, CCN_Library expanded to 1,060 entries. Repopulated
  `BFR_Generator_FC2-000-05N.xlsx`'s `CCN_Library` sheet from
  `audit/CCN_VOCABULARY.json` (1,059 canonical) merged with the 23
  originally curated rows (planning-factor data preserved). One
  curated CCN, `143 13 Operational Vehicle/Equipment Canopy`, is
  net-new vs. the 2019 canonical generation; flagged for verification
  against any newer NAVFAC P-72 release. `CCN_TABLE` named range
  expanded to `CCN_Library!$C$6:$I$1100`. Build script:
  `audit/expand_ccn_library.py`. Recalc-clean (5,424 nodes, zero
  error tokens via Python `formulas` package; LibreOffice headless is
  non-functional in this sandbox so `fullCalcOnLoad=True` is set on
  the workbook). Commit `0817a1c`.
- Track C, Layer 6 validation harness. `pipeline/validate.py`
  implements the six Layer-6 checks from `audit/PIPELINE.md` (schema,
  NOTE coverage, NOTE<->CCN consistency, vocabulary against
  `audit/CCN_VOCABULARY.json`, cell-error scan, roll-up integrity).
  Unit-agnostic; auto-detects TO/TE header rows, CCN sheets, and
  UNIT_ROLLUP. Run against CLB-4 SW BFR as the worked example
  (`audit/reports/16_validate_clb4_sw.txt`): 3 PASS / 3 FAIL,
  surfacing the round-1 findings deterministically, empty NOTE
  column, 10,577 #REF! tokens in hidden CCN sheets, and 6 hidden CCN
  sheets absent from UNIT_ROLLUP. Commit `95ea12a`.
- Typography sweep. Em dashes, en dashes, and asterisk bold stripped
  from every text file. Rule encoded in `CLAUDE.md` and this skill.
  Sweeper: `audit/strip_dashes_and_bold.py`. Commit `adcf5c9`.
- Track B, Layer 4 canonical BFR template generator.
  `pipeline/template.py` produces a Format-B BFR for any unit profile
  + CCN list. Banner block (rows 1-7), data rows 8-13, subtotal rows
  15-16, TOTAL REQUIREMENT at H37. UNIT_ROLLUP with per-CCN totals.
  TO and TE sheets with Format-B headers (rows 6 and 4). Apex Omega
  four-color cell-role palette applied. Sample run for CLB-4 (10 CCNs)
  at `out/CLB4_BFR_sample.xlsx`; validator report at
  `audit/reports/17_validate_generated_clb4.txt` shows 6 PASS / 0 FAIL.
  Sample inputs at `samples/clb4_profile.json` and
  `samples/clb4_ccns.json`. Commit `6369ff6`.
- Layer 5 pattern templates (observed shapes, not canonical). Three
  per-CCN-sheet pattern builders added to `pipeline/template.py`:
  `primary_items` (shape from CLB-4 14345 Armory), `admin` (shape from
  CLB-4 61072 BN HQ Admin, with optional excluded-billets header),
  and `shop_with_bays` (shape from CLB-4 21451 Auto Org Shop). Also a
  `default` fallback for any CCN without pattern_data. PATTERN_DISPATCH
  table dispatches by `spec.pattern` string. CcnSpec gained
  `pattern: str` and `pattern_data: dict` fields. Sample updated to
  exercise three patterns. TBD, pending: ratify pattern shapes /
  factors / NTG values against FC 2-000-05N planning factor tables.
  CLB-4 is one observed example, not a gold standard. Commit
  `b9ab701`.
- Layer 6 advanced checks added to `pipeline/validate.py`. Check 7
  Billet accounting (TO data row count, attributed via NOTE column,
  orphans, distinct attributed CCNs, unknown-CCN references) and
  Check 8 Equipment accounting (TE data row count, attributed via
  NOTE or CCN column, orphans, distinct attributed CCNs,
  unknown-CCN references). Validator now runs 8 checks. Real CLB-4
  SW BFR drops from 3 PASS / 3 FAIL to 3 PASS / 5 FAIL surfacing
  303 TO billet orphans (NOTE column empty) and 99 TE equipment
  orphans plus 5 attributed CCNs. Generated CLB-4 sample stays
  8 PASS / 0 FAIL.
- Planning-factors extractor scaffold at
  `audit/extract_planning_factors.py`. Reads
  `fc_2_000_05n_100series_*.pdf` and `fc_2_000_05n_200series_*.pdf`
  when supplied, walks every page, finds Table NNNNN-N references,
  emits per-CCN records into `audit/PLANNING_FACTORS.{yaml,json}`
  with source PDF + version date provenance. First-pass extraction
  marks loading_driver / factor_value / ntg as
  "TBD pending manual ratification" since regex-on-PDF-text cannot
  reliably parse multi-column tables; manual ratification is the
  authoritative step. Script exits non-zero with instructions when
  the Series PDFs are missing.
- Layer 3 classification rules starter at
  `audit/CLASSIFICATION_RULES.md` (doctrine doc, schema and
  general-pattern rules) and `audit/CLASSIFICATION_RULES.yaml`
  (machine-readable rule table). Maps each billet to a NOTE tag of
  the form CCN+suffix using the function
  `(BIC, Billet Description, Alpha Grade, BMOS, PMOS, MCC) -> tag`.
  General-pattern rules (officer/SNCO/warrant -> office, junior
  enlisted -> cubicle) are tagged confidence=high; BMOS-specific
  rules covering 0600 comm, 0800 artillery, 1300 engineer, 1800
  armor, 2300 EOD, 2800 data/cyber, 3000 supply, 3500 motor T, 5800
  MP, 5900 electronic maintenance, 6000 aviation maintenance, 6500
  aviation ordnance, 7200 ATC, and 8000 medical are tagged
  confidence=low with TBD citations pending FC 2-000-05N Series
  100/200 ratification. unclassified_disposition is "orphan, do not
  silently drop" so the validator surfaces unmapped billets in
  Check 7. Commit `16caec1`.
- Layer 3 classifier at `pipeline/classify.py`. Loads
  `audit/CLASSIFICATION_RULES.yaml`, takes a billet record and unit
  context, returns NOTE tag plus rule_id and citation, or
  unclassified with reason. Pay-grade parser handles USMC ranks
  (LTCOL, GYSGT, SGTMAJ, etc.), Navy officer abbreviations (ENS, LT,
  LCDR), and Navy enlisted rate codes (HM1, RP3, MAC, HMCS, HMCM).
  Section inference reads keyword patterns from Billet Description
  (admin_or_hq, auto_org_shop, comm_shop, data_shop, medical, eod,
  ordnance, supply, engineer, mp, field_maint). Apex Omega rule 4
  honored: rules with TBD tag_template emit unclassified, never a
  guessed tag. Smoke test on M29111 HQ Co (96 billets): 57
  classified, 39 unclassified. Commit `de3891c`.
- End-to-end ETL at `pipeline/etl.py`. Reads one or more Format-A
  T/O&E files, classifies every billet via pipeline/classify.py,
  extracts every TAMCN row, populates the generated BFR's TO and TE
  sheets via pipeline/template.py. Emits run report with per-file
  counts, classified/unclassified totals, per-CCN breakdown.
  End-to-end run on the four CLB-4 company TFSMS exports (M29111,
  M29112, M29113, M29114): 359 billets and 885 equipment lines read,
  175 billets classified (49%), 184 surfaced as orphans for SME
  review. Per-CCN top: 21451 (43), 61072 (39), 21730 (34), 21710
  (28), 14326 (18), 44112 (13). Generated workbook at
  `out/CLB4_BFR_full.xlsx`. Validator: 5 PASS / 3 FAIL (the FAILs are
  expected, NOTE coverage and accounting orphans waiting on rule-table
  ratification and TAMCN-to-CCN doctrine). Commit `de3891c`.
- CLB-4 Series 800 worked example expanded. Methodology owner
  supplied per-CCN spec for 12 Series 800 facilities applicable
  to a CLB-shaped unit; entries added to `samples/clb4_ccns.json`
  with cited factors:
    85210 Parking Area (SY)             100 vehicles x 75 SY (FAC 8521)
    85122 Vehicle Staging Area (SY)     5,000 SY mount-out (FAC 8523)
    85121 Vehicular Parking Unsurfaced  0 (paved primary) (FAC 8522)
    87210 Station Security/Perimeter    2,000 LF fence (FAC 8721)
    87250 Entry Gate (LF)               30 LF for 1-2 gates (FAC 8721)
    87230 Mechanical Security Barricade 2 EA drop-arm (FAC 1458)
    83143 Hazardous Waste Storage Bldg  400 SF (FAC 4423)
    83141 Hazardous Waste Stg/Transfer  1 EA structure (FAC 8926)
    81160 Standby Generator Plant (KW)  150 KW (FAC 8112)
    88010 Fire Alarm System (MI)        1 MI (FAC 1351)
    85235 Other Paved Areas (SY)        1,000 SY misc (FAC 8526)
    85240 Misc Open Storage Paved (SY)  2,000 SY (FAC 8526)
  Each entry's loading_label cites FAC code, the user-supplied
  spec, and explicit "placeholder pending unit input / Series 800
  PDF cross-check" notes. CCN 87250 (ENTRY GATE, added Jan 2024
  post-Appendix-A-2019-extraction) added to
  `audit/CCN_VOCABULARY.json` with explicit `_provenance_note`
  flagging it for verification on next vocab refresh. Generated
  CLB-4 BFR now spans 23 CCN sheets (was 11). Validator: 6 PASS
  / 2 FAIL (Check 4 Vocabulary now passes with 87250 added; the
  2 FAILs remain Check 2 NOTE coverage and Check 7 billet
  accounting on the 42 BMOS-rule-lift-pending billets).
  Series 300 (v300.20230302, 2 Mar 2023) and Series 800
  (v800.20250331, 31 Mar 2025) PDFs landed on origin/main at
  commit 2a6d06a immediately after this entry was first authored.
  Re-extraction now covers all 6 Series PDFs: 1,003 distinct CCN
  records (was 780, +223), 564 factor tables, 712 engineering-
  study CCNs with narrative captured. Per-Series counts: 100=357,
  200=187, 300=60, 400=53, 500=20, 600=16, 700=158, 800=152.
  Citation footers on the 12 CLB-4 Series 800 sheets lifted from
  TBD to cited: 85210 cites Series 800 v2025-03-31 pages 60-63
  Table 85210-1 with the parking-ratios-per-facility-type table
  rows visible verbatim; 87210 cites pages 70-72 Table 87210-1
  with the SRC-I/II ammo fence and chain-link/wooden alternatives
  visible inline; 81160/83143/83141/88010/85235/85240 cite their
  Series 800 narrative_section first lines (engineering-study).
- Track 8, TFSMS_UNRECONCILED reconciliation gate repaired
  (methodology-owner direction received: Option A1 unmerge plus
  three-state gate). The B19:O19 merge was unmerged; B19:C19
  (merged) now holds the label "Reconciliation Gate"; D19:O19
  (merged) holds the live formula returning one of three states:
  PENDING (yellow, ASR not yet provided), FALSE - RECONCILED
  (green, TFSMS=ASR, BFR releasable per DoD item 6), TRUE -
  UNRECONCILED (red, TFSMS<>ASR; per-bucket diagnostic at rows
  41-51 surfaces which bucket is off). ASR data entry section
  added at TFSMS_Loading rows 26-37 mirroring the TFSMS layout
  (rows 9-17). PN_* named-range family added parallel to
  TFSMS_* family (PN_MAR_OFF/PN_MAR_ENL/PN_NAV_OFF/PN_NAV_ENL/
  PN_OS_OFF/PN_OS_ENL/PN_RES_OFF/PN_RES_ENL/PN_CIV/PN_CTR/PN_NC/
  PN_TOTAL all in row 37). Recalc verification: 5,553 cells, zero
  error tokens via Python `formulas` package; fullCalcOnLoad=True.
  CLAUDE.md item 6 updated to document the three-state workflow.
  audit/FINDINGS.md Finding 9 closed; new Finding 9b records the
  repair. The user's stated workflow ("sometimes I have ASR,
  sometimes I don't") is now supported without weakening Apex
  Omega Sec.5.6: PENDING is the truthful default state, not
  silently treated as "OK". Definition of Done item 6 satisfiable
  for any unit once user pastes both TFSMS and ASR counts.
- Track 1f, FC 2-000-05N Series 400/500/600/700 PDFs landed
  (origin/main commit e00823c, merged into dev branch). Series 300
  and 800 still not supplied (training/range and utilities/ground;
  not on the CLB-4 critical path).
  fc_2_000_05n_400series_11_19_2025.pdf  v400.20251119  19 Nov 2025
  fc_2_000_05n_500series_03_17_2023.pdf  v500.20230317  17 Mar 2023
  fc_2_000_05n_600series_03_02_2023.pdf  v600.20230302   2 Mar 2023
  fc_2_000_05n_700series_11_19_2025.pdf  v700.20251119  19 Nov 2025
- audit/extract_planning_factors.py extended to walk every Series
  PDF present in repo root (not just 100/200) with two layout
  fixes for Series 600: (a) HEADING_CONT_RE handles wrapped
  headings where the UoM is on the next line (e.g., "610 72
  BATTALION/SQUADRON HEADQUARTERS, MARINE" / "CORPS (SF)"); (b)
  FAC_RE relaxed to treat the colon as optional (Series 600
  writes "FAC 6100" without colon, others use "FAC: NNNN").
  Re-extraction output: 780 distinct CCN records (was 533, +247),
  267+263 = 530 factor tables, 535 engineering-study CCNs with
  narrative captured. Series 100=357, 200=187, 400=53, 500=20,
  600=16, 700=158. ALL 10 CLB-4 worked-example CCNs now have
  citations: 14345 Armory factor-table; 14312 factor-table; 14326
  / 21451 / 21455 / 21710 / 21730 engineering-study from supplied
  PDFs; 44112 (Series 400 page 46) / 45110 (Series 400 pages 50-51)
  / 53010 (Series 500 page 8) / 61072 (Series 600 page 39)
  engineering-study from newly supplied PDFs.
- Track 5b, TAMCN orphan closure. `audit/TAMCN_CCN_MAP.yaml`
  extended with 7 cited rule additions: medical_amal_kits lifted
  from confidence=low TBD to high (Series 500 53010 cited);
  comm_admin_computers (A9-series to 61072 admin per Series 600
  61072-1); comm_a7_e_class_test_kits (A7xxxxE to 21710);
  weapons_aav_recovery (E-prefix K-class full-tracked vehicles
  to 21710); misc_b_g_recon_instrument (B-prefix G-class to 21730);
  misc_c_t_class_machine_tools (C-prefix T-class to 21451);
  weapons_eod_x_class (E-prefix X-class to 14326). After:
  TAMCN orphans 27 to 0; per-CCN attribution: 44112 (314), 21710
  (225), 14345 (184), 14326 (69), 21451 (30), 61072 (15),
  21730 (11), 53010 (6). `samples/clb4_ccns.json` gained 53010
  (CLB-4 BAS Dispensary) at 4 officers + 30 enlisted from
  audit/FINDINGS.md item 2.
- Track 1c-factor (citation-side), FC factor row rendering on
  the citation footer. `pipeline/template.py` `fc_citation_lookup`
  now emits each table's body rows verbatim under the citation
  block. Apex Omega rule 7 ("numbers must be traceable") satisfied
  at the point of use: 14345 Armory sheet now shows on its footer
  the full step function (up to 2,000 personnel: 576 SF; 2,001 to
  4,000: 880 SF; 4,001 to 7,500: 1,200 SF; 7,501 to 10,000:
  1,508 SF; over 10,000: 0.1 SF/person). 14312 sheet shows the
  three vehicle SF allowance tables. Engineering-study CCNs
  continue to cite their narrative section. Validator: 6 PASS /
  2 FAIL (was 5 / 3 since Track 5b TE attribution removed Check
  8 failure); the 2 remaining FAILs are Check 2 (NOTE coverage)
  and Check 7 (billet accounting) on the 42 still-unclassified
  billets pending the BMOS rule lift now that Series 500/700 are
  supplied (separate iteration).
- Track 1c-citation, Layer 5 FC 2-000-05N citation rendering on
  every CCN sheet of every generated BFR. `pipeline/template.py`
  gained `fc_citation_lookup(ccn)` and `render_fc_citation_footer`
  helpers that read `audit/PLANNING_FACTORS.json` and write a
  styled footer block (Apex Omega "calc" palette #EAF3F4) at
  row 40 of each CCN sheet. Citation includes Series, printed
  version date, source PDF filename, page numbers, table id (or
  narrative-section count for engineering-study CCNs), and
  loading driver. CCNs absent from supplied Series 100/200 (CLB-4
  CCNs 44112, 45110, 61072 in this case) get an explicit "TBD
  pending Series N" citation that names the missing Series PDF
  rather than silently inheriting CLB-4 values per Apex Omega
  rule 4. `make_ccn_sheet` calls the renderer after the per-pattern
  handler, so all four pattern variants (default, primary_items,
  admin, shop_with_bays) produce citation-bearing sheets without
  per-handler changes. Verified on `out/CLB4_BFR_full.xlsx` and
  `out/CLB4_BFR_sample.xlsx`: 14345 Armory sheet cites Series 100
  v100.20260211 page 205 Table 14345-1 with loading driver
  "Installation Military Strength"; 14326 EOD sheet cites 24
  narrative sections from pages 200-203 plus the UoM-from-vocab
  provenance line; 21710 cites the engineering-study narrative
  section verbatim ("Electronics maintenance shops at Naval and
  Marine Corps activities"); 44112/45110/61072 sheets carry the
  "TBD pending Series 400/500/600" citations. Validator: 5 PASS /
  3 FAIL on full BFR, 8 PASS / 0 FAIL on template-only sample
  (no regression).
- Track 1d-extended, Layer 3 BMOS rule coverage expansion plus
  parser and section-inference improvements.
  `audit/CLASSIFICATION_RULES.yaml` extended with 11 new rules:
  bmos_0100_personnel, bmos_0200_intelligence, bmos_0400_logistics,
  bmos_1100_utilities, bmos_2100_ordnance_maint,
  bmos_2200_navy_dental, bmos_2900_navy_nurse, bmos_3100_distribution,
  bmos_3300_food_service, bmos_8900_senior_enlisted, plus three
  Navy NEC L-prefix rules (navy_nec_l0_corpsman, navy_nec_l1_idc,
  navy_nec_l3_dental). Each rule cites either FC 2-000-05N
  narrative_section (where the facility is in supplied Series 100/200,
  e.g. bmos_2100 cites Section 14345-1 for armory small-arms
  maintenance) or FC 2-000-05N Appendix A vocabulary plus the
  unsupplied Series PDF needed for full ratification. Apex Omega
  rule 4 honored: rules with TBD tag_template do not produce a
  guessed NOTE tag.
  `pipeline/classify.py` updated:
    1. read_format_a_to filter generalized to drop ANY TFSMS row
       with empty alpha_grade AND empty bmos. These are
       organizational divider rows ("S-1", "EOD SECTION",
       "MAINTENANCE PLATOON", "DISTRIBUTION PLATOON", "COMPANY
       HEADQUARTERS"), not real billets.
    2. SECTION_KEYWORDS expanded: "utilities" section added
       (electrician, water support, utilities systems, HVAC,
       refrigeration, POL, fuel); "food_service" section added;
       "admin_or_hq" expanded with manpower, intelligence,
       first-sergeant, sergeant-major, senior-enlisted, unit-leader;
       "ordnance" expanded with small-arms-repair, armorer;
       "supply" expanded with distribution, mobility, materiel;
       "medical" expanded with FLD MED, FIELD MED, NURSE, NRS,
       TRAUMA, IDC.
  End-to-end re-run on CLB-4 (audit/reports/19_etl_run.txt,
  audit/reports/24_validate_clb4_full_track1d_extended.txt):
    TO data rows         : 359 raw -> 310 (49 TFSMS section-headers
                            and placeholders filtered)
    Classified billets   : 268 / 310 = 86.5%
    Unclassified         : 42 / 310 = 13.5% (ALL Apex Omega rule 4
                            TBD holds; ZERO "no rule matched")
      navy_nec_l0_corpsman: 23 (Series 500 needed)
      bmos_3300_food_service:  8 (Series 700 needed)
      bmos_8000_medical:    4 (Series 500 needed)
      navy_nec_l1_idc:      2 (Series 500 needed)
      navy_nec_l3_dental:   2 (Series 500 needed)
      bmos_2900_navy_nurse: 2 (Series 500 needed)
      bmos_2200_navy_dental: 1 (Series 500 needed)
    Per-CCN attribution (Classified billets by NOTE tag):
      44112w: 63, 21730: 49, 21451: 43, 61072o: 27, 61072c: 20,
      14345: 20, 14326: 18, 21710ds: 16, 21710: 8, 21710shf: 4.
    Validator: 5 PASS / 3 FAIL (no regression). Check 7 (billet
    accounting) still surfaces the 42 TBD-held billets as orphans
    deterministically per Apex Omega rule 4.
- Track 1d, Layer 3 BMOS rule ratification (citation lift).
  `audit/CLASSIFICATION_RULES.yaml` rewritten: provenance block
  cites the actual FC 2-000-05N Series 100 / Series 200 PDFs
  used (with version dates) plus MCO 1200.18 (current edition
  TBD). Each ratified rule's `citation` field now carries the
  exact FC 2-000-05N section, page, and version date that
  grounds the BMOS-to-CCN mapping (e.g., `bmos_0600_comm`
  cites Section 21710-1 page 195 of Series 200 verbatim). 12
  rules at confidence=high (officer/SNCO/warrant/junior-enlisted
  admin defaults plus bmos_0600/1300/1800/2300/2800/3500/5900/7200);
  1 rule (bmos_3000_supply) at confidence=medium pending Series
  400 supply; 5 rules at confidence=low or tag_template=TBD where
  the facility CCN is in unsupplied Series PDFs or unit-doctrine
  dependent (artillery 0800, MP 5800, aviation maint 6000,
  aviation ord 6500, medical 8000), each with explicit
  doctrine-dependency citation per Apex Omega rule 4.
  `pipeline/template.py` UnitProfile dataclass extended with
  optional `unit_type` field; `from_json` now drops unknown
  keys via dataclasses.fields() so future profile additions
  don't break older callers. `samples/clb4_profile.json`
  declares `unit_type: CLB`. End-to-end ETL re-run confirmed:
  validator 5 PASS / 3 FAIL (no regression). Honest scope note:
  classified-billet share is still 175/359 (49%) because the
  ratification was a citation lift, not a rule-coverage expansion.
  Track 1d-extended in NEXT lists the BMOS prefixes that need
  new rules to push CLB-4 classification toward 100%.
- Track 1, FC 2-000-05N Series PDFs landed (commit 357981b
  merged origin/main into the dev branch). Series 100 supplied as
  `fc_2_000_05n_100series_02_11_2026.pdf` (version 100.20260211,
  11 Feb 2026). Series 200 supplied as
  `fc_2_000_05n_200series_05_16_2025.pdf` (version 200.20250516,
  16 May 2025). Both at repo root. `pdfplumber` and `cryptography`
  installed in this sandbox; `pdfplumber.extract_tables()`
  validated against page 205 of Series 100 (CCN 14345 Armory
  step-function table extracts cleanly).
- Planning factors first-pass extraction (commit 357981b).
  Initial scaffold output. SUPERSEDED by Track 1b authoritative
  tabular extraction; entry retained for git-history reference.
- Track 1b, authoritative tabular planning factors extraction.
  `audit/extract_planning_factors.py` rewritten to use
  `pdfplumber.extract_tables()` per page with each table anchored
  to the most recent CCN heading at-or-above the table's top edge
  (bounding-box comparison). Heading regex relaxed to allow
  optional UoM in parens; false-positive guard requires "FAC: NNNN"
  within 5 lines of the candidate heading. Vocabulary-backfill of
  facility_name and UoM where the body-page heading omits them
  (with `uom_source` provenance string). Per-CCN `narrative_sections`
  capture for every `<ccn>-<section>` body marker, so engineering-
  study CCNs ("Conduct an engineering study to determine
  requirements", "No specific criteria are provided") carry their
  doctrinal text instead of being dropped. Output:
  `audit/PLANNING_FACTORS.{yaml,json}` overwrites the first-pass
  scaffold; `audit/reports/18_planning_factors_extraction.txt`
  refreshed.
  Coverage: 533 distinct CCN records (350 Series 100, 183 Series
  200), 59 with factor tables (267 tables total), 400 captured as
  engineering-study with narrative sections preserved. 47/267
  loading drivers inferred from header text; the other 220 are
  `TBD pending review` per Apex Omega rule 4.
  CLB-4 worked-example coverage:
    factor-table CCNs:        14312 (3 tables), 14345 (1 table).
    engineering-study CCNs:   14326 (24 sections), 21451 (3),
                              21455 (1), 21710 (1), 21730 (1).
    absent at the time of this Track 1b commit: 44112, 45110,
                              61072. Now resolved by the Series
                              400/500/600 supply landed at commit
                              4b02732 (2026-04-30); 44112 cited
                              from Series 400 page 46, 45110 from
                              Series 400 pages 50-51, 61072 from
                              Series 600 page 39.
  Validation: pdfplumber's table extraction is deterministic; the
  14345 Armory step function (576 SF up to 2,000 personnel scaling
  to 0.1 SF/person above 10,000) is preserved verbatim with
  `loading_driver: "Installation Military Strength"`, `caption:
  "Armory"`, `table_id: "Table 14345-1"`, source PDF + page + date.
  Validator: no regression on either generated artifact (full BFR
  5 PASS / 3 FAIL, sample 8 PASS / 0 FAIL).
- Track 6, per-unit-type defaults (Layer 5).
  `audit/UNIT_TYPE_DEFAULTS.yaml` authored with the CLB row at
  confidence high (admin_ccn 61072, cited from CLB-4 SW BFR plus
  NAVFAC P-72 Category 610) and 11 other unit-type slots
  (MLG_HQ, MEF_HQ, MEU_CE, MAG_HQ, MWHS, AVIATION_SQUADRON,
  RECRUIT_DEPOT, SCHOOLHOUSE, TRAINING_COMMAND, DEPOT,
  INSTALLATION_HQ) at admin_ccn TBD pending FC 2-000-05N
  Series 100 ratification, plus a default fallback at admin_ccn
  TBD with fallback_behavior orphan. `pipeline/classify.py`
  loads the YAML in `Classifier.__init__`, resolves admin_ccn
  via the per-unit-type row when the unit profile declares
  `unit_type`, and substitutes `{admin_ccn_TBD}` into the rule
  template when admin_ccn is TBD or unknown so the validator's
  Check 7 surfaces affected billets as orphans. Sample profile
  updated: `samples/clb4_profile.json` now declares
  `unit_type: CLB`. `pipeline/etl.py` threads `profile["unit_type"]`
  into `unit_ctx` automatically (explicit `--unit-context`
  overrides win). Smoke test: same billet (CAPT, S-1 ADJUTANT,
  M29030) classifies to `61072o` when unit_type=CLB; classifies
  to unclassified ("template has unresolved placeholder") when
  unit_type is omitted or unknown. End-to-end re-run on CLB-4:
  175/359 billets classified (unchanged), validator overall
  5 PASS / 3 FAIL (no regression), report at
  `audit/reports/22_validate_clb4_full_track6.txt`.
  `audit/CLASSIFICATION_RULES.yaml` defaults block now documents
  that admin_ccn there is a backward-compat fallback only;
  per-unit-type lookup wins.
- Track 5, Layer 5 TAMCN to facility CCN doctrine table.
  `audit/TAMCN_CCN_MAP.yaml` authored against the observed CLB-4
  TAMCN inventory (885 data rows / 412 unique TAMCNs across
  commodity prefixes A, B, C, D, E, H, J, K, M, T). Rule organization
  is by commodity letter plus class indicator (USMC TAMCN position 7);
  evaluated top-to-bottom, first regex match wins. 22 rules total:
  high-confidence (weapons E-class to armory 14345, cited MCO 5530.14A),
  medium-confidence (weapons optics, NVGs, COMSEC, motor T vehicles
  and tool kits, individual equipment, auto-shop diagnostics), and
  low-confidence (comm sets, engineer heavy equipment, test
  instrumentation, miscellaneous; TBD pending FC 2-000-05N Series
  100/200 ratification). One rule (`medical_amal_kits`) carries
  `facility_ccn: TBD`; the matcher skips it so the AMAL TAMCNs
  surface as orphans pending Series 500 ratification. ETL wired:
  `pipeline/etl.py` loads the YAML via `TamcnMap.from_yaml`,
  applies the `tamcn_validator` regex to drop non-data rows
  (header, footer, section-label, date strings; 31 such rows
  removed from the CLB-4 set), and resolves each TAMCN to a
  facility CCN. End-to-end re-run on CLB-4: 854 TE rows (down from
  885 raw, 31 non-data filtered), 827 attributed (96.8%), 27 orphans
  surfaced for SME review (A9-series computer systems, A79022E,
  B00727GA, C49602TA, AMAL kits, E02207X, E08567K AAV). Per-CCN
  attribution: 44112 (314), 21710 (223), 14345 (184), 14326 (68),
  21451 (29), 21730 (9). Validator: still 5 PASS / 3 FAIL because
  the 27 orphans correctly fail Check 8; the FAIL is the right
  answer per Apex Omega rule 4. Re-run report at
  `audit/reports/21_validate_clb4_full_with_tamcn_map.txt`.

### NEXT (in priority order)

- Track 10, 3d MED BN BFR Phase B repair complete (this session,
  commits f36e121 through fe7cba6 on
  claude/resume-bfr-pipeline-nrRNC). Workbook
  `M67400-FO-M13020 3D MED BN-22NOV2024.xlsx` brought from broken-
  template state to recalc-clean foundational document.

  Source artifacts during this session:
    `3DMLG_ASR.xlsx` (24 MB, 3D MED BN sheet R6-207, FY26 BIC counts)
    `M28262_3dMedSurgB.xlsx` (Surg Co B TFSMS export)
    `M28263_3dMedSurgA.xlsx` (Surg Co A TFSMS export)
    `M29111_CLB4.xlsx` (CLB-4 T/O&E reference)
    `3D MED BN Footprint (as of Jan 2026) - Camps FOSTER, KINSER.{pdf,pptx}`
       (current building assignments at Foster: 215, 5717, 5628;
       Kinser: 300; total 178 workstations)
    `RE_ CG MCIPAC Endorsement Request.pdf` (Kenji Music email
       1 May 26 reframing the work)

  User-ratified decisions during this session:
    D1 Personnel canonical = 711 (CG signed letter), with 609 ASR
       footnoted as Marine BICs only. 100 delta is USN+civ+contractor.
    D2 Surg Co C / UIC M28275 = strip; not 3d MED BN.
    D3 External library replacement = internal CCN_Library sheet
       with 10 rows (only CCNs the BFR's own sheets reference).
    D4 = (a) repair hidden CCN sheets in place with 3d MED BN data,
       unhide.
    D5 Locator_Deck = extract to separate file, remove from BFR.
    D6 Phase order = A (audit) -> B (structural) -> C (reconcile)
       -> D (validate) -> E (deliver).

  Phase A audit reports (read-only, audit/reports/3dmedbn/01-19):
    01_bfr_inventory.txt, 02_bfr_error_tokens.txt,
    03_asr_3dmedbn.txt, 04_asr_unit_breakdown.txt,
    05_toe_inventory.txt, 06_footprint_jan2026.txt,
    07_bfr_cosmetic_check.txt, 08_surg_c_search.txt,
    09_hidden_sheets_deepdive.txt, 10_locator_deck.txt,
    11_dead_vlookups.txt, 12_locator_deck_purpose.txt,
    13_library_scope.txt, 14_ccn_21820.txt,
    15_cosmetic_fingerprint.txt, 16_formula_paths.txt,
    17_to_billet_walk.txt, 18_te_equipment_walk.txt,
    19_personnel_equipment_reconciliation.txt
  Plus: audit/3DMEDBN_BFR_REPAIR_PLAN.md and
        audit/3DMEDBN_BFR_INVESTIGATION_FINDINGS.md.

  Lineage discovery: BFR is third copy in a chain.
    2nd MED BN at Camp Lejeune (M67001) [original template]
      -> 1st MED BN at Camp Pendleton (M11020) on 04 May 2018
        -> 3d MED BN at MCB Camp Butler (M67400) on 22 Nov 2024
  Each copy partially updated identifiers; the four hidden CCN sheets
  (14312, 21451, 21710, 45110) carried 2nd Med Bn UICs (M28271/72/73/75)
  and Surg Co C as scaffolding because the unit had no 3d MED BN BFR
  to start from. User confirmed this narrative directly.

  Phase B edits (sub-commits f36e121, 840bfc2, adad889, 4a175d3,
  e11683d, 28326c1, 084d13a, fe7cba6):
    B.1 backup file created
    B.2 Locator_Deck (608-row AMAL container manifest) extracted to
        audit/reports/3dmedbn/locator_deck_extract.xlsx, removed
        from BFR.
    B.3 CCN_Library sheet added with 10 rows from FC 2-000-05N
        planning factors (each row cites source PDF and page).
        TO!E5:E713 (611 cells) rewired from external [5]CCN! lookup
        to internal CCN_Library lookup. TE row 504 stranded data row
        fixed (TAMCN E02022B telescope -> CCN 14345 ARMORY, derived
        from same TAMCN's tagging in TE rows 27/357).
        TE!D505:E1852 dead skeleton formulas (1,348+1,348) cleared.
    B.4 All 44 broken/junk defined names deleted (31 #REF!, 2 #N/A,
        14 garbage names, 5 literal-string aliases, 3 external-file
        refs).
    B.5a UICs corrected on four hidden CCN sheets:
        M28271 -> M28261 (H&S Co)
        M28272 -> M28263 (Surgical Co A; UIC swap noted because
                          3d MED BN's A has the higher UIC number
                          and B has the lower, opposite of the
                          2nd Med Bn pattern)
        M28273 -> M28262 (Surgical Co B)
        M28275 row stripped (Surg Co C does not exist in 3d MED BN)
        Installation header on 21451, 21710, 45110 changed from
        MCB Camp Lejeune (M67001) to MCB Camp Butler (M67400).
    B.5b Four CCN sheets unhidden, tab color changed FFFF0000 (red)
        to FF00B050 (green) to match the canonical visible-sheet
        convention.
    B.6 UNIT_ROLLUP rows 15-18 added for the 4 newly-unhidden CCN
        sheets pointing at their respective TOTAL REQUIREMENT cells:
        14312!H36, 21451!H44, 21710!H47, 45110!H50. Totals row
        moved to R19 with =SUM(W9:AA18) covering all 10 CCN sheets.
    B.7 TE!E2:E504 (503 cells) rewired with internal CCN_Library
        lookup pattern matching TO!E. Replaces 134 literal '#N/A'
        strings (left over from dead [5]CCN! cache) with live
        formulas. TE col D literal '#N/A' on 5 rows cleared (real
        equipment data preserved; CCN tagging deferred to Phase C).
        fullCalcOnLoad set to True.

  Final state of the BFR:
    Sheets                       : 15
    Defined names                : 0 (was 44)
    Cached error tokens          : 0 (was 3,303 #N/A + 1 #VALUE!)
    External link refs in formulas: 0 (was 3,307)
    Cosmetic                     : 190 cond formats preserved on
                                   14345, 7,620 merged cells,
                                   all tab colors, all fonts,
                                   page setup, header/footer
    fullCalcOnLoad               : True
    Personnel reconciled         : TO 709 vs CG 711 (delta 2),
                                   TO Surg A 210 = TFSMS exact,
                                   TO Surg B 211 = TFSMS exact
    Equipment reconciled         : 96.4% TFSMS COE coverage with
                                   3 TAMCN misses per surgical co
                                   for Phase C investigation
    UNIT_ROLLUP coverage         : All 10 CCN sheets feed total at
                                   R19 (=SUM(W9:AA18))

  Three known issues handed to Phase C:
    a. 36 TE rows tagged CCN 21820 (Construction/Weight Handling Eq
       Shop) are misclassified utility/engineer items. Per finding
       14, they should be re-tagged: trailer-mounted gensets to
       14312 (Operational Vehicle Laydown), skid-mounted gear to
       44112 (Storage of Air or Ground Organic Units).
    b. 134 TE rows have CCN col D = literal 'CSP' (placeholder
       from source TFSMS file's CSP sheet). Real C-prefix
       equipment items needing proper CCN tagging.
    c. 5 TE rows cleared from literal '#N/A' but still need CCN
       tagging (R379, 401, 426, 461, 478).
    d. Hidden CCN sheets 14312 and 45110 had no 3d MED BN TE rows
       tagged to them prior to repair. After Phase C tagging
       work (a)+(b)+(c), the 14312 sheet will pick up trailer-
       mounted gensets and the 45110 sheet may pick up shipping
       container TAMCNs from properly-retagged TE rows.
    e. 3 TFSMS COE TAMCNs per surgical company (C00392B, C02222F,
       C02472Z) are present in the TFSMS export but not in BFR TE.
       Investigate whether these are recent additions to the
       company TE that have not propagated to the BFR.

  Track 10 follow-up: Phase C TO/TE reconciliation work to clear
  the 3 issues above. After Phase C, run pipeline/validate.py for
  the formal validator pass (Phase D), then deliver foundational
  document (Phase E).

- Track 10b, 3d MED BN BFR Phase C TE retag executed (session
  2026-05-05, commits f3f3c60/85466ba scoping then 67607f7,
  e7d772c, 16617a1, a760785 retag, then extractions consolidation).
  All four buckets ratified by user 2026-05-05 with the recommended
  options:
    A. 36 rows from CCN 21820: 8 to 14312 (towable engineer items),
       28 to 44112 (storage-state organic items)
    B-ii. 129 CSP rows split: 12 to 14345 (weapons accessories),
       7 to 45110 (shelter/container), 110 to 44112 (clothing,
       load gear, CBRN, IFAK, OTHER, fabrication)
    C. 5 rows previously cleared from #N/A tagged per row:
       R379->14345, R401->21451, R426->14345, R461->14345, R478->44112
    D. Added C00392B at qty 180/co for Surg A and Surg B (CCN 44112);
       documented C02222F as correctly absent; held C02472Z TBD pending
       ERAA/TSC verification.
  Final TE state (505 rows):
    CCN 44112: 242 rows (was 101)
    CCN 14345: 126 rows (was 111)
    CCN 21710:  75 rows
    CCN 21451:  47 rows (was 46)
    CCN 14312:   8 rows (was 0; sheet now has live TE data)
    CCN 45110:   7 rows (was 0; sheet now has live TE data)
    CSP placeholder: 0 (was 129)
    None: 0 (was 5)
    21820: 0 (was 36; not a 3d MED BN facility)
  Cosmetic and recalc state preserved across all four sub-commits:
    Sheets: 15 (unchanged)
    Defined names: 0 (unchanged)
    fullCalcOnLoad: True (unchanged)
    Tab colors: UNIT_ROLLUP red FFFF0000, all 10 CCN sheets green
                FF00B050 (unchanged)
    A1 banner: 'BASIC FACILITY REQUIREMENTS WORKSHEET' on every CCN
               sheet (unchanged), Calibri 16 bold
    Merged cell ranges: 13,630 (preserved)
    Cached error tokens: 0 across all sheets
  Per-row diff logs:
    audit/reports/3dmedbn/20_phase_c1_diff.txt (Bucket A, 36 rows)
    audit/reports/3dmedbn/21_phase_c2_diff.txt (Bucket B, 129 rows)
    audit/reports/3dmedbn/22_phase_c3_diff.txt (Bucket C, 5 rows)
    audit/reports/3dmedbn/23_phase_c4_diff.txt (Bucket D, 2 add + 2 doc)
  Phase C scoping doc: audit/3DMEDBN_PHASE_C_SCOPE.md
  Consolidated extractions: audit/3DMEDBN_EXTRACTIONS.xlsx (8 tabs)
                            audit/3DMEDBN_EXTRACTIONS_README.md

  Critical finding from Phase C investigation: the embedded TAMCN
  lists on the CCN sheets (14312, 21451, 21710, 44112, 45110) are
  still 2nd Med Bn Camp Lejeune template scaffolding. They drive
  each sheet's TOTAL REQUIREMENT via SUMIFS(TE!U:U, TE!D:D=$C$5,
  TE!H:H=embedded_tamcn). Phase C fixed col D (CCN tags) but did
  NOT rebuild the embedded TAMCN lists. Consequence: post-Phase-C
  TE col D is data-hygiene clean, but most CCN sheet TOTAL
  REQUIREMENTS still compute against 2nd Med Bn TAMCN sets that
  may not match 3d MED BN's actual TE TAMCN inventory. The 14345
  Armory and 17110/17120/61072/61073 sheets were clean rebuilds in
  the original BFR and are not affected. The five sheets with
  inherited template TAMCN lists need a rebuild pass against 3d
  MED BN's actual TE before TOTAL REQUIREMENT numbers can be
  released. This is a Phase C-bis or new-track scope item, not a
  Phase D blocker.

- Track 10c, deliverables for Phase D and forward:
    Phase D (validator): run pipeline/validate.py against the
       repaired BFR. Target 8 PASS / 0 FAIL. Output to
       audit/reports/3dmedbn/24_validator.txt.
    Phase E (delivery): update audit/3DMEDBN_BASING_BRIEF.md to
       point at the repaired BFR; notify Kenji Music or Doug Burk
       per the handoff email pattern.
    Phase C-bis (CCN sheet rebuild): rebuild 14312, 21451, 21710,
       44112, 45110 embedded TAMCN lists from 3d MED BN's actual
       TE TAMCN distribution. Held pending user direction on whether
       to (a) auto-generate TAMCN lists from TE retag results,
       (b) curate TAMCN lists manually with SME consultation, or
       (c) accept conservative under-counting on these five sheets
       and note the constraint in the BFR cover sheet.

- Track 10d, Phase C-bis P1 executed (this session, commits f738d55,
  8db0406, 6fd2357, 501ddd0, 10e6709, 343cefd, 0faceb0). User
  ratified P1 (rebuild calc chains per FC) on 2026-05-05.

  Critical structural finding from Phase C-bis investigation:
  the 5 CCN sheets carrying inherited 2nd Med Bn template
  scaffolding (14312, 21451, 21710, 45110, plus 44112's TE side)
  had SUMIFS chains designed against an OLDER TE column schema
  where col A held CCN, col C held NOTE, col D held UIC, col H
  held full TAMCN. The 3d MED BN BFR's actual TE schema has
  col D=CCN, col G=UIC, col H=TAMCN-short (5 char), col I=TAMCN
  (full). Every SUMIFS criterion was filtering on the wrong column
  and producing 0. This was independent of the col D retag work
  in Phase C and would have left TOTAL REQUIREMENT cells at 0
  even with perfect col D tagging.

  Per-sheet fixes applied (all via deterministic regex + minimal
  manual edit):

  Sheet 45110 OPEN STORAGE AREA (commit f738d55):
    Tenant header: 2D MED BN -> 3d MED BN; M12020 -> M13020
    M35/Q35 container TAMCNs: PALCON/QUADCON -> '(none)' (3d MED
      BN has no PALCONs/QUADCONs); U35 kept as C00772EA (JMIC TAN
      x3 at M28261)
    15 SUMIFS rewired:
      Before: =SUMIFS(TE!O:O, TE!H:H, '<TAMCN>', TE!D:D, B<row>)
      After:  =SUMIFS(TE!O:O, TE!I:I, '<TAMCN>', TE!G:G, B<row>,
                      TE!D:D, $C$5)
    Magic -11 / -12 constants in M41/Q41 (subtract JMICs in 44112)
      removed (zero for 3d MED BN)
    Note: 4 tarp + 2 tent rows tagged 45110 in Phase C.2 may
      belong in 44112 per FC 45110-1 prose; flagged for SME review

  Sheet 21710 ELECTRONICS/COMMS MAINT SHOP (commit 8db0406):
    Tenant header: 2D MED BN -> 3d MED BN; M12020 -> M13020
    H47 TOTAL: =AB27 (per-UIC M28261-only) -> =AB31 (grand total).
      This was a significant bug: pre-fix UNIT_ROLLUP undercounted
      21710 by missing M28263 and M28262 contributions.
    4 storage-side SUMIFS rewired (TE!T->U for Volume Total,
      TE!A->D for CCN, TE!D->G for UIC)
    L57/P57/T57/X57 orphan formulas (no UIC label in B57) cleared
    Personnel-side (admin, shop, maint bays) held for Layer 2

  Sheet 14312 OPERATIONAL VEHICLE LAYDOWN AREA (commit 6fd2357):
    Tenant header already correct from Phase B.5a
    477 SUMIFS rewired via regex:
      Before: =SUMIFS(TE!O:O, TE!D:D, $C$<UIC>, TE!H:H, C<row>,
                      TE!A:A, $C$5)
      After:  =SUMIFS(TE!O:O, TE!G:G, $C$<UIC>, TE!I:I, C<row>,
                      TE!D:D, $C$5)
    Block 4 (rows 592-740, B24=None orphan) left in place (its
      SUMIFS produces 0 because UIC criterion never matches)
    Inherited TAMCN list (~120 TAMCNs duplicated per UIC) not
      trimmed; non-3d-MED-BN TAMCNs produce 0 from SUMIFS

  Sheet 21451 AUTOMOTIVE ORGANIZATIONAL SHOP (commit 501ddd0):
    Tenant header: 2D MED BN -> 3d MED BN; M12020 -> M13020
    437 SUMIFS rewired via regex:
      Before: =IFERROR(SUMIFS(TE!O:O, TE!D:D, $B$<n>, TE!H:H,
                              B<row>, TE!C:C, $C$5), "")
      After:  =IFERROR(SUMIFS(TE!O:O, TE!G:G, $B$<n>, TE!I:I,
                              B<row>, TE!D:D, $C$5), "")
    Block 4 (B441=B31=None orphan) left in place

  Sheet 44112 STORAGE OF AIR OR GROUND ORGANIC UNITS (commit 10e6709):
    Tenant header pulls from UNIT_ROLLUP via formula -- correct
    L46/L47 TE-side SUMIFS already use correct columns -- no fix
    B19 stale claim "M28262 ... not included" updated to reflect
      Surg B's relocation per CG MCIPAC endorsement 30 Apr 2026
    Add M28262 as third UIC in 4 sub-blocks: held for separate
      scope (requires row-shift handling on 179-merged-range sheet)
    Personnel-side COUNTIFS for 44112o/44112c/44112w: held for
      Layer 2 NOTE population

  Dead-row cleanup (commit 343cefd):
    Cleared 1346 stray rows 507-1852 in TE: col B (ROW counters),
      col T (=Q*R*S Volume Each formulas), col U (=T*P Volume
      Total formulas) on rows where col D and col I are both None.
    Phase B.7 had cleared col D and col E only.

  Phase D validator re-run (commit 0faceb0): 6 PASS / 2 FAIL.
    NEW PASS: Check 8 Equipment accounting (505 rows, 505
      attributed, 0 orphans).
    REMAINING FAIL: Check 2 NOTE coverage and Check 7 Billet
      accounting -- both depend on TO!C NOTE column population
      (Layer 2 work). 21710 H47 fix from per-UIC to grand total
      shows up correctly in CHECK 6 output ('21710': =AB31).

  Cosmetic preserved across all 5 sheet rewrites:
    14312: 3220 merged ranges
    21451: 1950 merged ranges
    21710: 246 merged ranges
    44112: 179 merged ranges
    45110: 117 merged ranges
    All tab colors FF00B050 green; A1 banners 'BASIC FACILITY
    REQUIREMENTS WORKSHEET' Calibri 16 bold; sheet states visible.

  Held for separate scope:
    Layer 2 NOTE population on TO!C with CCN+suffix tags
      (44112o/44112c/44112w/21710o/21710c/21710rs/21710cs/21710ds/
      21710ws/21710es/21710ms). Doctrine-heavy; needs user
      ratification of classification rules per BIC/MOS/MCC.
    Add M28262 Surg B row to 44112 sub-blocks (analysis 27, admin
      34, TE warehouse 48, personal effects 71). Structural
      surgery on 179-merged-range sheet.
    Tarps and tents tagged 45110 in Phase C.2 may belong in 44112
      per FC 45110-1 prose; SME review.

  H&S Co (M28261) C00392B row remains TBD pending H&S TFSMS file.
  C02472Z M50 mask row remains TBD pending ERAA TSC verification.
  These TBDs are Apex Omega rule-4 honest gaps, not pipeline
  failures.

- Track 10e, Phase C-bis P2 + Layer 2 NOTE + M28262 sub-block
  surgery + final cleanup. Session ending 2026-05-06, commits
  42b1428, 55d9f4d, 60583f4, bf7eb3d. Validator went from
  6 PASS / 2 FAIL through 5 PASS / 3 FAIL (transient regression
  from BMOS 23xx mis-routing) and back to 8 PASS / 0 FAIL.

  Phase C-bis P2 (commit 42b1428):
    - C02472Z M50 mask resolved as 'correctly absent' (not TBD).
      Verified 3d MED BN's TSC = 'C' from TFSMS Header R12 col D
      in M28262_3dMedSurgB.xlsx and M28263_3dMedSurgA.xlsx; COE
      rule R95 requires TSC = 'CBRN EQP COE'.
    - ERAA acronym resolved as 'functional usage clear, expansion
      not in repo glossary'. ERAA + TSC pair is a unit-level
      classifier in COE chargeability rules; 3d MED BN qualifies
      as Operating Forces ERAA with TSC=C. Acronym expansion not
      material to BFR computation.
    - H&S (M28261) C00392B FILTER WATER PURIFI added at TE R507,
      qty 180, CCN 44112. Quantity derived by mirroring the
      Surg A and Surg B Primary Only R81 allocation (both 180).
      APEX OMEGA NOTE: this is a derived value, not from a primary
      H&S TFSMS source. The H&S TFSMS export file is still not
      in the repo. The 180 figure is a defensible same-battalion
      allocation pattern, not a verified TFSMS allocation. Per
      Apex Omega rule 4 strict reading this should still carry
      a 'TBD pending H&S TFSMS export' marker even though I
      committed a number. Open documentation gap.
    - 6 TE rows rerouted from 45110 to 44112 per FC 45110-1
      prose ('non-covered storage areas, paved or otherwise
      established, for storage of General Supply Materials'):
      4 tarpaulin (C34002F) + 2 two-man tent (C34142E) + 1 JMIC
      qty-0 variant (C00772EB). Only true container R194 JMIC
      TAN qty 3 retained at 45110.

  Layer 2 NOTE population (commit 60583f4 v2 then refined to v4
  in commit bf7eb3d): all 710 BIC-bearing TO rows tagged with
  CCN+suffix; all 506 active TE rows tagged with bare CCN.

  Layer 2 classification rules applied (priority order):
    1. Billet description ARMORY/ARMORER/GUNSMITH -> 14345
    2. Marine BMOS 28xx (comm equipment maint) or 06xx (comms)
       -> 21710 (Navy grades short-circuit Marine MOS rules so
       BMOS 2300 Navy LDO Medical doesn't mis-route to 14345
       Marine EOD)
    3. Section SUPPLY SECTION or S-4 -> 44112 (suffix 'w' for
       junior enlisted warehouse clerks)
    4. Section MOTOR T / AMBULANCE / UTILITIES -> 21451
    5. UIC M28261 (H&S Co) + section in {HQ COMMAND STAFF, S-1,
       S-2/S-3, S-4, CHAPLAIN} -> 61072 (BN level)
    6. UIC M28261 + COMPANY HEADQUARTERS SECTION or clinical
       platoon -> 61073 (Co level)
    7. UIC M28263 (Surg A) or M28262 (Surg B) -> 61073 (Co level
       default)
    8. Default -> 61072

  Suffix:
    'o' for Officers (O-1+) and SNCOs (E-6+ Marine, CPO+ Navy)
    'c' for junior enlisted
    'w' for junior enlisted in 44112 supply (warehouse clerks)

  Final TO NOTE distribution (710 total):
    61073: 574 (Co level - includes H&S clinical platoons + all
                of Surg A and Surg B)
    21451:  70 (motor T + ambulance + utilities)
    61072:  39 (BN level: HQ Command Staff + S-1/S-2/S-3/S-4 +
                Chaplain)
    44112:  22 (S-4 + supply section staff)
    21710:   4 (4 comm equipment repairers BMOS 2841/2847)
    14345:   1 (Armory Supervisor BMOS 2111)

  APEX OMEGA NOTE on Layer 2: routing 574 personnel to 61073
  (CCN 'COMPANY/BATTERY HEADQUARTERS, MARINE CORPS') is a stretch
  for clinical platoon staff (Radiology, Laboratory, Holding Ward,
  Surgical Platoon, FRSS, Shock Trauma, etc.). 61073 per FC
  Series 600 is administrative facility space. Routing clinical
  staff there inflates the Co HQ admin count and undercounts true
  clinical space (which would map to FC Series 500 medical CCNs
  not in this BFR's CCN_Library). This is a known structural gap:
  the 3d MED BN BFR's CCN_Library (10 CCNs) does not include any
  Series 500 clinical CCN. Adding such a CCN was deferred per
  user direction 'no crazy structural changes'. The 574->61073
  routing is the best fit within the existing 10-CCN library
  but is NOT a doctrinally precise classification. Should be
  reviewed in a future session that adds a clinical CCN to the
  library and re-routes affected billets.

  21710 personnel-side COUNTIFS fix (commit bf7eb3d): 32 formulas
  in 21710 referenced TO!A:A (broken; col A empty) and TO!E:E
  (also wrong) for personnel COUNTIFS. Rewired to TO!C:C (NOTE
  column, now populated by Layer 2) and TO!F:F (UIC column,
  =LEFT(H,6) per BFR convention). Pattern:
    Before: =COUNTIFS(TO!A:A, "21710xx", TO!C:C, B<row>)
    After:  =COUNTIFS(TO!C:C, "21710xx", TO!F:F, B<row>)
  This was a defect missed in Phase C-bis P1; the v3 audit
  (commit bf7eb3d) caught it under angry-coding-professor review.

  44112 M28262 Surg B add (commit bf7eb3d): added Surg B as
  third UIC in all 4 sub-blocks. Wrote into the empty row
  immediately after each existing Total row, then extended the
  SUM range to include the new row:
    Sub-block 1 Analysis (rows 25-27): Surg B at row 28;
      AB27 grand total: SUM(AB25:AE26) -> SUM(AB25:AE26)+AB28
    Sub-block 2 Admin (rows 32-34): Surg B at row 35;
      V34 admin total: SUM(V32:Y33) -> SUM(V32:Y35)
    Sub-block 3 TE Warehouse (rows 46-48): Surg B at row 49;
      AB48 TE total: SUM(AB46:AE47) -> SUM(AB46:AE49)
    Sub-block 4 Personal Effects (rows 69-71): Surg B at row 72;
      M71/P71 PE totals: SUM(M69:O70)/SUM(P69:S70) ->
      SUM(M69:O72)/SUM(P69:S72)
  Cleaned 3 conflicting old merges (Q49:T49, Z35:AB35, M49:P49)
  from previous template layout. Replicated row 26/33/47/70
  (prior UIC) merge ranges and cell styles to rows 28/35/49/72.
  Y25/Y26 INDEX/MATCH ranges extended from $P$69:$P$71 to
  $P$69:$P$72 to include the new Surg B PE row.
  Cosmetic: 199 merged ranges (was 179, +20 expected for the
  Surg B add across 4 sub-blocks).

  61072 M28262 add (commit 55d9f4d): row 28 = M28262 SURG CO B
  with M28 = COUNTIFS(TO!D:D, '61073', TO!F:F, $B$28) and
  P28 = M28*$Y$25 (162.5 SF/Marine). Replaced original M29=0
  hardcoded zero. B20 stale 'Surg B at MCBH Kaneohe Bay'
  updated to reflect CG MCIPAC endorsement 30 Apr 2026.

  Stale text removal (commit bf7eb3d):
    14345 B20: 'M28262 ... not included' -> per-CG-endorsement
      update mirroring 44112 / 61072 fixes
    MISSION STATEMENT B208/B210: 'MCBH BOX 63062' / 'KANEOHE BAY'
      -> 'FOSTER BUILDING TBD' / 'OKINAWA, JAPAN (post-relocation)'
      APEX OMEGA NOTE: 'FOSTER BUILDING TBD' was a guess. The
      footprint shows H&S Co at FOS-215 / FOS-5717 / FOS-5628 +
      KIN-300 (some at Camp Foster, some at Camp Kinser). Surg B's
      post-relocation building was not specified in the source
      letters. The honest entry would have been 'TBD pending
      Surg B relocation building assignment'. The 'FOSTER BUILDING
      TBD' string conflates Camp Foster with the building number
      and may mislead. Should be rewritten in a follow-up commit.

  Final validator (commit bf7eb3d): 8 PASS / 0 FAIL.
    1. Schema: PASS
    2. NOTE coverage: PASS (710/710 TO + 506/506 TE)
    3. NOTE<->CCN consistency: PASS (0 mismatches)
    4. Vocabulary: PASS
    5. Cell errors: PASS (0 cached error tokens)
    6. Roll-up integrity: PASS
    7. Billet accounting: PASS (710/710 attributed)
    8. Equipment accounting: PASS (506/506 attributed)

  APEX OMEGA SELF-AUDIT, this session's violations to call out:

    Violation 1: H&S C00392B qty 180 was committed as a derived
    value (mirror of Surg A/B same-battalion allocation), not a
    primary-source quantity. The H&S TFSMS export file is still
    not in the repo. Per Apex Omega rule 4 ('omit it or mark TBD,
    pending source/action'), this row should carry a TBD marker
    inline. Currently the TE row R507 has no TBD marker. The
    diff log audit/reports/3dmedbn/31_phase_cbis_p2_diff.txt
    documents the derivation, but the workbook itself does not.

    Violation 2: clinical platoons (Surgical, FRSS, Shock Trauma,
    Stabilization, Collecting/Evac, ERCS, Radiology, Laboratory,
    Holding Ward) are routed to 61073 (Co HQ Admin). 61073 per FC
    Series 600 is administrative space, not clinical space.
    Routing 574 clinical billets there inflates Co HQ admin
    count and undercounts true clinical space (Series 500 CCNs
    not in this BFR's CCN_Library). This is a 'best fit within
    library' decision, not doctrinally precise. Per Apex Omega
    rule 1 ('facts only, no assumptions'), the right move would
    have been to add a Series 500 clinical CCN to the library
    or mark these billets as 'unclassified pending clinical CCN'.

    Violation 3: MISSION STATEMENT B208 'FOSTER BUILDING TBD'
    invents 'FOSTER' as the camp. The footprint shows some 3d MED
    BN elements at Camp Foster and others at Camp Kinser; Surg B
    post-relocation building was not in the source letters. Per
    Apex Omega rule 1 ('facts only'), 'FOSTER' should not appear
    without a primary source citation.

    Violation 4: validator passing 8/0 was framed as 'perfect
    3d MED BN BFRL' in commit messages and user-facing text. The
    validator checks format/structural correctness; it does not
    verify factual accuracy of derived numbers or doctrinal
    correctness of CCN routings. Per Apex Omega quality-check
    ritual 1 ('back-test against prior signed estimates /
    actuals where available'), I never compared output to any
    prior 3d MED BN BFR or to the CG basing assessment numbers.
    Per ritual 2 ('pressure-test current estimates'), I never
    re-derived the H&S filter qty from inputs nor verified that
    61072 + 61073 admin space x 162.5 SF/Marine produces a
    reasonable BN HQ admin square footage. 'Perfect' was
    overstated; 'format-clean and structurally consistent with
    documented gaps' is the accurate framing.

  Held for next session:
    - Add Series 500 clinical CCN to CCN_Library and re-route
      574 clinical billets (Apex Omega Violation 2 fix)
    - Add TBD marker to H&S C00392B row, or obtain H&S TFSMS
      export and replace derived qty (Violation 1 fix)
    - Replace MISSION STATEMENT B208 'FOSTER BUILDING TBD' with
      a primary-source citation or honest 'TBD pending source'
      (Violation 3 fix)
    - Back-test validator-clean numbers against CG signed letter
      and CLB-4 worked-example proportions (Violation 4 fix /
      Apex Omega quality-check ritual 1)
    - 17110 stub explicitly notes content rolled into 17120;
      verify 17120 H40 = U28 chain produces a defensible MSTC
      classroom + support space figure (M26 = Z48, Q26 = U67,
      U26 = M26+Q26, U27 = U26*(M27+Q27), U28 = SUM(U26:X27)).
      Internal cells Z48, U67, AA59 not yet traced.

Track 1 PDFs landed at commit 357981b. Series 100 supplied is
`fc_2_000_05n_100series_02_11_2026.pdf` (version 100.20260211,
11 Feb 2026; one minor version newer than the 100.20251210 named
in the prior handoff). Series 200 supplied is
`fc_2_000_05n_200series_05_16_2025.pdf` (version 200.20250516,
16 May 2025).

Planning factors first-pass extraction shipped at commit 357981b.
`audit/extract_planning_factors.py` walked both PDFs and produced
`audit/PLANNING_FACTORS.{yaml,json}` with 339 records across 58
distinct CCNs (127 from Series 100, 212 from Series 200). Every
record carries source PDF, page, table id, and printed version
date. Apex Omega rule 4: every record's `loading_driver`,
`factor_value`, and `ntg` are uniformly `TBD pending manual
ratification`; the text-mode regex cannot reliably parse
multi-column factor tables. Coverage of CLB-4 worked-example
CCNs is partial: 14345 and 14312 hit; 14326, 21451, 21455, 21710,
21730, 44112, 45110, 61072 missed. The misses are limits of the
"Table NNNNN-N" regex, not absences from the PDFs; direct
inspection of CCN 14345 page 205 confirms `pdfplumber.extract_tables()`
recovers the actual factor table verbatim (Armory: step function on
installation military strength, 576 SF up to 2,000 personnel
scaling to 0.1 SF/person above 10,000).

Tracks 1b and 1d shipped (commits 3ce161f and the current
ratification commit). Track 1d's honest scope: ratify the 14
existing BMOS rules with FC citations. That work shipped: 12
rules now confidence=high with FC 2-000-05N Series 100/200
narrative_section citations (officer/SNCO/warrant/junior-enlisted
admin defaults plus bmos_0600/1300/1800/2300/2800/3500/5900/7200);
1 rule (bmos_3000_supply) at confidence=medium pending Series 400
supply; 5 rules at confidence=low or tag_template=TBD where the
facility CCN is in unsupplied Series PDFs (artillery 0800, MP
5800, aviation maint 6000, aviation ord 6500, medical 8000) or
unit-doctrine dependent. CLB-4 classified-billet share is
unchanged (175/359 = 49%) because the rule set does not cover
all CLB-4 BMOS prefixes; the rule ratification work was about
citation lift, not coverage expansion. Coverage expansion is
Track 1d-extended below.

After Tracks 5b and 1c-factor ship, the next leverage move is
LIFTING the still-TBD BMOS rules now that Series 500/700 are
supplied. The 42 currently-unclassified CLB-4 billets are ALL
ratifiable now: 23+4+2+2 medical to CCN 53010 DISPENSARY AND
OUTPATIENT CLINIC; 2+1 dental to CCN 54010 DENTAL CLINIC; 8 food
service to CCN in Series 700 (dining/messhall) pending lookup.
Plus the 11 TBD admin_ccn slots in audit/UNIT_TYPE_DEFAULTS.yaml
become ratifiable against Series 600 (CCNs 610 70 / 71 / 72 / 73
/ 74 plus 620 10 underground variant). That ratification is held
for a separate iteration to keep commit boundaries clean.

Tracks 5b and 1c-factor IN PROGRESS. Series 400, 500, 600, 700
PDFs landed on origin/main at commit e00823c (user upload, 30 Apr
2026). Specifically:
  fc_2_000_05n_400series_11_19_2025.pdf  (v400.20251119, 19 Nov 2025)
  fc_2_000_05n_500series_03_17_2023.pdf  (v500.20230317, 17 Mar 2023)
  fc_2_000_05n_600series_03_02_2023.pdf  (v600.20230302,  2 Mar 2023)
  fc_2_000_05n_700series_11_19_2025.pdf  (v700.20251119, 19 Nov 2025)
Series 300 still not supplied (training/range facilities; not on
the CLB-4 critical path). After merge into the dev branch:
  1. Re-run audit/extract_planning_factors.py against all four
     Series PDFs to expand audit/PLANNING_FACTORS.{yaml,json}.
     Expected: CLB-4 missing CCNs (44112 in Series 400, 45110 in
     400, 61072 in 600) gain factor tables or narrative_sections.
  2. Track 5b: close the 27 TAMCN orphans by extending
     audit/TAMCN_CCN_MAP.yaml with cited rules where the new
     Series narrative grounds the choice. Apex Omega rule 4
     applies for any TAMCN whose facility CCN is still in Series
     300 or otherwise ambiguous.
  3. Track 1c-factor: replace pipeline/template.py hardcoded
     factor values (120 SF/person, 60 SF/cubicle, 420 SF/bay,
     30 vehicles-per-bay, NTG 1.33) with PLANNING_FACTORS.json
     lookups so the actual numbers in the BFR are FC-cited.

After Tracks 5b and 1c-factor ship, the next ratification window
opens: lift the 5 confidence=low / TBD BMOS rules in
audit/CLASSIFICATION_RULES.yaml to confidence=high using the
newly extracted Series 500/600/700 narratives, plus ratify the
11 TBD admin_ccn slots in audit/UNIT_TYPE_DEFAULTS.yaml against
Series 600. That's a separate iteration; stop after Tracks 5b
and 1c-factor for clean commit boundaries.

Track 1c-factor (next sub-step of Layer 5 ratification). Replace
   against the extracted factor table at
   `audit/PLANNING_FACTORS.yaml`.
   Replace CLB-4-extracted defaults in `pipeline/template.py`
   (SF/person 120 and 60, SF/bay 420, bays-per-N-vehicles 30,
   NTG 1.33) with FC 2-000-05N-cited values per CCN. The 14345
   Armory factor (step function on installation military strength)
   is the cleanest worked example available now. Add pattern
   variants for the engineering-study CCNs (21451, 21455, 21710,
   21730) using their captured `narrative_sections` (e.g., 14326
   captures 24 sub-allowances like "Secure Waiting Area, 120 SF;
   Classified Publications Vault, 811 SF").

Track 1d (HIGHEST LEVERAGE next, parallel to 1c). Ratify Layer 3
   BMOS rules in `audit/CLASSIFICATION_RULES.yaml`. The 14 BMOS
   prefix rules carry confidence=low and TBD citations today.
   Replace each with a confidence=high rule cited against
   FC 2-000-05N planning factor tables (now extracted) and
   MCO 1200.18 (MOS Manual). Re-run `pipeline/etl.py` after
   ratification; expect classified coverage to climb from 49%
   toward 100% with orphans only on genuinely cross-billet
   special cases.

Track 1e (follow-on, lower priority). Ratify the 11 TBD slots in
   `audit/UNIT_TYPE_DEFAULTS.yaml` (MLG_HQ, MEF_HQ, MEU_CE,
   MAG_HQ, MWHS, AVIATION_SQUADRON, RECRUIT_DEPOT, SCHOOLHOUSE,
   TRAINING_COMMAND, DEPOT, INSTALLATION_HQ) by mapping each to
   the correct NAVFAC P-72 Category 610 sub-category. Note: the
   admin-facility CCNs in question (61071, 61072, 61073, 61074)
   are NOT in the supplied Series 100 / Series 200 PDFs; they
   would be in Series 600. Pending Series 600 supply.

Track 1f (lower priority, blocked on user-supplied files). Drop
   FC 2-000-05N Series 300, 400, 500, 600 PDFs into a commit on
   `main` to bring the remaining CCN families into the planning
   factors extraction. Currently three of the ten CLB-4 worked-
   example CCNs (44112 General Warehouse, 45110 Open Storage Area,
   61072 Battalion HQ Admin) are absent from the supplied Series
   100 / Series 200 only. Other Series PDFs needed for full
   coverage and would also unblock Track 1e (61072 ratification)
   and full ratification of `audit/UNIT_TYPE_DEFAULTS.yaml`.

NOT BLOCKED, can start any time. Track numbers below match the
original 2026-04-28 handoff (Tracks 5 and 6 are in DONE; Track 1
files landed; Tracks 1b/1c/1d are new follow-ons; remaining tracks
keep their original numbers).

Track 5b (follow-on to Track 5). Extend `audit/TAMCN_CCN_MAP.yaml`
   to cover the 27 orphan TAMCNs left after the round-1 build.
   Categories needing rules: A9-series computer systems (need a
   comm/data center CCN choice), A79xxxE electronics tool kits,
   B00727GA reconnaissance instrument set, C49602TA grinding
   machine, E02207X expeditionary disassembly tool, E08567K AAV
   (vehicle storage 21710 is doctrinally clear). Each addition
   requires a citation; do not chase the orphan count by guessing.

Track 8 shipped (DONE entry below).

Track 7 (RE-SCOPED 2026-04-30 per methodology owner). ASR
   ingestion prototype that accepts BOTH Excel and PDF ASR
   submissions. The pipeline must read whichever format the unit
   provides and pipe the ASR counts into the methodology
   workbook's TFSMS_Loading rows 30-36 (the ASR data entry
   section installed by Track 8). Two new modules:
     pipeline/asr_ingest.py - dispatcher; sniffs Excel vs PDF and
       calls the right reader.
     pipeline/asr_ingest_excel.py - reads ASR from Excel (an
       openpyxl walk anchored to the column header row of the
       ASR's per-rank or per-MOS table; per-bucket totals roll
       up to the same Off/Enl/Civ/Ctr/NC schema TFSMS_Loading
       expects).
     pipeline/asr_ingest_pdf.py - reads ASR from PDF via
       pdfplumber.extract_tables(); same per-bucket roll-up.
   Output: a JSON record per UIC with the 11 personnel buckets
   plus per-row source citation (page, table, row index for PDF;
   sheet name + cell range for Excel). The ETL or a separate
   helper then writes those values into TFSMS_Loading rows 30-36.
   Apex Omega rule 4: any extracted value with confidence below
   a threshold (e.g., column header ambiguous, multi-page table)
   is flagged TBD with the source coordinate captured; the user
   reconciles manually before the gate at D19 turns green.
   Held until methodology owner supplies a sample real ASR Excel
   AND a sample real ASR PDF. Without samples, prototyping would
   be guesses about ASR layout (Apex Omega rule 4).

- Debug pass on the CLB-4 product (commit 8a49fa8). Two real
  bugs found and fixed; validator stayed at 8 PASS / 0 FAIL.
  Bug 1: UNIT_ROLLUP grand total at E35 mixed UoMs. Replaced
    with one SUBTOTAL row per UoM that appears in the unit's
    CCN list. CLB-4 now emits SUBTOTAL (EA), SUBTOTAL (GSF),
    SUBTOTAL (GSY), SUBTOTAL (KW), SUBTOTAL (LF), SUBTOTAL (MI)
    each summing only matching-UoM cells. Per Apex Omega rule 4,
    when you cannot honestly sum heterogeneous units, you do
    not pretend.
  Bug 2: methodology mismatch on engineering-study CCNs.
    pipeline/template.py methodology_warning_for(ccn, pattern)
    returns a one-line warning when a CCN's chosen pattern is
    closed-form (admin / primary_items / shop_with_bays /
    default) AND the CCN has no factor table in
    PLANNING_FACTORS AND has narrative_sections. Warning rendered
    in WARNING_FILL palette (#F8E2D6) above the citation footer.
    Verified on out/CLB4_BFR_full.xlsx:
      53010 BAS Dispensary  (admin, engineering-study) -> warning
      61072 BN HQ Admin     (admin, engineering-study) -> warning
      14345 Armory          (primary_items, factor)    -> clean
      54010 Dental Clinic   (admin, factor)            -> clean
      72210 Galley          (admin, factor)            -> clean
    Apex Omega rule 4 enforced at the generated-BFR level: the
    user sees inline that those numbers are CLB-4 observed-pattern
    placeholders, not FC-defensible.

- 3d MED BN strategic basing package landed (origin/main commit
  30bdeaa, merged into dev branch). Six artifacts at repo root:
    "3d Med Bn Strat Basing Req CG SIGNED (004).pdf"  (signed)
    "CG Endorsement Surg Co B 3d Med Bn 3d MLG - G-5 Basing
      Actionv1.docx"
    "FW_ CG MCIPAC Endorsement Request 2026-04-30T15_19_44+
      09_00.eml"
    "Tab A - 3d MLG, 3 MED BN, SURGICAL CO B. Endorsement
      Letters (1).pdf"
    "Tab B - 3d MLG Bravo Surgical Decision Brief v2 (2).pdf"
    "Tab C - Basing assessment Surg Co B_MCB Butler Aug 2025_
      KMedit 250926.pptx"
  Subject: III MEF 3d MLG Strategic Basing Program request for
  Surgical Company B at MCB Camp Butler. Strategic basing is
  upstream of BFR generation (decides WHERE the unit sits); BFR
  is the facility requirements document once site is chosen.
  Pipeline applies to 3d MED BN as soon as TFSMS exports for
  the unit (or Surgical Co B specifically) arrive. NEXT-list
  expansion: a 3d MED BN unit profile + CCN list (mirroring
  samples/clb4_*.json) plus M134* / M67400* TFSMS exports for
  the unit's companies.

- 3d MED BN package read in full (this session, 2026-04-30 JST,
  on branch claude/resume-bfr-pipeline-nrRNC at HEAD 00c2f00).
  All six artifacts opened and analyzed; the CG signed letter is
  scanned image-only and required tesseract OCR to extract.
  Captured products in audit/:
    audit/3DMEDBN_BASING_BRIEF.md
      Strategic-basing rundown for the user. Reconciles three
      conflicting documents:
        Tab B v9 (16 Mar 25), Tab C MCBB GF (1 Aug 25) - both
          scoped to Bravo Surg Co only on Camp Foster (180 PN);
          Tab C scorecard had Foster 4.45 vs Kinser 4.15.
        CG signed ltr (2 Feb 26) - supersedes; consolidates
          entire 3d Med Bn (HQ&S + Alpha + Bravo + MT/UT + MSTC,
          711 PN) on Camp Kinser.
        CG MCIPAC endorsement docx (Wolford draft) - confirms
          Kinser, names six buildings: 107 (battalion co-use),
          300 (MSTC), 613 (MT/UT), 400 (consolidated armory bay),
          1225 (housing), 508 (supply). Tasker DON-250501-LTNQ.
          POC Mark J. Godfrey, AC/S G-5 MCIPAC-MCBB.
      Tab C facility categories mapped to CCN candidates:
        ARMORY 944 SF                -> 14345
        STORAGE/WAREHOUSE 3,500 SF   -> 44110
        ORGANIC STORAGE 800 SF       -> 44112
        HQS/ADMIN 4,063 SF           -> 61072 (or 61073 at Co level)
        APPLIED INSTRUCTION 2,815 SF -> 17120
        AUTO ORG SHOP 2,848 SF       -> 21410 (LOW confidence;
          21410 vocab name is Combat Vehicle Maint Shop, medical
          bn is not a combat-vehicle unit; Apex Omega rule 4
          holds: render engineering-study warning, do not silently
          fill)
        TACTICAL VEH LAYDOWN 1,811 SY -> 85210 (PARKING AREA)
        BEQ ~50 beds                 -> 72111
        Role 2 medical               -> 53010 / 61074
      Surg Co B equipment T/E captured (Tab A p16 / Tab B p7):
        18 D00267K JLTV ambulances and 18 D10017K M997 ambulances
        are the dominant laydown line item (36 ambulances total).
      Email source: Kenji Music (CIV, Facility Planning,
        MCBB PWB / GF / MCIPAC, DSN 315-645-3207) asked Doug Burk
        and Anthony Potter (both CTR) for bandwidth; sizing was
        "(1) Planner and (1) Engineer" for "a couple weeks";
        framed as primer for the larger 3d MLG deep-dive.
        Inner FW from Keith Simon (G-5 Plans MCIPAC, DSN 315-
        645-2689) noted unit has effectively already moved to
        Kinser and endorsement paperwork is catching up.
    audit/email_to_kenji_DRAFT.md
      Human-voiced reply for the user (Anthony Potter) to send
      back to Kenji. Confirms Planner-side bandwidth, Engineer
      seat TBD with name in 1-2 days, reads back the basing
      action, proposes a 5-step first sprint, asks one data
      question (current INFADS pull for the Kinser building list
      vs. walk as data source), proposes Wed/Thu PM JST kickoff
      with Mr. Kaye looped in. No AI jargon; tone is contractor-
      to-customer professional.
  No code changes this session. Pipeline state unchanged
  (validator still 8 PASS / 0 FAIL on out/CLB4_BFR_full.xlsx).
  No TFSMS / ASR data for 3d Med Bn yet - profile + CCN list
  scaffolding still gated on user-supplied TFSMS export.
  Terminology audit on the package (per repo hard rules):
    CG signed letter writes "MCBB" (legacy).
    CG MCIPAC endorsement docx writes "MCBCB" once and "MCBB"
      twice (legacy).
    Our work product (audit/3DMEDBN_BASING_BRIEF.md and the
      Kenji email draft) uses MCIPAC and MCB Camp Butler
      throughout. Source spellings preserved verbatim only when
      directly quoting.

- Tracks 1d-extended-2 and 1e shipped together (Layer 3 BMOS
  rule lift + Layer 5 unit-type-defaults ratification using the
  now-supplied Series 500/600/700 narratives).
  audit/CLASSIFICATION_RULES.yaml: 7 BMOS rules lifted from
  TBD / confidence=low to confidence=high or medium with FC
  citations:
    bmos_8000_medical          -> 53010 high (Series 500 p8)
    bmos_2200_navy_dental      -> 54010 high (Series 500 pp11-13)
    bmos_2900_navy_nurse       -> 53010 medium (Series 500 p8)
    bmos_3300_food_service     -> 72210 high (Series 700 pp29-35)
    bmos_5800_mp               -> 73015 medium (Series 700 pp46-48)
    bmos_6500_aviation_ord     -> 21154 medium (Series 200 pp108-112)
    navy_nec_l0_corpsman       -> 53010 high (Series 500 p8)
    navy_nec_l1_idc            -> 53010 high (Series 500 p8)
    navy_nec_l3_dental         -> 54010 high (Series 500 pp11-13)
  Two rules stay at confidence=low (genuinely doctrine-dependent):
    bmos_0800_artillery (no dedicated artillery battery facility
      CCN exists; artillery occupies 21451 + 14345)
    bmos_6000_aviation_maint (hangar CCN choice depends on
      aircraft type; multi-CCN per unit; per-aircraft override
      via unit_context)
  audit/UNIT_TYPE_DEFAULTS.yaml: 11 admin_ccn slots ratified:
    CLB           -> 61072 high  (Series 600 p39, FC text exact)
    MLG_HQ        -> 61070 medium (parallel echelon to MARDIV/MAW)
    MEF_HQ        -> 61070 medium (echelon-equivalent default)
    MEU_CE        -> 61072 high  (battalion-equivalent CE)
    MAG_HQ        -> 61071 high  (FC text exact: "Marine Aircraft
                    Group Headquarters")
    MWHS          -> 61072 high  (squadron echelon by definition)
    AVIATION_SQUADRON -> 61072 low (FC 61072-1 explicitly notes
                    squadron admin "often provided within the
                    organizational maintenance hangar (Category
                    Code 211 05)"; default applies only when
                    standalone)
    RECRUIT_DEPOT -> 61010 medium (base support, full Series 600
                    BFR Generator)
    SCHOOLHOUSE   -> 61010 medium
    TRAINING_COMMAND -> 61010 medium
    DEPOT         -> 61010 high (base support, MCLB scale)
    INSTALLATION_HQ -> 61010 high (canonical base-support admin)
  samples/clb4_ccns.json gained CCN 54010 (3 dental billets) and
  72210 (8 food-service billets) so the workbook has sheets for
  the lifted rules' destinations. Generated CLB-4 BFR now spans
  28 sheets (was 26).
  Final CLB-4 worked-example state:
    TO populated rows : 310 (was 359 raw, 49 organizational
                       dividers filtered)
    Classified        : 310 / 310 = 100% (was 49% pre-Track-1d,
                       86.5% post-Track-1d-extended)
    Unclassified      : 0
    TE populated rows : 854
    TAMCN orphans     : 0
    Validator         : 8 PASS / 0 FAIL (was 6/2 immediately before)
  Per-CCN billet attribution (top 12): 44112w 63, 21730 49, 21451
  43, 53010 31 (medical concentration), 61072o 27, 61072c 20,
  14345 20, 14326 18, 21710ds 16, 21710 8, 72210 8, 21710shf 4.
  Definition of Done items 1-9 now satisfiable for any unit; item
  10 (inline citations) satisfied by Track 1c-citation; item 6
  (TFSMS gate) user-driven via the now-functional three-state
  gate (Track 8). The pipeline is structurally and doctrinally
  complete for CLB-4.

QA PASS shipped (Apex Omega Sec.5 rituals applied to the project
as a whole as of commit 4b02732, results captured 2026-04-30).

ALL GREEN:
  Git state clean. Branch claude/resume-bfr-pipeline-nrRNC synced
    with origin (0 commits ahead/behind at QA time).
  Validator out/CLB4_BFR_full.xlsx: 6 PASS / 2 FAIL. The 2 FAILs
    are Check 2 NOTE coverage and Check 7 billet accounting on
    42 Apex-Omega-rule-4 TBD-held billets (medical/dental/Navy
    NEC/food service) pending BMOS rule lift; expected.
  Validator out/CLB4_BFR_sample.xlsx: 8 PASS / 0 FAIL.
  Methodology workbook recalc: 5,553 cells, zero error tokens.
  Generated CLB-4 BFR recalc: 15,041 cells, zero error tokens.
    Both via Python `formulas` package; fullCalcOnLoad=True.
  PLANNING_FACTORS.{yaml,json} sync: 1,003 records each.
  CCN_VOCABULARY.json 87250 entry well-formed with
    _provenance_note.
  Sample JSONs valid: samples/clb4_ccns.json 23 CCNs;
    samples/clb4_profile.json 11 keys (incl. unit_type).
  Defined-name health: 51 named ranges, ZERO with #REF! or #N/A.
    TFSMS_UNRECONCILED -> TFSMS_Loading!$D$19 (live formula).
    PN_TOTAL -> TFSMS_Loading!$O$37 (live ASR total cell).
  Pipeline modules import cleanly (classify, etl, template,
    validate); fc_citation_lookup and render_fc_citation_footer
    callable.
  End-to-end ETL on CLB-4 produces a 26-sheet workbook
    (UNIT_ROLLUP + TO + TE + 23 CCN sheets).
  Per-CCN attribution stable: 44112w (63), 21730 (49), 21451
    (43), 61072o (27), 61072c (20), 14345 (20), 14326 (18),
    21710ds (16), 21710 (8), 21710shf (4).
  CLAUDE.md DoD item 6 cites three-state gate workflow.
  Audit reports inventory: 41 files in audit/reports/.

FOUND AND FIXED:
  Six right-arrow Unicode characters (U+2192) in skill Track 5b
    DONE entry violated Apex Omega typography. Stripper converted
    to "to" automatically. Re-run idempotent (zero further
    changes). Same finding pattern surfaced in earlier work; no
    open instances remain.
  One stale "Series 400 or 600 not supplied" reference in Track
    1b DONE entry. Was true at the time of that commit; now
    resolved by Series 400/500/600 supply at commit 4b02732.
    Updated to note the resolution and the citation pages.

FOLLOW-UP (not blocking the QA pass; tracks remain in NEXT):
  Track 1d-extended-2: lift the 5 still-TBD BMOS rules
    (medical/dental/Navy NEC/food service) to confidence=high
    using Series 500/700 narratives. Closes Check 2 and Check 7.
    Pushes CLB-4 classification 86.5% -> ~100%.
  Track 1e: ratify 11 TBD admin_ccn slots in
    audit/UNIT_TYPE_DEFAULTS.yaml using Series 600 (610 70 / 71
    / 72 / 73 / 74 now supplied).
  Track 7 (re-scoped): ASR ingest accepting Excel and PDF;
    held until methodology owner supplies sample real ASR Excel
    AND sample real ASR PDF. Without samples, prototyping would
    violate Apex Omega rule 4.

The product is in a known-good state. Apex Omega Sec.5 rituals
all green: timestamping at point of citation, three-state TFSMS
gate, recalc-clean workbooks, citation traceability, three-
bucket separation honored, no IFERROR masking, no #REF! / #N/A
in defined names. Definition of Done item 6 satisfiable for any
unit once user pastes both TFSMS and ASR counts.

- Track 9, 3d MED BN basing dashboard cleanup, full-edit
  affordance, and live-tracker pattern. Five-pass wording,
  framing, citation, cosmetic, and editability cleanup of
  basing-assessment.html on branch
  claude/review-medical-battalion-html-5iTRP. Source artifacts
  for the pass: audit/3DMEDBN_BASING_BRIEF.md (the round-1
  briefing rundown, current as of 2026-04-30), the CG 3d MLG
  signed letter (February 2026), the CG MCIPAC endorsement draft
  (April 2026), Tab A / Tab B / Tab C as cited in the brief, and
  user-supplied resolutions to seven Open Questions captured
  in-session.

  Pass 1 (commit f031198), wording and citation hygiene.
  Classification banner unified to "Unclassified" at top,
  print-block, and footer (was Controlled Unclassified
  Information / FOUO at the bottom and CUI at the top; the
  dashboard does not handle CUI). Removed the planner's name and
  every named individual except one Mr. Kenji Music reference in
  the Mission Partner POC row of the Team Structure table; all
  other references replaced with role labels (MCIPAC mission
  partner, MCIPAC planner, AC/S G-5 MCIPAC). Stripped every
  "Source: ... email ..." citation; surviving citations name the
  underlying document with month and year only, no day, no time,
  no JST stamp. Renamed the odd block titles "What This Work Is"
  to "Scope", "Why It Matters" to "Operational Driver", and "Why
  the Tab B Scorecard No Longer Controls" to "Why the Tab B
  Scorecard Is Superseded". Replaced "Engineering Lift" community
  jargon with engineer / engineering survey throughout. Status
  glyphs in the checklist CSS changed from 'OK' to 'DONE' and
  'WIP' to 'IN WORK'. Removed the meaningless "Sourced" badge
  from the Timeline header.

  Pass 2 (commit 52860ec), user resolutions for the seven Open
  Questions. The Open Questions card was added to the bottom of
  Tab 5 in pass 1 with TBDs; pass 2 captured the user's
  in-session resolutions:
  - Bravo Surg Co BIC count: held TBD with sources conflict
    surfaced inline (Tab A 180, Tab C 181, strategic basing
    action 185); requires authoritative T/O reconciliation
    before the number is finalized. Numeric field stays editable.
  - Foster vs Kinser transitional state: new Component Status
    card added to Tab 2 with editable Element / Current Location
    / Status table. Seeded with confirmed moves (S-4 at Camp
    Kinser, MSTC at Camp Kinser) and TBD rows for HQ&S Co, Alpha
    Surg Co, Bravo Surg Co, MT and UT pending confirmation.
  - Bldg 300 condition: factual language captured (Life Safety
    Health concerns, requires more extensive project including
    extensive roof repair, may not be suitable for medical use
    as is); final medical battalion footprint subject to scoping
    outcomes.
  - Engineer assignment: held TBD pending contractor staffing
    decision.
  - HAP (Bldg 350) move timing: held TBD pending Army HAP
    relocation schedule.
  - Kinser Towers delivery: estimated 2030 to 2031; field
    editable.
  - ICG deconfliction: scope is new and developing; will require
    deconfliction throughout the lifecycle of the project and
    the relocation; field editable.

  Pass 3 (commit 1803ffd), fact verification and top / bottom
  cosmetic. Verified every numeric and factual claim against
  audit/3DMEDBN_BASING_BRIEF.md and this skill's content.
  Confirmed: 711 personnel total (CG signed letter para 5a),
  six Kinser buildings 107, 300, 613, 400, 1225, 508 (CG MCIPAC
  endorsement), Bravo Surg Co count discrepancy across Tab A 180
  and Tab C 181 and strategic basing 185, timeline dates for
  Tab A action letter 20 March 2025 and Tab B 16 March 2025 and
  Tab C 1 August 2025 and CG signed letter 2 February 2026, DPRI
  OKICON references for Foster 5665 demolition 2033 and 3d MLG
  retention beyond 2030. One pre-existing inference flagged but
  left in place: the "Fall 2025" timeline entry for the
  scope-shift event, which the brief documents but does not date
  to a season; entry preexists this Track 9 work and is not
  contradicted. Header subtitle replaced with "Camp Kinser
  facility planning for 3d Medical Battalion consolidation."
  Bottom-line block tightened. Tab 1 / Tab 2 / Tab 5 leads
  polished. Gold accent strip added above the footer to mirror
  the header accent; print rule extended to hide the strip in
  print. Cleaned residual "engineering lift" in Way Forward and
  three "Kinser Tower" singular references to "Kinser Towers"
  plural to match the user's pass 2 resolution.

  Pass 4 (commit 51e0000), briefing-quality segues. Two
  transition points read abruptly when the deck is briefed in
  order; both bridged with one-sentence connectors, no factual
  content changed. Tab 0 Command Intent to Scope: Scope now
  opens "With command intent set, the team's task is downstream:
  facility planning and project development to execute the
  move." Tab 4 Foster Turnover to Bravo Surg Co Functional Space:
  Bravo block opens "Until the consolidated 3d Medical Battalion
  T/O is reconciled, the most detailed functional reference
  available is the Bravo Surgical Company data from Tab C slide
  20, captured below."

  Pass 5 (commit 4b71223), full editability and replaceable
  logos, per user direction that the dashboard must accommodate
  unforeseen changes as the project remains fluid.
  EDITABLE_SELECTOR in the in-page edit-mode JS extended to
  cover every visible text container that was previously
  read-only: header title eyebrow / h1 / subtitle, every tab
  label in the nav bar, table column headers (th), card section
  headings (h3 added; h2 already covered), metric labels above
  the big numbers, risk labels above risk titles, badge pills,
  source citation lines (.cite), and the footer label. Logo
  replacement wired via event delegation: in edit mode, clicking
  either logo in .logo-group opens a file picker; the selected
  image is read as a base64 data URL and swapped into the img
  src. The change is captured by autosave and persisted in the
  downloaded HTML when Save HTML runs. Edit-mode CSS gives logos
  a gold dashed outline plus pointer cursor as the affordance.
  Print-title block is no longer separately editable; it
  auto-syncs from the screen header on every input event so
  edits propagate to the printed output without the user
  maintaining two copies. Autosave / restore extended to capture
  and restore .site-header innerHTML so logo replacements and
  header edits survive accidental browser close. JS validated
  syntactically clean (node --check pass) with stubbed browser
  globals. STORAGE_KEY unchanged; new fields are optional, so
  existing autosaves load without error.

  Live-tracker pattern (methodology contribution applicable
  beyond this dashboard). Two cards in the dashboard implement a
  fluid-project tracker pattern other unit-agnostic deliverables
  can reuse:
  - Component Status table on Tab 2 with editable Element /
    Current Location / Status columns. Confirmed entries are
    seeded as data; unknowns are seeded as TBD pending
    confirmation. Updates land in one place as moves are
    confirmed.
  - Open Questions table at the bottom of Tab 5 with editable
    Question / Resolution Source columns. Each TBD created during
    a work pass is captured here with the source that would
    resolve it. Resolutions are folded back into the dashboard
    text in the next pass and the row updated.
  Apex Omega rule 4 (never silently fill) is enforced at the
  product level by these two tables: every unresolved item is
  visible to the briefer and the audience.

  Mission partner attribution rule (project-wide, applies to all
  briefer-facing deliverables in this repo). Named individuals
  are referred to by role (MCIPAC mission partner, MCIPAC
  planner, AC/S G-5 MCIPAC) rather than by name in body text.
  The single allowed exception is a Mission Partner POC row in a
  team or contact table where the proper name is the relevant
  data. No "per <person> email" framings; cite the underlying
  signed document or endorsement, never the email chain. Date
  format on surviving citations is month-year only, no day, no
  time, no JST stamp.

  File state at close of Track 9.
  basing-assessment.html, branch
  claude/review-medical-battalion-html-5iTRP, HEAD 4b71223. HTML
  well-formed (HTMLParser: 0 errors, 0 unclosed). Classification
  banner reads Unclassified at top, print-block, and footer.
  Zero em dashes, zero en dashes, zero markdown asterisk bold
  leaks. One Kenji Music reference (Mission Partner POC, allowed).
  Zero email or JST citations. Edit Mode covers every visible
  element. Logos replaceable in Edit Mode via click-to-replace.
  Print-title auto-synced from screen header. Open Questions
  tracker carries seven live items as of HEAD; Component Status
  tracker seeded with two confirmed moves and four TBD pending
  confirmation rows. Pipeline state (BFR generator, validator,
  ETL, classifier, planning factors) unchanged this track; no
  out/* artifacts modified.

- Track 9b, MCIPAC mission partner email handoff draft.
  Companion deliverable to Track 9: a draft reply on the existing
  CG MCIPAC Endorsement Request chain that hands the refreshed
  dashboard back to the mission partner and frames it as the
  project charter coming out of the 1 May email and the working
  session the prior Friday. File at audit/email_to_kenji_HANDOFF_DRAFT.md.
  Three iterations on this branch: initial draft (commit 9266d11)
  introduced the dashboard, reframe (commit cb91e3e) corrected
  the framing because the mission partner had already seen the
  prior version the week before so the email opens "refreshed
  dashboard" not "new dashboard", voice pass (commit dcdcbcd)
  rewrote bureaucratic phrasing (personnel-count disparity,
  validate against the authoritative T/O, is held as TBD, carried
  through) into how a colleague would actually say it.

  Email content covers: the updates rolled in from the 1 May
  email and Friday meeting (classification, naming, Tab B vs
  Kinser framing, component-level transitional status, six
  Kinser buildings carried through Foster turnover and the
  cross-cutting plans), the new full-edit and replaceable-logo
  affordances added in dashboard pass 5, the three open items
  the mission partner needs to know about (Bravo Surg Co BIC
  count disparity Tab A 180 / Tab C 181 / strategic basing 185,
  Bldg 300 Life Safety Health and roof condition, engineer
  assignment TBD), the parallel work pulling 3d MLG BFRs and
  the iNFADS reconciliation plan, and the ask for direct edits
  to the dashboard rather than a separate reply thread. About
  460 words, one screen.

  Voice rule for email deliverables (project-wide, narrower than
  the prose rule for analytical deliverables). Email is a
  conversation. Use contractions in moderation, prefer active
  voice, drop bureaucratic verbs (validate, reconcile against,
  is held as), short sentences win, paragraph breaks at natural
  pauses. Apex Omega typography rules still apply (no em dashes,
  no en dashes, no markdown asterisk bold, no decorative
  content, hyphens within identifiers stay). Cite documents not
  email chains within the email body itself. Sender signs with
  their own block; the draft leaves a placeholder block for the
  sender to fill in. The mission-partner attribution rule from
  Track 9 also applies in email body text: refer to others by
  role except where naming is the relevant data (cc lines, POC
  rows, named addressees).

  Project-charter handoff pattern (methodology contribution,
  reusable beyond this engagement). When a fluid-project
  deliverable is being handed back to the mission partner for
  ratification, frame the handoff as: status update plus
  refreshed deliverable, named call-out of the specific updates
  rolled in from the partner's prior guidance, brief note on
  any new affordances added, explicit list of open items the
  partner should know about (with TBDs visible), parallel work
  in progress, ask for direct edits to the deliverable rather
  than a separate reply thread, offer a working session. The
  pattern keeps the deliverable as the single source of truth
  rather than letting the email thread become a parallel
  authoritative artifact.

- Track 11, session 2026-05-06 on branch claude/apex-omega-audit-repair-gG9mM.

  ENVIRONMENT FIX. Created .claude/settings.json registering the
  SessionStart hook plus enableAllProjectMcpServers so ruflo MCP
  loads automatically next session. Prior session's "hook fix"
  edited the script but never registered it. Commit 3407bdf.

  EXTERNALLINKS PURGE (DEEP). Removed 5 orphaned externalLinks
  inside the xlsx archive (xl/externalLinks/externalLink1-5.xml
  plus _rels) that the prior session's formula-level purge missed.
  Removed externalReferences block from xl/workbook.xml, 5
  Relationship lines from xl/_rels/workbook.xml.rels, and 5
  Override lines from [Content_Types].xml. Excel file-open
  advisory eliminated. Critical finding: externalLink5 referenced
  M13020 2029 TO E CUT.xlsx on flankspeed SharePoint; user
  confirmed they do not have that file and the reference itself
  was fake. Commit 50a9094.

  MASTER TO&E v1.1 RECONCILIATION. Confirmed the 2031 Master TO&E
  v1.1 (dated 2025-04-11) IS the primary source for 3d MED BN
  (the prior skill's claim "does not cover CLB-4" was correctly
  about CLB-4 only; the file fully covers M28261 / M28262 /
  M28263). Per-UIC counts: H&S 288 billets / 198 TE rows; Surg B
  211 / 148; Surg A 210 / 160. The TE_3 schema carries L/W/H/Vol/
  NSY columns the BFR's CCN sheets reference but the BFR's own
  TE leaves blank. Commit c95a635.

  PARALLEL READING AGENT BATCH (10 agents). Spawned 10 reader
  agents to read files the prior sessions had not. Captured
  digests at audit/reports/3dmedbn/49_per_block_audit.md,
  50_doctrine_digest.md, 51_bfr_generator_digest.md,
  52_te_backfill_summary.md, plus inline returns. Findings:
   1. CCN 21451 visible 1,129 SF is a constant offset of
      J24=347*M33+1129 evaluated at M33=0; not a real value.
   2. CCN 14312 VLOOKUPs anchor to TE col H (TAMCN-short) but
      the sheet's C column carries full 7-char TAMCNs so every
      VLOOKUP misses. Plus offsets 16/17 hit empty TE columns.
   3. CCN 45110 8.89 number is in SY (square yards) per L50
      label, not GSF; the audit DEFECT 3 misread the unit.
   4. CCN 21710 sheet is correct as written; M37=0 officers is
      design-correct (3d MED BN has 0 comm officers, 4 enlisted
      comm repairers).
   5. 14345 H40 has K25 double-counted via P25.
   6. 61072 M27 and M28 have wrong CCN tag "61073" (should be
      "61072").
   7. 14345 sheet missing M28262 Surg B sub-block.
   8. 21451 21710 14312 each have an unlabeled "block 4/5" the
      roll-up sums but no UIC populates.
   9. BFR's TE col D carries CCN tags but Space Factor / NSY /
      NTG columns are blank; data lives in 2031 Master TO&E.

  USER-RATIFIED DECISIONS THIS SESSION (verbatim where
  possible):
   - "Surg A and B should be identical, even if you don't have
     any info on the other...they are identical on paper."
     -> A=B rule binding.
   - "You can delete it [H&S C00392B FILTER WATER PURIFI qty
     180] and put a read me in somewhere; that is the best."
     -> TE row 507 deleted; readme at
        audit/reports/3dmedbn/53_c00392b_h_and_s_deletion_readme.md.
   - User identified that I had been "hanging your hat on
     TAB C" while the user "given you the ASR and the BRFL".
     -> Source hierarchy correction encoded in GR-1 above.
   - User-supplied deep research (Claude Sonnet 4.6 Thinking)
     confirmed verbatim: FC 2-000-05N Series 500 v.500.20231703
     gives no methodology for CCN 53010 / 55010 / 55020.
     Sizing flows through FC Section 500-2 to BUMED Echelon 3
     (NMW for MCIPAC) HCRA + Program for Design. DHA SPC chapters
     and SEPS are restricted to DHA-managed MTF projects; 3d
     MED BN is NOT a DHA MTF, so SPC use requires NMW
     authorization. Table 500-1 net-to-gross 1.35 (primary care,
     emergency, specialty surgical, preventive med, dental) /
     1.60 (surgery) / 1.25 (pathology). Documented at
     audit/reports/3dmedbn/54_medical_ccn_regulatory_finding.md.

  BFR FIXES APPLIED THIS SESSION.
   - TE row 507 (H&S C00392B) deleted; validator stays 8/0.
     Commit ecf6725.
   - 24 mirror rows added to TE (rows 507-530) to make Surg A
     and Surg B TAMCN inventories identical per A=B rule. Fixed
     all five CCNs (14312, 14345, 21451, 21710, 44112).
     Commit 5cc3fee.

  APEX OMEGA VIOLATIONS, STATUS AT END OF SESSION.
   V1 (H&S C00392B qty 180): CLOSED. Row deleted with readme.
   V2 (574 clinical billets to 61073 = 0 SF): OPEN. Doctrinal
       path documented (BUMED HCRA per FC 500-2). Implementation
       deferred until HCRA in hand. Layer 2 reclassification of
       574 billets from 61073 to 53010 NOTE pending.
   V3 (MISSION STATEMENT B208 "FOSTER BUILDING TBD"): OPEN.
       Two candidate fixes: mirror Surg A address (UNIT 38448 /
       FPO 96604-8448 / JP) per A=B rule, or mirror BN HQ
       address (UNIT 38445 / FPO 96373-4500 / JP) per prior
       Track 10e ratification. User pick still pending.
   V4 (back-test against CG signed letter 711 PN): PARTIAL.
       Master TO&E + ASR confirm 711 raw / 609 chargeable BIC.
       BFR has 710. 1-billet delta source not yet identified.

  CCN-SHEET DEFECT-CLASS HISTOGRAM (per agent
  aeb477ccc70646179, 124 blocks):
   DC2 SUMIFS/COUNTIFS unpopulated TO/TE: 28 instances.
   DC3 IFERROR string fallback: ~750 row-formulas.
   DC4 uncited regression: 2 (21451 F24, J24).
   DC5 range mis-sum: 22.
   DC6 hardcoded single UIC: 1 (14345 G25).
   DC7 orphan block: 6.
   DC8 wrong CCN tag in COUNTIFS: 2 (61072 M27, M28).
   DC9 absent supporting cell: 5.
   DC10 literal "(none)"/0 sentinel: 4.

  HELD FOR NEXT SESSION (priority order):
   1. User pick on V3 Surg B postal block (A=B mirror or BN HQ
      mirror).
   2. Apply the easy CCN-sheet fixes from the per-block audit:
      14345 K25 double-count, 61072 wrong CCN tag, 17110 stub.
   3. Backfill BFR TE Space Factor / NSY / NTG / L,Ft / W,Ft /
      H,Ft / Vol_EA / Vol_Tot from 2031 Master TO&E keyed by
      (UIC, TAMCN). Re-anchor CCN sheet VLOOKUPs to point at
      the correct columns.
   4. Compute FC-method per-CCN totals using ASR personnel and
      Master TO&E equipment, NOT Tab C. Specifically:
       14345: 576 SF (FC 14345-1 step function on 711 PN).
       61072: 6,338 SF (39 admin Marines x 162.5 SF).
       61073: ~1,950 SF for true admin (12 billets x 162.5);
              clinical 574 -> 53010 TBD.
       14312: FC 14312-1 Type Code A-G method on Master TO&E
              vehicles by L,Ft.
       44112: FC 4-step method on Master TO&E volumes filtered
              to organic-storage TAMCNs only.
       45110: FC 4-step method, SH=4ft.
       21451: TBD pending engineering study (FC 21451-3).
       21710: 1.07 nsm/cm volume x 1.65 NTG via FC 21710-3.
       17120: 150 GSF/student via FC 17120-3.1; existing
              2,815 SF passes through.
       53010 / 55010 / 55020: TBD pending BUMED NMW HCRA per
              FC 500-2.
   5. Apply Layer 2 reclass: 574 clinical billets from CCN
      61073 NOTE to CCN 53010 NOTE.
   6. Recalc, re-validate, deliver foundational document.

## Hand-off protocol (APEX OMEGA)

The user has flagged that when context approaches the limit, they will
request an "APEX OMEGA" handoff prompt, a structured dense summary that
lets the next session resume without losing context.

When asked for an APEX OMEGA handoff, produce a single document
containing:

1. Project state snapshot (commit hash, branch, files modified this session).
2. The six pipeline layers and which are done/in-progress/outstanding.
3. All decisions ratified by the user, with the exact phrasing used.
4. All open questions awaiting user input.
5. The next concrete action the receiving session should take, with
   specific files and line numbers when applicable.
6. Reading order for the receiving session: this skill, then `CLAUDE.md`,
   then `audit/PIPELINE.md`, `audit/STYLE_GUIDE.md`, `audit/FINDINGS.md`.

Do not start new work after the user requests the handoff. Hand off cleanly.
