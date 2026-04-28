"""Read internal workbook metadata (created, modified, last_modified_by)
for every xlsx in the repo so we know which is actually the latest version."""
from __future__ import annotations

import sys
from pathlib import Path

from openpyxl import load_workbook


def report(path: Path) -> None:
    wb = load_workbook(filename=str(path), read_only=True, data_only=True)
    p = wb.properties
    print(f"FILE     : {path.name}")
    print(f"  size   : {path.stat().st_size:,} bytes")
    print(f"  created: {p.created}")
    print(f"  modifiy: {p.modified}")
    print(f"  by     : {p.lastModifiedBy!r}")
    print(f"  creator: {p.creator!r}")
    print(f"  title  : {p.title!r}")
    print(f"  subject: {p.subject!r}")
    print(f"  rev    : {p.revision!r}")
    print()


if __name__ == "__main__":
    paths = [Path(a) for a in sys.argv[1:]]
    for p in paths:
        try:
            report(p)
        except Exception as e:  # noqa: BLE001
            print(f"FILE     : {p.name}\n  ERROR  : {e}\n")
