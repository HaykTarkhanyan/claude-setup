"""Text checks for an explainer page before the browser check.

Usage: python check_html.py path/to/page.html
Fails (exit 1) on: em/en dashes or curly quotes in the page text, external script/style/image loads,
leftover __PLACEHOLDERS__, contents links that point at no element, a missing <title>.
Runtime: under a second.
"""
import re
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    html = path.read_text(encoding="utf-8")
    problems = []

    for ch, name in (("—", "em dash"), ("–", "en dash"), ("‘", "curly quote"), ("’", "curly quote"),
                     ("“", "curly quote"), ("”", "curly quote")):
        for m in re.finditer(re.escape(ch), html):
            line = html.count("\n", 0, m.start()) + 1
            problems.append(f"line {line}: {name} '{ch}'")

    for m in re.finditer(r'<(script|link|img|iframe)\b[^>]*\b(src|href)="(https?:)?//[^"]+"', html, flags=re.I):
        line = html.count("\n", 0, m.start()) + 1
        problems.append(f"line {line}: external load: {m.group(0)[:90]}")

    for m in re.finditer(r"__[A-Z][A-Z0-9_]+__", html):
        line = html.count("\n", 0, m.start()) + 1
        problems.append(f"line {line}: leftover placeholder {m.group(0)}")

    ids = set(re.findall(r'\bid="([^"]+)"', html))
    for target in re.findall(r'href="#([^"]+)"', html):
        if target not in ids:
            problems.append(f"contents/internal link to #{target} has no matching id")

    if not re.search(r"<title>[^<]+</title>", html):
        problems.append("missing or empty <title>")

    size_mb = path.stat().st_size / 1e6
    if problems:
        print(f"FAIL {path.name} ({size_mb:.2f} MB): {len(problems)} problem(s)")
        for p in problems[:60]:
            print("  " + p)
        return 1
    print(f"OK {path.name} ({size_mb:.2f} MB): no dashes, curly quotes, external loads, placeholders or dead links")
    return 0


if __name__ == "__main__":
    sys.exit(main())
