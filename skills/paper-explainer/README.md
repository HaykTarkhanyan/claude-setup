# paper-explainer

A Claude skill that turns a research paper into one self-contained HTML page you can actually learn from:
the paper in one minute, the background you need, every finding with its exact numbers, the paper's key
figures, equations with a symbol table and a worked example, what came after it (follow-ups, replications,
is it superseded?), an honest critique kept apart from what the paper says, how it connects to your
project, and a short "check yourself" quiz. Every number on the page comes from a facts file that says
where in the paper it is.

Say something like "make an explainer page for arXiv 2401.12345" or "I don't get this paper, explain it:
<link>". It takes arXiv IDs and links, DOIs, OpenReview and ACL Anthology links, local PDFs, and plain titles
(it finds the paper and checks the match).

## Install (Claude Code)

```bash
# macOS / Linux
git clone https://github.com/HaykTarkhanyan/claude-setup.git
mkdir -p ~/.claude/skills
cp -r claude-setup/skills/paper-explainer ~/.claude/skills/
```

```powershell
# Windows (PowerShell)
git clone https://github.com/HaykTarkhanyan/claude-setup.git
New-Item -ItemType Directory -Force "$HOME\.claude\skills" | Out-Null
Copy-Item -Recurse -Force claude-setup\skills\paper-explainer "$HOME\.claude\skills\"
```

Create the `skills` folder first, as above: if it doesn't exist yet, the copy would put the files straight
into `skills/` instead of `skills/paper-explainer/`, and Claude Code wouldn't find the skill.

Restart Claude Code; the skill shows up in the skills list. To update later: `git pull` and run the same
copy command again (`-Force` overwrites the old files). Your `preferences.md` is not in the repo, so the
copy leaves it alone.

The scripts need Python 3.8 or newer and no packages (`python3` on macOS and Linux).

In the Claude apps with Skills enabled you can also upload the folder as a .zip; the scripts and the
browser check need a machine with Python, so the full workflow runs best in Claude Code.

## Optional tools (nothing breaks without them)

| Tool | What it adds | Install |
|---|---|---|
| poppler | exact text, page images, zooming into figures for precise numbers | Windows: `winget install oschwartz10612.Poppler`; macOS: `brew install poppler`; Linux: `sudo apt install poppler-utils` |
| OpenAlex MCP | reliable citation counts and the "What came after" papers | `claude mcp add --transport http openalex https://mcp.openalex.org/mcp`, then log in with `/mcp` (free daily allowance) |
| Playwright MCP | a real browser check: charts render, no overflow on a phone | `claude mcp add playwright npx @playwright/mcp@latest` |

Without them the skill uses fallbacks (the PDF reader, a keyless citation script, text-only checks) and
lists what you could add at the end of its reply.

## Make it yours

Copy `preferences.example.md` to `preferences.md` in the same folder and edit it: reader level (`student`
gives more background and a worked example per new idea), chart and heat-map colors, typography, the demo's
random seed, where pages go, how to open them, which project files to read, and what to do when a tool is
missing. Anything you leave out keeps
the default. To keep your preferences in a backed-up place (a notes repo, say), put them there and make
`preferences.md` a single line: `Read <full path to your file>`.

## Files

- `SKILL.md`: the workflow Claude follows (read in full, facts file, citations and follow-ups, link to your work, write, check, open).
- `assets/explainer_template.html`: the page template with light and dark themes, charts, equation, figure and quiz blocks.
- `scripts/check_html.py`: text checks before opening (external loads, placeholders, dead links, tables, size).
- `scripts/paper_meta.py`: citation counts and citing papers without any API key, the fallback for OpenAlex.
- `preferences.example.md`: what you can customize.
