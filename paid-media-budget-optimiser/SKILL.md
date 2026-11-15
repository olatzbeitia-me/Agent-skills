---
name: paid-media-budget-optimiser
description: Reallocates a fixed weekly paid media budget across campaigns and platforms using marginal cost per conversion (what the next pound buys) rather than average cost, fitted from weekly spend and conversion history. Flags campaigns whose history is too thin or flat to trust, and spend with no recent conversions. Use when asked where to move paid media budget, whether to scale or cut a campaign, why a cheap-looking campaign should not get more money, or to plan a budget shift across Google, Microsoft, Meta and LinkedIn.
---

# Paid media budget optimiser

Answer: **if the total budget stays the same, where should each pound go next week?**

The modelling lives in `scripts/optimise.py` (Python 3, standard library only). Your job is to get comparable data, run it, sense-check what the model cannot see, and give a staged plan.

## 1. Get comparable data

Weekly rows, ideally 10 to 16 weeks per campaign:

```
week,platform,campaign,spend,conversions
2026-08-17,Google Ads,Search: brand,1612.40,40
```

Before running, confirm with the user:
- **The same conversion on every platform** (for example a qualified demo request, not "lead" on one and "page view" on another), with similar attribution windows. If one platform counts view-through conversions and another does not, fix that first or the comparison is meaningless.
- **No major structural change mid-window** (new bidding strategy, tracking break, campaign restructure). If there was one, start the history after it.

## 2. Run it

```bash
python3 scripts/optimise.py --data weekly.csv --out output/plan
```

Useful options: `--max-change 0.2` for a more cautious plan, `--reallocate-waste` to move budget out of campaigns with no recent conversions, `--currency €`.

## 3. Sense-check what the model cannot see

The curves only know spend and conversions. Before recommending, check:
- **Brand search increases**: limited by how many people search for the brand. Ask for impression share; above about 90%, extra budget mostly raises cost per click.
- **Audience size**: a LinkedIn or Meta audience can be exhausted. Ask for frequency; if it is already high, more budget means seeing the same people more often.
- **Learning phases**: large changes can reset automated bidding. That is why the plan caps changes and stages them.
- **Campaign purpose**: an awareness campaign judged on conversions will always look like waste. Say so rather than recommending a cut by default.

## 4. Write the answer

1. The headline: same budget, predicted conversions before and after, cost per conversion before and after.
2. The moves, biggest first, each with the reason in marginal terms ("the next conversion on LinkedIn costs £240 against £98 on Microsoft Ads").
3. Held campaigns and how to make them readable (a structured spend test).
4. Possible waste, with tracking checked first.
5. A staged plan: half the change now, the rest in a fortnight if results track the prediction.

## Rules

- Never invent performance data. If history is too short, say so and recommend a test instead.
- Present predictions as estimates from past data, not guarantees.
- Explain marginal cost in plain words the first time: "what the next pound buys", not jargon.
