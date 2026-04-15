#!/bin/bash
# PreToolUse hook - blocks Gmail write operations (create, send, modify, delete, etc.)
# Keeps Gmail access read-only.
#
# This is already built into the global settings.json as inline JSON,
# but this script version can be used if you prefer file-based hooks.
#
# Usage in settings.json:
#   "PreToolUse": [{
#     "matcher": "mcp__claude_ai_Gmail__gmail_create|mcp__claude_ai_Gmail__gmail_send|mcp__claude_ai_Gmail__gmail_modify|mcp__claude_ai_Gmail__gmail_delete|mcp__claude_ai_Gmail__gmail_update|mcp__claude_ai_Gmail__gmail_trash|mcp__claude_ai_Gmail__gmail_star",
#     "hooks": [{ "type": "command", "command": "bash path/to/gmail-readonly.sh" }]
#   }]

echo '{"decision":"block","reason":"Gmail write access is blocked. Only read/search operations are allowed."}'
exit 0
