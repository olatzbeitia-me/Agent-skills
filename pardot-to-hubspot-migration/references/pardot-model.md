# Pardot (Marketing Cloud Account Engagement) data model and behaviours

The detail an expert needs to audit Pardot accurately and predict what breaks when it is removed. Read the section you need.

## Contents
1. Naming, editions, business units
2. Identity: visitors, prospects, duplicate-email setting
3. Prospect fields and field sync behaviour
4. Mailability: Opted Out, Do Not Email, bounces
5. Accounts and opportunities
6. Campaigns and connected campaigns
7. Lists, segmentation rules, dynamic lists, tags
8. Automation: automation rules, completion actions, page actions, Engagement Studio
9. Scoring and grading
10. Content: forms, form handlers, landing pages, emails, templates, dynamic content, files, custom redirects, snippets
11. Tracker domains and tracking code
12. The Salesforce–Pardot connector (version 2)
13. What Pardot leaves in Salesforce (`pi__` fields, components, objects)
14. Getting data out: UI exports and API version 5
15. What happens when Pardot is switched off

---

## 1. Naming, editions, business units

- Pardot was renamed **Marketing Cloud Account Engagement** in 2022. Salesforce documentation, settings and the API now say "Account Engagement"; most practitioners still say Pardot. Both names refer to the same product. (Certain)
- Editions: **Growth, Plus, Advanced, Premium**. Limits and features differ by edition — for example scoring categories, custom object sync, business units, multi-touch attribution models, Einstein features and API call allowances. (Depends: edition — confirm from the Account Engagement contract or Setup)
- **Business units** split one Pardot licence into separate marketing databases, each with its own prospects, assets and connector settings, all connected to one Salesforce org. If the client has more than one, each needs its own inventory and its own HubSpot design decision (one portal with brands or partitioning, versus separate portals). (Depends: edition, typically Advanced or Premium)

## 2. Identity: visitors, prospects, duplicate-email setting

- **Visitor**: an anonymous browser tracked by Pardot cookies. A visitor becomes a **prospect** when identified — typically by submitting a Pardot form or form handler, or clicking a tracked link in a Pardot email. Visitor activity before identification is attached to the prospect at that point. (Certain)
- **Allow Multiple Prospects with the Same Email Address** (the setting practitioners call AMPSEA) is on by default for accounts bought after mid-2016. With it on, the unique key is the **CRM ID** (the Salesforce lead or contact ID), not email, so one email address can have several prospects — one per Salesforce lead or contact. (Certain) Check: Account Engagement Settings → Account Settings.
- Consequences under the duplicate-email setting (Certain unless marked):
  - An unsubscribe or hard bounce from one prospect is applied to **all prospects sharing that email**.
  - Engagement Studio admits only one prospect per email address per programme.
  - A form submission from an uncookied visitor whose email matches several prospects has to choose one; the matching rules favour the most recently active record (Verify: in the account's behaviour).
  - The API (version 4 onwards) cannot update a prospect by email alone; it needs the Pardot ID or CRM ID.
- **Why this matters for HubSpot:** HubSpot holds one contact per email. Every set of same-email prospects collapses to one HubSpot contact linked to one Salesforce record. See `object-and-field-mapping.md` §4.

## 3. Prospect fields and field sync behaviour

- **Default fields** include email, names, company, job title, phone, address fields, score, grade, source, campaign (the prospect's source campaign — effectively first touch), assigned user, Opted Out, Do Not Email, Do Not Call, created date, last activity, plus system fields for CRM IDs. (Certain)
- **Custom fields** are created in Pardot and usually mapped to a Salesforce lead and contact field by API name. Types include text, number, date, dropdown, radio, checkbox, multi-select, textarea, hidden and CRM user. (Certain)
- **Sync behaviour** is set per field: *Use Salesforce's value*, *Use Account Engagement's value*, or *Use the most recently updated record*. Checkbox and multi-select fields can be set to *Record and display multiple responses*. (Certain) Export the field list with sync behaviour — it is the starting point for deciding the owner of each field after migration.
- Pardot fills blank required Salesforce fields with **`[[unknown]]`** (for example Company or Last Name) when it creates a lead. Expect those values in Salesforce and decide how HubSpot should treat them. (Certain — search Salesforce for the literal string to size it)

## 4. Mailability: Opted Out, Do Not Email, bounces

- **Opted Out** — set when the prospect unsubscribes (link or email preference centre). Intended to be controlled by the prospect. Syncs with the Salesforce standard **Email Opt Out** field (`HasOptedOutOfEmail`) according to its sync behaviour setting. (Certain)
- **Do Not Email** — a marketer-controlled suppression flag. Since 2023 it is decoupled from Opted Out and can have a different sync behaviour. Admins use it for competitors, legal holds, internal staff and so on. (Certain)
- **Hard bounce** — the prospect becomes unmailable; Pardot records bounce details and syncs a hard-bounced flag to Salesforce (`pi__Pardot_Hard_Bounced__c`). Repeated soft bounces also make a prospect unmailable after a threshold. (Certain for hard bounce; Verify the soft-bounce threshold in the account)
- **Public lists and the email preference centre** — prospects can opt in or out of individual public lists while staying subscribed overall. These are the nearest thing to HubSpot subscription types. (Certain)
- **Operational emails** in Pardot are sent regardless of opt-out status. They need a lawful basis and a HubSpot equivalent that also bypasses marketing opt-out (see `object-and-field-mapping.md`). (Certain)
- **Suppression lists** used on sends (competitors, customers, internal) are business rules too and must be carried over.

## 5. Accounts and opportunities

- **Prospect accounts** mirror Salesforce accounts and are effectively read-only from Salesforce; a prospect belongs to an account through its Salesforce contact. Leads have no account. (Certain)
- **Opportunities** are read from Salesforce, and Pardot links them to prospects only through **opportunity contact roles**. Opportunities without contact roles are invisible to Pardot scoring, automation and ROI reporting. (Certain) The same contact-role dependency applies to HubSpot's deal–contact associations, so a poor contact-role habit affects reporting in both systems.

## 6. Campaigns and connected campaigns

- Every Pardot asset belongs to a Pardot campaign, and every prospect has one **source campaign** (first touch). (Certain)
- With **connected campaigns** (standard in Lightning-era accounts), each Pardot campaign is the same record as a Salesforce campaign. Campaign membership in Salesforce is written by Pardot completion actions, automation rules and Engagement Studio actions ("Add to Salesforce campaign" with a member status). (Certain)
- Engagement metrics and Engagement History dashboards on Salesforce campaign records are populated by Account Engagement. (Certain)

## 7. Lists, segmentation rules, dynamic lists, tags

- **Static lists** — members added by people, completion actions, rules or imports. (Certain)
- **Dynamic lists** — rule-based, continuously re-evaluated; members cannot be added or removed by hand. (Certain)
- **Segmentation rules** — run once against existing prospects to add to lists or tag them; they do not run again unless re-run. (Certain)
- **Public lists** — appear on the email preference centre (see §4). **Test lists** — for test sends.
- **Tags** — free-text labels on prospects and assets. HubSpot has no tag object for contacts.

## 8. Automation

- **Automation rules**: criteria (match all or any, with nested groups) against prospect fields, activities, list membership, Salesforce campaign status, account and opportunity data; actions include add or remove from list, adjust score, change field value, assign, notify, add to Salesforce campaign, create Salesforce task, add tag, change profile. They are **retroactive** — once resumed they act on every matching prospect, including existing ones. They can be set to **repeat** ("can match every N days, up to N times"), which is how score decay is usually built. (Certain)
- **Completion actions**: fire after a specific interaction with a form, form handler, landing page, file, custom redirect or, where configured, tracked email links. Not retroactive. Same action vocabulary as automation rules plus "send autoresponder email" and assignment via the active Salesforce assignment rule. (Certain; Verify email-link completion actions are in use in the account)
- **Page actions**: on specific tracked web pages; adjust score, flag priority pages, run completion actions. Require the Pardot tracking code. (Certain)
- **Engagement Studio** programmes: recipient lists and suppression lists; **actions** (send email, add to list, adjust score, assign, change field, notify, add to Salesforce campaign, create task, add tag, end), **triggers** (email opened, link clicked, form or landing page completed, file or custom redirect clicked, webinar events, and others, with "wait up to N days"), **rules** (field values, score, grade, list membership, Salesforce campaign status, account and opportunity values), wait steps, send days and times, and an option to let prospects re-enter. One prospect per email per programme under the duplicate-email setting. Programmes are paused, not exported; there is no built-in export of the step logic or of each prospect's current step. (Certain; Verify how much step detail the API version 5 Engagement Studio program object returns)

## 9. Scoring and grading

- **Score** — behavioural points. Default scoring rules award points per activity type (configured under Account Engagement Settings → Scoring). There is no built-in decay; decay is built with repeating automation rules. **Scoring categories** (by campaign folder) are available on higher editions. **Einstein Behavior Scoring** is separate and edition-dependent. Score syncs to `pi__score__c`. (Certain; Depends: edition for categories and Einstein)
- **Grade** — fit, as a letter from A+ to F. Prospects start at **D**. A prospect is assigned a **profile** (usually by automation rule); each profile criterion that matches moves the grade up or down by a third of a letter, two thirds or a full letter. Automation can mark criteria as matched or not matched. Grade syncs to `pi__grade__c`. (Certain)
- Screenshot the scoring rules, every profile and every rule that adjusts score or profile — there is no single export of the scoring model.

## 10. Content assets

- **Forms**: hosted on the tracker domain and embedded on websites in an **iframe**. Features: progressive profiling, dependent fields, bot protection (reCAPTCHA-based, needs a tracker domain), thank-you content or redirect, completion actions, layout templates, and **kiosk or data entry mode** (does not cookie the browser). (Certain)
- **Form handlers**: the website's own HTML form posts its fields to a Pardot handler URL; Pardot maps field names, runs completion actions and sends the visitor to success or error locations. No progressive profiling. Common on CMS-built forms. (Certain)
- **Landing pages**: hosted on the tracker domain, built from layout templates, with or without a form; vanity URLs. (Certain)
- **Emails**: list emails, Engagement Studio emails, autoresponders, operational emails, one-to-one emails sent by sales users. Templates exist as classic email templates and Lightning email content. Merge languages: **PML** (`%%first_name%%`, `%%unsubscribe%%`) and **HML** (`{{Recipient.FirstName}}`, `{{{unsubscribe}}}`, `{{{EmailPreferenceCenter}}}`). (Certain)
- **Dynamic content**: variations driven by **one** prospect field (or grade), embedded in emails, landing pages, forms or, via a JavaScript embed, on the website. (Certain)
- **Files**: hosted on the tracker domain; downloads are tracked and can fire completion actions. Links to them often live in PDFs, slide decks and partner sites. (Certain)
- **Custom redirects**: tracked links on the tracker domain that redirect to any URL, record a click activity and can fire completion actions. Used in social posts, ads, QR codes and printed material. (Certain)
- **Snippets**: reusable content blocks in Lightning-era accounts.
- Asset URLs typically look like `https://<tracker-domain>/l/<account id>/<date>/<code>` unless a vanity URL is set. (Verify against a few real assets)

## 11. Tracker domains and tracking code

- A **tracker domain** is a subdomain of the client's domain (for example `go.` or `info.`) with a CNAME record pointing at Pardot. It serves forms, landing pages, files, custom redirects and vanity URLs, and enables first-party tracking. Only one tracker domain can be primary per account. (Certain)
- The tracking code is a JavaScript snippet with variables `piAId` (account ID), `piCId` (campaign ID) and `piHostname`, loading Pardot's `pd.js`. Pardot cookies include `visitor_id<account id>`, `visitor_id<account id>-hash`, `lpv<account id>` and `pi_opt_in<account id>`. (Certain for variables; Verify cookie names against the live site's cookie policy)

## 12. The Salesforce–Pardot connector (version 2)

- Runs as the **B2BMA Integration User** in Salesforce. Settings include: automatically create prospects when leads or contacts are created in Salesforce (optionally limited by **Marketing Data Sharing** rules), sync emails to Salesforce as activities, connected campaigns, Salesforce user sync, and record-deletion behaviour (a deleted Salesforce record sends the prospect to the Pardot recycle bin). (Certain; Depends: edition for Marketing Data Sharing)
- Matching is by **CRM ID** under the duplicate-email setting; a prospect without a CRM ID matches by email to the first record Salesforce returns. (Certain)
- The connector can be **paused**. Pausing stops sync in both directions. (Certain) Whether changes made while paused are queued and replayed on unpause, and for how long, should be confirmed before relying on it. (Verify: Salesforce Help, "pause the Account Engagement connector")
- Salesforce flows, validation rules and Apex in many orgs exclude changes made by the B2BMA Integration User (for example "if last modified by integration user, skip"). Each needs the HubSpot integration user added. (Certain as a pattern; Verify in the client's org)

## 13. What Pardot leaves in Salesforce

- **Managed package fields** (namespace `pi`) on Lead and Contact. Typical set: `pi__score__c`, `pi__grade__c`, `pi__url__c`, `pi__campaign__c`, `pi__comments__c`, `pi__conversion_date__c`, `pi__conversion_object_name__c`, `pi__conversion_object_type__c`, `pi__created_date__c`, `pi__first_activity__c`, `pi__last_activity__c`, `pi__first_search_term__c`, `pi__first_search_type__c`, `pi__first_touch_url__c`, `pi__notes__c`, `pi__Pardot_Hard_Bounced__c`, `pi__utm_source__c`, `pi__utm_medium__c`, `pi__utm_campaign__c`, `pi__utm_content__c`, `pi__utm_term__c`, `pi__pardot_last_scored_at__c`, `pi__Needs_Score_Synced__c`. (Verify: Object Manager → Lead/Contact → Fields, filter by the `pi__` prefix — the exact list depends on package version)
- **Irreversible / Data loss:** uninstalling the managed package deletes its components, including these fields and every value in them. Salesforce offers a temporary export at uninstall, but do not rely on it — copy values you want to keep into your own custom fields first (`object-and-field-mapping.md` §5). Uninstall is also blocked while package components are referenced by layouts, buttons, reports, flows or formulas, so a dependency sweep is needed anyway. (Certain)
- **Lightning components and related lists** (Engagement History, Account Engagement activity) read from Pardot. When Pardot is switched off they stop showing data; deleted prospects already show as "archived". (Certain)
- **Campaign-level engagement metrics, B2B Marketing Analytics / CRM Analytics datasets** and Account Engagement multi-touch attribution models are populated from Pardot and stop updating; analytics datasets can be deleted when the app is reconfigured or removed. (Certain; Depends: whether the client licenses these)
- **Tasks** logged by the connector for emails sent stay in Salesforce as ordinary task records. (Certain)

## 14. Getting data out

- **UI exports**: prospect lists (choose all fields), list membership, asset tables, email reports. UI exports may carry a byte-order mark in the CSV — strip it before loading elsewhere. (Certain)
- **API version 5 query endpoints** for objects such as prospects, lists, list memberships, forms, form handlers, landing pages, custom redirects, files, emails and templates, tracker domains, campaigns and users. (Certain)
- **Export API (version 5)** for large volumes, especially visitor activities: asynchronous jobs, processed one after another per account, subject to the account's daily and concurrent API limits; exports that do not finish within 7 days expire; narrower date ranges finish faster. (Certain) Older API versions capped a single visitor-activity export at a one-year date range — chunk by quarter or month regardless. (Verify current limit in the version 5 Export API docs)
- Plan the API budget: activity history for a large database can take many days of the daily allowance. Start early.

## 15. What happens when Pardot is switched off

- Landing pages, forms, files, custom redirects and vanity URLs on the tracker domain stop working; reported behaviour is that landing pages render blank. (Certain that they stop; Verify exact behaviour)
- Unsubscribe and preference-centre links in emails already sent stop working — a compliance exposure (`web-tracking-and-domains.md` §6).
- The connector stops; `pi__` field values stay frozen in Salesforce until the package is uninstalled.
- **Data loss:** account data is reported to be permanently deleted around 90 days after deactivation. Get the actual retention period, and the date it starts, from the Salesforce account team in writing, and finish all exports well before it. (Verify)
