# claude-setup

All my Claude Code workflows, configs, hooks, and patterns in one place.

## Structure

```
global/                     # Global config (lives at ~/.claude/)
  CLAUDE.md                 # Global instructions for all projects
  settings.json             # Global settings: plugins, hooks, permissions

hooks/                      # Reusable hook scripts (copy into .claude/hooks/)
  notify.sh                 # Windows toast notification on Notification event
  guard-push.sh             # Block git push unless user explicitly approves
  session-start.sh          # Multi-repo orientation on session start
  post-compact.sh           # Re-inject critical rules after context compression
  pre-check.sh              # Block edits to secret files (.env, .pem, .key, etc.)
  gmail-readonly.sh         # Block Gmail write operations (keep read-only)

project-configs/            # Documented patterns extracted from real projects
  notes-productivity.md     # Daily notes + Gmail/Calendar/Telegram integration
  monorepo-with-hooks.md    # Full hook architecture for multi-repo workspace
  content-pipeline.md       # 10-step content pipeline with approval gates
  benchmark-task-design.md  # LLM benchmark tasks with skill-based workflow
  video-editing.md          # ffmpeg-based video processing
  course-delivery.md        # Quarto + Beamer course automation
```

## Global plugins

- **superpowers** - brainstorming, planning, TDD, debugging, code review workflows
- **code-review** - PR review agent
- **code-simplifier** - simplifies changed code
- **playwright** - browser automation and testing
- **telegram** - Telegram bot integration
- **claude-code-setup** - automation recommender

## Global hooks

- **Gmail read-only** - blocks all Gmail write operations (create, send, modify, delete)
- Permissions default to `acceptEdits` mode

## How to use

### New project setup
1. Copy relevant hook scripts to `.claude/hooks/`
2. Create `.claude/settings.local.json` with project-specific permissions
3. Create `CLAUDE.md` with project-specific rules
4. Check `project-configs/` for patterns that match your project type

### Hook installation
Add to your project's `.claude/settings.json` or `.claude/settings.local.json`:
```json
{
  "hooks": {
    "PreToolUse": [
      { "matcher": "Edit|Write", "hooks": [{ "type": "command", "command": "bash .claude/hooks/pre-check.sh" }] },
      { "matcher": "Bash", "hooks": [{ "type": "command", "command": "bash .claude/hooks/guard-push.sh" }] }
    ],
    "Notification": [
      { "matcher": "", "hooks": [{ "type": "command", "command": "bash .claude/hooks/notify.sh" }] }
    ]
  }
}
```

## Source projects

| Project | What it contributes |
|---------|-------------------|
| `~/.claude/` | Global CLAUDE.md, settings, SEO agents/skills |
| `00_notes/` | Productivity system, morning/eod routines, Telegram MCP |
| `02_Promet/` | Hook architecture, monorepo patterns, 9 agents |
| `content-writing-workflow/` | Content pipeline, approval gates, 9 agents |
| `mindrift_clean/` | Benchmark task skills, Playwright monitoring |
| `video_editing_tools/` | ffmpeg patterns, QSV detection |
| `01_python_math_ml_course/` | Quarto/Beamer automation |
