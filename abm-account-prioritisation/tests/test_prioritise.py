import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts"))
import prioritise as pr  # noqa: E402

CFG = {
    "fit": {
        "industry": {"weight": 50, "values": {"Banking": 1.0, "Insurance": 0.5}, "default": 0.0},
        "employees": {"weight": 50, "bands": [[0, 999, 0.5], [1000, None, 1.0]]},
    },
    "engagement": {"intent_score": {"weight": 100, "max": 100}},
    "thresholds": {"fit": 70, "engagement": 50},
    "pursue_now_capacity": None,
    "open_opportunity_column": "open_opportunity",
}


def acc(name, industry="Banking", employees="5000", intent="80", open_opp="no"):
    return {"account": name, "industry": industry, "employees": employees, "intent_score": intent,
            "open_opportunity": open_opp}


class PrioritiseTests(unittest.TestCase):
    def tier_of(self, result, name):
        return next(a["tier"] for a in result["accounts"] if a["account"] == name)

    def test_four_quadrants(self):
        r = pr.prioritise([acc("A"), acc("B", intent="10"), acc("C", industry="Retail", intent="90"),
                           acc("D", industry="Retail", intent="5")], dict(CFG))
        self.assertEqual(self.tier_of(r, "A"), "Pursue now")
        self.assertEqual(self.tier_of(r, "B"), "Warm up")
        self.assertEqual(self.tier_of(r, "C"), "Check fit")
        self.assertEqual(self.tier_of(r, "D"), "Hold")

    def test_scores(self):
        r = pr.prioritise([acc("A", industry="Insurance", employees="500", intent="150")], dict(CFG))
        a = r["accounts"][0]
        self.assertEqual(a["fit"], 50.0)          # 0.5 x 50 + 0.5 x 50
        self.assertEqual(a["engagement"], 100.0)  # intent capped at max

    def test_open_opportunity_is_kept_out_of_prospecting(self):
        r = pr.prioritise([acc("A", open_opp="Yes")], dict(CFG))
        self.assertEqual(self.tier_of(r, "A"), "In sales cycle")

    def test_capacity_overflow(self):
        cfg = dict(CFG, pursue_now_capacity=2)
        r = pr.prioritise([acc("A", intent="90"), acc("B", intent="80"), acc("C", intent="70")], cfg)
        self.assertEqual(r["counts"]["Pursue now"], 2)
        self.assertEqual(self.tier_of(r, "C"), "Pursue next (over capacity)")

    def test_missing_data_is_reported_not_hidden(self):
        r = pr.prioritise([acc("A", employees="")], dict(CFG))
        self.assertIn("missing employees", r["accounts"][0]["data_issues"])

    def test_example_runs(self):
        ex = HERE.parent / "examples"
        r = pr.prioritise(pr.load_accounts(ex / "accounts.csv"), pr.load_config(ex / "icp.json"))
        self.assertEqual(len(r["accounts"]), 30)
        self.assertLessEqual(r["counts"]["Pursue now"], 4)


if __name__ == "__main__":
    unittest.main()
