# Claude Code Tips & Tricks

## Before starting a project

### Research first, code later
Before diving into implementation, ask Claude to research the topic:
```
Research [topic/library/pattern] thoroughly. Save your findings to a knowledge/ folder
as markdown files so we can reference them throughout the project.
```
This front-loads context and avoids hallucinated APIs mid-implementation.

### Set up the project for Claude
```
Read the entire codebase and suggest what should go in CLAUDE.md,
what hooks would help, and what skills would save time.
```
Or use the `/claude-automation-recommender` skill which does this automatically.

### Name your sessions
```bash
claude -n "feature-auth"     # descriptive name
claude -n "review-auth"      # separate session for review
```
Makes it easy to resume: `claude --resume feature-auth`

## During development

### Don't let Claude guess - point it to examples
"Implement X following the pattern in @existing-file" works much better than "implement X".

### Interview trick for complex features
Say "Interview me about the requirements before you start." Claude asks the right questions, you write a spec, then start a fresh session for implementation.

### Use subagents for exploration
Don't pollute your main context with research. Say "Use a subagent to explore how X works and report back a summary."

### Checkpoint with git
Commit working states frequently. If Claude goes off the rails, you can rewind: `Esc Esc` or `git checkout .`

### Watch your context
- Stay under ~50% context usage (ccstatusline shows this)
- `/clear` between unrelated tasks
- `/compact` only between related tasks (lossy - prefer fresh session)
- `/btw` for quick side questions (reuses prompt cache, cheap)

## Writing better prompts

### Be specific about output format
- "Show me a table comparing X and Y"
- "Give me the command I need to run, nothing else"
- "Plan first, then code. Wait for my approval before implementing."

### Constrain scope explicitly
- "Only modify file X. Don't touch anything else."
- "Fix just this bug. Don't refactor surrounding code."
- "Maximum 50 lines of code."

### Use effort levels
- `/effort low` for simple questions
- `/effort high` for architecture and complex reasoning
- Write `ultrathink` in your prompt for maximum thinking on a single turn

## After completing work

### Review in a fresh session
Always review code in a new session - the coding session has accumulated bias. Use `/code-review` or start `claude -n "review-X"`.

### Ask Claude to improve itself
- "What workflow improvements would you suggest?"
- "Review my CLAUDE.md - what's missing?"
- "What should I automate with hooks or skills?"
- "What did you learn from this session that's worth saving to memory?"

### Build skills for repeated work
If you've done something 3+ times, turn it into a skill:
```
Take what we just did and create a reusable skill in .claude/skills/
```

## Cost savings

### Model selection
- **Opus**: complex architecture, multi-file refactors
- **Sonnet**: most daily coding
- **Haiku**: quick questions, `/btw` side questions

### Token reduction
- Caveman plugin cuts ~75% output tokens
- Subagents keep main context clean
- Front-load context with CLAUDE.md and rules/ instead of re-explaining each session
- `/context` to see what's filling your context window
