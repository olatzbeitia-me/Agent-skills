# 2026-11-22: marketing-performance-audit

**Date:** 22 November 2026
**Agent:** [marketing-performance-audit](../marketing-performance-audit/)
**Why this agent:** 6 agents had never been reviewed and no `improve/` pull requests were open; broken alphabetically, this one comes first.

## What changed

1. **Share of search as a public proxy for brand demand (missing method step).** The audit judged performance from public proxies but had no measure linked by published evidence to commercial outcomes. It now asks for the company's share of search against its competitor set, using Google Trends, and a new reference file sets out the method (one comparison for the whole set, brand variants grouped, topics for ambiguous names, a rolling average over 6 to 12 months), the evidence and the limits. New guardrails: Trends values are relative, never search volumes; a 0 means "not measurable", never "no demand"; share of search is never converted into a market share figure.
2. **Funnel coverage grounded in purchase cycles, and buying situations added to the strategic read (sharper method).** The skill said, without a source, that most companies over-invest in capturing demand. That sentence is replaced with the in-market and out-of-market lens from the Ehrenberg-Bass Institute: estimate the category's purchase cycle, work out the rough share of buyers in the market, and judge the balance of capture and creation against it, with no invented "right" ratio. The synthesis now also asks which buying situations (category entry points) the messaging ties the brand to and which situations competitors leave open, using Romaniuk's prompts and 3 tests, while making clear that messaging shows intent, not what buyers remember.
3. **Google Ads Transparency Center facts corrected, and one definition sharpened.** The reference said the tool covers "roughly the past year" and that European Union regions add ranges of times shown. Google's help gives no fixed look-back period and lists the extra European Union detail as targeting information, the total number of recipients of each ad and a subject label. The entry now says this, and tells the agent to record the earliest date it sees. Separately, the proxy called "share of voice" measured share of mentions; it is renamed, with a note that in effectiveness research share of voice means share of advertising spend, which public sources do not show.

Detail sits in a new file, `references/demand-proxies.md` (77 lines, with contents and sources). `SKILL.md` grows from 136 to 139 lines: 1 new proxy, 1 rewritten proxy, 1 renamed proxy, 1 new trap, 1 new synthesis question, a routing sentence and an extra final check. The description is unchanged.

## Why

- Les Binet's share of search work, presented at the Institute of Practitioners in Advertising's EffWorks conference in 2020, found it tracked market share in cars, household energy and mobile handsets, and in cars warned of changes up to a year ahead. The Institute's think tank (2021) pooled 30 case studies from 12 categories and 7 countries and found share of search averaged about 83% of market share, varying by category and country, and recommended smoothing over 6 to 12 months. Both stress correlation rather than cause. That makes it a better-evidenced proxy than anything else in the skill's list, provided its limits travel with it.
- Google's own Trends help says values are sampled, normalised and scaled from 0 to 100, low-volume terms show as 0, privacy noise is most visible on low-interest terms, spikes should not be read as popularity, and Trends is not a scientific poll. The Compare help gives the current limits (8 groups of up to 50 terms in Explore, 5 groups of up to 25 in the classic view) and says misspellings, variants and plurals are not merged. Those facts became the method steps and guardrails, which matter most for business-to-business brands that often fall below the volume line.
- John Dawes's 95-5 article (Ehrenberg-Bass Institute, May 2021) shows the arithmetic: a provider changed about every 5 years means around 20% of buyers in the market in a year and roughly 5% in a quarter; a 2-year cycle gives about 50% and 13%. He calls the 95% a heuristic. Tying funnel coverage to the category's own purchase cycle replaces an unsourced generalisation with a method the agent can show.
- Jenni Romaniuk's paper for The B2B Institute at LinkedIn (June 2022) defines category entry points, gives prompts for finding them from both the business's and the buyer's point of view, and 3 tests for prioritising them (credibility, competitiveness, commonality). It also reports higher acquisition and retention for brands linked to wider, fresher sets of buying situations. Mapping which situations a company's messaging claims, against competitors, is a sharper strategic read than message consistency alone, and it suits interview and pitch preparation.
- Google's Ads transparency help page does not support the "roughly the past year" claim or the "times shown" wording, so the entry now follows the help page.

## Considered and rejected

- **Turning share of search into a market share estimate using the 83% average.** Rejected: the think tank says the ratio varies by category and country, and the skill already forbids presenting estimates as fact.
- **Stitching several Trends comparisons together through a shared anchor brand when the competitor set is large.** A common practitioner technique, but none of the sources read in this run describes it, and the current Explore limit of 8 groups covers most competitor sets.
- **Measuring mental availability (mental market share, mental penetration, network size).** Romaniuk's metrics need a survey of category buyers; a public-evidence audit cannot produce them. The skill maps messaging coverage instead and says so.
- **Citing the 96% of business-to-business marketers who expected campaign effects within 2 weeks** (from a LinkedIn trends page). The page gives no date or method, so the figure was left out.
- **Naming Türkiye among the countries with extra transparency data.** The help page's country list could not be confirmed as the list of countries with that data rather than a page-localisation menu, so the entry says only "certain countries, including European Union member states".
- **Rewriting the description.** At 431 characters it is well within limits and already covers the right triggers.
- **Re-checking Anthropic's skill authoring guidance.** The page could not be fetched in this run; the structure follows the repository's existing pattern (`SKILL.md` as an overview with detail one level down in `references/`) rather than a fresh reading.

## Noticed outside this agent

- The repository `README.md` still opens with "reussable" (should be "reusable"), first noted on 21 November.

## Sources

- Institute of Practitioners in Advertising, *Binet presents fast, cheap, predictive Share of Search metric* (14 October 2020): https://ipa.co.uk/news/binet-presents-fast-cheap-predictive-share-of-search-metric/
- Institute of Practitioners in Advertising, *New findings from the cross-industry IPA Share of Search think tank data* (12 October 2021): https://ipa.co.uk/news/share-of-search/
- Google Trends Help, *FAQ about Google Trends data*: https://support.google.com/trends/answer/4365533?hl=en-GB, and *Compare Trends search terms*: https://support.google.com/trends/answer/4359550?hl=en
- Dawes, J., *Advertising effectiveness and the 95-5 rule: most B2B buyers are not in the market right now*, Ehrenberg-Bass Institute (May 2021): https://marketingscience.info/news-and-insights/advertising-effectiveness-and-the-95-5-rule-most-b2b-buyers-are-not-in-the-market-right-now
- Romaniuk, J., *Category Entry Points in a B2B World: Linking Buying Situations to Brand Sales*, The B2B Institute at LinkedIn (June 2022): https://business.linkedin.com/content/dam/lem/business/en/advertise/resources/b2b-institute/b2bi-cepinb2b-final.pdf (landing page: https://business.linkedin.com/advertise/resources/b2b-institute/cep-in-b2b)
- Google Advertising Policies Help, *Ads transparency*: https://support.google.com/adspolicy/answer/13733850
