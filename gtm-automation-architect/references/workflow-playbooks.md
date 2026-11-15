# Workflow playbooks

Starting points, not templates to hand over unchanged. Adapt each one to the company's stack, volumes, motion and goal. Each playbook gives: the goal and metric, the trigger, the flow, a lean and a scale tool option, human checkpoints, cost levers and common failure points.

Notation: **[A]** automated step, **[AI]** language-model step, **[H]** human checkpoint.

## Contents
- Events: E1 pre-event invitations · E2 event-day alerts · E3 24-hour follow-up · E4 event return report
- Partner communications: P1 overlap to pipeline · P2 partner update · P3 ecosystem alerts and deal registration · P4 joint campaigns
- Product marketing: M1 launch kit and distribution · M2 competitive digest · M3 win–loss and voice of customer · M4 customer story pipeline
- Outbound and inbound: O1 signal-led outbound · O2 champion moves · I1 inbound enrichment and routing
- Choosing what to build first

---

## Events

Events generate the most manual drag of any programme: list building before, spreadsheets during, slow follow-up after. The prize is speed: follow-up in hours, not days, and clean attribution.

### E1 — Pre-event: target-account invitations

- **Goal and metric:** registrations from target accounts; meetings pre-booked.
- **Trigger:** event created in the events platform, or campaign created in the CRM.
- **Flow:**
  1. [A] Pull target accounts from the CRM: ideal-customer tier, region, open opportunities, partner overlaps, previous event attendance.
  2. [A] Exclude accounts with active deals in late stages where sales owns contact; flag them for rep-led invites instead.
  3. [A] Check which accounts already have the right contacts in the CRM. Enrich only the gaps (Clay waterfall, emails only).
  4. [AI] Write one line on why this event or session matters to this account (from industry, recent news, product usage).
  5. [H] Account owners approve the personal invitation list for top-tier accounts; the rest go to a marketing email.
  6. [A] Registrations sync back to the CRM campaign; a daily Slack digest tells each owner which of their accounts registered.
- **Lean option:** HubSpot or Salesforce campaign, Clay Launch, native email, Slack.
- **Scale option:** Swoogo, Clay Growth or Cargo with CRM sync, Outreach sequences for rep invites.
- **Cost levers:** enrich only missing contacts; no phone enrichment for invitations; AI line only for top tiers.
- **Failure points:** invites sent to contacts in an active sales cycle without the rep knowing — always check open opportunities first.

### E2 — Event day: arrival and meeting alerts

- **Trigger:** check-in or badge scan in the events platform.
- **Flow:** [A] check-in syncs to the CRM campaign member status → [A] if the account is a target account or has an open opportunity, alert the owner in Slack with a short brief (role, open deal stage, last contact, talking point) → [AI] Meeting Prep briefs for booked meetings (Outreach Meeting Prep Agent or a Claude/n8n agent reading the CRM).
- **Failure points:** venue connectivity; agree a fallback (export at end of each session).

### E3 — Post-event follow-up within 24 hours

- **Goal and metric:** time from event end to first follow-up; meetings booked per attendee; pipeline created within 90 days.
- **Trigger:** event end time, or attendance file uploaded.
- **Flow:**
  1. [A] Sync attendance status for every registrant: Attended, No-show, Cancelled; add badge scans and booth conversations.
  2. [A] Match to existing CRM accounts by email domain; deduplicate; flag personal email addresses and sole traders (see compliance reference). Route existing customers to the account manager and open opportunities to the deal owner before any scoring.
  3. [H] Event lead adds host notes within two hours ("asked about data residency", "evaluating a competitor"). For dinners and roundtables this one line is the biggest quality lever on the follow-up.
  4. [AI] Score each attendee against the ideal customer profile using role, company, sessions attended, questions asked, host notes and survey answers. Output: tier (1, 2, 3), reason, suggested next step. Skip scoring for curated events (dinners, roundtables): the guest list was the qualification, so everyone is tier 1.
  5. [A] Registration data already holds work email, title and company — map it in and do not run an email waterfall. Enrich only genuine gaps on tier 1 and tier 2 (phones only if someone will call).
  6. Route:
     - Tier 1 → [AI] draft a personal follow-up referencing what they attended, asked or the host noted → [H] owner edits and sends; task due within the service level, with an escalation alert a few hours before it lapses.
     - Tier 2 → tailored nurture sequence by session theme.
     - Tier 3 and non-fit → general nurture or no action.
     - No-shows → recording and a single relevant resource.
  7. [A] Write campaign member status, tier and follow-up date to the CRM so attribution and reporting work.
- **Lean option:** HubSpot workflows plus Clay for scoring and enrichment.
- **Scale option:** Swoogo → CRM, Cargo or Clay play for scoring, Outreach for rep follow-up, Slack for alerts.
- **Cost levers:** score before enriching; AI drafts only for tier 1; use the cheapest model for scoring and a stronger one for tier 1 drafts.
- **Failure points:** one generic email to everyone; scoring that ignores existing customers (route those to the account manager, not sales).

### E4 — Event return report

- **Trigger:** 30, 60 and 90 days after each event.
- **Flow:** [A] pull campaign members, opportunities created or influenced, stage movement → [AI] two-paragraph summary with what worked and the cost per opportunity → [H] programme owner reviews before it goes to leadership.
- **Metric:** cost per opportunity and pipeline per pound spent, by event type (flagship, roundtable, dinner, webinar).

---

## Partner communications

### P1 — Partner overlap to pipeline

- **Goal and metric:** partner-sourced and partner-influenced pipeline; introductions requested and accepted.
- **Trigger:** new overlap in Crossbeam (your prospect is a partner's customer), or a weekly batch.
- **Flow:**
  1. [A] Import overlaps (Crossbeam source in Clay, Crossbeam MCP, or Crossbeam's own agents).
  2. [A] Qualify: ideal-customer fit, no open late-stage deal, not already a customer.
  3. [AI] Draft the ask to the partner's account owner: why the intro makes sense for their customer, one line of context.
  4. [H] Partner manager and account executive approve; partner manager sends.
  5. [A] Record the partner and the ask in the CRM (partner-influenced field) and set a follow-up reminder.
- **Cost levers:** qualify before enriching; most overlap records need little or no enrichment.
- **Failure points:** spamming partners with weak asks — cap asks per partner per month and prioritise by deal value.

### P2 — Monthly partner update

- **Trigger:** monthly schedule.
- **Flow:** [A] collect inputs — product release notes, new case studies, upcoming events, co-marketing assets, programme deadlines, top shared opportunities by partner → [AI] draft one version per partner tier (strategic, growth, registered) → [H] partner manager approves → [A] send through the marketing platform or partner portal → [A] log opens and clicks against the partner record.
- **Failure points:** the same update for every partner; tiering is the point.

### P3 — Ecosystem alerts and deal registration

- **Flow:** Crossbeam Agents post to Slack when a defined condition occurs (a new mutual customer, a partner closing a deal on a shared account) → [A] create a CRM task for a co-marketing or case-study ask. Deal registration form → [A] duplicate and conflict check against open opportunities → [A] route to the right owner → [A] service-level alert if not accepted within the agreed time.

### P4 — Joint campaigns (webinars, co-hosted events)

- **Flow:** shared registration page with a partner field → [A] split leads by overlap and agreed ownership rules → [A] one follow-up owner per lead so nobody is contacted twice → [A] report shared results to the partner monthly.

---

## Product marketing

### M1 — Launch kit and distribution

- **Goal and metric:** launch materials ready on launch day; feature adoption among the target segment; sales confidence (quick pulse survey).
- **Trigger:** release ticket moves to "ready for release" in Jira or Linear, or a launch date is set.
- **Flow:**
  1. [AI] From the spec and ticket, draft the launch kit: internal enablement summary, customer email, release note, sales talk track, FAQ, objection handling.
  2. [H] Product marketer edits and approves; product manager checks accuracy.
  3. [A] Distribute: Slack enablement post, enablement hub, CRM email to the segment that uses the affected feature (from product usage data), help centre update request.
  4. [A] Two weeks later: adoption report for the target segment.
- **Cost levers:** this is token cost, not credit cost; one strong-model drafting pass plus human editing beats several cheap passes.
- **Failure points:** shipping AI drafts unreviewed; claims that outrun the product.

### M2 — Weekly competitive digest

- **Trigger:** weekly schedule.
- **Flow:** [A] monitor competitor pricing pages, changelogs, blogs, job postings and review sites (Claygent, an n8n scheduled agent, or a dedicated tool) → [AI] summarise only changes since last week, each with a "so what for sales" line → [H] product marketer approves → [A] post to the sales channel and suggest battlecard edits.
- **Cost levers:** compare page snapshots first and only run AI on pages that changed.

### M3 — Win–loss and voice of customer synthesis

- **Trigger:** monthly, or each closed deal.
- **Flow:** [A] collect closed-lost reasons, call transcripts (Gong or similar), survey responses → [AI] cluster themes with supporting quotes and counts → [H] product marketer validates → feed messaging, roadmap input and battlecards.

### M4 — Customer story pipeline

- **Trigger:** a customer hits a milestone (renewal, usage threshold, high satisfaction score).
- **Flow:** [A] check eligibility (no open support escalation, account manager agrees) → [AI] draft a personal ask → [H] account manager sends → [A] track the story through stages.

---

## Outbound and inbound

### O1 — Signal-led outbound

- **Trigger:** a buying signal — funding, hiring for a relevant role, leadership change, pricing-page visit, a champion's job move.
- **Flow:** [A] deduplicate against the CRM (customer? open opportunity? contacted in the last 30 days?) → [A] qualify the account → [A] enrich two or three relevant contacts → [AI] first line tied to the signal → [H] rep approves in the supervised stage → [A] sequence → [A] write signal and outcome back to the CRM for learning.
- **Cost levers:** most signals should die at the deduplication and qualification steps before any paid enrichment.

### O2 — Champion moves

- **Trigger:** a known champion or past buyer changes company.
- **Flow:** [A] detect job change → [A] check the new company's fit → [AI] draft a congratulatory note with a reason to reconnect → [H] the original relationship owner sends.

### I1 — Inbound enrichment and routing

- **Goal and metric:** speed to lead; correct routing rate.
- **Trigger:** form submission or demo request.
- **Flow:** [A] check whether the contact or account already exists → [A] enrich only missing routing fields (company size, country, industry) with the cheapest accurate provider → [A] score → [A] route by territory and segment → [A] Slack alert with a service-level timer → [A] escalate if untouched.
- **Cost levers:** enrichment here is per record and time-sensitive; keep the waterfall to one or two providers.

---

## Choosing what to build first

Score candidate workflows (1–5) on business impact, frequency, rule clarity, data readiness and risk (inverse). In most B2B programmes the order that pays back fastest is:

1. Inbound enrichment and routing (I1) — every lead touches it.
2. Post-event follow-up (E3) — visible, time-critical, high manual load.
3. Partner overlap to pipeline (P1) — cheap to run, often untapped.
4. Launch kit (M1) — high time saving per launch.
5. Signal-led outbound (O1) — powerful but needs clean data and routing first.

Change the order when the Diagnose phase says otherwise; a company running 40 events a year should start with E3.
