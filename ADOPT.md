# Adopt this setup

- Repo: https://github.com/HaykTarkhanyan/claude-setup
- Workshop recording: https://youtu.be/KdtXO7Pj9DI
- Handout: [`claude-codex-workshop-standalone.html`](claude-codex-workshop-standalone.html)

**Read the handout first - it has the main content.** Setup step by step, models, context, hooks, permissions, skills, parallel agents, plugins, worktrees, and the reasoning behind the main rules in `CLAUDE.md`. GitHub shows the file as source code, so download it first. Open https://raw.githubusercontent.com/HaykTarkhanyan/claude-setup/main/claude-codex-workshop-standalone.html, press Ctrl+S (Cmd+S on a Mac), save it as an `.html` file and open that in a browser. Or run `curl -LO https://raw.githubusercontent.com/HaykTarkhanyan/claude-setup/main/claude-codex-workshop-standalone.html` in a terminal. It is one self-contained file and works offline.

Then paste the prompt below into Claude Code. It detects your machine itself, adopts the general rules without asking, and stops only for what it cannot know or what carries risk.

```text
Adopt the Claude Code setup from https://github.com/HaykTarkhanyan/claude-setup and adapt it to me. Do the safe parts on your own; stop only for the questions and approvals listed below.

1. Clone the repo into a temp folder and read README.md, CLAUDE.md, hooks/ and skills/. Also read workshop-template.html: it is the source of the workshop handout and has the main content and the reasoning behind the rules (same text as claude-codex-workshop-standalone.html, without the 6 MB of embedded images).

2. Detect my setup yourself instead of asking: OS and shell, CPU, RAM and GPU, which tools are installed (git, gh, python, uv, node, pandoc, docker), and what I already have in ~/.claude (CLAUDE.md, settings.json, hooks, skills, status line).

3. Ask me once, in a single batch of questions, only what you cannot detect: which language I write in and how I like answers written, whether my repos are public, and how much freedom you should have (asking before subagents, commits, pushes, deletes, paid API calls).

4. Write my ~/.claude/CLAUDE.md without asking for approval:
   - Back up any existing file first, and merge into it rather than replacing it.
   - Keep the general rules: fail loudly instead of silent fallbacks, verify facts instead of guessing, ask before heavy compute or spawning many subagents, run long jobs in the background, confirm the exact scope of critical changes, keep edits surgical, record decisions in DECISIONS.md, keep session logs in _work_sessions/ and learnings in _learnings/, make HTML reports standalone, pin exact dependency versions.
   - Drop what only fits the author: machine details that don't match mine, their personal tools and accounts, their language and plot colors, and any dated "Learned ..." story that makes no sense for me (keep the rule if it still applies).
   - Fill in my detected machine facts and my answers from step 3.
   - Add a rule: never write personal data or keys into repo files.

5. Skills: copy the skills from skills/ that clearly fit my tools into ~/.claude/skills/, adapting paths and commands. List the rest in one line each so I can ask for them later.

6. Hooks: these run shell scripts with my permissions, so this is the one part that needs my approval. Read each script in hooks/ fully, tell me in one line what it does and whether it fits me, and install only the ones I pick, showing the exact settings.json change first.

7. Status line: if I have none, set one up that shows the model, git branch and context usage. Mention ccstatusline (I run "npx -y ccstatusline@latest" in a normal terminal) as the richer option.

8. Finish with a short summary: what changed on my machine, what you dropped from the author's CLAUDE.md and why, and how to undo each part. Point me to the handout sections worth reading for my setup.
```

## What it does on its own and what it asks

- **Without asking:** reading the repo, detecting your machine, writing `~/.claude/CLAUDE.md` (after backing up any old one), copying the skills that fit, setting up a basic status line.
- **Asks once:** your language and writing preferences, whether your repos are public, and how much freedom Claude gets.
- **Needs your approval:** each hook, because hooks run shell scripts with your permissions.
- **Undo:** the summary at the end says how to reverse each change.

The repo's `CLAUDE.md` is tied to the author's machine (Windows, an Intel laptop GPU, OneDrive, two Claude accounts, Telegram, Armenian). Step 4 is what keeps those parts out of your copy.
