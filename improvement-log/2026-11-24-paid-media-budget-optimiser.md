# 2026-11-24: paid-media-budget-optimiser

**Date:** 24 November 2026
**Agent:** [paid-media-budget-optimiser](../paid-media-budget-optimiser/)
**Why this agent:** 2 `improve/` pull requests were open (marketing-performance-audit and martech-stack-audit), so those 2 agents count as reviewed today. Of the 4 agents never reviewed, this one comes first alphabetically.

## What changed

1. **The plan now stays inside each campaign's spend history (model limitation fixed in code, with tests).** The optimiser could move a campaign up to 30% either way, even when that took it above the highest or below the lowest weekly spend the curve had been fitted on. By default, each campaign's bounds are now also limited to that observed range. Campaigns that stop at the edge while the marginal costs say money would still have moved are listed in the report, with a test to widen their history. A new `--allow-extrapolation` option lifts the limit, and the report then flags every move that goes beyond the history. Budget released from possible waste can still push a campaign past its history, because that money has to go somewhere; the same flag then appears. 4 new tests cover the upper edge, the lower edge, a campaign at its peak that should not be flagged, and the override. The example test now checks that no example recommendation leaves its history. In the example, the Meta cut now stops at £1,877 a week rather than going down to £1,552, because the campaign has never run below £1,860. The predicted gain falls from +3% to +2%. That is an honest loss: the old figure relied on a part of the Meta curve that the data never covered.
2. **Automated bidding facts corrected (outdated platform fact).** The skill said large changes can reset automated bidding, and gave that as the reason for capping and staging moves. Google's current Smart Bidding guidance says budget changes take effect in the next auction and never trigger a "Learning" status. Only a new bid strategy, a change to what the strategy covers, or a changed conversion goal does. Performance still takes 1 to 2 conversion cycles to settle, and Google suggests judging results over 2 conversion cycles or 2 weeks, whichever is longer, allowing for conversion delay. The skill now states this for Google Ads. It asks Claude to check current guidance for Meta, LinkedIn and Microsoft Advertising rather than assume. It gives the real reason for staging, which is that the curves are estimates. The staged plan in `SKILL.md` and the report's "Before acting" section now use Google's evaluation window instead of a flat fortnight.
3. **A sourced search check replaces an unsourced threshold (sharper definition).** The skill and the report told users that extra brand search budget mostly raises cost per click once impression share is "above about 90%". No source was given for that figure. The check now uses Google's Search lost impression share (budget): how often the ads were not shown because the budget was too low. If that is close to zero, budget is not the constraint and the predicted gain is unlikely to appear. Search lost impression share (rank) shows whether Ad Rank is the constraint instead. In `SKILL.md` the check now covers any search campaign the plan increases; the report's note still appears for brand campaigns, as before.

`SKILL.md` grows from 53 to 55 lines and the description is unchanged. `README.md` gains a bullet on the history limit, an updated example excerpt and a limit explaining the trade-off. The example outputs were regenerated, and all 12 tests pass. The 4 new tests and the extended example test fail against the previous script.

## Why

- Google's Meridian documentation says extrapolation risk affects points on a response curve above historical spend, and grows the further out you go. It applies the same warning to the zero-spend case when a channel has always spent steadily.
- Meta's Robyn budget allocator documentation advises against exaggerated upper bounds, especially when the new level is far above historical spend.
- PyMC-Marketing's budget allocation guide notes that the scatter of past spend against contribution only shows the "observable space", and says nothing about what happens beyond those points.
- These are 3 independent, widely used open-source modelling projects, and all 3 treat a response curve as least reliable outside the spend it was fitted on. A simple curve fitted on 10 to 16 weeks deserves at least the same caution. Using the observed range as the bound needs no new figure: the data sets it.
- Google's "About Smart Bidding learning" help page, read on 24 November 2026, lists the 3 causes of a "Learning" status and says budget changes never trigger it. The skill's earlier claim was therefore wrong for Google Ads, and the staging advice needed a different reason.
- Google's "Get impression share data" help page defines Search lost impression share (budget) and (rank). This gives the search check a documented metric in place of a threshold with no source.

## Considered and rejected

- **Uncertainty ranges on the predicted gain.** PyMC-Marketing shows uncertainty bands around its curves, and a resampling interval would show whether a +2% gain is distinguishable from noise. It is worth its own review; this run kept to one code change.
- **Carry-over (lagged) effects.** Meridian notes that lagged effects matter more over short windows, and this agent works on weekly data without modelling any carry-over from one week to the next. Modelling carry-over needs more history than 10 to 16 weeks per campaign and changes the method, so it was left for a future review.
- **Stating Meta's rules on budget edits and the learning phase.** Meta's Business Help Centre pages refused automated reading, so the rules could not be confirmed from Meta's own documentation. Third-party summaries were not used. The skill asks Claude to check the platform's current help pages instead.
- **Replacing "about 90%" with a different impression share threshold.** None of the sources gives one, so the check moved to lost impression share (budget), which answers the real question directly.
- **A tolerance that lets recommendations go a little beyond the history.** No source gives a safe margin, and a made-up margin would be a figure without a source. The edge is exact, and `--allow-extrapolation` is the explicit way past it.

## Noticed outside this agent

- `pardot-to-hubspot-migration/SKILL.md` still has a 1,035-character description, above Anthropic's documented 1,024-character limit. It is next in line for review.
- The "reussable" typo in the repository `README.md` is fixed in the open martech-stack-audit pull request, so it is not repeated here.

## Sources

- Google Meridian, *Incremental outcome, ROI, mROI and response curves*: https://developers.google.com/meridian/docs/basics/roi-mroi-response-curves
- Google Meridian, *Interpret the optimizations*: https://developers.google.com/meridian/docs/post-modeling/interpret-optimizations
- Meta Robyn, `robyn_allocator` reference (CRAN package documentation): https://rdrr.io/cran/Robyn/man/robyn_allocator.html
- PyMC-Marketing, *Budget allocation with PyMC-Marketing*: https://www.pymc-marketing.io/en/stable/notebooks/mmm/mmm_budget_allocation_example.html
- Google Ads Help, *About Smart Bidding learning* (read 24 November 2026): https://support.google.com/google-ads/answer/13020501?hl=en-GB
- Google Ads Help, *Get impression share data*: https://support.google.com/google-ads/answer/7103314?hl=en-GB
