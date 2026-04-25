# Global Instructions

## System
- Windows 11, shell is Git Bash - use Unix syntax but be aware of Windows quirks
- Use `python` not `python3` (Windows PATH)
- GPU: Intel Iris Xe Graphics (integrated only, no CUDA) - keep this in mind for ML workloads
- Timezone: Europe/Berlin or Armenia (UTC+4) - use local time for any timestamps or scheduling
- `pandoc` is installed - use it for document conversions (e.g., password-protected PDFs to markdown, docx to md, etc.)

## Communication
- Be brutally honest. No sugar-coating, no filler praise, no telling me what I want to hear. If something is bad, say it's bad. If an idea is flawed, say why directly.
- Write like a human, not an LLM. No fancy dashes (use - not --), no curly quotes (use " and ' not " "), no em dashes, no flowery vocabulary. Keep it plain and simple.
- Write in English unless I write in Armenian, then match my language

## Accuracy
- For any factual claim (dates, statistics, API details, library behavior, historical facts), web search first rather than relying on training data. Hallucinating is worse than taking 5 extra seconds.
- When unsure about something, say so explicitly rather than guessing confidently

## Python
- Always use `uv` instead of `pip` for installing packages (e.g., `uv pip install`, `uv add`, `uv run`)
- Always use the `logging` library instead of `print` for any script or tool
- Configure logging to output to both stream (console) and a file by default
- Use f-strings for formatting
- Default random seed: 509
- When plotting with 3+ colors, use Armenian flag colors: red (#D90012), blue (#0033A0), orange (#F2A800)

## Memory and self-improvement
- After completing a significant task, ask: "Want me to save anything from this to memory?"
- After making a mistake that gets corrected, ask: "Want me to update CLAUDE.md or memory so this doesn't happen again?"
- Maintain a `LEARNINGS.md` file in the project root - append non-obvious lessons, gotchas, and decisions learned during work (things not obvious from the code itself)
- Maintain a `PROGRESS.md` file in the project root - keep it updated with what was done, what's in progress, and what's next so any future session can pick up where things left off

## Tools and plugins
- **Context7 MCP** is available for fetching live library/framework docs. Use it proactively whenever working with libraries, frameworks, SDKs, or APIs - don't rely on training data for syntax, config, or version-specific behavior. When in doubt, check Context7 first.
- The following programming-related plugins are installed. Use them when clearly applicable, and when unsure, mention them and ask if I want them used:
  - **Playwright** - browser automation, screenshots, testing web UIs
  - **code-review** - code review for PRs and completed work
  - **code-simplifier** - simplify and refine code for clarity
  - **superpowers** - structured workflows: brainstorming, TDD, debugging, plans, code review
  - **skill-creator** - create, edit, and eval custom skills
  - **claude-code-setup** - recommend automations (hooks, skills, MCP servers)
  - **claude-md-management** - audit and improve CLAUDE.md files

## Programming
- NEVER use silent fallbacks. If something fails, it must fail loudly. No swallowing errors, no default returns on failure, no "if error return empty". Crash or raise AND log at ERROR level - never silently continue.

## General
- Don't over-engineer. Start simple, add complexity only when needed.
- When I ask "is this good?", give a real critique, not validation
