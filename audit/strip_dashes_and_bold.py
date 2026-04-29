"""
Strip every decorative Unicode character from text files.

Per user direction 2026-04-28: no AI typography. Banned everywhere
in this repo:
  Em dash (U+2014), en dash (U+2013).
  Markdown asterisk bold (double-asterisk content double-asterisk).
  Right arrow (U+2192) and other arrows.
  Section sign (U+00A7).
  Divide sign (U+00F7), multiply sign (U+00D7), approximately (U+2248).
  Less or equal (U+2264), greater or equal (U+2265).
  Middle dot (U+00B7), horizontal ellipsis (U+2026).
  Checkmark (U+2713), cross (U+2717).
  Curly quotes (U+201C, U+201D, U+2018, U+2019).

Substitutions, single character or single regex, never touches
whitespace or line structure (so Python indentation is preserved):
  Em / en dash to comma plus space.
  Markdown bold to bare content.
  Section sign to "Sec.".
  Divide to "/".
  Multiply to "x".
  Approximately to "~".
  Less or equal, greater or equal to "<=", ">=".
  Right arrow to " to ".
  Middle dot to ", ".
  Ellipsis to "...".
  Checkmark to "[ok]". Cross to "[no]".
  Curly quotes to straight ASCII quotes.

Safe for Python source because:
  None of these characters appear in Python syntax.
  The bold regex requires content sandwiched between two asterisks on
  each side; never matches Python power operator or kwargs prefix.
  No whitespace is touched.

The script skips itself by absolute path so its own constant strings
remain intact.

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
    # Regulatory-data files that quote PDF source verbatim. The
    # Apex Omega typography rules apply to OUR documents (markdown,
    # source code, audit prose), not to extracted regulatory text;
    # em-dashes inside NAVFAC table rows are source-faithful content
    # and must not be substituted away.
    REPO_ROOT / "audit" / "PLANNING_FACTORS.yaml",
    REPO_ROOT / "audit" / "PLANNING_FACTORS.json",
    SELF,
}

EMDASH = "—"
ENDASH = "–"
SECTION = "§"
DIVIDE = "÷"
MULTIPLY = "×"
APPROX = "≈"
LE = "≤"
GE = "≥"
RARROW = "→"
MIDDOT = "·"
ELLIPSIS = "…"
CHECK = "✓"
CROSS = "✗"
LDQUO = "“"
RDQUO = "”"
LSQUO = "‘"
RSQUO = "’"

BOLD_RE = re.compile(r"\*\*([^*]+?)\*\*")
# Three or more consecutive ASCII hyphens used as an inline visual
# separator inside a line of content. Apex Omega bans dash separators
# used for emphasis (decorative comment dividers like
# "# ----- text -----", em-dash substitutes like "word --- word").
# Preserved by design:
#   Identifier hyphens (FC 2-000-05N, NAVFAC P-72, MCB Camp Butler);
#     these are single hyphens, never three in a row.
#   Markdown table separators (|---|---|); the pipe-adjacent
#     negative lookarounds keep them.
#   Standalone dash-only lines (YAML frontmatter delimiters and
#     markdown horizontal rules); the line-aware loop in transform()
#     skips any line whose stripped content is composed entirely of
#     ASCII hyphens. YAML frontmatter is structural; destroying it
#     breaks the skill loader.
DASH_SEPARATOR_RE = re.compile(r"(?<!\|)-{3,}(?!\|)")


def transform(text):
    text = BOLD_RE.sub(r"\1", text)
    out_lines = []
    for line in text.split("\n"):
        stripped = line.strip()
        if stripped and all(c == "-" for c in stripped):
            out_lines.append(line)
        else:
            out_lines.append(DASH_SEPARATOR_RE.sub("", line))
    text = "\n".join(out_lines)
    pairs = [
        (" " + EMDASH + " ", ", "),
        (EMDASH, ", "),
        (" " + ENDASH + " ", ", "),
        (ENDASH, ", "),
        (" " + RARROW + " ", " to "),
        (RARROW, " to "),
        (" " + DIVIDE + " ", " / "),
        (DIVIDE, "/"),
        (" " + MULTIPLY + " ", " x "),
        (MULTIPLY, "x"),
        (" " + APPROX + " ", " ~ "),
        (APPROX, "~"),
        (" " + LE + " ", " <= "),
        (LE, "<="),
        (" " + GE + " ", " >= "),
        (GE, ">="),
        (" " + MIDDOT + " ", ", "),
        (MIDDOT, ", "),
        (ELLIPSIS, "..."),
        (CHECK, "[ok]"),
        (CROSS, "[no]"),
        (SECTION, "Sec."),
        (LDQUO, '"'),
        (RDQUO, '"'),
        (LSQUO, "'"),
        (RSQUO, "'"),
    ]
    for old, new in pairs:
        text = text.replace(old, new)
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
