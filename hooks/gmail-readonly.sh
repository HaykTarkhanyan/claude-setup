#!/usr/bin/env bash
# PreToolUse guard for the claude.ai Gmail connector: reads and drafts are allowed, sending never.
# Everything not on the allowlist is blocked, so new connector tools are blocked by default.
# Exit 2 = block; stderr is shown to Claude as the reason.
#
# Usage in ~/.claude/settings.json:
#   "PreToolUse": [{
#     "matcher": "^mcp__claude_ai_Gmail__",
#     "hooks": [{ "type": "command", "command": "bash ~/.claude/hooks/gmail-readonly.sh" }]
#   }]

input=$(cat)
tool=$(printf '%s' "$input" | grep -o '"tool_name"[[:space:]]*:[[:space:]]*"[^"]*"' | head -n 1 | sed 's/.*"\([^"]*\)"$/\1/')

case "$tool" in
  mcp__claude_ai_Gmail__search_threads|\
  mcp__claude_ai_Gmail__get_thread|\
  mcp__claude_ai_Gmail__get_message|\
  mcp__claude_ai_Gmail__list_labels|\
  mcp__claude_ai_Gmail__list_drafts|\
  mcp__claude_ai_Gmail__get_draft|\
  mcp__claude_ai_Gmail__create_draft|\
  mcp__claude_ai_Gmail__update_draft)
    exit 0
    ;;
esac

echo "Blocked by gmail-readonly.sh: '${tool:-<could not parse tool_name>}' is not allowed. Gmail is reads + drafts only (search/get/list, create_draft, update_draft). Never send, reply, forward, label, trash, mark spam or delete." >&2
exit 2
