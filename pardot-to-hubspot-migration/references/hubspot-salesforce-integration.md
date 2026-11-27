# Configuring the HubSpot–Salesforce integration to replace the Pardot connector

Facts checked against HubSpot's knowledge base in October 2026. The integration changes often — re-check any setting name before writing it into a runbook.

## Contents
1. Prerequisites and the integration user
2. Install order and sandboxes
3. How and when records sync
4. Contacts: direction, creation, inclusion segment, selective sync
5. Field mappings and sync rules
6. Owners
7. Companies and deals
8. Email opt-out sync
9. Activity and task sync
10. Salesforce campaigns and campaign members
11. Duplicates
12. API usage and sync health
13. Running alongside the Pardot connector
14. Recommended starting configuration for the client

---

## 1. Prerequisites and the integration user

- HubSpot: a Professional or Enterprise hub (Marketing Hub Professional or above for this use). (Certain) One HubSpot portal connects to **one** Salesforce instance. (Certain)
- Salesforce: an edition with API access. (Certain)
- Create a **dedicated Salesforce integration user** (not a person's login), so changes are attributable and flows can identify it. It needs API access, read and edit on every synced object and field (field-level security included), visibility of all records that should sync (sharing rules — if it cannot see leads, they will not sync), and the HubSpot integration permission set installed with the package. (Certain)
- Validation rules, required fields and duplicate rules apply to the integration user's writes. Either make HubSpot supply valid values or exempt the integration user deliberately. (Certain)
- Login IP restrictions on the integration user, or "Enforce login IP ranges on every request", can stop the connection. (Certain)

## 2. Install order and sandboxes

1. Install and test against a **Salesforce sandbox** first: on install, tick "Yes, this will connect to a sandbox". (Certain) Use a HubSpot sandbox or a separate test portal so production HubSpot is not polluted. (Depends: HubSpot Enterprise for standard sandboxes; Verify sandbox support for the integration)
2. The installer puts the HubSpot integration package into Salesforce and walks through default mappings. (Certain)
3. **Installing syncs nothing by itself.** Records sync when a sync trigger fires or when you run a Salesforce import in HubSpot. (Certain) This lets you configure everything before a single record moves.
4. Later switching from sandbox to production uses "Connect a different production user" / "Connect a new sandbox" actions; changing the integration user needs equal or higher permissions. (Certain)

## 3. How and when records sync

- Sync triggers include record creation in either system (subject to settings), changes to mapped fields, form submissions, marketing and sales email events (if activity sync is on), lifecycle transitions (if that setting is on), adding a contact to a Salesforce campaign through a HubSpot form, and manual resyncs. (Certain)
- HubSpot also checks for changes about **every 15 minutes**. (Certain) Changes to **formula fields** in Salesforce do not trigger a sync. (Certain)
- Contacts without an email address do not sync to Salesforce. (Certain)

## 4. Contacts: direction, creation, inclusion segment, selective sync

- Salesforce leads and contacts both sync to **HubSpot contacts**. (Certain)
- **HubSpot → Salesforce creation**: new HubSpot contacts create Salesforce **leads** by default; the alternative is contacts. Choose one — it is not conditional. Creating contacts without accounts produces private contacts visible only to the integration user and admins, so leads are the safer default for the client unless sales works contact-first. (Certain)
- If HubSpot creates **leads**, turn off HubSpot's "automatically create and associate companies with contacts" setting, or you will get duplicate companies and accounts; HubSpot recommends syncing as contacts if you keep that setting on. (Certain)
- **Salesforce → HubSpot creation**: settings decide whether new Salesforce leads and/or contacts create HubSpot contacts. When on, they are created **even if the contact would not be in the inclusion segment**. (Certain)
- **Inclusion segment** (formerly inclusion list): an **active** segment; only members sync from HubSpot to Salesforce. With no inclusion segment, every HubSpot contact syncs. Membership changes trigger a sync; selecting a segment does not bulk-sync it. Records outside the segment that were imported from Salesforce arrive with only the email populated. (Certain)
- **Selective sync** filters which Salesforce records sync into HubSpot, set in the integration settings. Use it to keep, for example, customer-support contacts or particular record types out of HubSpot. (Certain; Verify filter options available in the client's portal)
- **Marketing contacts**: records created by integrations are non-marketing by default, and the Salesforce integration has its own setting for whether synced contacts become marketing contacts (Settings → Integrations → Marketing contacts). Leave it off and promote with a workflow, or the HubSpot bill jumps. (Verify: setting location and default in the portal)
- **Deletion**: the integration settings decide whether deleting a Salesforce lead or contact deletes the HubSpot contact. Turn this on only if Salesforce deletions are deliberate (for example erasure requests); merges in Salesforce delete the losing records' HubSpot contacts when it is on. (Certain)

## 5. Field mappings and sync rules

- Sync rules for contact mappings: **Prefer Salesforce unless blank**, **Always use Salesforce**, **Two-way** (most recent change wins), **Don't sync**. The updated deal sync and custom object sync add **Always use HubSpot** and **Use HubSpot unless blank**. (Certain) Check whether the HubSpot-led rules are now offered for contact mappings in the client's portal. (Verify)
- Owner mapping is always two-way, whatever the screen shows. (Certain)
- Standard mappings cannot be deleted, only set to Don't sync — except "Unsubscribed from all email", which cannot be set to Don't sync. (Certain)
- Limit: 500 mappings per object. Field types must be compatible; picklist values must match exactly. Reference (lookup) fields arrive as 18-character IDs. A lead field and contact field with the same API name both receive the value. (Certain)
- After adding a mapping, existing values do not backfill by themselves — resync records, or run a Salesforce import in HubSpot. (Certain)
- Mappings can be exported to CSV from the property mappings tab — export after every change and keep it with the field-mapping workbook. (Certain)
- **Salesforce state and country picklists**, if enabled, reject free-text values that do not match; build HubSpot dropdown properties with Salesforce's exact values. (Certain as Salesforce behaviour; Verify which value form the integration sends)

## 6. Owners

See `automation-rebuild.md` §7 for assignment. Integration facts: owners are matched on **name and email** between HubSpot users and active Salesforce users; unmatched owners do not sync; new Salesforce leads with no matching owner get Salesforce lead assignment rules; records that end up with no owner belong to the integration user. (Certain) Provision HubSpot users for everyone who owns records in Salesforce, with the same email address.

## 7. Companies and deals

- **Company sync** (accounts ↔ companies) is optional. HubSpot matches companies to accounts through **associated syncing contacts**, not domain. Leads have no accounts. Company sync now supports its own inclusion segment and selective sync. Bulk resyncs of company mappings are capped at 200,000 companies at a time. (Certain)
- **Deal sync** (opportunities ↔ deals): turn company sync on and import Salesforce accounts **before** deal sync, or account associations on opportunities are lost. Map pipelines and stages. HubSpot **does not deduplicate deals** — a HubSpot-created deal always creates a new opportunity. The updated deal sync adds pipeline mappings, association sync, selective sync and inclusion segments. (Certain; Depends: Sales Hub tier for number of syncing pipelines)
- For a marketing-led migration, sync opportunities **from** Salesforce to HubSpot for reporting and keep opportunity creation in Salesforce.

## 8. Email opt-out sync

- When a contact unsubscribes from all email in HubSpot, or **Email Opt Out** is ticked on the Salesforce lead or contact, the other system is updated. (Certain)
- Clearing Email Opt Out in Salesforce **does not** resubscribe a HubSpot contact; the person must opt back in themselves. (Certain)
- Opt-out status does not sync for a contact until that contact's **first sync** — people outside the inclusion segment are not covered. (Certain)
- The sync touches only the **one** Salesforce lead or contact the HubSpot contact is linked to; same-email duplicates in Salesforce keep their own Email Opt Out value. (Certain) This is why the opt-out import into HubSpot (`data-migration-and-compliance.md` §3) is required, not optional.
- Subscription-type preferences (individual newsletters) do not map to Salesforce by default; if sales needs them, add custom checkbox fields fed by workflows. (Verify current options)

## 9. Activity and task sync

- HubSpot can create Salesforce **tasks** for form submissions, marketing email sends, opens and clicks, sales emails, meetings, calls, notes and tasks. (Certain)
- Opens and clicks are **not deduplicated** when sent to Salesforce: repeated opens and forwarded emails create multiple tasks. Only form submissions within one year of the contact's first sync are sent. (Certain)
- Recommendation: sync form submissions and email clicks; do not sync opens or sends. Give sales the full engagement view through HubSpot Embed (below) rather than through task volume. (Certain as practice)

**HubSpot Embed: the replacement for Engagement History** (HubSpot knowledge base, checked November 2026)

- HubSpot Embed is a window inside Salesforce records that shows the record's HubSpot timeline, property history and workflow enrolments, and lets users enrol the record in a workflow or sequence and book meetings. It is the closest equivalent to Pardot's Engagement History components. HubSpot is deprecating its legacy managed package and the Visualforce module inside it; use HubSpot Embed instead. (Certain)
- **Install:** in HubSpot, Settings → Integrations → Connected Apps → Salesforce → Feature Discovery → Install HubSpot Embed. Then, in Salesforce, add the `HubSpot_Embed_[object]_V2` Visualforce page to every lead, contact, account and opportunity page layout that needs it — one layout at a time — or make those pages available for Lightning Experience and add them to Lightning record pages as Visualforce components. Installing it, and receiving its automatic updates, needs the Customize Application permission in Salesforce. (Certain)
- **Each viewer needs a HubSpot login.** A Salesforce user sees the window only if they are also a HubSpot user, logged in to HubSpot, with permission to view the record. List everyone in sales who reads Engagement History today and plan a HubSpot user for each. (Certain for the login requirement; Verify with the HubSpot account team which seat each user needs and what it costs)
- **Not on mobile.** HubSpot Embed does not work in mobile apps or their in-app browsers, so anyone who reads engagement on the Salesforce mobile app loses that view. (Certain)
- Accounts and opportunities show HubSpot data only when they sync to a HubSpot company or deal that is associated with a syncing contact. (Certain)

## 10. Salesforce campaigns and campaign members

- **HubSpot campaigns and Salesforce campaigns are separate objects and do not sync** (HubSpot knowledge base, August 2026). (Certain as of that date) A HubSpot product manager stated in 2026 that two-way campaign and campaign-member sync was in development. (Verify status before designing around it)
- Native ways to write membership (Certain):
  - Workflow action **Set Salesforce campaign**, choosing campaign and member status. Status values must exist on that campaign.
  - Associating a HubSpot form with a Salesforce campaign — member status is fixed at "Responded", cannot be edited, the association cannot be removed, and share-link submissions are excluded. With the updated form editor HubSpot recommends workflows instead.
  - Only campaigns marked **Active** in Salesforce are available. 
- Reading membership in HubSpot: the **Salesforce Campaign ID** contact property holds the campaigns a contact belongs to and can be used in segments; member status is not available natively. (Certain)
- Full campaign and member data in HubSpot: sync Campaign and Campaign Member as **custom objects** (Enterprise). Limits: a custom object syncs to contacts **or** leads, not both; removing someone from a campaign does not trigger a sync. (Certain)
- Pattern for continuity with Pardot's connected campaigns: keep creating campaigns in Salesforce, keep the same member-status vocabulary, and have each HubSpot asset's workflow set membership exactly as Pardot's completion actions did (`attribution-and-reporting.md`).

## 11. Duplicates

- Matching key is **email**. When Salesforce has several leads or contacts with the same email, HubSpot links to the first record returned on first sync, then follows whichever was updated most recently. Merge in Salesforce keeping the record HubSpot is linked to. (Certain)
- A HubSpot contact re-paired with a different Salesforce record is treated as a new pairing — an initial sync — so field values may be pushed back to Salesforce. (Certain)
- Several HubSpot contacts with different emails pointing to one Salesforce record: merge in HubSpot keeping the syncing contact. (Certain)
- Turn on Salesforce duplicate rules for leads and contacts on email (alert or block for the integration user, per the client's tolerance) so new duplicates do not appear after the clean-up.

## 12. API usage and sync health

- Allocate a share of Salesforce's daily API calls to HubSpot in the integration settings; the **Sync health** tab shows calls used in the last 24 hours and every sync error. (Certain)
- Third-party guidance puts usage at up to about four calls per contact sync and three per record on resync — budget large imports and resyncs in batches. (Verify against the client's limits during the sandbox load)
- Check sync errors daily during migration; the commonest are picklist mismatches, validation rules, required fields, field-level security and records the integration user cannot see.

## 13. Running alongside the Pardot connector

Both connectors writing the same Salesforce fields at the same time is the main technical risk of the migration.

- Until cutover, keep HubSpot from writing to Salesforce for live records: either no inclusion segment members yet, or mappings set to *Always use Salesforce* / *Don't sync* for anything Pardot also writes. (Certain as approach)
- Never map HubSpot properties to `pi__` fields.
- Email Opt Out is the exception that helps: during parallel running both Pardot (via the Opted Out sync behaviour) and HubSpot sync opt-outs with Salesforce's Email Opt Out, so Salesforce can carry an unsubscribe from one system to the other. Set Pardot's Opted Out sync behaviour to *Use the most recently updated record* (or *Use Salesforce's value*) for the parallel period, and test it with a dummy record both ways. It only covers people who exist in Salesforce and, on the HubSpot side, have synced at least once. (Certain mechanism; Verify end-to-end in sandbox)
- Update Salesforce automation that recognises the B2BMA Integration User so it also recognises the HubSpot integration user.
- At cutover, pause the Pardot connector **before** turning on HubSpot's write paths (`cutover-checklist.md`).

## 14. Recommended starting configuration for the client

Adjust once the discovery facts are known.

| Setting | Starting recommendation | Why |
|---|---|---|
| HubSpot-created Salesforce records | Leads | Avoid account-less private contacts |
| Auto-create and associate companies by domain | Off | Prevent duplicate companies with lead sync |
| Inclusion segment | Active segment: has email, not a known test or competitor domain, and (lifecycle stage ≥ marketing qualified lead **or** already linked to a Salesforce record **or** submitted a sales-intent form) | Stops the integration creating a Salesforce lead for every newsletter subscriber |
| New Salesforce leads/contacts create HubSpot contacts | On, with selective sync excluding records sales does not want marketed to | Keeps marketing's view of Salesforce complete |
| Marketing contact status for synced records | Non-marketing; promote via workflow | Controls cost |
| Contact deletion follows Salesforce | Off until erasure process is defined | Merges would delete HubSpot contacts |
| Company sync | On, after Salesforce de-duplication | Needed for deal associations and account-level reporting |
| Deal sync | On, Salesforce → HubSpot reporting focus | Attribution reporting in HubSpot |
| Activity sync to tasks | Form submissions and email clicks only | Task volume |
| HubSpot Embed | On lead and contact layouts (accounts and opportunities if they sync); HubSpot users for the salespeople who need it | Replaces Engagement History; each viewer needs a HubSpot login |
| Lifecycle automatic transitions | On | Moves stages forward from Salesforce events |
| Owner | Salesforce assignment rules on first sync | Reuse existing routing |
