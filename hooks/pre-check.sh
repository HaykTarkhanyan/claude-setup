#!/bin/bash
# PreToolUse hook - blocks edits to secret files
# Add project-specific checks (e.g., smart quote validation) as needed.
#
# Usage in settings.json:
#   "PreToolUse": [{ "matcher": "Edit|Write", "hooks": [{ "type": "command", "command": "bash path/to/pre-check.sh" }] }]

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | python -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('file_path',''))" 2>/dev/null)
[ -z "$FILE_PATH" ] && exit 0

# === Secret file protection (fast string match) ===
BASENAME=$(basename "$FILE_PATH")
case "$BASENAME" in
    *.env*|*credentials*|*serviceAccountKey*|*.pem|*.key)
        echo "BLOCKED: Editing $BASENAME is not allowed - may contain secrets. If intentional, edit manually." >&2
        exit 2
        ;;
esac

exit 0
