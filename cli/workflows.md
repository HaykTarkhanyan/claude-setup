# Claude Code Workflows & Patterns

## Plan-Review-Code-Review

The core workflow for non-trivial tasks:

```
1. Plan (plan mode) -> 2. Review Plan (read & edit) -> 3. Code (auto mode) -> 4. Review Code (NEW session)
```

- `claude -n "impl-auth"` for the coding session
- `claude -n "review-auth"` for review in a fresh session
- Or use `/code-review` plugin (4 parallel agents)

**Why separate sessions?** Fresh context = fresh eyes. No accumulated bias from the coding phase. The reviewer catches what the author missed.

**Rule:** Never skip the plan phase for non-trivial tasks. A 2-minute plan saves 20 minutes of rework.

## Prompt Templates

### Bug fix
"Symptom: [X]. Expected: [Y]. Check @file. Write a failing test first, then fix."

### Feature
"Implement [X] following the pattern in @example. Plan first, then code."

### Refactor
"Refactor [X] to [goal]. Keep all tests passing. Show me the plan before changing code."

### The "interview me" trick
Before complex tasks, say: "Interview me about the requirements before you start."
- Claude asks about edge cases, constraints, preferences
- Write the spec to `SPEC.md`
- Start a fresh session focused purely on implementation

**Key insight:** Output quality is determined by input quality. Templates and interviews enforce good input.

## Subagent Patterns

### Explicit delegation
- `@"reviewer (agent)"` - delegate to a named agent inline
- `claude --agent reviewer` - use a specific agent for the whole session
- `isolation: worktree` - safe parallel development in isolated repo copy
- `Ctrl+B` - background any task

### Implement + review pattern
1. One subagent implements in a worktree
2. Another subagent reviews the diff
3. Main session merges the results

### Keep main context clean
Use subagents for exploration and heavy lifting. Main session only holds summaries, not full workloads.

## Autoresearch Pattern

From Karpathy's [autoresearch](https://github.com/karpathy/autoresearch):
```
modify -> evaluate -> keep/discard -> repeat
```

- 83 runs overnight, 15 kept, 11% performance gain
- Works for any task with a measurable metric
- Claude Code + headless mode (`claude -p`) is perfect for this

## Meta-Improvement Loop

Periodically ask Claude:
- "What workflow improvements would you suggest?"
- "Review my CLAUDE.md - what's missing?"
- "What should I automate with hooks or skills?"

### Self-improvement habits
- "Keep track of your progress as you go"
- "Save what you learned to memory"
- Name sessions: `claude -n "feature-X"`

## Context Management Rules

| Situation | Action |
|-----------|--------|
| Switching to unrelated task | `/clear` |
| Continuing related work | `/compact` |
| Context past ~50% | Start fresh session |
| Quick side question | `/btw` (reuses prompt cache, cheap) |
| Heavy exploration | Dispatch a subagent |

**"Friends don't let friends compact"** - `/compact` is worst of both worlds: you lose working context but keep the "context poisoning" from before. Prefer `/clear` + fresh session when possible.
