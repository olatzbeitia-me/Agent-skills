# Website tracking, forms, domains and redirects

## Contents
1. Inventory: find every Pardot touchpoint on the web
2. Tracking code replacement and cookies
3. Replacing forms and form handlers
4. Domains: tracker domain, landing-page domain, CNAME changes
5. Redirect plan for Pardot URLs
6. Unsubscribe and preference links in emails already sent
7. Order of web changes

---

## 1. Inventory

Pardot is usually embedded in more places than anyone remembers. Build a URL inventory before changing anything.

1. **Pardot side**: query via API version 5 (or export from the UI) every form, form handler, landing page, file, custom redirect and vanity URL, with its full URL and tracker domain. (Certain)
2. **Website side**: crawl every client site and subdomain with a crawler that supports custom source-code search, looking for: the tracker domain hostname, `pi.pardot.com`, `pd.js`, `piAId`, `piCId`, `/l/` paths on the tracker domain, form `action=` attributes pointing at the tracker domain (form handlers), iframes from the tracker domain (embedded forms), and dynamic-content embed scripts.
3. **Off-site**: links in PDFs and decks, partner and event sites, paid ads, social posts, email signatures, QR codes on printed material, other systems' email templates. Search shared drives and the ad platforms for the tracker domain.
4. **Integrations posting to Pardot**: webinar tools, event platforms, chat, enrichment, website plugins, Zapier and any custom code using the Pardot API. Pardot's connector settings and API user activity show most of these. (Certain)

Record each in `assets/pardot-inventory-template.csv` with its replacement and redirect target.

## 2. Tracking code replacement and cookies

- Replace the Pardot tracking snippet with the HubSpot tracking code copied from the portal (Settings → Tracking code). EU-hosted portals load the script from a regional host, so copy it rather than typing it. (Certain; Verify the host in the copied code)
- Install through the tag manager or CMS template so it is on every page, including any external careers or event sites the client wants tracked.
- **Parallel running**: both scripts can run side by side during transition; each sets its own cookies. Remove the Pardot script at cutover, once Pardot forms and dynamic content are gone. (Certain)
- **Cookies change**: Pardot cookies (`visitor_id…`, `lpv…`, `pi_opt_in…`) are replaced by HubSpot's (`__hstc`, `hubspotutk`, `__hssc`, `__hssrc`). Update the cookie policy, the consent management platform's cookie categories and any scripts that read Pardot cookies. (Certain for names in common use; Verify against HubSpot's current cookie list)
- **Consent**: HubSpot has its own cookie banner, or can be controlled by the client's existing consent platform through HubSpot's privacy consent API so that tracking waits for consent. Test that HubSpot does not set tracking cookies before consent where the policy requires prior consent. (Verify integration method with the consent platform in use)
- Visitors' previous anonymous Pardot history does not carry over. Known contacts are re-identified when they click a HubSpot email link or submit a HubSpot form. (Certain)

## 3. Replacing forms and form handlers

**Pardot forms (iframes) → HubSpot forms**

- HubSpot forms embed into the page (not an iframe), so they inherit site styling and are easier to make accessible. (Certain)
- Features to rebuild per form: progressive fields, dependent fields, hidden fields (including UTMs), CAPTCHA or bot protection, consent checkboxes and text tied to subscription types, redirect or thank-you message, notifications, Salesforce campaign association (prefer a workflow — `hubspot-salesforce-integration.md` §10). (Certain; Depends: Professional or above for progressive fields and some logic)
- HubSpot moved to an updated form editor; some options differ between legacy and updated forms. Build new forms in the updated editor unless a needed option is missing. (Verify)
- Kiosk / data entry mode has no direct equivalent (`object-and-field-mapping.md` §6).

**Pardot form handlers (site's own forms) → two options**

| Option | How | Pros | Cons |
|---|---|---|---|
| **Forms API submission** (recommended) | Create a matching HubSpot form; the site's back end or front end posts fields to HubSpot's form submission endpoint with the `hutk` cookie value, page URL and page name | Full attribution (links the submission to the visitor's history), works with any form technology, supports consent fields | Developer work; forms with HubSpot CAPTCHA enabled are not supported by the endpoint; HubSpot does not validate submitted values, so the site must (Certain) |
| **Non-HubSpot forms** (collected forms) | Turn on collected forms; the tracking code captures submissions | No developer work | Form must use `<form>` tags, not be in an iframe, exist at page load; JavaScript-bound submits often fail; **hidden fields are not collected**; sensitive fields block capture; limited control over field mapping (Certain) |

Do not use the Forms API endpoint for collected (non-HubSpot) forms. EU-hosted portals may use a regional API host for form submissions. (Verify in the developer documentation for the portal's region)

## 4. Domains

| Domain role | Pardot today | HubSpot after |
|---|---|---|
| Tracker domain (e.g. `go.`, `info.`) | CNAME to Pardot; serves forms, landing pages, files, redirects, vanity URLs | Repoint to HubSpot at cutover so old Pardot URLs can be redirected (§5) |
| Landing pages | Tracker domain | A subdomain connected to HubSpot — can be the same subdomain once repointed, or a new one |
| Email sending | Domain authenticated for Pardot | Same domain authenticated for HubSpot (`email-deliverability.md`) |
| Email link tracking | Tracker domain | HubSpot's link-tracking domain; branded tracking domain if offered (Verify) |
| Files | Tracker domain | HubSpot file hosting (file URLs cannot be redirected — Certain) |

**Repointing the tracker domain**

- Lower the DNS record's time-to-live a few days before the change so it propagates quickly — and so a rollback propagates quickly. (Certain)
- **Irreversible in effect** once Pardot is decommissioned: the moment the CNAME points to HubSpot, every Pardot form, landing page, file and custom redirect on that host stops working. Have the redirects (§5) and replacement forms live **before** the switch. While Pardot is still licensed, pointing the CNAME back is the rollback.
- HubSpot must provision a security certificate for the connected domain; allow time and test over HTTPS before announcing. (Certain)
- If the tracker domain is also used for things you are not ready to move, use a new subdomain for HubSpot landing pages and repoint the tracker domain later, once only redirect traffic remains.

## 5. Redirect plan for Pardot URLs

- HubSpot URL redirects work only on domains **connected to and hosted in HubSpot**; once the tracker domain is connected, HubSpot can answer requests to old Pardot paths. (Certain)
- Use **standard redirects** for named vanity URLs and high-value assets, and **flexible pattern redirects** (with variables and an optional "match query strings" setting) for families of paths, with a catch-all to a sensible page. (Certain)
- HubSpot **cannot redirect file URLs**; Pardot file links need a redirect from the old Pardot path to wherever the file now lives — that is fine because the old path is on the tracker domain, not a HubSpot file URL. (Certain)
- Build the redirect map as a spreadsheet: old URL → new URL → type → owner → tested date. Prioritise by traffic (Pardot asset reports) and by permanence (print and QR codes first).
- Custom redirects used in live ads and social posts: replace the link at source where possible, as well as redirecting.

## 6. Unsubscribe and preference links in emails already sent

**Compliance.** Emails sent from Pardot in the weeks before cutover carry Pardot unsubscribe and preference-centre links on the tracker domain. Recipients can still click them after cutover. United States commercial email law expects an unsubscribe mechanism to work for at least 30 days after sending, and data protection rules expect objections to marketing to be honoured whenever they are made. (Certain)

- Keep Pardot licensed and the tracker domain pointing at Pardot for at least 30 days after the last Pardot send, **or**
- After repointing, redirect Pardot's unsubscribe and preference-centre paths (capture the exact paths from recent emails) to a HubSpot page that lets the person unsubscribe from all email — a HubSpot form that sets the opt-out, or the subscription preferences page — and monitor it.
- Either way, unsubscribes received in Pardot during the overlap must reach HubSpot: via Salesforce Email Opt Out sync (`hubspot-salesforce-integration.md` §13) and the cutover-delta opt-out import.

## 7. Order of web changes

1. Add HubSpot tracking code alongside Pardot's (with consent handling).
2. Connect a HubSpot landing-page subdomain; build and test new landing pages there.
3. Replace forms and form handlers page by page; each replacement form writes Salesforce campaign membership like its predecessor.
4. Remove Pardot dynamic-content embeds.
5. At cutover: remove the Pardot tracking code; repoint the tracker domain to HubSpot with redirects already configured; test the top 50 Pardot URLs and the unsubscribe paths.
6. Monitor 404s on the old tracker domain for several weeks and add redirects as they appear.
