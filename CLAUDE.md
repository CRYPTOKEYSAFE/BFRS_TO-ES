# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

This is **not a software project**. It is the working repository for a USMC
**Basic Facility Requirements (BFR)** audit and pipeline development effort.
The deliverable is an airtight, unit-agnostic, doctrinally-sound data pipeline
that ingests T/O&E source data and produces compliant BFRL workbooks per
**FC 2-000-05N** (the NAVFAC facility planning criteria, formerly UFC
2-000-05N / NAVFAC P-80, last updated Feb 2026).

CLB-4 (UIC `M29030`, 3d MLG, MCB Camp Butler / Okinawa) is the **worked
example** — the first unit being driven through the pipeline. It is **not**
the only unit and the tooling must be unit-agnostic.

The user has explicitly stated: **zero assumptions, zero gap-filling**. If a
formula is wrong, flag it. If a CCN doesn't fit the unit's mission, flag it.
If a personnel-loading source is ambiguous, ask before proceeding. Never
guess.

## Authoritative documents

- **`audit/FINDINGS.md`** — Round-1 forensic findings on CLB-4 (which file is
  authoritative, what's broken, what's missing).
- **`audit/PIPELINE.md`** — Round-2 unit-agnostic pipeline contract spec.
  Defines the six layers that must hold for a BFR to be airtight. Read this
  first.
- **`audit/reports/`** — All evidence artifacts (sheet inventories, CCN-tab
  dumps, schema maps, probe outputs). Never delete.

## Data files in repository root (inputs, never edit)

| File | Format | Role |
|---|---|---|
| `SW_M29030_CLB4_BFR_2026-NWPCW167400L021.xlsx` | B (BFR-embedded TO/TE) | **Authoritative CLB-4 BFR**, Feb 2026 |
| `SW_M29030_CLB4_BFR_2026.xlsx` | B | Earlier sibling, ignore unless diffing |
| `FO_M29030_CLB 4_FINAL BFR.xlsx` | B | **STALE** (May 2025), do not use |
| `M29111_HQ_CO_CLB-4.xlsx` | A (per-co T/O export) | CLB-4 HQ Co billet+TE roster |
| `M29112_CLC_A_CLB-4.xlsx` | A | CLC A Co roster |
| `M29113_CLC_B_CLB-4.xlsx` | A | CLC B Co roster — **openpyxl-touched** on upload day; data preserved but flagged |
| `M29114_GS_CO_CLB-4.xlsx` | A | GS Co roster — **openpyxl-touched**, same caveat |
| `M67400-FO-M13020 3D MED BN-22NOV2024.xlsx` | B | 3d Med Bn benchmark (also problematic) |
| `2031 Master TO&E v1.1 - 20250411.xlsx` | C (Master MEF) | Does **not** cover CLB-4; covers a different MEF/MLG |
| `E_BFR_F_PRC_BU26-5836R_POM26_20260228_2_OF_2.pdf` | — | POM26 package "2 of 2"; "1 of 2" is missing |
| `Sch1024_Worklist for Unit Brief.xlsx` | — | Unit briefing worklist |

## The data pipeline contract (read `audit/PIPELINE.md` for the full spec)

Six layers, every one must hold:

1. **Source format awareness** — three formats (A: per-co MCTOFD-style; B:
   BFR-embedded; C: Master MEF/MTOMS-T-style).
2. **CCN+suffix tagging mechanism** — the `NOTE` column in Format B carries
   tags like `21710o`, `44112w`, `14345a`. **This is the pipeline spine and
   it is currently unpopulated across every workbook in the repo.**
3. **Classification rule set** — function from
   `(BIC, Billet Description, Alpha Grade, BMOS, PMOS, MCC)` to a NOTE tag.
   Currently undocumented; needs FC 2-000-05N + unit doctrine input.
4. **In-workbook TO/TE schema** — Format B layout (TO has `LINE | NOTE | CCN
   | CCN Description | UIC | Rec CD | BIC | Billet Description | Alpha Grade
   | BMOS | PMOS | …`; TE has `ROW | NOTE | CCN | … | TAMCN | … | L,Ft |
   W,Ft | H,Ft | Volume Ea | Volume Total`).
5. **Stable lookup contracts in CCN sheets** — full-column refs
   (`'TO'!$B:$B`), no `IFERROR` masking, named-range constants. Legacy CCN
   sheets violate this with brittle restricted ranges that have all become
   `#REF!`.
6. **Validation harness** — pass/fail report on schema, NOTE coverage,
   roll-up integrity, billet/equipment accounting. Does not yet exist.

## Cosmetic / structural style guide (binding)

The output BFR must look and tally like the **CLB-4 SW BFR** —
specifically the four rebuilt clean CCN sheets:

- `14345` (Armory)
- `21451` (Auto Org Shop)
- `21455` (Vehicle Wash Platform)
- `61072` (BN HQ Admin)

These are the visual + structural reference. The hidden broken sheets
(`14312`, `14326`, `21710`, `21730`, `44112`, `45110`) are **not** the
reference — they're the legacy template the rebuilds replaced.

If `audit/STYLE_GUIDE.md` exists, it captures the extracted fills, fonts,
borders, merge patterns, column widths, and page setup of those four
sheets. Treat it as binding.

The output must not look "robotic" or arbitrary — match the CLB-4
typography, colors, header banding, and page framing.

## Working conventions

- **Never modify the source workbooks.** They are inputs. All output goes
  to `audit/` (reports, generated artifacts) or to a clearly-named output
  directory.
- **All audit artifacts are committed.** Evidence trail matters; don't
  rewrite history of `audit/reports/`.
- **Branch policy:** all development on `claude/usmc-bfr-pipeline-jZb5F`.
  Push there; never to `main` without explicit instruction.
- **Stop hook** in this environment requires committing and pushing
  before stop. Plan accordingly.
- **Cosmetic fidelity is not optional.** When generating workbooks, match
  the CLB-4 style exactly (see `audit/STYLE_GUIDE.md` if present).
- **Math must be airtight.** Every formula must be verifiable against
  FC 2-000-05N planning factor tables. Every roll-up must trace.
  No `IFERROR(…,"")` masking allowed at the top level.
- **Unit-agnostic.** Tools that take a unit identifier or workbook path
  as a parameter, not hardcoded. CLB-4 is one example, not the universe.

## Common commands

The audit tooling is plain Python with `openpyxl`. Install once:

```bash
pip install openpyxl
```

Then:

```bash
# Inventory any workbook (sheet list, defined names, external links,
# per-sheet formula counts, merged cells, conditional formats, CCN-bearing rows).
python3 audit/inventory.py "<file.xlsx>"

# Dump every non-empty cell of a single sheet, formula side-by-side with
# cached value. Useful for forensic inspection.
python3 audit/sheet_dump.py "<file.xlsx>" "<sheet name>" [max_row]

# Map TO/TE header rows across all unit-data files.
python3 audit/schema_map.py

# Probe TO/TE sheets for CCN+suffix tags (the pipeline spine).
python3 audit/pipeline_probe.py
```

All of these write to stdout. Capture into `audit/reports/` for evidence:

```bash
python3 audit/inventory.py "<file>" > audit/reports/<n>_<name>.inventory.txt 2>&1
```

## What the audit has already established (round 1 + round 2)

Read `audit/FINDINGS.md` and `audit/PIPELINE.md` for full detail. The
short version:

1. The CLB-4 SW BFR rolls up to **14,299 GSF** across only 4 visible CCN
   sheets. Six additional CCN sheets exist in the same workbook, are
   hidden, and are all broken (lookup ranges destroyed, IFERROR masking
   blank values, copy-paste errors like CCN 21730 still searching for
   `21710o`). The 4 working sheets are clean rebuilds that hardcode
   counts; they are the cosmetic reference.
2. The `61072` admin sheet itself documents that 156 of CLB-4's billets
   are excluded from the admin count and require their own facility
   CCNs — exactly the broken-and-hidden ones.
3. Every TO/TE sheet in every workbook is missing the `NOTE` column
   tagging. The pipeline spine is empty.
4. The "Master TO&E" file does not cover CLB-4; CLB-4's source-of-truth
   T/O&E is the four `M2911x` company workbooks.
5. The 3d Med Bn benchmark has its own template-residue and external-link
   problems; it is not a clean reference.
6. All BFR files descend from a single 2017 NAVFAC MIDLANT template
   (Brunson, James J CIV); the accumulated debt is nine years deep.

## What's outstanding (round 3+)

- **Layer 2 vocabulary** — canonical CCN+suffix tag list per CCN, sourced
  from FC 2-000-05N. Doctrine work; needs SME or PDF extraction.
- **Layer 3 classification rules** — billet → tag function. Doctrine work.
- **Layer 4 ETL tool** — Format A/C → Format B. Engineering work.
- **Layer 4 canonical BFR template** — unit-agnostic, cosmetically matching
  CLB-4. Engineering work.
- **Layer 5 stable-lookup CCN sheet templates** — one per CCN type.
- **Layer 6 validation harness** — schema + coverage + roll-up checks.

## Hand-off discipline

When this session approaches its context limit, the user will request an
**APEX OMEGA handoff prompt** — a structured, dense summary that lets the
next session resume without losing context. Watch for that request and
prepare the prompt rather than starting new work.
