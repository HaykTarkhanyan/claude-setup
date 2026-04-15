# Claude Code Plugins

## Installed (global settings.json)

| Plugin | What it does |
|--------|-------------|
| **superpowers** | Enforced 5-phase dev workflow: clarify, design, plan, code (TDD), verify. Subagent-driven development, git worktree isolation, systematic debugging. |
| **code-review** | `/code-review` runs 4 parallel agents. CLAUDE.md compliance, bug scan, git-blame context. Findings scored 0-100. |
| **code-simplifier** | `/simplify` - post-implementation cleanup. Preserves functionality, improves clarity. |
| **playwright** | Browser automation via MCP. Screenshots, form filling, E2E testing. |
| **telegram** | Telegram bot integration - reply, send files, reactions. |
| **claude-code-setup** | Analyzes codebase and recommends automations (hooks, skills, MCPs). |

## Worth knowing about

| Plugin | What it does | Install |
|--------|-------------|---------|
| **Caveman** | Cut ~75% output tokens. Three levels: lite (drops filler), full (fragments), ultra (telegraphic). Research showed 26pp accuracy improvement from brevity. | `claude plugin marketplace add JuliusBrussee/caveman` then `claude plugin install caveman@caveman` |
| **MemPalace** | Local-first persistent memory with knowledge graph. 96.6% recall on LongMemEval. Method of loci hierarchy. 29 MCP tools. | `pip install mempalace` |

## Recommended workflow

```
code -> /code-review -> /simplify
```

## Superpowers key commands

| Command | What it does |
|---------|-------------|
| `superpowers brainstorm` | Explore requirements, propose approaches, write spec |
| `superpowers write plan` | Turn spec into implementation plan with line-by-line changes |
| `superpowers execute plan` | Dispatch subagents to implement the plan |
| `superpowers test-driven-development` | Red-green-refactor cycle |
| `superpowers systematic-debugging` | Root-cause analysis before proposing fixes |
| `superpowers dispatching-parallel-agents` | Split independent tasks across agents |
| `superpowers verification-before-completion` | Run verification before claiming done |
