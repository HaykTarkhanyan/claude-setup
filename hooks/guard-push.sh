#!/bin/bash
# PreToolUse guard - blocks git push even in dangerouslySkipPermissions mode
# Lightweight: just reads command from stdin JSON and greps for git push
#
# Usage in settings.json:
#   "PreToolUse": [{ "matcher": "Bash", "hooks": [{ "type": "command", "command": "bash path/to/guard-push.sh" }] }]

INPUT=$(cat)
CMD=$(echo "$INPUT" | grep -o '"command":"[^"]*"' 2>/dev/null || echo "$INPUT" | grep -o '"command": "[^"]*"' 2>/dev/null)

if echo "$CMD" | grep -qi 'git push'; then
    echo "BLOCKED: git push requires explicit user approval. Do not push without being asked." >&2
    exit 2
fi

exit 0
