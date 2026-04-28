# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Apex Omega — binding methodology

Every output in this session operates under **Apex Omega** rules.
The full briefing is `APEX_OMEGA.pdf` (root). Read it first. The
non-negotiables are also restated below; if they conflict with anything
else in this file, Apex Omega wins.

1. **Facts only.** No assumptions, speculation, or AI jargon.
2. **Verify line by line, block by block, reference by reference.**
   Confirm publication status (date, change page, supersession) of every
   reference before producing a report.
3. **Use only current authoritative sources.** Older PDFs are never
   treated as current authority without re-verification.
4. **If something cannot be verified, omit it or mark `TBD — pending
   [source/action]`.** Never guess to fill a gap.
5. **Time-stamp external data at the point of citation**
   (e.g. *"UFS 3-701-01, current as of 2026-03-27"*).
6. **Three-bucket fact separation:** (a) regulatory facts, (b)
   program-practice facts, (c) external benchmarks. Do not blend.
7. **Numbers must be traceable.** Only use numbers explicitly stated in
   a cited source or a user-supplied file.
8. **Plain prose only.** Lead with the answer. No "let's", no
   "I'll help you", no preamble, no marketing tone, no emojis or
   decorative content.

### Anti-patterns (banned)

- Speculation or invented numbers.
- Stale citations.
- **Treating TFSMS exports as authoritative without ASR reconciliation.**
- Conflating ERC (Economic Replacement Cost) with PRV (Plant Replacement Value).
- AI-style hedging ("widely believed", "in general", "may be approximately").
- Decorative content in technical deliverables.

### Quality-check rituals (before any deliverable is "done")

1. Back-test against prior signed estimates / actuals where available.
2. Pressure-test current estimates: re-derive from inputs.
3. Confirm publication status of every cited document.
4. Verify references against primary sources, not secondary citations.
5. Recalculate spreadsheets after any change (LibreOffice headless via
   `scripts/recalc.py` or equivalent). **Zero `#REF!`, `#DIV/0!`,
   `#NAME?`, `#VALUE!` after recalc — required.**
6. **Reconciliation gate:** TFSMS RecapMCC personnel data must be
   reconciled against the unit's authoritative ASR / T/O&E before any
   BFR can be released.

## What this repository is

The working repository for a USMC **Basic Facility Requirements (BFR)**
audit and pipeline development effort. The deliverable is an airtight,
unit-agnostic, doctrinally-sound data pipeline that ingests TFSMS / ASR
T/O&E source data and produces compliant BFR workbooks per
**FC 2-000-05N (Series 100, 11 Feb 2026)** — Marine Corps Basic Facility
Requirements (formerly UFC 2-000-05N / NAVFAC P-80).

CLB-4 (UIC `M29030`, 3d MLG, MCIPAC, MCB Camp Butler / Okinawa) is
the worked example. It is **not** the only unit; tooling must be
unit-agnostic.

**Terminology — current correct nomenclature.** The installation is
**MCB Camp Butler**; the Echelon II command is **MCIPAC** (Marine Corps
Installations Pacific). Do **not** use "MCBJ" (Marine Corps Base Japan)
or "MCBB" (Marine Corps Base Butler) as place or organization terms —
those are legacy / pre-MCIPAC and are technically incorrect. The
filename `MCBJ_BFR_Generator_FC2-000-05N.xlsx` retains the legacy
prefix as supplied; references to the file itself use that filename
verbatim, but no project documentation uses "MCBJ" as a term.

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
| `APEX_OMEGA.pdf` | — | **Binding methodology briefing.** Always read first. |
| `MCBJ_BFR_Generator_FC2-000-05N.xlsx` | — | **Apex Omega methodology reference workbook** for BFR work. Implements TFSMS-to-ASR reconciliation gate, `CCN_Library`, Okinawa ACF/SIOH/PD/Contingency adjustments, and named-range API (`PN_OFF`, `PN_ENL`, `PN_TOTAL`, `Okinawa_Navy_ACF`, etc.). |
| `SW_M29030_CLB4_BFR_2026-NWPCW167400L021.xlsx` | B (BFR-embedded TO/TE) | **Authoritative CLB-4 BFR**, Feb 2026. Cosmetic + structural reference. |
| `SW_M29030_CLB4_BFR_2026.xlsx` | B | Earlier sibling, ignore unless diffing |
| `FO_M29030_CLB 4_FINAL BFR.xlsx` | B | **STALE** (May 2025), do not use |
| `M29111_HQ_CO_CLB-4.xlsx` | A (TFSMS export, per-co) | CLB-4 HQ Co billet+TE roster |
| `M29112_CLC_A_CLB-4.xlsx` | A (TFSMS export, per-co) | CLC A Co roster |
| `M29113_CLC_B_CLB-4.xlsx` | A (TFSMS export, per-co) | CLC B Co roster — **openpyxl-touched** on upload day; data preserved but flagged |
| `M29114_GS_CO_CLB-4.xlsx` | A (TFSMS export, per-co) | GS Co roster — **openpyxl-touched**, same caveat |
| `M67400-FO-M13020 3D MED BN-22NOV2024.xlsx` | B | 3d Med Bn benchmark (also problematic; not a clean reference) |
| `2031 Master TO&E v1.1 - 20250411.xlsx` | C (Master MEF, TFSMS-style) | Does **not** cover CLB-4; covers a different MEF/MLG |
| `E_BFR_F_PRC_BU26-5836R_POM26_20260228_2_OF_2.pdf` | — | POM26 package "2 of 2"; "1 of 2" is missing |
| `Sch1024_Worklist for Unit Brief.xlsx` | — | Unit briefing worklist |

**Reference hierarchy when generating BFR output:**

- **Methodology + math:** `MCBJ_BFR_Generator_FC2-000-05N.xlsx` (named-range
  API, CCN library, TFSMS reconciliation gate, Okinawa adjustments).
- **Cosmetic + structural breakout:** the four rebuilt clean CCN sheets in
  `SW_M29030_CLB4_BFR_2026-NWPCW167400L021.xlsx` (`14345`, `21451`,
  `21455`, `61072`) — see `audit/STYLE_GUIDE.md`.
- **Cell-role palette:** Apex Omega 4-color (input/calc/output/warning)
  overlaid on CLB-4 theme styling — see `audit/STYLE_GUIDE.md` §"Apex
  Omega cell-role palette".

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
