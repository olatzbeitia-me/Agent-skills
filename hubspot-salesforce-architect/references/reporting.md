# Reporting and measurement

Contents: 1 Principles · 2 Which system owns which metric · 3 Definitions to agree first · 4 Report catalogue · 5 Dashboards · 6 Attribution

## 1. Principles

- **One official number per metric.** Decide which system is the source of truth for each metric, publish it, and treat the other system's version as diagnostic. Two "official" pipeline numbers will end every meeting in an argument about data instead of decisions.
- **Build in the system that already holds the data.** Pipeline and revenue live in Salesforce, so finance-grade numbers come from Salesforce. Engagement lives in HubSpot, so channel and content performance come from HubSpot.
- **Stamp, don't look up.** Write the marketing source onto the opportunity when it is created (a Salesforce flow copying from the primary contact role). A report that looks up a contact's source today will change when the contact's data changes.
- **Cohort and period views answer different questions.** Period view: "How many MQLs did we create in October and how many opportunities were created in October?" Cohort view: "Of the MQLs created in October, how many became opportunities, whenever that happened?" With a long sales cycle, only the cohort view gives an honest conversion rate. Label every conversion chart with which one it is.

## 2. Which system owns which metric

| Metric | Owner | Why |
|---|---|---|
| Email, web, form and content engagement | HubSpot | Data originates there |
| Contacts and MQLs created by source | HubSpot | Source and lifecycle dates live there |
| MQL acceptance, disposition, speed-to-lead | Salesforce | Rep actions happen there |
| Opportunities, pipeline, bookings, win rate | Salesforce | Finance reconciles to it |
| Marketing-sourced and influenced pipeline (official) | Salesforce | Needs opportunity amounts and stages |
| Multi-touch attribution (diagnostic) | HubSpot (Enterprise revenue attribution) | Needs full touch history; requires opportunities synced as deals |
| Campaign return on investment | Salesforce campaign influence, with costs held on the campaign | Keeps cost and revenue in one place |
| Sync and data health | HubSpot Sync Health plus Salesforce data quality reports | Both sides fail differently |

## 3. Definitions to agree first

Write these down, with exact field logic, before building anything.

| Term | Recommended definition |
|---|---|
| MQL | Date entered Marketing Qualified Lead is set (see `hubspot-inbound.md`) |
| Accepted | Lead status moved from New to a working value by a sales user |
| SQL | Lead status set to the qualified value, or lead converted with an opportunity |
| Marketing-sourced opportunity | `Marketing_Source__c` on the opportunity is a marketing channel AND the primary contact's MQL date is before the opportunity created date |
| Marketing-influenced opportunity | At least one contact role on the opportunity had a marketing campaign touch within the agreed look-back (for example 180 days) before the opportunity created date |
| Speed-to-lead | Business hours from MQL date to first logged sales activity or status change |
| Pipeline | Sum of opportunity amount for open opportunities at or beyond the agreed qualified stage |

Never add influenced pipeline across campaigns. One opportunity influenced by five campaigns counts once.

## 4. Report catalogue

Each entry gives: the question it answers, where to build it, data source, filters and breakdowns, and the visual.

1. **Funnel volume and conversion**
   - Question: where do contacts stall?
   - Build: HubSpot funnel report on lifecycle stages (Lead, MQL, SQL, Opportunity, Customer), cohort by create date, last 12 months.
   - Breakdowns: client segment, original source, region.
   - Visual: funnel with stage-to-stage conversion and median days in stage.

2. **Lead source and channel performance**
   - Question: which channels create MQLs and pipeline, not just contacts?
   - Build: HubSpot for contacts and MQLs by original source and drill-down; Salesforce opportunity report grouped by `Marketing_Source__c` for pipeline.
   - Visual: table with contacts, MQLs, MQL rate, opportunities, pipeline, closed-won per source.

3. **Lead-to-opportunity conversion**
   - Question: what share of MQLs turn into opportunities, and how fast?
   - Build: Salesforce report type of leads with converted lead information plus contacts with opportunities, filtered on MQL date cohort; 90 and 180-day windows.
   - Breakdowns: segment, source, region, owner.

4. **Speed-to-lead**
   - Question: are hand-raisers contacted inside the agreed time?
   - Build: Salesforce, using a flow-stamped first activity date or status change date on Lead.
   - Metrics: median business hours, share within the agreed time.
   - Breakdowns: owner, region, hand-raiser versus scored MQL.

5. **Sales and marketing service level agreement**
   - Question: is every MQL dispositioned?
   - Build: Salesforce leads with lifecycle MQL and status New older than two business days (the "aging" list), acceptance rate, rejection reasons, recycle volume.
   - Audience: weekly joint pipeline meeting.

6. **Campaign return on investment**
   - Question: which campaigns and events earn their cost?
   - Build: Salesforce campaigns with Actual Cost entered, campaign influence for pipeline and closed-won; HubSpot campaign reports for engagement.
   - For events and webinars add registrants, attendees, meetings booked, influenced pipeline.

7. **Content performance**
   - Question: which research and assets create qualified demand?
   - Build: HubSpot attribution reports (contact create attribution by asset and interaction type), downloads by asset, MQLs from first conversion by asset, influenced pipeline where Enterprise attribution is available.
   - Pair with ungated page views and AI assistant referrals for the full picture.

8. **Pipeline sourced and influenced**
   - Question: what is marketing's contribution to pipeline?
   - Build: Salesforce using the definitions above; trended monthly with a 12-month view.
   - Show sourced and influenced side by side, never combined.

9. **Account engagement (account-based)**
   - Question: are target accounts warming up, and across the buying group?
   - Build: HubSpot company report for target accounts with count of engaged contacts in 30 days, buying roles covered, account engagement trend; Salesforce pipeline from target versus non-target accounts.

10. **Expansion**
    - Question: is marketing helping existing clients buy more?
    - Build: Salesforce opportunities of type upsell or cross-sell with campaign influence; HubSpot engagement of contacts at client accounts.

11. **Data and sync health**
    - Question: can we trust the numbers above?
    - Build: HubSpot Sync Health error counts by category; Salesforce reports of records owned by the integration user, leads missing country or segment, duplicate candidates; HubSpot contacts missing lawful basis.

## 5. Dashboards

| Dashboard | Audience | System | Cadence | Contents |
|---|---|---|---|---|
| Executive marketing contribution | Chief marketing officer, chief revenue officer, leadership | Salesforce | Monthly | Sourced and influenced pipeline, closed-won from marketing-sourced, MQL to opportunity cohort conversion, top five campaigns by influenced pipeline |
| Marketing performance | Marketing team | HubSpot | Weekly | Contacts and MQLs by source, funnel, content and email performance, scoring distribution |
| Sales and marketing service level agreement | Sales and marketing leads | Salesforce | Weekly | MQL aging, acceptance rate, rejection reasons, speed-to-lead by owner |
| Campaign and event | Campaign owner | Both | Per campaign | Registrations, attendance, MQLs, meetings, influenced pipeline, cost |
| Operations health | Marketing ops, Salesforce admin | Both | Daily in hypercare, weekly after | Sync errors, API use, integration-owned records, data completeness |

## 6. Attribution

- Pick the model to fit the question. For long business-to-business cycles use a W-shaped model (first touch, lead creation, opportunity creation) or full-path for diagnosis; do not make last touch the official model, because it credits whatever happened just before a rep logged the opportunity.
- HubSpot revenue attribution needs Marketing Hub Enterprise (verify current packaging) and Salesforce opportunities synced as HubSpot deals with contacts associated. Without opportunity sync it cannot see revenue.
- Salesforce campaign influence assigns opportunities to campaigns through contact roles and a look-back window. Configure the look-back to match the sales cycle and enforce contact roles, or influence will be understated.
- Report self-reported source ("How did you hear about us?") alongside software attribution. Where they disagree, that gap is often where peer referral, podcasts and AI assistants sit.
- Present attribution as a range of evidence for budget decisions, not as an exact accounting truth.
