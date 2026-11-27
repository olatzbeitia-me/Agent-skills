# Pitfalls specific to Pardot-to-HubSpot migrations (Salesforce staying)

Each item: what goes wrong, why, and how to prevent it. Grouped by area. Skim the relevant group before advising on a build, data load or cutover step.

## Data and identity

1. **Duplicate-email prospects collapse.** Pardot holds one prospect per Salesforce record; HubSpot one contact per email. Data from several prospects merges into one contact, and the Salesforce link can flip between records. *Prevent:* deduplicate in Salesforce first; set survivorship rules; take the strictest mailability value across duplicates.
2. **Pardot-only prospects flood Salesforce.** Without an inclusion segment, every HubSpot contact syncs, so thousands of newsletter-only people become Salesforce leads on day one. *Prevent:* define the inclusion segment before the first HubSpot-to-Salesforce write.
3. **New Salesforce records ignore the inclusion segment.** If "create HubSpot contacts from new Salesforce leads/contacts" is on, they arrive in HubSpot regardless. *Prevent:* use selective sync to filter what comes in.
4. **`[[unknown]]` placeholders.** Pardot filled required Salesforce fields with `[[unknown]]`; HubSpot copies them into personalisation ("Dear [[unknown]]"). *Prevent:* clean in Salesforce; add default values to personalisation tokens.
5. **Marketing-contact bill shock.** Setting every synced or imported record as a marketing contact jumps the HubSpot tier. *Prevent:* default to non-marketing; promote by workflow on a defined segment.
6. **Picklist mismatches.** Lead Status, Industry, Country, State and custom picklists fail to sync when values differ, including Salesforce state and country picklists. *Prevent:* build HubSpot dropdowns from Salesforce's exact values; test with edge values.
7. **Reference fields arrive as IDs.** Mapping a lookup field gives an 18-character ID, not a name. *Prevent:* map a formula or text field that holds the label.
8. **Formula fields don't trigger syncs.** A value computed in Salesforce changes but HubSpot does not hear about it. *Prevent:* use a flow to stamp a real field, or accept the 15-minute polling and resyncs.
9. **Merging in Salesforce deletes HubSpot contacts** when "delete HubSpot contact when Salesforce record is deleted" is on. *Prevent:* keep that setting off during clean-up; merge into the record HubSpot is linked to.

## Compliance and suppression

10. **Opt-out sync only covers synced contacts.** People outside the inclusion segment never get Salesforce's Email Opt Out. *Prevent:* opt-out import into HubSpot before any contact load, and again at cutover.
11. **Do Not Email has no HubSpot field.** Imported Do Not Email records become mailable. *Prevent:* include them in the opt-out import or enforce an exclusion segment.
12. **Recycle-bin opt-outs forgotten.** Deleted Pardot prospects who unsubscribed are missing from exports of active prospects; if they return through Salesforce, HubSpot treats them as mailable. *Prevent:* include the recycle bin in the suppression file.
13. **Broken unsubscribe links in sent Pardot emails** once the tracker domain moves. *Prevent:* keep Pardot answering for 30 days after the last send, or redirect those paths to a working HubSpot unsubscribe.
14. **Clearing Email Opt Out in Salesforce does not resubscribe** in HubSpot — correct behaviour, but sales teams expect it to. *Prevent:* explain it; resubscription happens only by the person's own action.
15. **Erasure history not replayed.** People permanently deleted in Pardot for privacy reasons can come back from Salesforce. *Prevent:* reconcile erasure logs against Salesforce before first sync.

## Salesforce side

16. **Uninstalling the package deletes `pi__` fields and values**, and breaks every report, formula and flow using them. *Prevent:* copy to legacy fields; repoint dependencies; uninstall last.
17. **Engagement History goes blank.** Sales loses the Pardot activity view on records. *Prevent:* add HubSpot Embed to lead and contact layouts (accounts and opportunities too if they sync), give every salesperson who needs it a HubSpot login, and choose activity-to-task sync before cutover; tell sales that HubSpot Embed does not work in mobile apps.
18. **Flows that exclude the Pardot integration user** run on HubSpot changes and loop or overwrite. *Prevent:* search flows, Apex and validation rules for the B2BMA Integration User and add the HubSpot integration user.
19. **Validation rules and required fields reject HubSpot-created leads.** Pardot side-stepped some with placeholders. *Prevent:* sandbox test with minimal records; supply defaults or exempt the integration user.
20. **Integration user cannot see records** because of sharing rules, so they never sync. *Prevent:* view-all on synced objects for the integration user.
21. **Task volume explosion** from syncing email opens and sends as tasks, with no deduplication. *Prevent:* sync form submissions and clicks only.
22. **Two connectors writing the same fields** during parallel running. *Prevent:* one writer per field; HubSpot read-only until cutover; pause Pardot connector before HubSpot writes.
23. **A paused connector is not a frozen Pardot.** Campaigns, users and metadata keep syncing, and the Send to Pardot button still pushes single leads and contacts into Pardot, where its automation can still act on them. *Prevent:* hide Send to Pardot on layouts at the freeze; test resume behaviour in a sandbox before relying on it for rollback (`pardot-model.md` §12).
24. **Queue-owned leads** have no HubSpot owner equivalent; owner-based segments and notifications miss them. *Prevent:* test and design around queues.

## Automation

25. **Retroactivity mismatch.** Pardot automation rules act on everyone who matches; a HubSpot workflow switched on with "enrol existing" can re-send emails or re-stamp values on thousands of records. *Prevent:* decide enrolment of existing records per workflow; default no.
26. **Duplicate nurture emails** when Pardot programmes drain while HubSpot workflows start. *Prevent:* suppress HubSpot enrolment for people still in Pardot programmes.
27. **Building on the legacy HubSpot score.** It was retired in August 2025. *Prevent:* use the Lead scoring tool only.
28. **Open-based branching** rewards machine opens. *Prevent:* branch on clicks and form actions.
29. **Literal port of every rule.** Imports years of clutter. *Prevent:* triage first.

## Web and tracking

30. **Unknown Pardot embeds** on microsites, partner pages and PDFs break silently. *Prevent:* crawl and search off-site; monitor 404s after repointing.
31. **Collected forms miss hidden fields and JavaScript forms**, so UTMs and campaign values disappear. *Prevent:* Forms API or HubSpot forms.
32. **CAPTCHA-enabled HubSpot forms reject Forms API submissions.** *Prevent:* handle bot protection on the site side for API-posted forms.
33. **Repointing the tracker domain too early** kills live Pardot assets during drain. *Prevent:* move it only after drain and the 30-day unsubscribe window, or after everything on it is redirected.
34. **Cookie policy and consent platform not updated** for HubSpot cookies. *Prevent:* include in web change list; test consent behaviour.

## Reporting

35. **Original source shows "offline" for every migrated contact.** *Prevent:* legacy first-touch properties and a unified first-touch field.
36. **Account Engagement attribution models and analytics datasets stop.** *Prevent:* move to Salesforce's customizable campaign influence or HubSpot attribution; snapshot dashboards before cutover.
37. **Engagement metrics start from zero** in HubSpot. *Prevent:* set expectations; use legacy summary properties.

## Contract and platform

38. **Pardot data unrecoverable after termination.** Salesforce's published terms allow 30 days to request a data return and delete inactive data after 90, so planning around the 90 days misses the real deadline. *Prevent:* finish and check exports before the contract ends; diary the 30-day request deadline; confirm the contract's terms with the account team (`pardot-model.md` §15).
39. **No overlap negotiated**, removing rollback and drain options. *Prevent:* negotiate overlap in Phase 0.
40. **HubSpot hosted in the wrong region**; EU-hosted accounts cannot move out. *Prevent:* data protection sign-off before portal creation.
41. **Other tools post to Pardot** (webinar, events, chat, enrichment, custom API) and silently stop delivering leads. *Prevent:* inventory integrations and API users; repoint each to HubSpot or Salesforce.
42. **Sales-side Pardot features disappear** (Pardot emails sent by sales from Salesforce, engagement alerts). *Prevent:* identify users; provide HubSpot sales email or Salesforce alternatives.
