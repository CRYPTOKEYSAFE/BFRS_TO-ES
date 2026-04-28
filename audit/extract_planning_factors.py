"""
Extract per-CCN planning factor tables from FC 2-000-05N Series PDFs.

Source PDFs (must be present in repo root before running):
  fc_2_000_05n_100series_<dateversion>.pdf  (Series 100, current edition
    100.20251210, 10 Dec 2025)
  fc_2_000_05n_200series_<dateversion>.pdf  (Series 200, current edition
    200.20250516, 16 May 2025)

Both PDFs are public WBDG documents at:
  https://www.wbdg.org/FFC/DOD/UFC/fc_2_000_05n_100series_12_10_2025.pdf
  https://www.wbdg.org/FFC/DOD/UFC/fc_2_000_05n_200series_05_16_2025.pdf
WBDG egress is blocked from this sandbox; user supplies via main branch
upload then `git checkout origin/main, file`.

Output:
  audit/PLANNING_FACTORS.yaml , per-CCN planning factor records
  audit/PLANNING_FACTORS.json , same as YAML, machine-readable
  audit/reports/18_planning_factors_extraction.txt , extraction summary

Per-CCN record schema:
  ccn               5-digit, e.g. "14345"
  ccn_display       spaced, e.g. "143 45"
  facility_name     from CCN_VOCABULARY.json
  series            "100" or "200"
  table_id          e.g. "Table 14345-1", "Table 21451-2"
  loading_driver    text, e.g. "PN_MIL", "Number of vehicles"
  uom               "SF", "SY", "AC", "EA"
  factor_value      numeric where stated, else null
  factor_basis      text formula or table reference
  ntg               numeric where stated, else null
  source_page       PDF page number
  source_pdf        filename
  source_date       version date printed on PDF
  notes             free-text caveats, low-confidence flags

Apex Omega Sec. 5.5 timestamping: every record carries source PDF
filename and printed version date. Apex Omega Sec. 5.4 verification:
every numeric factor cited inline with table id and page number.
Low-confidence extractions (ambiguous column boundaries, multi-row
factor tables that span pages) are marked notes="TBD pending review"
per Apex Omega rule 4.

Run:
  python3 audit/extract_planning_factors.py

Status: SCAFFOLD ONLY. Source PDFs not yet supplied. The script exits
non-zero with instructions when either PDF is missing.
"""

from __future__ import annotations

import json
import re
import sys
from collections import OrderedDict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SERIES_PATTERNS = {
    "100": "fc_2_000_05n_100series_*.pdf",
    "200": "fc_2_000_05n_200series_*.pdf",
}
VOCAB_PATH = REPO_ROOT / "audit" / "CCN_VOCABULARY.json"
YAML_OUT = REPO_ROOT / "audit" / "PLANNING_FACTORS.yaml"
JSON_OUT = REPO_ROOT / "audit" / "PLANNING_FACTORS.json"
SUMMARY_OUT = REPO_ROOT / "audit" / "reports" / "18_planning_factors_extraction.txt"

CCN5 = re.compile(r"\b(\d{5})\b")
TABLE_RE = re.compile(r"\bTable\s*(\d{5})\s*-\s*(\d+)", re.IGNORECASE)


def find_pdf(series: str):
    matches = list(REPO_ROOT.glob(SERIES_PATTERNS[series]))
    return matches[0] if matches else None


def load_vocabulary() -> dict:
    if not VOCAB_PATH.exists():
        return {}
    data = json.loads(VOCAB_PATH.read_text())
    return {v["ccn"]: v for v in data["ccns"]}


def vocab_uom(rec: dict) -> str:
    for key in ("uom_area", "uom_other", "uom_alt"):
        v = rec.get(key)
        if v:
            return v.strip("[]")
    return ""


def extract_series(pdf_path: Path, series: str, vocab: dict) -> list:
    """Walk the PDF, find Table NNNNN-N references, capture surrounding
    paragraph text, anchor each table to a CCN, emit a record per
    distinct (ccn, table_id) pair.

    First-pass extraction only. Loading driver, factor value, and NTG
    are populated where the surrounding text states them numerically;
    otherwise marked TBD."""
    try:
        import pdfplumber
    except ImportError:
        sys.exit("FATAL: pdfplumber not installed. pip install pdfplumber")

    records = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_no, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            for m in TABLE_RE.finditer(text):
                ccn = m.group(1)
                table_num = m.group(2)
                start = max(0, m.start() - 240)
                end = min(len(text), m.end() + 360)
                snippet = text[start:end].replace("\n", " ").strip()
                vocab_rec = vocab.get(ccn, {})
                records.append({
                    "ccn": ccn,
                    "ccn_display": f"{ccn[:3]} {ccn[3:]}",
                    "facility_name": vocab_rec.get("title") or "",
                    "series": series,
                    "table_id": f"Table {ccn}-{table_num}",
                    "loading_driver": "TBD pending manual review",
                    "uom": vocab_uom(vocab_rec),
                    "factor_value": None,
                    "factor_basis": snippet[:240],
                    "ntg": None,
                    "source_page": page_no,
                    "source_pdf": pdf_path.name,
                    "source_date": parse_version_from_filename(pdf_path.name),
                    "notes": "TBD pending manual ratification",
                })
    return records


def parse_version_from_filename(fname: str) -> str:
    m = re.search(r"(\d{2})_(\d{2})_(\d{4})", fname)
    if m:
        mm, dd, yyyy = m.groups()
        return f"{yyyy}-{mm}-{dd}"
    return "unknown"


def yaml_escape(s):
    if s is None:
        return "null"
    if isinstance(s, (int, float)):
        return str(s)
    s = str(s).replace("\\", "\\\\").replace('"', '\\"')
    return '"' + s + '"'


def emit_yaml(records, provenance, path):
    lines = [
        "# FC 2-000-05N Planning Factors, extracted from Series 100 and",
        "# Series 200 PDFs. Apex Omega Sec. 5.5 timestamping: each record",
        "# carries source PDF filename and printed version date.",
        "",
        "provenance:",
    ]
    for k, v in provenance.items():
        lines.append(f"  {k}: {yaml_escape(v)}")
    lines.append("")
    lines.append(f"record_count: {len(records)}")
    lines.append("")
    lines.append("factors:")
    for r in records:
        lines.append(f"  - ccn: {yaml_escape(r['ccn'])}")
        for key in ("ccn_display", "facility_name", "series", "table_id",
                    "loading_driver", "uom", "factor_value", "factor_basis",
                    "ntg", "source_page", "source_pdf", "source_date",
                    "notes"):
            lines.append(f"    {key}: {yaml_escape(r.get(key))}")
    path.write_text("\n".join(lines) + "\n")


def emit_json(records, provenance, path):
    path.write_text(json.dumps({"provenance": provenance,
                                "record_count": len(records),
                                "factors": records}, indent=2) + "\n")


def main():
    pdf100 = find_pdf("100")
    pdf200 = find_pdf("200")
    if not pdf100 or not pdf200:
        sys.stderr.write(
            "FC 2-000-05N Series PDFs not found in repo root.\n\n"
            "Expected files (glob patterns):\n"
            f"  Series 100: {SERIES_PATTERNS['100']}\n"
            f"  Series 200: {SERIES_PATTERNS['200']}\n\n"
            "Status currently:\n"
            f"  Series 100 found: {pdf100 if pdf100 else 'NOT FOUND'}\n"
            f"  Series 200 found: {pdf200 if pdf200 else 'NOT FOUND'}\n\n"
            "Both PDFs are public WBDG documents but cannot be retrieved\n"
            "from this sandbox (egress allowlist blocks wbdg.org). User\n"
            "supplies via main-branch upload then 'git checkout origin/main'.\n\n"
            "Source URLs:\n"
            "  https://www.wbdg.org/FFC/DOD/UFC/fc_2_000_05n_100series_12_10_2025.pdf\n"
            "  https://www.wbdg.org/FFC/DOD/UFC/fc_2_000_05n_200series_05_16_2025.pdf\n"
        )
        sys.exit(2)

    vocab = load_vocabulary()
    rec100 = extract_series(pdf100, "100", vocab)
    rec200 = extract_series(pdf200, "200", vocab)
    records = rec100 + rec200

    provenance = OrderedDict([
        ("source_pdf_100", pdf100.name),
        ("source_pdf_200", pdf200.name),
        ("source_date_100", parse_version_from_filename(pdf100.name)),
        ("source_date_200", parse_version_from_filename(pdf200.name)),
        ("authority", "FC 2-000-05N (Marine Corps Basic Facility Requirements)"),
        ("extractor", "audit/extract_planning_factors.py"),
        ("apex_omega_note",
         "First-pass scaffold. Loading driver, factor value, and NTG "
         "are TBD pending manual ratification against the actual table "
         "rows, which a regex-based extractor cannot reliably parse from "
         "multi-column PDF page layouts."),
    ])

    YAML_OUT.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY_OUT.parent.mkdir(parents=True, exist_ok=True)
    emit_yaml(records, provenance, YAML_OUT)
    emit_json(records, provenance, JSON_OUT)

    summary = [
        "FC 2-000-05N Planning Factors Extraction Summary",
        "=" * 56,
        f"Series 100 PDF : {pdf100.name}",
        f"Series 200 PDF : {pdf200.name}",
        f"Total records  : {len(records)}",
        f"From Series 100: {len(rec100)}",
        f"From Series 200: {len(rec200)}",
        "",
        "Distinct CCNs referenced:",
    ]
    distinct = sorted({r["ccn"] for r in records})
    summary.append(f"  count={len(distinct)}")
    summary.append(f"  sample (first 20): {distinct[:20]}")
    SUMMARY_OUT.write_text("\n".join(summary) + "\n")
    print("\n".join(summary))


if __name__ == "__main__":
    main()
