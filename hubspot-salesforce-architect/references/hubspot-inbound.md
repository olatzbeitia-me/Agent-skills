# HubSpot inbound and Marketing Hub

Contents: 1 Lifecycle and lead status · 2 MQL, SQL and the handoff agreement · 3 Lead scoring · 4 Forms, landing pages and calls to action · 5 Email, workflows and sequences · 6 Campaigns and naming · 7 Segments · 8 Subscriptions and consent · 9 Content and search

## 1. Lifecycle stage and lead status

Two properties do two different jobs. Keep them separate.

- **Lifecycle stage** (`lifecyclestage`) records how far a contact has progressed in the relationship. It is a one-way ratchet: HubSpot only moves it forward unless a workflow first clears the value. Default stages: Subscriber, Lead, Marketing Qualified Lead, Sales Qualified Lead, Opportunity, Customer, Evangelist, Other. Stages can be customised on Professional and Enterprise (verify current options before recommending renames).
- **Lead status** (`hs_lead_status`) records the working state of a contact in the sales queue. Default values: New, Open, In Progress, Open Deal, Unqualified, Attempted to Contact, Connected, Bad Timing. Replace these with values that match the Salesforce lead status picklist exactly.

Analogy for non-admins: lifecycle stage is the highest school year a pupil has reached; lead status is whether they are in class today.

### Recommended definitions for a B2B data-as-a-service business

| Stage | Entry rule | Set by |
|---|---|---|
| Subscriber | Opted in to research or newsletter emails only | HubSpot form or import |
| Lead | Any conversion or known contact with a lawful basis | HubSpot default |
| Marketing Qualified Lead | Combined score crosses the agreed threshold, or any hand-raiser (demo request, data sample request, contact sales) | HubSpot workflow |
| Sales Qualified Lead | Sales representative has accepted and confirmed need, authority or timing (lead status moved to the agreed "qualified" value in Salesforce) | Sync from Salesforce lead status, via HubSpot workflow |
| Opportunity | Contact is a contact role on an open Salesforce opportunity | Connector setting "Adjusting Lifecycle Stage" |
| Customer | Contact is a contact role on a closed-won opportunity, or the account is an active client | Connector setting, plus company lifecycle sync |

### Recycling without breaking reports

When sales rejects or disqualifies an MQL, do not drag lifecycle stage backwards by default. Instead:

1. Set lead status to the agreed rejection value in Salesforce (for example "Unqualified" or "Recycle") with a required reason picklist (`Recycle reason`: no budget, wrong role, timing, competitor customer, student or personal, duplicate).
2. A HubSpot workflow triggered by that status enrols the contact in a re-engagement nurture and stamps a `Recycled date`.
3. If the business insists on resetting lifecycle to Lead so the contact can re-qualify, use a controlled workflow (clear lifecycle stage, then set Lead) and test in a sandbox first how the stage date properties behave, because funnel reports depend on them.

### Lifecycle stage in Salesforce

Create one custom picklist with the same API name on Lead and Contact, for example `HubSpot_Lifecycle_Stage__c`, so HubSpot writes to both. Contact field mappings do not offer an "Always use HubSpot" rule, so make the field HubSpot-owned like this: map it with the **Two-way** rule, then make it read-only in Salesforce for every profile except the integration user (field-level security). Add it to the Lead conversion field mapping in Salesforce so the value carries from Lead to Contact.

## 2. MQL, SQL and the handoff agreement

Write the service level agreement down and get sales leadership to sign it. Without it, scoring and routing arguments never end.

| Element | Recommendation |
|---|---|
| MQL definition | Fit threshold AND engagement threshold, OR any hand-raiser form. Document the exact score thresholds. |
| Hand-raiser response | First contact within four business hours in the prospect's region. Agree the figure with sales; measure it from the MQL date. |
| Scored MQL response | First contact within two business days. |
| Disposition | Every MQL gets a lead status change within five business days: accepted, working, qualified, or rejected with a reason. |
| Rejection reasons | Fixed picklist, never free text, so marketing can learn from it. |
| Review | Monthly joint review of acceptance rate, rejection reasons and conversion to opportunity. |

## 3. Lead scoring

Build scoring in the Lead Scoring tool (Marketing > Lead Scoring on Professional and Enterprise). The legacy "HubSpot score" property stopped working on 31 August 2025. Each score you create generates a score property and a threshold property, which is what workflows and Salesforce should use. Check current point limits per tier before designing.

Use separate Fit and Engagement scores. A combined single number hides why someone qualified, and sales trusts a score they can read.

### Fit score (who they are)

| Criterion | Example points |
|---|---|
| Client segment = Bank, Asset manager or owner, Insurance provider | +20 |
| Client segment = Corporate, Private equity or debt, Hedge fund | +15 |
| Buying role in a core buying function | +15 |
| Seniority: head of, director or above | +10 |
| Country in a covered sales territory | +5 |
| Personal or free email domain | -20 |
| Student, academic (unless public sector is a target), or competitor domain | -30 |

### Engagement score (what they do)

| Criterion | Example points | Notes |
|---|---|---|
| Pricing, solutions or demo page visit | +10 | Cap per time frame |
| Gated research report download | +8 | Weight flagship reports higher than older ones |
| Webinar attended | +10 | Registered but did not attend: +3 |
| Email click | +3 | Ignore opens: Apple Mail Privacy Protection inflates them |
| Return visit within 7 days | +5 | |
| Regulatory hub visit | +5 | |
| Inactivity | Decay over 90 days | Use the tool's decay or time-frame options |

Hand-raisers bypass the score: a workflow sets MQL directly.

### Account-level view

For account-based work, score companies as well as contacts where the tool supports company scores, or roll contact engagement up to a company property via workflow. A useful trigger for an account-based play: two or more engaged contacts from two different buying roles at a target account within 30 days.

### Calibration

Back-test against the last 12 months: score the contacts who became Sales Qualified Lead or sat on a closed-won opportunity, and check that most would have crossed the threshold. Review thresholds quarterly with sales using MQL acceptance and conversion rates.

## 4. Forms, landing pages and calls to action

- Use HubSpot forms with progressive profiling. Capture company, job title, country (dropdown using the same values as the Salesforce State and Country picklists), client segment and buying role. Fewer fields on report downloads; more on demo requests.
- Add hidden fields for UTM parameters only if they are needed beyond HubSpot's own source tracking (for example to pass to Salesforce campaigns).
- Associate each form with an active Salesforce campaign where campaign membership matters. The Salesforce campaign must be set to Active in Salesforce to appear.
- Block free email domains on demo and data sample forms; allow them on report downloads but score them down.
- Gate deep research; publish an ungated summary page for search engines and AI assistants.
- Add a free-text "How did you hear about us?" field on demo requests. Self-reported source catches podcasts, peer referrals and AI assistants that tracking misses.

## 5. Email, workflows and sequences

Core workflows for this profile:

1. **Hand-raiser routing**: form = demo, data sample or contact sales → set lifecycle MQL, lead status New, add to inclusion segment, notify the owner or let Salesforce assignment rules assign.
2. **Scored MQL**: threshold property reached → set MQL, lead status New, add to inclusion segment.
3. **Nurture by segment and use case**: banks receive due diligence content; asset managers receive portfolio screening content. Exit on MQL or unsubscribe.
4. **Webinar**: registration confirmation, reminders, attended versus no-show follow-up, recording delivery.
5. **Recycle**: triggered by the rejection lead status.
6. **Data hygiene**: normalise country, job title to buying role, and segment from company properties.

Sequences in HubSpot need Sales Hub seats. If sales prospects from Salesforce or a sales engagement tool, keep one-to-one outreach there and do not split it across two tools.

## 6. Campaigns and naming

- HubSpot campaigns group assets (emails, pages, forms, ads, social). Salesforce campaigns group people and their member status. They do not natively sync; see `integration-sync.md` for the bridge.
- Naming convention used in both systems: `YYYY-Qn | Region | Type | Name`, for example `2026-Q4 | EMEA | Webinar | Supply-chain due diligence`.
- One UTM convention, written down: source in lower case, medium from a fixed list (paid-social, paid-search, email, organic-social, referral, partner, event), campaign matching the campaign name in slug form.
- Parent and child campaigns exist in both systems; check current HubSpot hierarchy depth before designing.

## 7. Segments (formerly lists)

- Active segments for anything that drives automation, sync or suppression. Static segments for one-off sends and imports.
- Name by purpose: `SYNC | Inclusion | Salesforce`, `SUPP | Global suppression`, `NUR | Banks | Due diligence`.
- Keep one global suppression segment (unsubscribed, hard bounced, competitors, legal holds) and apply it everywhere.

## 8. Subscriptions and consent

- Turn on the data privacy settings (Settings > Privacy & Consent) so the lawful basis property ("Legal basis for processing contact's data") and consent records are available.
- Subscription types by topic, not by format: Research and reports, Webinars and events, Regulatory briefings, Product updates, plus one-to-one sales email.
- Set the lawful basis on every form and import. For business contacts in the UK, legitimate interest with a clear opt-out is common for corporate addresses; sole traders and some markets need consent. The data protection officer makes the call; you make it operational.
- Check that "Unsubscribed from all email" and the Salesforce `HasOptedOutOfEmail` (Email Opt Out) field are mapped and syncing in both directions. Test it: unsubscribe a test contact in each system and confirm the other updates within one sync cycle (about 15 minutes).
- Know the limits of that sync (HubSpot Knowledge Base, August 2026). An opt-out passes between the systems only for contacts that sync, so a contact outside the inclusion segment, or a Salesforce record hidden from HubSpot by selective sync, does not carry it across. Clearing Email Opt Out in Salesforce never resubscribes a contact HubSpot holds as unsubscribed; only the person can do that. HubSpot sends only "opted out" or blank, so if Salesforce needs subscribed, unsubscribed and not specified as separate states, use custom Salesforce fields and Salesforce automation.
- Marketing contacts drive the HubSpot bill. Decide how contacts created from Salesforce are set (marketing or non-marketing) and review the count monthly.

## 9. Content and search

- Build topic clusters around use cases and regulations: a pillar page per use case, linking to reports, case studies and webinar recordings.
- Each research report should have: an ungated summary page, a gated full report, a webinar or briefing, a nurture branch, and a sales one-pager. That makes one piece of research work across every stage of the funnel.
- Track content performance with attribution reports (see `reporting.md`), not page views alone.
