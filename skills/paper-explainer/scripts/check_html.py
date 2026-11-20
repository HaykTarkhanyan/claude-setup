"""Text checks for an explainer page before the browser check.

Usage: python check_html.py path/to/page.html [--no-dashes]
Fails (exit 1) on: external loads (script, style, image, font, media, CSS @import, JS module imports),
leftover __PLACEHOLDERS__, internal links that point at no element, a missing contents box, collapsible
sections not listed in it, tables without a <colgroup>, a page over 10 MB, a missing or empty <title> in
<head>. With --no-dashes (a preference) also on em/en dashes and curly quotes, typed or as HTML entities.
Exit 2: wrong arguments, or the file is missing or not UTF-8. Runtime: under a second. Python 3.8+.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

MAX_MB = 10
Q = "[\"']"  # either quote style

# Characters and the HTML entities that produce them, for --no-dashes.
DASHES = {
    "em dash": ("—", "&mdash;", "&#8212;", "&#x2014;"),
    "en dash": ("–", "&ndash;", "&#8211;", "&#x2013;"),
    "curly quote": ("‘", "’", "“", "”", "&lsquo;", "&rsquo;", "&ldquo;", "&rdquo;",
                    "&#8216;", "&#8217;", "&#8220;", "&#8221;", "&#x2018;", "&#x2019;", "&#x201c;", "&#x201d;"),
}


def line_of(html: str, pos: int) -> int:
    return html.count("\n", 0, pos) + 1


def attr_values(tag: str, name: str) -> list[str]:
    """Values of attribute `name` in one tag, double-quoted, single-quoted or bare."""
    pat = rf"(?<![\w:-]){re.escape(name)}\s*=\s*(?:\"([^\"]*)\"|'([^']*)'|([^\s>\"']+))"
    return [a or b or c for a, b, c in re.findall(pat, tag, flags=re.I)]


def has_class(tag: str, cls: str) -> bool:
    return any(cls in v.split() for v in attr_values(tag, "class"))


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")  # page snippets can hold any character; Windows defaults to cp1252
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = {a for a in sys.argv[1:] if a.startswith("--")}
    unknown = flags - {"--no-dashes"}
    if len(args) != 1 or unknown:
        print(__doc__, file=sys.stderr)
        return 2
    path = Path(args[0])
    try:
        raw = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"ERROR: no such file: {path}", file=sys.stderr)
        return 2
    except UnicodeDecodeError as e:
        print(f"ERROR: {path} is not UTF-8 ({e}); save it as UTF-8", file=sys.stderr)
        return 2
    # Structure checks ignore HTML comments (the template keeps example markup in them); blanking them with
    # their newlines keeps the reported line numbers right.
    html = re.sub(r"<!--.*?-->", lambda m: "\n" * m.group(0).count("\n"), raw, flags=re.S)
    problems = []

    if "--no-dashes" in flags:
        for name, forms in DASHES.items():
            for form in forms:
                for m in re.finditer(re.escape(form), html, flags=re.I):
                    problems.append(f"line {line_of(html, m.start())}: {name} '{form}'")

    # External loads. Plain <a href> links are fine (they load nothing); everything else that fetches a URL
    # starting with http(s):// or // is not.
    remote = re.compile(r"^\s*(?:https?:)?//", flags=re.I)
    for m in re.finditer(r"<(?!a\b)([a-z][\w:-]*)\b[^>]*>", html, flags=re.I):
        tag = m.group(0)
        urls = []
        for name in ("src", "href", "xlink:href", "poster", "data", "background"):
            urls += attr_values(tag, name)
        for value in attr_values(tag, "srcset"):
            urls += [part.strip().split(" ")[0] for part in value.split(",")]
        if any(remote.match(u) for u in urls):
            problems.append(f"line {line_of(html, m.start())}: external load: {tag[:90]}")
    for m in re.finditer(rf"@import\b|url\(\s*{Q}?\s*(?:https?:)?//", html, flags=re.I):
        problems.append(f"line {line_of(html, m.start())}: external load in CSS ({m.group(0).strip()[:30]})")
    for m in re.finditer(rf"\bimport\s*(?:\(\s*|[\w*{{}},\s]+\bfrom\s*){Q}\s*(?:https?:)?//", html):
        problems.append(f"line {line_of(html, m.start())}: external JS module import")

    for m in re.finditer(r"__[A-Z][A-Z0-9_]+__", html):
        problems.append(f"line {line_of(html, m.start())}: leftover placeholder {m.group(0)}")

    # id= as a whole attribute name, so data-id= or aria-labelledby= don't count as targets.
    ids = set(re.findall(rf"(?<![\w:-])id\s*=\s*{Q}([^\"']+){Q}", html, flags=re.I))
    for m in re.finditer(rf"(?<![\w:-])href\s*=\s*{Q}#([^\"']+){Q}", html, flags=re.I):
        if m.group(1) not in ids:
            problems.append(f"line {line_of(html, m.start())}: internal link to #{m.group(1)} has no matching id")

    # Only links inside the contents box count for "listed in the contents" (a link from body text doesn't).
    toc_body = None
    for m in re.finditer(r"(<nav\b[^>]*>)(.*?)</nav>", html, flags=re.S | re.I):
        if has_class(m.group(1), "toc"):
            toc_body = m.group(2)
            break
    toc_links = set(re.findall(rf"(?<![\w:-])href\s*=\s*{Q}#([^\"']+){Q}", toc_body or "", flags=re.I))
    if toc_body is None:
        problems.append('no contents box (<nav class="toc">)')
    for m in re.finditer(r"<details\b[^>]*>", html, flags=re.I):
        if not has_class(m.group(0), "sec"):  # "sec" as a whole class name, not "sec-x"
            continue
        sec_ids = attr_values(m.group(0), "id")
        if not sec_ids:
            problems.append(f"line {line_of(html, m.start())}: section without an id (the contents box can't link to it)")
        elif sec_ids[0] not in toc_links:
            problems.append(f"line {line_of(html, m.start())}: section #{sec_ids[0]} is missing from the contents box")

    for m in re.finditer(r"<table\b[^>]*>(.*?)</table>", html, flags=re.S | re.I):
        if not re.search(r"<colgroup\b", m.group(1), flags=re.I):
            problems.append(f"line {line_of(html, m.start())}: table without a <colgroup> (headers drift off their columns)")

    head = re.search(r"<head\b[^>]*>(.*?)</head>", html, flags=re.S | re.I)
    if not (head and re.search(r"<title\b[^>]*>\s*\S[^<]*</title>", head.group(1), flags=re.I)):
        problems.append("missing or empty <title> in <head>")

    size_mb = path.stat().st_size / 1e6
    if size_mb > MAX_MB:
        problems.append(f"page is {size_mb:.1f} MB, over {MAX_MB} MB: downscale the embedded images")

    if problems:
        print(f"FAIL {path.name} ({size_mb:.2f} MB): {len(problems)} problem(s)")
        for p in problems[:60]:
            print("  " + p)
        return 1
    print(f"OK {path.name} ({size_mb:.2f} MB): no external loads, placeholders, dead links, missing sections or bare tables"
          + (", no dashes or curly quotes" if "--no-dashes" in flags else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
