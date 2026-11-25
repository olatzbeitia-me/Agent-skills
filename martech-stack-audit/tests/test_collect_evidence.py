"""Browser tests for scripts/collect_evidence.js.

The collector runs inside a web page, so these tests open small fictional pages in headless Chromium
through Playwright. Every request is answered by the test itself, so nothing reaches the network.
If Playwright or its Chromium browser is not installed, the tests are skipped rather than failed.

Run:          python3 -m unittest discover -s martech-stack-audit/tests
Set up once:  pip install playwright && python3 -m playwright install chromium
"""

import pathlib
import unittest
from urllib.parse import urlsplit

try:
    from playwright.sync_api import sync_playwright
except ImportError:  # pragma: no cover - depends on the machine
    sync_playwright = None

SCRIPT = (pathlib.Path(__file__).resolve().parent.parent / "scripts" / "collect_evidence.js").read_text(encoding="utf-8")
SITE = "https://www.example.co.uk"
GIF = bytes.fromhex("47494638396101000100800000000000ffffff21f90401000000002c00000000010001000002024401003b")

# A site that routes Google measurement through infrastructure it controls, sets its consent default
# only after a Google tag has been configured, and writes a first-party cookie with a value.
FIRST_PARTY_PAGE = """<!doctype html>
<html><head><title>Fixture: first-party tagging</title>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-TEST12345', {server_container_url: 'https://sgtm.example.org'});
  gtag('consent', 'default', {ad_storage: 'denied', analytics_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied'});
  document.cookie = 'testpref=SECRETVALUE42; path=/';
</script>
<script async src="/metrics/?id=GTM-TEST123"></script>
<script async src="https://www.googletagmanager.com/gtm.js?id=GTM-GOOG456"></script>
</head><body>
<img src="/metrics/g/collect?v=2&tid=G-TEST12345" alt="">
<img src="https://sgtm.example.org/g/collect?v=2&tid=G-TEST12345" alt="">
<img src="https://region1.google-analytics.com/g/collect?v=2&tid=G-TEST12345" alt="">
</body></html>"""

# A conventional set-up: consent default first, Google tags from Google's own domains.
STANDARD_PAGE = """<!doctype html>
<html><head><title>Fixture: standard tagging</title>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('consent', 'default', {ad_storage: 'denied', analytics_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied'});
  gtag('js', new Date());
  gtag('config', 'G-TEST67890');
</script>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-TEST67890"></script>
</head><body>
<img src="https://region1.google-analytics.com/g/collect?v=2&tid=G-TEST67890" alt="">
</body></html>"""

PAGES = {"/first-party": FIRST_PARTY_PAGE, "/standard": STANDARD_PAGE}


def handle(route):
    request = route.request
    parts = urlsplit(request.url)
    host = parts.hostname or ""
    if host == "www.example.co.uk" and parts.path in PAGES:
        route.fulfill(status=200, content_type="text/html", body=PAGES[parts.path], headers={"server": "fixture"})
    elif request.resource_type == "script":
        route.fulfill(status=200, content_type="application/javascript", body="")
    else:
        route.fulfill(status=200, content_type="image/gif", body=GIF)


def section(text, title):
    """Return one section line of the collector's output, or '' if the section is absent."""
    for line in text.splitlines():
        if line.startswith(title + ":"):
            return line
    return ""


@unittest.skipIf(sync_playwright is None, "Playwright is not installed")
class CollectEvidenceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.results = {}
        try:
            playwright = sync_playwright().start()
        except Exception as error:  # pragma: no cover - depends on the machine
            raise unittest.SkipTest(f"Playwright could not start: {error}")
        try:
            browser = playwright.chromium.launch()
        except Exception as error:  # pragma: no cover - depends on the machine
            playwright.stop()
            raise unittest.SkipTest(f"Chromium is not available: {error}")
        try:
            for path in PAGES:
                context = browser.new_context()  # fresh session storage, so every page is a first run
                page = context.new_page()
                page.route("**/*", handle)
                page.goto(SITE + path, wait_until="load")
                page.wait_for_timeout(300)
                text = page.evaluate(SCRIPT)
                site = page.evaluate("window.__martechAudit.data.site")
                cls.results[path] = {"text": text, "site": site}
                context.close()
        finally:
            browser.close()
            playwright.stop()

    def first_party(self, title):
        return section(self.results["/first-party"]["text"], title)

    def standard(self, title):
        return section(self.results["/standard"]["text"], title)

    # ---- Existing behaviour kept ----

    def test_first_run_reports_all_items(self):
        header = self.results["/first-party"]["text"].splitlines()[0]
        self.assertTrue(header.startswith("MARTECH AUDIT run 1 | www.example.co.uk/first-party | all items"), header)

    def test_two_part_suffix_gives_registrable_domain(self):
        self.assertEqual(self.results["/first-party"]["site"], "example.co.uk")

    def test_cookie_names_reported_without_values(self):
        self.assertIn("testpref", self.first_party("COOKIES"))
        self.assertNotIn("SECRETVALUE42", self.results["/first-party"]["text"])

    def test_first_party_analytics_hits_still_labelled(self):
        self.assertIn("www.example.co.uk first-party GA4 collect", self.first_party("PATH HINTS"))

    # ---- Google tags and hits routed through infrastructure the site controls ----

    def test_google_tag_from_first_party_path_reported_with_its_id(self):
        self.assertIn(
            "www.example.co.uk Google tag GTM-TEST123 served first-party from /metrics/ (Google tag gateway or server-side tagging)",
            self.first_party("PATH HINTS"),
        )

    def test_analytics_hits_to_non_google_host_reported(self):
        self.assertIn(
            "sgtm.example.org GA4 hits sent to a non-Google host (server-side tagging or another proxy)",
            self.first_party("PATH HINTS"),
        )

    def test_google_own_hosts_not_reported_as_routing(self):
        hints = self.first_party("PATH HINTS")
        self.assertNotIn("GTM-GOOG456", hints)
        self.assertNotIn("google-analytics.com", hints)
        self.assertEqual(self.standard("PATH HINTS"), "")

    def test_server_container_url_reported_as_host(self):
        self.assertIn("config G-TEST12345 server_container_url sgtm.example.org", self.first_party("GOOGLE TAG COMMANDS"))

    def test_plain_config_unchanged(self):
        commands = self.standard("GOOGLE TAG COMMANDS")
        self.assertIn("config G-TEST67890", commands)
        self.assertNotIn("server_container_url", commands)

    # ---- Consent default order ----

    def test_consent_default_after_config_reported(self):
        self.assertIn("consent default queued after config G-TEST12345", self.first_party("GOOGLE TAG COMMANDS"))

    def test_consent_default_before_config_not_reported(self):
        commands = self.standard("GOOGLE TAG COMMANDS")
        self.assertIn("consent default", commands)
        self.assertNotIn("queued after", commands)


if __name__ == "__main__":
    unittest.main()
