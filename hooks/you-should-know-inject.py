"""UserPromptSubmit hook: pass the you-should-know plugin's heads-up notes to the session.

The built-in cc-plugin-you-should-know shows "Heads up" notes in the Claude Code UI,
but the main agent never sees them. The plugin keeps its state in
~/.claude/plugins/store/cc-plugin-you-should-know_builtin-*.json:
  sessions[].view  the note on screen right now (line + explanation), per session
  seen / known     headlines shown so far (global, no session id); "known" = the user
                   marked it as already known

On each prompt this injects the current session's on-screen note once. If a note was
offered and dismissed before the prompt, only its headline is left, so that is injected.

Needs the plugin enabled: claude plugin enable cc-plugin-you-should-know@builtin
Usage in ~/.claude/settings.json:
  "UserPromptSubmit": [{
    "hooks": [{ "type": "command", "command": "python ~/.claude/hooks/you-should-know-inject.py" }]
  }]
Runtime ~0.6 s per prompt (measured 2026-10-19, mostly Python startup).
Manual test: echo '{"session_id":"<id>"}' | python ~/.claude/hooks/you-should-know-inject.py
"""
import json
import logging
import sys
from pathlib import Path

CLAUDE_HOME = Path.home() / ".claude"
STORE_DIR = CLAUDE_HOME / "plugins" / "store"
STORE_GLOB = "cc-plugin-you-should-know_builtin-*.json"
STATE_DIR = CLAUDE_HOME / "hooks" / "state" / "you_should_know"
LOG_DIR = CLAUDE_HOME / "hooks" / "logs"

LOG_DIR.mkdir(parents=True, exist_ok=True)
log = logging.getLogger("you_should_know_inject")
log.setLevel(logging.INFO)
_fh = logging.FileHandler(LOG_DIR / "you_should_know_inject.log", encoding="utf-8")
_fh.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
log.addHandler(_fh)
_sh = logging.StreamHandler(sys.stderr)
_sh.setLevel(logging.WARNING)  # stdout is the hook's output; stderr only for problems
log.addHandler(_sh)

PREAMBLE = (
    "[you-should-know plugin] Under your previous reply, the built-in 'you should know' "
    "plugin showed the user the note(s) below. A separate model wrote them, not you, and "
    "the user has read them, so they may refer to them. Treat each one as a claim to check "
    "before acting on it."
)


def main() -> None:
    session_id = json.load(sys.stdin)["session_id"]

    stores = sorted(STORE_DIR.glob(STORE_GLOB), key=lambda p: p.stat().st_mtime)
    if not stores:
        log.warning(f"no file matching {STORE_DIR / STORE_GLOB}: plugin not run yet, disabled or renamed")
        return
    store = json.loads(stores[-1].read_text(encoding="utf-8"))
    entry = next((s for s in store["sessions"] if s["id"] == session_id), {})
    headlines = store["seen"] + store["known"]

    state_file = STATE_DIR / f"{session_id}.json"
    first_run = not state_file.exists()
    if first_run:
        state = {"offeredTurn": None, "injected": [], "snapshot": []}
    else:
        state = json.loads(state_file.read_text(encoding="utf-8"))

    notes = []
    view = entry.get("view") or {}
    line = view.get("line")
    if line and line not in state["injected"]:
        notes.append(f"{line}\n\n{view.get('explanation', '').strip()}")
        state["injected"].append(line)

    offered = entry.get("offeredTurn")
    if not first_run and offered != state["offeredTurn"]:
        for h in headlines:
            if h in state["snapshot"] or h in state["injected"]:
                continue
            known = " The user marked it as already known." if h in store["known"] else ""
            notes.append(f"{h}\n\n(Dismissed before this prompt, so only the headline is stored.{known})")
            state["injected"].append(h)

    if notes:
        log.info(f"session {session_id}: injecting {len(notes)} note(s)")
        context = PREAMBLE + "\n\n---\n\n" + "\n\n---\n\n".join(notes)
        sys.stdout.reconfigure(encoding="utf-8")
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit",
                                                 "additionalContext": context}}, ensure_ascii=False))
        sys.stdout.flush()

    # State is saved last: if the hook times out before this (it did on 2026-10-20, with the
    # machine at 100% CPU and 1.2 GB RAM free), its output is discarded and nothing is marked
    # as passed on, so the next prompt retries instead of losing the note.
    state["offeredTurn"] = offered
    state["snapshot"] = headlines
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    state_file.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        # Exit 1 = non-blocking hook error: the prompt still goes through, the user sees the error.
        log.exception("you_should_know_inject failed")
        sys.exit(1)
