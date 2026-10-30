# Adopt this setup

- Repo: https://github.com/HaykTarkhanyan/claude-setup
- Workshop recording: https://youtu.be/KdtXO7Pj9DI
- Handout: [`claude-codex-workshop-standalone.html`](claude-codex-workshop-standalone.html)

**Read the handout first - it has the main content.** Setup step by step, models, context, hooks, permissions, skills, parallel agents, plugins, worktrees, and the reasoning behind the main rules in `CLAUDE.md`. GitHub shows the file as source code, so download it first. Open https://raw.githubusercontent.com/HaykTarkhanyan/claude-setup/main/claude-codex-workshop-standalone.html, press Ctrl+S (Cmd+S on a Mac), save it as an `.html` file and open that in a browser. Or run `curl -LO https://raw.githubusercontent.com/HaykTarkhanyan/claude-setup/main/claude-codex-workshop-standalone.html` in a terminal. It is one self-contained file and works offline.

Then paste the prompt below into Claude Code. It detects your machine itself, adopts the general rules without asking, and stops only for what it cannot know or what carries risk.

```text
Adopt the Claude Code setup from https://github.com/HaykTarkhanyan/claude-setup and adapt it to me. Do the safe parts on your own; stop only for the questions and approvals listed below.

1. Detect my setup yourself instead of asking: OS and shell, CPU, RAM and GPU, which tools are installed (git, gh, python, uv, node, npm, pandoc, docker), which plugins and MCP servers I already have, and what is in ~/.claude (CLAUDE.md, settings.json, hooks, skills, status line).

2. Get the repo into a temp folder: with git clone if git is installed, otherwise download and unzip https://github.com/HaykTarkhanyan/claude-setup/archive/refs/heads/main.zip. Read README.md, CLAUDE.md, hooks/ and skills/, and workshop-template.html: it is the source of the workshop handout and has the main content and the reasoning behind the rules (same text as claude-codex-workshop-standalone.html, without the 6 MB of embedded images).

3. Before the interview, read my past conversations so your questions are informed:
   - ~/.claude/history.jsonl: every prompt I typed, one line each, with the project folder and time.
   - The most recent session transcripts in ~/.claude/projects/ (one folder per project, one .jsonl per session), and ~/.codex/sessions/ if I use Codex.
   These files get large, so use a short script that pulls only my own messages from the last month or two instead of loading whole files. Work out my stack, my main projects, the tasks I repeat, what tends to go wrong, and the corrections I keep making. Use it as context only: never copy conversation text, names or keys into any file. If there is no history, skip this step.

4. Interview me once, in a single batch of questions. Start with a few lines on what you learned from my history, then ask only what it and the detection didn't answer:
   - my main stack and languages (for example Python, JavaScript/TypeScript, MATLAB, R, C++)
   - what kind of work I do and which services I use (GitHub, CI, email, research papers, and so on)
   - which language I write in and how I like answers written
   - whether my repos are public
   - how much freedom you should have (asking before subagents, commits, pushes, deletes, paid API calls)

5. Offer me one list of things to install, with your recommendations pre-selected and one line on what each does, so I can approve it in one go:
   - Missing basics that fit my work: git, the GitHub CLI (gh), Node.js with npm, Python with uv, pandoc.
   - The plugins from the handout's setup section: Playwright (browser automation), Context7 (live library docs), Superpowers (structured workflows), plus any other plugin or MCP server from the handout that fits my work.
   - Extras for my main stack: an official MCP server, a code-intelligence or language-server plugin, a linter or formatter, a useful skill. Search for current options instead of answering from memory, and only offer ones that are actively maintained.
   - The hooks from hooks/ that fit me. Hooks run shell scripts with my permissions, so read each one fully first and show the exact settings.json change.
   Then install what I picked. Explain each command before you run it. For steps that need me (gh auth login, git config user.name and user.email, logins in a browser), tell me the exact command to run with the ! prefix.

6. Write my ~/.claude/CLAUDE.md without asking for approval:
   - Back up any existing file first, and merge into it rather than replacing it.
   - Keep the general rules: fail loudly instead of silent fallbacks, verify facts instead of guessing, ask before heavy compute or spawning many subagents, run long jobs in the background, confirm the exact scope of critical changes, keep edits surgical, record decisions in DECISIONS.md, keep session logs in _work_sessions/ and learnings in _learnings/, make HTML reports standalone, pin exact dependency versions.
   - Drop what only fits the author: machine details that don't match mine, their personal tools and accounts, their language and plot colors, and any dated "Learned ..." story that makes no sense for me (keep the rule if it still applies).
   - Fill in my machine facts, my answers from step 4, and a short section for my main stack: how to run, test and lint it, and which of the installed tools to use for what.
   - Turn the corrections I kept making in past conversations into rules.
   - Add a rule: never write personal data or keys into repo files.

7. Skills: from my answers and what you detected, decide yourself which skills in skills/ are relevant and install those into ~/.claude/skills/, adapting paths and commands. Don't walk me through the rest.

8. Status line: if I have none, set one up that shows the model, git branch and context usage. Mention ccstatusline (I run "npx -y ccstatusline@latest" in a normal terminal) as the richer option.

9. Verify what you installed: show the version of each tool, and for Playwright open example.com and tell me the page heading.

10. Finish with a short summary: what changed on my machine, what you dropped from the author's CLAUDE.md and why, and how to undo each part. Point me to the handout sections worth reading for my setup.
```

## What it does on its own and what it asks

- **Without asking:** detecting your machine, getting and reading the repo, reading your past Claude Code and Codex conversations (to shape the questions), writing `~/.claude/CLAUDE.md` (after backing up any old one), picking and installing the skills that fit your work, setting up a basic status line, and checking that everything works.
- **Asks once:** your main stack (Python, MATLAB, and so on), what kind of work you do, your language and writing preferences, whether your repos are public, and how much freedom Claude gets.
- **Needs your approval, in one go:** what to install - missing tools like git, plugins like Playwright and Context7, extras for your stack, and the hooks it picked.
- **Needs you at the keyboard:** logins such as `gh auth login`, and your git name and email.
- **Undo:** the summary at the end says how to reverse each change.

The repo's `CLAUDE.md` is tied to the author's machine (Windows, an Intel laptop GPU, OneDrive, two Claude accounts, Telegram, Armenian). Step 6 is what keeps those parts out of your copy.
