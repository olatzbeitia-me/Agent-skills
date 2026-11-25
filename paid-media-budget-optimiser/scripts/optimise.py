#!/usr/bin/env python3
"""Paid media budget optimiser: move weekly budget to where the next pound buys the most conversions.

Average cost per conversion tells you what you paid for everything so far. Marginal cost per conversion
tells you what the *next* pound will buy, and that is what budget decisions should follow. A brand search
campaign can have the lowest average cost and still be the worst place for extra money, because the
people searching for you are already being reached.

For each campaign this script:
  * fits a diminishing-returns curve, conversions = a x spend^b, to weekly history (b below 1 means each
    extra pound buys a little less than the last);
  * refuses to trust the curve when the history cannot support it (too few weeks, spend that barely
    varied, or a poor fit), and says so;
  * flags spend with no conversions in recent weeks;
  * moves budget in small steps from the campaign with the highest marginal cost to the one with the
    lowest, within a maximum change per campaign, keeping the total budget the same;
  * keeps each recommendation inside the range of weekly spend the curve was fitted on, because beyond
    the lowest and highest spend in the history the curve is extrapolating rather than describing.

Standard library only. Run:  python3 optimise.py --data weekly.csv --out output/plan
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import statistics
from collections import defaultdict
from pathlib import Path


def load(path: Path) -> dict:
    campaigns: dict = defaultdict(list)
    with open(path, newline="", encoding="utf-8") as f:
        for line_no, row in enumerate(csv.DictReader(f), start=2):
            try:
                key = (row["platform"].strip(), row["campaign"].strip())
                campaigns[key].append({"week": row["week"].strip(), "spend": float(row["spend"]),
                                       "conversions": float(row["conversions"])})
            except (KeyError, ValueError) as exc:
                raise SystemExit(f"{path}, line {line_no}: missing or non-numeric value ({exc})")
    for rows in campaigns.values():
        rows.sort(key=lambda r: r["week"])
    if not campaigns:
        raise SystemExit(f"{path}: no rows")
    return campaigns


def fit_curve(rows: list[dict]) -> dict:
    """Least squares on log(conversions) = log(a) + b log(spend), using weeks with spend and conversions."""
    pts = [(math.log(r["spend"]), math.log(r["conversions"])) for r in rows if r["spend"] > 0 and r["conversions"] > 0]
    n = len(pts)
    if n < 3:
        return {"n": n, "a": None, "b": None, "r2": 0.0}
    mx = statistics.mean(x for x, _ in pts)
    my = statistics.mean(y for _, y in pts)
    sxx = sum((x - mx) ** 2 for x, _ in pts)
    if sxx == 0:
        return {"n": n, "a": None, "b": None, "r2": 0.0}
    b = sum((x - mx) * (y - my) for x, y in pts) / sxx
    ln_a = my - b * mx
    ss_tot = sum((y - my) ** 2 for _, y in pts)
    ss_res = sum((y - (ln_a + b * x)) ** 2 for x, y in pts)
    r2 = 1 - ss_res / ss_tot if ss_tot else 0.0
    return {"n": n, "a": math.exp(ln_a), "b": b, "r2": r2}


def predicted(c: dict, spend: float) -> float:
    return c["a"] * spend ** c["b"] if spend > 0 else 0.0


def marginal_cost(c: dict, spend: float) -> float:
    """Cost of one more conversion at this spend level: 1 / (d conversions / d spend)."""
    if spend <= 0:
        return 0.0
    slope = c["a"] * c["b"] * spend ** (c["b"] - 1)
    return 1 / slope if slope > 0 else float("inf")


def analyse(campaigns: dict, args) -> dict:
    results = []
    for (platform, name), rows in campaigns.items():
        recent = rows[-args.lookback_weeks:]
        current = statistics.mean(r["spend"] for r in recent)
        spend_total = sum(r["spend"] for r in rows)
        conv_total = sum(r["conversions"] for r in rows)
        spends = [r["spend"] for r in rows]
        variation = statistics.pstdev(spends) / statistics.mean(spends) if statistics.mean(spends) else 0.0
        curve = fit_curve(rows)
        fitted_spend = [r["spend"] for r in rows if r["spend"] > 0 and r["conversions"] > 0]
        c = {"platform": platform, "campaign": name, "weeks": len(rows), "current": current,
             "spend_total": spend_total, "conversions_total": conv_total,
             "average_cost": spend_total / conv_total if conv_total else None,
             "spend_variation": variation, **curve,
             "observed_min": min(fitted_spend) if fitted_spend else None,
             "observed_max": max(fitted_spend) if fitted_spend else None,
             "status": "optimise", "reasons": []}
        waste_window = rows[-args.waste_weeks:]
        if sum(r["conversions"] for r in waste_window) == 0 and sum(r["spend"] for r in waste_window) > 0:
            c["status"] = "waste"
            c["reasons"].append(f"no conversions in the last {len(waste_window)} weeks")
        else:
            if curve["n"] < args.min_weeks:
                c["reasons"].append(f"only {curve['n']} weeks with conversions (need {args.min_weeks})")
            if variation < args.min_variation:
                c["reasons"].append(f"spend barely varied ({variation:.0%} week to week), so the curve cannot be read")
            if curve["b"] is not None and curve["r2"] < args.min_r2:
                c["reasons"].append(f"poor fit (R squared {curve['r2']:.2f})")
            if curve["b"] is not None and curve["b"] <= 0:
                c["reasons"].append("more spend did not bring more conversions in this history")
            if c["reasons"]:
                c["status"] = "hold"
            else:
                c["b_raw"] = curve["b"]
                c["b"] = min(curve["b"], 1.0)  # no increasing returns at scale
        results.append(c)

    opt = [c for c in results if c["status"] == "optimise"]
    allow_extrapolation = getattr(args, "allow_extrapolation", False)
    for c in opt:
        c["lo"], c["hi"] = c["current"] * (1 - args.max_change), c["current"] * (1 + args.max_change)
        c["lo_limit"] = c["hi_limit"] = "change limit"
        if not allow_extrapolation:
            # the curve is only known between the lowest and highest weekly spend it was fitted on
            floor, ceiling = min(c["observed_min"], c["current"]), max(c["observed_max"], c["current"])
            if floor > c["lo"]:
                c["lo"], c["lo_limit"] = floor, "history"
            if ceiling < c["hi"]:
                c["hi"], c["hi_limit"] = ceiling, "history"
        c["recommended"] = c["current"]
    if args.reallocate_waste:
        released = sum(c["current"] for c in results if c["status"] == "waste")
        if opt and released:
            # share released budget across optimisable campaigns in proportion to current spend, within limits
            base = sum(c["current"] for c in opt)
            for c in opt:
                needed = c["current"] + released * c["current"] / base
                if needed > c["hi"]:
                    c["hi"], c["hi_limit"] = needed, "released budget"
                c["recommended"] += released * c["current"] / base
    step = args.step
    for _ in range(100000):
        donors = [c for c in opt if c["recommended"] - step >= c["lo"]]
        takers = [c for c in opt if c["recommended"] + step <= c["hi"]]
        if not donors or not takers:
            break
        donor = max(donors, key=lambda c: marginal_cost(c, c["recommended"]))
        taker = min(takers, key=lambda c: marginal_cost(c, c["recommended"]))
        if donor is taker or marginal_cost(donor, donor["recommended"]) <= 1.01 * marginal_cost(taker, taker["recommended"]):
            break
        donor["recommended"] -= step
        taker["recommended"] += step

    for c in results:
        if c["status"] == "optimise":
            c["conv_now"] = predicted(c, c["current"])
            c["conv_after"] = predicted(c, c["recommended"])
            c["marginal_now"] = marginal_cost(c, c["current"])
            c["marginal_after"] = marginal_cost(c, c["recommended"])
        else:
            c["recommended"] = 0.0 if (c["status"] == "waste" and args.reallocate_waste) else c["current"]
    for c in opt:
        # stopped by the edge of the history: no room for another step that way, although the marginal costs
        # say the money would still have moved (same 1% tolerance as the optimiser)
        others = [o["marginal_after"] for o in opt if o is not c]
        c["history_edge"] = None
        if others and c["hi_limit"] == "history" and c["recommended"] + step > c["hi"] + 1e-9 \
                and 1.01 * c["marginal_after"] < max(others):
            c["history_edge"] = "highest"
        elif others and c["lo_limit"] == "history" and c["recommended"] - step < c["lo"] - 1e-9 \
                and c["marginal_after"] > 1.01 * min(others):
            c["history_edge"] = "lowest"
        c["beyond_history"] = (c["recommended"] > c["observed_max"] + 0.5
                               or c["recommended"] < c["observed_min"] - 0.5)
    budget = sum(c["current"] for c in opt)
    conv_now = sum(c["conv_now"] for c in opt)
    conv_after = sum(c["conv_after"] for c in opt)
    return {"campaigns": results, "optimised_budget_now": budget,
            "optimised_budget_after": sum(c["recommended"] for c in opt),
            "conversions_now": conv_now, "conversions_after": conv_after,
            "settings": {k: v for k, v in vars(args).items() if k not in ("data", "out")}}


def render_markdown(r: dict, cur: str) -> str:
    def m(x):
        return f"{cur}{x:,.0f}"
    opt = [c for c in r["campaigns"] if c["status"] == "optimise"]
    hold = [c for c in r["campaigns"] if c["status"] == "hold"]
    waste = [c for c in r["campaigns"] if c["status"] == "waste"]
    lines = ["# Paid media budget reallocation", ""]
    if opt and r["conversions_now"]:
        uplift = r["conversions_after"] / r["conversions_now"] - 1
        cpc_now = r["optimised_budget_now"] / r["conversions_now"]
        cpc_after = r["optimised_budget_after"] / r["conversions_after"]
        added = r["optimised_budget_after"] - r["optimised_budget_now"]
        how = (f"moving budget without changing the total ({m(r['optimised_budget_now'])} a week)" if abs(added) < 1
               else f"moving budget and adding the {m(added)} a week released from possible waste")
        lines += [f"Across the {len(opt)} campaigns with readable history, {how} is predicted to lift conversions from "
                  f"{r['conversions_now']:.1f} to {r['conversions_after']:.1f} a week (**{uplift:+.0%}**), "
                  f"taking cost per conversion from {m(cpc_now)} to {m(cpc_after)}.", ""]
    lines += ["## Recommended weekly budgets", "",
              "| Platform | Campaign | Now | Recommended | Change | Average cost per conversion | Cost of the next conversion: now → after |",
              "|---|---|---:|---:|---:|---:|---|"]
    for c in sorted(opt, key=lambda c: c["recommended"] / c["current"] - 1, reverse=True):
        change = c["recommended"] / c["current"] - 1
        lines.append(f"| {c['platform']} | {c['campaign']} | {m(c['current'])} | {m(c['recommended'])} | "
                     f"{change:+.0%} | {m(c['average_cost'])} | {m(c['marginal_now'])} → {m(c['marginal_after'])} |")
    extrapolating = r["settings"].get("allow_extrapolation", False)
    lines += ["", "The last column is the one that matters: budget moves from where the next conversion is most "
              "expensive to where it is cheapest, until the two meet or a campaign reaches its limits "
              f"({r['settings']['max_change']:.0%} up or down"
              + (", and no further than the lowest or highest weekly spend in its history)." if not extrapolating
                 else ")."), ""]
    edge = [c for c in opt if c.get("history_edge")]
    if edge:
        lines += ["**Stopped at the edge of its history.** Beyond the lowest and highest weekly spend a campaign has "
                  "actually run at, the curve has no weeks to learn from, so a prediction there would be a guess:", ""]
        for c in edge:
            bound = c["observed_max"] if c["history_edge"] == "highest" else c["observed_min"]
            lines.append(f"- **{c['platform']}: {c['campaign']}** stopped at {m(c['recommended'])} a week; the "
                         f"{c['history_edge']} weekly spend in its history is {m(bound)}.")
        lines += ["", "To learn whether a bigger move would pay, test a step past that edge for 2 weeks, keeping "
                  "everything else fixed, then rerun with the new weeks added.", ""]
    beyond = [c for c in opt if c.get("beyond_history")]
    if beyond:
        lines += ["**Beyond the spend levels in its history.** The curve has no weeks to learn from at this level, so "
                  "the prediction is a guess rather than an estimate; treat the move as a test:", ""]
        for c in beyond:
            lines.append(f"- **{c['platform']}: {c['campaign']}** at {m(c['recommended'])} a week (history: "
                         f"{m(c['observed_min'])} to {m(c['observed_max'])}).")
        lines.append("")
    lowest_avg = min(opt, key=lambda c: c["average_cost"]) if opt else None
    if lowest_avg and lowest_avg["recommended"] < lowest_avg["current"] * 1.01:
        lines += [f"Note **{lowest_avg['campaign']}**: it has the lowest average cost ({m(lowest_avg['average_cost'])}) "
                  f"but its next conversion costs {m(lowest_avg['marginal_now'])}, so it is not where extra money "
                  "should go. Average cost hides diminishing returns.", ""]
    for c in opt:
        if "brand" in c["campaign"].lower() and c["recommended"] > c["current"] * 1.05:
            lines += [f"Check before increasing **{c['platform']}: {c['campaign']}**: brand search is limited by how "
                      "many people search for you. Look at Search lost impression share (budget): how often the ads "
                      "were not shown because the budget was too low. If it is close to zero, budget is not what "
                      "holds this campaign back, so the extra conversions the curve predicts are unlikely to appear, "
                      "and the curve cannot see that.", ""]
    if hold:
        lines += ["## Held at current budget", "",
                  "The history cannot support a reliable recommendation for these campaigns:", ""]
        for c in hold:
            lines.append(f"- **{c['platform']}: {c['campaign']}** ({m(c['current'])} a week): {'; '.join(c['reasons'])}.")
        lines += ["", "To make them readable, run a structured spend test: change the budget by about 20% for "
                  "2 weeks, then 20% the other way for 2 weeks, keeping everything else fixed.", ""]
    if waste:
        lines += ["## Possible waste", ""]
        for c in waste:
            lines.append(f"- **{c['platform']}: {c['campaign']}** ({m(c['current'])} a week): {'; '.join(c['reasons'])}. "
                         "Check conversion tracking first; if tracking is sound, pause or rebuild it.")
        lines.append("")
    lines += ["## Before acting", "",
              "- Move budget in 2 steps and compare actual results with the prediction before taking the second. "
              "Judge each step over 2 weeks or 2 conversion cycles, whichever is longer, allowing for conversions "
              "that are reported late.",
              "- The curves describe the past. Seasonality, new creative, bidding changes or a competitor's push "
              "can all change them.",
              "- Conversions are only comparable if every platform counts them the same way, with similar "
              "attribution windows. If one platform counts view-throughs and another does not, fix that first.", ""]
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--data", required=True, type=Path, help="CSV: week,platform,campaign,spend,conversions")
    ap.add_argument("--out", type=Path, help="Write <out>.md and <out>.json (otherwise print the report)")
    ap.add_argument("--currency", default="£")
    ap.add_argument("--lookback-weeks", type=int, default=4, help="Weeks averaged for current weekly spend (default 4)")
    ap.add_argument("--max-change", type=float, default=0.30, help="Largest change per campaign, as a share (default 0.30)")
    ap.add_argument("--step", type=float, default=25.0, help="Budget moved per iteration (default 25)")
    ap.add_argument("--min-weeks", type=int, default=6, help="Weeks with conversions needed to fit a curve (default 6)")
    ap.add_argument("--min-variation", type=float, default=0.10, help="Minimum week-to-week spend variation (default 0.10)")
    ap.add_argument("--min-r2", type=float, default=0.30, help="Minimum fit quality, R squared (default 0.30)")
    ap.add_argument("--waste-weeks", type=int, default=4, help="Weeks without conversions that count as waste (default 4)")
    ap.add_argument("--reallocate-waste", action="store_true", help="Move budget from waste campaigns into the plan")
    ap.add_argument("--allow-extrapolation", action="store_true",
                    help="Let recommendations go beyond the lowest and highest weekly spend in each campaign's "
                         "history, where the curve is extrapolating (not recommended)")
    args = ap.parse_args()
    result = analyse(load(args.data), args)
    report = render_markdown(result, args.currency)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.with_suffix(".md").write_text(report, encoding="utf-8")
        args.out.with_suffix(".json").write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")
        print(f"Wrote {args.out.with_suffix('.md')} and {args.out.with_suffix('.json')}")
    else:
        print(report)


if __name__ == "__main__":
    main()
