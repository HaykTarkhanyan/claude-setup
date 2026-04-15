# MCP Servers

## Connected (personal setup)

| Server | What it does | Access |
|--------|-------------|--------|
| **Google Calendar** | Read/write events, find free time, suggest meeting times | OAuth |
| **Gmail** | Read/search only (write blocked by hook) | OAuth |
| **Google Drive** | Read, search, create files | OAuth |
| **Notion** | Search, create/update pages, databases, comments | OAuth |
| **Telegram** | Read/reply via bot + custom reader MCP for chat history | Bot token + API keys |
| **Context7** | Live library/framework documentation lookup | Free |

## Setup commands

### Context7 - live library docs (no hallucinated APIs)
```bash
claude mcp add context7 -- npx -y @upstash/context7-mcp@latest
```
Say "use context7" in prompt to get current API docs.

### Sequential Thinking - deeper reasoning
```bash
claude mcp add seq-think -- npx -y @modelcontextprotocol/server-sequential-thinking
```
Best for: architecture decisions, scope discovery, multi-step planning. 60-70% time savings reported on complex features.

### Playwright - browser automation
```bash
claude mcp add playwright npx @playwright/mcp@latest
```
Automated testing, screenshots, form filling.

### GitHub - repo integration
```
/install-github-app
```
Enables @claude in issues/PRs, auto PR reviews, custom instructions per repo.

## How MCP tools load

MCP tools lazy-load via `ToolSearch` - hundreds of tools available without context bloat. Only loaded when actually needed.
