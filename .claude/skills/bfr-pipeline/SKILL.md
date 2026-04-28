---
name: bfr-pipeline
description: USMC Basic Facility Requirements (BFR) audit and workbook generation for the BFRS_TO-ES repository. Use whenever the user asks about BFR worksheets, BFRL, FC 2-000-05N planning factors, TO&E ingestion, CCN classifications, the data pipeline between TO&E source data and BFRL output, the cosmetic style of generated workbooks, or any operation on the .xlsx files in this repo. Triggers include words like BFR, BFRL, CCN, TO&E, FC 2-000-05N, UFC 2-000-05N, P-80, MCTOFD, MTOMS-T, INFADS, NTG factor, GSF/GSY/NSY, MLG/MEF/CLB unit names.
---

# BFR Pipeline Skill (project-local)

Activate this skill the moment any BFR-related task is requested in this
repository. It encodes the project's contract, conventions, audit state,
and binding style guide so a fresh session does not re-derive them or drift.

## Read-first artifacts (always)

Before doing any BFR work, read these in order:

1. `CLAUDE.md` — repository overview and working conventions.
2. `audit/PIPELINE.md` — the six-layer unit-agnostic data pipeline contract.
3. `audit/STYLE_GUIDE.md` — binding cosmetic specification for generated
   workbooks (extracted from the four rebuilt clean CCN sheets in CLB-4 SW).
4. `audit/FINDINGS.md` — Round-1 forensic findings on CLB-4 (current state).

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

## Hard rules

These come directly from the user. Treat as non-negotiable.

- **Zero assumptions.** If a value, rule, or mapping is unclear, ask.
  Never guess. Never gap-fill from training data.
- **Unit-agnostic.** CLB-4 is the *worked example*, not the universe.
  Tools take a unit identifier or path as input.
- **Cosmetic fidelity.** Generated workbooks must match the CLB-4
  rebuilt clean sheets pixel-for-pixel (theme colors, fonts, fills,
  borders, merged-cell skeleton, page setup, footer text). Robotic /
  default-Excel output is rejected.
- **Math airtight.** Every formula traces to FC 2-000-05N. Every roll-up
  ties out. No `IFERROR(…,"")` masking allowed at the top level. No
  restricted-range lookups (use full-column refs). No external links.
- **Source files are read-only.** Inputs in repo root are never edited.
  Outputs go under `audit/` or a clearly-named output directory.
- **Branch:** all development on `claude/usmc-bfr-pipeline-jZb5F`.
  Commit and push at meaningful milestones (the stop hook enforces this).

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

## CLB-4 file inventory (as of round 2)

- **Authoritative BFR:** `SW_M29030_CLB4_BFR_2026-NWPCW167400L021.xlsx`
  (Feb 2026). Roll-up = 14,299 GSF across 4 visible CCN sheets.
- **Stale, do not use:** `FO_M29030_CLB 4_FINAL BFR.xlsx` (May 2025).
- **Cosmetic reference sheets (clean):** `14345`, `21451`, `21455`,
  `61072` inside the SW file.
- **Hidden broken sheets:** `14312`, `14326`, `21710`, `21730`, `44112`,
  `45110` — same workbook. Lookup ranges all `#REF!`. Do not extend
  these; rebuild against the contract.
- **Per-co T/O exports (Format A):** `M29111_HQ_CO_CLB-4.xlsx`,
  `M29112_CLC_A_CLB-4.xlsx`, `M29113_CLC_B_CLB-4.xlsx` (openpyxl-touched),
  `M29114_GS_CO_CLB-4.xlsx` (openpyxl-touched).
- **Master TO&E:** `2031 Master TO&E v1.1 - 20250411.xlsx` does **not**
  cover CLB-4 (covers a different MEF/MLG; M29030/M29111-14 absent).

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
