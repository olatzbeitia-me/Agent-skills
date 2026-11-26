# Audit checklist by channel

Read only the sections for channels in play. Each item gives what to check and why it matters. Platform features change often; confirm anything you recommend against the channel primers in `channels/` and a fresh check of official sources (`sources.md`).

## Contents
1. Account-wide checks
2. Google Ads: Search (including AI Max)
3. Google Ads: Performance Max and Shopping
4. Google Ads: Demand Gen and YouTube
5. Microsoft Advertising
6. Meta (Facebook, Instagram)
7. LinkedIn
8. TikTok, Pinterest, Snapchat, Reddit, X
9. Programmatic and demand-side platforms
10. Creative and assets (all channels)
11. Wasted spend sweep

---

## 1. Account-wide checks

- **Goal alignment**: list each campaign's optimisation goal next to the business goal. Mismatches are findings.
- **Budget allocation**: compare each channel's share of spend with its share of *qualified* outcomes, and think in marginal terms. A channel with a great average result may already be saturated; a budget-limited campaign that converts well may deserve more. Look for campaigns limited by budget while others underspend.
- **Overlap and cannibalisation**: the same query or person targeted by several campaigns (Search versus Performance Max; prospecting versus retargeting; LinkedIn and Meta retargeting the same visitors). Overlap raises costs and muddies attribution.
- **Geography and language**: Google's default location option includes people "interested in" a location, not just present in it, which leaks spend abroad. Check location settings and the geographic report.
- **Change frequency**: constant edits reset learning periods on automated bidding. Check change history if available.
- **Frequency and reach**: on social, video and display, frequency well above what the audience size justifies signals saturation.
- **Landing pages**: message match with the ad, load speed on mobile, form length and friction, proof (reviews, logos, regulation), and a clear next step. Paid media performance is capped by the page.
- **Team capacity**: an account structure the team can't maintain is a finding in itself.

## 2. Google Ads: Search (including AI Max)

- **Structure by intent**: brand; competitor; high-intent category ("international payments for business"); problem-aware; informational. Each has different economics and should not share a budget with the others.
- **Brand**: separate campaign; check whether brand spend is incremental (brand holdout test) and whether competitors bid on the brand. Make sure brand terms are excluded from non-brand campaigns, Performance Max and AI Max (brand exclusions).
- **AI Max for Search**: an optional layer on Search campaigns that expands matching beyond keywords, rewrites ad text and picks landing pages. It is replacing Dynamic Search Ads (Google's automatic migration is now set for February 2027 per its developer blog; check the current date). Check: is it on; does the search terms report (with its AI Max match-type indicators) show relevant queries; are brand controls and URL exclusions set; is conversion volume enough to steer it? AI Max is also the route into ads in AI Overviews and AI Mode, so being off it has a reach cost. Verify current status and defaults.
- **Match types and negatives**: broad match only works with sound conversion signal and Smart Bidding. Review search terms for waste (jobs, careers, free, login, how-to, DIY, wrong product, competitors' support queries). Shared negative lists across campaigns.
- **Competitor keywords**: check economics separately; UK rules allow bidding on competitor trademarks as keywords, but trademark use in ad text can be restricted after a complaint.
- **Ads and assets**: responsive search ads with distinct headlines (not ten variations of one idea); limited pinning; message match with the landing page; sitelinks, callouts, structured snippets, images, lead form assets where relevant.
- **Bidding fit**: does each campaign have enough conversions for its strategy? Target cost per acquisition or target return on ad spend on thin volume behaves erratically. Look at impression share lost to rank versus budget.
- **Conversion goals**: see `measurement.md`; confirm what each campaign bids towards.

## 3. Google Ads: Performance Max and Shopping

- **Brand leakage**: Performance Max will bid on brand searches unless brand exclusions are applied, which inflates its results. Check search term categories and the search terms report.
- **Negative keywords**: campaign-level negatives (up to 10,000) are now available. They only affect Search and Shopping inventory, not Display or YouTube placements inside Performance Max.
- **Channel performance report**: breaks down spend and conversions across Search, Shopping, Display, YouTube, Discover, Gmail and Maps. A large share going to Display or YouTube with weak results is a common finding.
- **Placements**: placement report segmented by network; exclude poor apps and sites at account level.
- **Customer acquisition**: new customer goal settings; customer list exclusions to stop paying to reach existing customers.
- **Asset groups**: grouped by theme or product line with relevant audience signals; full asset coverage (video included; otherwise Google may auto-generate it).
- **Final URL expansion**: if on, check where traffic lands; add URL exclusions for careers, blog, login and support pages.
- **Lead generation in Performance Max**: high risk of spam or low-quality leads from Display and partner inventory. Only viable with qualified-lead or offline conversion optimisation.
- **Shopping feeds**: titles front-loaded with what people search; correct product identifiers; image quality; price competitiveness; custom labels for margin, best-sellers and stock so budget follows profit; Merchant Center diagnostics.
- **Overlap**: Performance Max versus Standard Shopping and Search. Exact-match Search usually wins identical queries, but check.

## 4. Google Ads: Demand Gen and YouTube

- Role: creating demand and mid-funnel reach, not last-click conversion. Judge on lift (brand search lift, conversion lift studies) rather than last-click cost per acquisition.
- Creative fit: vertical and horizontal video, Shorts-ready cuts, first five seconds carry the message.
- Audiences: customer lists, lookalike segments, custom segments built from search terms and competitor sites.
- View-through conversions: report separately; don't let them justify spend on their own.

## 5. Microsoft Advertising

- Often under-used: lower competition, older and desktop-heavy audiences, strong for business-to-business and higher-income consumers.
- Google imports: check that imports haven't carried over settings that don't fit (location options, unsuitable broad match without signal) and that budgets aren't simply mirrored.
- LinkedIn profile targeting (company, industry, job function) on search and audience ads: a genuine edge for business-to-business.
- Microsoft Audience Network and Copilot placements: ads in Copilot are generated from existing Microsoft Advertising assets; check whether the account is eligible and how those placements perform.
- Performance Max on Microsoft now supports negative keywords (Search and Shopping inventory only).

## 6. Meta (Facebook, Instagram)

- **Structure**: a Sales, Leads or App campaign counts as Advantage+ only while all 3 automation levers are on: Advantage+ campaign budget, Advantage+ audience in at least one ad set, and Advantage+ placements in every ad set (placement exclusions set at account level don't switch it off). Check which levers each campaign uses and why any are off, rather than assuming a newer campaign is Advantage+ (see `channels/meta.md`). Fewer, consolidated campaigns and ad sets generally learn faster; fragmented structures starve each ad set of signal.
- **Creative is the targeting**: Meta's delivery system uses the creative itself to find audiences, and broad audience settings are treated as suggestions. The lever is a library of conceptually different creative (different hooks, angles, formats and people), not small variations of one idea. Check concept count, format coverage (vertical video, static, carousel), and fatigue (rising frequency with falling click-through rate).
- **Signal**: pixel plus Conversions API, deduplicated; event match quality; the right optimisation event (purchase versus add to cart; qualified lead versus any lead).
- **Lead ads**: instant forms produce high volume and variable quality. Check for qualifying questions, "higher intent" form type, customer relationship management system feedback, and the downstream qualification rate.
- **Existing customers**: check that something limits spend on buyers who would return anyway. The old existing-customer budget cap isn't available in new Advantage+ campaigns; Meta's documented replacement is 2 ad sets, one for existing customers with a spending limit and one that excludes them.
- **Attribution settings**: confirm the window and whether view-through is included before comparing periods; default or setting changes break like-for-like comparisons.
- **Regulated categories**: financial products, health, housing, employment and others have restricted targeting and, in some markets, restricted optimisation events. Check current rules for the markets in play.

## 7. LinkedIn

- **Targeting precision**: company lists and job function plus seniority are the core. Check audience sizes (too small saturates, too large wastes budget), and whether audience expansion and the LinkedIn Audience Network are on without having been tested; both usually dilute business-to-business precision.
- **Objective and bidding**: lead gen forms versus website conversions; manual bidding versus maximum delivery; cost per click versus cost per thousand impressions. Maximum delivery on small audiences can overspend fast.
- **Lead quality**: lead gen forms are low friction and pre-filled, so intent varies. Check qualifying questions, customer relationship management system sync, and qualification rate by campaign.
- **Formats**: Thought Leader ads (sponsored posts from employees or creators) often outperform company-page ads on engagement and trust; document ads suit research-heavy buyers; conversation ads for event or demo invitations; video for reach. BrandLink (in-stream video alongside publisher and creator content) and LinkedIn's connected TV ads suit brand-building budgets.
- **Frequency**: small business-to-business audiences see the same ad many times; rotate creative on a schedule.
- **Measurement**: Insight Tag plus Conversions API; customer relationship management system integration for revenue attribution. View-through conversions inflate results; decide on click-through or lift tests.
- **Retargeting**: video viewers, lead form openers, website visitors, company page engagers, in sequence.

## 8. TikTok, Pinterest, Snapchat, Reddit, X

- **TikTok**: creative must look native (creator-style, sound on, fast hook). Spark Ads boost organic or creator posts. Automated campaign types need conversion signal like Meta's. Strong for consumer brands with visual products and audiences under about 45.
- **Pinterest**: planning and inspiration intent; strong for home, fashion, food, weddings and travel; long consideration windows.
- **Snapchat**: young UK audience; augmented reality formats; useful reach for youth-skewed consumer brands.
- **Reddit**: community and conversation targeting; useful for technical, gaming, finance and niche business-to-business audiences that research in forums; creative must respect community norms.
- **X**: reach at low cost for news, sport, tech and finance audiences; check brand safety and suitability controls carefully.

For each: is the audience genuinely there for this company, is conversion tracking in place, and is spend large enough to exit learning phases?

## 9. Programmatic and demand-side platforms

Covers Display & Video 360, The Trade Desk, and other demand-side platforms, plus Google Display Network.

- **Supply quality**: share of spend on made-for-advertising sites, mobile games and apps, and unknown domains. Inclusion lists, private marketplaces and curated deals versus open exchange.
- **Brand safety and suitability**: verification partner in place; settings appropriate to the brand.
- **Viewability and attention**: viewable impression rates; placements and formats with real attention.
- **Frequency**: cross-device frequency caps.
- **Fees**: platform fee, data fees, agency fees and verification fees as a share of media; the working media share is often lower than expected.
- **Measurement**: view-through windows inflate results most here; incrementality tests are essential before scaling.
- **Data**: first-party audiences, contextual targeting, retail and publisher data, and the business's own customer data where consent allows.

## 10. Creative and assets (all channels)

- **Message-market fit**: does the core message speak to the buyer's actual trigger (cost, speed, risk, status, compliance) or only describe features?
- **Proof**: customer names, numbers, reviews, regulation and security credentials where trust matters.
- **Offer and call to action**: matched to funnel stage (a demo request is too big an ask for cold audiences in a long cycle).
- **Variety**: number of genuinely different concepts live per channel; format coverage per placement (vertical video, square, landscape, static, carousel).
- **Fatigue**: frequency and click-through trends by creative.
- **Testing discipline**: are tests of concepts or of trivial variations; is there a log of what has been learnt?
- **Consistency**: does creative across channels tell one story, with the landing page continuing it?

## 11. Wasted spend sweep

Quick checks that often find money:

- Search terms with spend and no qualified conversions over a meaningful period
- Brand spend that isn't incremental (holdout test it)
- Performance Max or AI Max serving on brand terms without exclusions
- Display, app and partner placements with no qualified outcomes
- Location leakage (people "interested in" the area, not present)
- Out-of-hours spend for businesses that rely on calls and can't answer
- Retargeting existing customers or recent converters without exclusions
- Duplicate campaigns competing in the same auctions
- LinkedIn Audience Network or audience expansion on by default
- Excessive frequency on small audiences
- Spending into automated campaign types that never exit the learning phase
- Fees and data costs on programmatic buys that don't earn their keep
