# Dining ROI

Ask an LLM the same question three ways: **which menu items are the best value — the lowest markup over raw ingredient cost?** Attach `menu/menu.pdf` and run the steps in order.

## Step 1 — model alone
> I want the best bang for my buck on this menu. Which 3 dishes give me the most food value for the money? Rank them and explain.

## Step 2 — with the expertise skill
> Use your restaurant markup expertise to estimate each dish's markup (menu price vs. raw ingredient cost) and rank the best-value dishes.

## Step 3 — with real data + tools
> Use the dining-roi tools to compute the actual markup of every dish from real ingredient costs. Rank the best and worst value. Show your work.

## Setup
**Skill (Step 2)** — copy in, then start a new conversation:
```
cp -R skills/dining-roi-expertise ~/.claude/skills/
```
**MCP server (Step 3)** — add to `~/Library/Application Support/Claude/claude_desktop_config.json`, then fully quit and reopen Claude Desktop:
```json
{ "mcpServers": { "dining-roi": { "command": "python3", "args": ["/ABSOLUTE/PATH/TO/dining-roi-demo/mcp/mcp_server.py"] } } }
```
python3 only, zero dependencies. Bundled plugin (server + skill): `plugin/dining-roi/`.
