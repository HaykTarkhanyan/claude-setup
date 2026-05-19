# Setting Up Terminal for Claude Code

Personal reference for Claude Code terminal configuration on Windows 11 + Git Bash.

## First-time setup

Run Claude's built-in terminal setup command:
```bash
claude setup-terminal
```
This configures your shell (bash/zsh) with completions, keybindings, and PATH integration. Re-run after major updates.

## Shell Aliases

`kachayt` and `kachaytr` are shortcuts for running Claude Code with auto-approve (no permission prompts). Defined in all 3 shells:

| Command     | What it does                                           |
|-------------|--------------------------------------------------------|
| `kachayt`   | `claude --dangerously-skip-permissions`                |
| `kachaytr`  | `claude --dangerously-skip-permissions --resume`       |

Where they live:
- **Git Bash:** `~/.bashrc` (alias)
- **CMD:** `~/bin/kachayt.bat` and `~/bin/kachaytr.bat`
- **PowerShell:** `Microsoft.PowerShell_profile.ps1` (function)

## VS Code Keybindings

File: `%APPDATA%/Code/User/keybindings.json`

These fix key sequences that Claude Code's terminal intercepts:

| Key          | What it sends      | Why                                                     |
|--------------|--------------------|----------------------------------------------------------|
| `Escape`     | `\x1b`            | Escape key works properly in terminal (vim, menus, etc.) |
| `Alt+V`      | `\x1bv`           | Alt+V passthrough to terminal                            |
| `Shift+Enter`| `\x1b\r`          | Sends escaped enter to terminal                          |
| `Alt+Enter`  | Jupyter exec       | Runs selected Python code in interactive window          |

## VS Code Terminal Tips

- Use a Nerd Font for ccstatusline icons
- Increase scrollback: `terminal.integrated.scrollback: 10000`
- Watch for `Ctrl+B` conflict (toggles sidebar in VS Code, backgrounds task in Claude)
- Remap or disable VS Code shortcuts that clash with Claude Code

## VS Code Layout Shortcut (Ctrl+Alt+K)

`Ctrl+Alt+K` splits the editor into 2 columns and opens a `Kachaytr` terminal on the right that auto-runs `claude --dangerously-skip-permissions --resume`. Used right after opening a fresh project.

Two pieces of config are needed.

**1. Terminal profile** in `%APPDATA%/Code/User/settings.json` under `terminal.integrated.profiles.windows`:

```json
"Kachaytr": {
    "path": "C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe",
    "args": ["-NoExit", "-Command", "claude --dangerously-skip-permissions --resume"],
    "icon": "robot"
}
```

**2. Keybinding** in `%APPDATA%/Code/User/keybindings.json`:

```json
{
    "key": "ctrl+alt+k",
    "command": "runCommands",
    "args": {
        "commands": [
            "workbench.action.editorLayoutTwoColumns",
            "workbench.action.focusSecondEditorGroup",
            {
                "command": "workbench.action.terminal.newWithProfile",
                "args": {
                    "profileName": "Kachaytr",
                    "location": "editor"
                }
            }
        ]
    }
}
```

Notes:
- Command is hardcoded in the profile (not via `kachaytr.bat`) to avoid PATH dependencies in PowerShell.
- `editorLayoutTwoColumns` splits the editor area only; Explorer sidebar stays as a sidebar.
- Pressing twice opens two Kachaytr terminals (no dedup guard).
- `-NoExit` keeps PowerShell alive after `claude` exits.

## Settings

File: `~/.claude/settings.json`

Key settings:
- **Default permission mode:** `acceptEdits` - auto-approves file edits, prompts for shell commands
- **Effort level:** `high`
- **Voice:** enabled
- **Dangerous mode skip prompt:** enabled (so `kachayt` doesn't ask "are you sure")
- **Auto-updates:** `latest` channel
- **Telegram plugin:** enabled

### Gmail Write Block Hook

A `PreToolUse` hook blocks any Gmail write/send/modify/delete tool calls. Gmail is read-only - emails are drafted as files instead.

## MCP Servers (Integrations)

Connected services via MCP:
- **Google Calendar** - read/write events, find free time
- **Gmail** - read/search only (write blocked by hook)
- **Notion** - search, create/update pages, databases, comments
- **Telegram** - read/reply via custom bot + plugin
- **Context7** - live library/framework documentation lookup

## CLAUDE.md Files

Instructions that Claude Code reads automatically:
- `~/.claude/CLAUDE.md` - global rules (all projects): language prefs, Python defaults, Armenian text handling, communication style
- Per-project `CLAUDE.md` - project-specific rules

## Memory System

Claude Code maintains persistent memory at `~/.claude/projects/<project>/memory/`:
- `MEMORY.md` - index of all memories (auto-loaded each conversation)
- Individual `.md` files for user profile, feedback, project context, references
- Memories persist across conversations - no need to re-explain preferences

## Useful Commands

| Command          | What it does                                    |
|------------------|-------------------------------------------------|
| `claude`         | Start new conversation                          |
| `claude --resume`| Resume last conversation                        |
| `kachayt`        | Start with all permissions auto-approved        |
| `kachaytr`       | Resume last conversation with auto-approve      |
| `/morning`       | Daily briefing (calendar, email, telegram)      |
| `/eod`           | End of day review                               |
| `/mcp`           | Check MCP server connections                    |
| `/help`          | Show help                                       |
| `Esc` then `:`   | Enter vim-style command mode in terminal        |
