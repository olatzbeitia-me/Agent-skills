# 2026-11-28: pipeline-forecast

**Date:** 28 November 2026
**Agent:** [pipeline-forecast](../pipeline-forecast/)
**Why this agent:** No `improve/` pull requests were open. This was the only agent never reviewed.

## What changed

1. **Timing check on the "more leads" lever (model limitation fixed in code, with tests).** The model rated the lead volume lever only on volume: could the remaining months reach the monthly lead count needed, compared with the best recent month? It ignored how long a lead takes to become an opportunity, so it could call "buy more leads" realistic when most of those leads would only turn into opportunities after the quarter ends. `plan.json` now takes 2 optional fields:
   - `lead_to_opportunity_days`: the median days from lead creation to opportunity creation, from the user's own CRM.
   - `as_of`: today's date, if the quarter is already under way.

   When the first is given, `scripts/forecast.py` works out the last date an extra lead can arrive and still count this quarter. It then works out the monthly pace needed to fit the extra leads into that window and compares it with the best recent month. If the window has already closed, the lever is marked "Too late for this quarter". The report explains the cut-off in a "Timing" paragraph and says the median is used as a hard cut-off, so the result is a guide rather than an exact count. Without the field, results are unchanged and the report's limits section says the timing has not been checked. 5 new tests cover the timing maths, the too-late case, the unchanged behaviour without the field, and input validation. All 11 tests pass.
2. **Example regenerated, and the recommendation changes.** The fictional example plan now includes a fictional 45-day median. Without the timing check, the extra leads looked realistic at 2,248 a month spread over November and December, against a best month of 2,300. With it, they have to arrive by 16 November, which means a pace of 3,318 a month. So no single lever now closes the gap, and the report recommends combining moves or resetting the target. The README's worked example and explanation are updated to match.
3. **Sharper checks on what the history counts (`SKILL.md` guardrail).** Before forecasting, Claude now confirms 3 things rather than 1:
   - the stage definitions did not change during the window (as before);
   - the history covers one kind of opportunity, because new business, expansion and renewal opportunities convert at different rates and speeds;
   - whether several people from one buying group are each counted as a lead, which makes lead-based rates look low and means extra leads from accounts already in the pipeline add few new opportunities.

   `SKILL.md` also tells Claude where to find the median days in HubSpot and Salesforce, and never to recommend more leads without the timing check. It is now 65 lines.

## Why

- Winning by Design's Bowtie Standard (2026) describes every stage of the funnel with 3 kinds of measure: volume, conversion rate and time to convert. The agent already used the first 2 and average opportunity value. Time was missing, and it matters most for mid-quarter decisions. The same document also warns against assuming that doubling leads doubles results.
- Winning by Design's Bowtie Data Model page (22 July 2026) repeats that forecasts should rest on defined time, conversion and volume metrics for each stage.
- Forrester's article on its revised revenue waterfall explains that opportunity types each convert at different rates and spend different times in each stage. It also explains how counting several leads per buying group holds lead conversion rates down. Both points affect whether the funnel history is fit to forecast from.
- HubSpot's knowledge base (updated 24 November 2026) documents the "Date entered" stage properties, which give the time between 2 stages for each record. Salesforce's object reference documents the lead's converted date, which can be compared with its created date. So the new input is something users can actually get from their CRM, not a figure they would have to guess.

## Considered and rejected

- **Spreading conversion over time with a full lag distribution (cohort model).** This would replace the same-month ratios with a proper cohort forecast and also fix the "last month is optimistic" limit. It needs lead-level dates, not monthly totals, and would change every number in the model. It is too large for one review. The timing check is a first step that uses one figure the user can find.
- **Discounting December's planned leads in the base forecast.** Same-month ratios already count, in a steady month, the opportunities that come from earlier months' leads. Applying a timing cut to the base forecast as well would count the lag twice. The check is limited to the extra leads in the lever analysis, where the lag is genuinely missing.
- **A backtest of the method's past accuracy.** Testing how close the median-rate method would have been in each past month (the rolling-origin approach used by open-source forecasting tools such as Prophet) would show whether the forecast tends to run high when rates are falling. It is worth a future review. It was left out to keep this pull request to one change in the model.
- **Adding "faster follow-up" as a lever.** Shortening the time from lead to opportunity would pull some pipeline into the quarter. Measuring that properly needs the lag distribution above, so it was not added.
- **Changing the skill description.** It is 393 characters and already says what the skill does and when to use it. No change was needed.

## Noticed outside this agent

- Nothing.

## Sources

- Winning by Design, *The Bowtie Standard: A Modern Data Model for Recurring Revenue Businesses* (2026): https://winningbydesign.com/wp-content/uploads/2026/01/The-Bowtie-Standard.pdf
- Winning by Design, *Bowtie Data Model* (22 July 2026): https://winningbydesign.com/bowtie-data-model
- Forrester, *Why We Have A New Waterfall For 2021 (And Why You Should Care)* (27 April 2021): https://www.forrester.com/blogs/why-we-have-a-new-waterfall-for-2021-and-why-you-should-care
- HubSpot Knowledge Base, *Use stage calculated properties* (updated 24 November 2026): https://knowledge.hubspot.com/properties/stage-calculated-properties
- Salesforce Developers, *Object Reference: Lead*: https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_lead.htm
