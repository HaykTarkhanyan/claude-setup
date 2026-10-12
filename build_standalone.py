"""Build claude-codex-workshop-standalone.html from workshop-template.html.

Inlines assets/ images (and the verse beat MP3, from non_essential/make_beat.py)
as base64 data URIs and embeds the woff2 fonts from assets/fonts/ so the output
is fully self-contained (works offline).

Usage: python build_standalone.py    (~1 s on this laptop)
"""
import base64
import logging
import mimetypes
import re
import sys
import time
from pathlib import Path

START = time.perf_counter()

REPO = Path(__file__).parent
TEMPLATE = REPO / "workshop-template.html"
ASSETS = REPO / "assets"
FONTS_DIR = ASSETS / "fonts"
OUT = REPO / "claude-codex-workshop-standalone.html"

Path(REPO / "logs").mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(REPO / "logs" / "build_standalone.log", encoding="utf-8"),
    ],
)
log = logging.getLogger(__name__)

mimetypes.add_type("image/webp", ".webp")
mimetypes.add_type("audio/mpeg", ".mp3")

# family, style, weight, file - latin subsets fetched from Google Fonts
FONT_FACES = [
    ("Instrument Serif", "normal", 400, "instrument-serif-400.woff2"),
    ("Instrument Serif", "italic", 400, "instrument-serif-400italic.woff2"),
    ("IBM Plex Sans", "normal", 400, "plex-sans-400.woff2"),
    ("IBM Plex Sans", "normal", 500, "plex-sans-500.woff2"),
    ("IBM Plex Sans", "normal", 600, "plex-sans-600.woff2"),
    ("IBM Plex Mono", "normal", 400, "plex-mono-400.woff2"),
    ("IBM Plex Mono", "normal", 500, "plex-mono-500.woff2"),
    # armenian subset, variable font: one file covers 400-600 (Plex has no Armenian glyphs)
    ("Noto Sans Armenian", "normal", "400 600", "noto-sans-armenian-armenian.woff2"),
]

html = TEMPLATE.read_text(encoding="utf-8")

if "/*{{FONTS}}*/" not in html:
    log.error("Template missing /*{{FONTS}}*/ placeholder")
    sys.exit(1)
faces = []
for family, style, weight, fname in FONT_FACES:
    path = FONTS_DIR / fname
    if not path.is_file():
        log.error(f"Missing font: {path}")
        sys.exit(1)
    b64 = base64.b64encode(path.read_bytes()).decode("ascii")
    faces.append(
        f"@font-face {{ font-family: '{family}'; font-style: {style}; font-weight: {weight}; "
        f"font-display: swap; src: url(data:font/woff2;base64,{b64}) format('woff2'); }}"
    )
    log.info(f"Embedded font {fname} ({path.stat().st_size / 1024:.0f} KB)")
html = html.replace("/*{{FONTS}}*/", "\n  ".join(faces))

placeholders = re.findall(r"\{\{IMG:([^}]+)\}\}", html)
log.info(f"Found {len(placeholders)} image placeholders")
for name in placeholders:
    path = ASSETS / name
    if not path.is_file():
        log.error(f"Missing asset: {path}")
        sys.exit(1)
    mime, _ = mimetypes.guess_type(str(path))
    if mime is None:
        log.error(f"Unknown MIME type for {path}")
        sys.exit(1)
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    html = html.replace(f"{{{{IMG:{name}}}}}", f"data:{mime};base64,{data}")
    log.info(f"Inlined {name} ({path.stat().st_size / 1024:.0f} KB, {mime})")

leftover = re.findall(r"\{\{[A-Z]+:[^}]*\}\}", html)
if leftover:
    log.error(f"Unreplaced placeholders remain: {leftover}")
    sys.exit(1)

OUT.write_text(html, encoding="utf-8")
log.info(f"Wrote {OUT.name} ({OUT.stat().st_size / 1024 / 1024:.2f} MB) in {time.perf_counter() - START:.2f} s")
