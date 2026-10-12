# Handoff: Read-Only Telegram MCP Server

**Audience:** an LLM assistant (Claude Code, Cursor, etc.) helping a *new person* stand up their own copy of this MCP server on their own machine and their own Telegram account.

**Goal:** give the person a working MCP server that lets their AI assistant **read** their Telegram — list chats, read message history, and full-text search — without ever sending, editing, or deleting anything.

Read this whole file before you start guiding. It is written so you can drive the setup end to end. Do not skip the security section.

---

## 0. What this is (and what it is NOT)

- It is a small Python MCP server built on **Telethon**, which logs into Telegram as a **real user account over MTProto**. That is why it can read chat history and do server-side search.
- It is **NOT** a Telegram bot. A bot (Bot API) cannot read history or search old messages — it only sees new messages sent directly to it. If the person only wants a bot, this is the wrong tool.
- It is **read-only by design**. The server exposes only read tools. There is no send/edit/delete tool anywhere in the code. Keep it that way unless the person explicitly asks to add write capability (and warn them if they do).

Tools it exposes:

| Tool | What it does |
|---|---|
| `get_me` | Profile of the logged-in account |
| `list_chats` | List conversations (filter by type / name substring) |
| `read_chat` | Read messages from one chat (by id or `@username`) |
| `search_messages` | Full-text search, globally or within one chat |
| `get_chat_info` | Details about a user / group / channel |

---

## 1. Install Python + pip (from scratch)

Assume **nothing** is installed. **You (the LLM) install it yourself by running the commands below in your shell tool** — do not tell the human to open a browser and click through a GUI installer. First check whether Python already exists; only install if it does not. Do not go further until `python --version` and `python -m pip --version` both succeed.

### Check first (all platforms)

```bash
python --version || python3 --version || py --version
```
If this prints `3.10` or newer, skip to section 1b. Otherwise install below.

### Windows

**Preferred — winget** (ships with Windows 10/11; installs Python *and* adds it to PATH automatically, no GUI, no admin needed for a user-scope install):

```powershell
winget install -e --id Python.Python.3.13 --silent --accept-package-agreements --accept-source-agreements
```

winget edits PATH in a way the *current* shell does not see. **Open a new shell** (or refresh PATH) before verifying:
```powershell
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
python --version
python -m pip --version
```

**Fallback — no winget available** (older Windows, or `winget` not found): download the official installer and run it *silently* with the PATH flag set. `PrependPath=1` is the command-line equivalent of the "Add python.exe to PATH" checkbox, so no human interaction is needed:

```powershell
# Pick the current 3.x version. If this URL 404s, fetch https://www.python.org/downloads/
# to read the latest version number and substitute it in both places below.
$ver = "3.13.1"
$exe = "$env:TEMP\python-$ver-amd64.exe"
Invoke-WebRequest "https://www.python.org/ftp/python/$ver/python-$ver-amd64.exe" -OutFile $exe
# Silent, per-user install, added to PATH, skip the test suite:
Start-Process -Wait $exe -ArgumentList '/quiet','InstallAllUsers=0','PrependPath=1','Include_test=0'
```
Flags (from the official installer docs): `/quiet` = no UI, `InstallAllUsers=0` = per-user (no admin), `PrependPath=1` = add to PATH, `Include_test=0` = skip the stdlib test suite. Then open a new shell and verify as above.

> If `python` launches the Microsoft Store stub instead of running, PATH was not set — use `py -3` and `py -3 -m pip` instead, or reinstall via winget.

### macOS

```bash
# If Homebrew is missing, install it first (non-interactive):
which brew || NONINTERACTIVE=1 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install python
python3 --version
python3 -m pip --version
```
On macOS use `python3` / `pip3` everywhere this guide says `python` / `pip`.

### Linux (Debian/Ubuntu)

```bash
sudo apt update && sudo apt install -y python3 python3-pip python3-venv
python3 --version
python3 -m pip --version
```

> Requirement: **Python 3.10 or newer.** The server uses `str | None` type hints, which fail to parse on 3.9 and older. If `--version` shows 3.9.x or lower, install a newer one.

> **Faster alternative — `uv`** (installs itself *and* Python via one command, no GUI): Windows `powershell -c "irm https://astral.sh/uv/install.ps1 | iex"`, macOS/Linux `curl -LsSf https://astral.sh/uv/install.sh | sh`. Then `uv python install 3.13` and later use `uv venv` + `uv pip install -r requirements.txt`, skipping the venv/pip steps. Optional; plain Python + pip below works fine.

## 1b. Get Telegram API credentials

These are per-account and free:
- Go to https://my.telegram.org and log in with the phone number of the account they want to read.
- Open **API development tools**, create an app (any name, e.g. "mcp reader"), platform "Desktop".
- Copy the **`api_id`** (a number) and **`api_hash`** (a hex string). These are secrets — treat like a password.
- The phone must be able to receive the Telegram login code (it arrives in the Telegram app itself, or by SMS).

> The `api_id` / `api_hash` are NOT the same as a bot token. Do not let them paste a `bot123:ABC...` token here — that will not work.

---

## 2. Get the files

The server is three small files plus (after auth) a session file:

```
mcp_server/
  telegram_mcp_server.py    # the server (the only file that matters)
  requirements.txt          # telethon>=1.36.0, mcp>=1.10.0
  .env.example              # template for the two secrets
  telegram_reader.session   # created LATER by --auth; DO NOT copy from anyone
```

Two ways to get them:

- **Preferred:** copy `telegram_mcp_server.py`, `requirements.txt`, and `.env.example` from the source repo into a new folder on the person's machine.
- **No repo access:** recreate `telegram_mcp_server.py` from the full source in **Appendix A** at the bottom of this file, and create `requirements.txt` with:
  ```
  telethon>=1.36.0
  mcp>=1.10.0
  ```

**Do NOT copy anyone else's `telegram_reader.session` file.** It is a live login to their account. Each person generates their own in step 4.

---

## 3. Install the Python dependencies

Only two packages are needed: `telethon` and `mcp`. Install them into a **virtual environment** (venv) — a self-contained folder of packages — so this does not touch the system Python.

Step by step, from inside the server folder:

```bash
# 1. Move into the folder that has requirements.txt
cd path/to/mcp_server

# 2. Create a venv named .venv
python -m venv .venv          # macOS/Linux: python3 -m venv .venv

# 3. Activate it (this is per-terminal; re-run it every new terminal)
#    Windows PowerShell:
.venv\Scripts\Activate.ps1
#    Windows CMD:
#    .venv\Scripts\activate.bat
#    macOS/Linux/Git Bash:
#    source .venv/bin/activate

# 4. Upgrade pip, then install the two deps
python -m pip install --upgrade pip
pip install -r requirements.txt
```

After activation the prompt usually shows `(.venv)` at the front — that means you are inside the venv and `pip`/`python` point at it.

If Windows PowerShell blocks `Activate.ps1` with an execution-policy error, run once:
`Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned` and try again. (Or skip activation and call the venv Python directly: `.venv\Scripts\python.exe -m pip install -r requirements.txt`.)

**Verify the install worked** — this must print `ok`:
```bash
python -c "import telethon, mcp; print('ok')"
```
If it errors with `ModuleNotFoundError`, the venv is not active or pip installed into a different Python — re-activate (step 3) and re-run step 4.

> Note which Python this venv uses — you will point the MCP config at it in step 5 (`.venv\Scripts\python.exe` on Windows, `.venv/bin/python` on Unix).

---

## 4. First-time authentication (one-time, interactive)

The server reads two environment variables: `TELEGRAM_API_ID` and `TELEGRAM_API_HASH`. Set them, then run the auth flow. Auth is **interactive** — it asks for the phone number, then a login code, and possibly a 2FA password — so it must be run by hand in a terminal, not by the LLM in the background.

**Run this in the same terminal where the venv from step 3 is active** (prompt shows `(.venv)`), or the `telethon` import will fail. If you opened a fresh terminal, re-activate first (step 3), or call the venv Python directly, e.g. `.venv\Scripts\python.exe telegram_mcp_server.py --auth`.

```bash
# Set the secrets for this shell (use the person's real values):
# Windows PowerShell:
$env:TELEGRAM_API_ID="1234567"; $env:TELEGRAM_API_HASH="abcdef0123456789abcdef0123456789"
# macOS/Linux / Git Bash:
export TELEGRAM_API_ID="1234567"; export TELEGRAM_API_HASH="abcdef0123456789abcdef0123456789"

python telegram_mcp_server.py --auth
```

What happens:
1. It prompts for the phone number in international format (e.g. `+491701234567`).
2. Telegram sends a login code (in-app or SMS). It prompts for the code.
3. If the account has 2FA / a cloud password, it prompts for that too.
4. On success it prints `Authenticated as: <name> (@username)` and writes `telegram_reader.session` next to the script.

After this, the session file lets the server log in silently. The person will not be asked for the code again unless the session is revoked or the file is deleted.

> **Tip:** keeping the secrets in the shell is fine for the one-time auth. For the running server, pass them via the MCP config `env` block (step 5) so they are always available.

---

## 5. Register the server with the MCP client

The server speaks MCP over **stdio** (`mcp.run(transport="stdio")`), so any MCP-capable client launches it as a subprocess.

### Claude Code — project config (`.mcp.json` in the repo root)

Point `command` at the **venv Python from step 3** (not bare `python`), so `telethon`/`mcp` are importable. Use absolute paths to avoid "works in my terminal, fails in the client" surprises. On Windows JSON, backslashes must be doubled (`\\`).

```json
{
  "mcpServers": {
    "telegram-reader": {
      "command": "C:\\path\\to\\mcp_server\\.venv\\Scripts\\python.exe",
      "args": ["C:\\path\\to\\mcp_server\\telegram_mcp_server.py"],
      "env": {
        "TELEGRAM_API_ID": "REPLACE_WITH_THEIR_API_ID",
        "TELEGRAM_API_HASH": "REPLACE_WITH_THEIR_API_HASH"
      }
    }
  }
}
```

On macOS/Linux the `command` is `/path/to/mcp_server/.venv/bin/python` and forward slashes need no escaping.

Key points to get right:
- **Name it `telegram-reader`** (or another unique name), NOT `telegram`. Many setups already have a built-in Telegram *bot* plugin registered under `telegram`; reusing that name causes a tool-name collision. Using a distinct name means the tools show up as `mcp__telegram-reader__*`.
- **`command` must be the venv Python**, otherwise the client launches a Python without `telethon`/`mcp` and the server dies on import. Bare `"python"` only works if the deps happen to be in the system Python (no venv) — the fragile case this guide's venv step avoids.
- Prefer **absolute paths** for both `command` and `args`. A relative `args` path is resolved against wherever the MCP client is launched (the repo root for Claude Code project config), which is easy to get wrong.
- The two `env` values are the same secrets from step 4. They are stored in plaintext in the config file — see security notes.

Alternatively, from the CLI: `claude mcp add telegram-reader -- python /abs/path/telegram_mcp_server.py` and then set the env vars (or export them in the shell before launching Claude Code).

### Other MCP clients (Cursor, etc.)

Same idea — a stdio server entry with `command: python`, `args: [<path to script>]`, and the two env vars. Consult that client's MCP config docs for the exact file location.

After editing config, **restart the MCP client** so it picks up the new server. Confirm the tools appear (e.g. ask the assistant to call `get_me` — it should return the account profile).

---

## 6. Smoke test

Have the assistant (or the person) exercise each tool once:
- `get_me` → returns their name/username. Proves auth + connection work.
- `list_chats` with `limit: 10` → returns recent conversations.
- `read_chat` with a `chat_id` from the list → returns messages.
- `search_messages` with some `query` → returns matches.

If `get_me` works but others do not, it is almost always a bad `chat_id` (use the numeric `id` from `list_chats`, or an `@username`).

---

## 7. Security — say this out loud to the person

This is the part that matters most. Reading someone's whole Telegram is high-trust.

1. **The `.session` file is a full login.** Anyone who has `telegram_reader.session` can read (and, with different code, act as) the account **without the password or a code**. Treat it like a private SSH key.
   - Never commit it to git. Add to `.gitignore`: `*.session` and `*.session-journal`.
   - Never send it to anyone, never sync it to a shared drive, never copy someone else's.
2. **`api_id` / `api_hash` are secrets.** Do not paste them into chats, issues, or public repos. If they leak, revoke the app at https://my.telegram.org.
3. **The env values live in plaintext in the MCP config.** If the config file is in a repo, either keep the repo private or move the secrets to environment variables / a local-only untracked file.
4. **This logs in as a real user, not a bot.** All of that account's private chats are readable. Make sure the person actually wants their assistant to have that. If they only need one group, they still get access to everything — there is no per-chat scoping.
5. **To revoke access:** in Telegram → Settings → Devices/Active Sessions, terminate the "Telethon"/session, and/or delete the local `.session` file. Deleting the file forces a fresh `--auth`.

Also add a `.gitignore` in the server folder:
```
*.session
*.session-journal
.env
```

---

## 8. Troubleshooting

| Symptom | Cause / fix |
|---|---|
| `TELEGRAM_API_ID and TELEGRAM_API_HASH must be set` | The env vars are not reaching the process. Put them in the MCP config `env` block, or export before launching. |
| `Telegram session not authorized. Run: ... --auth` | No valid `.session` file. Run step 4 in the same folder, with the env vars set. |
| `ModuleNotFoundError: telethon` (or `mcp`) | Deps installed in a different Python than the one `command` points to. Point `command` at the venv Python. |
| Auth hangs / no code arrives | Wrong phone format (use `+countrycode...`), or code went to the Telegram app not SMS — check the app. |
| `FloodWaitError` | Too many auth attempts. Wait the number of seconds Telegram reports, then retry. |
| Tools do not appear in the client | Config not reloaded (restart client), wrong path in `args`, or name collided with an existing `telegram` server (rename to `telegram-reader`). |
| `database is locked` on the `.session` | Two processes using the same session file at once. Only run one instance. |

---

## 9. If the person wants to change something

- **Add more read tools** (e.g. list group members, get pinned messages): follow the existing pattern — a new `@mcp.tool()` async function that pulls `client` from `ctx.request_context.lifespan_context["client"]` and returns `json.dumps(...)`.
- **Add write capability** (send/edit): possible with Telethon, but this crosses from read-only to full account control. Warn the person explicitly and get clear consent before adding it. Consider keeping write tools in a *separate* server so the read-only one stays trustable.
- **Change the session location:** set `TELEGRAM_SESSION_PATH` env var (the code already honors it).

---

## Appendix A — full source of `telegram_mcp_server.py`

If the person cannot copy the file from the repo, recreate it verbatim from below.

```python
"""
Read-only Telegram MCP server for Claude Code.

Exposes tools to list chats, read messages, and search — never sends or modifies anything.

Usage:
    First-time auth:  python telegram_mcp_server.py --auth
    MCP server mode:  python telegram_mcp_server.py
"""

import json
import os
import sys
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path

from mcp.server.fastmcp import FastMCP, Context
from telethon import TelegramClient
from telethon.tl.types import User, Chat, Channel

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

API_ID = os.environ.get("TELEGRAM_API_ID")
API_HASH = os.environ.get("TELEGRAM_API_HASH")

SCRIPT_DIR = Path(__file__).parent
SESSION_PATH = Path(
    os.environ.get("TELEGRAM_SESSION_PATH", str(SCRIPT_DIR / "telegram_reader"))
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _chat_type(entity) -> str:
    if isinstance(entity, User):
        return "bot" if entity.bot else "personal"
    if isinstance(entity, Chat):
        return "group"
    if isinstance(entity, Channel):
        return "channel" if entity.broadcast else "group"
    return "unknown"


def _serialize_date(dt) -> str | None:
    if dt is None:
        return None
    return dt.isoformat()


def _message_to_dict(msg, chat_name: str | None = None) -> dict:
    d = {
        "id": msg.id,
        "date": _serialize_date(msg.date),
        "from_id": msg.sender_id,
        "text": msg.text or "",
    }
    if msg.sender:
        if isinstance(msg.sender, User):
            name_parts = [msg.sender.first_name or "", msg.sender.last_name or ""]
            d["from_name"] = " ".join(p for p in name_parts if p)
        else:
            d["from_name"] = getattr(msg.sender, "title", str(msg.sender_id))
    if msg.reply_to:
        d["reply_to_msg_id"] = msg.reply_to.reply_to_msg_id
    if msg.media:
        d["media_type"] = type(msg.media).__name__
    if chat_name is not None:
        d["chat_name"] = chat_name
    return d


# ---------------------------------------------------------------------------
# Lifespan: manage a single Telethon client for the server's lifetime
# ---------------------------------------------------------------------------

@asynccontextmanager
async def app_lifespan(server: FastMCP):
    if not API_ID or not API_HASH:
        raise RuntimeError(
            "TELEGRAM_API_ID and TELEGRAM_API_HASH must be set. "
            "Get them at https://my.telegram.org"
        )

    client = TelegramClient(str(SESSION_PATH), int(API_ID), API_HASH)
    await client.connect()

    if not await client.is_user_authorized():
        await client.disconnect()
        raise RuntimeError(
            "Telegram session not authorized. "
            "Run: python telegram_mcp_server.py --auth"
        )

    try:
        yield {"client": client}
    finally:
        await client.disconnect()


# ---------------------------------------------------------------------------
# MCP Server
# ---------------------------------------------------------------------------

mcp = FastMCP("Telegram Reader (read-only)", lifespan=app_lifespan)


@mcp.tool()
async def get_me(ctx: Context) -> str:
    """Get the authenticated Telegram user's profile info."""
    client: TelegramClient = ctx.request_context.lifespan_context["client"]
    me = await client.get_me()
    return json.dumps({
        "id": me.id,
        "first_name": me.first_name,
        "last_name": me.last_name,
        "username": me.username,
        "phone": me.phone,
    }, ensure_ascii=False)


@mcp.tool()
async def list_chats(
    ctx: Context,
    limit: int = 50,
    chat_type: str | None = None,
    query: str | None = None,
) -> str:
    """List Telegram conversations.

    Args:
        limit: Max number of chats to return (default 50).
        chat_type: Filter by type: "personal", "group", "channel", "bot".
        query: Filter chat names (case-insensitive substring match).
    """
    client: TelegramClient = ctx.request_context.lifespan_context["client"]
    results = []
    async for dialog in client.iter_dialogs():
        if len(results) >= limit:
            break

        entity = dialog.entity
        ctype = _chat_type(entity)

        if chat_type and ctype != chat_type:
            continue

        name = dialog.name or ""
        if query and query.lower() not in name.lower():
            continue

        results.append({
            "id": dialog.id,
            "name": name,
            "type": ctype,
            "unread_count": dialog.unread_count,
            "last_message_date": _serialize_date(dialog.date),
            "last_message_preview": (dialog.message.text or "")[:100] if dialog.message else "",
        })

    return json.dumps(results, ensure_ascii=False)


@mcp.tool()
async def read_chat(
    ctx: Context,
    chat_id: str,
    limit: int = 50,
    offset_date: str | None = None,
) -> str:
    """Read messages from a specific chat.

    Args:
        chat_id: Chat ID (number) or @username.
        limit: Number of messages to fetch (default 50, max 200).
        offset_date: Only return messages before this ISO date (e.g. "2025-01-15").
    """
    client: TelegramClient = ctx.request_context.lifespan_context["client"]
    limit = min(limit, 200)

    entity_id = int(chat_id) if chat_id.lstrip("-").isdigit() else chat_id
    entity = await client.get_entity(entity_id)

    kwargs = {"entity": entity, "limit": limit}
    if offset_date:
        kwargs["offset_date"] = datetime.fromisoformat(offset_date).replace(
            tzinfo=timezone.utc
        )

    messages = []
    async for msg in client.iter_messages(**kwargs):
        messages.append(_message_to_dict(msg))

    return json.dumps(messages, ensure_ascii=False)


@mcp.tool()
async def search_messages(
    ctx: Context,
    query: str,
    chat_id: str | None = None,
    limit: int = 20,
) -> str:
    """Full-text search across Telegram messages.

    Args:
        query: Search text.
        chat_id: Limit search to a specific chat (ID or @username). Omit to search globally.
        limit: Max results (default 20, max 100).
    """
    client: TelegramClient = ctx.request_context.lifespan_context["client"]
    limit = min(limit, 100)

    entity = None
    if chat_id:
        entity_id = int(chat_id) if chat_id.lstrip("-").isdigit() else chat_id
        entity = await client.get_entity(entity_id)

    results = []
    async for msg in client.iter_messages(entity, search=query, limit=limit):
        chat_name = ""
        if msg.chat:
            chat_name = getattr(msg.chat, "title", None) or getattr(msg.chat, "first_name", "") or ""
        results.append(_message_to_dict(msg, chat_name=chat_name))

    return json.dumps(results, ensure_ascii=False)


@mcp.tool()
async def get_chat_info(ctx: Context, chat_id: str) -> str:
    """Get detailed info about a chat (user, group, or channel).

    Args:
        chat_id: Chat ID (number) or @username.
    """
    client: TelegramClient = ctx.request_context.lifespan_context["client"]
    entity_id = int(chat_id) if chat_id.lstrip("-").isdigit() else chat_id
    entity = await client.get_entity(entity_id)

    info = {
        "id": entity.id,
        "type": _chat_type(entity),
    }

    if isinstance(entity, User):
        info["first_name"] = entity.first_name
        info["last_name"] = entity.last_name
        info["username"] = entity.username
        info["phone"] = entity.phone
        info["bot"] = entity.bot
    elif isinstance(entity, (Chat, Channel)):
        info["title"] = entity.title
        if isinstance(entity, Channel):
            info["username"] = entity.username
            info["members_count"] = entity.participants_count

    return json.dumps(info, ensure_ascii=False)


# ---------------------------------------------------------------------------
# Interactive auth (one-time setup)
# ---------------------------------------------------------------------------

async def _run_auth():
    if not API_ID or not API_HASH:
        print("Error: set TELEGRAM_API_ID and TELEGRAM_API_HASH environment variables.")
        print("Get them at https://my.telegram.org")
        sys.exit(1)

    client = TelegramClient(str(SESSION_PATH), int(API_ID), API_HASH)
    print("Starting Telegram authentication...")
    print(f"Session will be saved to: {SESSION_PATH}.session")
    await client.start()
    me = await client.get_me()
    print(f"Authenticated as: {me.first_name} {me.last_name or ''} (@{me.username})")
    await client.disconnect()
    print("Done! You can now use the MCP server.")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    if "--auth" in sys.argv:
        import asyncio
        asyncio.run(_run_auth())
    else:
        mcp.run(transport="stdio")
```

---

## Appendix B — how the code works (for an LLM adapting it)

- **Config via env vars** (`API_ID`, `API_HASH`) read at import; `SESSION_PATH` defaults next to the script but is overridable via `TELEGRAM_SESSION_PATH`. Telethon appends `.session` to that path.
- **`app_lifespan`** is a FastMCP lifespan context manager: on server start it connects one `TelegramClient` and checks `is_user_authorized()`; if not authorized it raises with a clear message telling the user to run `--auth`. The single client is yielded in a dict and reused by every tool via `ctx.request_context.lifespan_context["client"]`. On shutdown it disconnects.
- **Each tool** is an `async` function decorated with `@mcp.tool()`, takes `ctx: Context` plus typed args (which FastMCP turns into the tool's JSON schema from the type hints + docstring), and returns a JSON string (`ensure_ascii=False` so non-Latin text like Armenian/Cyrillic is preserved, not escaped).
- **`chat_id` handling:** the helper `int(chat_id) if chat_id.lstrip("-").isdigit() else chat_id` lets a tool accept either a numeric id (including negative group ids) or an `@username`.
- **Read-only guarantee:** it only ever calls Telethon read methods (`iter_dialogs`, `iter_messages`, `get_entity`, `get_me`). No `send_message`, no `edit_message`, no `delete_messages` anywhere. Adding any of those breaks the read-only guarantee — do it only on explicit request.
- **`--auth` branch** runs `client.start()`, which performs Telethon's interactive login (phone → code → optional 2FA) and writes the session file. Kept separate from `mcp.run()` so normal server startup never blocks on input.
