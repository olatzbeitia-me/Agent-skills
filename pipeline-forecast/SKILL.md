---
name: pipeline-forecast
description: Forecasts a quarter's marketing-sourced pipeline from funnel history, shows low, base and high scenarios, sizes the gap to target, and tests which single lever could realistically close it. Use when asked whether marketing will hit its pipeline number, to build or explain a pipeline forecast, to plan what to change after a missed or at-risk target, or to prepare a quarterly business review.
---

# Pipeline forecast

Answer three questions, in this order: **Will we hit the number? If not, by how much do we miss? What is the most realistic way to close the gap?**

The maths lives in `scripts/forecast.py` (Python 3, standard library only). Your job is to get clean inputs, run it, and turn the output into a diagnosis and a decision, not to restate the tables.

## 1. Get the inputs

You need two files. Ask for what is missing; do not invent numbers.

**Funnel history** (`funnel.csv`), one row per month, at least 3 months before the quarter (6 is better), plus any months of the current quarter that have already happened:

```
month,leads,mqls,sqls,opportunities,pipeline_value
2026-04,2100,714,286,103,1957000
```

**Quarter plan** (`plan.json`): label, the quarter's months, the pipeline target, and planned leads for each month still to come.

```json
{"quarter_label": "Q4 2026", "quarter_months": ["2026-10","2026-11","2026-12"],
 "pipeline_target": 5600000, "planned_leads": {"2026-11": 2200, "2026-12": 1700},
 "lookback_months": 6, "currency": "£"}
```

If the user only has a CRM export, help them shape it into these columns first. Confirm the stage definitions: if what counts as a marketing qualified lead changed during the window, say the rates are not comparable before forecasting.

## 2. Run it

```bash
python3 scripts/forecast.py --history funnel.csv --plan plan.json --out output/forecast
```

This writes `output/forecast.md` (the report) and `output/forecast.json` (all numbers). Read both.

## 3. Write the answer

Lead with the verdict in one sentence: base forecast, share of target, gap in money.

Then the diagnosis. Use the **warning signs** first: a falling conversion rate matters more than the gap, because it means the base forecast is generous and more volume will buy less pipeline. Say where to look for the cause (for example a channel bringing lower-quality leads, a change in qualification rules, or slower sales follow-up).

Then the recommendation. Start from the levers marked **Realistic**. If none closes the gap alone, propose a combination of smaller moves and show the arithmetic. If nothing realistic closes it, say so and recommend resetting the target with this evidence, rather than promising a stretch that recent months do not support.

End with what to watch weekly until quarter end (normally the falling rate and lead volume against plan).

## Rules

- Never fabricate history or targets. Every number in the answer must come from the user's data or the script output.
- Keep the low scenario in perspective: it puts every rate at a weak month simultaneously, so it is a floor, not a forecast.
- Name the model's limits when they apply (same-month ratios, late-quarter leads converting next quarter).
- Plain language: say "marketing qualified lead", not acronyms, unless the user uses them.
