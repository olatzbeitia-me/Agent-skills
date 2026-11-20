# Migration playbook, A to Z

Contents: Scenarios · Phases 0 to 9 · Load order · One-time transfer or ongoing sync · Testing and user acceptance scenarios · Cutover and rollback · Account Engagement (Pardot) to HubSpot mapping · Indicative timeline · Risks · RACI

## Scenarios

Identify which one applies; the plan changes.

| Scenario | Typical for | Biggest risk |
|---|---|---|
| A. Add HubSpot alongside Salesforce | Sales stays in Salesforce, marketing adopts HubSpot | Sync design and duplicates |
| B. Move marketing automation from Account Engagement (Pardot) to HubSpot, Salesforce stays | A B2B data-as-a-service business, given its stack signal | Losing opt-outs, attribution history and deliverability |
| C. Consolidate the customer relationship management system (Salesforce to HubSpot, or the reverse) | Smaller teams simplifying, or scaling teams moving to Salesforce | Opportunity history, reporting continuity, user adoption; duplicates if a one-time transfer and the connector both touch the same data |

## Phases

Every phase has an owner and exit criteria. Do not start a phase until the previous one's exit criteria are met; this is where most migrations save or lose their timeline.

### Phase 0: Mobilise
- Executive sponsor, steering group, decision log, RACI (below), scope statement, success measures.
- Exit: sponsor signs scope and success measures (for example: no opt-out lost; MQL to opportunity conversion reportable end to end; sync error rate under 1 percent of synced records).

### Phase 1: Discovery and audit
- Inventory of every system touching the funnel: Salesforce, Account Engagement, webinar platform, event tools, enrichment, intent data, website forms, chat, data warehouse.
- Salesforce audit: objects in use, fields with fill rates, required fields, validation rules, duplicate and matching rules, flows (Workflow Rules and Process Builder reached end of support at the end of 2025, so treat any still running as migration items), assignment rules, record types, page layouts, reports and dashboards actually opened in the last 90 days.
- Account Engagement audit: automation rules, completion actions, segmentation rules, Engagement Studio programmes, forms and form handlers, landing pages, custom redirects, scoring and grading models, email templates, preference centre, tracker domain, connector settings, business units.
- Data quality profile: duplicate rates by object, invalid emails, missing country, picklist value sprawl, records owned by inactive users.
- Stakeholder interviews: marketing, sales development, account executives, sales leadership, finance (revenue reporting), data protection officer, web team.
- Exit: current-state document and a list of what will not be migrated.

### Phase 2: Design
Design reports first, then the data model that feeds them. A field nobody reports on or automates from does not need to migrate.

- System-of-record matrix (see `integration-sync.md` section 4).
- Data model: objects, properties, picklists with internal values agreed across both systems.
- Lifecycle, lead status and service level agreement (see `hubspot-inbound.md`).
- Scoring model, routing design, consent model and lawful basis per source.
- Naming conventions, folder structure, user roles and permissions.
- Integration specification: every connector setting and every field mapping with its rule and owner.
- Exit: design signed by marketing, sales operations, the Salesforce admin and the data protection officer.

### Phase 3: Data preparation
Recommendation: clean before migrating, not after. Duplicates and bad values multiply through the sync on day one, and fixing them once in the source is cheaper than fixing them in two connected systems.

- De-duplicate leads against contacts and accounts against accounts in Salesforce; resolve leads and contacts sharing an email.
- Normalise countries and states to the Salesforce picklist values.
- Collapse picklist sprawl to the agreed values.
- Validate emails; flag hard bounces.
- Archive rather than migrate: no engagement for 24 months, no open opportunity, not a client, and no lawful basis to keep marketing to them. Agree the rule with the data protection officer.
- Take a full backup of Salesforce and Account Engagement before anything is changed.
- Exit: data quality targets met on a re-run of the Phase 1 profile.

### Phase 4: Build
- HubSpot: properties, subscription types, forms, templates, segments, scoring, workflows, campaigns, reports.
- Salesforce: custom fields with field-level security, Lead conversion mapping, contact role enforcement, source stamping flow on opportunity, duplicate rule changes, integration user.
- Integration configured in a Salesforce sandbox (and a HubSpot sandbox on Enterprise).
- Decide in the sandbox, before production, whether to switch on HubSpot's updated company and deal syncs. Neither can be switched back, and both change how records match (see `integration-sync.md` section 2).
- Exit: every item in the integration specification built and peer-reviewed.

### Phase 5: Migrate and test
See load order and test scenarios below. Exit: user acceptance signed, reconciliation within tolerance.

### Phase 6: Cutover
See cutover and rollback below. Exit: go or no-go decision recorded.

### Phase 7: Go-live and hypercare (two to four weeks)
- Daily: Sync Health review, error triage, form submission spot checks, opt-out round-trip test.
- Watch: MQL volume against the pre-migration baseline, speed-to-lead, sync error count, bounce rate, spam complaint rate (Gmail and Yahoo require bulk senders to stay under 0.3 percent; aim for under 0.1 percent).
- Daily 15-minute stand-up with marketing operations, the Salesforce admin and a sales representative.
- Exit: two consecutive weeks within thresholds.

### Phase 8: Training and adoption
- Role-based sessions: marketers (forms, emails, segments, campaigns), sales development and account executives (what an MQL is, disposition rules, HubSpot Embed in Salesforce, contact roles), leaders (dashboards), operations (runbooks).
- Quick-reference guides of one page per role.
- Adoption measures: MQL disposition within the agreed time, contact roles present on opportunities, records owned by the integration user trending to zero.

### Phase 9: Decommission and document
- Switch off Account Engagement automations and the connector; keep the account read-only for an agreed period, then export prospect activity history and email statistics to the data warehouse or archive files.
- Remove obsolete `pi__` fields from page layouts (keep the data).
- Final documentation: data dictionary, integration specification with exported field mappings, lifecycle and service level agreement, runbooks, decision log.

## Load order

1. Users and owners (matching name and email in both systems)
2. Opt-outs and suppression, before anything that can send email
3. Companies and accounts
4. Contacts with lawful basis and subscription status
5. Opportunities and deals (with pipelines and stages mapped)
6. Associations (contact to company, contact to deal, contact roles)
7. Campaigns and memberships
8. Historical engagement where it can be carried (see the Account Engagement table)
9. Assets: templates, emails, landing pages, files, redirects

Use the connector's Salesforce import to bring existing Salesforce leads and contacts into HubSpot rather than a CSV round trip, so record IDs link from the start. Run large loads out of business hours and watch the API allocation.

## One-time transfer or ongoing sync

HubSpot offers 2 routes for Salesforce data, and they must never overlap (HubSpot Knowledge Base, November 2026).

| Route | Use when | Watch for |
|---|---|---|
| Salesforce connector | Salesforce stays (scenarios A and B) | Initial load through the connector's Salesforce import, as above |
| HubSpot Smart Transfer | Salesforce is being retired (scenario C, Salesforce to HubSpot) | Super Admins only. Carrying custom field mappings needs a Data Hub subscription. It creates workflows to bridge data-model differences and switches them on automatically, so review them before go-live. Turn off its automatic sync when filters or a mapping check are needed first, or unwanted records come across, which breaks the archive rule in Phase 3. Its sync keeps running in the background after the first pass. It can revert a transfer, so name that step in the rollback plan. Data moved in its optional one-time transfers does not stay up to date. |

The 2 routes identify records differently, so running both on the same Salesforce data creates duplicates in HubSpot and in Salesforce. If Smart Transfer has been used, switch off all its sync connections before turning the connector on.

Smart Transfer also lists Account Engagement (Pardot) as a source. In scenario B the connector stays live, and HubSpot's duplicate warning is written about Salesforce data only, so confirm with HubSpot how a Smart Transfer from Account Engagement matches records before relying on it there.

## Testing and user acceptance scenarios

Test types: unit (each mapping in both directions), end to end (scripts below), user acceptance with real users, reconciliation (record counts per object and a 50-record field-level spot check), load (API usage at expected peak).

End-to-end scripts for a B2B data-as-a-service business:

1. A bank analyst downloads a gated report: contact created, scored, not sent to Salesforce.
2. The same analyst requests a demo: becomes MQL, syncs as a lead, assigned by territory, joins the Salesforce campaign.
3. A contact at an existing client account requests a demo: matched to the existing contact, not a new lead; expansion route followed.
4. Webinar: registrant who attends and one who does not get the right member status and follow-up.
5. Unsubscribe in HubSpot: Email Opt Out set in Salesforce within one sync cycle. Then the reverse. Then clear Email Opt Out in Salesforce and confirm the contact stays unsubscribed in HubSpot, which is the documented behaviour.
6. Representative rejects an MQL with a reason: recycle nurture starts in HubSpot.
7. Representative converts a lead with a contact role on the opportunity: lifecycle moves to Opportunity; closed-won moves to Customer.
8. Lead and contact share an email: the agreed resolution works and is documented.
9. Contact in a market treated as double opt-in: not mailed until confirmed.
10. Partner referral: correct source stamped and visible on the opportunity.

## Cutover and rollback

Cutover sequence (for scenario B):

1. Announce the freeze: no new Account Engagement assets or field changes from the agreed date.
2. Final delta export from Account Engagement; import opt-outs first, then remaining changes.
3. Authenticate the HubSpot sending domain (SPF, DKIM, DMARC) at least two weeks before the first send; warm up volume gradually, starting with the most engaged segments.
4. Pause Account Engagement automations, then pause its Salesforce connector at the cutover time, so two systems never write the same Salesforce fields.
5. Swap website tracking code and form embeds; set 301 redirects from Account Engagement landing page URLs.
6. Turn on HubSpot workflows in the agreed order: suppression, hygiene, routing, nurture.
7. Run end-to-end scripts 1, 2 and 5 in production with test contacts.

Rollback triggers, agreed in advance: opt-outs not syncing; more than an agreed share of new records erroring; forms failing; routing sending MQLs to the integration user.

Rollback steps: turn the HubSpot integration off (one toggle), restore the previous form embeds, resume the Account Engagement connector and automations (keep them paused, not deleted, for at least 30 days), restore affected Salesforce fields from the pre-cutover backup.

## Account Engagement (Pardot) to HubSpot mapping

| Account Engagement | HubSpot | Notes |
|---|---|---|
| Prospect | Contact | HubSpot allows one contact per email. Resolve any multiple-prospects-per-email cases first. |
| Default and custom prospect fields | Contact properties | Map only fields used in reports or automation. |
| Score | Engagement score in Lead Scoring | Rebuild; do not copy point values blindly. |
| Grade (profile A to F) | Fit score in Lead Scoring | Combined thresholds can replace the score-and-grade matrix. |
| `pi__score__c`, `pi__grade__c` and other `pi__` fields on Salesforce records | Keep in Salesforce as history | Optionally copy final values into read-only HubSpot properties for before-and-after comparison. |
| Automation rules, completion actions, segmentation rules | Workflows | Consolidate; many rules collapse into a few workflows. |
| Engagement Studio programmes | Workflows with branching | Rebuild around current content; retire programmes nobody can explain. |
| Static and dynamic lists | Static and active segments | Rebuild active segments from criteria, not from exports. |
| Forms and form handlers | HubSpot forms, or non-HubSpot form capture for existing site forms | Map hidden fields and campaign association. |
| Landing pages on the tracker domain | HubSpot landing pages on a HubSpot-connected subdomain | 301 redirects from every live URL. |
| Email templates | HubSpot templates | Rebuild in the drag-and-drop editor; test rendering. |
| Custom redirects | Tracking URLs with UTM parameters | |
| Connected campaigns | HubSpot campaigns plus Salesforce campaign bridging | See `integration-sync.md` section 8. |
| Opted Out, Do Not Email | "Unsubscribed from all email" and subscription types | Import first, before any send. |
| Email preference centre | Subscription preferences page | Map old topic lists to new subscription types. |
| Prospect activity history | No direct import as HubSpot activity | Archive; carry key dates (last activity, first conversion) as properties; Enterprise custom events if history must be queryable. |
| B2B Marketing Analytics | HubSpot reports plus Salesforce campaign influence | Define a reporting epoch: compare like with like across the cutover. |
| Business units | HubSpot business units or brands | Check current tier and add-on requirements. |

## Indicative timeline (scenario B)

Assumptions: one Salesforce org, one HubSpot account, 50,000 to 150,000 contacts, one marketing operations lead and one Salesforce admin with partner support.

| Weeks | Phase |
|---|---|
| 1 to 2 | Mobilise and discovery |
| 3 to 4 | Design and sign-off |
| 4 to 7 | Data preparation (overlaps build) |
| 5 to 9 | Build in sandbox; domain authentication started |
| 9 to 11 | Migrate, test, user acceptance |
| 12 | Cutover |
| 12 to 15 | Hypercare and training |
| 16 | Decommission and documentation |

## Risks

| Risk | Impact | Mitigation |
|---|---|---|
| Opt-outs lost or late | Regulatory and reputational | Import suppression first; round-trip test before first send; block sends until verified |
| Duplicate explosion at first sync | Rep confusion, broken routing | Clean in Phase 3; inclusion segment; sample sync of 50 records first |
| Hidden Salesforce automation fires on integration writes | Corrupted fields, errors | Audit flows and validation rules; exempt or adapt for the integration user |
| API allocation exhausted during backfill | Sync stalls, including opt-outs | Load out of hours; raise allocation temporarily; monitor |
| Attribution history break | Leadership loses trend lines | Keep first-touch fields from the old system; define a reporting epoch |
| Deliverability dip | Lower email performance | Authenticate the domain early; warm up; send to engaged segments first |
| Sales does not adopt MQL process | Pipeline leakage | Signed service level agreement; weekly disposition report; leadership sponsor |
| Scope creep | Delay | Change requests through the steering group only |

## RACI

R = responsible, A = accountable, C = consulted, I = informed.

| Workstream | Sponsor | Marketing ops | Salesforce admin | Sales ops | Sales leaders | Data protection officer | Web or IT | Partner |
|---|---|---|---|---|---|---|---|---|
| Scope and success measures | A | R | C | C | C | I | I | C |
| System-of-record decisions | A | R | R | C | C | C | I | C |
| Data model and mappings | I | A/R | R | C | I | I | I | C |
| Consent model | I | R | C | I | I | A | I | C |
| Data cleansing | I | R | A/R | R | I | C | I | C |
| Integration build | I | A/R | R | C | I | I | I | R |
| Tracking, domains, redirects | I | C | I | I | I | I | A/R | C |
| User acceptance | I | A | R | R | R | I | I | C |
| Go or no-go | A | R | R | C | C | C | C | C |
| Training | I | A/R | R | R | C | I | I | C |
| Hypercare | I | A/R | R | C | I | I | C | R |
