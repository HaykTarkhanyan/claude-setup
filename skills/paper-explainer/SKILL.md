---
name: paper-explainer
description: Turn a research paper (arXiv link or ID, DOI, OpenReview or ACL Anthology link, a local PDF, or just its title) into a plain-language, standalone HTML explainer page. The paper is read in full first, its claims are kept apart from your own critique, it is placed among the papers that came after it, linked to the user's current project, and the page is checked before it opens. Use this whenever the user shares a paper and asks to "create html for", "make an html for", "explain this paper better", says they "don't get it by reading it", or asks for a page, explainer or walkthrough of a paper, even if they don't say "HTML". Not for a quick verbal take in chat ("what's your take?", "what was its point?"): answer that directly.
---

# Paper explainer

Produce one self-contained HTML page that makes a paper understandable to a reader who is technical but could not get it from the paper itself. The page is a teaching document first and a critical review second. Everything on it must be traceable to the paper (or a cited source) or clearly marked as your own analysis.

Do the steps in order; each exists because skipping it produced a real error before.

## 0. Preferences and tools

**Preferences.** If `preferences.md` exists in this skill's folder, read it before anything else: its rules override every default below that is marked *(default)*. If it only points to another file ("Read <path>"), read that file instead; that is how a user keeps the real preferences somewhere backed up. Without it, use the defaults. Don't create the file unasked; `preferences.example.md` lists what can be set (reader level, chart colors, typography, demo seed, where pages go, how to open them, which project files to read, what to do when a tool is missing).

**Tools.** Every tool is optional: when one is missing, use the fallback, say on the page or in the reply what that skipped, and keep going. Never block on a missing tool *(default)*.

| Tool | Used for | If missing |
|---|---|---|
| poppler (`pdftotext`, `pdftoppm`, `pdfinfo`) | full text, page images, zooming into figures | the Read tool on the PDF (or `pypdf`); without page images, mark every value taken from a figure "approx." and skip figure crops |
| OpenAlex MCP (`get_work`, `list_citations`) | citation count, the papers that came after | `scripts/paper_meta.py` (Semantic Scholar, then the OpenAlex REST API, no key needed) |
| Playwright MCP | browser check: charts render, no overflow at phone width | the text checks only; the reply says the page was not browser-checked |
| web search / fetch | venue, code repository, paywalled landing pages | venue from the PDF only; code availability from links in the PDF |

At the end, the reply lists the missing tools once, under "Optional improvements", with one line each on what they would have added (and how to add them, see `README.md`).

**Commands.** Script paths (`scripts/...`, `assets/...`) are relative to this skill's folder, the one holding this SKILL.md: call them by their full path from wherever you work. The commands say `python`; use `python3` where that is the interpreter's name (stock macOS and Linux). In Windows PowerShell 5.1, `curl` is an alias for `Invoke-WebRequest`: write `curl.exe`.

## 1. Get the paper

- **arXiv ID or URL** (new style `2401.12345`, or old style `hep-th/9711200`): download the PDF into the scratchpad (`curl -sSL -o paper.pdf https://arxiv.org/pdf/<id>`). Check first whether the repo already has it (a `papers/` folder, a manifest). Record the version (v1, v2, ...): numbers can change between versions.
- **Only a title** (or a paper with no arXiv ID or DOI, e.g. OpenReview-only): find it by title (OpenAlex MCP `search_works`, or `python <skill folder>/scripts/paper_meta.py --title "<title>"`), and check that the match has the same title, authors and year before using it.
- **DOI:** resolve it (`https://doi.org/<doi>`) and look for an open PDF (arXiv version, author page, OpenAlex `open_access` link). **OpenReview / ACL Anthology:** the PDF link is on the page (`openreview.net/pdf?id=...`, `aclanthology.org/<id>.pdf`).
- **Paywalled with no open copy:** first try the institutional access the user's CLAUDE.md describes (a library proxy prefix or single sign-on in the Playwright browser), if there is any. If that fails too, stop and ask the user for the PDF. Never write the page from the abstract alone.
- **Local PDF:** use it in place.
- Take the title, authors and ID from the PDF itself (`pdfinfo`, first page), not from memory. If an ID resolves to an unrelated paper, say so and find the intended one.
- If the Read tool reports a PDF as "password-protected", don't surface it: `pdftotext` and `pdftoppm` read such files fine.
- **Where the files go** *(default)*: `<project>/paper_explainers/<arxiv-id>_<short-slug>.html` for the page and `<arxiv-id>_<short-slug>_facts.md` next to it (create the folder if needed; outside a project, the current folder; without an arXiv ID, a short slug of the title). Decide this now: step 2 starts writing the facts file. Don't commit unless asked.

## 2. Read all of it, figures included

Shallow reading caused most past mistakes, so this step is the core of the skill.

- Extract the full text (`pdftotext paper.pdf text.txt`). Read the main body completely and the appendix at least for its prose (skim tables, but open the ones the main text leans on).
- Render pages (`pdftoppm -r 100 -png paper.pdf p`) and look at every page with a figure.
- **Zoom into key figures** before quoting numbers from them: `pdftoppm -f N -l N -r 300 -x X -y Y -W W -H H -png paper.pdf crop`. Values read off a plot are approximate: mark them "approx." and keep only the precision you can actually read.
- **Write the facts file as you go** (where: step 1), one line per fact with its location (`Table 3`, `Fig. 5a`, `Appendix B.2`, `p. 7`), plus the paper's version and page count at the top. Every number on the page must come from this file; it is the record that lets anyone check the page.
- Check internal consistency as you go: abstract vs results, text vs figures, counts that don't add up, undefined axes or units, claims the figures don't support. These become the critique.
- **Code and data:** note any repository or dataset links in the paper. If a web fetch is available, check that the repository exists and roughly matches the paper (released code, data, license).

## 3. Venue, citations and what came after

- **Venue:** from the paper itself (first-page footer, "Proceedings of ...", arXiv comments). A later venue is fine to confirm with a quick web check; never guess.
- **Citations and follow-ups, with the OpenAlex MCP:** `get_work` with the DOI (an arXiv paper's DOI is `10.48550/arXiv.<id>`; the published version, if any, has its own record, so check both), then `list_citations` for the papers citing it. Read the titles and abstracts of the most-cited and the most recent ones.
- **Without the MCP:** `python <skill folder>/scripts/paper_meta.py <arxiv-id-or-doi> --citing 8` (or `--title "<title>"` instead of the ID for a paper without one; `arXiv:` prefixes and arxiv.org or doi.org links are accepted). If the user's CLAUDE.md names a Semantic Scholar API key, put it into the environment variable `SEMANTIC_SCHOLAR_API_KEY` for that one command, read straight from the key file (for example `SEMANTIC_SCHOLAR_API_KEY="$(sed -n 's/^SEMANTIC_SCHOLAR_API_KEY=//p' <keys file> | tr -d '\r')" python ...`), so the key never shows up in the command or its output. It prints citation counts (Semantic Scholar, then OpenAlex) and the most-cited citing papers (OpenAlex) as JSON; a title lookup also prints the matched title, so check it is the right paper. The arXiv record usually undercounts: say so when it is the only source. If every source fails, the page says "not available" with the reason, never a guess.
- From the follow-ups, answer on the page: did anyone confirm, extend or contradict the main result? Is the method superseded, and by what? Mark these judgments as yours ("My take") when the follow-up papers don't state them outright. State the source and the date checked.

## 4. Find the link to the user's current work

Read the current project's README and CLAUDE.md *(default; preferences can add more files, such as session logs or proposals)* and any proposal, review or research-idea documents you find. Write a section on how this paper bears on that work: methods to reuse, risks it reveals, experiments it suggests, contrasts with papers the user already knows. Be concrete (file names, research questions, existing results). If the paper is unrelated to the project, or there is no project, keep this to one honest sentence instead of inventing a connection.

## 5. Write the page

Start from `assets/explainer_template.html`. It contains the tested CSS (light and dark themes, collapsible sections, tables, callout boxes, equation, figure and quiz blocks) and the JavaScript helpers (theme toggle, open-section-on-link, `barChart`, `lineChart`, `heat`, a seeded random generator), so you only write content. Copy it, replace every `__PLACEHOLDER__`, and delete the example blocks you don't use.

**Reader level** *(default: researcher)*: a technical reader outside the subfield. With `student` in the preferences, the reader is still learning the field's basics: the background section is longer, starts from first principles, uses one worked example per new idea, and the findings get a "why this matters" line each.

**Sections, in this order** (every section collapsible, all listed in the contents box):

1. **The paper in one minute.** The question, the answers as a short numbered list in plain words, and a one-line "My take" verdict.
2. **Background you need first.** Only what is needed to follow the paper: define each term once, with a schematic SVG diagram where a picture beats prose.
3. **The findings,** one section per main result or experiment: what they did, what they found (exact numbers with table or figure references), and a "My take" box when the evidence is weaker than the claim.
4. **An interactive demo** of the core idea, when a widget can make it tangible (a slider over the key parameter, a switch between the methods compared). Skip it when it would only decorate. Use made-up data from the template's seeded generator *(default seed 42)*, labeled as such.
5. **What came after** (step 3): a table of the follow-up papers that matter, with year, citations and what each one does with this paper (confirms, extends, contradicts, replaces), the date and source checked, and a one-line answer to "is this still the state of the art?".
6. **My critique.** What's good; code and data availability; then a table of problems with evidence and a "How sure" rating (High / Medium / Low).
7. **How it connects to your work** (step 4).
8. **Check yourself.** 3 to 5 questions that test whether the reader understood the core idea (not trivia), each answer hidden in a collapsed block.
9. **Glossary.**
10. **How to read the actual paper:** which pages and figures matter, what to skip on a first read.

At the top, under the title: authors, venue and year, the arXiv ID and version (or the DOI or venue ID), citations with source and date, and an honest reading time ("about 15 min"; roughly 200 words a minute plus a minute per chart or demo).

**Equations.** Show only the formulas the reader needs, each as: the formula (HTML with `<sub>` and `<sup>` in the `.eq` block, no math library), then a table of every symbol (meaning, shape or units), then a worked example with tiny made-up numbers that the reader could redo by hand. A formula without its symbol table is not explained.

**The paper's own figures.** For the 1 to 3 figures that carry the main results, embed a crop of the original figure (`pdftoppm` crop, downscaled, base64 JPEG in the `figure.paperfig` block) next to the explanation, with a caption that says what to look at. This teaches the reader to read the paper's figures, not just your description of them. Your own charts can redraw the same numbers more clearly; say which figure they come from.

**Separating claims from analysis.** The reader relies on this page to know what the paper actually says. Put all of your own analysis (critiques, hypotheses, syntheses across papers, reinterpretations) in "My take" boxes or in sections labeled as yours, with a "How sure" note. Never blend it into the summary of the paper.

**Writing style.**
- Plain English for a smart reader outside the subfield. Define jargon at first use. Short paragraphs, concrete examples, analogies where they genuinely help.
- Numbers exactly as the paper reports them, with their table or figure. Approximate values marked "approx.".
- **Parallel items go in a table or a bullet list, not a paragraph.** When text defines or compares several things of the same kind (metrics, methods, datasets, results with several numbers, steps of a procedure), use a table with one row per item and a column per attribute, or bullets for short items. A paragraph of the form "A: ... B: ... C: ..." is hard to scan. Keep prose for arguments, explanations and the "My take" reasoning. (Learned 2026-10-31: a benchmark explainer defined its five metrics in one dense paragraph.)
- Typography *(default)*: normal punctuation. Preferences can ban em and en dashes and curly quotes; then run the check with `--no-dashes`.

**Visual rules.**
- Bar charts, never pies; value labels on the bars. Series colors come from the CSS variables `--c1` to `--c4` *(default: a colorblind-safe blue, orange, green, gray)*; preferences can set other colors.
- Diverging heat coloring with the median as the pivot for numeric table cells (the `heat` helper does this). Its two colors are `--heat-good` and `--heat-bad` *(default: colorblind-safe blue and vermillion)*; preferences can set others, such as green and red.
- `table-layout: fixed` with a `<colgroup>` for every table, so headers sit over their columns.
- Standalone: no CDN, no external CSS, JS, fonts or images. Inline everything; an embedded image is a downscaled base64 data URI, and the whole page stays under 10 MB.
- SVG text must fit its viewBox; wrap long labels across lines yourself.

**Where it goes:** the path chosen in step 1.

## 6. Check it before opening

- **Text checks:** `python <skill folder>/scripts/check_html.py <page.html>` (add `--no-dashes` if the preferences ban dashes). It fails on external loads, leftover placeholders, broken contents links, sections missing from the contents box, tables without a `<colgroup>`, a page over 10 MB and a missing title. Fix everything it reports.
- **Browser check** (Playwright; it blocks `file://`, so serve the folder):
  1. `python -m http.server 8765 --bind 127.0.0.1` from the folder, in the background.
  2. Open `http://127.0.0.1:8765/<page>.html`; the only acceptable console error is a missing `favicon.ico`.
  3. Confirm with `browser_evaluate` that charts and demos rendered (count their SVG elements) and that interactive controls change the output.
  4. Screenshot every diagram, chart, embedded figure and demo, and look at each one: clipped labels, overlapping text and empty charts are the usual bugs.
  5. Resize to 390 px wide and check there is no horizontal overflow.
  6. Fix, recheck, then close the browser, stop the server, and delete only the screenshots and logs you created.
- Without Playwright: run the text checks, and say in the reply that the page was not browser-checked *(default; preferences may ask you to stop and get it connected instead)*.

## 7. Open and report

- Open the page in the default browser *(default: `Start-Process "<path>"` in Windows PowerShell or `start "" "<path>"` in cmd, `open "<path>"` on macOS, `xdg-open "<path>"` on Linux; preferences can name a browser)*. With a `#section` fragment, use a `file:///` URL: a plain path with `#...` appended makes the browser look for a file of that name.
- Reply briefly: what the paper is (title, authors, venue), where the page and the facts file are, the 3 to 5 most important critiques, what came after it in one line, how deeply you read it (pages, figures, appendix), what the checks verified, and anything you could not verify. End with "Optional improvements" for any missing tools (step 0).
