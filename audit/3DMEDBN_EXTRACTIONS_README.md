# 3d MED BN BFR, consolidated extractions workbook

File: `audit/3DMEDBN_EXTRACTIONS.xlsx`
Generated: 2026-05-05 on `claude/resume-bfr-pipeline-nrRNC`
Methodology: Apex Omega. No invented numbers. Every cell traceable
to a source file or report cited in the same workbook.

## What this file is

A single workbook that consolidates every distinct data extraction
that the BFR repair effort has produced for 3d MED BN. The original
extractions live in scattered Excel files, JSON, and text reports
under `audit/`. This workbook brings them together with a README
tab so a reviewer can see, in one place, what was pulled, where it
came from, and why.

This is read-only reference material. It does not replace any
source artifact and it is not part of the live BFR pipeline. The
authoritative inputs remain the source workbooks and PDFs in the
repository root.

## Tab inventory

| Tab | Source | What it carries |
|---|---|---|
| README | this document | Cover, tab inventory, file usage notes |
| AMAL_Locator_Deck | BFR sheet `Locator_Deck`, pre-Phase-B-2 | 608-row AMAL container manifest, originally embedded in the BFR; extracted out in commit 840bfc2 because Apex Omega scopes the BFR to facility-driver data only |
| Phase_C_Retag_Summary | Phase C diff logs 20-23 | 175-action consolidated retag/add/document summary across all four sub-buckets |
| Personnel_Reconciliation | audit report 19 | BFR TO vs TFSMS exports vs ASR vs CG signed letter |
| TFSMS_COE_3_Missing | M28262/M28263 COE sheets | The 3 TFSMS COE TAMCNs and their disposition (added, absent, TBD) |
| CCN_Library_used | BFR `CCN_Library` sheet | The 10 CCNs the BFR's own sheets reference, sourced from FC 2-000-05N |
| FC_References | repo PDFs | The 8 FC 2-000-05N series PDFs and the CCN sections cited in Phase C |
| Source_Workbooks | repo files | Inventory of every source file consulted in Phase A/B/C |

## Why each extraction matters

### AMAL Locator Deck (608 rows)
The Locator_Deck is the unit's AMAL/AAL/ADAL inventory record:
which container holds which TAMCN. It was embedded in the BFR
because the original 2nd Med Bn Camp Lejeune template (lineage
recorded in commit 173eb3b) carried it. Per FC 2-000-05N a BFR
captures facility space requirements, not container-level
inventory. We extracted the manifest to preserve it for ops use,
then removed the sheet from the BFR. The extraction lives at
`audit/reports/3dmedbn/locator_deck_extract.xlsx` and is replicated
in this workbook for convenience.

### Phase C retag summary (175 actions)
The single largest data-hygiene action set in the repair. Each row
documents one cell-value change in BFR TE column D, with before,
after, and the FC 2-000-05N source citation that justifies the
change. Reviewers can audit any retag decision without having to
walk the four separate Phase C diff logs.

### Personnel reconciliation
Resolves the spread between the four authoritative personnel
sources (BFR TO, TFSMS, ASR, CG signed letter) that the project
encountered. User direction 2026-05-05 made 711 (CG signed letter)
the canonical planning total, with 609 ASR footnoted as Marine BIC
structure only.

### TFSMS COE 3 missing
The Phase B equipment reconciliation found 96.4 percent TFSMS COE
coverage, with 3 TAMCNs per surgical company missing from the BFR
TE. This tab captures the disposition of each: 1 added, 1 documented
as correctly absent, 1 held TBD.

### CCN_Library, FC_References, Source_Workbooks
Reference material so a reviewer can connect any datum in the BFR
back to its FC source PDF, the originating workbook, and the role
that workbook played.

## How to use

Open the workbook in Excel or LibreOffice and start at the README
tab. Every other tab carries its own provenance line near the top.
For deeper detail than the consolidated tab carries, the audit
reports under `audit/reports/3dmedbn/` (numbered 01 through 23)
hold the raw forensic dumps.

## What this file is not

It is not the BFR. The live BFR remains
`M67400-FO-M13020 3D MED BN-22NOV2024.xlsx` in the repo root.

It is not the pipeline. Pipeline contracts and validation harness
live under `pipeline/` and `audit/PIPELINE.md`.

It is not authoritative for any input data. If a number in this
workbook differs from the source file cited on the same tab, the
source file wins. This file is a convenience consolidation, not a
new authoritative artifact.
