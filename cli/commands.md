# Claude Code CLI Reference

## Slash Commands

### Session management
| Command | What it does |
|---------|-------------|
| `/clear` | Wipe context, start fresh (use between unrelated tasks) |
| `/compact` | Compress context (use between related tasks) |
| `/resume` | Resume last session |
| `/rename <name>` | Rename current session |
| `/model <name>` | Switch model mid-session (opus, sonnet, haiku) |
| `/cost` | Show token usage and cost for current session |
| `/context` | Visualize what's filling your context window |
| `/fast` | Toggle fast mode (same Opus model, faster output) |

### Effort and thinking
| Command | What it does |
|---------|-------------|
| `/effort low` | Minimal thinking, fast responses |
| `/effort high` | Deep reasoning, thorough analysis |
| `ultrathink` | Write in prompt to get maximum thinking for that turn |

### Interaction
| Command | What it does |
|---------|-------------|
| `/btw` | Side question that reuses prompt cache (cheap) |
| `/voice` | Toggle voice mode |
| `/vim` | Enable vim keybindings |
| `/color` | Set accent color |
| `/rc` | Remote control - continue session from phone/browser |

### Code workflow
| Command | What it does |
|---------|-------------|
| `/code-review` | Run 4 parallel review agents on your code |
| `/simplify` | Post-implementation cleanup, preserve functionality |
| `/commit` | Stage and commit with auto-generated message |
| `/plugin` | Plugin management menu |
| `/mcp` | Check MCP server connections |
| `/help` | Show help |

## Keyboard Shortcuts

| Key | What it does |
|-----|-------------|
| `Shift+Tab` | Cycle permission modes (ask/auto-edit/dangerous) |
| `Esc` | Stop current generation |
| `Esc Esc` | Rewind to previous state |
| `Ctrl+O` | Toggle verbose mode (see thinking) |
| `Ctrl+B` | Background current task |
| `Ctrl+G` | Open prompt in external editor |
| `Ctrl+R` | Search command history |
| `Ctrl+C` | Cancel/interrupt |
| `Ctrl+L` | Clear screen |

## CLI Flags

### Starting sessions
| Flag | What it does |
|------|-------------|
| `claude` | Start new conversation |
| `claude --resume` | Resume last conversation |
| `claude -n "name"` | Start named session |
| `claude --dangerously-skip-permissions` | Auto-approve everything |
| `claude --worktree feature-x` | Start in isolated git worktree |
| `claude --agent reviewer` | Use a specific agent for the session |

### Headless / piping
| Flag | What it does |
|------|-------------|
| `claude -p "prompt"` | One-shot prompt, print response, exit |
| `cat file \| claude -p "explain"` | Pipe input into prompt |
| `claude -p "..." > out.txt` | Redirect output to file |
| `claude -p "..." --json` | Output as JSON |

## Prompt Tricks

### Templates
- **Bug fix:** "Symptom: [X]. Expected: [Y]. Check @file. Write a failing test first, then fix."
- **Feature:** "Implement [X] following the pattern in @example. Plan first, then code."
- **Refactor:** "Refactor [X] to [goal]. Keep all tests passing. Show me the plan before changing code."

### The interview trick
Say "Interview me about the requirements before you start" - Claude asks clarifying questions, then you write the spec to SPEC.md and start a fresh session for implementation.

### Context management
- `/clear` between unrelated tasks
- `/compact` between related tasks
- Don't let context go past ~50% - Claude degrades well before 100%
- Use subagents to keep main context clean
- `/btw` for quick side questions (reuses prompt cache, cheap)

## Model Selection Guide

| Model | When to use |
|-------|------------|
| **Opus** | Complex architecture, multi-file refactors, deep reasoning |
| **Sonnet** | Most daily coding, good balance of speed and quality |
| **Haiku** | Quick questions, simple edits, `/btw` side questions |
