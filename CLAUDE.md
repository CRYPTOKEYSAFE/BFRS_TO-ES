# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Apex Omega, binding methodology

Every output in this session operates under Apex Omega rules.
The full briefing is `APEX_OMEGA.pdf` (root). Read it first. The
non-negotiables are also restated below; if they conflict with anything
else in this file, Apex Omega wins.

1. Facts only. No assumptions, speculation, or AI jargon.
2. Verify line by line, block by block, reference by reference.
   Confirm publication status (date, change page, supersession) of every
   reference before producing a report.
3. Use only current authoritative sources. Older PDFs are never
   treated as current authority without re-verification.
4. If something cannot be verified, omit it or mark `TBD, pending
   [source/action]`. Never guess to fill a gap.
5. Time-stamp external data at the point of citation
   (e.g. *"UFS 3-701-01, current as of 2026-03-27"*).
6. Three-bucket fact separation: (a) regulatory facts, (b)
   program-practice facts, (c) external benchmarks. Do not blend.
7. Numbers must be traceable. Only use numbers explicitly stated in
   a cited source or a user-supplied file.
8. Plain prose only. Lead with the answer. No "let's", no
   "I'll help you", no preamble, no marketing tone, no emojis or
   decorative content.
9. Typography rules. No em dashes (U+2014). No en dashes (U+2013).
   No double hyphen used as em dash. No markdown asterisk bold
   (double-asterisk content double-asterisk). No dash separators
   used for emphasis. Hyphens within identifiers and compound words
   (FC 2-000-05N, MCB Camp Butler, NAVFAC P-72, unit-agnostic) are
   part of the identifier and stay. For emphasis, use sentence
   structure or ALL CAPS sparingly. Markdown bullets that begin a
   line with hyphen-space are allowed as functional list markers.

### Anti-patterns (banned)

- Speculation or invented numbers.
- Stale citations.
- Treating TFSMS exports as authoritative without ASR reconciliation.
- Conflating ERC (Economic Replacement Cost) with PRV (Plant Replacement Value).
- AI-style hedging ("widely believed", "in general", "may be approximately").
- Decorative content in technical deliverables.

### Quality-check rituals (before any deliverable is "done")

1. Back-test against prior signed estimates / actuals where available.
2. Pressure-test current estimates: re-derive from inputs.
3. Confirm publication status of every cited document.
4. Verify references against primary sources, not secondary citations.
5. Recalculate spreadsheets after any change (LibreOffice headless via
   `scripts/recalc.py` or equivalent). Zero `#REF!`, `#DIV/0!`,
   `#NAME?`, `#VALUE!` after recalc, required.
6. Reconciliation gate: TFSMS RecapMCC personnel data must be
   reconciled against the unit's authoritative ASR / T/O&E before any
   BFR can be released.

## What this repository is

The working repository for a USMC Basic Facility Requirements (BFR)
audit and pipeline development effort. The deliverable is an airtight,
unit-agnostic, format-agnostic, state-agnostic data pipeline that ingests
TFSMS / ASR T/O&E source data, in whatever format the unit supplies
it, together with the unit's existing BFR (if any), and produces
a compliant updated BFR workbook per FC 2-000-05N (Series 100,
11 Feb 2026), Marine Corps Basic Facility Requirements (formerly
UFC 2-000-05N / NAVFAC P-80).

CLB-4 (UIC `M29030`, 3d MLG, MCIPAC, MCB Camp Butler / Okinawa) is
the worked example. It is not the only unit; tooling must be
unit-agnostic.

## Input contract, accept any format the unit hands us

A real engagement supplies any combination of:

| Input | Possible formats | Notes |
|---|---|---|
| T/O&E source data | Excel (TFSMS per-company export, Master MEF / TFSMS-style), PDF (TFSMS printable, ASR PDF, other authoritative printout) | Must be ASR-reconciled before driving a BFR (Apex Omega Sec.5.6). PDF ingestion must extract tabular billet/equipment data with citation-grade fidelity (page, table, row). If extraction confidence is low, mark `TBD, pending [page reference]`; never guess values. |
| Existing BFR for the unit | Excel (Format B, BFR-embedded TO/TE) | May be stale, partially correct, or mid-edit. May contain hidden / broken sheets (the CLB-4 SW BFR is the worked example of this state). |
| Project metadata | Manual input (UIC, building number, planner, programmed FY, region) | Goes to the `Cover` sheet via the named-range API. BFRs do not carry a DD 1391; the 1391 is a downstream MILCON project document that may be informed by the BFR's gap analysis but is not part of the BFR itself. |

## Operational modes the pipeline must support

- Update-existing (the common case). Inputs: existing BFR + new
  T/O&E. Output: same BFR with refreshed loading, recalculated
  CCN totals, regenerated summary tabs, repaired lookup contracts,
  and a diff report enumerating every cell that changed (with
  before/after values and traceable cause).
- Generate-new. Inputs: T/O&E only. Output: fresh BFR built
  against the canonical template, cosmetic per `STYLE_GUIDE.md`.
- Audit-existing. Inputs: existing BFR only. Output: forensic
  report (the work product of round 1 on CLB-4 SW lives in
  `audit/FINDINGS.md`) plus a repair plan.

## Definition of done, binding for every deliverable

An updated/generated BFR is not done until all of the following
hold. This is the acceptance test.

1. Cosmetic, matches the CLB-4 four rebuilt clean CCN sheets per
   `audit/STYLE_GUIDE.md` (theme tints, Calibri/Arial fonts, thin
   black borders, merged-cell skeleton, page setup, footer text)
   plus the Apex Omega cell-role palette (input `#FFF8DC`, calc
   `#EAF3F4`, output `#DCE7C8`, warning `#F8E2D6`).
2. Recalc clean, after LibreOffice headless recalc, zero
   `#REF!`, `#DIV/0!`, `#NAME?`, `#VALUE!`, `#N/A` (except where
   `#N/A` is the documented intentional empty-lookup result).
3. Every CCN sheet computes, every CCN sheet's `TOTAL
   REQUIREMENT` cell evaluates to a real number traceable through
   the formula chain back to a TFSMS/ASR input cell or a documented
   FC 2-000-05N planning factor.
4. Roll-up integrity, every CCN's total flows to `UNIT_ROLLUP`
   exactly once. No dropped CCNs (the round-1 finding where 6 hidden
   CCN sheets were excluded from the 14,299 GSF roll-up cannot
   recur). No double counts.
5. All cross-references resolve, named ranges, sheet refs, and
   lookups all point at populated cells. No external links. No
   `#REF!` or `#N/A` in the defined-names list.
6. TFSMS reconciliation gate green, `TFSMS_UNRECONCILED` flag
   is `FALSE`; ASR-reconciled `PN_*` named ranges populated.
7. Personnel summaries populated and accurate, billet
   breakdowns by rank, by MOS, by MCC (the `RecapMCC` / `RecapMOS` /
   `Billet Summary` equivalents). Numbers tie out to source TFSMS
   and to the BFR's own loading inputs.
8. Equipment summaries by CCN populated and accurate, every
   TAMCN line maps to a CCN; counts tie out to source T/E and to
   the CCN sheets that consume them.
9. GSF / GSY totals consistent, every numeric value displayed
   in summary form ties to its detail-tab origin.
10. Audit-traceable, every regulatory or numeric claim cited
    inline with source + section + date (Apex Omega Sec.8.1). Every
    derived number reproducible from inputs visible in the same
    artifact (Apex Omega Sec.8.4).

A deliverable that fails any one of these is `TBD, pending
<failing item>` per Apex Omega rule 4. Never silently release.

Terminology, current correct nomenclature. The installation is
MCB Camp Butler; the Echelon II command is MCIPAC (Marine Corps
Installations Pacific). Do not use "MCBJ" (Marine Corps Base Japan),
"MCBB" (Marine Corps Base Butler), or "COMMARCORBASESJAPAN" as place or
organization terms, those are legacy / pre-MCIPAC and are technically
incorrect. The methodology workbook was originally supplied as
`BFR_Generator_FC2-000-05N.xlsx` and renamed in this repo to
`BFR_Generator_FC2-000-05N.xlsx` per the no-MCBJ rule; the legacy name
appears only in commit history.

## Authoritative documents

- `audit/FINDINGS.md`, Round-1 forensic findings on CLB-4 (which file is
  authoritative, what's broken, what's missing).
- `audit/PIPELINE.md`, Round-2 unit-agnostic pipeline contract spec.
  Defines the six layers that must hold for a BFR to be airtight. Read this
  first.
- `audit/reports/`, All evidence artifacts (sheet inventories, CCN-tab
  dumps, schema maps, probe outputs). Never delete.

## Data files in repository root (inputs, never edit)

| File | Format | Role |
|---|---|---|
| `APEX_OMEGA.pdf` |, | Binding methodology briefing. Always read first. |
| `BFR_Generator_FC2-000-05N.xlsx` |, | Apex Omega methodology reference workbook for BFR work. Implements TFSMS-to-ASR reconciliation gate, `CCN_Library`, Okinawa ACF/SIOH/PD/Contingency adjustments, and named-range API (`PN_OFF`, `PN_ENL`, `PN_TOTAL`, `Okinawa_Navy_ACF`, etc.). |
| `SW_M29030_CLB4_BFR_2026-NWPCW167400L021.xlsx` | B (BFR-embedded TO/TE) | Authoritative CLB-4 BFR, Feb 2026. One observed example unit (there is no gold standard); cosmetic typography is extracted to `STYLE_GUIDE.md`, structural patterns derive from FC 2-000-05N, not from this file. |
| `SW_M29030_CLB4_BFR_2026.xlsx` | B | Earlier sibling, ignore unless diffing |
| `FO_M29030_CLB 4_FINAL BFR.xlsx` | B | STALE (May 2025), do not use |
| `M29111_HQ_CO_CLB-4.xlsx` | A (TFSMS export, per-co) | CLB-4 HQ Co billet+TE roster |
| `M29112_CLC_A_CLB-4.xlsx` | A (TFSMS export, per-co) | CLC A Co roster |
| `M29113_CLC_B_CLB-4.xlsx` | A (TFSMS export, per-co) | CLC B Co roster, openpyxl-touched on upload day; data preserved but flagged |
| `M29114_GS_CO_CLB-4.xlsx` | A (TFSMS export, per-co) | GS Co roster, openpyxl-touched, same caveat |
| `M67400-FO-M13020 3D MED BN-22NOV2024.xlsx` | B | 3d Med Bn benchmark (also problematic; not a clean reference) |
| `2031 Master TO&E v1.1 - 20250411.xlsx` | C (Master MEF, TFSMS-style) | Does not cover CLB-4; covers a different MEF/MLG |
| `E_BFR_F_PRC_BU26-5836R_POM26_20260228_2_OF_2.pdf` |, | POM26 package "2 of 2"; "1 of 2" is missing |
| `Sch1024_Worklist for Unit Brief.xlsx` |, | Unit briefing worklist |

Reference hierarchy when generating BFR output:

- Methodology + math: `BFR_Generator_FC2-000-05N.xlsx` (named-range
  API, CCN library, TFSMS reconciliation gate, Okinawa adjustments).
- Cosmetic + structural breakout: the four rebuilt clean CCN sheets in
  `SW_M29030_CLB4_BFR_2026-NWPCW167400L021.xlsx` (`14345`, `21451`,
  `21455`, `61072`), see `audit/STYLE_GUIDE.md`.
- Cell-role palette: Apex Omega 4-color (input/calc/output/warning)
  overlaid on CLB-4 theme styling, see `audit/STYLE_GUIDE.md` Sec."Apex
  Omega cell-role palette".

## The data pipeline contract (read `audit/PIPELINE.md` for the full spec)

Six layers, every one must hold:

1. Source format awareness, three formats (A: per-co MCTOFD-style; B:
   BFR-embedded; C: Master MEF/MTOMS-T-style).
2. CCN+suffix tagging mechanism, the `NOTE` column in Format B carries
   tags like `21710o`, `44112w`, `14345a`. This is the pipeline spine and
   it is currently unpopulated across every workbook in the repo.
3. Classification rule set, function from
   `(BIC, Billet Description, Alpha Grade, BMOS, PMOS, MCC)` to a NOTE tag.
   Currently undocumented; needs FC 2-000-05N + unit doctrine input.
4. In-workbook TO/TE schema, Format B layout (TO has `LINE | NOTE | CCN
   | CCN Description | UIC | Rec CD | BIC | Billet Description | Alpha Grade
   | BMOS | PMOS | ...`; TE has `ROW | NOTE | CCN | ... | TAMCN | ... | L,Ft |
   W,Ft | H,Ft | Volume Ea | Volume Total`).
5. Stable lookup contracts in CCN sheets, full-column refs
   (`'TO'!$B:$B`), no `IFERROR` masking, named-range constants. Legacy CCN
   sheets violate this with brittle restricted ranges that have all become
   `#REF!`.
6. Validation harness, pass/fail report on schema, NOTE coverage,
   roll-up integrity, billet/equipment accounting. Does not yet exist.

## Cosmetic / structural style guide (binding)

The output BFR must look and tally like the CLB-4 SW BFR , 
specifically the four rebuilt clean CCN sheets:

- `14345` (Armory)
- `21451` (Auto Org Shop)
- `21455` (Vehicle Wash Platform)
- `61072` (BN HQ Admin)

These four are the only clean rebuilds in CLB-4 SW. They are useful
as a cosmetic example (typography is the NAVFAC convention used across
DoD BFRs) but are not a gold standard for structural patterns; there
is no gold standard. Structural / row-level patterns derive from
FC 2-000-05N planning factor tables plus unit doctrine for the unit
type at hand (CLB, MAG, MWHS, MEU, depot, training command, etc.),
not from these four CLB-4 sheets. The hidden broken sheets in the
same workbook (`14312`, `14326`, `21710`, `21730`, `44112`, `45110`)
are 2017 NAVFAC MIDLANT template residue and not a reference at all.

If `audit/STYLE_GUIDE.md` exists, it captures the extracted fills,
fonts, borders, merge patterns, column widths, and page setup of the
four CLB-4 rebuild sheets. The cosmetic/typography spec is binding;
the row-by-row structural shape is illustrative only.

The output must not look "robotic" or arbitrary, match the CLB-4
typography, colors, header banding, and page framing.

## Working conventions

- Never modify the source workbooks. They are inputs. All output goes
  to `audit/` (reports, generated artifacts) or to a clearly-named output
  directory.
- All audit artifacts are committed. Evidence trail matters; don't
  rewrite history of `audit/reports/`.
- Branch policy: development branch is set per session by the
  Claude Code harness (the session-suffixed branch name appears in
  the harness instructions at session start). Push there. Never
  push to `main` without explicit instruction. Do not name a
  specific session-suffix in this file; it goes stale instantly.
- Stop hook in this environment requires committing and pushing
  before stop. Plan accordingly.
- Cosmetic fidelity is not optional. When generating workbooks, match
  the CLB-4 style exactly (see `audit/STYLE_GUIDE.md` if present).
- Math must be airtight. Every formula must be verifiable against
  FC 2-000-05N planning factor tables. Every roll-up must trace.
  No `IFERROR(...,"")` masking allowed at the top level.
- Unit-agnostic. Tools that take a unit identifier or workbook path
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

1. The CLB-4 SW BFR rolls up to 14,299 GSF across only 4 visible CCN
   sheets. Six additional CCN sheets exist in the same workbook, are
   hidden, and are all broken (lookup ranges destroyed, IFERROR masking
   blank values, copy-paste errors like CCN 21730 still searching for
   `21710o`). The 4 working sheets are clean rebuilds that hardcode
   counts; they are the cosmetic reference.
2. The `61072` admin sheet itself documents that 156 of CLB-4's billets
   are excluded from the admin count and require their own facility
   CCNs, exactly the broken-and-hidden ones.
3. Every TO/TE sheet in every workbook is missing the `NOTE` column
   tagging. The pipeline spine is empty.
4. The "Master TO&E" file does not cover CLB-4; CLB-4's source-of-truth
   T/O&E is the four `M2911x` company workbooks.
5. The 3d Med Bn benchmark has its own template-residue and external-link
   problems; it is not a clean reference.
6. All BFR files descend from a single 2017 NAVFAC MIDLANT template
   (Brunson, James J CIV); the accumulated debt is nine years deep.

## What's outstanding (round 3+)

- Layer 2 vocabulary, canonical CCN+suffix tag list per CCN, sourced
  from FC 2-000-05N. Doctrine work; needs SME or PDF extraction.
- Layer 3 classification rules, billet to tag function. Doctrine work.
- Layer 4 ETL tool, Format A/C to Format B. Engineering work.
- Layer 4 canonical BFR template, unit-agnostic, cosmetically matching
  CLB-4. Engineering work.
- Layer 5 stable-lookup CCN sheet templates, one per CCN type.
- Layer 6 validation harness, schema + coverage + roll-up checks.

## Hand-off discipline

When this session approaches its context limit, the user will request an
APEX OMEGA handoff prompt, a structured, dense summary that lets the
next session resume without losing context. Watch for that request and
prepare the prompt rather than starting new work.
