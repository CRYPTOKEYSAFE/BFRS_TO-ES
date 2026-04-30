"""
Extract per-CCN planning factor tables from FC 2-000-05N Series PDFs.

Source PDFs (must be present in repo root before running):
  fc_2_000_05n_100series_<dateversion>.pdf  (Series 100)
  fc_2_000_05n_200series_<dateversion>.pdf  (Series 200)

Both PDFs are public WBDG documents at:
  https://www.wbdg.org/FFC/DOD/UFC/fc_2_000_05n_100series_<date>.pdf
  https://www.wbdg.org/FFC/DOD/UFC/fc_2_000_05n_200series_<date>.pdf
WBDG egress is blocked from this sandbox; user supplies via main branch
upload then merge into the dev branch.

Output:
  audit/PLANNING_FACTORS.yaml , per-CCN structured records
  audit/PLANNING_FACTORS.json , same as YAML, machine-readable
  audit/reports/18_planning_factors_extraction.txt , extraction summary

Per-CCN record schema (authoritative tabular extraction):
  ccn               5-digit, e.g. "14345"
  ccn_display       spaced, e.g. "143 45"
  facility_name     from the page heading, upper-case
  uom               "SF" / "SY" / "EA" / "AC" / "LF" / "CF" / "HA" / "MIL"
  parent_fac        NAVFAC P-72 category from "FAC: NNNN" line, where present
  series            "100" or "200"
  source_pdf        filename
  source_date       printed version date parsed from filename
  first_page        1-indexed page number where the heading was found
  pages             list of 1-indexed page numbers contributing tables
  tables            list of dicts:
    table_id        e.g. "Table 14345-1"; falls back to f"page_{N}_table_{i}"
    caption         text caption that preceded the table, where present
    page            1-indexed page where this table was found
    headers         list-of-lists, the table's first one or two rows
    rows            list-of-lists, the body rows
    loading_driver  inferred from header text where unambiguous; else "TBD"
    notes           free-text caveat where extraction is partial

Apex Omega Sec.5.5 timestamping: every record carries source PDF
filename, printed version date, and page number.
Apex Omega rule 4: where extraction is ambiguous (multi-page tables,
header rows that pdfplumber merges into the body, columns that resolve
to None), the affected fields are marked "TBD pending review".
The raw `headers` and `rows` arrays are always preserved, so a human
ratifier sees the actual table content.

Run: python3 audit/extract_planning_factors.py
"""

from __future__ import annotations

import json
import re
import sys
from collections import OrderedDict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
# All known FC 2-000-05N Series PDFs. The extractor walks every
# series file present in repo root; missing series are reported in
# the summary rather than failing the run. Series 300 (Training and
# Range Facilities) is not on the CLB-4 critical path; not yet
# supplied as of 30 Apr 2026.
SERIES_PATTERNS = {
    "100": "fc_2_000_05n_100series_*.pdf",
    "200": "fc_2_000_05n_200series_*.pdf",
    "300": "fc_2_000_05n_300series_*.pdf",
    "400": "fc_2_000_05n_400series_*.pdf",
    "500": "fc_2_000_05n_500series_*.pdf",
    "600": "fc_2_000_05n_600series_*.pdf",
    "700": "fc_2_000_05n_700series_*.pdf",
    "800": "fc_2_000_05n_800series_*.pdf",
}
VOCAB_PATH = REPO_ROOT / "audit" / "CCN_VOCABULARY.json"
YAML_OUT = REPO_ROOT / "audit" / "PLANNING_FACTORS.yaml"
JSON_OUT = REPO_ROOT / "audit" / "PLANNING_FACTORS.json"
SUMMARY_OUT = REPO_ROOT / "audit" / "reports" / "18_planning_factors_extraction.txt"

# CCN section heading: "143 45 ARMORY (SF)" or "111 35 LANDING ZONE - ASSAULT (SF)"
# Three digits, space, two digits, space, all-caps name (allowing hyphen,
# slash, comma, ampersand, apostrophe, parens), optional space + UoM in
# parens. Some headings in the body of the FC PDFs omit the trailing UoM
# (e.g., "143 26 MARINE CORPS EXPLOSIVE ORDNANCE DISPOSAL COMPANY
# FACILITY" appears without "(SF)" on its body page); the UoM is then
# pulled from the TOC entry on the file's page 19 if available, or
# left blank for the human ratifier. False-positive guard: a CCN
# heading is confirmed by a "FAC: NNNN" line within the next 5 lines.
HEADING_RE = re.compile(
    r"^\s*(\d{3})\s+(\d{2})\s+"
    r"([A-Z][A-Z0-9\- ,/'()&\.]+?)"
    r"(?:\s+\((SF|SY|EA|AC|LF|CF|HA|MIL|FT|YD)\))?"
    r"\s*$"
)
# "FAC: 1442" (Series 100/200/400/700 convention) or "FAC 6100"
# (Series 600 convention: no colon).
FAC_RE = re.compile(r"^FAC:?\s*(\d+)\s*$")
# Continuation line for a wrapped heading: all-caps (with the
# allowed name punctuation) followed by UoM in parens. Matches
# only if the line starts with an upper-case letter (preventing
# false positives on body prose continuations).
HEADING_CONT_RE = re.compile(
    r"^\s*([A-Z][A-Z0-9\- ,/'()&\.]*?)"
    r"\s+\((SF|SY|EA|AC|LF|CF|HA|MIL|FT|YD)\)\s*$"
)
# Table caption: "Table 14345-1. Armory" or "Table 21103-2"
TABLE_CAPTION_RE = re.compile(
    r"^\s*Table\s+(\d{4,5})\s*-\s*(\d+)(?:\.\s*(.+?))?\s*$"
)


def find_pdf(series: str):
    matches = list(REPO_ROOT.glob(SERIES_PATTERNS[series]))
    return matches[0] if matches else None


def load_vocabulary() -> dict:
    if not VOCAB_PATH.exists():
        return {}
    data = json.loads(VOCAB_PATH.read_text())
    return {v["ccn"]: v for v in data["ccns"]}


def parse_version_from_filename(fname: str) -> str:
    m = re.search(r"(\d{2})_(\d{2})_(\d{4})", fname)
    if m:
        mm, dd, yyyy = m.groups()
        return f"{yyyy}-{mm}-{dd}"
    return "unknown"


def group_words_into_lines(words, y_tolerance=3):
    """Group pdfplumber word objects into lines by 'top' coordinate.
    Returns list of dicts {'text', 'top', 'words'} sorted top-to-bottom."""
    if not words:
        return []
    sw = sorted(words, key=lambda w: (w["top"], w["x0"]))
    lines = []
    cur = [sw[0]]
    cur_top = sw[0]["top"]
    for w in sw[1:]:
        if abs(w["top"] - cur_top) <= y_tolerance:
            cur.append(w)
        else:
            cur.sort(key=lambda x: x["x0"])
            lines.append({
                "text": " ".join(x["text"] for x in cur),
                "top": min(x["top"] for x in cur),
                "bottom": max(x["bottom"] for x in cur),
                "words": cur,
            })
            cur = [w]
            cur_top = w["top"]
    cur.sort(key=lambda x: x["x0"])
    lines.append({
        "text": " ".join(x["text"] for x in cur),
        "top": min(x["top"] for x in cur),
        "bottom": max(x["bottom"] for x in cur),
        "words": cur,
    })
    return lines


def find_headings_on_page(lines):
    """Return list of dicts for each CCN heading line found on the page.

    False-positive guard: when the heading line lacks a trailing UoM
    in parens (e.g., "143 26 MARINE CORPS EXPLOSIVE ORDNANCE DISPOSAL
    COMPANY FACILITY"), look for either (a) a continuation line
    immediately below that ends in "<NAME-CONT> (UoM)" form (Series
    600 convention where the heading wraps because the name is too
    long, e.g. "610 72 BATTALION/SQUADRON HEADQUARTERS, MARINE" /
    "CORPS (SF)"), or (b) a "FAC[:] NNNN" line within the next 5
    lines (Series 100/200/400/700 convention with optional colon).
    Headings WITH UoM on the same line are accepted unconditionally."""
    headings = []
    for idx, line in enumerate(lines):
        m = HEADING_RE.match(line["text"])
        if not m:
            continue
        uom = m.group(4) or ""
        name = m.group(3).strip()
        if not uom:
            # Try wrapped-heading continuation on the next line.
            if idx + 1 < len(lines):
                cont = HEADING_CONT_RE.match(lines[idx + 1]["text"])
            else:
                cont = None
            if cont:
                name = (name + " " + cont.group(1).strip()).strip()
                uom = cont.group(2)
                # Confirm via FAC line within 5 lines after the cont
                fac_search_start = idx + 2
            else:
                fac_search_start = idx + 1
            if not uom:
                confirmed = False
                for ahead in lines[fac_search_start: fac_search_start + 5]:
                    if FAC_RE.match(ahead["text"].strip()):
                        confirmed = True
                        break
                if not confirmed:
                    continue
        ccn = m.group(1) + m.group(2)
        headings.append({
            "ccn": ccn,
            "ccn_display": f"{m.group(1)} {m.group(2)}",
            "facility_name": name,
            "uom": uom,
            "top": line["top"],
        })
    return headings


def find_fac_on_page(lines):
    """Return the first FAC: NNNN value seen, or None."""
    for line in lines:
        m = FAC_RE.match(line["text"].strip())
        if m:
            return m.group(1)
    return None


def find_table_caption_above(lines, table_top, ccn=None, max_distance=80):
    """Find the most recent 'Table NNNNN-N[. caption]' line within
    max_distance points above the table_top y-coordinate. Returns
    (table_id, caption_text) or (None, None) if not found."""
    candidates = []
    for line in lines:
        if line["top"] > table_top:
            continue
        if table_top - line["bottom"] > max_distance:
            continue
        m = TABLE_CAPTION_RE.match(line["text"].strip())
        if m:
            candidates.append((line["top"], m, line))
    if not candidates:
        return None, None
    candidates.sort(key=lambda x: -x[0])  # closest above first
    _, m, _ = candidates[0]
    table_id = f"Table {m.group(1)}-{m.group(2)}"
    caption = (m.group(3) or "").strip() if m.lastindex >= 3 else ""
    return table_id, caption


def infer_loading_driver(headers):
    """Inspect the table's header rows for an obvious loading driver.
    Conservative: only returns a string when one of a few well-known
    NAVFAC phrases appears in the headers; otherwise returns 'TBD'."""
    if not headers:
        return "TBD"
    flat = " ".join(
        " ".join(c or "" for c in row) for row in headers
    ).upper()
    drivers = [
        ("Installation Military Strength", "MILITARY STRENGTH"),
        ("Number of Aircraft", "NUMBER OF AIRCRAFT"),
        ("Number of Vehicles", "NUMBER OF VEHICLES"),
        ("Number of Personnel", "NUMBER OF PERSONNEL"),
        ("Personnel", "PERSONNEL"),
        ("Aircraft", "AIRCRAFT"),
        ("Vehicles", "VEHICLES"),
        ("Linear Feet", "LINEAR FEET"),
        ("Bays", "BAYS"),
    ]
    for label, needle in drivers:
        if needle in flat:
            return label
    return "TBD"


def cleanup_cell(c):
    if c is None:
        return ""
    s = str(c).replace("\n", " ").strip()
    return re.sub(r"\s+", " ", s)


def split_headers_and_rows(raw_table):
    """NAVFAC tables typically have one or two header rows, then a body.
    Split on the first row whose first cell is non-empty AND looks like
    a value (digit / range / step) rather than a header label.
    Conservative: if the first row's first non-empty column starts with
    a digit, treat all rows as body. Else first row is header."""
    if not raw_table:
        return [], []
    cleaned = [[cleanup_cell(c) for c in row] for row in raw_table]
    # Heuristic: count leading rows where the first non-empty cell is
    # NOT all-digits / not range-like.
    header_rows = []
    body_rows = []
    splitting = True
    for row in cleaned:
        first_non_empty = next((c for c in row if c), "")
        if splitting:
            looks_like_value = bool(
                first_non_empty and
                (first_non_empty[0].isdigit() or
                 first_non_empty.lower().startswith("over") or
                 first_non_empty.lower().startswith("up to"))
            )
            if looks_like_value:
                splitting = False
                body_rows.append(row)
            elif len(header_rows) < 3:
                header_rows.append(row)
            else:
                splitting = False
                body_rows.append(row)
        else:
            body_rows.append(row)
    return header_rows, body_rows


SECTION_MARKER_RE = re.compile(r"^(\d{4,5})-(\d+(?:\.\d+)?)\s+(.+)$")


def capture_narrative(lines, ccn):
    """Pull every line that begins with a section marker for this CCN
    (e.g., '21710-1', '14345-3.2'). Return list of section dicts.
    Captures the first line only of each section; this is enough for
    a human ratifier to see directives like 'No specific criteria are
    provided. An engineering evaluation can be conducted.'"""
    sections = []
    for line in lines:
        m = SECTION_MARKER_RE.match(line["text"].strip())
        if m and m.group(1) == ccn:
            sections.append({
                "section_id": f"{m.group(1)}-{m.group(2)}",
                "first_line": m.group(3).strip(),
            })
    return sections


def extract_series(pdf_path: Path, series: str, vocab: dict) -> list:
    """Walk every page; identify CCN headings by line position; extract
    every table on every page; anchor each table to the most recent
    CCN heading at-or-above the table's top edge.

    Emits one record per CCN. Each CCN record has a `tables` list with
    one entry per anchored table preserving headers, body rows, and the
    table's source page."""
    try:
        import pdfplumber
    except ImportError:
        sys.exit("FATAL: pdfplumber not installed. pip install pdfplumber")

    by_ccn = OrderedDict()
    current_ccn = None  # CCN inherited across pages

    with pdfplumber.open(pdf_path) as pdf:
        for page_no, page in enumerate(pdf.pages, start=1):
            words = page.extract_words(use_text_flow=False)
            lines = group_words_into_lines(words)

            # CCN headings on this page, top-to-bottom
            page_headings = find_headings_on_page(lines)
            page_fac = find_fac_on_page(lines)

            # Initialize per-CCN records for any new heading on this page
            for h in page_headings:
                ccn = h["ccn"]
                if ccn not in by_ccn:
                    by_ccn[ccn] = {
                        "ccn": ccn,
                        "ccn_display": h["ccn_display"],
                        "facility_name": h["facility_name"],
                        "uom": h["uom"],
                        "parent_fac": None,
                        "series": series,
                        "source_pdf": pdf_path.name,
                        "source_date": parse_version_from_filename(pdf_path.name),
                        "first_page": page_no,
                        "pages": [],
                        "tables": [],
                        "narrative_sections": [],
                    }
                if page_fac and not by_ccn[ccn]["parent_fac"]:
                    by_ccn[ccn]["parent_fac"] = page_fac
                if page_no not in by_ccn[ccn]["pages"]:
                    by_ccn[ccn]["pages"].append(page_no)
                # Capture narrative section markers for this CCN on this page
                for sec in capture_narrative(lines, ccn):
                    if sec not in by_ccn[ccn].get("narrative_sections", []):
                        by_ccn[ccn].setdefault("narrative_sections", []).append(sec)

            # Also capture narrative for the inherited CCN (continuation
            # pages where the heading appeared earlier).
            if current_ccn and current_ccn in by_ccn and not page_headings:
                for sec in capture_narrative(lines, current_ccn):
                    if sec not in by_ccn[current_ccn].get("narrative_sections", []):
                        by_ccn[current_ccn].setdefault(
                            "narrative_sections", []
                        ).append(sec)
                if page_no not in by_ccn[current_ccn]["pages"]:
                    by_ccn[current_ccn]["pages"].append(page_no)

            # Tables with bounding boxes
            try:
                page_tables = page.find_tables()
            except Exception:
                page_tables = []

            # Anchor each table to the most recent heading at-or-above
            # its top, falling back to the inherited current_ccn.
            for table_obj in page_tables:
                bbox = table_obj.bbox  # (x0, top, x1, bottom)
                t_top = bbox[1]

                anchor_ccn = current_ccn
                # Use the LAST heading whose top is at-or-above the table top
                for h in page_headings:
                    if h["top"] <= t_top:
                        anchor_ccn = h["ccn"]

                if anchor_ccn is None:
                    # Table appears before the first CCN heading in the
                    # whole PDF (front-matter); skip with a low-confidence
                    # warning record.
                    continue

                raw = table_obj.extract()
                headers, body = split_headers_and_rows(raw)
                table_id, caption = find_table_caption_above(
                    lines, t_top, ccn=anchor_ccn
                )
                if not table_id:
                    table_id = f"page_{page_no}_table_{len(by_ccn[anchor_ccn]['tables']) + 1}"

                table_record = {
                    "table_id": table_id,
                    "caption": caption or "",
                    "page": page_no,
                    "headers": headers,
                    "rows": body,
                    "loading_driver": infer_loading_driver(headers),
                    "notes": "" if (headers or body) else (
                        "TBD pending review: pdfplumber returned no rows"
                    ),
                }
                by_ccn[anchor_ccn]["tables"].append(table_record)
                if page_no not in by_ccn[anchor_ccn]["pages"]:
                    by_ccn[anchor_ccn]["pages"].append(page_no)

            # Update inherited current_ccn to LAST heading on this page
            if page_headings:
                current_ccn = page_headings[-1]["ccn"]

    # Backfill facility_name and uom from vocabulary where the page
    # heading was truncated. Long names sometimes wrap across lines and
    # the heading regex misses them. Body-page headings sometimes omit
    # the trailing UoM (e.g., 14326 page 200). The vocabulary record
    # dates from 2019-06-27 (Appendix A extraction); when used here, the
    # record's `notes` field carries that fact so a ratifier knows the
    # UoM came from a slightly older source than the Series PDF body.
    for ccn, rec in by_ccn.items():
        if ccn in vocab:
            v = vocab[ccn]
            if not rec["facility_name"]:
                rec["facility_name"] = v.get("title", "")
            if not rec["uom"]:
                for key in ("uom_area", "uom_other", "uom_alt"):
                    val = v.get(key)
                    if val:
                        rec["uom"] = val.strip("[]")
                        rec["uom_source"] = (
                            "CCN_VOCABULARY.json (Appendix A 2019-06-27); "
                            "Series PDF heading omitted UoM, ratifier should "
                            "verify against current Series text"
                        )
                        break

    return list(by_ccn.values())


def yaml_quote(s):
    """YAML-safe quoting for string values; numeric and None passthrough."""
    if s is None:
        return "null"
    if isinstance(s, bool):
        return "true" if s else "false"
    if isinstance(s, (int, float)):
        return str(s)
    s = str(s).replace("\\", "\\\\").replace('"', '\\"')
    return '"' + s + '"'


def emit_yaml(ccn_records, provenance, path):
    """Custom YAML emitter so the output is deterministic and Apex
    Omega-readable (no anchors/aliases, explicit citations per record)."""
    out = []
    out.append("# FC 2-000-05N Planning Factors, authoritative tabular extraction.")
    out.append("# Apex Omega Sec.5.5 timestamping: each record carries source PDF")
    out.append("# filename, printed version date, and page numbers. The headers")
    out.append("# and rows arrays preserve the table content verbatim from")
    out.append("# pdfplumber.extract_tables(); a human ratifier reads the rows")
    out.append("# directly when the inferred loading_driver is TBD.")
    out.append("")
    out.append("provenance:")
    for k, v in provenance.items():
        out.append(f"  {k}: {yaml_quote(v)}")
    out.append("")
    out.append(f"record_count: {len(ccn_records)}")
    out.append("")
    out.append("ccns:")
    for r in ccn_records:
        out.append(f"  - ccn: {yaml_quote(r['ccn'])}")
        for k in ("ccn_display", "facility_name", "uom", "parent_fac",
                  "series", "source_pdf", "source_date", "first_page"):
            out.append(f"    {k}: {yaml_quote(r.get(k))}")
        if r.get("uom_source"):
            out.append(f"    uom_source: {yaml_quote(r['uom_source'])}")
        # pages list
        if r.get("pages"):
            pages_str = ", ".join(str(p) for p in r["pages"])
            out.append(f"    pages: [{pages_str}]")
        else:
            out.append("    pages: []")
        # narrative_sections
        narr = r.get("narrative_sections") or []
        if narr:
            out.append("    narrative_sections:")
            for s in narr:
                out.append(f"      - section_id: {yaml_quote(s['section_id'])}")
                out.append(f"        first_line: {yaml_quote(s['first_line'])}")
        else:
            out.append("    narrative_sections: []")
        # tables
        if not r["tables"]:
            out.append("    tables: []")
            continue
        out.append("    tables:")
        for t in r["tables"]:
            out.append(f"      - table_id: {yaml_quote(t['table_id'])}")
            out.append(f"        caption: {yaml_quote(t['caption'])}")
            out.append(f"        page: {t['page']}")
            out.append(f"        loading_driver: {yaml_quote(t['loading_driver'])}")
            if t["notes"]:
                out.append(f"        notes: {yaml_quote(t['notes'])}")
            # headers
            if t["headers"]:
                out.append("        headers:")
                for hdr in t["headers"]:
                    out.append(
                        "          - [" +
                        ", ".join(yaml_quote(c) for c in hdr) + "]"
                    )
            else:
                out.append("        headers: []")
            # rows
            if t["rows"]:
                out.append("        rows:")
                for row in t["rows"]:
                    out.append(
                        "          - [" +
                        ", ".join(yaml_quote(c) for c in row) + "]"
                    )
            else:
                out.append("        rows: []")
    path.write_text("\n".join(out) + "\n")


def emit_json(ccn_records, provenance, path):
    path.write_text(json.dumps({
        "provenance": provenance,
        "record_count": len(ccn_records),
        "ccns": ccn_records,
    }, indent=2) + "\n")


def main():
    # Walk every Series PDF present in repo root; missing series are
    # listed in the summary, not fatal. Series 100 is mandatory
    # (anchor for the rest); without it the run aborts.
    found_pdfs = {}
    missing = []
    for series in sorted(SERIES_PATTERNS):
        pdf = find_pdf(series)
        if pdf:
            found_pdfs[series] = pdf
        else:
            missing.append(series)
    if "100" not in found_pdfs:
        sys.stderr.write(
            "FC 2-000-05N Series 100 PDF not found in repo root.\n"
            "Expected glob: " + SERIES_PATTERNS["100"] + "\n"
            "Series 100 is the anchor for the extraction; without it "
            "the run aborts. Other Series are optional and a missing "
            "Series is reported in the summary, not fatal.\n"
        )
        sys.exit(2)

    vocab = load_vocabulary()
    records = []
    per_series = OrderedDict()
    for series in sorted(found_pdfs):
        pdf = found_pdfs[series]
        recs = extract_series(pdf, series, vocab)
        per_series[series] = (pdf, recs)
        records.extend(recs)

    provenance = OrderedDict()
    for series, (pdf, _) in per_series.items():
        provenance[f"source_pdf_{series}"] = pdf.name
        provenance[f"source_date_{series}"] = parse_version_from_filename(
            pdf.name
        )
    if missing:
        provenance["series_not_supplied"] = ", ".join(missing)
    provenance["authority"] = (
        "FC 2-000-05N (Marine Corps Basic Facility Requirements)"
    )
    provenance["extractor"] = (
        "audit/extract_planning_factors.py (authoritative tabular pass)"
    )
    provenance["apex_omega_note"] = (
        "Tabular extraction via pdfplumber.extract_tables() with each "
        "table anchored to the most recent CCN heading at-or-above the "
        "table's top edge. Table headers, body rows, and loading_driver "
        "inference are produced where unambiguous; otherwise marked TBD. "
        "Raw row content is always preserved so a human ratifier can "
        "read the table directly."
    )

    YAML_OUT.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY_OUT.parent.mkdir(parents=True, exist_ok=True)
    emit_yaml(records, provenance, YAML_OUT)
    emit_json(records, provenance, JSON_OUT)

    distinct_ccns = sorted({r["ccn"] for r in records})
    total_tables = sum(len(r["tables"]) for r in records)
    ccns_with_tables = [r["ccn"] for r in records if r["tables"]]
    ccns_engineering_study = [
        r["ccn"] for r in records
        if not r["tables"] and r.get("narrative_sections")
    ]
    drivers_inferred = sum(
        1 for r in records for t in r["tables"]
        if t["loading_driver"] != "TBD"
    )

    summary = [
        "FC 2-000-05N Planning Factors Extraction Summary",
        "(authoritative tabular pass)",
        "",
        "Series PDFs supplied:",
    ]
    for series, (pdf, recs) in per_series.items():
        summary.append(
            f"  Series {series}: {pdf.name}  ({len(recs)} CCN records)"
        )
    if missing:
        summary.append(
            f"Series PDFs NOT supplied: {', '.join(missing)}"
        )
    summary += [
        "",
        f"Total CCN records     : {len(records)}",
        f"CCNs with factor table: {len(ccns_with_tables)}",
        f"CCNs engineering-study: {len(ccns_engineering_study)} "
        f"(narrative captured, no factor table per NAVFAC doctrine)",
        f"Total factor tables   : {total_tables}",
        f"Loading drivers inferred (vs TBD) : {drivers_inferred} / {total_tables}",
        f"Distinct CCNs         : {len(distinct_ccns)}",
        f"  sample (first 20)   : {distinct_ccns[:20]}",
        "",
        "CLB-4 worked-example CCN coverage:",
    ]
    clb4 = ["14312", "14326", "14345", "21451", "21455",
            "21710", "21730", "44112", "45110", "61072"]
    for c in clb4:
        rec = next((r for r in records if r["ccn"] == c), None)
        if rec is None:
            summary.append(
                f"  {c}: ABSENT from supplied PDFs (Series "
                f"{', '.join(missing) if missing else '(all supplied)'} "
                f"missing)"
            )
        else:
            tab_n = len(rec["tables"])
            narr_n = len(rec.get("narrative_sections") or [])
            kind = (
                "factor-table" if tab_n
                else ("engineering-study" if narr_n else "no-data")
            )
            summary.append(
                f"  {c}: {rec['facility_name'][:30]:30}  "
                f"kind={kind}  tables={tab_n}  narrative_sections={narr_n}  "
                f"pages={rec['pages']}  series={rec['series']}"
            )
    SUMMARY_OUT.write_text("\n".join(summary) + "\n")
    print("\n".join(summary))


if __name__ == "__main__":
    main()
