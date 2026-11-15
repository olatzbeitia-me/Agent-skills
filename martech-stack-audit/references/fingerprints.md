# Fingerprints reference

Signatures for matching what you observe to a tool. Vendors rebrand, move domains and change cookie names, so treat these as leads: the report cites what you actually observed, not this file. If an entry here contradicts what you see, trust the observation, and look the domain up if unsure.

Format per tool: **hosts** (script or request domains), **globals** (window objects), **cookies**, **other** (identifiers, paths, markup).

## Contents
1. Category checklist (for "Not detected" lines)
2. Tag management
3. Web and product analytics
4. Heatmaps, session replay and feedback
5. Advertising pixels
6. Business-to-business intent, visitor identification and account-based marketing
7. Marketing automation, email, SMS and push
8. Chat, conversational marketing and scheduling
9. Popups, on-site messaging and product tours
10. Experimentation and personalisation
11. Site search and recommendations
12. Reviews, ratings and loyalty
13. Affiliate, referral and partner
14. Social integrations
15. Consent management
16. E-commerce platforms
17. Payments, buy now pay later and subscriptions
18. Forms and lead capture
19. Video, interactive demos, webinars and content hubs
20. CMS, site builders and frameworks
21. Hosting, CDN and security (response headers)
22. Monitoring, accessibility and other
23. Help centres, status pages, careers and authentication
24. Tag manager containers
25. Public DNS
26. Renamed and discontinued products
27. Common false positives

---

## 1. Category checklist

Use these subcategories for the "Not detected" lines in the report.

- **Promotion and marketing**: search advertising; paid social; programmatic and retargeting; business-to-business intent and visitor identification; marketing automation and email; SMS and push; social integrations; SEO tools; affiliate and referral; content, video and webinar platforms; landing page builders.
- **Personalisation and engagement**: experimentation (A/B testing); personalisation; recommendations and site search; chat and chatbots; popups and on-site messaging; product tours; reviews and ratings; loyalty.
- **Selling and commerce**: e-commerce platform; payment processing; buy now pay later; subscriptions and billing; booking and scheduling; lead-capture forms and CRM; marketplaces.
- **Analytics and data**: tag management; web analytics; product analytics; heatmaps and session replay; customer data platform; consent management; surveys and feedback.
- **Underlying stack**: CMS or site builder; front-end framework; hosting and content delivery network; security and bot protection; performance and error monitoring; help centre, status page, careers platform; authentication.

## 2. Tag management

- **Google Tag Manager**: hosts `www.googletagmanager.com/gtm.js`; globals `google_tag_manager`, `dataLayer`; other `GTM-XXXXXXX` container ID. `Object.keys(google_tag_manager)` lists loaded container and Google tag IDs.
- **Google tag (gtag.js)**: hosts `www.googletagmanager.com/gtag/js?id=`; global `gtag`; IDs `G-` (Analytics), `AW-` (Ads), `DC-` (Floodlight).
- **Server-side Google Tag Manager**: `gtm.js` or `/g/collect` served from a first-party subdomain or custom path. Vendors behind it are hidden from the browser.
- **Adobe Experience Platform Tags (formerly Launch / DTM)**: hosts `assets.adobedtm.com`; global `_satellite`.
- **Tealium iQ**: hosts `tags.tiqcdn.com`; global `utag`. Tealium EventStream / AudienceStream: `collect.tealiumiq.com`.
- **Segment (Twilio)**: hosts `cdn.segment.com`, `api.segment.io`; global `analytics` (check it has `_writeKey` or `SNIPPET_VERSION`; the name is generic); cookie `ajs_anonymous_id`, `ajs_user_id`.
- **RudderStack**: hosts `cdn.rudderlabs.com`; global `rudderanalytics`.
- **mParticle**: hosts `jssdkcdns.mparticle.com`, `*.mparticle.com`; global `mParticle`; cookies `mprtcl-*`.
- **Ensighten**: hosts `nexus.ensighten.com`; global `Bootstrapper`.
- **Cloudflare Zaraz**: global `zaraz`; path `/cdn-cgi/zaraz/`.

## 3. Web and product analytics

- **Google Analytics 4**: requests to `www.google-analytics.com/g/collect` or `region1.google-analytics.com/g/collect`; cookies `_ga`, `_ga_<ID>`; ID `G-XXXXXXXXXX`.
- **Universal Analytics (discontinued)**: `www.google-analytics.com/analytics.js`, `/collect` (not `/g/collect`); global `ga`; ID `UA-12345-1`. Dead since July 2023; flag as legacy.
- **Adobe Analytics**: hosts `*.omtrdc.net`, `*.2o7.net`, path `/b/ss/`; globals `s_gi`, `AppMeasurement`; cookies `s_cc`, `s_sq`, `AMCV_*` (Experience Cloud ID). Adobe Web SDK: global `alloy`, requests to `edge.adobedc.net`.
- **Matomo**: `matomo.js` or `piwik.js`; global `_paq`; cookies `_pk_id.*`, `_pk_ses.*`.
- **Plausible**: `plausible.io/js/`; global `plausible`.
- **Fathom**: `cdn.usefathom.com`; global `fathom`.
- **Cloudflare Web Analytics**: `static.cloudflareinsights.com/beacon.min.js`.
- **Vercel Web Analytics**: path `/_vercel/insights/script.js`.
- **Mixpanel**: `cdn.mxpnl.com`, `api-js.mixpanel.com`; global `mixpanel`; cookies `mp_*_mixpanel`.
- **Amplitude**: `cdn.amplitude.com`, `api2.amplitude.com`; global `amplitude`; cookies `AMP_*`.
- **Heap**: `cdn.heapanalytics.com`, `heapanalytics.com`; global `heap`; cookies `_hp2_*`.
- **PostHog**: `us.i.posthog.com`, `eu.i.posthog.com`, `*-assets.i.posthog.com`; global `posthog`; cookies `ph_*_posthog`.
- **Pendo**: `cdn.pendo.io`, `app.pendo.io`; global `pendo`; cookies `_pendo_*`.
- **Kissmetrics**: global `_kmq`. **Woopra**: global `woopra`.
- **Adobe Marketo Measure (formerly Bizible), multi-touch attribution**: `cdn.bizible.com`; global `Bizible`; cookie `_biz_uid`.

## 4. Heatmaps, session replay and feedback

- **Microsoft Clarity**: `www.clarity.ms/tag/<ID>`; global `clarity`; cookies `_clck`, `_clsk`.
- **Hotjar (Contentsquare)**: `static.hotjar.com`, `script.hotjar.com`; global `hj`; cookies `_hjSessionUser_*`, `_hjSession_*`; ID `hjid`.
- **Contentsquare**: `t.contentsquare.net`; global `_uxa`.
- **FullStory**: `edge.fullstory.com`, `rs.fullstory.com`; global `FS`; cookie `fs_uid`.
- **Mouseflow**: `cdn.mouseflow.com`; global `_mfq`.
- **Crazy Egg**: `script.crazyegg.com`; global `CE2`.
- **Lucky Orange**: `tools.luckyorange.com`, `settings.luckyorange.net`.
- **Quantum Metric**: `cdn.quantummetric.com`.
- **LogRocket**: `cdn.lr-ingest.io`, `cdn.logrocket.io`; global `LogRocket`.
- **Smartlook**: `web-sdk.smartlook.com`; global `smartlook`.
- **Qualtrics site intercept**: `*.siteintercept.qualtrics.com`; global `QSI`.
- **Medallia Digital (formerly Kampyle)**: `nebula-cdn.kampyle.com`; global `KAMPYLE_ONSITE_SDK`.
- **Usabilla**: global `usabilla_live`. **Delighted**: global `delighted`. **Sprig**: global `Sprig`.

## 5. Advertising pixels

- **Google Ads**: `www.googleadservices.com/pagead/conversion`, `googleads.g.doubleclick.net/pagead/viewthroughconversion` (remarketing); ID `AW-XXXXXXXXX`; cookie `_gcl_au` (conversion linker).
- **Google Campaign Manager 360 / Floodlight**: `*.fls.doubleclick.net`, `ad.doubleclick.net/activity`; ID `DC-XXXXXXX`.
- **Google Ad Manager / publisher ads**: global `googletag` (Google Publisher Tag), `securepubads.g.doubleclick.net`. **Prebid** header bidding: global `pbjs`. **Amazon Publisher Services**: global `apstag`.
- **Meta Pixel**: `connect.facebook.net/*/fbevents.js`, requests to `www.facebook.com/tr`; global `fbq`; cookie `_fbp` (and `_fbc` after an ad click); ID in `fbq('init','<ID>')`.
- **LinkedIn Insight Tag**: `snap.licdn.com/li.lms-analytics/insight.min.js`, `px.ads.linkedin.com`; globals `_linkedin_partner_id`, `lintrk`.
- **Microsoft Advertising UET**: `bat.bing.com/bat.js`, `bat.bing.com/action/0?ti=<ID>`; global `uetq`; cookies `_uetsid`, `_uetvid`.
- **TikTok Pixel**: `analytics.tiktok.com/i18n/pixel/`; global `ttq`; cookie `_ttp`.
- **X (Twitter) Pixel**: `static.ads-twitter.com/uwt.js`, `analytics.twitter.com`, `t.co/i/adsct`; global `twq`.
- **Pinterest Tag**: `s.pinimg.com/ct/core.js`, `ct.pinterest.com`; global `pintrk`; cookie `_pin_unauth`.
- **Reddit Pixel**: `www.redditstatic.com/ads/pixel.js`, `alb.reddit.com`; global `rdt`; cookie `_rdt_uuid`.
- **Snap Pixel**: `sc-static.net/scevent.min.js`, `tr.snapchat.com`; global `snaptr`.
- **Quora Pixel**: `a.quora.com/qevents.js`; global `qp`.
- **Criteo**: `static.criteo.net`, `dynamic.criteo.com`; global `criteo_q`.
- **The Trade Desk**: `js.adsrvr.org`, `insight.adsrvr.org`; global `ttd_dom_ready`.
- **AdRoll**: `s.adroll.com`; global `adroll_adv_id`.
- **StackAdapt**: `tags.srv.stackadapt.com`; global `saq`.
- **Taboola**: `cdn.taboola.com`; global `_tfa`. **Outbrain**: `amplify.outbrain.com`; global `obApi`.
- **Amazon Ads**: `s.amazon-adsystem.com`, `c.amazon-adsystem.com`.
- **Spotify Ad Analytics**: `pixel.byspotify.com`.
- **AppLovin (Axon ads)**: `s.axon.ai`.

## 6. Business-to-business intent, visitor identification and account-based marketing

These reveal which companies visit (reverse IP lookup) or feed account-based advertising.
- **6sense**: `j.6sc.co`, `epsilon.6sense.com`; global `_6si`; cookies `_gd_visitor`, `_gd_session`.
- **Demandbase**: `tag.demandbase.com`, `api.company-target.com`; global `Demandbase`.
- **Clearbit (now HubSpot Breeze Intelligence)**: `tag.clearbitscripts.com`, `x.clearbitjs.com`.
- **ZoomInfo WebSights / FormComplete**: `ws.zoominfo.com`, `js.zi-scripts.com`.
- **Dealfront (formerly Leadfeeder)**: `sc.lfeeder.com/lftracker_v1_*`; cookie `_lfa`.
- **Albacross**: `serve.albacross.com`.
- **Bombora**: `ml314.com`.
- **G2 buyer intent**: `tracking.g2crowd.com`.
- **Qualified (Piper)**: `js.qualified.com`; global `qualified`. Also conversational marketing.
- **Warmly**: `opps-widget.getwarmly.com`.
- **RB2B**: scripts under `b2bjsstore` paths. Verify by searching the host if seen.

## 7. Marketing automation, email, SMS and push

- **HubSpot**: `js.hs-scripts.com/<portal>.js` (loader; also `js-eu1.hs-scripts.com` for EU data centre), `js.hs-analytics.net`, `js.hsforms.net`, `forms.hsforms.com`, `js.hs-banner.com` (HubSpot cookie banner), `js.usemessages.com` (HubSpot chat); globals `_hsq`, `hbspt`, `HubSpotConversations`; cookies `hubspotutk`, `__hstc`, `__hssc`. Portal ID in the loader path.
- **Marketo Engage (Adobe)**: `munchkin.marketo.net`, `*.mktoresp.com`, forms from `//app-*.marketo.com/js/forms2/`; globals `Munchkin`, `MktoForms2`; cookie `_mkto_trk`; ID format `123-ABC-456`.
- **Salesforce Marketing Cloud Account Engagement (Pardot)**: `pi.pardot.com`, `cdn.pardot.com`, form handlers and landing pages on a custom tracker domain with paths `/l/<id>/`; globals `piAId`, `piCId`, `piTracker`; cookies `visitor_id<number>`, `visitor_id<number>-hash`.
- **Oracle Eloqua**: `img.en25.com`, `*.t.eloqua.com`, `elqCfg.min.js`; global `_elqQ`; cookie `ELOQUA`.
- **Salesforce Marketing Cloud Engagement**: `*.igodigital.com` (collect.js), `*.exacttarget.com`; landing pages on `cloud.<domain>` subdomains.
- **Salesforce Personalization / Data Cloud (formerly Evergage, Interaction Studio)**: `cdn.evgnet.com`, `*.evergage.com`.
- **Klaviyo**: `static.klaviyo.com/onsite/js/`; globals `klaviyo`, `_learnq`; cookie `__kla_id`.
- **Mailchimp**: `chimpstatic.com` (connected site script), forms posting to `*.list-manage.com`; form class `mc-embedded-subscribe-form`.
- **Braze (formerly Appboy)**: `js.appboycdn.com`, `sdk.*.braze.com`; globals `braze`, `appboy`.
- **Customer.io**: `assets.customer.io`, `track.customer.io`; global `_cio`.
- **Iterable**: `js.iterable.com`.
- **Bloomreach Engagement (formerly Exponea)**: `api.exponea.com`; global `exponea`.
- **Emarsys (SAP)**: `cdn.scarabresearch.com`; global `ScarabQueue`.
- **Insider**: `*.api.useinsider.com`.
- **ActiveCampaign**: `diffuser-cdn.app-us1.com` (site tracking); global `vgo`.
- **Brevo (formerly Sendinblue)**: `sibautomation.com`, forms on `sibforms.com`.
- **Omnisend**: `omnisnippet1.com`. **Drip**: `tag.getdrip.com`. **Kit (formerly ConvertKit)**: `f.convertkit.com`.
- **Attentive (SMS)**: `cdn.attn.tv`. **Postscript (SMS)**: `sdk.postscript.io`.
- **OneSignal (web push)**: `cdn.onesignal.com`; global `OneSignal`.
- **Zoho SalesIQ / Zoho CRM forms**: `salesiq.zoho.com`, `salesiq.zoho.eu`, `crm.zoho.*` form actions.

## 8. Chat, conversational marketing and scheduling

- **Intercom**: `widget.intercom.io`, `js.intercomcdn.com`; global `Intercom`; cookies `intercom-id-*`, `intercom-session-*`.
- **Drift (Salesloft)**: `js.driftt.com`; global `drift`.
- **Zendesk Messaging / Chat**: `static.zdassets.com/ekr/snippet.js`; global `zE`.
- **LiveChat**: `cdn.livechatinc.com`; global `LiveChatWidget`.
- **Tidio**: `code.tidio.co`; global `tidioChatApi`.
- **Crisp**: `client.crisp.chat`; global `$crisp`.
- **tawk.to**: `embed.tawk.to`; global `Tawk_API`.
- **Freshchat / Freshdesk widget**: `wchat.freshchat.com`; globals `fcWidget`, `FreshworksWidget`.
- **Olark**: `static.olark.com`; global `olark`.
- **Gorgias**: `config.gorgias.chat`; global `GorgiasChat`.
- **Help Scout Beacon**: `beacon-v2.helpscout.net`; global `Beacon`.
- **Ada**: `static.ada.support`; global `adaEmbed`.
- **Kustomer**: `cdn.kustomerapp.com`; global `Kustomer`.
- **Salesforce Embedded Service / Messaging**: `*.my.salesforce-scrt.com`, `service.force.com/embeddedservice`; global `embedded_svc`.
- **Front Chat**: `chat-assets.frontapp.com`.
- **Chili Piper (meeting routing)**: `js.chilipiper.com`; global `ChiliPiper`.
- **Calendly**: `assets.calendly.com`, embeds from `calendly.com`; global `Calendly`.
- **HubSpot Meetings**: iframes from `meetings.hubspot.com` or `meetings-eu1.hubspot.com`.
- **Acuity Scheduling**: `embed.acuityscheduling.com`.
- Hospitality and local bookings seen in the UK: OpenTable (`www.opentable.co.uk` widgets), ResDiary (`*.resdiary.com`), SevenRooms (`*.sevenrooms.com`), Fresha (`*.fresha.com`), Mindbody (`*.mindbodyonline.com`).

## 9. Popups, on-site messaging and product tours

- **OptinMonster**: `a.omappapi.com`. **Privy**: `widget.privy.com`. **Justuno**: `cdn.justuno.com`. **Wisepops**: `loader.wisepops.com`. **Sumo**: `load.sumo.com`. **Hello Bar**: `my.hellobar.com`. **Poptin**: `cdn.popt.in`.
- Klaviyo and HubSpot also deliver popups (see section 7).
- **Appcues**: `fast.appcues.com`; global `Appcues`. **Userpilot**: `js.userpilot.io`; global `userpilot`. **Chameleon**: `fast.chameleon.io`; global `chmln`. **WalkMe**: `cdn.walkme.com`; global `WalkMeAPI`.

## 10. Experimentation and personalisation

- **Optimizely Web**: `cdn.optimizely.com/js/<project>.js`, `logx.optimizely.com`; global `optimizely`.
- **VWO**: `dev.visualwebsiteoptimizer.com`; globals `_vwo_code`, `VWO`; cookies `_vwo_uuid*`.
- **AB Tasty**: `try.abtasty.com`; global `ABTasty`.
- **Convert**: `cdn-4.convertexperiments.com`; global `convert`.
- **Kameleoon**: `*.kameleoon.eu`, `*.kameleoon.io`; global `Kameleoon`.
- **Adobe Target**: `at.js`, `*.tt.omtrdc.net`; global `adobe.target`; cookie `mbox`.
- **Google Optimize (discontinued September 2023)**: `www.googleoptimize.com/optimize.js`. Flag as dead code.
- **Dynamic Yield**: `cdn.dynamicyield.com`, `st.dynamicyield.com`; globals `DY`, `DYO`.
- **Monetate**: `se.monetate.net`; global `monetateQ`.
- **Mutiny**: `*.mutinycdn.com`.
- **Intellimize (now Webflow Optimize)**: `cdn.intellimize.co`.
- **Unbounce (landing pages, Smart Traffic)**: `*.unbounce.com`, `ubembed.com`; pages on `unbouncepages.com`.
- **LaunchDarkly (feature flags)**: `app.launchdarkly.com`, `clientstream.launchdarkly.com`, `events.launchdarkly.com`.
- **Statsig**: `api.statsig.com`, `featuregates.org`.

## 11. Site search and recommendations

- **Algolia**: `*.algolia.net`, `*.algolianet.com`.
- **Coveo**: `platform.cloud.coveo.com`.
- **Constructor**: `*.cnstrc.com`.
- **Nosto**: `connect.nosto.com`; global `nostojs`.
- **Klevu**: `js.klevu.com`.
- Dynamic Yield, Bloomreach and Salesforce Personalization also recommend (sections 7 and 10).

## 12. Reviews, ratings and loyalty

- **Trustpilot**: `widget.trustpilot.com`; global `Trustpilot`.
- **Feefo**: `api.feefo.com`. **Reviews.io**: `widget.reviews.io`.
- **Yotpo**: `staticw2.yotpo.com`, `cdn-widgetsrepository.yotpo.com`; globals `yotpo`, `Yotpo`.
- **Okendo**: `cdn-static.okendo.io`. **Judge.me**: `judge.me`; global `jdgm`. **Stamped**: `cdn1.stamped.io`.
- **Bazaarvoice**: `apps.bazaarvoice.com`. **PowerReviews**: `ui.powerreviews.com`.
- **G2 / Capterra / Gartner Peer Insights badges**: images or widgets from `g2.com`, `capterra.com`, `gartner.com`.
- **Smile.io**: `js.smile.io`. **LoyaltyLion**: `sdk.loyaltylion.net`; global `LoyaltyLion`.

## 13. Affiliate, referral and partner

- **Awin**: `www.dwin1.com`; global `AWIN`.
- **Impact**: `*.impactcdn.com`, tracking links on `*.sjv.io`; global `ire`.
- **CJ (Commission Junction)**: `www.emjcd.com`, links on `www.anrdoezrs.net`, `www.dpbolvw.net`, `www.jdoqocy.com`, `www.kqzyfj.com`, `www.tkqlhce.com`.
- **Rakuten Advertising**: `*.linksynergy.com`.
- **Partnerize**: `prf.hn`.
- **PartnerStack**: `snippet.growsumo.com`; global `growsumo`.
- **Rewardful**: `r.wdfl.co`; global `rewardful`.
- **FirstPromoter**: `cdn.firstpromoter.com`; global `fpr`.
- **Tapfiliate**: `script.tapfiliate.com`.
- **Mention Me**: `tag.mention-me.com`.

## 14. Social integrations

- Social profile links (LinkedIn company page, Instagram, YouTube, TikTok, X, Facebook) from outbound link hosts. Report which networks are linked.
- **Facebook JavaScript SDK** (login, plugins): `connect.facebook.net/*/sdk.js`. Different from the Meta Pixel (`fbevents.js`).
- **Sign in with Google**: `accounts.google.com/gsi/client`.
- **ShareThis**: `platform-api.sharethis.com`. AddThis was discontinued in 2023; flag if present.
- **Embedded social feeds**: Elfsight (`static.elfsight.com`), Curator (`cdn.curator.io`), Juicer (`www.juicer.io`), Instagram or X embeds.

## 15. Consent management

- **OneTrust**: `cdn.cookielaw.org`, `optanon.blob.core.windows.net`; globals `OneTrust`, `Optanon`; cookies `OptanonConsent`, `OptanonAlertBoxClosed`.
- **Cookiebot (Usercentrics)**: `consent.cookiebot.com`; global `Cookiebot`; cookie `CookieConsent`.
- **Usercentrics**: `app.usercentrics.eu`, `web.cmp.usercentrics.eu`; global `UC_UI`.
- **Didomi**: `sdk.privacy-center.org`; global `Didomi`.
- **TrustArc**: `consent.trustarc.com`; global `truste`.
- **Osano**: `cmp.osano.com`; global `Osano`.
- **Termly**: `app.termly.io`. **iubenda**: `cdn.iubenda.com`; global `_iub`. **CookieYes**: `cdn-cookieyes.com`.
- **Civic Cookie Control** (common in the UK public and charity sectors): `cc.cdn.civiccomputing.com`; global `CookieControl`.
- **Quantcast Choice**: `cmp.quantcast.com`. **Sourcepoint**: `cdn.privacy-mgmt.com`.
- **HubSpot cookie banner**: `js.hs-banner.com`; cookies `__hs_cookie_cat_pref`, `__hs_opt_out`.
- **IAB Transparency and Consent Framework**: global `__tcfapi` (any compliant platform); `__gpp` for the Global Privacy Platform.
- **Google Consent Mode**: `gtag('consent','default',…)` and `('consent','update',…)` entries in the data layer, or `gcs=`/`gcd=` parameters on Google requests.

## 16. E-commerce platforms

- **Shopify**: `cdn.shopify.com`, checkout under `/checkouts/` or on `checkout.shopify.com`; global `Shopify`; headers `x-shopid`, `powered-by: Shopify`.
- **WooCommerce**: `/wp-content/plugins/woocommerce/`; body class `woocommerce`; global `woocommerce_params`; `?wc-ajax=` requests.
- **Adobe Commerce (Magento)**: `script[type="text/x-magento-init"]`, `/static/version<number>/frontend/` paths; local storage `mage-cache-storage`.
- **BigCommerce**: `cdn11.bigcommerce.com`; global `BCData`.
- **Salesforce Commerce Cloud**: `/on/demandware.static/`, `/on/demandware.store/`; cookie `dwsid`.
- **Wix**: `static.wixstatic.com`, `static.parastorage.com`; header `x-wix-request-id`.
- **Squarespace**: `static1.squarespace.com`, `assets.squarespace.com`; global `Static` (with `SQUARESPACE_CONTEXT`).
- **Ecwid**: `app.ecwid.com`. **PrestaShop**: global `prestashop`.

## 17. Payments, buy now pay later and subscriptions

- **Stripe**: `js.stripe.com`, `checkout.stripe.com`, `buy.stripe.com`; global `Stripe`; cookie `__stripe_mid`.
- **PayPal**: `www.paypal.com/sdk/js`, `www.paypalobjects.com`; global `paypal`.
- **Adyen**: `checkoutshopper-live.adyen.com`.
- **Braintree (PayPal)**: `js.braintreegateway.com`.
- **Checkout.com**: `cdn.checkout.com` (Frames).
- **Square**: `web.squarecdn.com`.
- **Mollie**: `js.mollie.com`. **GoCardless**: `pay.gocardless.com`.
- **Klarna**: `js.klarna.com`, `x.klarnacdn.net` (on-site messaging); global `Klarna`.
- **Clearpay / Afterpay**: `js.afterpay.com`, `static.afterpay.com`; global `AfterPay`.
- **Google Pay**: `pay.google.com/gp/p/js/pay.js`. **Apple Pay**: visible button; `ApplePaySession` exists in Safari only, so don't treat it as evidence on its own.
- **Chargebee**: `js.chargebee.com`. **Paddle**: `cdn.paddle.com`. **Recurly**: `js.recurly.com`. **Recharge**: `static.rechargecdn.com`. **Zuora hosted pages**: `static.zuora.com`.
- Payment badges in the footer are "likely" on their own (logos get left up); a payment script or checkout hand-off is "confirmed".

## 18. Forms and lead capture

- **HubSpot forms**: `js.hsforms.net`, `forms.hsforms.com`; class `hs-form`, `hbspt-form`.
- **Marketo forms**: id `mktoForm_<n>`; global `MktoForms2`.
- **Pardot form handlers**: forms posting to the tracker domain `/l/<id>/…`, or iframes from it.
- **Salesforce Web-to-Lead / Web-to-Case**: form action `webto.salesforce.com/servlet/servlet.WebToLead`.
- **Typeform**: `embed.typeform.com`. **Jotform**: `form.jotform.com`. **Tally**: `tally.so`. **Formstack**: `*.formstack.com`. **Google Forms**: `docs.google.com/forms`. **Microsoft Forms**: `forms.office.com`.
- **WordPress form plugins**: Gravity Forms (class `gform_wrapper`, global `gform`), Contact Form 7 (class `wpcf7`, global `wpcf7`), WPForms (class `wpforms-form`), Ninja Forms (class `nf-form-cont`), Elementor forms (class `elementor-form`).
- **Bot protection on forms**: Google reCAPTCHA (`www.google.com/recaptcha`, global `grecaptcha`), hCaptcha (`hcaptcha.com`), Cloudflare Turnstile (`challenges.cloudflare.com/turnstile`).

## 19. Video, interactive demos, webinars and content hubs

- **Wistia**: `fast.wistia.com`, `fast.wistia.net`; global `_wq`, `Wistia`. **Vidyard**: `play.vidyard.com`; global `VidyardV4`. **Vimeo**: `player.vimeo.com`. **YouTube**: `www.youtube.com/embed`, `www.youtube-nocookie.com`. **Loom**: `www.loom.com/embed`. **Brightcove**: `players.brightcove.net`. **JW Player**: `cdn.jwplayer.com`.
- **Interactive demos**: Navattic (`capture.navattic.com`, `*.navattic.com`), Storylane (`app.storylane.io`), Arcade (`demo.arcade.software`), Walnut (`app.teamwalnut.com`), Supademo (`app.supademo.com`).
- **Webinars and events**: ON24 (`event.on24.com`), Goldcast (`*.goldcast.io`), Zoom Webinars (`zoom.us/webinar/register`), Livestorm (`app.livestorm.co`), BigMarker (`www.bigmarker.com`), Eventbrite (`www.eventbrite.co.uk` widgets), Cvent (`*.cvent.com`).
- **Content experience**: Uberflip (`*.uberflip.com`), PathFactory (`*.pathfactory.com`), Turtl (`*.turtl.co`).

## 20. CMS, site builders and frameworks

- **WordPress**: `/wp-content/`, `/wp-includes/`, `/wp-json/`; meta generator `WordPress`; global `wp`. SEO plugins announce themselves in HTML comments: Yoast SEO, Rank Math, All in One SEO. Elementor: classes `elementor-*`, global `elementorFrontend`.
- **Webflow**: `html[data-wf-site]`, `html[data-wf-page]`; assets on `cdn.prod.website-files.com` or `assets-global.website-files.com`; global `Webflow`.
- **HubSpot CMS**: assets under `/hubfs/`; meta generator `HubSpot`; pages on `*.hs-sites.com`.
- **Contentful**: `images.ctfassets.net`. **Sanity**: `cdn.sanity.io`. **Storyblok**: `a.storyblok.com`. **Prismic**: `images.prismic.io`. **Contentstack**: `images.contentstack.io`. These are headless, so pair with a framework below.
- **Drupal**: `/sites/default/files/`, `/core/misc/`; meta generator `Drupal`; header `x-generator: Drupal`; global `Drupal`.
- **Adobe Experience Manager**: `/etc.clientlibs/`, `/content/dam/`.
- **Sitecore**: media under `/-/media/`; cookie `SC_ANALYTICS_GLOBAL_COOKIE`.
- **Framer**: `framerusercontent.com`. **Ghost**: meta generator `Ghost`. **Joomla**: global `Joomla`.
- **Next.js**: `#__NEXT_DATA__`, `/_next/static/`. **Nuxt**: `#__nuxt`, `/_nuxt/`, global `__NUXT__`. **Gatsby**: `#___gatsby`. **Astro**: `astro-island`, `/_astro/`. **Angular**: `[ng-version]`. **SvelteKit**: `/_app/immutable/`.

## 21. Hosting, CDN and security (response headers)

- **Cloudflare**: `server: cloudflare`, `cf-ray`; cookie `__cf_bm` (bot management); `/cdn-cgi/` paths.
- **Akamai**: `server: AkamaiGHost`, `x-akamai-*` headers; `akamai-grn`.
- **Fastly**: `x-served-by: cache-*`, `x-fastly-request-id`, `via: 1.1 varnish`.
- **Amazon CloudFront**: `x-amz-cf-id`, `x-amz-cf-pop`, `via: … (CloudFront)`.
- **Vercel**: `server: Vercel`, `x-vercel-id`. **Netlify**: `server: Netlify`, `x-nf-request-id`.
- **Azure Front Door**: `x-azure-ref`. **Google Cloud load balancer**: `via: 1.1 google`.
- **Managed WordPress hosts**: WP Engine (`x-powered-by: WP Engine`, `wpe-backend`), Kinsta (`x-kinsta-cache`), Pantheon (`x-pantheon-styx-hostname`), LiteSpeed (`x-litespeed-cache`).
- **GitHub Pages**: `x-github-request-id`. **Sucuri firewall**: `x-sucuri-id`.
- **AWS WAF bot control**: `*.edge.sdk.awswaf.com` (challenge.js); cookie `aws-waf-token`. **Cloudflare bot management**: cookie `__cf_bm`; `/cdn-cgi/challenge-platform/`.

## 22. Monitoring, accessibility and other

- **Sentry**: `browser.sentry-cdn.com`, `*.ingest.sentry.io`; global `__SENTRY__`.
- **Datadog RUM**: `www.datadoghq-browser-agent.com`, `browser-intake-datadoghq.com` or `.eu`; global `DD_RUM`; cookie `_dd_s`.
- **New Relic browser**: `js-agent.newrelic.com`, `bam.nr-data.net`; global `NREUM`.
- **Dynatrace**: `ruxitagentjs` scripts; global `dtrum`.
- **Accessibility overlays and tools**: UserWay (`cdn.userway.org`), accessiBe (`acsbapp.com`; global `acsbJS`), AudioEye (`wsmcdn.audioeye.com`), Recite Me (`api.reciteme.com`, common in UK public sector).
- **Fonts**: Google Fonts (`fonts.googleapis.com`), Adobe Fonts (`use.typekit.net`).
- **jQuery**: global `jQuery`. Worth noting only as a sign of an older front end.

## 23. Help centres, status pages, careers and authentication

Usually found through outbound links, first-party subdomains or CNAMEs.
- **Help centres**: Zendesk Guide (`*.zendesk.com`, `/hc/en-gb`), Intercom Articles (`intercom.help`), Freshdesk (`*.freshdesk.com`), Help Scout Docs (`*.helpscoutdocs.com`), Document360, ReadMe (`*.readme.io`), GitBook (`*.gitbook.io`).
- **Status pages**: Atlassian Statuspage (`*.statuspage.io`), Instatus, Better Stack.
- **Careers and applicant tracking**: Greenhouse (`boards.greenhouse.io`, `job-boards.greenhouse.io`), Lever (`jobs.lever.co`), Workable (`apply.workable.com`), Ashby (`jobs.ashbyhq.com`), Teamtailor (`*.teamtailor.com`), Personio (`*.jobs.personio.de`, `*.jobs.personio.com`), Workday (`*.myworkdayjobs.com`), SmartRecruiters (`jobs.smartrecruiters.com`), BambooHR (`*.bamboohr.com/careers`), Pinpoint (`*.pinpointhq.com`).
- **Authentication on login pages**: Auth0 (`*.auth0.com`), Okta (`*.okta.com`, `*.oktapreview.com`), Amazon Cognito (`*.amazoncognito.com`), Clerk (`clerk.*`, `*.clerk.accounts.dev`), Firebase Auth (`*.firebaseapp.com`), WorkOS (`*.authkit.app`), Microsoft Entra (`login.microsoftonline.com`).

## 24. Tag manager containers

When you open `gtm.js?id=GTM-…`, search the text for these tag function names (they appear as `"function":"__awct"` and similar):

| Identifier | Tag type |
|---|---|
| `__googtag` | Google tag (newer GA4 / Ads configuration) |
| `__gaawc` | GA4 configuration (older) |
| `__gaawe` | GA4 event |
| `__ua` | Universal Analytics (legacy, dead) |
| `__awct` | Google Ads conversion tracking |
| `__sp` | Google Ads remarketing |
| `__gclidw` | Conversion linker |
| `__flc`, `__fls` | Floodlight counter, Floodlight sales (Campaign Manager 360) |
| `__baut` | Microsoft Advertising UET |
| `__hjtc` | Hotjar tracking code |
| `__html` | Custom HTML: read the surrounding text for the vendor script or domain |
| `__img` | Custom image pixel: read the URL |
| `__pntr` | Pinterest tag |
| `__cvt_…` | Community template: the vendor is usually named in nearby strings |
| `__paused` | A tag switched off in the container: configured once, not live |

Trigger types worth noting for data maturity: `__fsl` (form submission), `__lcl` (link click), `__cl` (all clicks), `__sdl` (scroll depth), `__ytl` (YouTube video), `__evl` (element visibility), `__tl` (timer), `__hl` (history change, single-page apps), `__jel` (JavaScript errors).

Also search the container text for vendor domains from this file (`connect.facebook.net`, `snap.licdn.com`, `analytics.tiktok.com`, `bat.bing.com`, `j.6sc.co` and so on). Anything found only here is "likely": configured, not observed.

## 25. Public DNS

Look up with `https://dns.google/resolve?name=<domain>&type=TXT` (or `type=CNAME` for a subdomain).

**SPF includes** (email senders; rate "likely"):
| Include | Service |
|---|---|
| `_spf.google.com` | Google Workspace |
| `spf.protection.outlook.com` | Microsoft 365 |
| `_spf.salesforce.com` | Salesforce |
| `aspmx.pardot.com` | Salesforce Account Engagement (Pardot) |
| `mktomail.com` | Marketo |
| `*.spf0*.hubspotemail.net` | HubSpot |
| `_spf.en25.com` | Oracle Eloqua |
| `servers.mcsv.net` | Mailchimp |
| `spf.mandrillapp.com` | Mandrill (Mailchimp transactional) |
| `sendgrid.net` | SendGrid |
| `mailgun.org` | Mailgun |
| `amazonses.com` | Amazon SES |
| `spf.mtasv.net` | Postmark |
| `sparkpostmail.com` | SparkPost |
| `spf.sendinblue.com`, `spf.brevo.com` | Brevo |
| `spf.constantcontact.com` | Constant Contact |
| `mail.zendesk.com` | Zendesk |
| `email.freshdesk.com` | Freshdesk |
| `_spf.atlassian.net` | Atlassian (Jira, Confluence) |
| `zoho.eu`, `zoho.com` | Zoho |
| `_netblocks.mimecast.com` | Mimecast (email security) |
| `*.spf.has.pphosted.com` | Proofpoint hosted SPF: hides the real senders behind Proofpoint, so note it as a limit |

**Mail exchangers (MX)**: `aspmx.l.google.com` or `smtp.google.com` (Google Workspace), `*.mail.protection.outlook.com` (Microsoft 365), `*.pphosted.com` (Proofpoint), `*.mimecast.com` (Mimecast).

**DMARC reporting addresses** (who monitors email authentication): `emaildefense.proofpoint.com` (Proofpoint), `dmarcian.com` (dmarcian), `vali.email` (Valimail), `ondmarc.com` (Red Sift OnDMARC), `easydmarc` (EasyDMARC), `dmarc.postmarkapp.com` (Postmark).

**Verification records** (rate "inferred"): `google-site-verification` (Google Search Console), `facebook-domain-verification` (Meta Business), `MS=` (Microsoft 365), `atlassian-domain-verification`, `docusign=`, `apple-domain-verification`, `adobe-idp-site-verification`, `ahrefs-site-verification` (Ahrefs SEO), `yandex-verification`, `canva-site-verification`, `miro-verification`, `openai-domain-verification`, `anthropic-domain-verification`, `_github-challenge-*`. The same verification strings often appear as meta tags on the homepage (`google-site-verification`, `msvalidate.01` for Bing Webmaster Tools, `p:domain_verify` for Pinterest, `facebook-domain-verification`, `ahrefs-site-verification`). SEO tools rarely leave any other trace.

**CNAME targets** for linked subdomains: `*.mktoweb.com` (Marketo landing pages), `go.pardot.com` (Pardot tracker domain), `*.sites.hubspot.net` or `*.hubspot.net` (HubSpot-hosted pages), `unbouncepages.com` (Unbounce), `*.zendesk.com` (Zendesk help centre), `*.statuspage.io` (Statuspage), `shops.myshopify.com` (Shopify), `proxy-ssl.webflow.com` or `cdn.webflow.com` (Webflow), `sendgrid.net` or `mailgun.org` on `email.`/`links.` subdomains (email click tracking), `domains.aftership.com` (AfterShip order tracking pages), `*.queue-it.net` (Queue-it virtual waiting room for sales peaks).

## 26. Renamed and discontinued products

Use the current name, with the former name in brackets where readers may know it better.
- Pardot → Salesforce Marketing Cloud Account Engagement
- Bizible → Adobe Marketo Measure
- Evergage / Interaction Studio → Salesforce Personalization
- Drift → part of Salesloft
- Clearbit → HubSpot (Breeze Intelligence)
- Leadfeeder → Dealfront
- Sendinblue → Brevo
- ConvertKit → Kit
- Appboy → Braze
- Exponea → Bloomreach Engagement
- Twitter → X
- Hotjar and Heap → part of Contentsquare
- Intellimize → Webflow Optimize
- Adobe Launch → Adobe Experience Platform Tags
- Discontinued: Universal Analytics (July 2023), Google Optimize (September 2023), AddThis (2023). Any of these still loading is dead code.

## 27. Common false positives

- `doubleclick.net` requests coming from a YouTube embed are YouTube's, not the site's advertising set-up.
- `stats.g.doubleclick.net` alongside Google Analytics means Google signals or advertising features are on in Analytics; on its own it doesn't prove Google Ads.
- The global `analytics` is used by many libraries; only Segment-like if it has `_writeKey` or `SNIPPET_VERSION`, or loads from `cdn.segment.com`.
- Two-letter globals (`FS`, `DY`, `hj`) can clash with site code. Pair with a host or cookie.
- `connect.facebook.net/*/sdk.js` is the Facebook SDK (login, plugins), not the Meta Pixel.
- Payment and review logos in the footer can be stale artwork. Look for the script or widget before confirming.
- Content Security Policy allow-lists are often copied from templates and rarely pruned: "likely" at best.
- Cookie policies list vendors the site may have stopped using: "likely" at best.
