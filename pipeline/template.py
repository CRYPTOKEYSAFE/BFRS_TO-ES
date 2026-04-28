"""
Layer 4 canonical BFR template generator (Apex Omega).

Produces a Format-B BFR workbook for any unit, matching the CLB-4 SW
clean-CCN cosmetic spec from audit/STYLE_GUIDE.md plus the Apex Omega
four-color cell-role palette (FFF8DC input, EAF3F4 calc, DCE7C8 output,
F8E2D6 warning). Output is recalc-clean (full-column lookups, no
IFERROR masking) and validator-clean per pipeline/validate.py.

Run:
  python3 pipeline/template.py \\
      --profile <profile.json> \\
      --ccns <ccns.json> \\
      --output <path.xlsx>

Profile JSON schema (all fields required, strings):
  {
    "uic": "M29030",
    "tenant_unit": "CLB 4",
    "installation": "MCB CAMP BUTLER",
    "installation_uic": "M67400",
    "region": "Okinawa, Japan",
    "planning_area": "SW",
    "building_no": "TBD",
    "planner": "TBD",
    "fy": "2026",
    "project_date": "2026-04-28"
  }

CCNs JSON schema (list of objects):
  [
    {
      "ccn": "14345",
      "loading": 310,
      "factor": 1.0,
      "ntg": 1.0,
      "loading_label": "Total Personnel (PN_MIL)",
      "notes": ""
    },
    ...
  ]
  facility_name and uom are looked up from audit/CCN_VOCABULARY.json.

Output workbook layout:
  Sheet 'UNIT_ROLLUP'  : title banner + per-CCN total table.
  Sheet 'TO'           : Format-B header row 6, empty data rows.
  Sheet 'TE'           : Format-B header row 4, empty data rows.
  Sheet '<CCN>'        : one per CCN in --ccns; banner rows 1-7,
                         data rows 8-13, subtotal row 15-16,
                         TOTAL REQUIREMENT cell at H37.

Apex Omega notes:
  Source of CCN dictionary: audit/CCN_VOCABULARY.json (1,059 CCNs from
  FC 2-000-05N Appendix A, 27-JUN-2019 generation).
  This script is read-only against source data and writes only to the
  --output path.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.workbook import Workbook
from openpyxl.workbook.defined_name import DefinedName
from openpyxl.worksheet.page import PageMargins, PrintOptions

REPO_ROOT = Path(__file__).resolve().parent.parent
VOCAB_PATH = REPO_ROOT / "audit" / "CCN_VOCABULARY.json"

INPUT_FILL = PatternFill("solid", fgColor="FFF8DC")
CALC_FILL = PatternFill("solid", fgColor="EAF3F4")
OUTPUT_FILL = PatternFill("solid", fgColor="DCE7C8")
WARNING_FILL = PatternFill("solid", fgColor="F8E2D6")
BANNER_FILL = PatternFill("solid", fgColor="D9D9D9")
SUBHEAD_FILL = PatternFill("solid", fgColor="F2F2F2")

THIN = Side(border_style="thin", color="000000")
BOX = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
TOP_THIN = Border(top=THIN)

TITLE_FONT = Font(name="Calibri", size=16, bold=True)
SECTION_FONT = Font(name="Calibri", size=11, bold=True)
LABEL_FONT_C = Font(name="Calibri", size=11, bold=True)
LABEL_FONT_R = Font(name="Arial", size=10)
COLHEAD_FONT = Font(name="Calibri", size=10, bold=True)
BODY_FONT = Font(name="Calibri", size=10)

CENTER_WRAP = Alignment(horizontal="center", vertical="center", wrap_text=True)
LEFT_WRAP = Alignment(horizontal="left", vertical="center", wrap_text=True)
RIGHT = Alignment(horizontal="right", vertical="center")
CENTER = Alignment(horizontal="center", vertical="center")

FOOTER_TEXT = "&L\r# DISTRIBUTION: DoD COMMUNITY ONLY"


@dataclass
class UnitProfile:
    uic: str
    tenant_unit: str
    installation: str
    installation_uic: str
    region: str
    planning_area: str
    building_no: str
    planner: str
    fy: str
    project_date: str

    @classmethod
    def from_json(cls, path: Path) -> "UnitProfile":
        d = json.loads(path.read_text())
        return cls(**d)


@dataclass
class CcnSpec:
    ccn: str
    loading: float = 0.0
    factor: float = 1.0
    ntg: float = 1.0
    loading_label: str = "Loading driver"
    notes: str = ""
    facility_name: Optional[str] = None
    uom: Optional[str] = None


def load_vocabulary() -> dict:
    if not VOCAB_PATH.exists():
        sys.exit(f"FATAL: missing {VOCAB_PATH}")
    data = json.loads(VOCAB_PATH.read_text())
    return {v["ccn"]: v for v in data["ccns"]}


def vocab_uom(rec: dict) -> str:
    for key in ("uom_area", "uom_other", "uom_alt"):
        v = rec.get(key)
        if v:
            return v.strip("[]")
    return "EA"


def gsf_or_gsy(uom: str) -> str:
    u = (uom or "").upper()
    if u in ("SF", "GSF"):
        return "GSF"
    if u in ("SY", "GSY"):
        return "GSY"
    if u in ("AC",):
        return "AC"
    if u in ("EA", "LF", "LS"):
        return u
    return u or "GSF"


def apply_page_setup(ws):
    ws.page_setup.orientation = ws.ORIENTATION_PORTRAIT
    ws.page_setup.scale = 84
    ws.page_margins = PageMargins(left=0.75, right=0.5, top=0.75,
                                  bottom=0.5, header=0.0, footer=0.3)
    ws.print_options = PrintOptions(horizontalCentered=False,
                                    verticalCentered=False)
    ws.oddFooter.left.text = "\r# DISTRIBUTION: DoD COMMUNITY ONLY"


def set_col_widths(ws):
    ws.column_dimensions["A"].width = 2.8164
    for col in range(2, 33):
        ws.column_dimensions[get_column_letter(col)].width = 8.0
    ws.column_dimensions["AG"].hidden = True
    ws.column_dimensions["AH"].hidden = True
    ws.column_dimensions["AG"].width = 9.18
    ws.column_dimensions["AH"].width = 9.18


def set_row_heights(ws, total_data_row=37):
    heights = {1: 15.75, 2: 15.75, 3: 30.75, 4: 14.5, 5: 15.75,
               6: 28.5, 7: 14.5}
    for r, h in heights.items():
        ws.row_dimensions[r].height = h
    for r in range(8, total_data_row):
        ws.row_dimensions[r].height = 15.75
    for r in (8, 9, 10, 11, 12, 13):
        ws.row_dimensions[r].height = 12.75
    ws.row_dimensions[total_data_row].height = 12.75


def merge_and_set(ws, rng: str, value=None, font=None, fill=None,
                  alignment=None, border=None):
    ws.merge_cells(rng)
    top_left = rng.split(":")[0]
    cell = ws[top_left]
    if value is not None:
        cell.value = value
    if font is not None:
        cell.font = font
    if fill is not None:
        cell.fill = fill
    if alignment is not None:
        cell.alignment = alignment
    if border is not None:
        cell.border = border


def banner_block(ws, profile: UnitProfile, ccn_display: str,
                 facility_name: str):
    merge_and_set(ws, "A1:AF2",
                  value="BASIC FACILITY REQUIREMENTS WORKSHEET",
                  font=TITLE_FONT, alignment=CENTER)
    merge_and_set(ws, "A3:E3", value="Installation:",
                  font=LABEL_FONT_C, alignment=LEFT_WRAP)
    merge_and_set(ws, "F3:L3", value=profile.installation,
                  font=LABEL_FONT_R, alignment=LEFT_WRAP)
    merge_and_set(ws, "M3:Q3", value="Tenant:",
                  font=LABEL_FONT_C, alignment=LEFT_WRAP)
    merge_and_set(ws, "R3:AC3", value=profile.tenant_unit,
                  font=LABEL_FONT_R, alignment=LEFT_WRAP)
    merge_and_set(ws, "AE3:AF3")
    merge_and_set(ws, "A4:E4", value="Installation UIC:",
                  font=LABEL_FONT_C, alignment=LEFT_WRAP)
    merge_and_set(ws, "F4:L4", value=profile.installation_uic,
                  font=LABEL_FONT_R, alignment=LEFT_WRAP)
    merge_and_set(ws, "M4:Q4", value="Tenant UIC:",
                  font=LABEL_FONT_C, alignment=LEFT_WRAP)
    merge_and_set(ws, "R4:X4", value=profile.uic,
                  font=LABEL_FONT_R, alignment=LEFT_WRAP)
    merge_and_set(ws, "Y4:AF4",
                  value=f"Planning Area: {profile.planning_area}",
                  font=LABEL_FONT_C, alignment=LEFT_WRAP)
    merge_and_set(ws, "A5:B5", value="CCN:",
                  font=LABEL_FONT_C, alignment=LEFT_WRAP)
    merge_and_set(ws, "C5:L5", value=ccn_display,
                  font=LABEL_FONT_R, alignment=LEFT_WRAP)
    merge_and_set(ws, "M5:Q5", value="Nomenclature:",
                  font=LABEL_FONT_C, alignment=LEFT_WRAP)
    merge_and_set(ws, "R5:AF5", value=facility_name,
                  font=LABEL_FONT_R, alignment=LEFT_WRAP)
    section_text = (f"SPACE REQUIREMENT ANALYSIS  ,  CCN {ccn_display}  ,  "
                    f"FC 2-000-05N (Series 100, 11 Feb 2026)")
    merge_and_set(ws, "A6:AF6", value=section_text,
                  font=SECTION_FONT, fill=BANNER_FILL,
                  alignment=Alignment(horizontal="left", vertical="center",
                                      wrap_text=True))


def column_headers(ws, label_a7: str, header_v7: str, header_y7: str,
                   header_ab7: str):
    merge_and_set(ws, "A7:U7", value=label_a7,
                  font=SECTION_FONT, fill=SUBHEAD_FILL,
                  alignment=LEFT_WRAP, border=BOX)
    merge_and_set(ws, "V7:X7", value=header_v7,
                  font=COLHEAD_FONT, fill=SUBHEAD_FILL,
                  alignment=CENTER_WRAP, border=BOX)
    merge_and_set(ws, "Y7:AA7", value=header_y7,
                  font=COLHEAD_FONT, fill=SUBHEAD_FILL,
                  alignment=CENTER_WRAP, border=BOX)
    merge_and_set(ws, "AB7:AF7", value=header_ab7,
                  font=COLHEAD_FONT, fill=SUBHEAD_FILL,
                  alignment=CENTER_WRAP, border=BOX)


def data_row(ws, row: int, label: str, factor_val, count_val,
             total_formula: str, count_role: str = "input"):
    merge_and_set(ws, f"A{row}:U{row}", value=label,
                  font=BODY_FONT, alignment=LEFT_WRAP, border=BOX)
    merge_and_set(ws, f"V{row}:X{row}", value=factor_val,
                  font=BODY_FONT, alignment=CENTER, border=BOX,
                  fill=INPUT_FILL)
    merge_and_set(ws, f"Y{row}:AA{row}", value=count_val,
                  font=BODY_FONT, alignment=CENTER, border=BOX,
                  fill=(INPUT_FILL if count_role == "input" else CALC_FILL))
    merge_and_set(ws, f"AB{row}:AF{row}", value=total_formula,
                  font=BODY_FONT, alignment=CENTER, border=BOX,
                  fill=CALC_FILL)


def subtotal_row(ws, row: int, label: str, formula: str):
    merge_and_set(ws, f"A{row}:AA{row}", value=label,
                  font=LABEL_FONT_C, alignment=LEFT_WRAP, border=BOX)
    merge_and_set(ws, f"AB{row}:AF{row}", value=formula,
                  font=BODY_FONT, alignment=CENTER, border=BOX,
                  fill=CALC_FILL)


def total_requirement_row(ws, row: int, value_formula: str, uom_label: str):
    merge_and_set(ws, f"A{row}:G{row}", value="TOTAL REQUIREMENT:",
                  font=LABEL_FONT_C, alignment=Alignment(horizontal="right",
                                                         vertical="center"),
                  border=TOP_THIN)
    merge_and_set(ws, f"H{row}:K{row}", value=value_formula,
                  font=BODY_FONT, alignment=CENTER_WRAP,
                  fill=OUTPUT_FILL, border=BOX)
    fmt = '#,##0\\ "' + gsf_or_gsy(uom_label) + '"'
    ws[f"H{row}"].number_format = fmt
    merge_and_set(ws, f"O{row}:Q{row}", value=gsf_or_gsy(uom_label),
                  font=LABEL_FONT_C, alignment=CENTER, border=TOP_THIN)
    merge_and_set(ws, f"AB{row}:AF{row}", value="",
                  font=LABEL_FONT_C, alignment=Alignment(horizontal="right",
                                                         vertical="center"))


def make_ccn_sheet(wb: Workbook, profile: UnitProfile, spec: CcnSpec):
    ccn_display = f"{spec.ccn[:3]} {spec.ccn[3:]}"
    ws = wb.create_sheet(spec.ccn)
    set_col_widths(ws)
    set_row_heights(ws)
    apply_page_setup(ws)
    ws.print_area = "A1:AF37"

    banner_block(ws, profile, ccn_display, spec.facility_name or "")

    column_headers(
        ws,
        label_a7=f"{spec.facility_name or spec.ccn}  (Loading driver: "
                 f"{spec.loading_label})",
        header_v7="Factor",
        header_y7="Count",
        header_ab7=gsf_or_gsy(spec.uom or ""),
    )

    data_row(ws, 8,
             label=f"Primary loading row",
             factor_val=spec.factor,
             count_val=spec.loading,
             total_formula=f"=V8*Y8*{spec.ntg}",
             count_role="input")
    for r in range(9, 14):
        data_row(ws, r, label="", factor_val="", count_val="",
                 total_formula=f"=V{r}*Y{r}*{spec.ntg}",
                 count_role="input")

    subtotal_row(ws, 15, "Subtotal NSF",
                 f"=SUM(AB8:AF13)")
    subtotal_row(ws, 16, f"Net to Gross multiplier (NTG = {spec.ntg})",
                 f"=AB15*1")

    total_requirement_row(ws, 37,
                          value_formula=f"=AB16",
                          uom_label=spec.uom or "")
    return ws


def make_to_sheet(wb: Workbook, profile: UnitProfile):
    ws = wb.create_sheet("TO")
    apply_page_setup(ws)
    ws.row_dimensions[6].height = 30.0
    headers = ["", "LINE", "NOTE", "CCN", "CCN Description", "UIC",
               "Rec CD", "BIC", "Billet Description", "Alpha Grade",
               "BMOS", "PMOS"]
    for c, val in enumerate(headers, start=1):
        cell = ws.cell(row=6, column=c, value=val)
        cell.font = COLHEAD_FONT
        cell.alignment = CENTER_WRAP
        cell.fill = SUBHEAD_FILL
        cell.border = BOX
    ws.column_dimensions["B"].width = 6
    ws.column_dimensions["C"].width = 9
    ws.column_dimensions["D"].width = 9
    ws.column_dimensions["E"].width = 28
    ws.column_dimensions["F"].width = 9
    ws.column_dimensions["G"].width = 7
    ws.column_dimensions["H"].width = 14
    ws.column_dimensions["I"].width = 30
    ws.column_dimensions["J"].width = 11
    ws.column_dimensions["K"].width = 7
    ws.column_dimensions["L"].width = 7
    return ws


def make_te_sheet(wb: Workbook, profile: UnitProfile):
    ws = wb.create_sheet("TE")
    apply_page_setup(ws)
    ws.row_dimensions[4].height = 30.0
    headers = ["", "ROW", "NOTE", "CCN", "CCN Description",
               "CCN 21451 Equipment Type", "UIC", "TAMCN Short", "TAMCN",
               "Nomenclature", "TAM Stat", "U/I", "Rdy", "Ind Qty",
               "Org Qty", "Unit T/E", "L, Ft", "W, Ft", "H, Ft",
               "Volume Ea", "Volume Total"]
    for c, val in enumerate(headers, start=1):
        cell = ws.cell(row=4, column=c, value=val)
        cell.font = COLHEAD_FONT
        cell.alignment = CENTER_WRAP
        cell.fill = SUBHEAD_FILL
        cell.border = BOX
    return ws


def make_unit_rollup(wb: Workbook, profile: UnitProfile,
                     ccns: List[CcnSpec]):
    ws = wb.create_sheet("UNIT_ROLLUP", 0)
    set_col_widths(ws)
    apply_page_setup(ws)
    merge_and_set(ws, "A1:AF2",
                  value="BASIC FACILITY REQUIREMENTS UNIT ROLLUP",
                  font=TITLE_FONT, alignment=CENTER)
    merge_and_set(ws, "A3:E3", value="Installation:",
                  font=LABEL_FONT_C, alignment=LEFT_WRAP)
    merge_and_set(ws, "F3:L3", value=profile.installation,
                  font=LABEL_FONT_R, alignment=LEFT_WRAP)
    merge_and_set(ws, "M3:Q3", value="Tenant:",
                  font=LABEL_FONT_C, alignment=LEFT_WRAP)
    merge_and_set(ws, "R3:AC3", value=profile.tenant_unit,
                  font=LABEL_FONT_R, alignment=LEFT_WRAP)
    merge_and_set(ws, "A4:E4", value="Installation UIC:",
                  font=LABEL_FONT_C, alignment=LEFT_WRAP)
    merge_and_set(ws, "F4:L4", value=profile.installation_uic,
                  font=LABEL_FONT_R, alignment=LEFT_WRAP)
    merge_and_set(ws, "M4:Q4", value="Tenant UIC:",
                  font=LABEL_FONT_C, alignment=LEFT_WRAP)
    merge_and_set(ws, "R4:X4", value=profile.uic,
                  font=LABEL_FONT_R, alignment=LEFT_WRAP)
    merge_and_set(ws, "Y4:AF4",
                  value=f"Planning Area: {profile.planning_area}",
                  font=LABEL_FONT_C, alignment=LEFT_WRAP)

    headers = ["CCN", "Description", "UM", "Total"]
    base = 8
    for c, val in enumerate(headers, start=2):
        cell = ws.cell(row=base, column=c, value=val)
        cell.font = COLHEAD_FONT
        cell.alignment = CENTER_WRAP
        cell.fill = SUBHEAD_FILL
        cell.border = BOX
    for i, spec in enumerate(ccns):
        r = base + 1 + i
        ccn_display = f"{spec.ccn[:3]} {spec.ccn[3:]}"
        ws.cell(row=r, column=2, value=ccn_display).font = BODY_FONT
        ws.cell(row=r, column=3, value=spec.facility_name).font = BODY_FONT
        ws.cell(row=r, column=4, value=gsf_or_gsy(spec.uom or "")).font = BODY_FONT
        ws.cell(row=r, column=5, value=f"='{spec.ccn}'!H37").font = BODY_FONT
        ws.cell(row=r, column=5).fill = OUTPUT_FILL
        for c in range(2, 6):
            ws.cell(row=r, column=c).border = BOX
            ws.cell(row=r, column=c).alignment = CENTER_WRAP
    total_row = base + 1 + len(ccns) + 1
    ws.cell(row=total_row, column=2, value="GRAND TOTAL").font = LABEL_FONT_C
    ws.cell(row=total_row, column=5,
            value=f"=SUM(E{base+1}:E{base+len(ccns)})").font = LABEL_FONT_C
    ws.cell(row=total_row, column=5).fill = OUTPUT_FILL
    for c in range(2, 6):
        ws.cell(row=total_row, column=c).border = TOP_THIN
    return ws


def build(profile: UnitProfile, ccns: List[CcnSpec]) -> Workbook:
    wb = Workbook()
    wb.remove(wb.active)
    make_unit_rollup(wb, profile, ccns)
    make_to_sheet(wb, profile)
    make_te_sheet(wb, profile)
    for spec in ccns:
        make_ccn_sheet(wb, profile, spec)
    wb.calculation.fullCalcOnLoad = True
    return wb


def hydrate_ccns(raw_specs: list, vocab: dict) -> List[CcnSpec]:
    out = []
    for s in raw_specs:
        ccn = s["ccn"]
        v = vocab.get(ccn, {})
        spec = CcnSpec(
            ccn=ccn,
            loading=float(s.get("loading", 0)),
            factor=float(s.get("factor", 1.0)),
            ntg=float(s.get("ntg", 1.0)),
            loading_label=s.get("loading_label", "Loading driver"),
            notes=s.get("notes", ""),
            facility_name=s.get("facility_name") or v.get("title") or ccn,
            uom=s.get("uom") or vocab_uom(v),
        )
        out.append(spec)
    return out


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--profile", type=Path, required=True)
    ap.add_argument("--ccns", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()

    profile = UnitProfile.from_json(args.profile)
    raw = json.loads(args.ccns.read_text())
    vocab = load_vocabulary()
    ccns = hydrate_ccns(raw, vocab)

    wb = build(profile, ccns)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    wb.save(args.output)
    print(f"Wrote {args.output}")
    print(f"Sheets: {wb.sheetnames}")


if __name__ == "__main__":
    main()
