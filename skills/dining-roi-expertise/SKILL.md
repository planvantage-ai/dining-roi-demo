---
name: dining-roi-expertise
description: Restaurant menu markup expertise — estimate which dishes are the best value (lowest markup over raw ingredient cost). Use when analyzing a menu for value.
---

# Dining ROI — Menu Markup Expertise

This skill encodes restaurant-economics judgment so you can rank a menu by **value to the diner** even when you have **no cost data and no tools**. It is opinion and heuristics, not measurement. Use it to produce a directional, defensible estimate.

## The goal (don't get this wrong)

Best diner value = the **LOWEST markup multiple**, where:

```
markup_multiple = menu_price / raw_ingredient_cost
```

A **lower** multiple is **better** for the diner — you're paying less on top of the actual food.

The single most common mistake: equating "cheap menu price" with "good value." It is the opposite. A $14 pasta can be a far worse deal than a $58 steak, because the pasta is dirt-cheap to plate and the steak's raw protein is genuinely expensive. **Rank by the multiple, never by the price tag.**

## The core heuristic: the 3x line

- Restaurants target a **food cost of ~28–35% of menu price**, i.e. roughly a **3x markup** (sometimes quoted as the "33% rule").
- A dish near **3x** is priced "normally."
- A dish **BELOW the cost-share line** (cheap to make relative to its price) carries a **HIGH markup** → **worse value** for the diner.
- A dish that is **expensive to make** relative to its price sits at a **LOW markup** → **better value**.

So your job per dish: estimate the raw ingredient cost from the description, compare implied markup to ~3x, and rank ascending.

## Category tendencies (where the markup hides)

**HIGHEST markup — usually the WORST value (be skeptical of these):**
- Pasta and risotto (flour, a little cheese/egg — pennies of food, premium plating)
- Rice / grain bowls
- Fried apps (potatoes, batter, fryer oil)
- Eggs / brunch dishes
- Soda, coffee, espresso drinks
- Cocktails and spirits (huge pour-cost markups)
- Simple sides — greens, potatoes, bread, creamed/sautéed vegetables
- Desserts built on flour/sugar/dairy (bread pudding, cake)

**LOWEST markup — usually the BEST value (where the diner wins):**
- Steaks and chops **priced by weight** (ribeye, strip, porterhouse) — the protein itself is costly
- Whole fish / branzino / large seafood
- Any dish built on a genuinely **expensive raw protein**: lump crab, lobster, large gulf shrimp, scallops

The rule of thumb: **the more the plate's price is "paying for the actual animal/seafood," the better the value.** The more it's "paying for labor, ambiance, and a cheap base ingredient," the worse.

## The counterintuitive truths to flag explicitly

State these out loud when you present the ranking — they are the insight:

1. **The most expensive menu items are often the BEST value.** A $48 crab cake made of real lump crab can be a *better* multiple than a $16 side, because the crab itself nearly justifies the price.

2. **Cheap-looking comfort items are often the WORST value.** The humble pasta or the simple side dish is where the house makes its margin.

3. **A ripoff-looking dish can be a hidden gem.** High menu price + expensive raw ingredient (lobster mac, crab cakes) → surprisingly low multiple.

4. **Among steaks, prestige ≠ value.** A **by-weight bone-in ribeye** typically beats a **filet mignon** on value: the filet carries a prestige/scarcity markup that inflates its multiple even though it "feels" like the top indulgence. The priciest steak is usually *not* the best deal.

## Method

For each dish:

1. **Estimate raw ingredient cost** from the description — name the dominant cost driver (e.g., "8 oz lump crab," "16 oz bone-in ribeye," "2 oz spirits," "flour + pecorino").
2. **Divide** the menu price by your estimated cost to get the markup multiple.
3. **Sanity-check** against the ~3x line and the category tendencies above.
4. **Rank ascending** by multiple — lowest multiple first (best value).

Then present:

- A short reasoning line per dish (price, your cost estimate, the dominant ingredient, the resulting multiple).
- A **ranked table**: Dish | Menu Price | Est. Raw Cost | Markup Multiple | Verdict, sorted best value → worst.
- A one-line callout of the surprising winner and the worst "value trap."

## Honesty caveat (say this)

This is an **expert estimate without real cost data.** It gives good *directional* judgment — which dishes are likely the best and worst value, and why — but the exact multiples are educated guesses, not measured figures. With real wholesale costs and a deterministic calculator, the numbers would sharpen and any close calls could flip. Present the ranking with that confidence level.
