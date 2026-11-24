# Paid media budget optimiser

**Same budget, more conversions: where should each pound go next week?**

Most budget reviews rank campaigns by average cost per conversion and move money towards the cheapest. That is often wrong. Average cost tells you what you paid for everything so far; what matters for the next decision is **marginal cost**: what the *next* pound buys.

## What it does

- Fits a diminishing-returns curve to each campaign's weekly spend and conversions.
- Works out the cost of the next conversion for each campaign at its current spend.
- Moves budget in small steps from the campaign where the next conversion is most expensive to the one where it is cheapest, within a cap per campaign (30% by default), keeping the total the same.
- Stays inside the spend levels each campaign has actually run at. Beyond its lowest and highest weekly spend a curve is guessing, so a campaign that reaches that edge stops there and the report suggests a test to extend it.
- Refuses to guess when the history cannot support it: too few weeks, spend that barely varied, or a poor fit. Those campaigns are held, with a spend test to make them readable.
- Flags spend with no conversions in recent weeks, and tells you to check tracking before pausing.

## Example output

12 weeks of fictional data across Google Ads, Microsoft Ads, Meta and LinkedIn. Full report: [`examples/output/budget-plan.md`](examples/output/budget-plan.md).

> Same total (£9,187 a week), predicted conversions from 99.2 to 101.7 a week (**+2%**), cost per conversion from £93 to £90.
>
> | Campaign | Now | Recommended | Average cost per conversion | Cost of the next conversion: now → after |
> |---|---:|---:|---:|---|
> | Microsoft Ads: generic search | £539 | £689 | £91 | £98 → £99 |
> | Meta: lookalike audiences | £2,202 | £1,877 | £109 | £185 → £172 |
> | LinkedIn: lead gen forms | £2,203 | £1,553 | £184 | £240 → £222 |
>
> The Meta cut stops at £1,877 because the campaign has never run below £1,860 a week, so the curve cannot say what happens lower down. Brand search has the lowest average cost (£39), but its next conversion costs £135, and the report says to check how often its ads missed searches because the budget ran out before giving it more.

## How it works, in plain terms

Think of a fruit tree. The first hour of picking fills baskets fast because the low branches are full; by the fifth hour you are on a ladder for every apple. Average cost is the cost per apple across the whole day. Marginal cost is the cost of the next apple. If another tree still has full low branches, the next hour belongs there, even if this tree's daily average looks better.

The curve is `conversions = a × spend^b`. When `b` is below 1, each extra pound buys a little less than the last. The cost of the next conversion is the slope of that curve turned upside down.

## Run it

Python 3.9 or later, no packages to install.

```bash
python3 scripts/optimise.py --data examples/weekly-performance.csv --out output/plan
python3 -m unittest discover -s tests
```

The input format and the checks to make before acting are in [`SKILL.md`](SKILL.md). With Claude Code, install the folder as a skill and ask, for example: *"Here are 12 weeks of campaign data from Google, Meta and LinkedIn. Where should we move budget?"*

## Limits

- The curves describe the past. Seasonality, new creative, bidding changes or a competitor's push can change them.
- It cannot see impression share, audience saturation or frequency. The skill instructions tell Claude to check those before recommending a move.
- Keeping inside each campaign's spend history makes the plan cautious: a campaign whose spend has only ever varied a little cannot be moved far until a test widens its history. `--allow-extrapolation` lifts the limit and flags every move that goes beyond the history.
- Conversions must mean the same thing on every platform, with similar attribution windows.
- All campaign data in `examples/` is fictional.
