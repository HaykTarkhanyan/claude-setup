# Claude Code Setup

Personal reference for my Claude Code configuration on Windows 11 + Git Bash.

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

