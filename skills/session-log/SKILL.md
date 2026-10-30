---
name: session-log
description: Write the end-of-session TOML log into _work_sessions/. Use when the user says "save the session", "write the session log", "log this session", "session entry", or at the end of substantial work.
---

# Session Log

Writes one TOML file per session into `_work_sessions/` at the repo root.

## Step 1: Work out the filename

`_work_sessions/YYYY-MM-DD-HHMM_slug.toml`

- `HHMM` is the 24h local **start** time of the session, no colon. Not the
  current time: sessions get logged at the end, so look for the earliest
  evidence (first file written, first commit, first scratchpad artifact) and
  work backwards. State the estimate rather than pretending to precision.
- `slug` is short, lowercase, underscore-separated, and describes the outcome
  rather than the topic: `wsl_colab_gpu_setup`, not `linux_stuff`.
- Use the real calendar date, even after midnight, so the files sort
  chronologically.

## Step 2: Gather evidence before writing anything

Do not write the log from memory of the conversation alone. Check:

- `git -C <repo> status --porcelain` and `git -C <repo> log --oneline -10`
- `git -C <repo> diff --stat` for what actually changed
- The newest 2-3 files in `_work_sessions/` - carry forward any `pending`
  items that are still unresolved, and note if this session closed one.

Every `done` entry should trace to something observable: a file that exists, a
command that ran, a number that was measured. If a claim can't be traced, say
so in the entry rather than asserting it.

## Step 3: Write the TOML

Exact schema, in this order:

```toml
title = "outcome-first, one line"
date = "YYYY-MM-DD"
time = "HH:MM"
areas = ["folders touched"]

done = [
  "Dense factual entries. Include real numbers, file paths, versions, dates.",
  "Lead with the outcome, then the detail. Prefix a hard-won finding with a",
  "short ALL-CAPS tag when it deserves to be findable later.",
]

pending = ["what is unfinished, and enough context to resume cold"]

next = "the single most useful next action"

files = ["path (what it is / why it changed)"]

commits = []

notes = """
Gotchas. The things that would bite someone again: fragile pins, quoting
traps, commands that hang, non-obvious ordering requirements.
"""
```

Match the density of existing entries. A vague log is worse than none because
it looks like coverage.

## Step 4: Validate before claiming done

```bash
python -c "import tomllib; tomllib.load(open('<path>','rb')); print('ok')"
```

`tomllib` needs Python 3.11+. On an older Python the check fails with
`ModuleNotFoundError` instead of validating, so run it with a newer one:
`uv run --no-project --python 3.12 python -c "..."`.

Confirm all ten keys are present. A malformed log is worse than no log.

## Step 5: Report, don't commit

Summarise what was captured in a few lines. **Do not commit** unless the user
asks: a stray `git add -A` can sweep unrelated work into the commit.

## Also worth offering

If the session produced a non-obvious lesson (a gotcha, a fragile workaround, a
measurement that overturned an assumption), offer to add it to `_learnings/`
too, as **one file per lesson**: `_learnings/YYYY-MM-DD-HHMM_slug.md`, with an H1
title, then **Symptom** / **Cause** / **Consequences** where that shape fits, and
the evidence (command output, numbers). Session logs are chronological;
`_learnings/` is the lookup surface. They serve different purposes and the same
fact can belong in both.
