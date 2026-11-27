# Mapping Pardot to HubSpot and Salesforce

## Contents
1. Element-by-element mapping table
2. Where data should live: system-of-record rules
3. Field mapping method
4. Reconciling the prospect, contact and lead models
5. Preserving `pi__` field values
6. Known gaps with no HubSpot equivalent

---

## 1. Element-by-element mapping

Columns: what it is in Pardot → what to build in HubSpot → what Salesforce does after migration → gap or decision.

| Pardot | HubSpot | Salesforce after migration | Gap / decision |
|---|---|---|---|
| Visitor (anonymous) | Anonymous visitor (`hubspotutk` cookie) | — | Anonymous history does not transfer. Known people are re-identified on their next HubSpot email click or form fill. (Certain) |
| Prospect | Contact (unique by email) | Lead or contact, linked by Salesforce Lead ID / Contact ID properties | Several same-email prospects collapse to one contact (§4). |
| Prospect account | Company | Account (company sync) | HubSpot deduplicates companies through associated contacts, not domain (`hubspot-salesforce-integration.md`). |
| Opportunity (read-only in Pardot) | Deal (deal sync) | Opportunity stays the record | Deal sync needs company sync on first. Contact roles still drive contact associations. (Depends: hub and tier for pipelines) |
| Pardot campaign / connected campaign | HubSpot campaign (groups assets) **plus** Salesforce campaign membership written by workflows | Salesforce campaign remains the attribution record | HubSpot campaigns do not sync to Salesforce campaigns (Verify: HubSpot announced work on two-way campaign sync in 2026 — check status). |
| Static list | Static segment | — | Lists were renamed segments in HubSpot. |
| Dynamic list | Active segment | — | Criteria on Salesforce-only fields need those fields mapped into HubSpot first. |
| Public list (preference centre) | Subscription type | — | Map each public list to a subscription type deliberately; do not create one per list by reflex. |
| Segmentation rule | One-off workflow or import into a static segment | — | Run once at migration, then retire. |
| Automation rule | Workflow (with re-enrolment) | — | Pardot rules are retroactive; workflows enrol going forward unless you enrol existing records. |
| Completion action | Workflow triggered by the form submission, page view or email click; some actions are form settings | — | See `automation-rebuild.md` §4. |
| Page action | Workflow on page view, or an engagement-score rule | — | Needs HubSpot tracking code on those pages. |
| Engagement Studio programme | Workflow (branches, delays, goals) | — | In-flight prospects need a re-entry plan. |
| Score | Engagement score (Lead scoring tool) | Custom field fed by HubSpot | Legacy "HubSpot score" property is retired — do not build on it. (Certain) |
| Grade and profiles | Fit score(s) with threshold property | Custom field fed by HubSpot | No letter-grade arithmetic; bands come from thresholds (`automation-rebuild.md` §2). |
| Form | HubSpot form (embedded, not in an iframe) | — | Kiosk mode has no direct equivalent. |
| Form handler | Forms API submission to a HubSpot form, or non-HubSpot forms (collected forms) | — | See `web-tracking-and-domains.md` §3. |
| Landing page and layout template | Landing page and theme/template | — | Templates are rebuilt; no converter. (Depends: hub for landing pages and theme editing) |
| Email template / email content | Email template (drag-and-drop or coded) | — | Merge tags rewritten (§3). |
| List email | Marketing email (regular) | — | |
| Engagement Studio email / autoresponder | Automated marketing email sent by a workflow | — | |
| Operational email | Transactional email add-on, or a one-to-one sales email | — | No free bypass of marketing opt-out. (Depends: add-on) |
| Dynamic content | Smart content (rules include segment membership, lifecycle stage, country, device, referral source, language) or personalisation in coded templates | — | Pardot keys on one field; HubSpot rules key mostly on segment membership — create one active segment per variation. (Depends: Professional or above for smart content) |
| Snippet | Saved sections / global content | — | |
| File | File manager | — | File views from the website are not tracked as an activity; email link clicks are. File URLs cannot be redirected in HubSpot. (Certain) |
| Custom redirect | Tracking URL with UTM parameters; optionally a URL redirect on a HubSpot-connected domain | — | No "custom redirect clicked" activity or completion action. |
| Tag (prospect) | Multi-select or text property, or static segment | — | |
| Opted Out | **Unsubscribed from all email** (`hs_email_optout`) | Email Opt Out (synced both ways by the integration) | (Certain) |
| Do Not Email | No equivalent. Import as opted out, or a custom property plus a global exclusion segment | Keep a custom checkbox | §6. |
| Hard bounced | No importable bounce status. Exclude from import, or custom property plus exclusion segment | `pi__Pardot_Hard_Bounced__c` copied to a custom field before uninstall | §6 and `data-migration-and-compliance.md`. |
| Assigned user | Contact owner | Owner (synced two-way; users matched by name and email) | Queue owners need a plan (`hubspot-salesforce-integration.md` §6). |
| Source campaign, first touch URL, first referrer, UTM fields | Custom "Pardot legacy …" properties | Copies of `pi__` values in custom fields | HubSpot's original-source properties cannot be overwritten by import. |
| Business unit | One portal with the Brands add-on, or separate portals | — | (Depends: number of business units and how separate the teams are) |
| Salesforce user sync | HubSpot users; owners matched by name and email | — | |
| Webinar / event connectors | App marketplace integrations (Zoom, GoTo Webinar, ON24 and others) | — | Behaviour differs per app; test registration and attendance flows. |
| Einstein features | No equivalent; HubSpot's own AI features vary by tier | — | |

## 2. Where data should live: system-of-record rules

Decide the owner of each field, then express the decision as a sync rule. Default rules for this scenario:

1. **Salesforce owns** anything sales or finance uses to run the business: record owner, account, lead status, lead and contact record type, opportunity data, customer flags, territory, contract and product fields. In HubSpot these are read-only copies — sync rule *Always use Salesforce* (or *Prefer Salesforce unless blank* where HubSpot may legitimately fill a blank). (Certain as a design principle)
2. **HubSpot owns** marketing engagement and permission data: scores, subscription status, marketing-created source and UTM properties, form-collected interest fields, lifecycle stage up to the hand-off point. Push them to Salesforce custom fields that sales can see and report on. For contact properties, the integration's rules are expressed from Salesforce's side, so check whether *Always use HubSpot* / *Use HubSpot unless blank* are offered for contact mappings in the client's portal (they are offered for the updated deal sync and custom object sync). (Verify)
3. **Shared** (*Two-way*, most recent wins): name, job title, phone, address — fields both teams edit. Keep this list short; every two-way field is a potential overwrite.
4. **Email opt-out** is handled by the integration's dedicated opt-out sync, not an ordinary mapping (`hubspot-salesforce-integration.md` §8).
5. **Legacy Pardot values** are frozen: imported once, never synced again.

Write each decision into the field-mapping workbook (`assets/field-mapping-template.csv`).

## 3. Field mapping method

1. Export Pardot's prospect field list (default and custom) with sync behaviour and Salesforce field mapping.
2. Export Salesforce lead and contact field metadata (API name, type, picklist values, required, used by which flows and reports).
3. For each Pardot field decide: **migrate and sync**, **migrate once (legacy)**, or **retire**. Retire anything with no reads in the last 12 months unless legal or reporting needs it.
4. Create HubSpot properties with the **same type and identical picklist values** as the Salesforce field. Mismatched picklist values are the commonest sync error. (Certain)
5. Salesforce **reference fields** (lookups) arrive in HubSpot as 18-character record IDs, not labels; formula fields sync but changes to them do not trigger a sync. (Certain)
6. If a lead field and a contact field share an API name, HubSpot syncs one property to both — use this for fields that should follow a record through lead conversion. (Certain)
7. Each object allows up to 500 field mappings. (Certain)
8. Rewrite merge tags in content. Common pairs:

| Pardot (PML / HML) | HubSpot |
|---|---|
| `%%first_name%%` / `{{Recipient.FirstName}}` | `{{ contact.firstname }}` (set a default) |
| `%%company%%` / `{{Recipient.Company}}` | `{{ contact.company }}` |
| `%%user_name%%` / `{{Sender.FullName}}`-style sender tags | contact owner tokens, e.g. `{{ owner.firstname }}` (Verify exact token name in the editor) |
| `%%unsubscribe%%` / `{{{unsubscribe}}}` | The required footer's unsubscribe link — do not hand-code |
| `%%email_preference_center%%` / `{{{EmailPreferenceCenter}}}` | Subscription preferences link in the footer |
| Dynamic content tag | Smart content rule, or HubL `{% if %}` in a coded template |

## 4. Reconciling the prospect, contact and lead models

**The models side by side**

- Pardot: prospect ↔ one Salesforce lead **or** contact, keyed on CRM ID; several prospects may share an email. Prospect without a CRM ID = exists only in Pardot.
- HubSpot: contact ↔ one Salesforce lead **or** contact, keyed on email. One contact per email address. Companies ↔ accounts; deals ↔ opportunities.
- Salesforce: leads (no account) convert into contact + account (+ opportunity). The same person can exist as a lead and a contact at once.

**How HubSpot chooses when Salesforce has duplicates (Certain):** when the HubSpot contact first syncs, HubSpot searches Salesforce by email and links to the first record returned (in no defined order); after that it follows whichever same-email record was updated most recently. The link can therefore jump between records and overwrite data. When records are merged in Salesforce, the surviving record should be the one HubSpot is currently linked to (shown in the contact's Salesforce Lead ID or Contact ID property).

**Lead conversion (Certain):** when a synced lead is converted, HubSpot detects the new contact and keeps the same HubSpot contact, now linked to the contact. Setting a HubSpot lifecycle stage never converts a Salesforce lead. In Salesforce, converting a lead moves its campaign memberships, open activities and activity history to the contact — which makes "convert into the existing contact" the usual way to resolve lead-and-contact duplicates without losing campaign history. Converting into an existing contact does not simply overwrite the contact's field values with the lead's, so check opt-out and other key fields on the survivor. (Verify field behaviour with test pairs in the sandbox)

**Opt-out on surviving duplicates (Certain):** HubSpot's opt-out sync writes Email Opt Out only to the one Salesforce record a contact is linked to. Any duplicate left in Salesforce keeps its own value and can look mailable to sales — another reason to resolve duplicates rather than leave them.

**Recommended reconciliation sequence**

1. **Size the problem.** Salesforce report: leads and contacts grouped by email with count > 1, split into lead+lead, contact+contact and lead+contact. Pardot: prospects grouped by email with count > 1, and prospects with no CRM ID.
2. **Set a survivorship rule** with sales operations. A common rule: contact beats lead; among leads, the most recently active (or the one with an open opportunity or owner) wins. Lead+contact pairs: convert the lead into the existing contact, or delete or archive it if it carries nothing of value.
3. **Fix in Salesforce, not in HubSpot**, before the first HubSpot sync. **Irreversible:** merges, conversions and deletions cannot be undone — export the records first. Take the full Pardot prospect export (including the recycle bin) **before** the clean-up too: the suppression file must come from that export, because duplicates removed in Salesforce take their opt-out and Do Not Email flags with them. (Data loss if skipped)
   - While the Pardot connector is live, each conversion or merge also changes Pardot (the losing prospect may be relinked, duplicated on the surviving record or sent to the recycle bin). Harmless for HubSpot if suppression comes from the earlier export, but warn whoever reads Pardot reports. (Verify on test pairs)
4. **Mailability across duplicates:** if any same-email prospect was opted out, Do Not Email or hard bounced, the email address is suppressed in HubSpot. Pardot already applied unsubscribes and hard bounces across the set; Do Not Email may differ between duplicates, so take the strictest value. (Compliance)
5. **Pardot-only prospects** (no CRM ID): decide whether they should ever reach Salesforce. Usual answer: import into HubSpot, keep them out of the integration's inclusion segment until they meet a qualification threshold, so the integration does not create thousands of Salesforce leads on day one.
6. **Records without email** in Salesforce cannot be matched by HubSpot and are poor marketing targets anyway; leave them in Salesforce. (Verify how the integration treats them in the client's portal)
7. **Person accounts**, if enabled, need separate testing. (Depends)

## 5. Preserving `pi__` field values

**Data loss / Irreversible** if skipped: uninstalling the Pardot package deletes these fields and their values.

1. Create custom fields on Lead and Contact (same API names on both, so values survive conversion), for example `Legacy_Pardot_Score__c`, `Legacy_Pardot_Grade__c`, `Legacy_Pardot_Source_Campaign__c`, `Legacy_Pardot_First_Touch_URL__c`, `Legacy_Pardot_Created_Date__c`, `Legacy_Pardot_Last_Activity__c`, `Legacy_Pardot_Hard_Bounced__c`, `Legacy_UTM_Source__c` and so on.
2. Copy values with a data loader or flow after the connector is paused (so values are final).
3. Repoint reports, list views, dashboards, flows, validation rules and formulas from `pi__` fields to the new fields. Use "Where is this used?" on each field and search report metadata.
4. Optionally map the legacy fields to read-only HubSpot properties (*Always use Salesforce*) so marketers can segment on them.
5. Only then plan the package uninstall — and not before the post-cutover stabilisation period has ended.

## 6. Known gaps with no HubSpot equivalent

| Pardot feature | Closest HubSpot approach | Trade-off |
|---|---|---|
| Letter grades A+–F with thirds-of-a-letter arithmetic | Fit score with threshold bands; optional workflow writing a letter to a custom property | Different numbers from day one; communicate a new scale rather than pretending it matches |
| Do Not Email (marketer suppression distinct from opt-out) | (a) Opt-out import — strongest, but merges with "unsubscribed"; (b) custom checkbox + exclusion segment added to every send | (a) loses the distinction; (b) relies on people remembering the exclusion — enforce with a default send exclusion where available |
| Hard-bounce status | Exclude from import; or custom property + exclusion segment | HubSpot only learns bounces from its own sends |
| Custom redirect click as an activity with completion actions | Tracking URL with UTMs → page view of a tracked destination; workflow on page view | Only works when the destination carries HubSpot tracking |
| File download tracking from the website | Host behind a landing page or tracked page; or custom behavioural events | Extra click for the visitor; events need Enterprise |
| Kiosk / data entry mode forms | Separate form used only on staff devices, or entering contacts directly in the CRM | No cookie suppression switch equivalent (Verify current form options) |
| Repeating automation rules (match every N days) | Workflow re-enrolment on a date property, or schedule-based enrolment | Re-enrolment triggers are narrower than Pardot criteria (Verify available triggers) |
| Scoring categories by campaign folder | Multiple engagement scores, each filtered to the relevant assets | Number of scores limited by tier (Depends) |
| Engagement History in Salesforce | HubSpot Embed on Salesforce page layouts, plus activity sync to Salesforce tasks | Each viewer needs a HubSpot login; does not work in mobile apps; task sync creates volume (`hubspot-salesforce-integration.md` §9) |
| Account Engagement multi-touch attribution models in Salesforce | Salesforce Customizable Campaign Influence fed by HubSpot-written campaign members; HubSpot attribution reports | (Depends: Salesforce and HubSpot editions) |
