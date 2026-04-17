# Workshop Presenter Notes

Presenter cues extracted from `workshop.html`, organized by section.

## 1. Why CLI Over UI

Demo: open Claude Code in VS Code terminal, show Shift+Tab cycling, show a diff, show Ctrl+B backgrounding.

### Terminal setup

Show `cli/setting-up-terminal.md` for full keybinding list and alias setup across shells.

## 3. Project Setup & Self-Improvement

Open `global/CLAUDE.md` and walk through it. Run `/claude-automation-recommender` on a sample project live. Show the memory directory structure.

## 4. Hooks - Automating Safety & Workflows

Open `hooks/guard-push.sh` - show how simple a hook is. Show `hooks/session-start.sh` for the startup briefing pattern.

## 5. Permissions & Safety

Demo: Shift+Tab cycling through modes. Start a session with `--enable-auto-mode` and show it running. Open `hooks/guard-push.sh` and explain how PreToolUse blocks fire even in skip-permissions mode.

## 6. Skills - Reusable Workflows as Code

Open `skills/ci-status/SKILL.md` as a simple example. Then show `skills/literature-review/` for a complex one with scripts.

## 8. Plugins & MCPs

Demo Context7: ask Claude about a library API and say "use context7". Show the difference vs hallucinated docs.

## 9. Plugins

Demo `/review` on a real open PR. If time, contrast with `/code-review` plugin output on the same diff - shows when the heavier tool earns its keep. Then demo "use context7" on a library the attendee doesn't know well.

## 10. Useful Commands & Shortcuts

Demo: `/btw` in the middle of a task. Show `/color` with different terminals. Show `/context` output.

## 11. Workflow Patterns & Tips

Demo: start a named session, show the plan-review workflow. Show the interview trick live.

## 12. Parallel Sessions with Worktrees

Demo: ask Claude to implement a small feature "in a worktree, then open a PR". Show the worktree directory appear, the PR land, and that your main checkout is unchanged.

## 13. Remote & Cloud Agents

Demo `/rc` if possible (needs phone). Mention this is the "assign work overnight" pattern.
