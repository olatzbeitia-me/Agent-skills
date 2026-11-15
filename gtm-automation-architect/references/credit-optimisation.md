# Credit and cost optimisation

Credits behave like a pay-as-you-go electricity meter: the bill is set less by the tariff than by what you leave switched on. Most waste comes from running paid steps on rows that were never going to be used.

## Contents
1. Measure the right unit
2. The levers, ranked
3. Platform-specific levers
4. Worked example — 10,000-row batch in Clay
5. Quick arithmetic for other platforms
6. Monthly cost review

---

## 1. Measure the right unit

Track **cost per qualified output**, not cost per row:

> cost per qualified output = (Data Credits × price + Actions or executions × price + model token cost + share of seat licences) ÷ qualified outputs

"Qualified output" is whatever the business values: a contact that passes the ideal customer profile and has a verified email, a tier 1 attendee with a drafted follow-up, an approved partner introduction. A workflow can look cheap per row and be expensive per qualified output if most rows are discarded after paying for them.

Always state unit prices and assumptions next to any figure so the user can substitute their own.

## 2. The levers, ranked

1. **Use what you already hold.** Event registrations, form fills and CRM records usually already contain work email, job title and company. Map those fields in before any enrichment step — an email waterfall on event registrants is the commonest pure waste.
2. **Filter before you pay.** Deduplicate against the CRM and remove customers, open opportunities and recently contacted people before any paid step. Qualify at account level with cheap firmographic data before enriching people. Do deduplication upstream (in the CRM, warehouse or a free formula) where it costs nothing.
3. **Conditional runs.** Run a step only when its input exists and its output is missing ("only run if email is empty and tier is 1 or 2"). In Clay, use conditional run formulas; in Cargo, filters on the data model and processed-record tracking; in n8n, an IF node before the paid call.
4. **Shallow, ordered waterfalls.** Put the cheapest accurate provider first and stop at two or three providers. Each extra provider buys a little more coverage at a rising price per extra hit; measure the coverage gain per provider and cut the tail. Validate results (email verification, phone line type) rather than accepting the first answer — the cheapest provider can return the wrong person's number.
5. **Enrich on need.** Emails are cheap; phone numbers are expensive. Enrich phones only for top-tier accounts where a call will actually happen. Run AI research only where it changes the message.
6. **Right-size the model.** A small, cheap model for classification, extraction and scoring; the strongest model only for final customer-facing copy. Ask for structured output (fixed fields) so no second pass is needed to clean it.
7. **Cache and reuse.** Store enrichment results in the CRM or warehouse with a date stamp. Re-enrich only fields that decay (job title, employer) on a schedule, never the whole table.
8. **Bring your own API keys** where volume justifies the provider contract. In Clay this removes Data Credits for that provider but still uses one Action per run.
9. **Triggers and batching.** Webhooks over polling (polling burns executions even when nothing has changed). Batch on a schedule when the use case tolerates delay.
10. **Switch off auto-run while building.** Test on 10–50 rows in a sandbox; turn auto-update off on tables under construction.
11. **Caps and alerts.** Per-table or per-play run caps, daily burn alerts against the monthly budget, and an owner who receives them.
12. **Count the downstream bill.** Pushing records into other systems has its own cost: HubSpot Marketing Hub is priced by marketing contacts, so flooding it with unqualified rows can move you up a contact tier; senders charge per inbox or seat; reps lose time on poor leads. Push only qualified tiers, and in HubSpot consider keeping pushed records as non-marketing until they engage.
13. **Diagnose by column before redesigning.** Use the platform's usage breakdown (per column in Clay, per play in Cargo, per workflow in n8n) to find where the meter actually runs. Always-on AI, research and push columns usually outweigh the data itself.

## 3. Platform-specific levers

| Platform | Meter | Biggest levers |
|---|---|---|
| Clay | Data Credits (data) and Actions (every step). Actions reset monthly; Data Credits roll over up to 2× on Launch and Growth. Failed lookups cost no Data Credits | Filter and deduplicate before import; conditional runs; two- or three-provider waterfalls; own keys for high-volume providers; Sculptor Sandbox Mode and sandbox tables before full runs; review auto-run columns monthly |
| Cargo | Credits across enrichment, orchestration and storage | Filter segments on the data model; track processed records so plays never reprocess rows; give agents step budgets; keep enrichment waterfalls short |
| HubSpot Breeze | HubSpot Credits, outcome-based (for example $1 per Prospecting Agent recommended lead) | Clean and segment data before switching agents on; narrow agent plays; keep rule-based logic in standard workflows, which use no credits; do not budget on free beta agents |
| n8n | Executions (one full run regardless of steps) | Webhooks over polling; fold many small workflows into one run where sensible; self-host for very high volume; watch AI Workflow Builder credits separately |
| Zapier | Tasks (every step counts) | Move long, multi-step or high-volume flows to n8n; filter early in the Zap |
| Outreach | AI credits for agents | Schedule Research Agent only for accounts in active plays; avoid re-researching unchanged accounts — verify current metering with Outreach |
| Model APIs | Tokens | Small model to classify, strong model to write; short prompts; structured outputs; cache repeated context |

## 4. Worked example — 10,000-row batch in Clay

**Scenario:** 10,000 rows a month from event lists and website-intent visitors. Clay Growth plan (6,000 Data Credits, 40,000 Actions included).

**Assumptions (replace with the user's real figures):** Data Credit ≈ $0.05; Action ≈ $0.005 (Growth's 40,000 Actions are priced at about $205); full contact enrichment with phone ≈ 12 Data Credits; email only ≈ 2; phone only ≈ 10; company lookup ≈ 1. Treat Claygent and AI columns as one Action each plus model cost.

### Naive design
Every row: four-provider email waterfall, three-provider phone waterfall, Claygent research, AI first line, CRM push.

| Item | Calculation | Total |
|---|---|---|
| Data Credits | 10,000 rows × 12 | 120,000 |
| Actions | 10,000 rows × ~8 steps (≈5 waterfall steps actually run + research + AI + push) | 80,000 |
| Cost | 120,000 × $0.05 + 80,000 × $0.005 | ≈ $6,400 |

That is 20× the plan's Data Credits and 2× its Actions. If only 1,200 rows turn out to be qualified, the real cost is ≈ $5.33 per qualified contact.

### Optimised design

| Step | Rows in | Data Credits | Actions |
|---|---|---|---|
| 1. Deduplicate against CRM (customers, open deals, recent contact) — done in Clay | 10,000 → 7,000 | 0 | 10,000 |
| 2. Roll up to companies and check fit | 7,000 rows = 2,500 companies → 1,000 fit | 2,500 | 2,500 |
| 3. AI tier scoring with a small model | 2,800 people at fit companies | 0 | 2,800 |
| 4. Email waterfall, two providers, tiers 1–2 only | 1,200 | 2,400 | ~1,700 |
| 5. Phone, tier 1 only | 300 | 3,000 | 600 |
| 6. Research and AI first line, tier 1 only | 300 | 0 | 600 |
| 7. Push to CRM, tiers 1–2 | 1,200 | 0 | 1,200 |
| **Total** | | **7,900** | **≈ 19,400** |

Cost ≈ 7,900 × $0.05 + 19,400 × $0.005 ≈ $395 + $97 ≈ **$492**, about $0.41 per qualified contact — **roughly a 92% saving**.

Further step: move deduplication (step 1) upstream into a CRM report, warehouse query or import filter and the batch drops by another ~10,000 Actions, to ≈ 9,400.

The pattern to explain to stakeholders: spend shifts from "pay for everything, then filter" to "filter for free, then pay for the few".

## 5. Quick arithmetic for other platforms

- **HubSpot Prospecting Agent:** 500 recommended leads a month × 100 credits = 50,000 credits ≈ $500. Professional includes about 3,000 credits, so ≈ 47,000 credits (≈ $470) is overage — before any Customer Agent or Data Agent use draws from the same pool.
- **n8n versus Zapier:** a 15-step workflow run 3,000 times a month = 3,000 executions on n8n (fits Pro at €60/month) versus 45,000 tasks on Zapier, which needs a high tier.
- **Clay Actions trap:** a 10,000-prospect list through a four-tier waterfall can consume around 28,000 Actions — nearly double Launch's 15,000 monthly allowance — before any AI or CRM steps.

## 6. Monthly cost review

Run this checklist once a month for every live workflow:

1. Credits, Actions or executions used versus budget, by workflow and by column or step.
2. Cost per qualified output this month versus last month.
3. Rows processed that produced no qualified output — where did they drop out, and could they have been filtered earlier for free?
4. Waterfall hit rate by provider — remove providers that add little coverage.
5. AI steps — is each one changing an outcome? Could a smaller model do it?
6. Auto-run columns and scheduled plays still switched on for retired programmes.
7. Rollover and expiry — Actions that will reset unused, Data Credits approaching the rollover cap.
8. Keep, fix or kill decision for each workflow, recorded in the change log.
