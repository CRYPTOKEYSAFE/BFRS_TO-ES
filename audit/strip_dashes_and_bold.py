"""
Strip em dashes, en dashes, and markdown bold from text files.

Per user direction 2026-04-28: no AI jargon typography. Em dashes,
en dashes, and asterisk bold are forbidden everywhere in this repo.

Substitutions, single character or single regex, never touches
whitespace or line structure:
  Em dash U+2014 to comma plus space.
  En dash U+2013 to comma plus space.
  Markdown bold double asterisk content double asterisk to bare content.

Safe for Python source files because:
  Em and en dash characters never appear in Python syntax.
  The bold regex requires two asterisks then content then two asterisks,
  which does not match Python power operator (single asterisk pairs)
  or keyword expansion (single double-asterisk prefix).

The script skips itself by file path so its own constants stay intact.

Run: python3 audit/strip_dashes_and_bold.py
"""

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SELF = Path(__file__).resolve()

INCLUDE_EXT = {".md", ".py", ".txt", ".yaml"}
SKIP_PATHS = {
    REPO_ROOT / ".git",
    REPO_ROOT / "audit" / "CCN_VOCABULARY.csv",
    REPO_ROOT / "audit" / "CCN_VOCABULARY.json",
    SELF,
}

EMDASH = "—"
ENDASH = "–"
BOLD_RE = re.compile(r"\*\*([^*]+?)\*\*")


def transform(text):
    text = BOLD_RE.sub(r"\1", text)
    text = text.replace(" " + EMDASH + " ", ", ")
    text = text.replace(EMDASH, ", ")
    text = text.replace(" " + ENDASH + " ", ", ")
    text = text.replace(ENDASH, ", ")
    return text


def main():
    changed = []
    for p in REPO_ROOT.rglob("*"):
        if not p.is_file():
            continue
        rp = p.resolve()
        if rp == SELF:
            continue
        if any(str(rp).startswith(str(skip)) for skip in SKIP_PATHS):
            continue
        if p.suffix not in INCLUDE_EXT:
            continue
        try:
            original = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, IsADirectoryError):
            continue
        new = transform(original)
        if new != original:
            p.write_text(new, encoding="utf-8")
            changed.append(p.relative_to(REPO_ROOT))
    print(f"Files changed: {len(changed)}")
    for c in changed:
        print(f"  {c}")


if __name__ == "__main__":
    main()
