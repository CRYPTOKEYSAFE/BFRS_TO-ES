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
6. `audit/FINDINGS.md`, Round-1 forensic findings on CLB-4.

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
- Branch: development branch is set per session by the harness
  (current: `claude/resume-bfr-pipeline-Uf9Td`). Never push to `main`
  without explicit instruction. Commit and push at meaningful
  milestones (the stop hook enforces this).

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
- Pipeline package: `pipeline/`
  - `pipeline/template.py`, Layer 4 BFR generator. Produces a
    Format-B BFR for any unit profile + CCN list.
  - `pipeline/validate.py`, Layer 6 validator. Six-check pass/fail
    report against any Format-B BFR workbook.
- Sample inputs: `samples/clb4_profile.json`,
  `samples/clb4_ccns.json`. Worked-example unit profile and CCN list
  for CLB-4.
- Sample output: `out/CLB4_BFR_sample.xlsx`. Generator output for
  CLB-4 (10 CCNs). Validator report at
  `audit/reports/17_validate_generated_clb4.txt` (6 PASS / 0 FAIL).
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
python3 pipeline/template.py --profile <profile.json> --ccns <ccns.json> --output <path.xlsx>
python3 pipeline/validate.py <workbook.xlsx> [--report <path>]
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
  Check 7. No `pipeline/classify.py` yet; rule schema is stable
  enough to build against without churn.

### NEXT (in this order)

1. Pull FC 2-000-05N Series 100 (file
   `fc_2_000_05n_100series_12_10_2025.pdf`, version
   `100.20251210`, 10 Dec 2025) and Series 200 (file
   `fc_2_000_05n_200series_05_16_2025.pdf`, version
   `200.20250516`, 16 May 2025) into the repo (the Appendix A PDF is
   already at `fc_2_000_05n_appendixa.pdf`). Both Series PDFs are
   public WBDG documents but cannot be retrieved from this sandbox
   (egress allowlist blocks wbdg.org). User must supply the same way
   the Appendix A PDF was supplied (drop into a commit on `main`,
   pull from GitHub MCP, then `git checkout origin/main, file`).
2. Extract planning factor tables from Series 100 and Series 200 into
   `audit/PLANNING_FACTORS.yaml` (per-CCN: row layout, loading driver,
   SF/person or SF/bay, NTG, ROUNDUP convention, source page +
   table reference). Re-extractor script lives at
   `audit/extract_planning_factors.py`, similar pattern to
   `audit/extract_ccn_appendix_a.py`. Apex Omega timestamp every
   record with the source PDF's printed version date.
3. Layer 5 pattern ratification. Compare the three observed shapes
   from `pipeline/template.py` (primary_items, admin, shop_with_bays,
   commit `b9ab701`) against the per-CCN planning factors from step
   2. Update pattern_data defaults and docstrings to cite source +
   section + date inline. Add new pattern variants where the actual
   FC 2-000-05N table calls for a different shape (aviation
   maintenance, MEU embarkation, depot, training command, recruit
   depot, schoolhouse, range complex, ammo/ordnance, fuel farm,
   comm/data center, medical/dental, port, etc.). Drop any defaults
   that cannot be verified against the current FC 2-000-05N edition;
   mark such fields TBD per Apex Omega rule 4.
4. Layer 3 classification rules. Author
   `audit/CLASSIFICATION_RULES.md` + YAML/TOML rule table mapping
   `(BIC, Billet Description, Alpha Grade, BMOS, PMOS, MCC) -> NOTE
   tag`. Required to populate the NOTE column in TO/TE so the
   generator can place each billet on the right CCN sheet.
5. Track D, PDF ingestion prototype (only when a Format-D source
   actually arrives). Extracts billet/equipment rows from TFSMS / ASR
   / authoritative PDF into canonical Format A schema with per-row
   page+table citation. `pdfplumber` first; OCR only for scanned PDFs.
6. Layer 6 advanced checks. Billet accounting (TO row count equals
   sum across CCN sheets, no orphans, no double counts) and equipment
   accounting (every TAMCN row in TE referenced by exactly one CCN
   sheet). Add to `pipeline/validate.py` once specialized templates
   produce billet-bearing test fixtures.

### PARALLEL (doctrine work, can start any time)

- Layer 3, classification rules. Document the
  `(BIC, Billet Description, Alpha Grade, BMOS, PMOS, MCC) to NOTE-tag`
  function as `audit/CLASSIFICATION_RULES.md` + YAML/TOML rule table.
  Required for Track B to be fully unit-agnostic; Track B can stub
  with an externally-supplied rule list until this is authored.

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
