# Measurement and attribution checks

Read this before auditing any channel. Measurement problems are usually the highest-impact findings, because every automated bidding system learns from the conversion signal it is given. A wrong signal does not just mis-report performance; it actively steers spend towards the wrong people.

## 1. Is the optimisation signal the right one?

For every campaign, find out which conversion action it optimises towards, and compare that with what the business values.

| Business type | Weak signal (common) | Stronger signal |
|---|---|---|
| Business-to-business, long sales cycle | Any form fill, content download, lead gen form submit | Qualified lead, meeting booked, opportunity created, pipeline value, closed-won value, imported from the customer relationship management system |
| Ecommerce | All purchases at gross revenue | Purchases at revenue net of VAT and expected returns; ideally gross profit; new-customer purchases weighted higher if acquisition is the goal |
| Local services and clinics | Clicks to call, page views | Calls over a minimum duration, booked appointments, attended consultations |
| Subscription and apps | Installs, sign-ups | Trial-to-paid, first payment, retained at day 30 |

Questions to ask:
- Which actions are set as *primary* (used for bidding) versus *secondary* (reported only)? Google Ads lets each campaign use account-default or campaign-specific goals; check both.
- Are micro-conversions (page views, scrolls, video views) counted as conversions and inflating volume?
- Is the same action counted more than once (duplicate tags, both Google Ads tag and imported Google Analytics conversion, pixel plus Conversions API without deduplication)?
- For lead generation: what share of platform-reported leads become qualified? If the person doesn't know, that is itself a finding.

**When volume is thin**, bidding directly on the deepest stage (closed-won) may starve the algorithm. The usual fix is to optimise to the deepest stage that still produces enough volume (often qualified lead or meeting booked), and feed values so the algorithm can prefer better leads. Check each platform's current guidance on minimum volumes rather than quoting a number from memory.

## 2. Are the numbers true?

**Reconcile platform claims with the source of truth.** Add up conversions reported by every platform for the same period and compare with the customer relationship management system or back-end orders. Platforms each claim credit for the same customer, view-through windows add more, and modelled conversions fill consent gaps. Any material gap is a finding; explain it before trusting any platform's numbers.

**Tagging and data quality**
- Google: Google tag or Tag Manager firing on the right events; enhanced conversions (for web and for leads) sending hashed first-party data; consent mode implemented, which Google requires for users in the UK and European Economic Area for its personalisation and measurement features (verify current requirements).
- Meta: pixel plus Conversions API with deduplication (shared event ID); event match quality; correct optimisation event.
- LinkedIn: Insight Tag plus Conversions API; customer relationship management system integration for lead quality and revenue attribution.
- Microsoft Advertising: Universal Event Tracking tag; enhanced conversions; consent mode.
- Server-side tagging where client-side signal loss is high.

**UK consent rules (Information Commissioner's Office guidance, checked October 2026).** The Data (Use and Access) Act 2025 added a "statistical purposes" exception to the consent rules for cookies and similar technologies, in force from February 2026. It only covers aggregate analytics used solely to improve the site, with any provider acting as a processor and users told and able to object. The ICO states that advertising purposes are not exempt and never have been; that includes ad measurement and performance, frequency capping and click fraud detection, and linking a visitor to ad conversions. So advertising tags (Google Ads, Meta pixel, LinkedIn Insight Tag, TikTok pixel) still need consent, and consent rates and consent mode set-up still matter.

**Ecommerce specifics**
- Revenue in platforms usually includes VAT and excludes returns and cancellations, so reported return on ad spend overstates true return.
- Separate new from returning customers. Spend that mostly reaches existing customers looks efficient and grows little.
- Track a blended marketing efficiency ratio (total revenue ÷ total paid media spend) alongside platform figures as a sanity check.
- Check for reporting changes before diagnosing a decline. A drop in reported return on ad spend after an attribution setting or default change may be a measurement shift, not a performance one. Compare like with like.

**Long sales cycles**
- Conversion windows: if the cycle exceeds the platform's maximum click window, final outcomes can't be attributed directly; rely on earlier-stage proxies and offline imports with click identifiers.
- Lag: imported conversions arrive weeks after the click, so recent periods always look worse. Judge on cohorts by click date.

## 3. Offline and customer relationship management system feedback

This is the single most valuable fix for most business-to-business and high-consideration accounts.

- **Google Ads**: offline conversion import or enhanced conversions for leads, matched on the click identifier or hashed email. Native connectors exist for HubSpot and Salesforce. Import stages with values (qualified lead, opportunity, closed-won) so value-based bidding can prefer leads that become revenue.
- **Meta**: Conversions API events for customer relationship management system stages; Meta has a lead optimisation goal that learns from those downstream stages (check its current name and availability).
- **LinkedIn**: Conversions API and customer relationship management system connections; revenue attribution reporting depends on the integration.
- **Microsoft Advertising**: offline conversion import.

Check that the identifier (click ID or hashed email) is captured at the form and stored on the record, or the import will match nothing.

## 4. Attribution and incrementality

No single attribution model is the truth. Use them together:

- **Platform attribution**: fast, granular, biased towards itself.
- **Analytics data-driven attribution** (Google Analytics 4 and similar): cross-channel but limited to tracked, consented journeys.
- **Customer relationship management system source fields**: closest to revenue, but often first-touch or last-touch only.
- **Incrementality tests**: the most reliable answer to "did this spend cause sales?" Options include geographic holdouts (pause or add spend in matched regions), platform conversion lift studies, and brand search holdouts.
- **Marketing mix modelling**: for larger, multi-channel spend with two or more years of data. Open-source options include Google's Meridian and Meta's Robyn.

Recommend incrementality testing where a large share of spend sits in channels whose platform-reported results are hard to believe: brand search, retargeting, Performance Max, Advantage+, view-through-heavy display and video, connected TV.

## 5. Findings to look for (with typical business effect)

| Finding | Typical effect |
|---|---|
| Bidding on raw form fills while a large share of leads are unqualified | Algorithm learns to find more cheap, unqualified leads; cost per qualified lead rises while cost per lead looks healthy |
| No offline conversion import | Can't use value-based bidding; can't tell which campaigns produce revenue |
| Duplicate counting across tags | Inflated performance; budget scaled into campaigns that aren't working |
| Revenue includes VAT and returns | Return on ad spend overstated by roughly the VAT rate plus the return rate; break-even misjudged |
| No consent mode or poor consent rates | Large blind spots; modelled data filling gaps; weaker bidding |
| Brand and non-brand reported together | Brand conversions (which would mostly happen anyway) mask weak non-brand performance |
| View-through conversions counted equally with clicks | Display, video and social look far stronger than they are |
