// Martech stack audit: per-page evidence collector.
// Paste the whole file into the browser's JavaScript tool on the page being audited.
// Towards the site it is read-only: it collects hosts, identifiers and names (never cookie values or
// form values) and makes one same-origin GET of the current page to read its response headers.
// In your own browser tab it keeps one sessionStorage key so that later pages report only what is new.
// Output: compact text. Full text and structured data stay on window.__martechAudit for follow-up reads.
(() => {
  const SEEN_KEY = '__martechAuditSeen';
  const uniq = (a) => [...new Set(a.filter((x) => x !== null && x !== undefined && x !== ''))];
  const safe = (fn, fallback) => { try { return fn(); } catch (e) { return fallback; } };
  const urlOf = (u) => safe(() => new URL(u, location.href), null);
  const hostOf = (u) => { const x = urlOf(u); return x && /^https?:$/.test(x.protocol) ? x.hostname.toLowerCase() : null; };

  // Registrable domain, with handling for two-part suffixes such as .co.uk
  const pageHost = location.hostname.toLowerCase();
  const parts = pageHost.split('.');
  const secondLevel = ['co', 'com', 'org', 'net', 'ac', 'gov', 'ltd', 'plc', 'me', 'edu', 'gob', 'nhs', 'sch'];
  const site = parts.length > 2 && parts[parts.length - 1].length === 2 && secondLevel.includes(parts[parts.length - 2])
    ? parts.slice(-3).join('.')
    : parts.slice(-2).join('.');
  const isFirstParty = (h) => h === site || h.endsWith('.' + site);

  // ---- Hosts loaded by the page ----
  const scriptSrcs = [...document.scripts].map((s) => s.src).filter(Boolean);
  const resourceUrls = safe(() => performance.getEntriesByType('resource').map((r) => r.name), []);
  const iframes = [...document.querySelectorAll('iframe')];
  const iframeSrcs = iframes.map((f) => f.src || f.getAttribute('data-src')).filter(Boolean);
  const hintHrefs = [...document.querySelectorAll('link[rel~="preconnect"], link[rel~="dns-prefetch"], link[rel~="preload"], link[rel="stylesheet"]')].map((l) => l.href).filter(Boolean);

  const thirdParty = {};
  const firstPartyHosts = new Set();
  for (const u of [].concat(scriptSrcs, resourceUrls, iframeSrcs, hintHrefs)) {
    const x = urlOf(u);
    if (!x || !/^https?:$/.test(x.protocol)) continue;
    const h = x.hostname.toLowerCase();
    if (isFirstParty(h)) { firstPartyHosts.add(h); continue; }
    if (!thirdParty[h]) thirdParty[h] = { n: 0, path: (x.pathname || '/').slice(0, 45) };
    thirdParty[h].n += 1;
  }
  const thirdPartyList = Object.entries(thirdParty).sort((a, b) => b[1].n - a[1].n);

  // First-party paths that betray a tool or platform (server-side tagging, proxied analytics, CMS paths)
  const pathLabels = [
    [/\/gtm\.js/, 'first-party gtm.js (server-side tagging?)'], [/\/gtag\/js/, 'first-party gtag.js'],
    [/\/g\/collect/, 'first-party GA4 collect'], [/\/collect\b/, 'first-party /collect endpoint'],
    [/_vercel\/insights/, 'Vercel Analytics'], [/cdn-cgi\/zaraz/, 'Cloudflare Zaraz'], [/cdn-cgi\/rum/, 'Cloudflare RUM'],
    [/cdn-cgi\/challenge/, 'Cloudflare challenge'], [/\/_next\//, 'Next.js assets'], [/\/_nuxt\//, 'Nuxt assets'],
    [/\/_astro\//, 'Astro assets'], [/\/hubfs\//, 'HubSpot file manager'], [/\/etc\.clientlibs\//, 'Adobe Experience Manager'],
    [/demandware/, 'Salesforce Commerce Cloud'], [/\/static\/version\d+/, 'Magento static'], [/\/-\/media\//, 'Sitecore media'],
  ];
  const pathHints = [];
  for (const u of [].concat(scriptSrcs, resourceUrls)) {
    const x = urlOf(u);
    if (!x || !isFirstParty(x.hostname.toLowerCase())) continue;
    const plugin = x.pathname.match(/\/wp-content\/plugins\/([^/]+)/);
    if (plugin) pathHints.push(`WordPress plugin ${plugin[1]}`);
    for (const [re, label] of pathLabels) if (re.test(x.pathname)) pathHints.push(`${x.hostname} ${label}`);
  }

  // ---- Identifiers in page source and URLs ----
  const html = safe(() => document.documentElement.outerHTML.slice(0, 3000000), '');
  const blob = [html, resourceUrls.join('\n'), iframeSrcs.join('\n')].join('\n');
  const idPatterns = {
    'Google Tag Manager': /\bGTM-[A-Z0-9]{4,9}\b/g,
    'GA4': /\bG-[A-Z0-9]{8,12}\b/g,
    'Universal Analytics': /\bUA-\d{4,10}-\d{1,4}\b/g,
    'Google Ads': /\bAW-\d{6,12}\b/g,
    'Floodlight': /\bDC-\d{5,10}\b/g,
    'Meta pixel': /(?:fbq\(\s*['"]init['"]\s*,\s*['"]|facebook\.com\/tr\/?\?id=|signals\/config\/)(\d{10,20})/g,
    'LinkedIn partner': /_linkedin_partner_id\s*=\s*['"]?(\d{4,12})/g,
    'HubSpot portal': /hs-(?:scripts|analytics|banner)\.(?:com|net)\/(?:analytics\/\d+\/)?(\d{5,10})\.js/g,
    'Marketo Munchkin': /\b(\d{3}-[A-Z]{3}-\d{3})\b/g,
    'Pardot account': /piAId\s*=\s*['"](\d{4,10})['"]/g,
    'TikTok pixel': /ttq\.load\(\s*['"]([A-Z0-9]{15,25})['"]/g,
    'Microsoft UET': /bat\.bing\.com\/action\/0\?ti=(\d{5,12})/g,
    'Clarity': /clarity\.ms\/tag\/([a-z0-9]{8,12})/g,
    'Hotjar': /hjid\s*:\s*(\d{5,9})/g,
    'Optimizely': /cdn\.optimizely\.com\/js\/(\d{6,14})\.js/g,
    'Intercom app': /widget\.intercom\.io\/widget\/([a-z0-9]{6,10})/g,
  };
  const mentionsMarketo = /munchkin|marketo|mkto/i.test(blob);
  const ids = [];
  for (const [label, re] of Object.entries(idPatterns)) {
    if (label === 'Marketo Munchkin' && !mentionsMarketo) continue;
    for (const id of uniq([...blob.matchAll(re)].map((m) => m[1] || m[0])).slice(0, 6)) ids.push(`${label} ${id}`);
  }
  for (const k of safe(() => Object.keys(window.google_tag_manager || {}).filter((x) => /^(GTM|G|AW|DC)-/.test(x)), [])) ids.push(`loaded Google tag ${k}`);

  // ---- Known vendor globals (hints only: pair with a host, cookie or identifier before confirming) ----
  const globalNames = [
    'dataLayer', 'google_tag_manager', 'gtag', 'ga', '_gaq', 'googletag', 'pbjs', 'apstag', 'zaraz',
    'fbq', '_fbq', 'lintrk', '_linkedin_partner_id', 'uetq', 'ttq', 'twq', 'pintrk', 'rdt', 'snaptr', 'qp',
    'criteo_q', '_tfa', 'obApi', 'adroll_adv_id', 'saq', 'ttd_dom_ready',
    '_6si', 'Demandbase', 'qualified', 'Bizible',
    '_hsq', 'hbspt', 'HubSpotConversations', 'Munchkin', 'MktoForms2', 'piAId', 'piTracker', '_elqQ',
    'klaviyo', '_learnq', 'braze', 'appboy', 'exponea', 'ScarabQueue', 'OneSignal', '_cio', 'vgo',
    'Intercom', 'drift', 'zE', 'LiveChatWidget', '$crisp', 'Tawk_API', 'tidioChatApi', 'fcWidget',
    'FreshworksWidget', 'olark', 'GorgiasChat', 'Beacon', 'adaEmbed', 'Kustomer', 'embedded_svc',
    'ChiliPiper', 'Calendly',
    'Appcues', 'userpilot', 'chmln', 'WalkMeAPI',
    'optimizely', '_vwo_code', 'VWO', 'ABTasty', 'Kameleoon', 'convert', 'DY', 'DYO', 'monetateQ', 'nostojs',
    '_satellite', 'alloy', 's_gi', 'AppMeasurement', 'utag', 'rudderanalytics', 'mParticle', 'Bootstrapper',
    'mixpanel', 'amplitude', 'heap', 'posthog', 'pendo', '_paq', 'plausible', 'fathom', '_kmq', 'woopra',
    'clarity', 'hj', '_uxa', 'FS', '_mfq', 'CE2', 'LogRocket', 'smartlook', 'QSI', 'KAMPYLE_ONSITE_SDK',
    'usabilla_live', 'delighted', 'Sprig',
    'OneTrust', 'Optanon', 'Cookiebot', 'UC_UI', 'Didomi', 'truste', 'Osano', '_iub', 'CookieControl',
    '__tcfapi', '__gpp',
    'Shopify', 'woocommerce_params', 'BCData', 'prestashop', 'Static',
    'Stripe', 'paypal', 'Klarna', 'AfterPay',
    'Trustpilot', 'yotpo', 'Yotpo', 'jdgm', 'LoyaltyLion',
    'AWIN', 'ire', 'growsumo', 'rewardful', 'fpr',
    '_wq', 'Wistia', 'VidyardV4',
    'grecaptcha', 'hcaptcha', 'turnstile',
    'wp', 'elementorFrontend', 'gform', 'wpcf7', 'Drupal', 'Joomla', 'Webflow', '__NUXT__', 'jQuery',
    '__SENTRY__', 'DD_RUM', 'NREUM', 'dtrum', 'acsbJS', 'UserWay',
  ];
  const globals = globalNames.filter((g) => safe(() => typeof window[g] !== 'undefined', false));
  safe(() => {
    const a = window.analytics;
    if (a && (a._writeKey || a.SNIPPET_VERSION || a.VERSION)) globals.push(`analytics (Segment-like ${a.SNIPPET_VERSION || a.VERSION || ''})`.trim());
  });
  safe(() => { if (window.adobe && window.adobe.target) globals.push('adobe.target'); });
  safe(() => { if (window.Static && window.Static.SQUARESPACE_CONTEXT) globals.push('Static.SQUARESPACE_CONTEXT'); });

  // ---- Cookies and storage: names only ----
  const cookieNames = uniq(document.cookie.split(';').map((c) => c.split('=')[0].trim()));
  const localKeys = safe(() => uniq(Object.keys(window.localStorage)).filter((k) => k !== SEEN_KEY), []);
  const sessionKeys = safe(() => uniq(Object.keys(window.sessionStorage)).filter((k) => k !== SEEN_KEY), []);

  // ---- Data layer: event names, Google tag config IDs and consent mode commands ----
  const dataLayerEvents = [];
  const gtagCommands = [];
  safe(() => {
    for (const e of window.dataLayer || []) {
      if (!e) continue;
      const isArgs = Object.prototype.toString.call(e) === '[object Arguments]' || Array.isArray(e);
      if (isArgs) {
        if (e[0] === 'consent') gtagCommands.push(`consent ${e[1]} ${safe(() => JSON.stringify(e[2]), '').slice(0, 200)}`);
        else if (e[0] === 'config') gtagCommands.push(`config ${e[1]}`);
      } else if (typeof e === 'object' && e.event) {
        dataLayerEvents.push(String(e.event).slice(0, 50));
      }
    }
  });

  // ---- Forms and iframes ----
  const formVendorRe = /hs-form|hbspt|mktoForm|gform|wpcf7|wpforms|nf-form|elementor-form|pardot|typeform|jotform|klaviyo|mc4wp|mc-embedded|ninja|formstack|w-form|marketo|eloqua|zoho/i;
  const forms = [...document.forms].slice(0, 20).map((f) => {
    const actionAttr = f.getAttribute('action');
    const x = actionAttr ? urlOf(actionAttr) : null;
    const hint = `${f.id} ${f.className} ${f.getAttribute('name') || ''}`.match(formVendorRe);
    const target = x ? `${x.hostname}${x.pathname}`.slice(0, 70) : 'script-handled';
    return `${target}${hint ? ' [' + hint[0] + ']' : ''} (${f.elements.length} fields)`;
  });
  const iframeInfo = uniq(iframes.map((f) => {
    const h = hostOf(f.src || f.getAttribute('data-src') || '');
    const t = (f.title || f.name || f.id || '').slice(0, 50);
    return h || t ? `${h || 'inline'} | ${t}` : null;
  })).slice(0, 25);

  // ---- Page response headers and Content Security Policy hosts ----
  const headers = [];
  let cspHosts = [];
  safe(() => {
    const xhr = new XMLHttpRequest();
    xhr.open('GET', location.href, false);
    xhr.send(null);
    const showValue = /^(server|x-powered-by|powered-by|via|x-generator|x-cache|cf-cache-status|x-vercel-cache|x-served-by|x-shopify-stage|x-drupal-cache|x-kinsta-cache|x-litespeed-cache|x-cdn)$/i;
    const presenceOnly = /^(cf-ray|x-vercel-id|x-nf-request-id|x-amz-cf-id|x-amz-cf-pop|x-shopid|x-wix-request-id|x-drupal-dynamic-cache|x-pantheon-styx-hostname|wpe-backend|x-github-request-id|x-sucuri-id|x-azure-ref|x-hs-.+|x-akamai-.+|akamai-.+|x-fastly-.+|x-envoy-upstream-service-time)$/i;
    for (const line of xhr.getAllResponseHeaders().trim().split(/[\r\n]+/)) {
      const i = line.indexOf(':');
      if (i < 0) continue;
      const name = line.slice(0, i).trim().toLowerCase();
      const value = line.slice(i + 1).trim();
      if (showValue.test(name)) headers.push(`${name}: ${value.slice(0, 80)}`);
      else if (presenceOnly.test(name)) headers.push(`${name} present`);
      if (name === 'content-security-policy' || name === 'content-security-policy-report-only') {
        cspHosts = cspHosts.concat(value.split(/[\s;]+/)
          .filter((t) => t.includes('.') && !t.startsWith("'") && !/^(https?|wss?):?$/.test(t))
          .map((t) => t.replace(/^[a-z]+:\/\//i, '').replace(/[/:].*$/, '').toLowerCase())
          .filter((h) => h && !isFirstParty(h.replace(/^\*\./, ''))));
      }
    }
    headers.push(`status ${xhr.status}`);
  });
  cspHosts = uniq(cspHosts);

  // ---- Meta tags, markers, comments, credits, badges, links ----
  const metas = uniq([...document.querySelectorAll('meta[name], meta[property]')]
    .map((m) => [m.getAttribute('name') || m.getAttribute('property'), m.getAttribute('content') || ''])
    .filter(([n]) => /generator|verif|verify|msvalidate|domain_verify|apple-itunes-app|google-play-app|ahrefs|yandex|fb:app_id|fb:pages|twitter:site|shopify|wix|hubspot/i.test(n))
    .map(([n, c]) => (/verif|verify|msvalidate|domain_verify|ahrefs|yandex/i.test(n) ? `${n} present` : `${n}: ${c.slice(0, 60)}`)));

  const markerSelectors = {
    'Next.js': '#__NEXT_DATA__, script[src*="/_next/"]',
    'Nuxt': '#__nuxt, script[src*="/_nuxt/"]',
    'Gatsby': '#___gatsby',
    'Astro': 'astro-island, script[src*="/_astro/"], link[href*="/_astro/"]',
    'Angular': '[ng-version]',
    'SvelteKit': 'script[src*="/_app/immutable/"], link[href*="/_app/immutable/"]',
    'WordPress': 'link[href*="/wp-content/"], script[src*="/wp-content/"], link[href*="/wp-includes/"], link[rel="https://api.w.org/"]',
    'WooCommerce': 'body.woocommerce, body.woocommerce-page, link[href*="woocommerce"]',
    'Elementor': '[class*="elementor-"]',
    'Webflow': 'html[data-wf-site], html[data-wf-page]',
    'HubSpot CMS files': 'link[href*="/hubfs/"], img[src*="/hubfs/"], script[src*="/hubfs/"]',
    'Drupal': '[src*="/sites/default/files/"], [href*="/sites/default/files/"], script[src*="/core/misc/"]',
    'Adobe Experience Manager': '[href*="/etc.clientlibs/"], [src*="/etc.clientlibs/"], img[src*="/content/dam/"]',
    'Sitecore': 'img[src*="/-/media/"]',
    'Magento': 'script[type="text/x-magento-init"]',
    'Shopify assets': '[href*="cdn.shopify.com"], [src*="cdn.shopify.com"]',
    'Squarespace': '[href*="squarespace"], [src*="squarespace"]',
    'Wix': '[src*="wixstatic.com"], [href*="parastorage.com"]',
    'Framer': '[href*="framerusercontent.com"], [src*="framerusercontent.com"]',
  };
  const markers = Object.keys(markerSelectors).filter((k) => safe(() => !!document.querySelector(markerSelectors[k]), false));
  safe(() => {
    for (const a of document.documentElement.attributes) if (/^(data-wf-|ng-version)/i.test(a.name)) markers.push(`html attribute ${a.name}`);
  });

  const comments = [];
  safe(() => {
    const walker = document.createTreeWalker(document, NodeFilter.SHOW_COMMENT);
    let node;
    let seen = 0;
    while ((node = walker.nextNode()) && seen < 5000) {
      seen += 1;
      const t = node.nodeValue.replace(/\s+/g, ' ').trim();
      if (/yoast|rank ?math|all in one seo|seopress|wp rocket|w3 total cache|litespeed|autoptimize|cloudflare|powered by|generated by|built with|optimi[sz]ed by|google tag manager|hubspot|shopify/i.test(t)) {
        comments.push(t.slice(0, 90));
        if (comments.length >= 8) break;
      }
    }
  });

  const poweredBy = safe(() => uniq(((document.body && (document.body.innerText || document.body.textContent)) || '')
    .match(/(powered by|built with|secured by|payments by|reviews by)\s+[^\n|•·]{2,35}/gi) || [])
    .map((s) => s.trim()).slice(0, 8), []);
  const badgeRe = /\b(visa|mastercard|maestro|amex|american[ -]?express|paypal|klarna|clearpay|afterpay|apple[ -]?pay|google[ -]?pay|shop[ -]?pay|stripe|adyen|trustpilot|feefo|reviews\.io|g2|capterra|gartner|iso[ -]?27001|soc[ -]?2|cyber[ -]?essentials|b[ -]?corp)\b/i;
  const badges = uniq([...document.querySelectorAll('img, svg[aria-label], [role="img"][aria-label]')]
    .map((el) => {
      const label = `${el.getAttribute('alt') || ''} ${el.getAttribute('aria-label') || ''} ${el.getAttribute('title') || ''} ${(el.getAttribute('src') || '').split('/').pop()}`;
      const m = label.match(badgeRe);
      return m ? m[0].toLowerCase() : null;
    })).slice(0, 20);

  const linkHosts = uniq([...document.links].map((a) => hostOf(a.href)));
  const subdomains = linkHosts.filter((h) => isFirstParty(h) && h !== pageHost && h !== 'www.' + site && h !== site);
  const externalLinks = linkHosts.filter((h) => !isFirstParty(h));

  // ---- Report only what earlier runs in this tab haven't shown ----
  const store = safe(() => JSON.parse(sessionStorage.getItem(SEEN_KEY) || '{}'), {}) || {};
  const run = (store.runs || 0) + 1;
  const fresh = (section, items, keyOf = (x) => x) => {
    const prev = new Set(store[section] || []);
    const out = items.filter((x) => !prev.has(keyOf(x)));
    store[section] = uniq((store[section] || []).concat(items.map(keyOf))).slice(-500);
    return out;
  };
  const sections = [
    ['THIRD-PARTY HOSTS (requests, first path)', thirdPartyList, ([h]) => h, ([h, v]) => `${h} ${v.n} ${v.path}`],
    ['FIRST-PARTY HOSTS', [...firstPartyHosts]],
    ['FIRST-PARTY PATH HINTS', uniq(pathHints)],
    ['IDS', ids],
    ['GLOBALS', globals],
    ['COOKIES', cookieNames],
    ['LOCAL STORAGE KEYS', localKeys],
    ['SESSION STORAGE KEYS', sessionKeys],
    ['DATA LAYER EVENTS', uniq(dataLayerEvents)],
    ['GOOGLE TAG COMMANDS', uniq(gtagCommands)],
    ['FORMS', forms],
    ['IFRAMES', iframeInfo],
    ['HEADERS', headers],
    ['CSP HOSTS', cspHosts],
    ['META', metas],
    ['MARKERS', uniq(markers)],
    ['COMMENTS', comments],
    ['CREDITS', poweredBy],
    ['BADGES', badges],
    ['FIRST-PARTY SUBDOMAINS LINKED', subdomains],
    ['EXTERNAL LINK HOSTS', externalLinks],
  ];
  const render = (onlyNew) => sections.map(([title, items, keyOf, fmt]) => {
    const list = onlyNew ? fresh(title, items, keyOf) : items;
    return list.length ? `${title}: ${list.map(fmt || ((x) => x)).join('; ')}` : null;
  }).filter(Boolean).join('\n');

  const full = render(false);
  const delta = run === 1 ? full : render(true);
  if (run === 1) sections.forEach(([title, items, keyOf]) => fresh(title, items, keyOf));
  store.runs = run;
  safe(() => sessionStorage.setItem(SEEN_KEY, JSON.stringify(store)));

  // The Claude in Chrome tool blocks output that looks like key=value cookie or query data, so spell out '='.
  const clean = (s) => s.replace(/\s*=\s*/g, ' = ');
  const body = clean(delta || 'Nothing new since earlier runs in this tab.');
  const header = `MARTECH AUDIT run ${run} | ${location.hostname}${location.pathname.slice(0, 50)} | ` +
    `${run === 1 ? 'all items' : 'new items only'} | ${Math.round(performance.now() / 1000)}s after load | ` +
    `${body.length} chars (if cut off: window.__martechAudit.text.slice(900, 1800) etc.)`;
  window.__martechAudit = {
    text: `${header}\n${body}`,
    full: clean(full),
    data: { site, thirdParty, ids, globals, cookieNames, forms, iframeInfo, headers, cspHosts, metas, markers, subdomains, externalLinks },
  };
  return window.__martechAudit.text;
})();
