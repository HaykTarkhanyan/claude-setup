# paper-explainer preferences (example)

Copy this file to `preferences.md` in the same folder and edit it. Claude reads `preferences.md` before
every explainer, and its rules override the defaults in SKILL.md. Delete any section you don't need: a
missing section means the default. `preferences.md` is meant to stay personal (it is gitignored in the
claude-setup repo). To keep the real file somewhere backed up, make `preferences.md` one line instead:
`Read <full path to your preferences file>`.

## Reader level

researcher
<!-- researcher (default): technical, outside the paper's subfield. student: still learning the field's
     basics; longer background from first principles, a worked example per new idea, "why this matters"
     after each finding. -->

## Chart colors

<!-- Default: colorblind-safe blue, orange, green, gray for the series, blue / vermillion for the heat map,
     the same in light and dark mode. To use your own, write the rules to paste into the "Preference
     overrides" block at the end of the page's <style>. A plain :root rule applies to both themes; heat
     colors are "R G B" triplets:
:root { --c1: #0072B2; --c2: #E69F00; --c3: #009E73; --c4: #8a8f99; --accent: #E69F00; --link: #0b57d0;
        --heat-good: 34 150 60; --heat-bad: 217 0 18; }
     A color that is too dark for the dark background gets a dark-mode value too, under both selectors
     (the first follows the system setting, the second the page's theme button):
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { --c2: #4573e6; } }
:root[data-theme="dark"] { --c2: #4573e6; }
-->

## Typography

<!-- Default: normal punctuation. To ban em and en dashes and curly quotes (use hyphens, commas and straight
     quotes), write: "No em or en dashes, straight quotes only; run check_html.py with --no-dashes." -->

## Demo seed

42

## Where pages go

<!-- Default: <project>/paper_explainers/<arxiv-id>_<short-slug>.html, facts file next to it. -->

## How to open the page

<!-- Default: the system's default browser (start / open / xdg-open). Example for Chrome on Windows:
     Start-Process chrome "file:///C:/full/path/page.html" -->

## Project files to read for "How it connects to your work"

<!-- Default: README.md and CLAUDE.md, plus proposals or research notes you find. Add your own, e.g.
     "the newest 3 files in notes/sessions/" or "docs/research_questions.md". -->

## When a tool is missing

<!-- Default: use the fallback, say what was skipped, list the tool under "Optional improvements".
     Stricter example: "If Playwright is not connected, stop and ask me to reconnect it instead of
     skipping the browser check." -->
