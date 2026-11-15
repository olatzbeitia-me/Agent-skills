# Email deliverability through the move

## Contents
1. What carries over and what does not
2. Authentication: Sender Policy Framework, DomainKeys Identified Mail, DMARC
3. Mailbox-provider sender requirements
4. Shared versus dedicated sending infrastructure
5. Warm-up plan
6. Monitoring
7. Decommissioning Pardot's sending set-up

---

## 1. What carries over

- **Domain reputation travels with the domain.** Mailbox providers judge the From domain and the signing domain (DomainKeys Identified Mail, the `d=` value). If HubSpot sends from the same domain, signed with that domain, the reputation built in Pardot largely carries over. Changing the From domain resets it. Keep the same From domain unless there is a strong reason. (Certain)
- **IP reputation does not travel.** Pardot sends from Salesforce's IP addresses (shared, or a dedicated IP if the client bought one); HubSpot sends from HubSpot's. New IPs mean providers watch behaviour closely in the first weeks. (Certain)
- **Engagement history does not travel.** HubSpot's own features that depend on engagement (for example suppressing unengaged contacts) start without history. (Certain)

## 2. Authentication

Expand the terms once: **Sender Policy Framework (SPF)** lists servers allowed to send for a domain; **DomainKeys Identified Mail (DKIM)** signs messages with a key published in DNS; **Domain-based Message Authentication, Reporting and Conformance (DMARC)** tells receivers what to do when SPF and DKIM do not align with the From domain, and sends reports.

1. In HubSpot: Settings → Domains & URLs → **Email sending domains**; connect each From domain. HubSpot generates the DNS records (DKIM CNAME records, and any SPF or return-path records it asks for). Add exactly what the portal shows — do not copy records from guides. (Certain; Verify record set in the portal)
2. Keep Pardot's records in place during parallel sending: Pardot's SPF include (`include:aspmx.pardot.com`) and its DKIM record (selector shown in Pardot Domain Management). (Certain)
3. Watch the **SPF 10-lookup limit** while both platforms (plus Microsoft 365 or Google Workspace and any other senders) are included. Exceeding it makes SPF fail for everything. Check with an SPF lookup tool after each change. (Certain)
4. Confirm a **DMARC** record exists at least at `p=none` with reporting, and that HubSpot mail aligns through DKIM before moving the policy to `quarantine` or `reject`. Read the aggregate reports to confirm HubSpot traffic passes. (Certain)

## 3. Mailbox-provider sender requirements

Since February 2024 Google and Yahoo require bulk senders (roughly 5,000+ messages a day to their users) to authenticate with SPF and DKIM, publish DMARC, align the From domain, support **one-click unsubscribe** in message headers for marketing mail, honour unsubscribes within two days, and keep reported spam rates low (below 0.3%, ideally under 0.1%). Microsoft introduced similar requirements for Outlook.com consumer mailboxes in 2025. (Certain) HubSpot adds list-unsubscribe headers to marketing email (Verify in a test message's headers); authentication and spam rate remain the client's responsibility.

## 4. Shared versus dedicated sending

- HubSpot Professional sends from shared IP pools; HubSpot assigns pools partly on account behaviour. (Certain)
- A dedicated IP is an Enterprise-level add-on with minimum volume expectations; at B2B volumes a dedicated IP is often worse than a well-run shared pool because it needs steady volume to keep a reputation. If the client has a dedicated IP in Pardot, do not assume it needs one in HubSpot. (Depends; Verify current add-on terms)

## 5. Warm-up plan

The first weeks on HubSpot decide its reputation. Goals: low bounces, low complaints, high engagement.

1. **Clean before you send**: hard bounces and Do Not Email excluded (`data-migration-and-compliance.md` §3–4); long-unengaged contacts not yet marketing contacts.
2. **Week 1**: send only to the most engaged — clicked or submitted a form in the last 90 days — in modest batches.
3. **Weeks 2–4**: widen the window step by step (180 days, 12 months), increasing volume gradually; keep the content high-value (research, events, newsletters people expect).
4. **No "we've moved" blast** to the whole database on day one.
5. Turn on HubSpot's option not to send to unengaged contacts (graymail suppression) for broad sends once there is enough history. (Verify setting name)
6. If Pardot sending continues during a drain period (`automation-rebuild.md` §3), count both platforms' volume to the same recipients — avoid doubling frequency.

Typical health thresholds to hold during warm-up: hard bounce rate under 1–2%, spam complaints well under 0.1%, unsubscribes not spiking. If any breach, pause and narrow the audience. (Certain as practice)

## 6. Monitoring

- Google Postmaster Tools for domain and IP reputation and spam rate; Microsoft SNDS where useful. (Certain)
- DMARC aggregate reports (through a DMARC reporting service) to see that HubSpot mail passes authentication.
- HubSpot email health and bounce reporting per send.
- Seed tests to the client's own mailboxes and colleagues on common corporate filters, because B2B recipients sit behind security gateways that behave differently from consumer mailboxes.

## 7. Decommissioning Pardot's sending set-up

Only after the last Pardot send, the 30-day unsubscribe window (`web-tracking-and-domains.md` §6) and the drain period have passed:

1. Remove `include:aspmx.pardot.com` from SPF.
2. Remove Pardot's DKIM record.
3. Remove Pardot from any allow-lists in the client's own email security gateway.
4. Keep DMARC reporting on to catch anything still sending as the client through Pardot.
