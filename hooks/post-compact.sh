#!/bin/bash
# PostCompact hook - reinjects critical context after context window compaction
# This runs after Claude's context is compressed, so important rules may be lost.
#
# Customize: Replace the REMINDER block with your project's critical rules.
#
# Usage in settings.json:
#   "PostCompact": [{ "matcher": "", "hooks": [{ "type": "command", "command": "bash path/to/post-compact.sh" }] }]

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"

cat >&2 <<'REMINDER'
=== POST-COMPACT CRITICAL REMINDERS ===

RULES:
1. Never git push without explicit user approval
2. Re-read files after edits to verify correctness
3. Use logging, not print. Use uv, not pip.

=== END REMINDERS ===
REMINDER

# Show current branch state for orientation
echo "" >&2
echo "CURRENT STATE:" >&2
if [ -d "$PROJECT_DIR/.git" ]; then
    BRANCH=$(git -C "$PROJECT_DIR" branch --show-current 2>/dev/null)
    CHANGES=$(git -C "$PROJECT_DIR" status --porcelain 2>/dev/null | wc -l | tr -d ' ')
    echo "  Branch: $BRANCH ($CHANGES uncommitted)" >&2
fi

exit 0
