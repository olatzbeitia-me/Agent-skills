// Martech stack audit: site-level checks. Run once per audit, from any page on the site.
// 1. Tag manager containers: fetches each Google Tag Manager container the page loads (and Adobe or Tealium
//    tag libraries, if present) and lists the tag types and vendor domains configured inside.
// 2. Public DNS via dns.google: SPF senders, verification record names, DMARC reporting services,
//    mail exchangers, and CNAME targets of first-party subdomains linked from this page.
// Read-only. Output: compact text, also kept on window.__martechSiteChecks.text for follow-up reads.
// If your JavaScript tool doesn't support top-level await, run it, then read window.__martechSiteChecks.text.
window.__martechSiteChecksPromise = (async () => {
  const uniq = (a) => [...new Set(a.filter((x) => x !== null && x !== undefined && x !== ''))];
  const safe = (fn, fallback) => { try { return fn(); } catch (e) { return fallback; } };
  const hostOf = (u) => safe(() => new URL(u, location.href).hostname.toLowerCase(), null);
  const pageHost = location.hostname.toLowerCase();
  const parts = pageHost.split('.');
  const secondLevel = ['co', 'com', 'org', 'net', 'ac', 'gov', 'ltd', 'plc', 'me', 'edu', 'gob', 'nhs', 'sch'];
  const site = parts.length > 2 && parts[parts.length - 1].length === 2 && secondLevel.includes(parts[parts.length - 2])
    ? parts.slice(-3).join('.')
    : parts.slice(-2).join('.');
  const isFirstParty = (h) => h === site || h.endsWith('.' + site);
  const lines = [];

  // ---- 1. Tag manager containers ----
  // Google's own hosts are built into every container's runtime, so they prove nothing; Google tools are
  // read from the tag types instead.
  const googleHost = /(^|\.)(google\.[a-z.]+|googletagmanager\.com|google-analytics\.com|googleadservices\.com|googlesyndication\.com|doubleclick\.net|gstatic\.com|googleapis\.com|googleusercontent\.com|youtube\.com|ytimg\.com|w3\.org|schema\.org|example\.(com|org)|cct\.google|jquery\.(com|org)|mozilla\.org|whatwg\.org|email\.com)$/;
  // Minified code produces fake "hosts" such as k.d.se; require a registrable label of 3+ characters.
  const plausible = (h) => { const p = h.split('.'); const label = p.length > 2 && p[p.length - 1].length === 2 && ['co', 'com', 'org', 'net'].includes(p[p.length - 2]) ? p[p.length - 3] : p[p.length - 2]; return !!label && label.length >= 3; };
  const vendorHosts = (text) => uniq((text.match(/(?:[a-z0-9-]+\.)+(?:com|net|io|co|org|ai|app|tv|me|eu|uk|de|fr|nl|se|es|it|ly|so|sh|us|link|tech|site|xyz|info|cloud|dev)(?![a-z0-9-])/gi) || [])
    .map((h) => h.toLowerCase())
    .filter((h) => !googleHost.test(h) && !isFirstParty(h) && plausible(h)))
    .slice(0, 80);
  const countFunctions = (text) => {
    const counts = {};
    for (const m of text.matchAll(/"function":"(__[a-zA-Z0-9_]+)"/g)) {
      const k = m[1].startsWith('__cvt_') ? '__cvt_* (community template)' : m[1];
      counts[k] = (counts[k] || 0) + 1;
    }
    return Object.entries(counts).sort((a, b) => b[1] - a[1]).map(([k, n]) => `${k} ${n}`).join(', ');
  };

  const html = safe(() => document.documentElement.outerHTML, '');
  const gtmIds = uniq(safe(() => Object.keys(window.google_tag_manager || {}), []).concat(html.match(/\bGTM-[A-Z0-9]{4,9}\b/g) || []))
    .filter((k) => /^GTM-/.test(k)).slice(0, 5);
  if (!gtmIds.length) lines.push('GTM: no Google Tag Manager container found on this page');
  for (const id of gtmIds) {
    const text = await fetch(`https://www.googletagmanager.com/gtm.js?id=${id}`, { credentials: 'omit' })
      .then((r) => (r.ok ? r.text() : '')).catch(() => '');
    if (!text) { lines.push(`GTM ${id}: could not fetch the container`); continue; }
    const tagsStart = text.indexOf('"tags":[');
    const tagsEnd = text.indexOf('"predicates":[', tagsStart);
    const tagsPart = tagsStart > -1 && tagsEnd > tagsStart ? text.slice(tagsStart, tagsEnd) : '';
    lines.push(`GTM ${id} (${Math.round(text.length / 1024)} KB)`);
    lines.push(`  TAG TYPES: ${tagsPart ? countFunctions(tagsPart) || 'none' : 'could not isolate tags; all functions: ' + countFunctions(text)}`);
    lines.push(`  VENDOR HOSTS IN CONTAINER: ${vendorHosts(text).join(', ') || 'none besides Google'}`);
  }

  const otherLibraries = uniq([...document.scripts].map((s) => s.src).filter((u) => /assets\.adobedtm\.com|tags\.tiqcdn\.com\/utag/.test(u))).slice(0, 3);
  for (const src of otherLibraries) {
    const text = await fetch(src, { credentials: 'omit' }).then((r) => (r.ok ? r.text() : '')).catch(() => '');
    const label = /adobedtm/.test(src) ? 'ADOBE TAGS' : 'TEALIUM';
    lines.push(text
      ? `${label} ${hostOf(src)} (${Math.round(text.length / 1024)} KB) VENDOR HOSTS: ${vendorHosts(text).join(', ') || 'none found'}`
      : `${label}: could not fetch ${hostOf(src)} library (cross-origin rules); search it via the browser instead`);
  }

  // ---- 2. Public DNS ----
  const dns = async (name, type) => {
    const d = await fetch(`https://dns.google/resolve?name=${encodeURIComponent(name)}&type=${type}`, { credentials: 'omit' })
      .then((r) => r.json()).catch(() => null);
    if (!d) return null;
    const typeNo = { TXT: 16, MX: 15, CNAME: 5 }[type];
    return (d.Answer || []).filter((a) => a.type === typeNo).map((a) => String(a.data).replace(/"\s*"/g, '').replace(/"/g, ''));
  };

  const txt = await dns(site, 'TXT');
  if (txt === null) {
    lines.push('DNS: lookup service unreachable from this page');
  } else {
    const spf = txt.filter((t) => /^v\s*=\s*spf1/i.test(t));
    const spfTerms = uniq(spf.flatMap((t) => t.split(/\s+/).filter((x) => /^(include:|redirect=|exists:)/i.test(x)).map((x) => x.replace(/^(include:|redirect=|exists:)/i, ''))));
    lines.push(`SPF SENDERS: ${spfTerms.join(', ') || (spf.length ? 'SPF present, no includes' : 'no SPF record')}`);
    const named = {};
    let unnamed = 0;
    for (const t of txt.filter((x) => !/^v\s*=\s*spf1/i.test(x))) {
      const name = t.split(/[=:]/)[0].trim();
      if (/verif|verify|domain|site|^ms$|^zoom_|^_?github|^apple|^docusign|^atlassian|^stripe|^adobe|^canva|^miro|^slack|^openai|^anthropic|^mixpanel|^figma|^wrike|^jamf|^onetrust/i.test(name) && name.length < 60) {
        const key = name.replace(/[-_](?=[a-z]*\d)[a-z0-9]{5,}$/i, ''); // drop account-specific suffixes like -p52694
        named[key] = (named[key] || 0) + 1;
      } else {
        unnamed += 1;
      }
    }
    lines.push(`VERIFICATION RECORDS: ${Object.entries(named).map(([k, n]) => (n > 1 ? `${k} x${n}` : k)).join(', ') || 'none'}${unnamed ? ` (+${unnamed} other TXT records)` : ''}`);

    const dmarc = await dns(`_dmarc.${site}`, 'TXT');
    const dmarcRecord = (dmarc || []).find((t) => /v\s*=\s*DMARC1/i.test(t));
    const dmarcHosts = dmarcRecord ? uniq((dmarcRecord.match(/mailto:[^,;\s]+/gi) || []).map((m) => m.split('@')[1]).filter(Boolean)) : [];
    const policy = dmarcRecord ? (dmarcRecord.match(/\bp\s*=\s*(\w+)/i) || [])[1] : null;
    lines.push(`DMARC: ${dmarcRecord ? `policy ${policy || '?'}; reports to ${dmarcHosts.join(', ') || 'no reporting address'}` : 'no record'}`);

    const mx = await dns(site, 'MX');
    lines.push(`MAIL EXCHANGERS: ${(mx || []).map((m) => m.split(/\s+/).pop().replace(/\.$/, '')).slice(0, 6).join(', ') || 'none'}`);

    const subdomains = uniq([...document.links].map((a) => hostOf(a.href)).concat([pageHost]))
      .filter((h) => h && isFirstParty(h) && h !== site).slice(0, 12);
    const cnames = [];
    for (const h of subdomains) {
      const c = await dns(h, 'CNAME');
      if (c && c.length) cnames.push(`${h} -> ${c.map((x) => x.replace(/\.$/, '')).join(' -> ')}`);
    }
    lines.push(`CNAMES: ${cnames.join('; ') || `none among ${subdomains.length} linked subdomains`}`);
  }

  const body = lines.join('\n').replace(/\s*=\s*/g, ' = ');
  const text = `SITE CHECKS | ${site} | ${body.length} chars (if cut off: window.__martechSiteChecks.text.slice(900, 1800) etc.)\n${body}`;
  window.__martechSiteChecks = { text };
  return text;
})();
await window.__martechSiteChecksPromise;
