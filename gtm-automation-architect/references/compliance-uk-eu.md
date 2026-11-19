# Compliance for UK and EU outreach and enrichment

Read before designing any workflow that sends email, SMS or LinkedIn messages, or enriches personal data. This is a design checklist, not legal advice; for a new programme at scale, or anything unusual, recommend the user checks with their data protection lead or a lawyer.

UK sections checked against the Information Commissioner's Office guidance on 19 November 2026. The EU section was not re-checked then.

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

### "Electronic mail" is wider than email

The regulator's guidance counts texts, picture and voicemail messages, in-app messages and private messages on social media as electronic mail. Adverts shown publicly, including targeted adverts in a social media feed, are not. So the rules above apply to LinkedIn direct messages as well as to email (see the LinkedIn note under channel-specific risks).

### Where the contact details came from

- **Publicly available is not permission.** An address found on a website, a social profile or through an enrichment provider still needs consent, or a soft opt-in, if the subscriber is an individual (sole traders and ordinary partnerships included).
- **Bought-in lists:** consent only counts if it named your organisation and the channel you plan to use. Wording such as "trusted partners" does not. Check that the seller can show who consented, when and how.
- **The soft opt-in never covers bought-in or enriched contacts.** It requires that you collected the details from the person yourself, while selling or discussing a sale, with a chance to opt out at that point.

### Agencies, senders and responsibility

If an agency or another organisation sends marketing on your behalf, you remain responsible as the organisation that instigated it, and both of you must comply. Put a written contract in place and check how they comply. A bulk-email platform or webmail service that only delivers the messages does not normally share that responsibility; it stays with you. **Design implication:** outsourced outbound (an agency running sequences from its own tools) needs the same subscriber-type check, suppression list and opt-out handling as an in-house build.

### UK GDPR still applies to named business contacts

- A named work email (firstname.lastname@company) is personal data.
- The usual lawful basis for business-to-business outreach is **legitimate interests**. Document a legitimate interests assessment: purpose, necessity, and the balancing test against the person's reasonable expectations.
- **Transparency:** when data comes from enrichment or a third party rather than the person, tell them where it came from and link the privacy notice — at the latest in the first message, and within one month in any case.
- **Objection is absolute for direct marketing:** once someone objects, stop, and suppress them across every tool in the stack (CRM, sequencer, Clay tables, Cargo models, ad audiences).
- Minimise: enrich only the fields the workflow needs; do not stockpile phone numbers "just in case".

### Data (Use and Access) Act 2025

Received Royal Assent on 19 June 2025 and was brought into force in stages over the following year. Most of its data protection provisions, including the higher fines for the electronic marketing rules, took effect on 5 February 2026, and the Information Commissioner's Office confirmed on 19 June 2026 that all of them are now in force. What matters for go-to-market work:

- **Fines:** breaches of the electronic marketing rules can now be fined at the UK GDPR level, up to £17.5 million or 4% of global turnover, whichever is higher.
- **Legitimate interests:** the Act states that direct marketing can be a legitimate interest. The regulator describes this as a clarification that does not materially change how personal data may be used, so the balancing test and a written assessment are still needed.
- **Charities** gained a second soft opt-in, from 5 February 2026, for marketing that furthers their charitable purposes. It does not help commercial business-to-business outreach.
- **Guidance:** the regulator's detailed guidance on direct marketing by electronic mail was updated on 28 April 2026; its shorter Guide to the Privacy and Electronic Communications Regulations is marked as under review. Check both before finalising a programme.

## EU

Electronic marketing rules come from the ePrivacy Directive as implemented in each country, layered over the GDPR. Rules for business-to-business email differ by country, and several (Germany notably) require prior consent even for business email. Check each target country before designing a cold email workflow; for strict countries, design consent-first plays (events, content, partner introductions) instead.

## Channel-specific risks

- **LinkedIn automation:** two separate risks. First, LinkedIn's terms prohibit automated tools that send messages or scrape data on its platform, so tools that automate LinkedIn carry a real risk of account restriction. Second, a LinkedIn direct message is electronic mail under the Privacy and Electronic Communications Regulations, so the marketing rules apply, not only LinkedIn's terms. The regulator's guidance does not say how the corporate-subscriber rule applies to a social media account, which is normally held by the person rather than their employer: flag this as an open question for the data protection lead before automating LinkedIn messages at volume. State both risks when recommending LinkedIn automation; keep volumes conservative and human-like; never automate from an executive's profile without their informed agreement.
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
8. Every channel covered: texts, in-app messages and private social media messages (LinkedIn included) follow the same rules as email.
9. Source checked for every list: bought-in consent names your organisation and the channel; enriched or publicly found addresses are not treated as consent.
10. Any agency or third-party sender has a written contract, has been checked for compliance, and uses the shared suppression list.
