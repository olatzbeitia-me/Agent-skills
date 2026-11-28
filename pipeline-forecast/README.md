# Pipeline forecast

**The question every demand generation leader gets asked mid-quarter: will we hit the pipeline number, and if not, what are we doing about it?**

This agent answers it from funnel history, and separates the levers that recent performance shows are realistic from the ones that would need a miracle.

## What it does

1. Takes monthly funnel history (leads → marketing qualified → sales qualified → opportunities → pipeline value) and the quarter's plan.
2. Builds low, base and high forecasts from the conversion rates of recent months.
3. Sizes the gap to target.
4. For each lever (lead volume, each conversion rate, average opportunity value) works out what it would need to do *on its own* to close the gap, and checks that against the best month actually achieved.
5. Checks timing on the lead volume lever. Given the typical days from lead to opportunity, it works out the last date an extra lead can arrive and still count this quarter, and the monthly pace needed before then.
6. Flags conversion rates that are falling, because a falling rate quietly makes the forecast too optimistic.

## Example output

From the fictional sample data in [`examples/`](examples/). Full report: [`examples/output/q4-2026-forecast.md`](examples/output/q4-2026-forecast.md).

> **Target:** £5,600,000 · **Base forecast:** £5,075,084 (91% of target) · **Gap to close:** £524,916
>
> | Lever | Needed | Best recent month | Verdict |
> |---|---:|---:|---|
> | More leads in the remaining months | a pace of 3,318 a month until 16 November | 2,300 | Beyond recent performance |
> | Better marketing qualified to sales qualified rate | 42.1% | 40.1% | Beyond recent performance |
>
> **Timing:** leads take a median of 45 days to become opportunities, so the extra 596 leads have to arrive between 1 and 16 November to count this quarter.
>
> **Warning sign:** marketing qualified to sales qualified fell from 39.3% to 33.0%. Find the cause before adding volume: extra leads at a falling conversion rate buy less pipeline than this forecast assumes.

The obvious fix is to buy more leads. Spread across November and December, that needs 2,248 a month, which looks realistic next to a best month of 2,300. The timing check shows why it is not: December's leads will mostly become opportunities in January, so the extra volume has to land in the first half of November. The falling qualification rate means even that volume would underdeliver. The honest answer is to combine smaller moves, starting with finding out why qualification is slipping, or to reset the target with this evidence.

## How it works, in plain terms

Think of the funnel as a series of sieves. History tells you roughly what share passes through each sieve in a normal month. Pour the planned leads through those sieves and you get the forecast. Use a weak month's sieves and you get the low case; a strong month's, the high case.

To close a gap, you can pour in more (leads), widen a sieve (a conversion rate), or make each thing that comes out worth more (opportunity value). The agent asks how much each would need to change alone, then checks whether you have ever actually seen that level recently.

The sieves are also slow. A lead poured in today takes weeks to reach the bottom, so pouring more in late in the quarter fills next quarter's bucket, not this one. Volume, conversion and time are the 3 kinds of funnel measure in Winning by Design's Bowtie model; the timing check adds the third.

## Run it

Python 3.9 or later, no packages to install.

```bash
python3 scripts/forecast.py --history examples/funnel.csv --plan examples/plan.json --out output/forecast
python3 -m unittest discover -s tests
```

Inputs are described in [`SKILL.md`](SKILL.md). With Claude Code, install the folder as a skill and ask, for example: *"Here's our funnel export. Are we going to hit Q4 pipeline, and what should we change?"*

## Limits

- Uses same-month conversion ratios. Fine when lead volume is steady; use cohort data when it swings.
- Leads created late in the quarter often convert after it ends, so the last month is optimistic.
- The timing check uses the median days from lead to opportunity as a hard cut-off. In reality some later leads convert in time and some earlier ones do not, so read it as a guide to timing.
- Only as good as the stage definitions. If the definition of a qualified lead changed during the window, or the history mixes new business with expansion and renewal opportunities, the rates are not comparable.
