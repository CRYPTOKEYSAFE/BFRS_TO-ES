"""
Extract canonical CCN vocabulary from FC 2-000-05N Appendix A PDF.

Source PDF (committed to repo root): fc_2_000_05n_appendixa.pdf
  Origin: https://www.wbdg.org/FFC/DOD/UFC/fc_2_000_05n_appendixa.pdf
  Document title (cover): "Category Code Report (All Series)"
  Report date printed on every page header: 27-JUN-2019 08:33:51

Apex Omega note (Sec. 5.5): every emitted record carries source filename,
page number, and the document's printed report date. The 27-JUN-2019 stamp
is recorded in the YAML provenance block so consumers know this CCN
catalog is a 2019 Navy Real Property Inventory generation, not the FC
2-000-05N Series 100 (2025-12-10) or Series 200 (2025-05-16) facility-
planning chapters. The CCN dictionary itself is the canonical Navy/USMC
facility-code reference and changes infrequently; planning-factor tables
in the active Series chapters are what advance.

Page layout (verified on pages 1, 11, 51, 101, 151):
  Column anchors (x0, in PDF points; page width 612):
    CATEGORY CODE   ~ 32  (5-digit data; 3-digit prefix headers also at x0 ~32)
    FAC CODE        ~ 85  (4-digit)
    RPA TYPE        ~125  (single/double letter, e.g. B, S, LS)
    UoM AREA        ~150  (bracketed, e.g. [SF], [SY], [AC])
    UoM OTHER       ~190  (e.g. LF)
    UoM ALT         ~220  (rare)
    TITLE           ~248  (free text, may wrap)
    RQMTS RPTG IND  ~357  (Y or N)
    DESCRIPTION     ~374  (free text, multi-line)

  3-digit category-group rows (e.g. "100 OPER & TRNG FAC", "110 AIRFIELD
  PAVEMENTS") are skipped. Series-prefix prose blocks ("Series 111
  Category Codes include criteria for runways...") are also skipped.
"""

import json
import re
import sys
from collections import OrderedDict
from pathlib import Path

import pdfplumber

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_PDF = REPO_ROOT / "fc_2_000_05n_appendixa.pdf"
YAML_OUT = REPO_ROOT / "audit" / "CCN_VOCABULARY.yaml"
CSV_OUT = REPO_ROOT / "audit" / "CCN_VOCABULARY.csv"
JSON_OUT = REPO_ROOT / "audit" / "CCN_VOCABULARY.json"
SUMMARY_OUT = REPO_ROOT / "audit" / "reports" / "15_ccn_vocabulary_extraction.txt"

X_BANDS = {
    "ccn":         (28, 60),
    "fac":         (78, 110),
    "rpa":         (115, 145),
    "uom_area":    (145, 180),
    "uom_other":   (180, 210),
    "uom_alt":     (210, 240),
    "title":       (240, 345),
    "rqmts_ind":   (345, 372),
    "description": (372, 612),
}
ROW_TOL = 2.0
CCN5 = re.compile(r"^\d{5}$")
CAT3 = re.compile(r"^\d{3}$")


def cluster_rows(words):
    rows = OrderedDict()
    for w in words:
        key = round(w["top"] / ROW_TOL) * ROW_TOL
        rows.setdefault(key, []).append(w)
    return [(top, sorted(ws, key=lambda x: x["x0"])) for top, ws in sorted(rows.items())]


def in_band(x0, name):
    lo, hi = X_BANDS[name]
    return lo <= x0 < hi


def words_in_band(ws, name):
    return [w for w in ws if in_band(w["x0"], name)]


def join_words(ws):
    return " ".join(w["text"] for w in ws).strip()


def is_ccn_row(ws):
    return any(CCN5.match(w["text"]) and in_band(w["x0"], "ccn") for w in ws)


def get_ccn(ws):
    for w in ws:
        if CCN5.match(w["text"]) and in_band(w["x0"], "ccn"):
            return w["text"]
    return None


def extract_page(page, pageno):
    """Yield CCN-record dicts for this page."""
    words = page.extract_words(use_text_flow=False, keep_blank_chars=False)
    rows = cluster_rows(words)

    current = None
    for top, ws in rows:
        if is_ccn_row(ws):
            if current is not None:
                yield current
            ccn = get_ccn(ws)
            fac = join_words(words_in_band(ws, "fac"))
            rpa = join_words(words_in_band(ws, "rpa"))
            uom_area = join_words(words_in_band(ws, "uom_area"))
            uom_other = join_words(words_in_band(ws, "uom_other"))
            uom_alt = join_words(words_in_band(ws, "uom_alt"))
            title = join_words(words_in_band(ws, "title"))
            rqmts = join_words(words_in_band(ws, "rqmts_ind"))
            desc = join_words(words_in_band(ws, "description"))
            current = {
                "ccn": ccn,
                "fac_code": fac or None,
                "rpa_type": rpa or None,
                "uom_area": uom_area or None,
                "uom_other": uom_other or None,
                "uom_alt": uom_alt or None,
                "title_parts": [title] if title else [],
                "rqmts_rptg_ind": rqmts or None,
                "description_parts": [desc] if desc else [],
                "page": pageno,
                "top": top,
            }
        elif current is not None:
            cat3 = [w for w in ws if CAT3.match(w["text"]) and in_band(w["x0"], "ccn")]
            if cat3:
                yield current
                current = None
                continue
            title_ext = join_words(words_in_band(ws, "title"))
            desc_ext_words = [w for w in ws if w["x0"] >= X_BANDS["description"][0]]
            desc_ext = join_words(desc_ext_words)
            if title_ext and not desc_ext:
                current["title_parts"].append(title_ext)
            elif desc_ext and not title_ext:
                current["description_parts"].append(desc_ext)
            elif title_ext and desc_ext:
                current["title_parts"].append(title_ext)
                current["description_parts"].append(desc_ext)
    if current is not None:
        yield current


def finalize(rec):
    rec["title"] = " ".join(rec.pop("title_parts")).strip()
    rec["description"] = " ".join(rec.pop("description_parts")).strip()
    rec.pop("top", None)
    return rec


def yaml_escape(s):
    if s is None:
        return "null"
    if isinstance(s, (int, float)):
        return str(s)
    s = str(s)
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def emit_yaml(records, provenance, path):
    lines = ["# FC 2-000-05N Appendix A, Canonical CCN Vocabulary",
             "# Apex Omega Sec. 5.5 timestamping: every entry inherits the source",
             "# document's printed report date; consumers must treat this as the",
             "# 'as-of' date for the underlying NAVFAC P-72 / Real Property",
             "# Inventory CCN catalog snapshot.",
             "",
             "provenance:"]
    for k, v in provenance.items():
        lines.append(f"  {k}: {yaml_escape(v)}")
    lines.append("")
    lines.append(f"ccn_count: {len(records)}")
    lines.append("")
    lines.append("ccns:")
    for r in records:
        lines.append(f"  - ccn: {yaml_escape(r['ccn'])}")
        lines.append(f"    title: {yaml_escape(r['title'])}")
        lines.append(f"    fac_code: {yaml_escape(r['fac_code'])}")
        lines.append(f"    rpa_type: {yaml_escape(r['rpa_type'])}")
        lines.append(f"    uom_area: {yaml_escape(r['uom_area'])}")
        lines.append(f"    uom_other: {yaml_escape(r['uom_other'])}")
        lines.append(f"    uom_alt: {yaml_escape(r['uom_alt'])}")
        lines.append(f"    rqmts_rptg_ind: {yaml_escape(r['rqmts_rptg_ind'])}")
        lines.append(f"    description: {yaml_escape(r['description'])}")
        lines.append(f"    source_page: {r['page']}")
    path.write_text("\n".join(lines) + "\n")


def emit_csv(records, path):
    import csv
    cols = ["ccn", "title", "fac_code", "rpa_type", "uom_area", "uom_other",
            "uom_alt", "rqmts_rptg_ind", "description", "source_page"]
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, quoting=csv.QUOTE_ALL)
        w.writeheader()
        for r in records:
            w.writerow({c: (r.get(c) if r.get(c) is not None else "") for c in cols})


def emit_json(records, provenance, path):
    path.write_text(json.dumps({"provenance": provenance,
                                "ccn_count": len(records),
                                "ccns": records}, indent=2) + "\n")


def main():
    if not SRC_PDF.exists():
        print(f"FATAL: missing {SRC_PDF}", file=sys.stderr)
        sys.exit(2)

    records = []
    series_tally = {}
    with pdfplumber.open(SRC_PDF) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            for raw in extract_page(page, i):
                rec = finalize(raw)
                if not rec["ccn"]:
                    continue
                records.append(rec)
                series_tally[rec["ccn"][:3]] = series_tally.get(rec["ccn"][:3], 0) + 1

    seen = {}
    duplicates = []
    for r in records:
        if r["ccn"] in seen:
            duplicates.append((r["ccn"], r["page"], seen[r["ccn"]]))
        else:
            seen[r["ccn"]] = r["page"]

    provenance = OrderedDict([
        ("source_pdf", "fc_2_000_05n_appendixa.pdf"),
        ("source_url", "https://www.wbdg.org/FFC/DOD/UFC/fc_2_000_05n_appendixa.pdf"),
        ("document_title", "Category Code Report (All Series)"),
        ("source_report_date", "2019-06-27 08:33:51"),
        ("extraction_date", "2026-04-28"),
        ("extractor", "audit/extract_ccn_appendix_a.py"),
        ("apex_omega_note",
         "Source CCN catalog is dated 2019-06-27. Time-stamp at citation per "
         "Apex Omega Sec. 5.5. CCN catalog (NAVFAC P-72 lineage) changes "
         "infrequently; current planning-factor authority is FC 2-000-05N "
         "Series 100 (2025-12-10) and Series 200 (2025-05-16)."),
        ("authority_chain",
         "FC 2-000-05N Appendix A -> NAVFAC P-72 (DON Facility Category Codes)"),
    ])

    YAML_OUT.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY_OUT.parent.mkdir(parents=True, exist_ok=True)
    emit_yaml(records, provenance, YAML_OUT)
    emit_csv(records, CSV_OUT)
    emit_json(records, provenance, JSON_OUT)

    summary_lines = [
        "FC 2-000-05N Appendix A, CCN Vocabulary Extraction Summary",
        "=" * 60,
        f"Source PDF:       fc_2_000_05n_appendixa.pdf",
        f"Source date:      2019-06-27 08:33:51 (printed on every page header)",
        f"Pages processed:  196",
        f"CCNs extracted:   {len(records)}",
        f"Unique CCNs:      {len(seen)}",
        f"Duplicates found: {len(duplicates)}",
        "",
        "By 3-digit series prefix:",
    ]
    for series in sorted(series_tally):
        summary_lines.append(f"  {series}xx  {series_tally[series]:4d}")
    summary_lines.append("")
    if duplicates:
        summary_lines.append("Duplicate CCN occurrences (CCN, page, first-page):")
        for d in duplicates:
            summary_lines.append(f"  {d[0]}  page {d[1]} (first seen page {d[2]})")
    summary_lines.append("")
    summary_lines.append("First 20 records (sanity check):")
    for r in records[:20]:
        title = (r['title'] or '')[:40]
        summary_lines.append(f"  {r['ccn']}  fac={r['fac_code'] or '-':<6}  rpa={r['rpa_type'] or '-':<3}  uom={r['uom_area'] or '-':<6}  {title}")
    summary_lines.append("")
    summary_lines.append("Last 20 records (sanity check):")
    for r in records[-20:]:
        title = (r['title'] or '')[:40]
        summary_lines.append(f"  {r['ccn']}  fac={r['fac_code'] or '-':<6}  rpa={r['rpa_type'] or '-':<3}  uom={r['uom_area'] or '-':<6}  {title}")

    SUMMARY_OUT.write_text("\n".join(summary_lines) + "\n")
    print("\n".join(summary_lines))


if __name__ == "__main__":
    main()
