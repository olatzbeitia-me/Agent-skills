# Compliance for UK and EU outreach and enrichment

Read before designing any workflow that sends email, SMS or LinkedIn messages, or enriches personal data. This is a design checklist, not legal advice; for a new programme at scale, or anything unusual, recommend the user checks with their data protection lead or a lawyer.

## UK — two laws at once

UK email marketing sits under two overlapping regimes, both enforced by the Information Commissioner's Office:

1. **The Privacy and Electronic Communications Regulations** (the consent rules for electronic marketing).
2. **UK GDPR and the Data Protection Act 2018** (the rules for the personal data underneath).

Satisfying one does not satisfy the other.

### Subscriber type decides the email rule

- **Corporate subscribers** — limited companies, limited liability partnerships, Scottish partnerships and some government bodies. The electronic-mail consent rule does not apply to them, so cold business email to a work address at a limited company is permitted.
- **Individual subscribers** — includes **sole traders and ordinary (non-Scottish) partnerships**. Treat them like consumers: consent or the soft opt-in is required.
- Every marketing email, to anyone, must identify the sender, offer a simple way to opt out, and honour opt-outs promptly. Keep a suppression list and check it before every send.

**Design implication:** add a subscriber-type classification step before any cold send. If a record cannot be confidently classified as corporate (for example a personal email domain, or a company that looks like a sole trader), route it to a consent-first path (content offer, event invitation) or exclude it.

### UK GDPR still applies to named business contacts

- A named work email (firstname.lastname@company) is personal data.
- The usual lawful basis for business-to-business outreach is **legitimate interests**. Document a legitimate interests assessment: purpose, necessity, and the balancing test against the person's reasonable expectations.
- **Transparency:** when data comes from enrichment or a third party rather than the person, tell them where it came from and link the privacy notice — at the latest in the first message, and within one month in any case.
- **Objection is absolute for direct marketing:** once someone objects, stop, and suppress them across every tool in the stack (CRM, sequencer, Clay tables, Cargo models, ad audiences).
- Minimise: enrich only the fields the workflow needs; do not stockpile phone numbers "just in case".

### Data (Use and Access) Act 2025

Received Royal Assent on 19 June 2025, with changes phased in since. Most relevant here: it raises maximum fines for breaches of the electronic marketing rules to the UK GDPR level (up to £17.5 million or 4% of global turnover, whichever is higher). The Information Commissioner's Office has been updating its direct marketing guidance to reflect the Act — check the current version before finalising a programme.

## EU

Electronic marketing rules come from the ePrivacy Directive as implemented in each country, layered over the GDPR. Rules for business-to-business email differ by country, and several (Germany notably) require prior consent even for business email. Check each target country before designing a cold email workflow; for strict countries, design consent-first plays (events, content, partner introductions) instead.

## Channel-specific risks

- **LinkedIn automation:** LinkedIn's terms prohibit automated tools that send messages or scrape data on its platform; tools that automate LinkedIn carry a real risk of account restriction. State the risk when recommending them; keep volumes conservative and human-like; never automate from an executive's profile without their informed agreement.
- **Event attendee data:** only use attendee lists you have a right to use (the organiser's registration terms must cover sharing with sponsors; badge scans need notice at the stand). Do not buy or scrape attendee lists without clear provenance.
- **Cold email deliverability:** send from separate domains and inboxes, warm them up, keep volumes per inbox modest, and monitor bounce and complaint rates — a damaged sending reputation is a commercial risk as well as a compliance signal.

## AI agents and vendors

- Check each vendor's data processing agreement and where data is hosted (n8n Cloud is hosted in Frankfurt; self-hosting keeps data in your own environment).
- Send models only the personal data the step needs.
- Keep human approval on external sends while a workflow is in its supervised stage, and log what the agent sent and why.

## Pre-launch checklist

1. Lawful basis recorded, with a legitimate interests assessment where relied on.
2. Subscriber-type classification step in place for cold email.
3. Country check for every EU market targeted.
4. Privacy notice link and data-source statement in first contact.
5. Opt-out in every message; suppression list synced across every tool.
6. Data minimised to what the workflow uses; retention period set.
7. Vendor processing agreements and hosting locations confirmed.
