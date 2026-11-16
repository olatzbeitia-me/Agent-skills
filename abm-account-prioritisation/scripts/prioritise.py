#!/usr/bin/env python3
"""Account prioritisation for account-based marketing: score target accounts on fit and engagement, then tier them.

Fit asks "should we want this account?" (industry, size, region, technology and similar firmographics).
Engagement asks "is this account showing interest now?" (intent data, website visits, engaged contacts,
event attendance). Putting the two scores side by side gives four tiers with different plays:

  Pursue now    high fit, high engagement   sales and marketing together, this month
  Warm up       high fit, low engagement    marketing builds awareness before sales calls
  Check fit     low fit, high engagement    interested, but qualify before investing
  Hold          low fit, low engagement     no proactive spend

Accounts with an open opportunity are kept out of prospecting tiers. The "Pursue now" tier is capped at
sales capacity; the overflow is labelled so nobody pretends 40 accounts can get one-to-few attention.

Optionally, a buying group check flags Pursue now and Pursue next accounts whose engagement comes from
fewer people than the configured minimum. Business purchases are decided by groups, so interest from one
person is a lead to map the buying group, not a sign the account is ready for a sales push. The check flags;
it does not change tiers.

Standard library only. Run:  python3 prioritise.py --accounts accounts.csv --config icp.json --out output/tiers
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

TIERS = ["Pursue now", "Pursue next (over capacity)", "Warm up", "Check fit", "Hold", "In sales cycle"]
PLAYS = {
    "Pursue now": "Joint sales and marketing plan per account: map the buying group, personalised outreach "
                  "from the account owner, tailored content or an invitation to a small event, and a weekly "
                  "check on progress.",
    "Pursue next (over capacity)": "Same profile as Pursue now, but beyond what sales can work properly this "
                                   "period. Keep them warm with targeted advertising and promote the strongest "
                                   "when a Pursue now account closes or stalls.",
    "Warm up": "Right accounts, not buying yet. Most accounts are out of the market at any one time, so this "
               "is the long-running programme: steady advertising and content to the whole buying group so the "
               "brand is familiar when they do enter the market. Hand to sales when engagement crosses the "
               "threshold.",
    "Check fit": "Showing interest but outside the ideal profile. Qualify quickly (one call or a short "
                 "form) before spending on them; route to the standard inbound process if they are not a fit.",
    "Hold": "No proactive spend. Leave in general nurture and re-score next period.",
    "In sales cycle": "Already an open opportunity. Support the deal (content for the buying group, "
                      "references, executive involvement) rather than prospecting it.",
}


def load_config(path: Path) -> dict:
    cfg = json.loads(Path(path).read_text(encoding="utf-8"))
    for key in ("fit", "engagement", "thresholds"):
        if key not in cfg:
            raise SystemExit(f"{path}: missing '{key}'")
    cfg.setdefault("pursue_now_capacity", None)
    cfg.setdefault("open_opportunity_column", "open_opportunity")
    cfg.setdefault("buying_group", None)
    bg = cfg["buying_group"]
    if bg is not None and ("column" not in bg or "min_engaged" not in bg):
        raise SystemExit(f"{path}: 'buying_group' needs 'column' and 'min_engaged'")
    return cfg


def load_accounts(path: Path) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        rows = [dict(r) for r in csv.DictReader(f)]
    if not rows:
        raise SystemExit(f"{path}: no accounts")
    if "account" not in rows[0]:
        raise SystemExit(f"{path}: needs an 'account' column")
    return rows


def number(value) -> float | None:
    try:
        return float(str(value).replace(",", "").strip())
    except (TypeError, ValueError):
        return None


def score_criterion(name: str, rule: dict, row: dict, issues: list) -> float:
    """Return a 0-1 score for one criterion. Missing data scores 0 and is reported."""
    column = rule.get("column", name)
    raw = row.get(column, "")
    if raw is None or str(raw).strip() == "":
        issues.append(f"missing {column}")
        return 0.0
    if "values" in rule:  # categorical
        value = str(raw).strip()
        if value in rule["values"]:
            return float(rule["values"][value])
        if rule.get("warn_unknown", False):
            issues.append(f"unrecognised {column} '{value}'")
        return float(rule.get("default", 0.0))
    if "bands" in rule:  # numeric bands: [low, high_or_null, score]
        x = number(raw)
        if x is None:
            issues.append(f"non-numeric {column}")
            return 0.0
        for low, high, s in rule["bands"]:
            if x >= low and (high is None or x <= high):
                return float(s)
        return 0.0
    if "max" in rule:  # numeric, capped and scaled to 0-1
        x = number(raw)
        if x is None:
            issues.append(f"non-numeric {column}")
            return 0.0
        return max(0.0, min(x / float(rule["max"]), 1.0))
    raise SystemExit(f"Criterion '{name}' needs 'values', 'bands' or 'max'")


def score_block(block: dict, row: dict, issues: list) -> tuple[float, dict]:
    total_weight = sum(float(rule["weight"]) for rule in block.values())
    parts = {}
    for name, rule in block.items():
        parts[name] = score_criterion(name, rule, row, issues) * float(rule["weight"])
    score = 100 * sum(parts.values()) / total_weight if total_weight else 0.0
    # share of the maximum available for each criterion, used to explain the score
    shares = {n: parts[n] / float(block[n]["weight"]) for n in parts}
    return score, shares


def truthy(value) -> bool:
    return str(value).strip().lower() in {"yes", "y", "true", "1"}


def explain(fit_shares: dict, eng_shares: dict, cfg: dict) -> str:
    def label(n, block):
        return cfg[block][n].get("label", n.replace("_", " "))
    strong_fit = [label(n, "fit") for n, s in sorted(fit_shares.items(), key=lambda x: -x[1]) if s >= 0.8][:2]
    weak_fit = [label(n, "fit") for n, s in sorted(fit_shares.items(), key=lambda x: x[1]) if s < 0.5][:1]
    top_eng = [label(n, "engagement") for n, s in sorted(eng_shares.items(), key=lambda x: -x[1]) if s >= 0.6][:2]
    bits = []
    if strong_fit:
        bits.append("fits on " + " and ".join(strong_fit))
    if weak_fit:
        bits.append("weaker on " + weak_fit[0])
    bits.append(("engaged via " + " and ".join(top_eng)) if top_eng else "little engagement")
    return "; ".join(bits)


def buying_group_note(row: dict, rule: dict | None) -> str:
    """Return a warning when engagement comes from fewer people than the agreed minimum, else ''."""
    if not rule:
        return ""
    minimum = int(rule["min_engaged"])
    engaged = number(row.get(rule["column"], ""))
    if engaged is None:
        return f"number of engaged people unknown; check before outreach (minimum {minimum})"
    if engaged < minimum:
        n = int(engaged)
        people = "person" if n == 1 else "people"
        return f"engagement from {n} {people}, below the minimum of {minimum}; map the buying group first"
    return ""


def prioritise(accounts: list[dict], cfg: dict) -> dict:
    t_fit, t_eng = cfg["thresholds"]["fit"], cfg["thresholds"]["engagement"]
    bg_rule = cfg.get("buying_group")
    scored = []
    for row in accounts:
        issues: list[str] = []
        fit, fit_shares = score_block(cfg["fit"], row, issues)
        eng, eng_shares = score_block(cfg["engagement"], row, issues)
        if truthy(row.get(cfg["open_opportunity_column"], "")):
            tier = "In sales cycle"
        elif fit >= t_fit and eng >= t_eng:
            tier = "Pursue now"
        elif fit >= t_fit:
            tier = "Warm up"
        elif eng >= t_eng:
            tier = "Check fit"
        else:
            tier = "Hold"
        scored.append({"account": row["account"], "fit": round(fit, 1), "engagement": round(eng, 1),
                       "priority": round((fit + eng) / 2, 1), "tier": tier,
                       "why": explain(fit_shares, eng_shares, cfg), "data_issues": "; ".join(issues),
                       "buying_group": buying_group_note(row, bg_rule) if tier == "Pursue now" else ""})

    cap = cfg.get("pursue_now_capacity")
    pursue = sorted([a for a in scored if a["tier"] == "Pursue now"], key=lambda a: -a["priority"])
    if cap is not None and len(pursue) > cap:
        for a in pursue[cap:]:
            a["tier"] = "Pursue next (over capacity)"

    order = {t: i for i, t in enumerate(TIERS)}
    scored.sort(key=lambda a: (order[a["tier"]], -a["priority"]))
    counts = {t: sum(1 for a in scored if a["tier"] == t) for t in TIERS}
    return {"accounts": scored, "counts": counts, "thresholds": cfg["thresholds"], "capacity": cap,
            "buying_group_rule": bg_rule,
            "issues": [a for a in scored if a["data_issues"]],
            "thin_buying_group": [a for a in scored if a["buying_group"]]}


def render_markdown(r: dict, title: str) -> str:
    lines = [f"# {title}", "",
             f"{len(r['accounts'])} accounts scored. Fit threshold {r['thresholds']['fit']}, engagement threshold "
             f"{r['thresholds']['engagement']}" + (f", Pursue now capped at {r['capacity']} accounts for sales capacity."
                                                   if r["capacity"] is not None else ".")
             + (f" Buying group check: at least {r['buying_group_rule']['min_engaged']} engaged people."
                if r.get("buying_group_rule") else ""), "",
             "## Tiers", "", "| Tier | Accounts | Play |", "|---|---:|---|"]
    for t in TIERS:
        if r["counts"][t]:
            lines.append(f"| {t} | {r['counts'][t]} | {PLAYS[t]} |")
    lines.append("")

    def tier_table(t: str) -> None:
        group = [a for a in r["accounts"] if a["tier"] == t]
        if not group:
            return
        lines.extend([f"## {t}", "", "| Account | Fit | Engagement | Why |", "|---|---:|---:|---|"])
        for a in group:
            lines.append(f"| {a['account']} | {a['fit']:.0f} | {a['engagement']:.0f} | {a['why']} |")
        lines.append("")

    tier_table("Pursue now")
    tier_table("Pursue next (over capacity)")
    if r.get("thin_buying_group"):
        rule = r["buying_group_rule"]
        lines += ["## Buying group check", "",
                  f"Business purchases are decided by groups, not individuals. These accounts score as ready, but "
                  f"the engagement comes from fewer than {rule['min_engaged']} people. Before sales outreach, "
                  f"identify the other roles involved (for example budget holder, user, procurement) and widen "
                  f"engagement to more of the group.", ""]
        for a in r["thin_buying_group"]:
            lines.append(f"- **{a['account']}** ({a['tier']}): {a['buying_group']}")
        lines.append("")
    tier_table("Warm up")
    tier_table("Check fit")
    if r["issues"]:
        lines += ["## Data to fix", "",
                  "Missing values score zero, so these accounts may be ranked too low:", ""]
        for a in r["issues"]:
            lines.append(f"- **{a['account']}**: {a['data_issues']}")
        lines.append("")
    lines += ["## How to read this", "",
              "- Scores are relative to the weights in the configuration, not probabilities. Change the weights "
              "and the order changes; agree them with sales before acting on the list.",
              "- Engagement decays. Re-score at least monthly, and promote or demote accounts on the new scores.",
              "- Most accounts are not buying at any one time, so a long Warm up list is normal. Judge that "
              "programme over quarters, not by this month's pipeline.", ""]
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--accounts", required=True, type=Path, help="CSV with an 'account' column plus scoring columns")
    ap.add_argument("--config", required=True, type=Path, help="JSON scoring configuration (ideal customer profile)")
    ap.add_argument("--out", type=Path, help="Write <out>.md and <out>.csv (otherwise print the report)")
    ap.add_argument("--title", default="Account prioritisation")
    args = ap.parse_args()
    result = prioritise(load_accounts(args.accounts), load_config(args.config))
    report = render_markdown(result, args.title)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.with_suffix(".md").write_text(report, encoding="utf-8")
        with open(args.out.with_suffix(".csv"), "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["account", "tier", "priority", "fit", "engagement", "why",
                                              "buying_group", "data_issues"])
            w.writeheader()
            w.writerows(result["accounts"])
        print(f"Wrote {args.out.with_suffix('.md')} and {args.out.with_suffix('.csv')}")
    else:
        print(report)


if __name__ == "__main__":
    main()
