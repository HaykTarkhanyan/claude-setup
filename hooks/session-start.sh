#!/bin/bash
# SessionStart hook - comprehensive orientation at conversation start
# Shows git status, recent activity, open PRs, and pending memory items
#
# Customize: Change the REPOS array and MEMORY_DIR for your project.
#
# Usage in settings.json:
#   "SessionStart": [{ "matcher": "startup", "hooks": [{ "type": "command", "command": "bash path/to/session-start.sh" }] }]

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"

# --- Configure these for your project ---
REPOS=()  # e.g., REPOS=(api frontend tests) for a monorepo. Leave empty for single-repo.
MEMORY_DIR="$HOME/.claude/projects/$(echo "$PROJECT_DIR" | sed 's|[/:]|-|g')/memory"

echo "============================================" >&2
echo "  SESSION START - $(date '+%Y-%m-%d %H:%M')" >&2
echo "============================================" >&2

if [ ${#REPOS[@]} -eq 0 ]; then
    # Single repo mode
    if [ -d "$PROJECT_DIR/.git" ]; then
        BRANCH=$(git -C "$PROJECT_DIR" branch --show-current 2>/dev/null)
        CHANGES=$(git -C "$PROJECT_DIR" status --porcelain 2>/dev/null | wc -l | tr -d ' ')
        LAST_COMMIT=$(git -C "$PROJECT_DIR" log -1 --format="%h %s" 2>/dev/null)
        echo "" >&2
        echo "=== REPO STATUS ===" >&2
        echo "  Branch: $BRANCH | Uncommitted: $CHANGES" >&2
        echo "  Last: $LAST_COMMIT" >&2
    fi
else
    # Monorepo mode - fetch all repos in parallel
    for repo in "${REPOS[@]}"; do
        REPO_DIR="$PROJECT_DIR/$repo"
        if [ -d "$REPO_DIR/.git" ]; then
            timeout 5 git -C "$REPO_DIR" fetch --quiet 2>/dev/null &
        fi
    done
    wait

    echo "" >&2
    echo "=== REPO STATUS ===" >&2
    for repo in "${REPOS[@]}"; do
        REPO_DIR="$PROJECT_DIR/$repo"
        if [ -d "$REPO_DIR/.git" ]; then
            BRANCH=$(git -C "$REPO_DIR" branch --show-current 2>/dev/null)
            CHANGES=$(git -C "$REPO_DIR" status --porcelain 2>/dev/null | wc -l | tr -d ' ')
            BEHIND=$(git -C "$REPO_DIR" rev-list --count HEAD..@{u} 2>/dev/null || echo "?")
            AHEAD=$(git -C "$REPO_DIR" rev-list --count @{u}..HEAD 2>/dev/null || echo "?")
            LAST_COMMIT=$(git -C "$REPO_DIR" log -1 --format="%h %s" 2>/dev/null)
            echo "  $repo ($BRANCH) - $CHANGES uncommitted, ahead:$AHEAD behind:$BEHIND" >&2
            echo "    last: $LAST_COMMIT" >&2
            if [ "$BEHIND" != "0" ] && [ "$BEHIND" != "?" ]; then
                echo "    WARNING: BEHIND REMOTE by $BEHIND commits - consider git pull" >&2
            fi
        fi
    done

    # Recent commits across repos (last 24h)
    echo "" >&2
    echo "=== RECENT ACTIVITY (last 24h) ===" >&2
    HAS_RECENT=false
    for repo in "${REPOS[@]}"; do
        REPO_DIR="$PROJECT_DIR/$repo"
        if [ -d "$REPO_DIR/.git" ]; then
            RECENT=$(git -C "$REPO_DIR" log --all --oneline --since="24 hours ago" 2>/dev/null | head -3)
            if [ -n "$RECENT" ]; then
                HAS_RECENT=true
                echo "  $repo:" >&2
                echo "$RECENT" | while read line; do echo "    $line" >&2; done
            fi
        fi
    done
    $HAS_RECENT || echo "  (none)" >&2
fi

# --- Pending items from memory ---
if [ -f "$MEMORY_DIR/MEMORY.md" ]; then
    echo "" >&2
    echo "=== REMINDERS ===" >&2
    PENDING=$(python -c "
import re
with open('$MEMORY_DIR/MEMORY.md', 'r') as f:
    content = f.read()
match = re.search(r'## Pending\n(.*?)(?=\n## |\Z)', content, re.DOTALL)
if match:
    lines = [l.strip() for l in match.group(1).strip().split('\n') if l.strip().startswith('-')]
    for l in lines[:5]:
        print(l)
" 2>/dev/null)
    if [ -n "$PENDING" ]; then
        echo "$PENDING" | while read line; do echo "  $line" >&2; done
    fi
fi

echo "" >&2
echo "============================================" >&2
echo "  Ready." >&2
echo "============================================" >&2

exit 0
