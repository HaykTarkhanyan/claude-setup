# Workshop Presenter Notes

Present from the HTML handout (`claude-codex-workshop-standalone.html`). Section numbers below match its sidebar. Recording of a past run: https://youtu.be/KdtXO7Pj9DI

## Opening: the verse

The box at the top of the handout is an Armenian rap verse Claude wrote about itself. Read it out loud (or hand it to the best performer in the room) - it's 30 seconds and it breaks the ice. The beat is the player in that box (also `assets/verse-beat.mp3`): 4 bars of intro (~11 s), then one line per bar at 88 BPM; the drums drop out at 0:49 for the punchline, come back for one bar, and the track ends in a tape stop at 1:00. Check the room audio beforehand. Don't explain the Hugging Face and PyPI lines yet; they pay off in section 18, so call back to them there.

## 00. Setup, step by step

Best sent as pre-work a few days ahead (link the handout's § 00), then spend the first 15-20 minutes helping whoever is stuck. Walk the room during steps 1 and 4 - install PATH issues and `gh auth login` are where people stall. Point Codex/Cursor/Copilot users at the "Not on Claude Code?" part right away so they don't sit idle. Do step 3 (the interview) live on the projector once: it shows AskUserQuestion before section 14 explains it.

## 01. Why the terminal

Demo: open Claude Code in VS Code terminal, show Shift+Tab cycling, show a diff, show Ctrl+B backgrounding. Show the shortcut and VS Code keybinding tables in this section. Mention the YOLO aliases only AFTER pointing at the warning box - don't let attendees copy them before section 08.

## 02. Pick your model

Demo: `/model` picker, then `/effort` - point out that the 5.5 models start at `medium`, so anyone who upgraded and feels answers got shallower should check this first. Show `/advisor opus` on a Sonnet session and the "Advising" line when it fires. Warn before demoing `/fast`: it bills to usage credits, not plan limits, and costs most when switched on mid-session.

## 03. Know your context

Demo: ccstatusline in a live session, then `/context` - name the biggest consumer out loud. Show Esc Esc rewind, then `/rewind` restoring code + conversation together (stage a small bad edit first).

The screenshots in these sections (statusline, `/context`, the decision table, ccusage) are too small to read from the back of a room - they're illustrations. Run the real commands live instead of pointing at them.

## 04. Know your spend

Demo: `/usage` on the current session - point at the cache hit line and the per-plugin breakdown. Then `npx ccusage@latest` on your own machine if you dare. Run Lab I here if time allows (10 min).

## 05. Project setup & self-improvement

Open the repo's root `CLAUDE.md` (a real global instructions file) and walk through it. Run `/init` on a sample project live, then `/claude-automation-recommender`. For Codex users: show the AGENTS.md table and the trap (a `CLAUDE.local.md` silently switches AGENTS.md off), then `/import codex --dry-run`.

## 06. CLAUDE.md rules that earn their keep

Three beats: (1) the anti-bias table - tell the story of the "Codex has no fast mode" claim that search-first caught while writing these materials, and the features a claim-by-claim check still missed; (2) the memory-the-team-can-read files - open a real `_learnings/` file and a `_work_sessions/` TOML from one of your repos; (3) the hard-way cards - pick the three with the best war stories (fan-outs, destructive commands, tech choices) and tell the incidents. Close with the meta-pattern: "update CLAUDE.md so this doesn't happen again."

## 07. Hooks

Open `hooks/guard-push.sh` - show how simple a hook is. Show `hooks/session-start.sh` for the startup briefing pattern. Mention that `/goal` is a prompt-based Stop hook - it comes back in section 14.

## 08. Permissions & safety

Demo: Shift+Tab through the modes, open the `/permissions` Auto tab, then `/sandbox` and show a blocked network call. Explain why PreToolUse blocks fire even in skip-permissions mode. Run Lab II here (guard-push exercise, 15 min) - it's the highest-value lab.

## 09. Skills

Open `skills/ci-status/SKILL.md` as a simple example, `skills/literature-review/` as a complex one. Run `/skill-doctor` on your own setup and delete something live.

## 10. Running agents in parallel

Put the five-way table on screen first and keep it there - most confusion is about which approach to use. Demo: `claude --bg` two small tasks, open `claude agents`, peek with Space, answer one from the peek panel. Then `@`-mention one session from another. Show `/deep-research` only as a prompt and the approval card - do NOT run a full workflow or `/effort ultracode` live; state the cost warning instead. Agent teams: show the env var, don't demo.

## 11. Plugins & MCPs

Demo `/simplify` or `/code-review low` on a real diff. Then Context7: ask about a library API with and without "use context7" - show the hallucination difference.

## 12. Mods

Start from the comparison table: most people should use a hook, skill, or MCP server first - mods are for drawing and taking an event over. Demo: load `blast-radius` from claude-code-playground with `--plugin-dir` and trigger it with a harmless `rm -rf` in a scratch folder - the held command with proceed/cancel buttons is the moment it clicks. Then ask Claude live for a tiny mod (the tool-call counter from "Anatomy of a mod") and watch it hot-reload. At "You should know", enable it live (`/plugin enable cc-plugin-you-should-know@builtin`) and leave it on for the rest of the workshop - its notes will show up during the `/goal` demo in section 14, which is the payoff. Check beforehand that it's available on the account you present from. End on the "Mods are not sandboxed" box: run `claude plugin validate` and read the `calls:` line out loud before anyone installs a stranger's mod. Run Lab III after this section.

## 13-14. Commands & workflow patterns

Demo: `/btw` mid-task, `@` file references, `!` shell prefix. Then background work live: start `! npm run dev` (or any long command), press Ctrl+B, keep chatting, show it in `/tasks`. While Claude works on something, type a follow-up and press Enter to show it queues instead of interrupting; press Up to take it back. Then `/goal` on a failing test with a turn budget - press Ctrl+O on a "not yet met" verdict to show the evaluator's reason. Tie it back to Karpathy's rule 4 in section 06. Show the interview trick live (AskUserQuestion) - it lands well as the closer for the prompting segment.

## 15. Worktrees

Demo: ask Claude to implement a small feature "in a worktree, then open a PR". Show the worktree directory appear, the PR land, and the main checkout unchanged.

## 16. Remote & cloud

Demo `/rc` if a phone is handy. Mention `/schedule` as the "assign work overnight" pattern and Projects as its multi-day cloud version; Lab IV is homework, not live. Save the Telegram channel demo for section 17.

## 17. Showcases

Run order (pick by time left; each is 3-5 min):

1. **list.am with Playwright** - run the apartment prompt from the handout live; let the room watch the browser scroll. Have a fallback recording in case list.am is slow or blocks automation.
2. **Telegram** - message the running session from your phone and let the room watch the answer arrive in the terminal. The most memorable demo of the day.
3. **Gmail and Calendar** - triage + drafts only; book a slot only after confirming. Show `hooks/gmail-readonly.sh` as the guardrail.
4. **Kargin** - show the Kargin search site: a quote search that jumps to the moment, and a collection page.
5. **YouTube** - `check <link>` with the youtube-reference skill on a short video; then auto_dubbing output (English in, Armenian out) if a finished dub is at hand.
6. **Claude for learning** - nemeceren: open a lesson on the phone, then show Claude grading a free-text answer from the progress database.
7. **You should know** - if it hasn't fired yet, start a longer `/goal` task in auto mode and point at the heads-up notes as they appear above the prompt.
8. **Vahe's video on Armenian history** - show it.

Must show: **Kargin** and the **YouTube examples** - don't drop these if time runs short.

## 18. Wins and warnings

No demo - this is the story slot, 10-15 minutes. Open the timeline table and keep the arc simple: the same persistence that finishes a proof also finds the hole in a sandbox. Math: tell the GPT-5 false start first (it sets up why verification matters), then Knuth - read the "Shock! Shock!" line and point at Filip's plan.md rule, which is the progress-file trick from section 06 in the wild. Hugging Face: go slowly through the day-by-day table; the beats that land are the message board in cache names, the motive (stealing the answer key, not malice), and the 7% spoofed transcripts. Show "Not just OpenAI" so it doesn't sound like a dig at a competitor. End on the "your setup" table and the one-line version, then go to questions. These events are recent and reporting is still moving - check the sources at the end of section 18 the week before presenting.

## Appendix

Point at the Codex map when Codex users ask "what's my equivalent of X" - don't walk the table row by row.
