# Discovery questions, decision log and inventory guidance

Use this when client-specific facts are missing. Ask only the questions that change the answer in front of you; the full bank is for a structured discovery session.

## 1. Question bank (why each matters in brackets)

**Licences and contracts**
- Which Pardot edition, and how many business units? (Feature availability; one or several HubSpot designs)
- When does the Pardot contract end, and what notice period applies? Can we overlap 60–90 days? (Drain, rollback, unsubscribe window)
- Do the contract's post-termination terms match Salesforce's published ones: 30 days to request a data return, deletion after 90? (Export deadline)
- Which HubSpot hubs and tiers, and which add-ons (Brands, transactional email, dedicated IP, extra marketing contacts)? (What can be rebuilt natively)
- Has the HubSpot portal been created yet, and where is data hosted? (Irreversible hosting choice)
- Do we have HubSpot sandboxes and a Salesforce full or partial sandbox? (Test approach)

**Salesforce model**
- Which Salesforce edition? Is the org shared with other business units?
- Does marketing work with leads, contacts or both? How are leads converted, and by whom? (Create-as-leads versus contacts; reconciliation)
- Are person accounts enabled? (Extra testing)
- Which custom objects does Pardot read, or does segmentation rely on? (Custom object sync needs HubSpot Enterprise)
- Are state and country picklists enabled? (Sync errors)
- Which lead assignment rules, queues and routing tools are used? (Owner design)
- Which flows, Apex, validation rules and reports reference `pi__` fields or the B2BMA Integration User? (Dependency work)
- Are duplicate rules active for leads and contacts? (Clean-up and prevention)
- Who in sales reads Engagement History on records today, and does anyone rely on the Salesforce mobile app for it? (HubSpot Embed needs a HubSpot login per viewer and does not work in mobile apps)
- Is the Send to Pardot button on lead and contact layouts, and who uses it? (It still pushes records into Pardot while the connector is paused)

**Volumes**
- Pardot: total prospects, mailable prospects, prospects without a CRM ID, prospects in the recycle bin, emails shared by more than one prospect.
- Salesforce: leads, contacts, accounts, open opportunities; same-email duplicates by type.
- Monthly list-email volume and largest single send. (Warm-up plan)
- Visitor activities per year (rough). (Export API time)

**Assets and automation**
- Counts of forms, form handlers, landing pages, files, custom redirects, vanity URLs, email templates, dynamic content, automation rules, segmentation rules, Engagement Studio programmes (active, with prospects in them), scoring and grading rules, profiles.
- Which Engagement Studio programmes are business-critical, and how long is each? (Drain or re-entry)
- Which completion actions add people to Salesforce campaigns, with which statuses? (Attribution continuity)

**Web**
- Which CMS and tag manager? Which sites and subdomains carry Pardot tracking or forms?
- Which tracker domains exist, and which is primary? Is first-party tracking on?
- Which consent management platform, and is prior consent required for tracking cookies?
- Where do Pardot links live off-site (print, QR codes, partner sites, ads)?

**Email**
- Which From domains and reply-to addresses? Any subdomains used for marketing?
- Shared or dedicated IP in Pardot? Current bounce and complaint rates?
- Are operational emails sent from Pardot? Which?
- Do sales users send Pardot emails from Salesforce?

**Integrations**
- Webinar and event connectors (Zoom, GoTo Webinar, Webex, Cvent, ON24 and so on)?
- Other systems writing to Pardot or reading from it: chat, enrichment, intent data, Zapier, data warehouse, custom API users?

**Compliance**
- Which jurisdictions and data protection regimes apply, and who is the data protection lead?
- Consent model per region: explicit opt-in, soft opt-in for customers, legitimate interest? Double opt-in used?
- How are erasure requests handled today across Pardot and Salesforce?
- Retention policy for marketing data and for migration exports?

**Reporting**
- Which campaign influence model is official? Account Engagement multi-touch models, Salesforce customizable influence, or neither?
- Which dashboards does leadership look at monthly, and which Pardot fields feed them?
- Is B2B Marketing Analytics (CRM Analytics) licensed and used?

## 2. Decision log format

Keep one row per decision so the reasoning survives staff changes:

| ID | Date | Decision | Options considered | Reason | Owner | Reversible? | Status |
|---|---|---|---|---|---|---|---|
| D-001 | | HubSpot creates Salesforce leads, not contacts | Leads / contacts | Avoids private contacts; sales converts leads | Sales ops | Yes, setting | Agreed |

## 3. Inventory guidance

`assets/pardot-inventory-template.csv` has one row per Pardot asset or rule. Suggested extraction per type:

| Asset type | Source |
|---|---|
| Forms, form handlers, landing pages, files, custom redirects, emails and templates, lists, campaigns, tracker domains, users | Pardot API version 5 query endpoints, or table exports in the UI |
| Automation rules, segmentation rules, dynamic content, completion actions, page actions | UI review with screenshots (API coverage varies — Verify) |
| Engagement Studio programmes | UI: programme canvas screenshots and the programme's report; record active prospects per step |
| Scoring rules and grading profiles | UI: Settings → Scoring; Grading profiles; screenshots |
| Field list and sync behaviour | UI: prospect field configuration |
| Salesforce dependencies | "Where is this used?" on `pi__` fields; report and flow metadata search |
| Web touchpoints | Site crawl with source-code search; off-site link search |

`assets/field-mapping-template.csv` has one row per field across Pardot, Salesforce and HubSpot with the owner and sync rule.
