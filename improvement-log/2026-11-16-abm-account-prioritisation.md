# 2026-11-16: abm-account-prioritisation

**Date:** 16 November 2026
**Agent:** [abm-account-prioritisation](../abm-account-prioritisation/)
**Why this agent:** first review run; no agent had been reviewed, so the tie was broken alphabetically.

## What changed

1. **Buying group check (code, tests, example).** `prioritise.py` accepts an optional `buying_group` rule in the configuration (`column`, `min_engaged`). Pursue now and Pursue next accounts whose engagement comes from fewer people than the minimum are flagged in a new "Buying group check" section of the report and a `buying_group` column in the CSV. The flag does not change tiers. An unknown count is flagged rather than assumed. 8 new tests (14 in total, all passing); the example configuration uses a minimum of 2, and the regenerated example flags 1 account (Velloway Bank, which reaches Pursue now on intent data and website visits with 1 engaged contact).
2. **Warm up rationale.** The Warm up play, the report's "How to read this" notes, `SKILL.md` step 3.2 and the README now explain that most good-fit accounts are not in the market at any one time, so a long Warm up tier is expected and the programme should be judged over quarters. `SKILL.md` also asks for every engagement column to cover the same recent window, so a stale signal does not look current.
3. **New reference file.** `references/buying-groups-and-timing.md` holds the evidence for both changes, guidance on setting the buying group minimum, a way to estimate the in-market share from the time between purchases, and how the model's inputs map to HubSpot's fit scores, engagement scores, score decay, points limits, Buying role property and Ideal customer profile tier. `SKILL.md` links to it, keeping the skill itself short.

## Why

- The model let an account reach Pursue now on intent data plus one person's activity. Forrester's 2026 buyer research puts the average buying decision at 13 internal stakeholders plus 9 external participants, so interest from one contact is a reason to map the account, not proof it is in market.
- The Warm up guidance said "a programme, not a holding pattern" without saying why. The Ehrenberg-Bass 95-5 work gives the reason and a simple way to size expectations, which helps the user defend a long Warm up list to sales.
- HubSpot's current documentation (updated October and November 2026) confirms the fit and engagement split this model uses, and offers score decay and buying roles that make the inputs better; noting the mapping helps users who export from HubSpot.

## Considered and rejected

- **Demoting single-threaded accounts out of Pursue now.** Rejected: it would hide a high-intent account. Flagging keeps the ranking transparent and changes the next step instead.
- **Using the buying group count to decide who gets the capped Pursue now places.** Rejected for now: it mixes two rules and makes the tiering harder to explain. Worth revisiting if users ask for it.
- **Building time decay into the engagement score.** Rejected: customer relationship management systems such as HubSpot already offer decay, and the inputs here are period snapshots. A note on consistent time windows was added instead.
- **A default minimum taken from research.** Rejected: the sources report average group sizes, not a threshold. The minimum stays a configurable floor agreed with sales; the example uses 2 and says why.
- **Gartner's business buying journey page.** Not used: the public page now redirects to a general marketing leaders page with no figures.
- **Fixing the "reussable" typo in the top-level README.** Out of scope for an agent review; flagged in the pull request instead.

## Sources

- Forrester, *The State Of Business Buying: Risk-Averse Buyers Demand Proof, Not Promises* (Barbara Winters, 21 January 2026): https://www.forrester.com/blogs/state-of-business-buying-2026
- Forrester, *Forrester's 2026 Buyer Insights* press release (21 January 2026): https://www.forrester.com/press-newsroom/forrester-2026-the-state-of-business-buying/
- Forrester, *The State Of Business Buying In Europe, 2026* (report summary, 8 December 2025): https://www.forrester.com/report/the-state-of-business-buying-in-europe-2026/RES186871
- John Dawes, Ehrenberg-Bass Institute, *Advertising effectiveness and the 95-5 rule: most B2B buyers are not in the market right now* (B2B report, May 2021): https://marketingscience.info/news-and-insights/advertising-effectiveness-and-the-95-5-rule-most-b2b-buyers-are-not-in-the-market-right-now
- LinkedIn B2B Institute, *The 95-5 Rule* (page shows no date; used only alongside the dated Ehrenberg-Bass report it draws on): https://business.linkedin.com/advertise/resources/b2b-institute/b2b-research/trends/95-5-rule
- HubSpot Knowledge Base, *Build lead scores to qualify contacts, companies, and deals* (updated 3 November 2026): https://knowledge.hubspot.com/scoring/build-lead-scores
- HubSpot Knowledge Base, *Set up account-based marketing in HubSpot* (updated 6 October 2026): https://knowledge.hubspot.com/account/get-started-with-account-based-marketing-in-hubspot
- Anthropic, *Skill authoring best practices* (used to check the description and the split between `SKILL.md` and `references/`): https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
