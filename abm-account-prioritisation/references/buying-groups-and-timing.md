# Buying groups and timing: the evidence behind the plays

Read this when sales challenges the buying group check or the size of the Warm up tier, when setting the `buying_group` minimum, or when the inputs come from HubSpot. Figures below are from the cited sources; re-check them before quoting, as the research is updated each year.

## Accounts buy as groups

- Forrester's survey of nearly 18,000 business buyers found that, on average, 13 internal stakeholders and 9 external participants influence a buying decision, and that the number rises for larger or more complex purchases. Procurement acted as a decision-maker in 53% of buying cycles. (Forrester, The State Of Business Buying, 2026)
- Forrester's European report on the same survey found that buyers in Europe work in smaller buying groups than buyers elsewhere, and that deal cycles there can be slightly shorter as a result. (Forrester, The State Of Business Buying In Europe, 2026)

**What this means for the model.** An account can clear the engagement threshold on intent data plus one person's activity. That is a reason to map the account, not to treat it as in market. The `buying_group` minimum is a floor agreed with sales. The example uses 2, a deliberately low bar that only asks for engagement from more than one person; because groups grow with the size and complexity of the purchase, larger deals justify a higher floor. The sources do not give a "right" number, so set it from the user's own won deals where possible (how many people were engaged before the opportunity opened).

**Next step for a flagged account.** List the roles that usually take part in this purchase (for example the budget holder, the main user, IT or security, procurement), find who holds them at the account, and give marketing a plan to reach them before the account owner asks for a meeting.

## Most accounts are not buying right now

- The Ehrenberg-Bass Institute's "95-5 rule" holds that, for many business products and services, only a small share of potential buyers is in the market at any one time. The arithmetic: if companies replace a supplier about every 5 years, around 20% are in the market over a year and around 5% in any quarter. The 95% figure is a heuristic, not a precise law. (Dawes, Ehrenberg-Bass Institute, May 2021)
- The same work suggests a practical way to size the in-market share for a category: divide the period by the average time between purchases (a 2-year cycle gives roughly 13% in a quarter), or ask customers how often they buy.
- The LinkedIn B2B Institute, which ran joint research with the Ehrenberg-Bass Institute, recommends lead generation for the few buyers in market now but much heavier investment in reaching future buyers, because the brand that comes to mind most easily when a need arises tends to be the one bought. (LinkedIn B2B Institute, The 95-5 Rule)

**What this means for the model.** A long Warm up tier is the expected result, not a failure of targeting. Do not lower thresholds to fill Pursue now; it pulls in accounts that are not in market. Judge the Warm up programme on reach and familiarity across the buying group over several quarters, and use the in-market arithmetic above to set how many Warm up accounts can realistically move up each period.

## Mapping the inputs to HubSpot

Checked against HubSpot's knowledge base, November 2026. Confirm in the user's own portal, as features depend on subscription.

- **Fit and engagement as separate scores.** HubSpot's lead scoring tool offers separate company fit scores (property values) and company engagement scores (events), which map directly to the two halves of this model. For companies, engagement is calculated from the actions of associated contacts.
- **Capping one signal.** Event groups in HubSpot engagement scores can carry a points limit, which does the same job as `max` here: it stops one noisy signal from dominating.
- **Stale engagement.** HubSpot engagement scores can decay by a set percentage after a set period since the event. If the export uses decayed scores, say so; if it uses raw counts, make sure each column covers the same recent window.
- **Buying group.** HubSpot's account-based marketing tools include a contact-level "Buying role" property (for example Decision Maker, Budget Holder, Blocker). A count of contacts with a buying role who engaged in the period is a good source for the `buying_group` column.
- **Tiers.** HubSpot's "Ideal customer profile tier" company property has 3 tiers by default. It describes fit only; this model's tiers combine fit with engagement and capacity, so do not overwrite one with the other without agreeing it with whoever administers HubSpot.

## Sources

- Forrester, *The State Of Business Buying, 2026* (blog, 21 January 2026): https://www.forrester.com/blogs/state-of-business-buying-2026
- Forrester, *The State Of Business Buying In Europe, 2026* (report summary, 8 December 2025): https://www.forrester.com/report/the-state-of-business-buying-in-europe-2026/RES186871
- John Dawes, Ehrenberg-Bass Institute, *Advertising effectiveness and the 95-5 rule: most B2B buyers are not in the market right now* (May 2021): https://marketingscience.info/news-and-insights/advertising-effectiveness-and-the-95-5-rule-most-b2b-buyers-are-not-in-the-market-right-now
- LinkedIn B2B Institute, *The 95-5 Rule*: https://business.linkedin.com/advertise/resources/b2b-institute/b2b-research/trends/95-5-rule
- HubSpot Knowledge Base, *Build lead scores to qualify contacts, companies, and deals* (updated 3 November 2026): https://knowledge.hubspot.com/scoring/build-lead-scores
- HubSpot Knowledge Base, *Set up account-based marketing in HubSpot* (updated 6 October 2026): https://knowledge.hubspot.com/account/get-started-with-account-based-marketing-in-hubspot
