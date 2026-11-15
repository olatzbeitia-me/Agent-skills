# GTM tool landscape (checked October 2026)

Prices, plan gating and features move monthly. Treat every figure here as a starting point: re-check the vendor's pricing page before giving a budget, and quote the date you checked. Where this file says "verify", it was not confirmed from a primary or recent source.

## Contents
1. Market shifts to know (December 2025 – October 2026)
2. The six-layer model
3. Clay
4. Cargo
5. Outreach
6. HubSpot and Breeze agents
7. Salesforce
8. n8n
9. Zapier and Make
10. Signal tools
11. Partner ecosystem — Crossbeam
12. Events platforms
13. Senders for cold email and LinkedIn
14. Product marketing tools
15. Quick selection guide

---

## 1. Market shifts to know (December 2025 – October 2026)

- **Salesloft and Clari merged** (December 2025).
- **Apollo acquired Pocus** (March 2026).
- **Persana shut its platform** (May 2026) after joining Rox.
- **Outreach rebranded to Outreach.ai** and launched Agent Studio, Omni and new agents (April 2026).
- **HubSpot acquired Warmly** (announced 30 June 2026). Warmly said contracts, pricing and product stay unchanged for now, with deeper HubSpot integration planned — likely to favour HubSpot-native customers over Salesforce users.
- **Zoom agreed to acquire Common Room** (2 July 2026) to sit inside Zoom Revenue Accelerator; Common Room continues standalone for now.

What it means for architecture: the signal layer is being absorbed into larger platforms. Keep scoring, routing and qualification logic documented outside any single tool, and avoid making a tool at acquisition risk the only place a critical rule lives.

## 2. The six-layer model

A 2026 survey of 62 companies' GTM stacks (ColdIQ) found the same four core layers in every stack — data and enrichment, automation, CRM, specialist senders — with Clay in 71% of stacks, n8n in 48%, HubSpot in 39% and Attio in 32%. For programme work (events, partners, product marketing) two more layers matter, giving six:

| Layer | Job | Examples |
|---|---|---|
| 1. System of record | Holds the truth about accounts, contacts, deals, campaigns | Salesforce, HubSpot, Attio; Snowflake or BigQuery as warehouse |
| 2. Data and enrichment | Fills gaps: emails, phones, firmographics, research | Clay, Apollo, Hunter, Cognism, provider APIs |
| 3. Signals | Tells you who is in market now | Website visitor identification, intent data, social listening, product usage, partner overlap |
| 4. Orchestration and agents | Decides what happens next and runs it | Clay Workflows and Account Agents, Cargo, n8n, Make, Zapier, Outreach Agent Studio, HubSpot Breeze Studio, Claude with MCP servers |
| 5. Engagement (senders) | Sends the message | Outreach, Salesloft, HubSpot sequences, Clay Sequencer, Instantly, Smartlead, lemlist, HeyReach |
| 6. Programme-specific | Runs a programme end to end | Events (Swoogo, Luma), partners (Crossbeam, PartnerStack), competitive intelligence (Klue, Crayon), call recording (Gong) |

Analogy: layer 1 is the bank account, layers 2–3 are the information coming in, layer 4 is the person deciding what to do, layer 5 is the post room, layer 6 is the specialist department.

---

## 3. Clay

**What it is:** a spreadsheet-like workbench for enrichment, research and personalisation, now positioning itself as an end-to-end GTM system.

**Notable 2026 capabilities:**
- Waterfall enrichment across 150+ data providers (tries provider A, then B if A finds nothing, and so on).
- Claygent — AI web-research agent; open-weight model options added July 2026.
- Sculptor — natural-language builder and co-pilot for tables and workflows; Sculptor Sandbox Mode (May 2026) lets you review AI-generated columns before they go live and before credits burn.
- Audiences — combines CRM data, signals and enrichment in one view; generally available from June 2026, with SOQL imports from Salesforce, HubSpot deal imports, and reporting on the pipeline and revenue Clay-sourced accounts drove.
- Sequencer — native email sending from Clay. Since September 2026 it requires Launch or above; Growth can buy domains and inboxes for it.
- Account Agents, Workflows, Clay Plugin and command-line tool, Clay MCP server, company and people lookalikes, ad audiences.

**Pricing since 11 March 2026 ("Pricing 3.0") — two meters:**

| Plan | Monthly billing | Annual billing (per month) | Data Credits / month | Actions / month | Notable |
|---|---|---|---|---|---|
| Free | $0 | $0 | 100 | 500 | — |
| Launch | $185 | $167 | 2,500 | 15,000 | Phone enrichment, signals |
| Growth | $495 | $446 | 6,000 | 40,000 | CRM sync, HTTP API, webhooks, web intent, ads |
| Enterprise | Custom | Custom annual | Custom | Custom | — |

- **Data Credits** buy data from the marketplace (from about $0.05 each, cheaper at volume).
- **Actions** meter platform work — an enrichment step, an AI task, an HTTP call, a CRM push (under $0.01 each). Every step that fills in data or runs AI on a row uses one Action.
- Failed lookups no longer cost Data Credits.
- Using your own provider API key removes the Data Credit charge for that provider, but the step still uses one Action.
- Data Credits roll over up to 2× the monthly amount on Launch and Growth; Actions reset every month.
- Each paid plan is two sliders added together. Launch = $60 for 15,000 Actions + $125 for 2,500 Data Credits; Growth = $205 for 40,000 Actions + $290 for 6,000 Data Credits. Growth Action steps published in October 2026: 40,000 ≈ $205, 60,000 ≈ $290, 100,000 ≈ $450, 200,000 ≈ $850 — use these for overage arithmetic.
- **Plan gating is an architecture decision:** CRM sync (Salesforce, HubSpot), HTTP API calls, webhooks and web intent are Growth features. A design that writes back to the CRM from Clay needs Growth, or a different write-back route. Check before designing.
- Clay's guidance: a fully enriched contact typically uses 6–20 Data Credits; emails are cheap, phone numbers expensive.
- Legacy plans (Starter, Explorer, Pro) can stay indefinitely, but the newer features (Audiences, Account Agents, Workflows, Plugin, Sequencer on Audiences) are available to legacy plans only until 31 December 2026.

**Where it fits:** research-heavy enrichment, list and total-addressable-market building, row-level personalisation, rapid prototyping of plays, event and partner list processing.

**Where it breaks:** it is a build-it-yourself surface, so table sprawl and undocumented logic accumulate; orchestration-heavy flows can exhaust Actions quickly (a 10,000-row, four-provider waterfall can consume around 28,000 Actions — nearly double Launch's monthly allowance); it is not a system of record.

## 4. Cargo (getcargo.ai)

**What it is:** a Y Combinator-backed GTM orchestration platform that describes itself as infrastructure for AI agents. SOC 2 Type II.

**Core building blocks:**
- **Data models** — warehouse-hosted tables built from CRM, APIs, webhooks and SQL; can track processed records so plays do not handle the same row twice.
- **Plays** — event-driven automations bound to a data model that fire as rows change (enrich, score, route, write back, notify).
- **Agents** — workers with a prompt, a step budget, an evaluator and a set of permitted tools; can be chained (research → qualify → route).
- Operable from a visual interface, a command-line tool and over MCP; definitions can live as TypeScript in your own code repository. Waterfalls across providers such as Apollo and Cognism.

**Pricing:** credits split across three meters (enrichment, orchestration, storage), bought on a volume slider. Published points have included roughly 1,500 credits ≈ $165/month, 2,500 ≈ $250, 17,000 ≈ $1,190, and 50,000+ from ≈ $3,000; a free trial gives 100 credits. Third-party write-ups disagree on tier names — verify on the pricing page.

**Where it fits:** scale-ups with a GTM engineer or technical RevOps owner, a warehouse or many systems, always-on plays, and a wish to version-control GTM logic.

**Where it breaks:** steep learning curve, few public reviews, and a large price gap between the 2,500- and 17,000-credit points. Overkill for a team of one running a handful of workflows.

## 5. Outreach (Outreach.ai)

**What it is:** sales engagement and revenue workflow platform, now marketed as an agentic AI platform.

**2026 capabilities:**
- Agents and AI hub in the navigation (February 2026); Research Agent with a scheduler for recurring account research; Outreach MCP server so external agents (for example Claude) can read Outreach knowledge and trigger actions.
- Spring release (April 2026): **Omni** conversational agent (including Slack and mobile); **Agent Studio**, a visual canvas with pre-built agent workflow templates that admins configure and deploy (including running Research Agent inside a workflow and acting on deal inactivity); **Meeting Prep Agent**; **Prospect Research Agent**; **Deal Agent** sending suggested field updates to Slack; Deal Alerts.
- AI usage metered by AI credits. Third-party reviews describe Amplify Core, Plus and Pro packaging — verify with Outreach.

**Where it fits:** sales-led teams already running sequences in Outreach who want agents close to sequences and deals.

**Where it breaks:** enrichment depth is shallower than Clay; marketing programmes (events, partners, launches) are not its native territory; enterprise pricing.

## 6. HubSpot and Breeze agents

**Credits model:** Breeze agents draw from a shared HubSpot Credits pool (shared with Breeze Intelligence enrichment and Data Studio syncs). About $10 per 1,000 credits. Included monthly credits are roughly 500 on Starter, 3,000 on Professional and 5,000 on Enterprise. Autonomous agents need Professional or Enterprise.

**Outcome-based pricing from 14 April 2026:**

| Agent | Charge |
|---|---|
| Customer Agent | 50 credits (≈ $0.50) per resolved conversation |
| Prospecting Agent | 100 credits (≈ $1.00) per lead recommended for outreach; 10 credits (≈ $0.10) per research task |
| Data Agent | about 10 credits (≈ $0.10) per answer |

- **Breeze Studio** customises agents; the Breeze Marketplace offers beta agents (for example an account-based marketing landing page agent, a request-for-proposal agent, a sales-to-marketing feedback agent, a customer health agent). Beta agents are free for now; HubSpot aims to give about 30 days' notice before they consume credits — do not build long-term budgets on beta pricing.
- Standard HubSpot workflows (deterministic if/then automation) do not consume credits — a strong reason to keep rule-based logic native.
- Marketing Hub is priced by marketing contacts: records pushed in from enrichment tools can raise the contact tier. Custom objects need Enterprise (verify), so on Professional model things like partners as company records with a type property and associations.
- Warmly's visitor identification and Inbound and TAM (total addressable market) agents will be folded in over time.

**Watch-out:** a Prospecting Agent pointed at a messy database burns credits recommending leads nobody would call. Clean and segment the data before switching agents on.

## 7. Salesforce

Not re-checked in this research pass. Use Salesforce Flow for deterministic in-CRM logic and campaign member statuses for event and programme attribution. Agentforce pricing has changed several times — verify before quoting any figure.

## 8. n8n

**What it is:** open-source workflow automation with a visual canvas and a self-hosting option.

**Pricing — execution-based** (one execution = one complete workflow run, however many steps):

| Plan | Monthly | Executions / month |
|---|---|---|
| Starter | €24 | 2,500 |
| Pro | €60 | 10,000 |
| Business | €800 | 40,000 |
| Enterprise | Custom | Custom |

Roughly 17% off on annual billing. Since April 2026 every plan has unlimited workflows and users. The self-hosted Community Edition is free with unlimited executions (you pay for hosting). n8n Cloud is hosted in Frankfurt, useful for EU data residency. AI Workflow Builder credits are a separate allowance from executions.

**AI capability:** AI Agent node (built on LangChain) that can call any other node as a tool, memory and vector store nodes, an MCP Client node for connecting to MCP servers, and human-in-the-loop approval for agent tool calls (January 2026).

**Where it fits:** joining many systems, custom APIs, high volumes, cost-sensitive teams, EU data residency, Claude-powered agents that need approval gates.

**Where it breaks:** it has no built-in GTM concepts (no notion of account, contact or play — you model them); ownership can drift to a data or engineering team, putting GTM back in a ticket queue; polling triggers burn executions — use webhooks.

## 9. Zapier and Make

- **Zapier** is task-based: every step in a Zap counts as a task. Paid entry around $19.99/month (annual) for 750 tasks. Zapier Agents is a separate product that calls Zaps. Best for low-volume glue owned by non-technical teams.
- **Make** is a visual builder metered by operations or credits, with an AI Agents module — verify current pricing.
- Rule of thumb from 2026 comparisons: for technical teams, n8n becomes clearly cheaper from roughly 5,000 workflow runs a month.

## 10. Signal tools

| Tool | What it watches | Price signal (verify) |
|---|---|---|
| Unify | Website, research and social signals for warm outbound | Free tier, then about $20 rising to $60 per seat per month (August 2026) |
| Trigify | LinkedIn post engagement, topics, tracked accounts | From about $40/month |
| Common Room | Multi-source: social, community, product, web | Essential about $2,100–2,500/month billed annually; Zoom acquisition pending |
| Warmly | Person-level website visitor identification | Now part of HubSpot |
| 6sense, Bombora | Third-party intent | Verify |

## 11. Partner ecosystem — Crossbeam

- Maps account overlap with partners (your prospects who are their customers, and so on) and surfaces ecosystem-qualified leads.
- **Clay integration:** import overlapping accounts into a Clay table or enrich a company with partner data (partner owner, populations, record fields from the account overlaps endpoint). Requires Crossbeam's Supernode plan; Clay-side plan gating has changed with the 2026 repackaging — verify.
- **Crossbeam MCP** (read-only) gives AI clients overlaps, a single-account view, partner health metrics (overlap counts, open deals, win rate, recency), partner recommendations on an open opportunity and recent ecosystem activity.
- **August 2026 release:** Crossbeam Agents watch for a condition (for example a new mutual customer, or a partner closing a deal on a shared account) and post to Slack; Partner Invitations and Open Data Partners are generally available; an integration seat type for managing data connections.

## 12. Events platforms

- **Swoogo** — registration and event management. Typical integration pattern with Salesforce, HubSpot or Marketo: one CRM campaign per event; registrant status synced as Registered, Attended, No-show or Cancelled; no-show follow-up tasks; post-event survey answers written to the contact. Often wired through an integration platform; custom registration fields vary per event, so field mapping needs a per-event check.
- **Luma** — lightweight community and meetup events with an API and webhooks; good for community and ecosystem programmes.
- **Clay for events** — Clay's own playbook for event sign-ups scores registrants against the ideal customer profile with AI first and enriches only the best fits. Sculptor can assemble lists of companies linked to a public event; coverage depends on how public the attendee data is, and legality depends on the source's terms (see the compliance reference).

## 13. Senders for cold email and LinkedIn

Instantly, Smartlead and lemlist (email) and HeyReach (LinkedIn) are common specialist senders; Clay Sequencer is the native option inside Clay. Keep cold sending on separate domains and inboxes. LinkedIn's terms prohibit automated tools on its platform, so LinkedIn automation carries account-restriction risk — say so when recommending it. Prices not checked here — verify.

## 14. Product marketing tools

Competitive intelligence (Klue, Crayon), call recording and conversation intelligence (Gong), sales enablement content hubs (Highspot, Seismic), product change sources (Jira, Linear, changelogs). Not priced here — verify. In many stacks the cheapest competitive monitoring is a scheduled Claygent or n8n agent summarising competitor pages, with a product marketer approving the digest.

## 15. Quick selection guide

| If the job is… | Start with | Because |
|---|---|---|
| Rules on CRM records only (routing, status changes, reminders) | Native HubSpot workflow or Salesforce Flow | No credits, one system, easiest to maintain |
| Enrich and research a list, personalise per row | Clay | Waterfalls, Claygent and row-level AI in one place |
| Always-on plays across many systems with agents, owned by an engineer | Cargo | Data models plus plays plus agents, version-controlled |
| Glue many systems or custom APIs at volume, or EU hosting | n8n | Execution pricing, self-host option, agent nodes with approval |
| Two or three apps, low volume, marketer-owned | Zapier or Make | Fastest to set up, no engineering |
| Agents inside the sales engagement flow | Outreach Agent Studio | Agents sit next to sequences and deals |
| Agents on HubSpot data for a HubSpot-native team | Breeze agents | Native data, outcome pricing — clean data first |
| Partner overlap into pipeline | Crossbeam plus Clay or the Crossbeam MCP | Overlap data where the outreach is built |
