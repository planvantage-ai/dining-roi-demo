# Dining ROI

Ask an LLM the same question three ways: **which menu items are the best value — the lowest markup over raw ingredient cost?** Attach `menu/menu.pdf` and run the steps in order. (Claude Desktop, macOS.)

## Step 1 — model alone
> I want the best bang for my buck on this menu. Which 3 dishes give me the most food value for the money? Rank them and explain.

## Step 2 — add the expertise skill
Settings → Capabilities → Skills (or Customize → Skills) → **Create skill** → upload **`dist/dining-roi-expertise-skill.zip`**, toggle it on, then start a new chat.
> Use your restaurant markup expertise to estimate each dish's markup (menu price vs. raw ingredient cost) and rank the best-value dishes.

## Step 3 — add real data + tools
Settings → **Extensions** → drag in **`dist/dining-roi.mcpb`** (or Advanced → Install Extension…), then enable it.
> Use the dining-roi tools to compute the actual markup of every dish from real ingredient costs. Rank the best and worst value. Show your work.

Requires python3 (preinstalled on macOS); skills require code execution enabled in Settings.
