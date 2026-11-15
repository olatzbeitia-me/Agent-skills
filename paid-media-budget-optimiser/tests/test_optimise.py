import argparse
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts"))
import optimise as op  # noqa: E402


def settings(**overrides):
    base = dict(lookback_weeks=4, max_change=0.30, step=10.0, min_weeks=6, min_variation=0.10, min_r2=0.30,
                waste_weeks=4, reallocate_waste=False)
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
        self.assertIn("## Recommended weekly budgets", op.render_markdown(r, "£"))


if __name__ == "__main__":
    unittest.main()
