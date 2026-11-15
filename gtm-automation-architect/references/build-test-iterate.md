# Build, test and iterate

How to take a workflow from idea to trusted production system. The aim is that the stakeholder can see, in numbers, that the workflow meets the expectation they set — not merely that it runs.

## Contents
1. Agree "done" before building
2. Workflow blueprint template
3. Field ownership matrix
4. Build stages and promotion criteria
5. Test protocol
6. Iteration log
7. Runbook template
8. Monitoring and alerts
9. Naming, versioning and documentation

---

## 1. Agree "done" before building

Write this with the stakeholder before any build. It turns "make events less painful" into something testable.

| Item | Example |
|---|---|
| Business metric | Time from event end to first tier 1 follow-up |
| Baseline | 3 working days, done in spreadsheets |
| Target | Under 24 hours for tier 1; under 48 hours for tier 2 |
| Quality bar | Fewer than 1 in 20 tier 1 drafts needs a full rewrite |
| Cost ceiling | Under £X per event, or under Y credits per month |
| Review date | After three events, or six weeks |
| Decision owner | Head of field marketing |

## 2. Workflow blueprint template

```markdown
# Workflow: [Programme]-[Object]-[Purpose] v[n]

## Purpose
- Business goal and metric:
- Baseline → target:
- Owner (accountable):        Builder:
- Service level (e.g. "tier 1 follow-up within 24 hours"):

## Trigger
- Event or schedule:
- Source system:
- Expected volume (per run / per month):

## Inputs
| Field | Source | Required? | If missing |
|---|---|---|---|

## Steps
| # | Step | Tool | Type (rule / AI / human) | Runs only if | Output |
|---|---|---|---|---|---|

## AI steps
| Step | Task | Model tier | Output fields | Confidence rule (below X → human) |
|---|---|---|---|---|

## Human checkpoints
- Where, who, how long they have, what happens if nobody acts:

## Outputs and write-back
| Field written | System | Overwrite existing? | Field owner |
|---|---|---|---|

## Failure handling
- Missing data:
- Tool or API failure (retry, then alert whom?):
- Duplicate or conflict:
- How to pause the workflow:

## Cost
- Per run: Data Credits / Actions / executions / model tokens (show arithmetic):
- Per month at expected volume:
- Cost per qualified output:

## Compliance
- Personal data processed and lawful basis:
- Subscriber type check (corporate / individual) if sending:
- Opt-out and suppression handling:

## Acceptance criteria
| Criterion | Threshold | How measured |
|---|---|---|
```

## 3. Field ownership matrix

One writer per field. Any field with two writers needs a rule for which wins.

| Field | Object | Owning system | Written by | Overwrite rule | Read by |
|---|---|---|---|---|---|
| Job title | Contact | CRM | Clay enrichment | Only if empty or older than 6 months | Scoring, routing |
| Event tier | Campaign member | CRM | Scoring play | Always (latest wins) | Follow-up routing, reporting |
| Lead owner | Lead | CRM | Routing workflow | Never overwritten by enrichment | Everyone |

## 4. Build stages and promotion criteria

| Stage | What happens | Promote when |
|---|---|---|
| 1. Assisted | System prepares (drafts, lists, scores); a human does the action | Acceptance criteria met on the golden set and on one live cycle |
| 2. Supervised | System acts; a human approves each batch or each exception | Criteria met for an agreed run count (e.g. three events, or four weekly cycles) with edit rate under the quality bar |
| 3. Autonomous with monitoring | System acts alone; alerts and a weekly sample review | Ongoing; demote immediately if alerts breach thresholds |

External sends and overwrites of existing CRM data stay at stage 2 until promotion is agreed with the business owner.

Build environment rules:
- Build in a sandbox table, test play or copy of the workflow.
- Auto-run off; test on 10–50 rows first.
- Use test or sandbox CRM records where the CRM supports them; never test sends to real prospects.

## 5. Test protocol

1. **Golden set.** 30–50 real records with known correct answers (right tier, right owner, right email). Include edge cases:
   - duplicates and near-duplicates (same person, different email)
   - existing customers and accounts with open opportunities
   - personal email addresses (gmail.com, outlook.com and similar)
   - sole traders and ordinary partnerships (compliance)
   - non-English names and companies, subsidiaries, recently acquired companies
   - competitors and partners
   - records with almost no data
2. **Dry run.** Run the workflow on the golden set with sends disabled. Score each acceptance criterion.
3. **Shadow mode.** Run alongside the manual process for one or two live cycles and compare: speed, accuracy, coverage, cost.
4. **Stakeholder review.** Show results against the "done" table, not a demo of the build.
5. **Iterate.** Change one variable at a time (prompt, provider order, threshold, model) and re-run the golden set, so you know what moved the result.

Acceptance criteria examples:

| Criterion | Typical threshold |
|---|---|
| Routing accuracy | ≥ 95% to the correct owner |
| Email coverage (tiers 1–2) | ≥ 80% verified |
| Tier agreement with a human reviewer | ≥ 85% |
| Draft edit rate | ≤ 1 in 5 needs more than light edits |
| Cost per qualified output | Within the agreed ceiling |
| Time to complete | Within the service level |

## 6. Iteration log

| Date | Version | Change (one variable) | Golden-set result before → after | Cost before → after | Decision |
|---|---|---|---|---|---|

## 7. Runbook template

```markdown
# Runbook: [workflow name] v[n]
- What it does (two sentences):
- Business owner:            Technical owner:
- Trigger and schedule:
- Systems touched and fields written:
- Dependencies (API keys, integrations, plans):
- How to pause it:
- How to re-run a failed batch safely (without duplicating sends):
- Common failures and fixes:
  | Symptom | Likely cause | Fix |
- Alerts: what fires, where, who responds:
- Last reviewed:
```

## 8. Monitoring and alerts

| Metric | Alert when | Goes to |
|---|---|---|
| Records processed per run | Zero, or more than 2× normal | Technical owner |
| Error or failure rate | Above 5% of a run | Technical owner |
| Daily credit, Action or execution burn | Above the daily budget share | Technical owner and budget holder |
| Service level breaches | Any tier 1 item past its deadline | Business owner |
| Human queue age | Approvals waiting longer than the agreed time | Business owner |
| Bounce or complaint rate on sends | Above the sender's safe threshold | Technical owner; pause sends |

## 9. Naming, versioning and documentation

- Name every table, play and workflow `[Programme]-[Object]-[Purpose]-v[n]`, for example `Events-Attendee-Followup-v3`.
- Keep the blueprint, field ownership matrix, runbook and iteration log together in one place the team can find.
- When something changes, bump the version, note it in the change log, and keep the previous version paused rather than deleted until the new one has passed a live cycle.
- Run a short enablement session for the people who receive the outputs (reps, partner managers, product marketers): what will arrive, what they must do, how to flag a bad output.
