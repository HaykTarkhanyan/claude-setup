# Adopt this setup

Paste the prompt below into Claude Code. That is all: it reads your past conversations, interviews you, and sets everything up.

```text
Adopt the Claude Code setup from https://github.com/HaykTarkhanyan/claude-setup and adapt it to me. Do the safe parts on your own; stop only for the questions and approvals listed below. Open your first reply with a short fun hello (an interesting fact or a joke, a line or two), then tell me in a few lines what you are about to do and what you will ask me, and get to work. If you are not running as Opus 5.5, or can't tell whether effort is xhigh, suggest once that I type /model opus and /effort xhigh in this same session, then carry on without waiting.

1. Detect my setup yourself instead of asking: OS and shell, CPU, RAM and GPU, which tools are installed (git, gh, python, uv, node, npm, pandoc, docker), which plugins and MCP servers I already have, and what is in ~/.claude (CLAUDE.md, settings.json, hooks, skills, status line).

2. Get the repo into a temp folder: with git clone if git is installed, otherwise download and unzip https://github.com/HaykTarkhanyan/claude-setup/archive/refs/heads/main.zip. Read README.md, CLAUDE.md, hooks/ and skills/, and workshop-template.html: it is the source of the workshop handout and has the main content and the reasoning behind the rules (same text as claude-codex-workshop-standalone.html, without the 6 MB of embedded images).

3. Read my past conversations. This is the most important step: the interview and everything after it build on what you find here, so take your time.
   - ~/.claude/history.jsonl: every prompt I typed, one line each, with the project folder and time.
   - The session transcripts in ~/.claude/projects/ (one folder per project, one .jsonl per session), newest first, and ~/.codex/sessions/ if I use Codex.
   These files get large, so use a short script that pulls out my own messages (and the errors in your replies) instead of loading whole files, and go through all of it, not a sample. Claude Code deletes transcripts after 30 days by default (the cleanupPeriodDays setting), so expect about a month of history. Then write me a short report:
   - What I work on: stack, main projects, the tools and services I use.
   - What I repeat: tasks and prompts I type again and again (candidates for skills).
   - What goes wrong: errors, dead ends, things I had to redo.
   - How I correct you: things I keep restating (candidates for CLAUDE.md rules).
   - Manual steps I do every time (candidates for hooks or automation).
   End it with numbered suggestions (S1, S2, ...): a skill to write, a rule to add, a hook, an MCP server or plugin, a change to how I work. Back each one with the evidence from my history, quoted in your reply only: never copy conversation text, names or keys into any file. If there is no history, say so and skip to the interview.

4. Interview me once, in a single batch of questions. Let me accept or drop each suggestion from step 3, then ask only what the history and the detection didn't answer:
   - my main stack and languages (for example Python, JavaScript/TypeScript, MATLAB, R, C++)
   - what kind of work I do and which services I use (GitHub, CI, email, research papers, and so on)
   - whether I do research (reading papers, literature reviews), and in which field
   - whether I need heavy compute (training, embeddings, anything that wants a GPU)
   - which language I write in and how I like answers written
   - whether my repos are public
   - how much freedom you should have (asking before subagents, commits, pushes, deletes, paid API calls)

5. Offer me one list of things to install, with your recommendations pre-selected and one line on what each does, so I can approve it in one go:
   - Whatever the suggestions I accepted in step 4 need (plugins, MCP servers, tools).
   - Missing basics that fit my work: git, the GitHub CLI (gh), Node.js with npm, Python with uv, pandoc.
   - The plugins from the handout's setup section: Playwright (browser automation), Context7 (live library docs), Superpowers (structured workflows), plus any other plugin or MCP server from the handout that fits my work.
   - Extras for my main stack: an official MCP server, a code-intelligence or language-server plugin, a linter or formatter, a useful skill. Search for current options instead of answering from memory, and only offer ones that are actively maintained.
   - If I do research: the OpenAlex MCP server for literature search and citation counts (free daily allowance). Add it with "claude mcp add --transport http --scope user openalex https://mcp.openalex.org/mcp" and ask me to log in via /mcp. Also the companion skills that skills/literature-review relies on, from K-Dense's library (https://github.com/K-Dense-AI/scientific-agent-skills): scientific-schematics (the review skill requires figures from it), plus the ones that fit my field, such as citation-management, scientific-writing or gget. Install each with "gh skill install K-Dense-AI/scientific-agent-skills <skill> --agent claude-code" (needs gh 2.90 or newer; otherwise copy the skill's folder from that repo into ~/.claude/skills/). Only the relevant ones, not all 177.
   - If I need heavy compute: the colab-gpu skill from this repo, which rents GPUs through Google's official colab CLI (Linux and macOS only, so inside WSL on Windows). Also tell me that Hayk, the author of this repo, has some RunPod credits left, and that I can message Hayk for access.
   - Keeping my transcripts: set "cleanupPeriodDays": 3650 in ~/.claude/settings.json, so future conversations are not deleted after 30 days. Pre-select this one, but tell me the trade-off: transcripts also keep anything I pasted, keys included.
   - The hooks from hooks/ that fit me, including you-should-know-inject.py if my account has the plugin from step 8 (the hook passes its heads-up notes into my next prompt). Hooks run shell scripts with my permissions, so read each one fully first and show the exact settings.json change.
   Then install what I picked. Explain each command before you run it. For steps that need me (gh auth login, git config user.name and user.email, logins in a browser), tell me the exact command to run with the ! prefix.

6. Write my ~/.claude/CLAUDE.md without asking for approval:
   - Back up any existing file first, and merge into it rather than replacing it.
   - Keep the general rules: fail loudly instead of silent fallbacks, verify facts instead of guessing, ask before heavy compute or spawning many subagents, run long jobs in the background, confirm the exact scope of critical changes, keep edits surgical, record decisions in DECISIONS.md, keep session logs in _work_sessions/ and learnings in _learnings/, make HTML reports standalone, pin exact dependency versions.
   - Drop what only fits the author: machine details that don't match mine, their personal tools and accounts, their language and plot colors, and any dated "Learned ..." story that makes no sense for me (keep the rule if it still applies).
   - Fill in my machine facts, my answers from step 4, and a short section for my main stack: how to run, test and lint it, and which of the installed tools to use for what.
   - Turn the corrections I kept making in past conversations, and the rules I accepted from step 3, into rules.
   - Add a rule for a light start: the first reply in a session opens with a short fun hello (an interesting fact or a joke, a line or two). Only at the start of a session, or again every few days in a long-running one. Don't overdo it.
   - Add a rule: never write personal data or keys into repo files.

7. Skills: from my answers and what you detected, decide yourself which skills in skills/ are relevant and install those into ~/.claude/skills/, adapting paths and commands. Always include session-log, since the CLAUDE.md rules keep session logs in _work_sessions/. If I do research, always include literature-review and paper-explainer; if I need heavy compute, include colab-gpu. Don't walk me through the rest. Then write new skills for the repeated tasks I accepted in step 4, and the hooks I accepted, following the same patterns.

8. Status line and heads-up notes, without asking:
   - If I have no status line, set one up that shows the model, git branch and context usage. Mention ccstatusline (I run "npx -y ccstatusline@latest" in a normal terminal) as the richer option.
   - Enable the built-in "You should know" plugin (claude plugin enable cc-plugin-you-should-know@builtin), if my account has it. It is a side agent that leaves short heads-up notes during long tasks, so it uses some extra usage; tell me what it does and how to turn it off.

9. Verify what you installed: show the version of each tool, and if Playwright was installed, open example.com with it and tell me the page heading.

10. Finish with a short summary: what changed on my machine, what you dropped from the author's CLAUDE.md and why, and how to undo each part. List the suggestions from my history I haven't acted on yet. Then copy claude-codex-workshop-standalone.html from the repo into a folder I keep (for example Documents), open it in my browser, and tell me which of its sections are worth reading for my setup: it is the workshop handout and works offline. Also give me the workshop recording: https://youtu.be/KdtXO7Pj9DI
```
