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

## Armenian text (Opus bug)
- Claude Opus has a known bug generating Armenian script - output often corrupts or produces garbage
- When Armenian text is needed: use `[ARM: english description of what to write]` placeholders and let me fill them in, or copy-paste from a source verbatim - but never have the model generate Armenian directly when running on Opus

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

## Programming
- NEVER use silent fallbacks. If something fails, it must fail loudly. No swallowing errors, no default returns on failure, no "if error return empty". Crash or raise AND log at ERROR level - never silently continue.

## General
- Don't over-engineer. Start simple, add complexity only when needed.
- When I ask "is this good?", give a real critique, not validation
