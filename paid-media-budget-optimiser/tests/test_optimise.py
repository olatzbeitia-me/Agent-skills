import argparse
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts"))
import optimise as op  # noqa: E402


def settings(**overrides):
    base = dict(lookback_weeks=4, max_change=0.30, step=10.0, min_weeks=6, min_variation=0.10, min_r2=0.30,
                waste_weeks=4, reallocate_waste=False, allow_extrapolation=False)
    base.update(overrides)
    return argparse.Namespace(**base)


def exact_rows(a, b, spends):
    return [{"week": f"2026-01-{i + 1:02d}", "spend": s, "conversions": a * s ** b} for i, s in enumerate(spends)]


SPENDS = [800, 1000, 1200, 900, 1100, 1300, 700, 1000]


class OptimiseTests(unittest.TestCase):
    def test_curve_fit_recovers_parameters(self):
        fit = op.fit_curve(exact_rows(0.5, 0.7, SPENDS))
        self.assertAlmostEqual(fit["b"], 0.7, places=6)
        self.assertAlmostEqual(fit["a"], 0.5, places=6)
        self.assertAlmostEqual(fit["r2"], 1.0, places=6)

    def test_marginal_equals_average_without_diminishing_returns(self):
        c = {"a": 0.01, "b": 1.0}
        self.assertAlmostEqual(op.marginal_cost(c, 1000), 100.0)

    def test_marginal_above_average_with_diminishing_returns(self):
        c = {"a": 1.0, "b": 0.5}
        spend = 10000
        average = spend / op.predicted(c, spend)
        self.assertAlmostEqual(op.marginal_cost(c, spend), average / 0.5)

    def test_budget_moves_to_cheaper_next_conversion_and_total_is_kept(self):
        # next conversion: saturated ~£158 vs efficient ~£111 at £1,000 a week
        data = {("P", "saturated"): exact_rows(1.0, 0.4, SPENDS), ("P", "efficient"): exact_rows(0.02, 0.9, SPENDS)}
        r = op.analyse(data, settings())
        by = {c["campaign"]: c for c in r["campaigns"]}
        self.assertLess(by["saturated"]["recommended"], by["saturated"]["current"])
        self.assertGreater(by["efficient"]["recommended"], by["efficient"]["current"])
        self.assertAlmostEqual(r["optimised_budget_now"], r["optimised_budget_after"])
        self.assertGreaterEqual(r["conversions_after"], r["conversions_now"])

    def test_change_limit_respected(self):
        data = {("P", "saturated"): exact_rows(5.0, 0.2, SPENDS), ("P", "efficient"): exact_rows(0.02, 0.95, SPENDS)}
        r = op.analyse(data, settings(max_change=0.10))
        for c in r["campaigns"]:
            self.assertLessEqual(abs(c["recommended"] / c["current"] - 1), 0.10 + 1e-9)

    def test_increase_stops_at_highest_spend_in_history(self):
        # current spend is £1,025 (last 4 weeks); +30% would be £1,332, above the £1,300 the curve has seen
        data = {("P", "saturated"): exact_rows(5.0, 0.2, SPENDS), ("P", "efficient"): exact_rows(0.02, 0.95, SPENDS)}
        r = op.analyse(data, settings())
        by = {c["campaign"]: c for c in r["campaigns"]}
        self.assertLessEqual(by["efficient"]["recommended"], max(SPENDS) + 1e-9)
        self.assertEqual(by["efficient"]["history_edge"], "highest")
        self.assertFalse(by["efficient"]["beyond_history"])
        self.assertAlmostEqual(r["optimised_budget_now"], r["optimised_budget_after"])
        self.assertIn("Stopped at the edge of its history", op.render_markdown(r, "£"))

    def test_cut_stops_at_lowest_spend_in_history(self):
        narrow = [850, 1000, 1150, 900, 1100, 1000, 850, 1150]  # lowest week £850, current £1,025
        data = {("P", "saturated"): exact_rows(5.0, 0.2, narrow), ("P", "efficient"): exact_rows(0.02, 0.95, SPENDS)}
        r = op.analyse(data, settings())
        by = {c["campaign"]: c for c in r["campaigns"]}
        self.assertGreaterEqual(by["saturated"]["recommended"], min(narrow) - 1e-9)
        self.assertEqual(by["saturated"]["history_edge"], "lowest")

    def test_campaign_at_its_highest_spend_is_not_flagged_when_it_would_not_grow(self):
        # the expensive campaign already runs at its highest spend; money should leave it, not join it,
        # so it must not be reported as stopped at the top of its history
        at_peak = [700, 800, 900, 1000, 1400, 1400, 1400, 1400]  # current £1,400, highest week £1,400
        data = {("P", "saturated"): exact_rows(5.0, 0.2, at_peak), ("P", "efficient"): exact_rows(0.02, 0.95, SPENDS)}
        r = op.analyse(data, settings(max_change=0.05, step=100.0))
        by = {c["campaign"]: c for c in r["campaigns"]}
        self.assertEqual(by["saturated"]["hi_limit"], "history")
        self.assertIsNone(by["saturated"]["history_edge"])
        self.assertNotIn("Stopped at the edge of its history", op.render_markdown(r, "£"))

    def test_allow_extrapolation_lifts_the_history_limit_and_flags_it(self):
        data = {("P", "saturated"): exact_rows(5.0, 0.2, SPENDS), ("P", "efficient"): exact_rows(0.02, 0.95, SPENDS)}
        r = op.analyse(data, settings(allow_extrapolation=True))
        by = {c["campaign"]: c for c in r["campaigns"]}
        self.assertGreater(by["efficient"]["recommended"], max(SPENDS))
        self.assertTrue(by["efficient"]["beyond_history"])
        self.assertIsNone(by["efficient"]["history_edge"])
        self.assertIn("Beyond the spend levels in its history", op.render_markdown(r, "£"))

    def test_flat_spend_is_held(self):
        data = {("P", "flat"): exact_rows(0.1, 0.8, [1000] * 8)}
        r = op.analyse(data, settings())
        self.assertEqual(r["campaigns"][0]["status"], "hold")

    def test_no_recent_conversions_is_waste(self):
        rows = exact_rows(0.1, 0.8, SPENDS)
        for row in rows[-4:]:
            row["conversions"] = 0
        r = op.analyse({("P", "dead"): rows}, settings())
        self.assertEqual(r["campaigns"][0]["status"], "waste")

    def test_example_runs(self):
        data = op.load(HERE.parent / "examples" / "weekly-performance.csv")
        r = op.analyse(data, settings(step=25.0))
        statuses = sorted(c["status"] for c in r["campaigns"])
        self.assertEqual(statuses.count("waste"), 1)
        self.assertEqual(statuses.count("hold"), 1)
        for c in r["campaigns"]:
            if c["status"] == "optimise":
                self.assertFalse(c["beyond_history"], c["campaign"])
        report = op.render_markdown(r, "£")
        self.assertIn("## Recommended weekly budgets", report)
        self.assertNotIn("90%", report)


if __name__ == "__main__":
    unittest.main()
