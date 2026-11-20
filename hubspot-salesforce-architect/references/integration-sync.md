# HubSpot-Salesforce integration and sync

Facts marked (KB) were checked against the HubSpot Knowledge Base between September and November 2026. Re-verify anything about tiers, limits or new features before quoting it to a client.

Contents: 1 Prerequisites · 2 Core settings and recommended defaults · 3 Field mapping and sync rules · 4 System-of-record matrix · 5 Handoff flow end to end · 6 Owners and assignment · 7 Duplicates · 8 Campaign bridging · 9 Sync error catalogue · 10 "Record isn't syncing" runbook · 11 Beyond the native connector

## 1. Prerequisites

**HubSpot** (KB): Professional or Enterprise in any hub (Marketing, Sales, Service, Data, Content, Smart CRM), and a user with Account Access permission.

**Salesforce** (KB): an edition with API access, or Salesforce Professional. Not Group Edition. Government Cloud is supported.

**Connected user** (KB): the Salesforce user that connects the integration. HubSpot can only do what this user can do. It needs:

- System Administrator profile
- API Enabled
- View Setup and Configuration
- Modify All on every object you sync (accounts, campaigns, contacts, leads, opportunities)
- Modify Metadata (for the HubSpot Embed window and deal sync)
- Download AppExchange Packages
- Customize Application (for installing and updating HubSpot Embed)
- The Task Type field visible on the profile

Recommendations:

1. Use a dedicated integration user, never a named person. When that person leaves, the sync breaks. Check whether a full Salesforce licence is needed for a System Administrator profile, or whether a cheaper integration licence is now supported by HubSpot, before budgeting.
2. Login IP restrictions in Salesforce can stop the connector connecting. Set the HubSpot app's IP relaxation setting in Salesforce to Relax IP Restrictions, which exempts the app while users stay restricted. "Enforce IP Restrictions on Every Request" overrides that exemption, so restrict users with a network IP range instead of turning it on (KB).
3. One Salesforce org per HubSpot account (KB). If several HubSpot accounts connect to one Salesforce org, set "Creating contacts in HubSpot" to not create contacts automatically, or each account will create the other's records.
4. HubSpot's legacy managed package with the Visualforce window is being deprecated (KB). Use HubSpot Embed.
5. Connect to a Salesforce sandbox first (there is a sandbox checkbox at install), configure and test there, then repeat in production.
6. Records do not sync automatically after installation (KB). They sync through triggers or an import from Salesforce. Plan the initial load deliberately (see `migration-playbook.md`).
7. The connector is built for an ongoing sync. A one-time move of Salesforce data into HubSpot uses HubSpot Smart Transfer instead. The two identify records differently, so using both on the same Salesforce data creates duplicates in both systems. If Smart Transfer has ever been used in the account, switch off all its sync connections before turning the connector on (KB).

## 2. Core settings and recommended defaults

Path: Settings > Integrations > Connected Apps > Salesforce > Data sync.

| Setting (KB) | Options | Recommendation for a B2B data-as-a-service business | Why |
|---|---|---|---|
| Inclusion segment (Contacts > Sync rules > Limiting What Syncs) | Any active segment; none = every contact syncs | Use one. Include: MQL and later stages; hand-raisers; contacts already known to Salesforce (Salesforce Lead ID or Contact ID is known); contacts at accounts with an open opportunity or active client status. Exclude: global suppression, personal email domains, students, competitors, test records. | Keeps Salesforce for people sales should see, saves API calls, protects rep attention. The "already known to Salesforce" rule matters: a contact created from Salesforce but outside the segment is created once and then stops receiving updates (KB). Opt-outs also pass between the systems only for contacts that sync, so the rule is a consent safeguard as well (KB). |
| When a HubSpot contact is created or updated, in Salesforce | Create or update the contact; Create or update the lead | Lead, if sales already runs a lead queue with assignment rules (most likely here). Contact, if sales works accounts directly and has a lead-to-account matching process. | Leads have no account, so if you choose lead, turn off HubSpot's automatic company creation from email domain, or duplicate companies appear when leads convert (KB). |
| When a Salesforce lead or contact is updated, in HubSpot | Create or update the contact; Do nothing | Create or update | Marketing needs to see every person sales works, for suppression and attribution. Set these as non-marketing contacts unless they have a lawful basis for marketing, to control cost. |
| When a Salesforce lead or contact is deleted | Delete the contact; Do nothing | Do nothing | Keeps engagement and consent history. Deleting in HubSpot never deletes in Salesforce (KB). |
| Adjusting Lifecycle Stage | Update the contact's lifecycle stage; Do nothing | Update | Moves contacts to Opportunity and Customer from Salesforce. Only works through opportunity contact roles, only forward, and the lead must already be syncing before conversion (KB). Enforce contact roles in Salesforce (see section 5). |
| Matching state and country fields | Picklist disabled / enabled / enabled and customised; match default values or send HubSpot values | Match the real Salesforce configuration. Use HubSpot dropdowns whose internal values equal the Salesforce picklist values. | Prevents "Mismatched state or country value" and "Missing required country" errors. |
| API call use (Sync Health > Allocated to HubSpot) | A number | Set below the org's daily limit minus other integrations' usage, with headroom of at least 20 percent. One contact sync can take up to four API calls (KB). | API exhaustion silently queues every sync, including opt-outs. |
| Companies, Deals, Tickets, Activities tabs | Toggle each object on | Companies on, Deals on, Activities on for a narrow set of types, Tickets only if service uses it. | See below. |

### Limiting what syncs from Salesforce (selective sync)

Inclusion segments only control what HubSpot sends to Salesforce. HubSpot calls control in the other direction "selective sync" (KB, October 2026), and it works differently by object:

- **Companies and deals**: filters on account or opportunity fields, combined with AND, under Data sync > [object] > Sync rules. Available only once the updated company or deal sync is switched on (see below).
- **Leads and contacts**: there is no filter. HubSpot's selective sync guide hides records from the integration user with a cloned profile, a dedicated role, a Private organisation-wide default and criteria-based sharing rules. It needs Salesforce Enterprise, HubSpot Support does not cover it, records owned by the integration user always sync, and records HubSpot creates in Salesforce must also meet the sharing rule or they stop syncing. The guide is undated and refers to a permission set from HubSpot's Salesforce package, so check it against the current package before relying on it.

Recommendation for this profile: filter accounts and opportunities only where there is a clear rule, for example opportunity record types marketing never reports on, and check the filter against the attribution scope in `reporting.md`. Avoid the sharing-rule method for leads and contacts unless volume or data minimisation requires it. A Salesforce lead or contact hidden from HubSpot no longer receives HubSpot opt-outs through the sync, so any email sent from Salesforce to those records needs its own suppression check. To test whether a record will sync, log in to Salesforce as the integration user and open it: if the integration user can see it, it syncs.

### Companies and accounts

- HubSpot companies sync with Salesforce accounts. There are 2 versions of the company sync. Ask which one the account uses before answering anything about matching, sync rules or filters.
- The **standard company sync** de-duplicates companies by associated contacts, not by domain (KB).
- The **updated company sync** (Salesforce app settings > Feature discovery > New Company Sync; KB, September 2026) keeps the standard behaviour and adds:
  - companies sync even when they have no associated contacts;
  - matching on mapped fields whose values are identical in both systems, for example a domain field, for records matched after it is switched on;
  - object-level rules for what creating, updating and deleting does in each direction, and a conflict rule that decides which system wins when two records first match;
  - association sync from Salesforce lookup fields, with association labels and a chosen direction;
  - an "Always use HubSpot" field rule, which works only while the object-level rule is two-way;
  - selective sync filters on account fields.
- Merging companies in HubSpot does not merge the Salesforce accounts; merge them in Salesforce separately (KB).
- **Switching on the updated company sync cannot be undone**, and it raises Salesforce API use while it indexes records (KB). Treat it as a large-blast-radius change: test it in a sandbox, clean the matching field first (values must match exactly, so strip prefixes such as "www." and trailing slashes from domains), confirm API headroom, and record the decision in the integration specification.
- For an account-based, sales-led business, Salesforce should own account creation and ownership. Set the company sync rules so HubSpot does not create Salesforce accounts from marketing data.
- Map Client segment, territory, account tier, target account flag and active client flag from Salesforce to HubSpot with "Always use Salesforce", so marketing segments on what sales maintains.

### Deals and opportunities

- HubSpot deals sync with Salesforce opportunities. Map each Salesforce sales process (record type) to a HubSpot pipeline and every opportunity stage to a pipeline stage. Inactive stages cause errors.
- The **standard deal sync** does not de-duplicate deals (KB).
- The **updated deal sync** (Feature discovery > New Deal Sync; KB, October 2026) migrates existing pipeline mappings automatically and adds:
  - only deals in HubSpot pipelines mapped to a Salesforce record type are eligible to sync;
  - matching on identical mapped field values, for example an order number, for records matched after it is switched on;
  - object-level create, update and delete rules in each direction, and a first-match conflict rule;
  - association sync with labels and a chosen direction;
  - "Always use HubSpot" and "Use HubSpot unless blank" field rules, which work only while the object-level rule is two-way;
  - selective sync filters for opportunities coming into HubSpot, and an inclusion segment for deals going to Salesforce.
- Merging deals in HubSpot does not merge opportunities. The merged deal keeps syncing with the opportunity whose Salesforce record ID was kept as the winning value during the merge, so choose it deliberately (KB).
- Like the company sync, **the updated deal sync cannot be switched back** and raises API use while it indexes (KB). Same pre-flight as above.
- Let Salesforce create opportunities; treat HubSpot deals as a read-only mirror for attribution and segmentation, with mappings set to "Always use Salesforce". On the updated sync, also set the object-level rules so HubSpot deals do not create Salesforce opportunities.

### Activities

- HubSpot engagements (form submissions, email interactions, meetings) can sync to Salesforce tasks. Choose only what reps use (form submissions and high-intent page visits, not every email open), or task lists fill with noise and API calls rise.
- An activity can sync with only one contact association (KB).

## 3. Field mapping and sync rules

Path: Data sync > [object] > Property mappings. Up to 500 mappings per object (KB).

### Sync rules (KB)

| Rule | Behaviour | Use for |
|---|---|---|
| Prefer Salesforce unless blank | HubSpot sends a value only when Salesforce is blank. A Salesforce value always overwrites HubSpot. Deleting in Salesforce deletes in HubSpot. | Fields sales owns that marketing may seed once (for example Lead Source). |
| Always use Salesforce | HubSpot never sends data. Salesforce always overwrites HubSpot, including deletions. | Account and opportunity data, territories, owner-maintained fields. |
| Two-way | The most recent value wins in either system, including deletions. | Shared fields both teams edit, and HubSpot-owned fields that are locked read-only in Salesforce. |
| Don't sync | Nothing passes either way. | Standard mappings you cannot delete but want to stop. Not available for "Unsubscribed from all email" (KB). |

Which extra rules exist depends on the object (KB):

- **Contacts**: only the 4 rules above (checked September 2026). To make a contact field HubSpot-owned, map it Two-way and make it read-only in Salesforce for all profiles except the integration user.
- **Companies**: the updated company sync adds "Always use HubSpot".
- **Deals**: the updated deal sync adds "Always use HubSpot" and "Use HubSpot unless blank".
- **Custom objects and tickets**: "Always use HubSpot" is offered.

The HubSpot-favouring rules on companies and deals work only while that object's object-level rule is two-way; with a one-way object rule, the one-way direction wins. HubSpot's planning guide lists all 5 rules together, so confirm the object and the sync version before promising a rule to a client.

### Compatible field types (KB)

| HubSpot | Salesforce |
|---|---|
| Dropdown select or radio select | picklist, reference |
| Multiple checkboxes | multipicklist |
| Single checkbox | boolean |
| Number | double or int |
| Single-line text | string, textarea |
| Multi-line text | textarea |
| Date picker | date, datetime |

### Mapping gotchas (KB)

- If a Lead field and a Contact field share an internal name, HubSpot writes to both. Use identical API names deliberately, and set up the Salesforce Lead conversion field mapping to match.
- A new mapping does not backfill. Resync, bulk resync or run a Salesforce import to populate existing records.
- When a record has no sync history for a newly mapped field, the first sync uses the Salesforce value as the baseline and can overwrite a newer HubSpot value. Test on a sample first.
- Salesforce reference (lookup) fields arrive as 18-character record IDs. Map them to a HubSpot dropdown and add labels to the options by hand; this needs maintenance whenever values are added.
- Properties of the "HubSpot user" type cannot be mapped.
- Never map Lead ID or Contact ID fields yourself; the integration manages them and custom mappings cause "Duplicate id specified" errors.
- Never map one HubSpot property to several Salesforce fields, or add a mapping that overlaps a standard one: values get overwritten or loop between the systems. HubSpot still flags a duplicate pair when one of the two is set to Don't sync, so delete the custom mapping rather than parking it there (KB).
- A bulk resync of company mappings handles at most 200,000 companies at a time; beyond that HubSpot reports that not all updates synced, so split larger sets (KB).
- Use the Refresh action on a picklist mapping after adding values in Salesforce.
- Export the mappings regularly (Export field mappings (CSV)) and keep the file with the data dictionary.

### Recommended mappings for this profile

| HubSpot property | Salesforce field (Lead and Contact, same API name) | Rule | Owner |
|---|---|---|---|
| Lifecycle stage | `HubSpot_Lifecycle_Stage__c` | Two-way, read-only in Salesforce | HubSpot |
| Lead status | `Lead.Status`; custom status field on Contact | Two-way | Sales |
| Original source, drill-down 1 and 2 | `HubSpot_Original_Source__c`, `..._Detail_1__c`, `..._Detail_2__c` | Two-way, read-only in Salesforce | HubSpot |
| Latest source | `HubSpot_Latest_Source__c` | Two-way, read-only in Salesforce | HubSpot |
| First and recent conversion (event name and date) | `First_Conversion__c`, `Recent_Conversion__c`, `Recent_Conversion_Date__c` | Two-way, read-only in Salesforce | HubSpot |
| Fit score, Engagement score, threshold properties | `HubSpot_Fit_Score__c`, `HubSpot_Engagement_Score__c`, `HubSpot_Score_Tier__c` | Two-way, read-only in Salesforce | HubSpot |
| Date entered MQL | `MQL_Date__c` | Two-way, read-only in Salesforce | HubSpot |
| Marketing lead source (normalised by workflow) | `LeadSource` | Prefer Salesforce unless blank | Seeded by HubSpot, then sales |
| Client segment, buying role, primary use case | Matching restricted picklists | Two-way | Shared, with identical values |
| Unsubscribed from all email | `HasOptedOutOfEmail` | Two-way; verify current default | Both, must always agree |
| Legal basis for processing | `GDPR_Lawful_Basis__c` | Two-way, read-only in Salesforce | HubSpot |
| Contact owner | `OwnerId` | Two-way only (KB) | Sales |

## 4. System-of-record matrix

| Data | Owner | Other system |
|---|---|---|
| Accounts, hierarchy, territory, account owner, client status | Salesforce | Read in HubSpot |
| Opportunities, stages, amounts, products, close dates | Salesforce | Read-only mirror as HubSpot deals |
| Contact identity (name, email, title) | Shared | Two-way |
| Record owner | Salesforce assignment, then shared | Two-way |
| Marketing engagement, web activity, form history | HubSpot | Summary fields in Salesforce |
| Subscriptions, opt-outs, lawful basis | HubSpot | Opt-out must reach Salesforce; Salesforce opt-outs must reach HubSpot |
| Scores and lifecycle stage up to MQL | HubSpot | Read-only in Salesforce |
| Lead status and disposition | Salesforce | Mirrored in HubSpot for nurture triggers |
| Campaign membership | Salesforce (people); HubSpot (assets) | Bridged |

## 5. Handoff flow end to end

1. Prospect submits a demo request on a HubSpot form associated with an active Salesforce campaign.
2. HubSpot creates or updates the contact and sets the lawful basis.
3. Hand-raiser workflow sets lifecycle MQL, lead status New, and the contact enters the inclusion segment.
4. The connector creates a Salesforce lead (or updates the existing lead or contact matched by email) and adds campaign membership.
5. Salesforce assignment rules assign the owner by territory, unless an active owner was set in HubSpot before the first sync (see section 6).
6. The representative works the lead; lead status changes sync back to HubSpot and drive nurture or recycle workflows.
7. On qualification the representative converts the lead to contact, account and opportunity. A Salesforce validation rule or flow should require at least one opportunity contact role before the opportunity moves past its first stage, because HubSpot's lifecycle update depends on contact roles.
8. HubSpot moves the contact to Opportunity, then Customer at closed-won.
9. A Salesforce flow stamps the primary contact's marketing source onto the opportunity at creation (`Marketing_Source__c`), so pipeline reporting does not depend on later edits to the contact.

## 6. Owners and assignment (KB)

- Salesforce Standard, PowerPartner, Guest and Queue users are recognised as owners.
- A HubSpot owner syncs to Salesforce only if they match an active Salesforce user's name and email exactly. Otherwise the Owner ID resets to the last Salesforce value.
- On a new lead: if the HubSpot contact already has a matching active owner before its first sync, that owner is kept; if not, Salesforce lead assignment rules apply.
- On an existing lead with an active owner, the existing owner is kept on first sync; later changes sync both ways.
- Salesforce requires an owner, so an unassigned record created from HubSpot is owned by the integration user. Build a report of records owned by the integration user and treat it as a queue to clear.

Recommendation: let Salesforce assign owners (territory rules, or a lead-to-account matching and routing tool), and keep HubSpot rotation for cases with no Salesforce routing.

## 7. Duplicates

- HubSpot de-duplicates contacts by email. Companies: the standard sync matches through associated contacts; the updated company sync can match on an identical mapped field such as domain. Deals: the standard sync does not de-duplicate; the updated deal sync can match on an identical mapped field. Matching in the updated syncs applies only to records matched after they are switched on, so clean existing duplicates first (KB).
- Merging companies or deals in HubSpot never merges the Salesforce records (KB). Merge in Salesforce as well.
- A Salesforce lead and a Salesforce contact with the same email cannot both sync to one HubSpot contact: one fails with "Email already in use". Decide which wins and merge or convert in Salesforce.
- Salesforce duplicate rules set to Block will reject integration writes ("Salesforce duplicate rule" error). Prefer Allow with alert for the integration user, or add a rule condition that excludes the integration user, and clean the duplicates through a scheduled process.
- Clean before you connect. Every duplicate present on day one multiplies through the sync.

## 8. Campaign bridging

HubSpot campaigns group assets; Salesforce campaigns group people with a member status. They do not natively sync (status of HubSpot's announced two-way sync must be checked). Options, in order of preference:

1. **Form association** (all supported tiers): associate each HubSpot form with an active Salesforce campaign. Submissions add the lead or contact as a member.
2. **Workflow action "Set Salesforce campaign"**: add contacts to a Salesforce campaign with a specific member status (for example Registered, Attended, No-show, Downloaded) based on any HubSpot behaviour. Only campaign IDs are stored on the HubSpot contact (property "Salesforce Campaigns"); member status does not come back.
3. **Custom object sync** (Enterprise): mirror Salesforce Campaign and Campaign Member into HubSpot custom objects for segmentation and reporting. Lookup fields cannot be mapped on custom objects; use associations instead (KB).
4. **Middleware**: when member status must sync both ways at volume.

Removing a contact from a Salesforce campaign does not trigger a sync (KB), so do not build automation that depends on removal.

## 9. Sync error catalogue (KB categories)

Path: Data sync > Sync Health > Sync errors. Errors can be exported to CSV and bulk-resynced 100 at a time. Turn on error notifications (Manage notifications: instantly, daily or weekly).

| Category | Typical errors | Usual root cause | Fix |
|---|---|---|---|
| Associations | Association limit reached; Waiting for account to sync; Association cardinality mismatch | Account not yet in HubSpot; too many associations; activity linked to several contacts | Import Salesforce accounts; reduce associations; one contact per activity |
| Custom code | Salesforce automation; Salesforce flow; Salesforce custom field validation rule | Salesforce flows or validation rules reject integration writes | Salesforce admin adds integration-user exceptions or fixes the logic |
| Duplicates | Email already in use; Salesforce duplicate rule | Lead and contact share an email; blocking duplicate rule | Merge or convert in Salesforce; change rule action for the integration user |
| Permissions | Insufficient access or missing Salesforce record; Salesforce field permission; Insufficient Salesforce access | Integration user lacks object or field-level access | Grant Read and Edit on the field or object |
| Picklists | Missing Salesforce picklist option; Mismatched options; Restricted picklist value; Inactive Salesforce owner; Salesforce owners not synced; Inactive opportunity stage; Missing or invalid opportunity stage; Default sales process unavailable; Option limit exceeded | Values or internal names differ between systems; restricted picklist; inactive owner or stage; missing record type | Align internal values; add values or unrestrict; reassign owners; map stages; fix record types |
| Property mappings | Type mismatch; Missing Salesforce ID; Invalid Salesforce ID | Incompatible field types; non-ID value sent to a lookup | Fix types; map lookups correctly; check validation rules |
| Property values | String too long; Invalid email; Missing required country; Invalid value; Owner assignment; Restricted unique value; Missing required value | Bad record data; Salesforce required fields or unique constraints; task assigned to a queue | Correct the record; relax or populate required fields; check matching rules |
| Other | Duplicate id specified | Custom mapping on Lead ID or Contact ID | Delete that mapping |

Required fields and validation rules on Lead are the most common hidden cause. Before go-live, list every required field and validation rule on Lead, Contact and Account, and either guarantee HubSpot sends a value or exempt the integration user.

## 10. "Record isn't syncing" runbook

Work through in order; stop at the first failure.

1. Is the contact in the inclusion segment? (Contact record > Salesforce sync card, or the segment itself.)
2. Has a sync been triggered? HubSpot checks for changes about every 15 minutes (KB). A contact already in Salesforce syncs when a mapped property changes; otherwise use Actions > Resync on the Salesforce sync card.
3. Is there a sync error for this record? Check the Salesforce sync card and Sync Health.
4. Is the API allocation used up? Check API call use in Sync Health.
5. Does the record break a Salesforce rule: required field, validation rule, duplicate rule, restricted picklist, country picklist?
6. Does the integration user have field-level access to every mapped field?
7. Is the owner active in Salesforce and matched by name and email?
8. Still failing: export the error, capture the record IDs in both systems, and escalate to HubSpot support with the timestamp.

### When everything stops at once

A sudden stop across many records ("nothing since Monday") is almost never a record problem. Check these first, in order:

1. Connection status on the Salesforce app page in HubSpot: is the integration toggled on and still authenticated?
2. The integration user in Salesforce: active, not frozen, password or session policy not expired, profile unchanged.
3. API allocation: used up by a bulk job or another integration?
4. Salesforce Setup Audit Trail for the days before the stop: a new required field, validation rule, duplicate rule, flow, restricted picklist or field-level security change is the usual culprit.
5. HubSpot side: was the inclusion segment's criteria edited, or the workflow that adds hand-raisers to it switched off? Check the segment and workflow history.
6. Treat it as P1 if hand-raisers or opt-outs are affected (see `operations-governance.md`), and tell sales which records to work manually until it is fixed.

## 11. Beyond the native connector

| Need | Use |
|---|---|
| Standard objects, field-level rules, moderate volume | Native connector |
| Logic triggered by marketing behaviour (campaign membership, alerts, data normalisation) | HubSpot workflows, including the Salesforce workflow actions |
| Logic that must run on Salesforce data (contact role enforcement, lead conversion defaults, stamping source on opportunities, account matching) | Salesforce Flow |
| Custom code, data quality automation, extra app syncs on HubSpot's side | Data Hub (Professional or Enterprise) |
| Two-way campaign member status, multiple orgs, complex custom objects with lookups, volumes beyond the API budget, audit and retry needs | Middleware (for example Workato, MuleSoft, Boomi) or reverse extract-transform-load from a data warehouse |

Choose the simplest layer that meets the need, and record the choice in the integration specification so the next admin knows where each rule lives.
