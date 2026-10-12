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
