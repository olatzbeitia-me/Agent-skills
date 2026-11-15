# Attribution and reporting continuity

## Contents
1. What the client's reporting probably depends on today
2. The continuity design
3. Preserving first-touch and source data
4. UTM capture after migration
5. Campaign membership conventions
6. HubSpot-side attribution
7. Handling the transition period in reports

---

## 1. What reporting depends on today

Confirm which of these the client actually uses before designing anything (discovery questions in `discovery-questions.md`):

- **Prospect source campaign** (`pi__campaign__c`) — first touch, set once by Pardot. (Certain)
- **Connected campaigns** — Pardot campaigns are Salesforce campaigns; members and statuses are written by Pardot automation. (Certain)
- **Salesforce campaign influence**: either Salesforce's own **Customizable Campaign Influence** (auto-association of campaigns to opportunities through campaign membership and opportunity contact roles within a time window) or Account Engagement's **multi-touch attribution models** (first touch, last touch, even distribution) delivered with higher Account Engagement editions and B2B Marketing Analytics. (Depends: editions and setup — check Setup → Campaign Influence)
- **Pardot first-touch fields**: first touch URL, first referrer, search terms, and UTM values captured by Pardot's Google Analytics connector into `pi__utm_*` fields. (Depends: whether the connector was enabled)
- **Engagement History dashboards** and **B2B Marketing Analytics** (CRM Analytics) datasets. (Depends)

## 2. The continuity design

The aim is one series that runs unbroken through the cutover date. Salesforce is the only system that holds both the history and the future, so it is the reporting spine. (Certain as design principle)

1. **Keep Salesforce campaigns as the record of campaign response.** Keep creating campaigns there, with the same naming convention, hierarchy and member-status vocabulary Pardot used.
2. **HubSpot writes membership exactly where Pardot did.** For every Pardot completion action, automation rule or Engagement Studio step that added people to a Salesforce campaign, build the equivalent **Set Salesforce campaign** workflow action with the same status (`hubspot-salesforce-integration.md` §10).
3. **Keep influence calculated in Salesforce.** Salesforce's Customizable Campaign Influence auto-association runs on Salesforce data (campaign members plus contact roles), so it continues after Pardot as long as membership keeps arriving. Account Engagement's own attribution models stop updating when Pardot is switched off. If the client relies on those, decide now: move the official model to Salesforce's customizable influence (and rebuild reports on it), or to HubSpot attribution, and document the break. (Depends; Verify which model the current dashboards use)
4. **Opportunity contact roles** remain essential — influence and HubSpot deal–contact associations both need them. If sales does not add contact roles reliably, fix that as part of the project; a migration will not cure it.

## 3. Preserving first-touch and source data

- HubSpot's **Original Traffic Source** (previously "Original Source") and its drill-down properties are set by HubSpot and cannot be overwritten by import; contacts created by import or integration typically show an offline source. (Certain that they are system-set; Verify current label and import behaviour) Do not try to force Pardot values into them.
- Instead create frozen **legacy properties** in HubSpot (and matching Salesforce custom fields, filled from `pi__` copies): Legacy Pardot source campaign, Legacy first touch URL, Legacy first referrer, Legacy UTM source / medium / campaign / content / term, Legacy Pardot created date.
- Create a **unified "Marketing first touch" field** (Salesforce custom field, or HubSpot property synced to Salesforce) that reports read: legacy value if the record pre-dates cutover, HubSpot original source otherwise. A formula field in Salesforce can do this without moving data. (Certain as approach)

## 4. UTM capture after migration

- HubSpot reads UTM parameters on tracked page views into its traffic-source properties automatically. (Certain)
- To keep raw UTM values as Pardot did (for reporting in Salesforce), add hidden fields to HubSpot forms for utm_source, utm_medium, utm_campaign, utm_content and utm_term, mapped to custom properties; HubSpot can populate hidden fields from query-string parameters with matching names. Decide whether these are first-touch (set only when blank) or last-touch (overwrite) — Pardot's were first touch. (Certain; Verify persistence across pages — hidden fields only see parameters on the page where the form sits, so a short script that stores UTMs in a cookie may be needed)
- **Non-HubSpot (collected) forms do not collect hidden fields.** Use HubSpot forms or the Forms API if UTM capture matters. (Certain)

## 5. Campaign membership conventions

Write these down once and apply them to every HubSpot asset:

| Interaction | Salesforce campaign | Member status |
|---|---|---|
| Content download form | The content's campaign | Responded |
| Webinar registration | Webinar campaign | Registered |
| Webinar attendance (from webinar app) | Webinar campaign | Attended |
| Demo or contact-sales form | Inbound demo campaign | Responded |
| Email click in a campaign email | The email's campaign | Clicked (only if the client tracked this in Pardot) |

Statuses must exist on each Salesforce campaign (campaign member status setup), and "Responded" flags drive influence — keep the same choices Pardot made so historical and new data are comparable.

## 6. HubSpot-side attribution

- HubSpot's attribution reports (contact-create and deal/revenue attribution with first, last and multi-touch models) need HubSpot interactions and, for revenue, deals synced from Salesforce. (Depends: Marketing Hub Professional for some reports, Enterprise for revenue attribution; Verify current tier mapping)
- HubSpot interaction history starts at go-live, so HubSpot attribution is meaningful only for opportunities created after enough post-cutover activity has accumulated — typically one sales cycle. Use Salesforce influence for anything that spans the cutover. (Certain)
- Keep HubSpot campaigns for asset-level performance (what content worked); use Salesforce campaigns for people and pipeline (who responded, what revenue). (Certain as design principle)

## 7. Handling the transition period in reports

- Add a **migration date** marker (a dated annotation in dashboards, and a "System of record at creation" field on leads: Pardot / HubSpot) so analysts can split series.
- During parallel running, a person can generate activity in both systems; count campaign response from Salesforce membership only, never by adding Pardot and HubSpot email metrics together.
- Snapshot the key Pardot and Account Engagement dashboards (as exports and screenshots) on the day before cutover; they will not be reproducible after Pardot is switched off. (Data loss if skipped)
- Expect a visible dip in "known visitor" and identified-traffic metrics after the tracking-code swap: HubSpot starts with no cookies and re-identifies people only as they click or submit. Explain this to stakeholders in advance.
