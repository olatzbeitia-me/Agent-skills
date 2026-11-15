# Meta (Facebook, Instagram, Messenger, Threads, Audience Network)

## How it works
- Each ad opportunity runs an auction. Meta picks the ad with the highest *total value*: the advertiser's bid multiplied by the estimated chance the person takes the desired action, plus a measure of ad quality. Relevance and creative quality can beat a higher bid.
- People aren't searching; they are scrolling. Meta creates demand by putting the right creative in front of people likely to respond, then learns who responds.
- Meta's delivery system increasingly uses the creative itself to find the audience. Broad targeting with a varied set of creative concepts usually outperforms narrow interest targeting.

## Campaign types and formats
- Objectives: Awareness, Traffic, Engagement, Leads, App promotion, Sales.
- **Advantage+ sales, app and leads campaigns**: automation across three levers, placements, budget and audience; a campaign counts as Advantage+ when all three are on. They replaced the older Advantage+ shopping and app campaigns.
- Formats: Reels, Stories, Feed, single image and video, carousel, collection, instant experience, catalogue (dynamic product) ads, instant forms for lead generation, click-to-message ads (WhatsApp, Messenger, Instagram Direct).

## Targeting
Locations, age, gender, Advantage+ audience (Meta expands beyond suggestions), custom audiences (website visitors, customer lists, engagers), lookalikes, and placement and existing-customer controls. Some categories (credit, employment, housing, social issues, elections and politics) have restricted targeting; health and financial advertisers may also face limits on optimisation events. Check current rules for the market.

## Bidding and optimisation
Highest volume (no cap), cost per result goal, return on ad spend goal, bid cap. Ad sets go through a learning phase and need a steady flow of optimisation events (Meta's guidance has long been around 50 a week per ad set; check current guidance). Frequent edits restart learning.

## Measurement
Meta pixel plus Conversions API (server-side), deduplicated; event match quality score; attribution settings (click and view windows), which must match before comparing periods; conversion lift and A/B tests; marketing mix modelling for larger advertisers. For leads, sending downstream stages from the customer relationship management system lets Meta optimise for quality.

## Best for and weak for
- **Best for**: consumer brands; visual and demonstrable products; ecommerce with a catalogue; local services; generating demand at scale; retargeting.
- **Weak for**: niche business-to-business buyers defined by job or company (no professional targeting); very small budgets split across many ad sets; advertisers without creative capacity.
- **Watch for**: platform-reported results overstating impact (view-through, retargeting existing customers); creative fatigue; low-quality instant-form leads.

## Creative needs
High. The main lever is a steady supply of genuinely different concepts (different hooks, angles, people and formats), native to Reels and Stories, refreshed as fatigue sets in.

## Recent developments (checked October 2026)
- **Advantage+ campaign structure**: creating the old Advantage+ shopping and app campaigns is no longer possible through the API (from version 25.0); version 26.0 stops editing or migrating legacy ones, and legacy campaigns using an existing-customer budget percentage will be paused. Advertisers can reproduce that control by splitting new and existing customers into separate ad sets. Placement automation is on by default; budget and audience automation are opt-in. *Source: Meta for Developers, Advantage+ campaign experience documentation.* (Some blogs describe Advantage+ as "the default for all new campaigns"; Meta's documentation doesn't say that.)
- **Meta Enterprise Platform** launched 28 September 2026: Meta's AI agents packaged for businesses and developers; no advertiser-specific features described. *Source: About Meta newsroom.*

## Where to check for news
Meta for Business news (facebook.com/business/news), About Meta newsroom (about.fb.com/news), Meta for Developers changelog and Marketing API documentation, Meta Business Help Centre.
