---
name: dining-roi-analysis
description: Compute true menu markups using the dining-roi MCP tools. Use when asked for the best-value dishes with real cost data.
---

# Dining ROI Analysis (Deterministic Pass)

This is the **data + deterministic tools** pass. Same model, but now with real wholesale
ingredient costs and deterministic MCP tools instead of priors. The job: find the menu items
with the **lowest markup multiple** (best value for the diner), and show your work so anyone
can audit it.

**Core metric:** `markup_multiple = menu_price / food_cost`. **Lower is better** for the diner.

**Hard rule:** Do not guess or anchor on menu price, dish name, or "vibes." Every number below
must come from a tool call. The whole point of this pass is that the answer is grounded,
reproducible, and explainable.

## Procedure

Work through these steps in order. Use the `dining-roi` MCP server for every data lookup and
the final cross-check.

### 1. List the dishes
Call **`list_dishes`** to get the full menu (dish id, name, category, menu_price). This is the
universe you'll rank.

### 2. Decompose every dish (one batched call)
Call **`decompose_dishes`** ONCE, passing all dish ids from step 1 in a single batched request.
This returns each dish's ingredient breakdown — the ingredients and the quantity (e.g. ounces or
each) used per plated portion. Do not loop one dish at a time; send them all together.

### 3. Price every unique ingredient (one batched call)
Collect the **distinct** ingredients across all decompositions, then call
**`price_ingredients`** ONCE with that unique list. This returns the wholesale unit cost
(per oz / per each) for each ingredient. Batch it — one call, all ingredients.

### 4. Compute food cost and markup, then rank (show the arithmetic)
For each dish, compute deterministically:

- `food_cost = Σ (ingredient_quantity × ingredient_unit_cost)` over its ingredients
- `markup_multiple = menu_price / food_cost`

Then **rank ascending by `markup_multiple`** (lowest = best value first).

Present this as an **auditable table** so a reader can re-derive every figure. Include the
per-ingredient math (quantity × unit cost) at least for the headline dishes, and the rolled-up
columns for all of them:

| Rank | Dish | Category | Menu Price | Food Cost (show terms) | Markup × |
|------|------|----------|-----------:|------------------------|---------:|
| 1 | ... | ... | $.. | (q×c) + (q×c) + … = $.. | ..× |

Round displayed money to cents and the multiple to one decimal, but compute on the raw numbers.

### 5. Cross-check with the deterministic engine
Call **`analyze_menu`**, which independently computes food_cost, markup_multiple, and the
ranking from the same source data. **Reconcile** its output against your hand-computed table.
They should match. If anything diverges, trust the deterministic tool, flag the discrepancy,
and correct your table — do not paper over it.

### 6. Present the result and call out the surprises
Lead with the **best-value** dishes (lowest multiple) and the **worst-value** dishes (highest
multiple). Then explicitly surface the counterintuitive findings — this is the payoff of using
real cost data instead of priors:

- The **best value is a pricey-looking premium item**, not a cheap one. An expensive raw
  ingredient (lump crab, lobster, a big bone-in cut) means the kitchen marks it up *less*, so
  the diner gets more actual food per dollar.
- The **worst value is a cheap-looking comfort dish** (e.g. the pasta) — exactly the item a
  cost-blind guess would praise as "best bang for the buck." Its low menu price hides a tiny
  ingredient cost and a huge multiple.
- **The ribeye beats the filet.** The prestige filet mignon looks like *the* indulgence but is
  secretly a worse deal than the humbler bone-in ribeye on a markup basis.

State plainly that menu price alone is a misleading signal, and that the ranking flips once you
divide by real ingredient cost.

## Why this pass is different

These tools are **deterministic**: the same inputs always produce the same outputs. There's no
estimation or vibe in the final numbers — every figure traces back to a wholesale cost and a
portion size, and anyone can re-run the math and land on the identical ranking. That
reproducibility and explainability is the value the data + tools add over the model alone.
