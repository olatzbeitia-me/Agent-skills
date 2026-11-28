import json
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts"))
import forecast as fc  # noqa: E402

EXAMPLES = HERE.parent / "examples"


def steady_history(months=6, leads=1000):
    rows = []
    for i in range(months):
        rows.append({"month": f"2026-{i + 1:02d}", "leads": leads, "mqls": 300, "sqls": 120,
                     "opportunities": 60, "pipeline_value": 60 * 10000.0})
    return rows


class ForecastTests(unittest.TestCase):
    def test_steady_funnel_projects_exactly(self):
        plan = {"quarter_label": "Q3", "quarter_months": ["2026-07", "2026-08", "2026-09"],
                "pipeline_target": 1_800_000, "planned_leads": {"2026-07": 1000, "2026-08": 1000, "2026-09": 1000},
                "lookback_months": 6, "currency": "£"}
        r = fc.forecast(steady_history(), plan)
        # 3,000 leads x 30% x 40% x 50% x £10,000 = £1.8m, so exactly on target, all scenarios equal
        for name in ("low", "base", "high"):
            self.assertAlmostEqual(r["scenarios"][name]["total"], 1_800_000)
        self.assertAlmostEqual(r["gap_to_target"], 0)
        self.assertEqual(r["levers"], [])
        self.assertEqual(r["warnings"], [])

    def test_gap_levers_close_the_gap(self):
        plan = {"quarter_label": "Q3", "quarter_months": ["2026-07", "2026-08", "2026-09"],
                "pipeline_target": 2_160_000, "planned_leads": {"2026-07": 1000, "2026-08": 1000, "2026-09": 1000},
                "lookback_months": 6, "currency": "£"}
        r = fc.forecast(steady_history(), plan)
        self.assertAlmostEqual(r["gap_to_target"], 360_000)
        for lever in r["levers"]:
            self.assertAlmostEqual(lever["change"], 0.20)
            self.assertFalse(lever["achievable"])  # nothing in a flat history reaches +20%

    def test_actuals_count_towards_quarter(self):
        hist = steady_history(7)
        hist[6]["month"] = "2026-07"  # first quarter month already happened
        plan = {"quarter_label": "Q3", "quarter_months": ["2026-07", "2026-08", "2026-09"],
                "pipeline_target": 1_800_000, "planned_leads": {"2026-08": 1000, "2026-09": 1000},
                "lookback_months": 6, "currency": "£"}
        r = fc.forecast(hist, plan)
        self.assertEqual(r["months_with_actuals"], ["2026-07"])
        self.assertAlmostEqual(r["pipeline_to_date"], 600_000)
        self.assertAlmostEqual(r["scenarios"]["base"]["total"], 1_800_000)

    def test_falling_rate_is_flagged(self):
        hist = steady_history()
        for row in hist[3:]:
            row["sqls"] = 90  # marketing qualified to sales qualified drops from 40% to 30%
            row["opportunities"] = 45
            row["pipeline_value"] = 450_000.0
        plan = {"quarter_label": "Q3", "quarter_months": ["2026-07"], "pipeline_target": 1,
                "planned_leads": {"2026-07": 1000}}
        r = fc.forecast(hist, fc.load_plan(self._write(plan)))
        self.assertIn("mql_to_sql", [w["metric"] for w in r["warnings"]])

    def test_missing_planned_leads_is_an_error(self):
        plan = {"quarter_label": "Q3", "quarter_months": ["2026-07", "2026-08"], "pipeline_target": 1,
                "planned_leads": {"2026-07": 1000}}
        with self.assertRaises(SystemExit):
            fc.forecast(steady_history(), fc.load_plan(self._write(plan)))

    def _timing_case(self, **extra):
        # one strong month (1,500 leads, same rates) makes +20% leads look realistic on volume alone
        hist = steady_history()
        hist[2].update({"leads": 1500, "mqls": 450, "sqls": 180, "opportunities": 90, "pipeline_value": 900_000.0})
        plan = {"quarter_label": "Q3", "quarter_months": ["2026-07", "2026-08", "2026-09"],
                "pipeline_target": 2_160_000, "planned_leads": {"2026-07": 1000, "2026-08": 1000, "2026-09": 1000},
                "lookback_months": 6, "currency": "£", **extra}
        r = fc.forecast(hist, plan)
        return r, next(lv for lv in r["levers"] if lv["lever"] == "leads")

    def test_lead_lever_without_timing_is_unchanged(self):
        r, lead = self._timing_case()
        self.assertIsNone(lead["timing"])
        self.assertAlmostEqual(lead["needed_per_month"], 1200)
        self.assertTrue(lead["achievable"])  # 1,200 a month is below the best month of 1,500
        self.assertIn("Add `lead_to_opportunity_days`", fc.render_markdown(r))

    def test_lead_lever_timing_needs_a_faster_pace(self):
        # quarter ends 30 September; 61 days earlier is 31 July, so the 600 extra leads must all arrive in July
        r, lead = self._timing_case(lead_to_opportunity_days=61)
        t = lead["timing"]
        self.assertEqual(t["cutoff"], "2026-07-31")
        self.assertEqual(t["usable_days"], 31)
        self.assertAlmostEqual(t["extra_leads"], 600)
        self.assertEqual(t["peak_month"], "2026-07")
        self.assertAlmostEqual(t["peak_monthly_pace"], 1600)
        self.assertFalse(lead["achievable"])  # 1,600 a month is above the best month of 1,500
        report = fc.render_markdown(r)
        self.assertIn("a pace of 1,600 a month until 31 July 2026", report)
        self.assertIn("Beyond recent performance", report)

    def test_lead_lever_timing_can_still_be_realistic(self):
        # 31 days: cut-off 30 August, 61 usable days, so about 10 extra leads a day
        _, lead = self._timing_case(lead_to_opportunity_days=31)
        t = lead["timing"]
        self.assertEqual(t["cutoff"], "2026-08-30")
        self.assertEqual(t["usable_days"], 61)
        self.assertAlmostEqual(t["peak_monthly_pace"], 1000 + 600 / 61 * 31)
        self.assertTrue(lead["achievable"])

    def test_lead_lever_too_late(self):
        r, lead = self._timing_case(lead_to_opportunity_days=45, as_of="2026-08-20")
        # cut-off 16 August is before the as-of date, so no extra lead can convert in time
        self.assertTrue(lead["timing"]["too_late"])
        self.assertFalse(lead["achievable"])
        self.assertIn("Too late for this quarter", fc.render_markdown(r))

    def test_invalid_timing_fields_are_errors(self):
        base = {"quarter_label": "Q3", "quarter_months": ["2026-07"], "pipeline_target": 1,
                "planned_leads": {"2026-07": 1000}}
        for bad in ({"lead_to_opportunity_days": -5}, {"lead_to_opportunity_days": "45"},
                    {"as_of": "20/08/2026"}):
            with self.assertRaises(SystemExit):
                fc.load_plan(self._write({**base, **bad}))

    def test_example_runs(self):
        r = fc.forecast(fc.load_history(EXAMPLES / "funnel.csv"), fc.load_plan(EXAMPLES / "plan.json"))
        self.assertGreater(r["gap_to_target"], 0)
        self.assertIn("## What it would take to close the gap", fc.render_markdown(r))

    def _write(self, obj):
        f = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
        json.dump(obj, f)
        f.close()
        return Path(f.name)


if __name__ == "__main__":
    unittest.main()
