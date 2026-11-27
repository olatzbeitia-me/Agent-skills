# 2026-11-27: pardot-to-hubspot-migration

**Date:** 27 November 2026
**Agent:** [pardot-to-hubspot-migration](../pardot-to-hubspot-migration/)
**Why this agent:** 1 `improve/` pull request was open (paid-media-strategist), so that agent counts as reviewed today. Of the 2 agents never reviewed, this one comes first alphabetically.

## What changed

1. **The description now fits Anthropic's limit (clearer description).** At 1,035 characters it was above the documented maximum of 1,024. It is now 903 characters and says in the third person what the skill does and when to use it. Every trigger term is kept, and "decommissioning" is added. The phrase "for example a B2B data-as-a-service company" is gone; it did not help Claude decide when to use the skill.
2. **Switching Pardot off now rests on Salesforce's own documents (outdated or unconfirmed platform facts).**
   - *Pausing the connector.* The skill said pausing "stops sync in both directions". Salesforce Help says otherwise: campaigns, users and metadata keep syncing while paused, and the Send to Pardot button still pushes single leads and contacts into Pardot. The Pardot model reference now lists what stops and what continues. The cutover freeze now hides Send to Pardot, and Phase 2 adds a sandbox test of whether changes made while paused sync on resume, because the help page does not say. The rollback matrix uses that test result. A new pitfall (23) covers this, and the remaining pitfalls are renumbered.
   - *After the contract ends.* The skill said data was "reported to be" deleted about 90 days after deactivation. Salesforce's Account Engagement security, privacy and architecture document (published 22 May 2026) gives the actual terms. A customer can ask for its data back only within 30 days of termination. After that, the data is kept inactive for 90 days and then deleted, and backups are kept for 90 days. So the real deadline is 30 days, not 90. Principle 7 in `SKILL.md`, the Pardot model, the cutover checklist (Phase 0 and Phase 7), the pitfalls and the discovery questions now say this.
3. **HubSpot Embed replaces the vague "integration card" (outdated name and a new guardrail).** The skill told users to put a "HubSpot integration card" on Salesforce layouts to replace Pardot's Engagement History, and to verify how to install it. HubSpot's knowledge base calls this HubSpot Embed, and HubSpot is deprecating the legacy Visualforce package. The integration reference now gives the install path and 2 limits that change a migration plan. First, each Salesforce user needs their own HubSpot login, with permission to view the record, to see the window. Second, it does not work in mobile apps. The mapping gap table, pitfall 17, the recommended configuration table, the Phase 2 checklist, the smoke tests, the discovery questions and the list of renames in `SKILL.md` are updated to match.

`SKILL.md` stays at 98 lines. There are no scripts or tests in this agent.

## Why

- Anthropic's skill authoring guide sets a 1,024-character maximum for the description. It also says the description should be in the third person and state both what the skill does and when to use it.
- Salesforce Help's page on pausing the connector (version 2) lists the objects that stop syncing and the 3 that carry on. It says Send to Pardot still syncs a single record, and it asks admins using Marketing Data Sharing to check sharing rules before resuming. A cutover plan that treats a pause as a full freeze could let records slip into Pardot during the drain.
- Salesforce's Account Engagement security, privacy and architecture document is the published version of the post-termination terms. The skill's "around 90 days" figure was second-hand. More importantly, it missed the 30-day window for asking for data back, which is the deadline a migration team can actually miss.
- HubSpot's article on adding HubSpot Embed to Salesforce page layouts gives its name, what it shows, how to install it, its permission requirements and the mobile limit. HubSpot's implementation planning guide (updated 16 October 2026) uses the same name. The sister agent `hubspot-salesforce-architect` already uses it, so the 2 agents now agree.

## Considered and rejected

- **Campaign and campaign-member sync.** This is the fastest-moving fact in the agent, so it was checked first. HubSpot's Campaigns FAQ (updated 3 August 2026) still says HubSpot campaigns cannot sync to Salesforce. The planning guide says Salesforce campaigns have no direct equivalent in HubSpot. A HubSpot product manager wrote in a community thread in May 2026 that 2-way sync was in development, but that thread is a forum and no beta appears in the knowledge base. The skill's guidance and its "Verify status" flag stand.
- **HubSpot-led sync rules for contact mappings.** HubSpot's mapping article (updated 16 September 2026) lists 4 sync rules for mappings. The planning guide lists 5, adding "Always use HubSpot" and "Use HubSpot unless blank", without saying which objects offer them. Because the 2 sources conflict, the skill keeps its "Verify" label.
- **A note on the first sync after a new mapping.** The mapping article says that when a mapping is created after a contact last synced, the first sync takes Salesforce's value as the baseline and can overwrite a newer HubSpot value. This matters when Pardot data is loaded into HubSpot before mappings are finished. It was left for a future review to keep this run to 3 changes.
- **Timeline sync versus activity sync.** The planning guide separates the 1-way timeline sync from a 2-way activity sync that deduplicates. The skill's warning about duplicate tasks applies to timeline sync. Explaining activity sync properly needs its own article, so this was left for a future review.
- **Naming a HubSpot seat type for HubSpot Embed viewers.** None of the sources read says which seat a viewer needs, only that they need a HubSpot user with permission to view records. The skill asks the reader to confirm this with the HubSpot account team rather than guess.

## Noticed outside this agent

- Nothing new. `hubspot-salesforce-architect` already describes HubSpot Embed correctly.

## Sources

- Anthropic, *Skill authoring best practices*: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- Salesforce Help, *Pause the Salesforce Connector v2* (read 27 November 2026): https://help.salesforce.com/s/articleView?id=sf.pardot_sf_connector_v2_pause_connector.htm&language=en_US&type=5
- Salesforce, *Marketing Cloud Account Engagement (formerly Pardot) Security, Privacy and Architecture* (published 22 May 2026): https://www.salesforce.com/en-us/wp-content/uploads/sites/4/documents/legal/misc/marketing-cloud-account-engagement-security-privacy-and-architecture.pdf
- HubSpot Knowledge Base, *Add the HubSpot Embed window to your Salesforce page layouts*: https://knowledge.hubspot.com/salesforce/add-the-hubspot-visualforce-window-to-your-salesforce-page-layouts
- HubSpot Knowledge Base, *Plan your HubSpot - Salesforce implementation* (updated 16 October 2026): https://knowledge.hubspot.com/integrations/plan-your-hubspot-salesforce-implementation
- HubSpot Knowledge Base, *Campaigns: frequently asked questions* (updated 3 August 2026; confirms no change needed): https://knowledge.hubspot.com/campaigns/campaigns-faq
- HubSpot Knowledge Base, *Map HubSpot properties to Salesforce fields* (updated 16 September 2026; checked, no change made): https://knowledge.hubspot.com/salesforce/map-hubspot-properties-to-salesforce-fields
