# Maintenance, governance and team support

Contents: 1 Operating cadence · 2 Change control · 3 Naming conventions · 4 Property and workflow governance · 5 Documentation set · 6 Access · 7 Enablement · 8 Support triage and escalation · 9 Platform audit checklist

## 1. Operating cadence

| Frequency | Task | Owner |
|---|---|---|
| Daily during hypercare, weekly after | Review Sync Health: error counts by category, clear and resync (100 at a time), note root causes | Marketing ops |
| Weekly | MQL aging list and disposition rate; records owned by the integration user; form spam check; bounce and complaint rates | Marketing ops with sales ops |
| Weekly | Change advisory: 30 minutes, HubSpot owner and Salesforce admin review upcoming changes | Both admins |
| Monthly | Duplicate review in both systems; picklist drift (refresh mappings after new Salesforce values); API usage trend; inactive owners; marketing contact count against tier | Marketing ops, Salesforce admin |
| Monthly | Opt-out round-trip test with a test contact | Marketing ops |
| Quarterly | Scoring calibration; funnel and lifecycle audit; workflow audit (unused, failing, overlapping); property audit; segment clean-up; user access review; contacts missing lawful basis | Marketing ops, data protection officer for consent |
| Annually | Full platform audit (section 9); tier and contract review; data retention purge under the agreed policy | Sponsor with both admins |

Turn on sync error notifications in HubSpot (Sync Health > Sync errors > Manage notifications) to a shared mailbox or channel, not one person.

## 2. Change control

- Any change to a field mapping, sync setting, inclusion segment, picklist used in a mapping, lifecycle logic, scoring threshold or routing needs a change request.
- Change request fields: what and why; systems and fields affected; who is affected; test evidence (sandbox or 20 to 50-record sample); rollback step; requester; approver; date.
- Approval: HubSpot owner and Salesforce admin jointly for anything touching the sync. Marketing leadership for scoring and lifecycle. Data protection officer for consent changes.
- Batch low-risk changes into a weekly release. Avoid Friday changes to anything that syncs.

## 3. Naming conventions

| Item | Pattern | Example |
|---|---|---|
| Campaigns (both systems) | `YYYY-Qn \| Region \| Type \| Name` | `2026-Q4 \| EMEA \| Webinar \| Supply-chain due diligence` |
| Workflows | `Object \| Purpose \| Trigger` | `Contact \| MQL routing \| Hand-raiser form` |
| Segments | `PURPOSE \| Audience \| Detail` | `SYNC \| Inclusion \| Salesforce` |
| Custom properties | Plain label; group by owner (Marketing, Sales, System, Integration) | Group: Integration; Label: HubSpot Fit Score |
| Salesforce fields written by HubSpot | `HubSpot_` prefix in API name | `HubSpot_Original_Source__c` |
| Emails | `Campaign name \| Asset \| Version` | `2026-Q4 \| EMEA \| Webinar \| Reminder 1 \| v2` |

## 4. Property and workflow governance

- Restrict who can create and edit properties (user permission for editing property settings) to operations.
- Every custom property has a description stating its purpose, owner system and sync rule.
- Every workflow has an owner, a description, and a review date; keep workflows in folders by function.
- Before deleting a property, check where it is used (HubSpot shows usage) and whether it is mapped to Salesforce.
- Archive rather than delete workflows for one quarter in case something depended on them.

## 5. Documentation set

Keep these in one shared location with an owner each:

1. Data dictionary: every property and field that matters, with internal name, label, type, values, owner system, sync rule, where used.
2. Integration specification: every connector setting plus the exported field mapping CSV, dated.
3. Lifecycle, lead status and service level agreement.
4. Scoring model with thresholds and last calibration date.
5. Runbooks: record not syncing, opt-out not applied, bulk resync, adding a picklist value, onboarding and offboarding users.
6. Decision log: what was decided, by whom, when, and why.

## 6. Access

- Least privilege. Two HubSpot super admins at most; Salesforce System Administrator limited to the admin team and the integration user.
- Single sign-on where available.
- Time-box partner and agency access, and review it quarterly.
- Offboarding checklist covers both systems and reassigns owned records before deactivation, because inactive owners cause sync errors.

## 7. Enablement

| Audience | What they need | Format |
|---|---|---|
| Marketers | Building compliant forms and emails, segments, campaign set-up checklist, reading their dashboard | Hands-on session plus checklists |
| Sales development and account executives | What an MQL is and why, disposition rules and reasons, reading HubSpot Embed in Salesforce, adding contact roles | 30-minute session plus one-page guide |
| Sales and marketing leaders | Dashboard definitions, what sourced and influenced mean | Short briefing and a glossary |
| New starters | Accounts in both systems, the right permissions, the one-page guide for their role | Onboarding checklist |

Run monthly office hours. Keep a short internal "how do I" library that grows from real support questions.

## 8. Support triage and escalation

Intake through one form or channel. Required details: record link in each system, what was expected, what happened, time, screenshot.

| Severity | Examples | Response |
|---|---|---|
| P1 | Opt-outs not syncing; email sent to unsubscribed contacts; forms not submitting; sync stopped entirely | Within 1 business hour; pause affected sends; fix or roll back the same day |
| P2 | A subset of records failing to sync; MQLs routed to the wrong owner or the integration user | Same business day |
| P3 | Report numbers disagree; a picklist value missing | Within 3 business days |
| P4 | Enhancement request | Into the change request backlog |

Escalation tiers: Tier 1 marketing operations (how-to and data fixes); Tier 2 HubSpot owner with Salesforce admin (configuration, sync, automation); Tier 3 HubSpot support, Salesforce support or the implementation partner, with exported errors and record IDs attached.

## 9. Platform audit checklist

1. Connector: integration user is dedicated, active, and has the required permissions; API allocation has headroom.
2. Inclusion segment criteria still match the agreed rules.
3. Sync errors: count, trend, and the top three root causes.
4. Field mappings: exported, compared with the specification, no orphaned mappings.
5. Picklists: values identical in both systems for every mapped picklist.
6. Duplicates: rate for contacts, leads versus contacts, accounts.
7. Records owned by the integration user or inactive users.
8. Lifecycle: contacts stuck in MQL for more than 30 days; customers with lifecycle below Customer.
9. Scoring: distribution, share of MQLs accepted, last calibration.
10. Workflows: errors, unused, overlapping triggers, no owner.
11. Properties: unused, duplicated, missing descriptions.
12. Segments: unused, broken criteria, inclusion and suppression intact.
13. Consent: contacts without lawful basis; opt-out round trip working; subscription types current.
14. Email deliverability: authentication (SPF, DKIM, DMARC), bounce and complaint rates.
15. Users: inactive users removed, super admins limited, partner access reviewed.
16. Reporting: official dashboards load, definitions documented, numbers reconcile with finance.
17. Marketing contacts: count against tier, non-marketing rules applied.
18. Documentation: current and dated.
