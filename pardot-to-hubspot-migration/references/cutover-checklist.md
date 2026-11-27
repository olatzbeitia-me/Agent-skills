# Cutover sequencing, parallel running and rollback

A phased checklist. Adapt durations to the client's volumes and contract dates; the order matters more than the timing. Each phase ends with a gate — do not start the next phase until the gate is met. Steps marked **Irreversible** or **Data loss** need explicit sign-off.

## Contents
1. Choosing a cutover pattern
2. Phase 0 – Discovery and contract
3. Phase 1 – Design
4. Phase 2 – Build and sandbox test
5. Phase 3 – Data preparation and initial load
6. Phase 4 – Parallel running
7. Phase 5 – Cutover week (hour-by-hour shape)
8. Phase 6 – Stabilisation
9. Phase 7 – Decommission
10. Rollback matrix

---

## 1. Choosing a cutover pattern

| Pattern | What it means | When to choose |
|---|---|---|
| **Single cutover with drain** (recommended default) | Forms, tracking, Salesforce sync and new email sends switch to HubSpot on one day; Pardot keeps only in-flight nurtures running until they finish | Most B2B migrations; limits the time two systems write to Salesforce |
| Phased by function | Website forms move first (writing to Salesforce through HubSpot), email later | When the web team and email team move at different speeds — but needs careful one-writer rules while both systems are live |
| Big bang | Everything stops in Pardot on one day, nurtures restart in HubSpot | Small databases and short nurtures only |

## 2. Phase 0 – Discovery and contract

- [ ] Answer the discovery questions (`discovery-questions.md`); record answers in the decision log.
- [ ] Confirm Pardot contract end date and negotiate **overlap** (recommended: at least 60–90 days after planned cutover, covering drain, the 30-day unsubscribe window and rollback). Confirm the post-termination terms with the Salesforce account team: Salesforce's published documentation gives 30 days after termination to request a data return, and deletes the data after 90 (`pardot-model.md` §15).
- [ ] Confirm HubSpot tiers and add-ons, and **data-hosting location** before the portal is created. **Irreversible** for EU hosting.
- [ ] Name owners: Salesforce admin, HubSpot admin, web, data protection, sales operations, an executive sponsor who can approve go/no-go.

Gate: contract dates and overlap agreed; hosting decided; owners named.

## 3. Phase 1 – Design

- [ ] Full Pardot inventory (`assets/pardot-inventory-template.csv`), with keep/merge/retire decisions.
- [ ] Field-mapping workbook (`assets/field-mapping-template.csv`) with owner and sync rule per field.
- [ ] Prospect/lead/contact survivorship rules agreed with sales operations.
- [ ] Subscription types, legal-basis approach and Do Not Email treatment signed off by data protection.
- [ ] Scoring and fit model, lifecycle definitions, assignment approach agreed with sales.
- [ ] Integration settings decided (`hubspot-salesforce-integration.md` §14).
- [ ] Campaign-membership conventions (`attribution-and-reporting.md` §5).
- [ ] Redirect map started; web touchpoint inventory complete.
- [ ] Choose cutover pattern and a provisional date avoiding quarter-end and major events.

Gate: designs signed off by owners.

## 4. Phase 2 – Build and sandbox test

- [ ] HubSpot properties, subscription types, segments, scoring, workflows (all **off**), email templates, forms, landing pages.
- [ ] Integration installed against the **Salesforce sandbox**; mappings configured; end-to-end tests with named test records (new lead, existing contact, duplicate email, opted out, Do Not Email, hard bounce, mid-nurture, lead conversion, owner assignment, campaign membership).
- [ ] Salesforce changes in sandbox: legacy fields for `pi__` values, flows updated to recognise the HubSpot integration user, duplicate rules, validation rule review, integration user and permission set.
- [ ] HubSpot Embed added to sandbox lead and contact layouts (`hubspot-salesforce-integration.md` §9); list the sales users who will need a HubSpot login to see it.
- [ ] In the sandbox, pause and resume the Pardot connector with test edits made in between, and record whether those edits sync on resume. The rollback matrix depends on the answer.
- [ ] Email sending domain authenticated in HubSpot (DNS can be added early; it does not affect Pardot). Check SPF lookup count.
- [ ] HubSpot tracking code added to the website alongside Pardot (with consent handling) to start building visitor history.
- [ ] Start Export API jobs for Pardot visitor-activity history (long-running).

Gate: all test cases pass in sandbox; sync errors understood; data protection sign-off on consent handling.

## 5. Phase 3 – Data preparation and initial load

- [ ] Deduplicate Salesforce leads and contacts by email per survivorship rules. **Irreversible:** export affected records first.
- [ ] Clean `[[unknown]]` placeholders and invalid emails.
- [ ] Build the suppression file; run the **opt-out import** into production HubSpot **first**. (Compliance)
- [ ] Connect production Salesforce; import Salesforce leads and contacts into HubSpot (establishes record links). Keep inclusion segment empty or restricted so HubSpot writes nothing to Salesforce yet.
- [ ] Update-import Pardot-only fields, legacy properties and Pardot-only prospects.
- [ ] Set subscription statuses and legal basis; set marketing-contact status by workflow.
- [ ] Rebuild static segments.
- [ ] Reconciliation checks (`data-migration-and-compliance.md` §9).

Gate: reconciliation explained to zero unexplained differences; every suppressed address confirmed unsubscribed.

## 6. Phase 4 – Parallel running

Pardot still runs production marketing; HubSpot is loaded, tracking, and warming up.

- [ ] Set Pardot's **Opted Out** sync behaviour so unsubscribes in either system reach the other through Salesforce Email Opt Out; test both directions. (`hubspot-salesforce-integration.md` §13)
- [ ] Begin HubSpot warm-up sends to the most engaged segment (`email-deliverability.md` §5) — only content not also being sent from Pardot.
- [ ] Replace low-risk website forms with HubSpot forms if the phased pattern was chosen; otherwise stage replacements ready to publish.
- [ ] Freeze new Pardot builds (no new assets except fixes) from a set date.
- [ ] Decide drain or re-entry for each Engagement Studio programme; prepare HubSpot suppression of people still in Pardot programmes.
- [ ] Dry-run the cutover runbook in sandbox, timing each step.

Gate: go/no-go meeting — warm-up metrics healthy, runbook rehearsed, rollback owners on call.

## 7. Phase 5 – Cutover week

Shape of the day (adapt times; pick a Tuesday or Wednesday, never a Friday):

1. **T-1 day**: lower DNS time-to-live on the tracker domain (if it moves this week); final Pardot exports (prospects, lists, recent activity); snapshot dashboards; schedule the final copy of `pi__` values into legacy fields for straight after step 3, when the values stop changing.
2. **Freeze**: stop new entries into Engagement Studio programmes that will drain (adjust recipient-list feeding rules); pause Pardot automation rules that write to Salesforce; schedule no Pardot list emails from now on; hide the Send to Pardot button on lead and contact layouts, because it still pushes single records into Pardot while the connector is paused.
3. **Pause the Pardot connector** (Pause Sync on the Connectors page). From this point prospect data, campaign members, opportunities and email tasks stop flowing between Pardot and Salesforce; campaigns, users and metadata keep syncing (`pardot-model.md` §12). Reversible while Pardot is licensed — use the Phase 2 sandbox test to know whether Salesforce changes made while paused will sync on resume.
4. **Final delta**: export Pardot opt-outs, Do Not Email and bounces since the initial load; run the opt-out import again. (Compliance)
5. **Turn on HubSpot write paths**: set the inclusion segment to its production definition; switch mappings to their production sync rules; turn on activity sync choices.
6. **Turn on HubSpot workflows** one group at a time, checking enrolment settings for each (enrol existing records only where intended).
7. **Website**: publish replacement forms and form-handler code; remove Pardot dynamic-content embeds; remove the Pardot tracking script.
8. **Repoint the tracker domain** to HubSpot with redirects already configured — or defer this until the 30-day unsubscribe window has passed (`web-tracking-and-domains.md` §6). When done: test top Pardot URLs, vanity URLs and unsubscribe paths.
9. **Smoke tests**: submit each key form as a test contact; confirm HubSpot contact, Salesforce lead, owner, campaign membership and status, lifecycle, notification, autoresponder, and that HubSpot Embed shows the test contact's timeline on the Salesforce record.
10. **Hypercare**: check Sync health and Salesforce duplicate reports every few hours for the first two days.

Point of no return (in practice): the first HubSpot marketing sends to the broad database plus new website submissions arriving only in HubSpot. After that, rollback means replaying HubSpot data into Pardot.

## 8. Phase 6 – Stabilisation (typically 4–8 weeks)

- [ ] Daily sync-error review; weekly reconciliation.
- [ ] Monitor deliverability metrics; widen sending audience gradually.
- [ ] Monitor 404s on the old tracker domain; add redirects.
- [ ] Let drain programmes finish in Pardot; then stop all Pardot sending.
- [ ] Repoint the tracker domain (if deferred) once 30 days have passed since the last Pardot send.
- [ ] Repoint Salesforce reports and dashboards from `pi__` fields to legacy fields; confirm with report owners.

Gate: no Pardot sends for 30+ days; no unexplained sync errors; reports repointed; sign-off from marketing and sales operations.

## 9. Phase 7 – Decommission

Order matters; each step depends on the previous.

1. [ ] Final Pardot exports confirmed complete and readable (open a sample of each file). **Data loss** if skipped.
2. [ ] Remove Pardot Lightning components, buttons, related lists and Visualforce elements from Salesforce layouts and apps.
3. [ ] Remove dependencies on `pi__` fields (reports, flows, formulas, validation rules) — "Where is this used?".
4. [ ] Deactivate the B2BMA Integration User; remove Account Engagement permission sets from users.
5. [ ] Uninstall the Pardot managed package. **Irreversible / Data loss** — deletes `pi__` fields and values.
6. [ ] Remove Pardot SPF include and DKIM records; remove gateway allow-listing.
7. [ ] Update cookie policy and privacy notice; remove Pardot from the record of processing activities and sub-processor list.
8. [ ] Close the Pardot contract; diary the 30-day deadline for requesting a data return and the 90-day deletion date, and confirm deletion with Salesforce afterwards.

## 10. Rollback matrix

| If the problem appears… | Rollback | Cost |
|---|---|---|
| Before connector pause | Abandon cutover for the day; nothing changed in Salesforce | None |
| After connector pause, before HubSpot write paths on | Resume the Pardot connector; check Marketing Data Sharing rules first if used; if the sandbox test showed paused-period changes do not sync on resume, bring the affected records back into line (Send to Pardot works for small numbers) | Low |
| After HubSpot write paths on, before broad HubSpot sends | Clear inclusion segment / set mappings to Don't sync; turn off workflows; resume Pardot connector; republish Pardot forms; point the tracker domain back if moved | Medium: reconcile records HubSpot created or changed in Salesforce (report on last-modified-by HubSpot integration user) |
| After broad HubSpot sends and new submissions in HubSpot | Fix forward in HubSpot; full rollback means exporting HubSpot unsubscribes, new contacts and activity into Pardot | High — avoid; design go/no-go to catch problems earlier |
| After package uninstall or Pardot deprovisioned | No rollback | — |

Unsubscribes are the one thing that must flow back in any rollback: export HubSpot unsubscribes and apply them in Pardot (and Salesforce Email Opt Out) before any Pardot send resumes. (Compliance)
