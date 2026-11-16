import json
import sys
import tempfile
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
        # Velloway Bank reaches Pursue now on intent data and website visits, with 1 engaged contact
        self.assertEqual([a["account"] for a in r["thin_buying_group"]], ["Velloway Bank"])


BG_CFG = dict(CFG, buying_group={"column": "engaged_contacts", "min_engaged": 2})


def acc_bg(name, engaged, **kwargs):
    row = acc(name, **kwargs)
    row["engaged_contacts"] = engaged
    return row


class BuyingGroupTests(unittest.TestCase):
    def note_of(self, result, name):
        return next(a["buying_group"] for a in result["accounts"] if a["account"] == name)

    def test_single_person_engagement_is_flagged(self):
        r = pr.prioritise([acc_bg("A", "1"), acc_bg("B", "3")], dict(BG_CFG))
        self.assertIn("engagement from 1 person", self.note_of(r, "A"))
        self.assertEqual(self.note_of(r, "B"), "")
        self.assertEqual([a["account"] for a in r["thin_buying_group"]], ["A"])

    def test_flag_does_not_change_tiers(self):
        with_check = pr.prioritise([acc_bg("A", "0"), acc_bg("B", "0", intent="10")], dict(BG_CFG))
        without = pr.prioritise([acc_bg("A", "0"), acc_bg("B", "0", intent="10")], dict(CFG))
        self.assertEqual([(a["account"], a["tier"]) for a in with_check["accounts"]],
                         [(a["account"], a["tier"]) for a in without["accounts"]])

    def test_only_pursue_tiers_are_checked(self):
        # B is Warm up and C is Check fit: thin engagement there is expected, not a warning
        r = pr.prioritise([acc_bg("B", "0", intent="10"), acc_bg("C", "0", industry="Retail", intent="90")],
                          dict(BG_CFG))
        self.assertEqual(r["thin_buying_group"], [])

    def test_over_capacity_accounts_are_checked_too(self):
        cfg = dict(BG_CFG, pursue_now_capacity=1)
        r = pr.prioritise([acc_bg("A", "4", intent="90"), acc_bg("B", "1", intent="80")], cfg)
        self.assertEqual(r["accounts"][1]["tier"], "Pursue next (over capacity)")
        self.assertIn("map the buying group", self.note_of(r, "B"))

    def test_unknown_count_is_flagged_not_assumed(self):
        r = pr.prioritise([acc_bg("A", "")], dict(BG_CFG))
        self.assertIn("unknown", self.note_of(r, "A"))

    def test_check_is_off_unless_configured(self):
        r = pr.prioritise([acc_bg("A", "0")], dict(CFG, buying_group=None))
        self.assertEqual(r["thin_buying_group"], [])
        self.assertNotIn("Buying group check", pr.render_markdown(r, "t"))

    def test_report_lists_flagged_accounts(self):
        r = pr.prioritise([acc_bg("A", "1")], dict(BG_CFG))
        report = pr.render_markdown(r, "t")
        self.assertIn("## Buying group check", report)
        self.assertIn("- **A** (Pursue now): engagement from 1 person", report)

    def test_incomplete_rule_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "icp.json"
            path.write_text(json.dumps(dict(CFG, buying_group={"column": "engaged_contacts"})), encoding="utf-8")
            with self.assertRaises(SystemExit):
                pr.load_config(path)


if __name__ == "__main__":
    unittest.main()
