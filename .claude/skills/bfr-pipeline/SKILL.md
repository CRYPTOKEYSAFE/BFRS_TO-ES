---
name: bfr-pipeline
description: USMC Basic Facility Requirements (BFR) audit and workbook generation for the BFRS_TO-ES repository, under Apex Omega methodology. Use whenever the user asks about BFR worksheets, BFRL, FC 2-000-05N planning factors, TFSMS / ASR / T/O&E ingestion, CCN classifications, the data pipeline between T/O&E source data and BFR output, the cosmetic style of generated workbooks, or any operation on the .xlsx files in this repo. Triggers include words like BFR, BFRL, CCN, TFSMS, ASR, T/O&E, FC 2-000-05N, UFC 2-000-05N, P-80, INFADS, NTG factor, GSF/GSY/NSY, ACF, SIOH, MILCON, Okinawa, MCBJ, MCIPAC, MLG/MEF/CLB unit names, Apex Omega.
---

# BFR Pipeline Skill (project-local)

Activate this skill the moment any BFR-related task is requested in this
repository. It encodes the Apex Omega methodology, the project's
contract, conventions, audit state, and binding style guide so a fresh
session does not re-derive them or drift.

## Read-first artifacts (always, in this order)

1. **`APEX_OMEGA.pdf`** — binding methodology briefing. Non-negotiable
   rules in §2; anti-patterns in §6; QC rituals in §5; output
   conventions in §8.
2. `CLAUDE.md` — repository overview + Apex Omega rules restated +
   working conventions.
3. `audit/PIPELINE.md` — six-layer unit-agnostic data pipeline contract.
4. `audit/MCBJ_GENERATOR_NOTES.md` — annotated tour of the
   `MCBJ_BFR_Generator_FC2-000-05N.xlsx` (methodology + math reference).
5. `audit/STYLE_GUIDE.md` — binding cosmetic specification (CLB-4 theme
   styling + Apex Omega 4-color cell-role palette).
6. `audit/FINDINGS.md` — Round-1 forensic findings on CLB-4.

## Project mental model

The end-state is a unit-agnostic ETL + generator that:

1. **Ingests** TO&E source data in any of the three observed formats:
   - Format A (per-company MCTOFD-style export — no CCN tagging)
   - Format B (BFR-embedded TO/TE — CCN+suffix in NOTE column)
   - Format C (Master MEF/MTOMS-T-style — rich data, CCN header empty)
2. **Classifies** every billet to a `<CCN><suffix>` NOTE tag using a
   documented rule set (FC 2-000-05N planning factors + unit doctrine).
3. **Emits** a Format-B-compliant in-workbook TO and TE.
4. **Generates** CCN calculation sheets that reproduce the CLB-4
   rebuilt look exactly (per `STYLE_GUIDE.md`) and use stable lookup
   contracts (full-column refs, no IFERROR masking).
5. **Validates** the output against a deterministic harness (Layer 6).
6. **Rolls up** to a `UNIT_ROLLUP` sheet that traces every cell back
   to a CCN sheet's TOTAL REQUIREMENT cell.

## Hard rules (Apex Omega override defaults)

- **Facts only.** No assumptions, speculation, AI jargon. Ask if unclear.
- **Cite source + section + date inline** for every regulatory or
  numeric claim. Format: *"FC 2-000-05N §61010-3, current as of
  2026-02-11"*.
- **Three-bucket separation:** regulatory / program-practice / external
  benchmark. Never blend.
- **Mark unverified items as `TBD — pending [source/action]`.** Never
  silently fill.
- **Show the math.** Every derived number reproducible from inputs in
  the same artifact (formulas in Excel, equations in Markdown).
- **Plain prose.** Lead with the answer. No "let's", no "I'll help you",
  no preamble, no marketing tone, no emojis.
- **Reconciliation gate.** TFSMS RecapMCC must be reconciled against
  ASR / T/O&E before any BFR is releasable. The
  `TFSMS_UNRECONCILED` flag in MCBJ at `TFSMS_Loading!$D$19` is the
  operational implementation. Never bypass.
- **Recalc requirement.** Every openpyxl-generated workbook must be
  recalculated by LibreOffice headless before delivery. Zero `#REF!`,
  `#DIV/0!`, `#NAME?`, `#VALUE!` after recalc.
- **Unit-agnostic.** CLB-4 is the worked example. Tools take a unit
  identifier or path as input.
- **Cosmetic fidelity.** Generated workbooks reproduce the CLB-4
  rebuilt-clean-CCN look (theme tints, fonts, fills, borders, merged
  cells, page setup, footer text) **plus** the Apex Omega 4-color
  cell-role palette (input `#FFF8DC`, calc `#EAF3F4`, output `#DCE7C8`,
  warning `#F8E2D6`). No "default openpyxl" output.
- **Source files are read-only.** Inputs in repo root are never edited.
  Outputs go under `audit/` or a clearly-named output directory.
- **Branch:** all development on `claude/usmc-bfr-pipeline-jZb5F`.
  Commit and push at meaningful milestones (the stop hook enforces this).

## Authoritative references (Apex Omega §3) — confirm currency at use

| Reference | Use |
|---|---|
| **FC 2-000-05N (Series 100, 11 Feb 2026)** | Marine Corps BFR (primary for this work) |
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
form `<CCN><suffix>`. Observed suffix vocabulary (not yet canonical —
must be ratified against FC 2-000-05N):

| Suffix | Meaning |
|---|---|
| `o` | Office (≥ E-6 / officer) — 120 GSF/person |
| `c` | Cubicle (≤ E-5) — 60 GSF/person |
| `w` | Warehouse worker — 60 GSF/person, ÷3 ratio |
| `rs`/`cs`/`ds`/`ws`/`shf`/`ms` | Maintenance shop sections (radio/comm/data/wire/SHF/maint) — counted ÷15 → bays |
| `a` | Armory work-area / personnel |
| (bare CCN) | Equipment record's primary facility CCN (TE rows) |
| `1` | Personal Effects entitlement — 1 per chargeable person |

CCN calculation sheets count via `COUNTIFS('TO'!$B:$B, "21710o",
'TO'!$E:$E, $B$32)` etc. — `'TO'!$B:$B` is the NOTE column,
`'TO'!$E:$E` is the UIC column (per Format B schema).

## File inventory (as of round 3 merge from main)

- **Apex Omega briefing:** `APEX_OMEGA.pdf` (root). Read first.
- **Methodology + math reference:** `MCBJ_BFR_Generator_FC2-000-05N.xlsx`
  (root). Implements TFSMS reconciliation gate, CCN library, Okinawa
  adjustments, named-range API. See `audit/MCBJ_GENERATOR_NOTES.md`.
- **Authoritative CLB-4 BFR (cosmetic + structural reference):**
  `SW_M29030_CLB4_BFR_2026-NWPCW167400L021.xlsx` (Feb 2026). Roll-up =
  14,299 GSF across 4 visible CCN sheets.
- **Stale, do not use:** `FO_M29030_CLB 4_FINAL BFR.xlsx` (May 2025).
- **Cosmetic reference sheets (clean):** `14345`, `21451`, `21455`,
  `61072` inside the SW file.
- **Hidden broken sheets:** `14312`, `14326`, `21710`, `21730`, `44112`,
  `45110` — same workbook. Lookup ranges all `#REF!`. Do not extend
  these; rebuild against the contract.
- **TFSMS exports (Format A, per company):**
  `M29111_HQ_CO_CLB-4.xlsx`, `M29112_CLC_A_CLB-4.xlsx`,
  `M29113_CLC_B_CLB-4.xlsx` (openpyxl-touched),
  `M29114_GS_CO_CLB-4.xlsx` (openpyxl-touched).
- **Master TO&E (Format C, TFSMS-style):**
  `2031 Master TO&E v1.1 - 20250411.xlsx` — does **not** cover CLB-4
  (covers a different MEF/MLG; M29030/M29111-14 absent).

## Standard tooling (`audit/*.py`)

```bash
pip install openpyxl   # once

python3 audit/inventory.py "<file.xlsx>"
python3 audit/sheet_dump.py "<file.xlsx>" "<sheet>" [max_row]
python3 audit/schema_map.py
python3 audit/pipeline_probe.py
python3 audit/style_extract.py "<file.xlsx>" "<sheet>" [<sheet>...]
```

Capture output into `audit/reports/<NN>_<name>.txt` and commit. The
report numbering convention is sequential (`01_…`, `02_…`, …) — keep it.

## Outstanding work tracks (round 3+)

Pick from these. Each is independent enough to commit to as a unit.

- **Layer 2 vocabulary lock.** Extract the canonical CCN+suffix tag
  list from FC 2-000-05N (WBDG public PDFs) per CCN. Output:
  `audit/CCN_VOCABULARY.yaml`.
- **Layer 3 classification rules.** Document the
  `(BIC, Billet Description, Alpha Grade, BMOS, PMOS, MCC) → tag`
  function. Output: `audit/CLASSIFICATION_RULES.md` + a YAML/TOML
  rule table.
- **Layer 4 ETL.** Format-A-or-C reader → classifier → Format-B writer.
  Output: `pipeline/etl.py` + tests.
- **Layer 4 canonical BFR template.** Cosmetic-faithful CCN sheet
  generator using `openpyxl` + the `STYLE_GUIDE.md` spec. Output:
  `pipeline/template.py` + a generated sample to compare against
  CLB-4 SW visually.
- **Layer 5 stable-lookup CCN sheet patterns.** One per CCN type
  (admin, shop+bay, warehouse, laydown, etc.). Output:
  `pipeline/ccn_sheets/`.
- **Layer 6 validation harness.** Schema + NOTE coverage + roll-up +
  billet/equipment accounting. Output: `pipeline/validate.py` +
  pass/fail report format.

## Hand-off protocol (APEX OMEGA)

The user has flagged that when context approaches the limit, they will
request an "APEX OMEGA" handoff prompt — a structured dense summary that
lets the next session resume without losing context.

**When asked for an APEX OMEGA handoff, produce a single document
containing:**

1. Project state snapshot (commit hash, branch, files modified this session).
2. The six pipeline layers and which are done/in-progress/outstanding.
3. All decisions ratified by the user, with the exact phrasing used.
4. All open questions awaiting user input.
5. The next concrete action the receiving session should take, with
   specific files and line numbers when applicable.
6. Reading order for the receiving session: this skill, then `CLAUDE.md`,
   then `audit/PIPELINE.md`, `audit/STYLE_GUIDE.md`, `audit/FINDINGS.md`.

Do not start new work after the user requests the handoff. Hand off cleanly.
