# 2026-11-23: martech-stack-audit

**Date:** 23 November 2026
**Agent:** [martech-stack-audit](../martech-stack-audit/)
**Why this agent:** 5 agents had never been reviewed (`marketing-performance-audit` counts as reviewed today because its `improve/` pull request is open); broken alphabetically, this one comes first.

## What changed

1. **Consent findings read correctly (method and reference).** The skill told the auditor to report any advertising pixel that fired before a consent choice. Google's tags in advanced consent mode load before a choice by design and send measurements without cookies until the visitor agrees, so the old rule could report a correctly built site as tracking before consent. Step 1 of `SKILL.md` now separates Google's cookieless measurements (consent default denied, no `_ga` or `_gcl_au` cookie) from the real finding: cookies set, or other vendors' pixels sending requests, before the choice. It also asks the auditor to record which of Google's four consent types the default sets, for the data maturity summary. `references/fingerprints.md` section 15 explains basic and advanced consent mode, the 2 consent types added in November 2023, why the `gcs` and `gcd` request parameters should be quoted rather than decoded, and Microsoft Advertising's own consent mode for visitors from the European Economic Area, the UK and Switzerland. Section 27 gains the matching false positive.
2. **First-party Google tagging no longer assumed to be server-side tagging (method, reference and code).** The skill said that Google tags served from the site's own domain meant server-side tagging, which hides other vendors. Google tag gateway for advertisers produces the same picture with no server container: a content delivery network forwards a reserved path to Google, and other vendors still load from their own domains. `SKILL.md` step 4 and `references/fingerprints.md` section 2 now describe both set-ups, rate "Google tags served first-party" as confirmed, and call it server-side tagging only on direct evidence.
3. **Collector and tests (code).** `scripts/collect_evidence.js` now:
   - reports a Google tag loaded from the site's own domain by its identifier and path (a gateway path such as `/metrics/?id=GTM-…` was previously missed);
   - reports Google tags or Analytics hits sent to a host that isn't Google's;
   - shows the host of any `server_container_url` in a Google tag `config` command;
   - reports `consent default queued after config <ID>` when the data layer configures a Google tag before setting the consent default.

   The section `FIRST-PARTY PATH HINTS` is renamed `PATH HINTS`, because it now covers non-Google hosts too. The agent had no tests; `tests/test_collect_evidence.py` adds 11, which run the collector on 2 fictional pages in headless Chromium with every request answered locally. 4 check existing behaviour (for example cookie names without values, and two-part domain suffixes such as `.co.uk`); 7 check the new behaviour and guard against false alarms on standard set-ups. Against the previous collector 5 fail (4 missing features, 1 the renamed section); all 11 pass now. The tests skip if Playwright is not installed. The top-level `README.md` explains how to run them and lists tests for this agent.

`SKILL.md` grows from 187 to 194 lines; the description is unchanged (770 characters).

## Why

- Google's consent mode overview describes basic mode (tags blocked until the visitor chooses) and advanced mode (tags load at once, consent denied by default, measurements sent without cookies until consent is granted). An audit that reports every pre-consent Google request as tracking before consent would be wrong about a site that follows Google's own recommended set-up.
- Google's consent troubleshooting guide asks for a default covering at least `ad_storage`, `analytics_storage`, `ad_user_data` and `ad_personalization`, notes the November 2023 update, and lists a default set after tags have run as a common fault. Google Ads Help explains that the 2 newer types are needed for personalised advertising with visitors from the European Economic Area. These give the auditor objective, checkable markers of consent maturity instead of a vague "consent mode present".
- The overview also says the `gcs` and `gcd` parameters encode consent state but that their encoding may change, so the skill quotes them as evidence of consent mode and reads the state from commands and cookies instead of decoding values.
- Microsoft Advertising announced enforcement of consent signals from 5 May 2025, with a consent mode that adjusts its tag's cookie use for visitors from the European Economic Area, the UK and Switzerland. A UK audit should look for it alongside Google's.
- Google's documentation for Google tag gateway for advertisers (updated 6 November 2026) shows the container loading from a reserved first-party path and hits routed to that path, and Google recommends it for the most durable set-up. Google's server-side tagging documentation shows tagging servers on a path, a subdomain or a cloud provider's own domain, configured through `server_container_url`, with the server deciding where data goes next. Together they show a first-party path cannot tell the two apart, and that hits to a non-Google host or a `server_container_url` can.
- Anthropic's skill authoring guidance asks for a concise `SKILL.md`; the detail sits in the existing reference file and `SKILL.md` gains 7 lines.

## Considered and rejected

- **Decoding `gcs` values in the collector** (for example reading a value as "both denied"). Google does not document the encoding and says it may change, so a decoder could silently report the wrong state.
- **A legal note on the UK's changed cookie rules.** The skill deliberately gives no legal opinion; describing what loaded and when is the auditor's job, and the rules were not researched properly in this run.
- **Probing the gateway's health-check path** to tell Google tag gateway from server-side tagging. It would mean requesting a path the site does not link to, which breaks the skill's passive-visitor rule.
- **Searching Tag Manager containers for `server_container_url` in `scripts/site_checks.js`.** Worth doing, but the container format could not be checked in this run (Google Tag Manager was not reachable from the review environment), and guessing the format would risk a silent miss.
- **Reading Microsoft's consent commands from the page.** Once Microsoft's tag loads, its command queue is replaced, so a collector check would be unreliable; the reference file tells the auditor where else to look.
- **Server-side conversion programmes from other platforms** (for example Meta's). They fit the same limit, but no platform documentation was read for them in this run; the general limit about data passed on from a server covers them for now.

## Noticed outside this agent

- The repository `README.md` typo "reussable", flagged in earlier reviews, is fixed in this pull request because the file was being edited anyway.
- `pardot-to-hubspot-migration/SKILL.md` still has a description above Anthropic's 1,024-character limit (flagged on 21 November); it is next but two in the review order.

## Sources

- Google for Developers, *Consent mode overview*: https://developers.google.com/tag-platform/security/concepts/consent-mode
- Google for Developers, *Troubleshoot consent mode with Tag Assistant*: https://developers.google.com/tag-platform/devguides/consent-debugging
- Google Ads Help, *Updates to consent mode for traffic in European Economic Area (EEA)*: https://support.google.com/google-ads/answer/13695607
- Microsoft Advertising blog, *Providing user consent signals on your Microsoft campaigns by May 5, 2025* (Seema Vora and Stephanie Awad, 31 March 2025): https://about.ads.microsoft.com/en/blog/post/march-2025/providing-user-consent-signals-on-your-microsoft-campaigns-by-may-5-2025
- Google for Developers, *What is Google tag gateway for advertisers?*: https://developers.google.com/tag-platform/tag-manager/gateway, and *Set up Google tag gateway for advertisers* (last updated 6 November 2026): https://developers.google.com/tag-platform/tag-manager/gateway/setup-guide
- Google for Developers, *An introduction to server-side tagging*: https://developers.google.com/tag-platform/tag-manager/server-side/intro, and *Custom domain configuration* (last updated 27 June 2025): https://developers.google.com/tag-platform/tag-manager/server-side/custom-domain
- Anthropic, *Skill authoring best practices*: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
