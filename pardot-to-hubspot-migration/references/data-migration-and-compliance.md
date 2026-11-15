# Data migration, clean-up and compliance

## Contents
1. What to export from Pardot, and how
2. Load order into HubSpot
3. Opt-outs, Do Not Email and suppression
4. Bounces and list hygiene
5. Deduplication
6. Consent, legal basis and subscription types
7. Data protection: hosting, erasure, retention
8. Historical activity and engagement
9. Reconciliation checks

---

## 1. What to export from Pardot

Export everything below **before** any destructive step and keep it in client-controlled storage with access restricted (it is personal data). Record when each export was taken; take a final delta at cutover.

| Data | How | Notes |
|---|---|---|
| All prospects, all fields, including system fields (Pardot ID, CRM lead and contact IDs, Opted Out, Do Not Email, bounce fields, score, grade, source campaign, created and last-activity dates) | UI prospect export (all fields) or API version 5 prospect query | Include the **recycle bin** — deleted prospects may include opted-out addresses that must stay suppressed. (Certain) |
| List memberships (static, dynamic, public, suppression) | API version 5 list membership query, or per-list export | Public list membership becomes subscription status. |
| Visitor activities (email sends, opens, clicks, form and form-handler submissions, page views, file and custom-redirect clicks, webinar activity) | **Export API version 5**, chunked by date range | Asynchronous, uses daily API allowance, jobs expire after 7 days if not finished. Start weeks ahead. (Certain) |
| Form and form-handler submissions with timestamps and the consent text on the form | Visitor activities + screenshots/copies of form wording and privacy notices | Evidence of consent (§6). |
| Email sends and performance by email | Email reports export; API | For historical reporting. |
| Asset inventories: forms, form handlers, landing pages, files, custom redirects, vanity URLs, emails, templates, dynamic content, snippets, automation rules, segmentation rules, Engagement Studio programmes, scoring rules, profiles, tracker domains, users, connectors | API version 5 objects where available; screenshots for scoring, profiles and Engagement Studio logic | Fill `assets/pardot-inventory-template.csv`. |
| Field list with sync behaviour | Admin → configure fields | Input to the mapping workbook. |
| `pi__` field values in Salesforce | Copy into custom fields (`object-and-field-mapping.md` §5) | **Data loss** if the package is uninstalled first. |

## 2. Load order into HubSpot

Order matters because HubSpot can email anyone it holds. (Certain as principle)

1. **Portal-level settings**: data hosting location (§7) — **Irreversible** in one direction; data privacy settings turned on if the client relies on legal-basis tracking; subscription types created; required properties created (including legacy properties).
2. **Opt-out import** of every address that must never receive marketing (§3).
3. **Salesforce integration configured but quiet** (no inclusion-segment members, HubSpot-led write rules not yet active).
4. **Contacts**: either via a Salesforce import in HubSpot (keeps the record link) or CSV import keyed on email with Pardot data. Most migrations do both: Salesforce import to establish the link, then a CSV update import keyed on email to add Pardot-only fields and legacy values. (Certain as approach)
5. **Pardot-only prospects** (no CRM ID) via CSV import, outside the inclusion segment.
6. **Subscription statuses** per subscription type and **legal basis**, via import options or the communication preferences API (§6).
7. **Marketing contact status** set by workflow on a defined segment.
8. **Static segments** rebuilt from list membership.
9. Re-run the opt-out import with the cutover delta.

## 3. Opt-outs, Do Not Email and suppression

**Compliance** — this is the step with legal exposure.

- Build one suppression file of email addresses from: Pardot Opted Out = true, Do Not Email = true, hard bounced (unless handled separately, §4), the Pardot recycle bin with any of those flags, Salesforce Email Opt Out = true on leads and contacts, and any manual suppression lists (competitors, legal holds, former employees). Deduplicate on lower-cased, trimmed email.
- Use HubSpot's **opt-out import** ("List of contacts to opt out of emails"): it sets **Unsubscribed from all email** to true; addresses that are not already contacts are **not created and not billed**; existing contacts are unsubscribed and stay billable. The addresses are included when you export bounced and unsubscribed contacts. (Certain)
- With the Brands add-on, opt-out imports can be run per brand. (Certain)
- Once unsubscribed through an import, a person can be emailed one-to-one only with a one-time legal basis; they must resubscribe themselves to receive marketing again. (Certain)
- **Do Not Email**: HubSpot has no separate marketer suppression flag. Choose:
  - (a) Include them in the opt-out import — simplest and safest; loses the distinction from genuine unsubscribes. Document that the HubSpot "unsubscribed" population includes Pardot Do Not Email records.
  - (b) Import a custom checkbox "Do not email (legacy)" and an active segment that is excluded from every send — keeps the distinction but depends on people adding the exclusion.
  Recommend (a) unless someone has a real need to email Do Not Email records later.
- Run the same suppression file again at cutover for anything that changed during parallel running.

## 4. Bounces and list hygiene

- HubSpot cannot import a hard-bounce status; it learns bounces only from its own sends. (Certain)
- Options for Pardot hard bounces: leave them out of the contact import entirely (if they have no other value), or include them in the opt-out import, or import with a "Legacy hard bounce" property and exclude via segment. Re-sending to known-dead addresses from HubSpot damages its sending reputation in the first weeks — exactly when it matters most (`email-deliverability.md`). (Certain as practice)
- Long-unengaged records (no click or form in, say, 18–24 months): do not make them marketing contacts at launch. Consider a re-permission email **from Pardot before cutover**, so Pardot's established reputation carries the risk, then migrate only those who engage. (Certain as practice)
- Role addresses (info@, sales@) and obvious test records: review before import.

## 5. Deduplication

- Fix duplicates in **Salesforce** before the first HubSpot sync (`object-and-field-mapping.md` §4). **Irreversible:** export before merging.
- Normalise emails (trim, lower-case) before any import; HubSpot matches case-insensitively but stray spaces and invisible characters create separate contacts. (Verify with a test import)
- Clean Pardot placeholders such as `[[unknown]]` in Company and Last Name, or HubSpot will copy them into personalisation.
- After loading, run HubSpot's duplicate management tool for same-person-different-email cases.

## 6. Consent, legal basis and subscription types

- **Subscription types** replace Pardot public lists and the preference centre. Define a small set that matches how the client actually emails (for example: newsletter and research, events and webinars, product updates). Each marketing email must use one. (Certain)
- **Mapping status**: for each subscription type, set opted-in or not-opted-in from Pardot public list membership and global opt-out. Where the portal's import options cannot set subscription status with a legal basis, use the **communication preferences API**. (Verify which subscription fields the import tool currently accepts)
- **Legal basis**: if HubSpot's data privacy settings are on, every contact needs a legal basis for processing and for communication. Record it as stated in the client's records — for example "freely given consent" for opt-in forms, "legitimate interest – existing customer" where that is the client's documented position. Do not assign legal bases by guesswork; get sign-off. (Compliance)
- **Evidence of consent**: HubSpot import does not recreate the original consent event. Keep the Pardot export of form submissions with timestamps and the wording of each form's consent text, and store a "Consent source" and "Consent date (legacy)" property on the contact. (Certain as practice)
- **Double opt-in**: if the client used a confirmation step in Pardot (via autoresponder or form logic), decide whether to enable HubSpot's double opt-in for new subscribers. (Depends)

## 7. Data protection: hosting, erasure, retention

- **Data hosting location** is chosen when the paid HubSpot account is created; the EU data centre (Frankfurt) has been available since 2021. Accounts can move from the US East data centre to another location, but **not out of the EU data centre**. (Certain) Confirm with the client's data protection lead which regimes apply — for a company headquartered in Switzerland with European and other offices that may include the Swiss revised data protection act, EU and UK data protection regulation, and local rules where it has offices (Verify headquarters and office locations rather than assuming) — and which hosting location is required before the portal is provisioned. **Irreversible** in practice once data is loaded.
- Some HubSpot sub-processors process data outside the hosting region; the data protection officer should review HubSpot's sub-processor list and data processing agreement. (Certain)
- **Erasure requests**: HubSpot's permanent delete for privacy requests removes the contact and blocks the email from future marketing. (Verify exact behaviour in the knowledge base) Records permanently deleted in Pardot may still exist in Salesforce; if they do, the integration can recreate them in HubSpot. Reconcile Pardot's erasure history against Salesforce before the first sync. (Compliance)
- **Retention**: decide how long the raw Pardot exports are kept, where, and who can open them; record the decision. They contain personal data and behavioural history.

## 8. Historical activity and engagement

HubSpot cannot import Pardot email, page-view or form activity as native timeline activity. (Certain) Options, best first:

1. **Summary properties on the contact** (imported once): Pardot first activity date, last activity date, last email click date, last form submission date, number of form submissions in the last 24 months, final Pardot score and grade, Pardot source campaign, first touch URL. Cheap, segmentable, enough for most nurture and scoring decisions.
2. **Raw history in a warehouse or file store** (the Export API output), for analysis and audits.
3. **Custom behavioural events** sent through HubSpot's events API with the original timestamp, for a narrow set of high-value events (for example demo requests). (Depends: Enterprise; Verify how far back timestamps are accepted and whether scoring and reports use back-dated events)
4. Notes or timeline events through a private app — rarely worth the effort.

Accept and communicate that HubSpot's engagement reporting and engagement scores start at zero on go-live.

## 9. Reconciliation checks

Run after every load and again after cutover:

- Count: Pardot mailable prospects (deduplicated by email) versus HubSpot contacts not unsubscribed — explain every difference.
- Every address in the suppression file is unsubscribed in HubSpot (export unsubscribed contacts and compare).
- Sample of 50 records: field values match across Pardot export, HubSpot and Salesforce.
- No HubSpot contact in an active marketing segment has the legacy Do Not Email or hard-bounce flag.
- Salesforce: no new duplicate leads created by the integration (report on leads created by the integration user, grouped by email).
- Sync health: error count trending to zero; every remaining error explained.
