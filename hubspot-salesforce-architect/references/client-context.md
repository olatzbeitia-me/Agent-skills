# Reference client: a B2B data-as-a-service business

Use this file to tailor recommendations. "What the business is" describes a typical B2B risk and compliance data provider: a composite reference profile, not a named company. Everything under "Default assumptions" is an assumption: state it when you rely on it, and replace it as soon as the user gives you a real fact about their own business.

## What the business is

- A data-as-a-service company selling risk and compliance intelligence, combining artificial intelligence with a team of research analysts.
- Typical products: risk scores and metrics, a web platform, data feeds for integration, reports, and monitoring alerts.
- Client segments and their typical use cases:
  - Banks: due diligence, know-your-customer and client onboarding, reputational risk.
  - Asset managers and owners: portfolio screening and monitoring, compliance, engagement.
  - Corporates: third-party due diligence, vendor risk management, supplier monitoring.
  - Insurance providers: due diligence, underwriting risk assessment, compliance.
  - Private equity and debt: due diligence, portfolio monitoring, company engagement.
  - Hedge funds: quantitative analysis, alpha testing, portfolio construction.
- Partner and redistribution segments: index providers, financial data providers, credit rating agencies, stock exchanges, fund administrators, consultancies.
- Client retention is typically high in this category, so expansion revenue from existing clients matters as much as new logos.
- Typical demand generation assets: research reports, case studies, an interview series, a regulatory hub, a mailing list sign-up, and "Request a demo".

### Stack signal to check

If the website's "Request a demo" or mailing list links point to a path like `<tracker subdomain>/l/<account number>/<date>/<code>`, that is the pattern Account Engagement (Pardot) uses for its hosted forms and landing pages, and the current stack is probably Salesforce plus Account Engagement. A "HubSpot project" could then mean adding HubSpot next to Salesforce, or moving marketing automation from Account Engagement to HubSpot. Ask before assuming; if it is a move, use the Account Engagement section of `migration-playbook.md`.

## What this profile means for design

1. **Buying groups, not single leads.** A deal involves several functions: sustainability or ESG, risk, compliance and know-your-customer, procurement or third-party risk, portfolio management, quantitative research, and data or IT teams who integrate feeds. Design for account-level qualification: a buying role property on contacts, an account engagement view on companies, and opportunity contact roles in Salesforce.
2. **Long, considered cycles.** Expect months rather than weeks, with trials, data samples, security and procurement review. Funnel reports need cohort views over 6 to 12 months; a 30-day conversion window will make marketing look ineffective.
3. **Lead sources of very different intent.** Gated research reports bring volume with low intent; webinars sit in the middle; demo requests, data sample requests and "contact sales" are hand-raisers. Score and route them differently, and never let a report download reach a sales representative's queue as if it were a demo request.
4. **Regulation drives demand.** Interest spikes around sustainability reporting, supply-chain due diligence, sanctions and know-your-customer rules. Use a regulatory topic as a content taxonomy and as an interest property for segmentation and scoring.
5. **Existing clients re-enter buying cycles.** Do not use lifecycle stage to track upsell or new modules; once a contact is Customer it stays Customer. Track expansion with opportunity type in Salesforce and expansion campaigns in HubSpot.
6. **European privacy regimes apply.** Audiences in the UK, the European Union and Switzerland mean GDPR, UK GDPR with the Privacy and Electronic Communications Regulations, and the Swiss Federal Act on Data Protection. Store a lawful basis per contact, honour opt-outs across both systems within minutes, and treat some markets (for example Germany) as double opt-in by default. Final legal calls sit with the data protection officer.
7. **Marketing must prove pipeline.** Leadership will ask for marketing-sourced and marketing-influenced pipeline. That only works if the source of the first conversion is stamped onto the Salesforce opportunity at creation (see `reporting.md`).

## Recommended picklists for this profile

Create these as dropdown properties in HubSpot and restricted picklists in Salesforce with identical internal values, so they can map two-way without picklist errors.

| Property | Values |
|---|---|
| Client segment (company) | Bank; Asset manager or owner; Corporate; Insurance provider; Private equity or debt; Hedge fund; Partner or redistributor; Consultancy; Public sector, NGO or academic; Other |
| Buying role (contact) | Sustainability or ESG; Risk; Compliance or know-your-customer; Procurement or supply chain; Portfolio management or research; Quantitative or data science; Data or IT engineering; Executive sponsor; Other |
| Primary use case (contact or deal) | Due diligence and onboarding; Portfolio screening and monitoring; Third-party and supplier risk; Underwriting; Quantitative research; Regulatory reporting; Other |
| Regulatory interest (contact, multiple checkboxes) | Sustainability reporting; Supply-chain due diligence; Sanctions and know-your-customer; Greenwashing and claims; Other |

## Default assumptions when the user has not said

| Area | Assumption |
|---|---|
| HubSpot | Marketing Hub Professional. Recommend Enterprise only where a named need requires it (revenue attribution, custom objects, sandboxes, business units). |
| Salesforce | Sales Cloud Enterprise Edition, one production org, sandbox available. |
| Marketing automation today | Possibly Account Engagement (see signal above). Confirm. |
| System of record | Salesforce owns accounts, opportunities, products, contracts, revenue and record ownership. HubSpot owns marketing engagement, subscriptions and consent, marketing source and attribution, scoring, and lifecycle stage up to the sales handoff. |
| Sales process | Sales development representatives qualify inbound; account executives own opportunities; territories by region (Europe, Middle East and Africa; Americas; Asia Pacific). |
| Volumes | Tens of thousands of contacts and a few thousand accounts. Ask before planning a migration or bulk resync, because volume decides the API budget and the load plan. |
| Team | One marketing operations lead, one Salesforce admin, partner support available. |
