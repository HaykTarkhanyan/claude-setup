# Claude Code Workshop - Outline

**Audience:** Developers who already use coding agents. Goal is to deepen, not introduce.

---

## 1. Why CLI Over UI
- Better control: permission modes, piping, headless mode
- Automatic reasoning level selection (model picks thinking depth)
- Full transcripts - see exactly what Claude did and why
- Background agents (`Ctrl+B`) - dispatch work and keep going
- Voice mode, remote control (`/rc`), session naming
- See `cli/commands.md` for full shortcut/command reference

## 2. ccstatusline - Know Your Context
- Why context matters: Claude degrades well before 100% full
- The ~50% rule
- **Demo screenshot:** `assets/nice_status_line.png`
  - Line 1: Ctx%, git branch, staged changes
  - Line 2: session time, session cost%, token rate, reset timer, weekly usage
  - Permission mode indicator
- `/clear` vs `/compact` vs fresh session - when to use which
- `/btw` for cheap side questions (reuses prompt cache)

## 3. Project Setup - Teaching Claude Your Codebase
- **CLAUDE.md** - project-level instructions (under 200 lines, what Claude can't guess)
- **`.claude/rules/*.md`** - path-specific rules (load only when relevant files touched)
- Settings hierarchy: global > project > local
- Memory system - persistent across conversations
- **`/claude-automation-recommender`** - plugin that scans your codebase and suggests what to set up (hooks, skills, MCPs)
- See `global/CLAUDE.md` for a real example

## 4. Hooks - Automating Safety & Workflows
- What hooks are: shell scripts triggered by Claude Code lifecycle events
- **PreToolUse** - block dangerous actions (git push, secret file edits, Gmail writes)
- **PostToolUse** - auto-lint, auto-upload, auto-format after edits
- **SessionStart** - orientation briefing (git status, open PRs, reminders)
- **PostCompact** - re-inject critical rules after context compression
- **Notification** - Windows/macOS toast when Claude needs attention
- See `hooks/` folder for live examples

## 5. Skills - Reusable Workflows as Code
- What skills are: markdown files in `.claude/skills/` that define multi-step workflows
- Invoked with `/skill-name` or auto-triggered by description match
- When to build a skill: you've done something 3+ times
- Skill anatomy: frontmatter (name, description, allowed-tools) + step-by-step instructions
- See `skills/` folder for examples (morning, ci-status, literature-review, etc.)

## 6. Agents & Subagents - Delegation Patterns
- What agents are: `.claude/agents/*.md` - specialized Claude instances with focused instructions
- **Subagent architecture** - main session orchestrates, subagents do heavy lifting
  - Main context stays clean (only holds summaries)
  - Each subagent has its own fresh context window
- Patterns: implement+review, parallel exploration, `Ctrl+B` background
- See `cli/workflows.md` for patterns

## 7. Plugins & MCPs - Extending Claude Code
- Superpowers: brainstorm -> plan -> execute
- Code review + simplify loop
- Context7: live library docs (no hallucinated APIs)
- MCP servers: Gmail, Calendar, Telegram, Notion, Playwright, GitHub
- Deferred tool loading - hundreds of tools without context bloat
- See `cli/plugins.md` and `cli/mcps.md`

## 8. Workflow Patterns & Tips
- Plan-review-code-review (always review in a fresh session)
- The "interview me" trick
- Prompt templates (bug fix, feature, refactor)
- Model selection: Opus / Sonnet / Haiku
- `/effort low` vs `high` vs `ultrathink`
- See `cli/workflows.md` and `cli/tips.md`

---

## Format Notes
- HTML report (single file, self-contained)
- Dark theme, minimal text, point to repo files
- Screenshot embeds where relevant
- Target: ~20 minutes of presentation
