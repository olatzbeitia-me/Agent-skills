# Competitor research methods

The aim is not a dossier on each competitor. It is to answer: where are competitors investing, what are they saying, where are they absent, and what opening does that leave for this company? Every ad mentioned is shown as a screenshot with its direct library link and the date checked (see `sources.md`). Third-party tool estimates are "reported" and should name the tool.

## What you can observe directly (free, public)

| Source | What it shows | What it doesn't show |
|---|---|---|
| **Google Ads Transparency Center** (adstransparency.google.com) | Ads by advertiser or domain across Search, YouTube, Display and Shopping; filter by region and format; when ads were last shown | Spend, targeting, performance |
| **Meta Ad Library** (facebook.com/ads/library) | All currently active ads across Facebook, Instagram, Messenger and Audience Network; start dates; platforms; number of variants | Spend and targeting for ordinary commercial ads outside the EU; ads delivered in the EU carry extra reach and targeting detail under the Digital Services Act |
| **LinkedIn Ad Library** (linkedin.com/ad-library) | Ads run on LinkedIn in roughly the past year, searchable by advertiser; formats and copy; EU-delivered ads show impression ranges and targeting parameters | Spend; full targeting for non-EU delivery |
| **TikTok Commercial Content Library** and **TikTok Creative Center (Top Ads)** | EU-delivered ads (library); top-performing ads by region and industry, including the UK (Creative Center) | Spend; full coverage of every advertiser |
| **Microsoft, Pinterest and X ad repositories** | EU-delivered ads under the Digital Services Act | UK-only campaigns |
| **The company's own Auction Insights** (Google Ads, Microsoft Advertising) | Which competitors appear in the same search auctions, impression share, overlap rate, outranking share, top-of-page rate. The best observed evidence of search competition | Anything outside the company's own auctions |
| **Live search results** | Who is bidding on which terms today, ad copy, assets and offers. Use Google's Ad Preview and Diagnosis tool or a clean browser set to the target location | A full picture; results vary by user, time and device |
| **Competitor websites** | Landing pages linked from ads (look for tracking parameters such as gclid, utm_source, li_fat_id, fbclid); offers and pricing; tracking tags present (Meta pixel, LinkedIn Insight Tag, TikTok pixel, Google Ads tag, Reddit pixel) | Whether a tag means active spend (it's evidence of intent or past use, so label any channel conclusion Inferred) |

**Direct links that save time** (swap in the advertiser name, domain or country code):
- LinkedIn: `https://www.linkedin.com/ad-library/search?accountOwner=NAME&countries=GB&dateOption=last-30-days`
- Google: `https://adstransparency.google.com/?region=GB&domain=DOMAIN`
- Meta: `https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=GB&q=NAME`

**Practical notes from use**:
- The LinkedIn library's advertiser search matches names loosely ("Wise" also returns Wiser, WISE and others). Check the advertiser on each result, try the exact company page name, and say when coverage is partial.
- LinkedIn results show executive posts marked "Promoted by [company]" (Thought Leader ads) and sponsored messages with the sender's name and full text. Both are revealing about a competitor's sales motion.
- The Google Transparency Centre renders ads as images, so reading page text returns almost nothing. Take a screenshot and zoom in on the results instead.
- Domain searches for companies with consumer and business products (wise.com, revolut.com) mix both; look for business landing pages in the ads before drawing conclusions.
- Pages can take a few seconds to load after navigation; if the text you read looks like the previous page, wait and read again.

**Capturing screenshots and direct links**:
- **Meta**: open `https://www.facebook.com/ads/library/?id=LIBRARY_ID` (the library ID shows on every ad card). The page opens with the ad in a "Link to ad" panel; crop the screenshot to that panel. That URL is the direct link.
- **LinkedIn**: the search page's "View details" and image links point to `/ad-library/detail/NUMBER`; read the page's links to collect them. Video ads show a black frame on their detail page, so screenshot the search results row instead (three cards side by side read well) and give each card's detail link in the caption.
- **Google Transparency Centre**: screenshot the results grid after scrolling it into view; link to the domain search. Individual creative pages exist but are slower to reach.
- Save screenshots to disk with descriptive names (advertiser, platform, what the ad says). Crop to the ad; full-window shots are hard to read in a document.
- Screen capture fails when the computer running the browser is asleep or the window is hidden. After two failures, stop, keep the links, and note which images are missing.

**UK caveat**: the UK is outside the EU, so UK-only campaigns don't carry Digital Services Act reach and targeting detail. If a competitor also advertises in the EU, its EU entries can reveal how it targets and scales.

**Absence is weak evidence**: no ads in a library today doesn't mean the competitor doesn't use the channel; campaigns are often seasonal or bursty. Record the date checked and say "not observed on [date]" rather than "doesn't use".

## Third-party estimates (label as Reported, naming the tool)

Semrush, SpyFu and Similarweb (search keywords and traffic estimates), Adthena (search share of voice, and now AI assistant ad tracking), Pathmatics and Sensor Tower (social and display spend estimates), MediaRadar. These are estimates from panels and scraping. Useful for direction and relative scale; never present the numbers as fact.

## Indirect evidence (label as Inferred)

- Job adverts (hiring a paid social manager, a programmatic lead or a connected TV specialist signals investment)
- Platform case studies naming the competitor (LinkedIn, Google, Meta and The Trade Desk publish these)
- Press releases, award entries, agency announcements
- Annual reports and earnings commentary on marketing spend and channel mix
- Conference talks and podcasts by their marketing team
- Sponsorships and partnerships visible on social channels

## How to work through it

1. **Confirm the competitor set.** Use those named. If none are named, pick the three most likely from the description (direct product overlap, same buyer, same market) and say so. Separate *direct* competitors from *attention* competitors (others bidding for the same queries or audiences).
2. **For each competitor, check the libraries most relevant to the channels in play.** With a browser available, open them directly; without one, use web search and tell the person which checks to run, or ask for screenshots.
3. **Capture, per competitor:**
   - Channels present (with label and date)
   - Messaging angles: price, speed, trust or regulation, product breadth, integrations, service, customer proof, sustainability, local presence
   - Formats: video length and style, static, carousel, document, thought leader posts, creator content
   - Offers and calls to action: free trial, demo, calculator, guide, discount, event
   - Funnel emphasis: demand capture (search, retargeting) versus demand creation (video, connected TV, creators)
   - Markets and languages
   - Notable absences
4. **Turn findings into openings.** For each, state what this company could do and why it plausibly works:
   - An angle nobody owns
   - A channel where the audience is but competitors aren't (or are weak)
   - Keyword territories competitors don't cover, or cover with weak ads
   - Formats competitors use badly or not at all
   - Places where competitors are strong and the company should not try to win head-on

## Output table

| Competitor | Channels (label, date) | Lead messaging angle | Formats | Notable absences | Opening for us |
|---|---|---|---|---|---|

## Rules of fair play (UK)

- Comparative advertising must follow the CAP Code (comparisons must be verifiable and not misleading).
- Bidding on a competitor's trademark as a keyword is generally allowed in Google Ads in the UK; using it in ad text can be restricted after a trademark complaint.
- Don't recommend copying competitor creative; recommend learning from the pattern.
