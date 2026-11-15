# Rebuilding Pardot logic in HubSpot

## Contents
1. Triage before rebuilding
2. Scoring and grading
3. Engagement Studio programmes
4. Automation rules, segmentation rules, completion actions, page actions
5. Dynamic content
6. Lifecycle stages and lead status
7. Lead assignment and routing
8. Testing automation before go-live

---

## 1. Triage before rebuilding

For every automation item in the inventory, record: purpose (one sentence), last time it acted on a record, volume in the last 90 days, owner, and decision — **rebuild**, **merge** (with another), **replace with native HubSpot behaviour**, or **retire**. Typical outcome in a mature Pardot account is that a large share of automation rules are retired or merged; do not assume a one-to-one rebuild. (Certain as practice)

HubSpot building blocks you will use (Depends: Marketing Hub Professional or Enterprise for workflows):
- **Workflows**: enrolment triggers (property changes, segment membership, form submission, page view, email events, Salesforce-synced values and others), re-enrolment settings, if/then and value branches, random split, delays (fixed time, until a date or day, until an event happens with a maximum wait), goals and unenrolment criteria, actions (send automated marketing email, set or copy property, add to static segment, create task, rotate record to owner, internal notification, set marketing contact status, enrol in another workflow, **Set Salesforce campaign**). (Certain for core features; Verify exact trigger list in the portal)
- **Segments** (formerly lists): active (dynamic) and static.
- **Lead scoring tool**: engagement, fit and combined scores with threshold properties.

## 2. Scoring and grading

**State of HubSpot scoring (October 2026):** the legacy "HubSpot score" property was retired on 31 August 2025 — new legacy score properties could not be created from May 2025, and workflows, lists and reports using legacy scores stopped updating. The replacement is the **Lead scoring tool** (Marketing → Lead scoring). (Certain) It offers **fit**, **engagement** and **combined** scores, score groups with limits, rules and criteria, **decay** and time frames on engagement, and a **threshold property** created alongside each score for bands. (Certain) Maximum points per score and which score types each tier gets have changed several times — HubSpot's product team stated scores can go up to 10,000 for fit and engagement and 20,000 for combined, and some sources say combined scores need Enterprise. (Verify: current limits per tier in the knowledge base)

**Pardot score → HubSpot engagement score**

1. Export the Pardot scoring rules (Settings → Scoring) and every automation rule, completion action and page action that adjusts score, including decay rules.
2. Build one engagement score with groups that mirror the activity types that actually predict conversion at the client (form submissions, high-intent page views such as pricing or demo pages, email clicks, webinar attendance). Drop email opens or weight them near zero — machine opens from privacy protections inflate them.
3. Replace Pardot's decay automation rules with the tool's decay or time-frame settings rather than workflows.
4. **Do not try to import Pardot scores into the new score.** Engagement scores are calculated from HubSpot activity, which starts at zero. Store the final Pardot score in a frozen legacy property and, for the first months, let qualification rules use "legacy score above X **or** new engagement score above Y". (Certain that history is not replayed into the new tool)

**Pardot grade and profiles → HubSpot fit score**

1. Translate each profile's criteria (industry, company size, job level, region) into fit rules. HubSpot fit rules are additive points, not thirds of a letter. (Certain)
2. If the client uses several profiles (personas), either build one fit score with persona-specific groups, or several fit scores — limited by tier. (Depends)
3. Use the threshold property to create bands (for example A/B/C) and, if sales insists on letters, a workflow that writes a letter to a custom "Fit grade" property synced to Salesforce. Tell sales the scale is new; do not label it as the old Pardot grade.
4. Company-level fit is possible because the tool scores companies too.

**Sync to Salesforce:** map the score and threshold properties to new Salesforce custom fields (sync rule pushing HubSpot's value). Retire `pi__score__c` and `pi__grade__c` after values are copied to legacy fields (`object-and-field-mapping.md` §5).

**Einstein Behavior Scoring** has no HubSpot equivalent at Professional; HubSpot's predictive features vary by tier. (Depends)

## 3. Engagement Studio programmes

**Design translation**

| Engagement Studio | HubSpot workflow |
|---|---|
| Recipient list(s) | Enrolment trigger (segment membership or the event that added people to the list) |
| Suppression list(s) | Unenrolment / suppression segments, plus goal criteria |
| Send email | Send automated marketing email (create the email as automated first) |
| Wait N days | Delay for a set amount of time |
| Trigger "email opened / link clicked / form completed within N days" | Delay *until an event happens* with a maximum wait, then branch on whether it happened — or a fixed delay followed by an if/then branch on the activity property |
| Rule (field, score, grade, list) | If/then branch on property, score threshold or segment membership |
| Add to Salesforce campaign | **Set Salesforce campaign** action with the member status |
| Adjust score | No action needed — the engagement score reacts to the activity itself |
| Notify user / assign | Internal notification; rotate record to owner or set owner |
| Send days and times (business hours) | Workflow execution schedule (days and time window) |
| Allow re-entry | Re-enrolment settings on the trigger |
| End | Workflow end, or goal reached |

Notes:
- Branching on opens is unreliable because of privacy-related automatic opens; branch on clicks or later actions. (Certain as deliverability practice)
- Very long programmes are easier to maintain as two or three linked workflows (stage workflows that enrol into the next), each with a clear goal.
- HubSpot emails in workflows must respect subscription types — every automated email needs the right subscription type, which is where the email-preference-centre mapping pays off.

**In-flight prospects at cutover (no export of current step exists)**

Pick one pattern per programme and record the decision:

1. **Drain** (preferred for programmes shorter than the overlap period): stop new entries into the Pardot programme on cutover day (remove the recipient list's feeding rule or add a suppression list), let existing prospects finish in Pardot, and send new entrants to the HubSpot workflow. Requires Pardot sending to continue until the last prospect finishes — check the contract overlap and the deliverability plan. (Certain as approach)
2. **Re-enter at the equivalent stage**: before cutover, derive each prospect's position from which programme emails they have received (Pardot email activity per prospect), stamp it into a HubSpot property ("Nurture stage at migration"), and design the HubSpot workflow to branch on that property at enrolment so people skip what they have had. More work; no gap or duplicate sends.
3. **Restart**: only for programmes where repeating early emails is harmless. Usually not acceptable.

Whatever the pattern, make sure nobody receives the same email from both systems: suppress HubSpot enrolment for prospects still active in Pardot (a static segment of their emails used as unenrolment criteria) until the drain finishes.

## 4. Automation rules, segmentation rules, completion actions, page actions

**Automation rules → workflows**

1. Recreate criteria as enrolment triggers or as an active segment used as the trigger.
2. **Retroactivity differs.** A Pardot rule acts on everyone who already matches. A HubSpot workflow acts going forward unless you choose to enrol existing records when switching it on. Decide per rule; for rules whose outcome already exists on the records (because Pardot ran it), do not re-run. (Certain)
3. **Repeating rules** (match every N days, max N times): use re-enrolment on a property or segment trigger, or schedule-based enrolment if the portal offers it. (Verify available re-enrolment and schedule triggers)
4. Rules that only maintain a list → usually become an active segment, no workflow at all.
5. Rules that adjust score → handled by the scoring tool's rules.

**Segmentation rules** → run once during migration as a one-off workflow or an import into a static segment; do not rebuild as ongoing automation.

**Completion actions** → workflows triggered by the specific asset interaction:

| Pardot completion action | HubSpot |
|---|---|
| Add to list / remove from list | Workflow: add to or remove from static segment (or an active segment defined by form submission) |
| Notify user / assigned user | Form notification settings, or workflow internal notification |
| Send autoresponder email | Workflow on form submission sending an automated email (prefer this over form follow-up emails) |
| Add to Salesforce campaign (with status) | Workflow **Set Salesforce campaign** with status; or associate the form with a Salesforce campaign, but status is then fixed at "Responded" and cannot be removed (Certain) |
| Assign to user / queue / via active assignment rule | See §7 |
| Change field value / add tag | Workflow set property |
| Adjust score | Scoring tool rule |
| Create Salesforce task | HubSpot task (synced if task sync is on) or let Salesforce create it with a flow |
| Register for webinar connector event | The webinar app's own form integration |

**Page actions** → workflow with a page-view enrolment trigger, or engagement-score rule on page views; HubSpot tracking code must be on those pages.

## 5. Dynamic content

- Pardot dynamic content keys on a single field (or grade). HubSpot **smart content** rules key on segment membership, lifecycle stage, country, device, referral source or language. (Certain; Depends: Professional or above)
- Workaround for field-based variations: one active segment per variation value, then smart rules on those segments. Keep segments named consistently ("SC – Industry – Financial services").
- In emails, coded templates can use HubL conditions on contact properties for more than a handful of variations. (Certain)
- Website dynamic content embedded with Pardot's JavaScript snippet stops working when Pardot is switched off — inventory every page that embeds it. HubSpot smart content works on HubSpot-hosted pages; on an external CMS you need the CMS's own personalisation. (Certain)

## 6. Lifecycle stages and lead status

- HubSpot **lifecycle stage** (contacts and companies) is the funnel position; **lead status** maps by default to the Salesforce lead **Status** field. Keep the picklist values identical. (Certain)
- Custom lifecycle stages can now be created and renamed (Super Admin permission needed). (Certain) Keep the default spine (subscriber, lead, marketing qualified lead, sales qualified lead, opportunity, customer) unless the client's funnel definitions genuinely differ, because many reports assume it.
- **Integration setting "automatic lifecycle stage transitions"**: moves HubSpot lifecycle stages forward from Salesforce events (lead converted, opportunity created, closed won). It never moves a stage backwards, and changing a HubSpot stage never converts a Salesforce lead. (Certain)
- Lifecycle stages do not move backwards by default in HubSpot; recycling a lead back to nurture needs the property cleared then set, inside a workflow. (Certain)
- Agree who sets marketing qualified lead (HubSpot, from scores) and who sets sales accepted / qualified (Salesforce, by sales), and make each a one-direction sync.
- Do not confuse HubSpot's separate **Leads object** (Sales Hub prospecting workspace) with Salesforce leads; Salesforce leads sync as HubSpot **contacts**. (Certain)

## 7. Lead assignment and routing

- **Owner on first sync to Salesforce** (Certain): if a HubSpot contact creates a new Salesforce lead and already has a HubSpot owner who matches an active Salesforce user by name and email, that owner is used; otherwise **Salesforce lead assignment rules apply**. If it links to an existing lead with an active owner, the existing owner stays. After the first sync, owner changes sync both ways. Records with no owner fall back to the integration user.
- Recommended for the client unless routing is simple: **let Salesforce assignment rules own routing** (they already encode territories and queues), and keep HubSpot contacts unowned until they reach Salesforce. This mirrors Pardot's "assign via active Salesforce assignment rule" completion action.
- If routing must happen in HubSpot (round-robin for inbound demo requests): workflow **rotate record to owner** among a team, before the record first syncs. (Depends: Professional or above)
- **Queues**: HubSpot owners are users; Salesforce queue ownership has no HubSpot owner equivalent. (Verify how queue-owned records appear in the client's portal before relying on owner-based segments)
- Pardot's own "assigned user" field becomes irrelevant; owner is the Salesforce owner.

## 8. Testing automation before go-live

1. Build in a HubSpot sandbox or test portal connected to a **Salesforce sandbox** if available. (Depends: HubSpot Enterprise for standard sandboxes; Verify integration support in sandboxes)
2. Keep production workflows **off** until cutover; review enrolment settings ("enrol existing records?") on each before switching on.
3. Named test contacts (own addresses with plus-addressing) covering: new lead, existing Salesforce contact, duplicate email, opted-out person, Do Not Email person, hard-bounced address, person mid-nurture.
4. For each workflow, check: enrolment, branch path, email sent with the right subscription type, Salesforce campaign membership and status written, owner and lifecycle as expected, no duplicate sends from Pardot.
