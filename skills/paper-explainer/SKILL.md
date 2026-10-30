---
name: paper-explainer
description: Turn a research paper (arXiv link or ID, local PDF, or a paper already in the repo) into a plain-language, standalone HTML explainer page that is read in full first, separates the paper's claims from your own critique, links the paper to the user's current project, and is browser-checked before opening. Use this whenever the user shares an arXiv or PDF link and asks to "create html for", "make an html for", "explain this paper better", "make it better explained like before", says they "don't get it by reading it", or asks for a page, explainer or walkthrough of a paper - even if they don't say "HTML". Not for a quick verbal take on a paper in chat ("what's your take?", "what was its point?"), which should just be answered directly.
---

# Paper explainer

Produce one self-contained HTML page that makes a paper understandable to the user, who is technical but was not able to get it from reading the paper itself. The page is a teaching document first and a critical review second. Everything on it must be traceable to the paper or clearly marked as your own analysis.

The workflow has seven steps. Do them in order; each exists because skipping it produced a real error before.

## 1. Get the paper

- **arXiv ID or URL:** download the PDF into the scratchpad (`curl -sSL -o paper.pdf https://arxiv.org/pdf/<id>`). Check first whether the repo already has it (e.g. a `papers/` folder or a manifest).
- **Local PDF:** use it in place.
- Record the arXiv ID, title and authors from the PDF itself (`pdfinfo`, first page), not from memory. If the user gives an ID that resolves to an unrelated paper, say so and find the intended one.
- The Read tool sometimes reports PDFs as "password-protected". Don't surface that; use `pdftotext` and `pdftoppm` (poppler), which read them fine.

## 2. Read all of it, figures included

Shallow reading caused most past mistakes, so this step is the core of the skill.

- Extract the full text: `pdftotext paper.pdf text.txt`. Read the main body completely and the appendix at least for its prose (tables can be skimmed, but open the ones the main text leans on).
- Render pages to images: `pdftoppm -r 100 -png paper.pdf p` and look at every page that has a figure.
- **Zoom into key figures** before quoting numbers from them: `pdftoppm -f N -l N -r 300 -x X -y Y -W W -H H -png paper.pdf crop`. Values read off a plot are approximate; say so on the page ("approx.") and keep them to the precision you can actually read.
- Keep a running fact list with locations (Table 3, Fig. 5a, Appendix B.2). Every number on the page should come from that list.
- Check internal consistency as you go: abstract vs results, text vs figures, counts that don't add up, undefined axes or units, claims that the figures don't support. These become the critique.

## 3. Gather venue and citations

- **Venue:** from the paper itself (first-page footer, "Proceedings of ...", arXiv comments). If a later venue is plausible, a quick web check is fine; never guess.
- **Citations:** run `python scripts/paper_meta.py <arxiv-id-or-doi>` from this skill's folder. It tries Semantic Scholar, then OpenAlex, and prints JSON. State the source and date on the page. OpenAlex counts only the arXiv record and undercounts, so say so if it is the only source. If both fail, the page says "not available (rate-limited)" rather than a guess.

## 4. Find the link to the user's current work

Read the current repo's README, CLAUDE.md, recent `_work_sessions/` and any proposal, review or research-idea documents. Write a section on how this paper bears on that work: methods to reuse, risks it reveals, experiments it suggests, contrasts with papers the user already knows. Be concrete (file names, RQ numbers, existing results). If the paper is genuinely unrelated, keep this to one honest sentence instead of inventing a connection.

## 5. Write the page

Start from `assets/explainer_template.html`. It already contains the tested CSS (light and dark themes, collapsible sections, tables, callout boxes) and the JavaScript helpers (theme toggle, open-section-on-link, `barChart`, `lineChart`, `heat`), so you only write content. Copy it, replace every `__PLACEHOLDER__`, and delete the example blocks you don't use.

**Sections, in this order** (every section collapsible, listed in the contents box):

1. **The paper in one minute.** The question, the answers as a short numbered list in plain words, and a one-line "My take" verdict.
2. **Background you need first.** Only what is needed to follow the paper: define each term once, with a schematic SVG diagram where a picture beats prose (architectures, pipelines, what an operation does).
3. **The findings,** one section per main result or experiment: what they did, what they found (with exact numbers and table/figure references), and a "My take" box when the evidence is weaker than the claim.
4. **An interactive demo** of the paper's core idea, when one exists that a widget can make tangible (e.g. a vote vs prototype readout, clamping vs adding an activation, a model switcher over a figure's curves). Skip it when it would only decorate. Use made-up or seeded data, labeled as such.
5. **My critique.** What's good, then a table of problems with evidence and a "How sure" rating (High / Medium / Low).
6. **How it connects to your work** (step 4).
7. **Glossary.**
8. **How to read the actual paper:** which pages and figures matter, what to skip on a first read.

**Separating claims from analysis.** The user relies on this page to know what the paper actually says. Put all of your own analysis (critiques, hypotheses, syntheses across papers, reinterpretations) in "My take" boxes or in sections labeled as yours, with a "How sure" note. Never blend it into the summary of the paper.

**Writing style.**
- Plain English for a smart reader outside the subfield. Define jargon at first use. Short paragraphs, concrete examples, analogies where they genuinely help.
- No em dashes or en dashes anywhere (use a hyphen, a comma or two sentences); straight quotes only. The user reads these as machine-written.
- Numbers exactly as the paper reports them, with their table or figure. Approximate values marked "approx.".

**Visual rules.**
- Bar charts, never pies; value labels on the bars. With 3 or more colors use red `#D90012`, blue `#0033A0`, orange `#F2A800` (gray for a 4th).
- Diverging green-white-red heat coloring with the median as the pivot for numeric table cells (the `heat` helper does this).
- `table-layout: fixed` with a `<colgroup>` for every table.
- Standalone: no CDN, no external CSS, JS or images. Inline everything; an embedded image is a downscaled base64 data URI.
- SVG text must fit its viewBox; wrap long labels across lines yourself.

**Where it goes.** `<repo>/paper_explainers/<arxiv-id>_<short-slug>.html` (create the folder if needed). If the repo README lists folders in a layout block and `paper_explainers/` isn't there, add one line for it. Don't commit unless asked.

## 6. Check it before opening

- Text checks: `python scripts/check_html.py <page.html>`. It fails on dashes, curly quotes, external loads, leftover placeholders and broken contents links. Fix everything it reports.
- Browser check with Playwright (it blocks `file://`, so serve the folder):
  1. `python -m http.server 8765 --bind 127.0.0.1` from the folder, in the background.
  2. Navigate to `http://127.0.0.1:8765/<page>.html`; the only acceptable console error is the missing `favicon.ico`.
  3. Use `browser_evaluate` to confirm charts and demos rendered (count their SVG elements) and that interactive controls change the output.
  4. Screenshot every diagram, chart and demo (`browser_take_screenshot` with a CSS `target`, saved under `.playwright-mcp/`) and look at each one: clipped labels, overlapping text and empty charts are the usual bugs.
  5. Resize to 390 px wide and check there is no horizontal overflow.
  6. Fix, recheck, then close the browser, stop the server, and delete only the screenshot and log files you created.
- If Playwright is not connected, say so and ask the user to reconnect it (`/mcp`) rather than skipping the check.

## 7. Open and report

- Open with `Start-Process chrome "file:///C:/full/path/page.html"`. Use a `file:///` URL whenever there is a `#section` fragment; a Windows path with `#...` appended makes Chrome look for a file of that name.
- Reply briefly: what the paper is (title, authors, venue), where the page is, the 3-5 most important critiques, how deeply you read it (pages, figures, appendix) and what the checks verified. Mention anything you could not verify (e.g. citations rate-limited).
