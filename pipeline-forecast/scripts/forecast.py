#!/usr/bin/env python3
"""Pipeline forecast: will this quarter's marketing-sourced pipeline hit target, and if not, what closes the gap?

Reads monthly funnel history (leads, marketing qualified leads, sales qualified leads, opportunities,
pipeline value) and a quarter plan (target, planned leads for the months still to come). Produces:

  * a low / base / high forecast built from the conversion rates of recent months;
  * the size of any gap to target;
  * what each lever would have to do, on its own, to close that gap, checked against the best month
    actually achieved recently, so the answer separates realistic levers from wishful ones;
  * warning signs where a conversion rate is falling.

Standard library only. Run:  python3 forecast.py --history funnel.csv --plan plan.json --out report
"""
from __future__ import annotations

import argparse
import csv
import json
import statistics
from pathlib import Path

STAGES = ["leads", "mqls", "sqls", "opportunities"]
STAGE_LABELS = {
    "leads": "Leads",
    "mqls": "Marketing qualified leads",
    "sqls": "Sales qualified leads",
    "opportunities": "Opportunities",
}
RATES = [  # (key, from stage, to stage, plain-English label)
    ("lead_to_mql", "leads", "mqls", "Lead to marketing qualified lead"),
    ("mql_to_sql", "mqls", "sqls", "Marketing qualified to sales qualified"),
    ("sql_to_opp", "sqls", "opportunities", "Sales qualified lead to opportunity"),
]
VALUE_KEY = "value_per_opp"
LEVER_LABELS = {
    "leads": "More leads in the remaining months",
    "lead_to_mql": "Better lead to marketing qualified lead rate",
    "mql_to_sql": "Better marketing qualified to sales qualified rate",
    "sql_to_opp": "Better sales qualified lead to opportunity rate",
    VALUE_KEY: "Higher average opportunity value",
}
TREND_ALERT = 0.10  # flag a rate that fell more than 10% (relative) between the two halves of the window


# ---------- loading and validation ----------

def load_history(path: Path) -> list[dict]:
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for line_no, raw in enumerate(csv.DictReader(f), start=2):
            try:
                row = {"month": raw["month"].strip()}
                for key in STAGES:
                    row[key] = int(float(raw[key]))
                row["pipeline_value"] = float(raw["pipeline_value"])
            except (KeyError, ValueError) as exc:
                raise SystemExit(f"{path}, line {line_no}: missing or non-numeric value ({exc})")
            for a, b in zip(STAGES, STAGES[1:]):
                if row[b] > row[a]:
                    raise SystemExit(f"{path}, line {line_no}: {b} ({row[b]}) is larger than {a} ({row[a]})")
            rows.append(row)
    rows.sort(key=lambda r: r["month"])
    if len({r["month"] for r in rows}) != len(rows):
        raise SystemExit(f"{path}: duplicate months")
    return rows


def load_plan(path: Path) -> dict:
    plan = json.loads(Path(path).read_text(encoding="utf-8"))
    for key in ("quarter_label", "quarter_months", "pipeline_target", "planned_leads"):
        if key not in plan:
            raise SystemExit(f"{path}: missing '{key}'")
    plan.setdefault("lookback_months", 6)
    plan.setdefault("currency", "£")
    return plan


# ---------- maths ----------

def month_rates(row: dict) -> dict:
    rates = {}
    for key, a, b, _ in RATES:
        rates[key] = row[b] / row[a] if row[a] else 0.0
    rates[VALUE_KEY] = row["pipeline_value"] / row["opportunities"] if row["opportunities"] else 0.0
    return rates


def quantile(values: list[float], q: float) -> float:
    """Linear-interpolated quantile, q between 0 and 1."""
    s = sorted(values)
    if len(s) == 1:
        return s[0]
    pos = (len(s) - 1) * q
    lo, hi = int(pos), min(int(pos) + 1, len(s) - 1)
    return s[lo] + (s[hi] - s[lo]) * (pos - lo)


def project(leads: float, rates: dict) -> dict:
    """Push a volume of leads through the funnel with a given set of rates."""
    out = {"leads": leads}
    for key, a, b, _ in RATES:
        out[b] = out[a] * rates[key]
    out["pipeline_value"] = out["opportunities"] * rates[VALUE_KEY]
    return out


def forecast(history: list[dict], plan: dict) -> dict:
    quarter = plan["quarter_months"]
    actuals = [r for r in history if r["month"] in quarter]
    window = [r for r in history if r["month"] < quarter[0]][-plan["lookback_months"]:]
    if len(window) < 3:
        raise SystemExit("Need at least 3 months of history before the quarter starts.")
    remaining = [m for m in quarter if m not in {r["month"] for r in actuals}]
    missing = [m for m in remaining if m not in plan["planned_leads"]]
    if missing:
        raise SystemExit(f"plan.json: planned_leads missing for {', '.join(missing)}")

    per_month = [month_rates(r) for r in window]
    keys = [k for k, *_ in RATES] + [VALUE_KEY]
    series = {k: [m[k] for m in per_month] for k in keys}
    scenario_rates = {
        "low": {k: quantile(series[k], 0.25) for k in keys},
        "base": {k: statistics.median(series[k]) for k in keys},
        "high": {k: quantile(series[k], 0.75) for k in keys},
    }
    planned = sum(float(plan["planned_leads"][m]) for m in remaining)
    to_date = sum(r["pipeline_value"] for r in actuals)
    target = float(plan["pipeline_target"])

    scenarios = {}
    for name, rates in scenario_rates.items():
        proj = project(planned, rates)
        total = to_date + proj["pipeline_value"]
        scenarios[name] = {"rates": rates, "funnel": proj, "remaining_value": proj["pipeline_value"],
                           "total": total, "vs_target": total / target if target else 0.0}

    base = scenarios["base"]
    gap = target - base["total"]
    levers = []
    if gap > 0 and base["remaining_value"] > 0:
        needed_multiplier = (target - to_date) / base["remaining_value"]
        best_month_leads = max(r["leads"] for r in window)
        for key in ["leads"] + keys:
            if key == "leads":
                current = planned
                needed = planned * needed_multiplier
                # compare monthly lead volume against the best month in the window
                per_month_needed = needed / len(remaining) if remaining else needed
                best = best_month_leads
                achievable = per_month_needed <= best
                levers.append({"lever": key, "label": LEVER_LABELS[key], "current": current, "needed": needed,
                               "needed_per_month": per_month_needed, "best_recent": best,
                               "change": needed_multiplier - 1, "achievable": achievable})
            else:
                current = base["rates"][key]
                needed = current * needed_multiplier
                best = max(series[key])
                levers.append({"lever": key, "label": LEVER_LABELS[key], "current": current, "needed": needed,
                               "best_recent": best, "change": needed_multiplier - 1,
                               "achievable": needed <= best})
        levers.sort(key=lambda x: (not x["achievable"], x["change"]))

    warnings = []
    half = len(window) // 2
    if half >= 2:
        for key in keys:
            early = statistics.mean(series[key][:half])
            late = statistics.mean(series[key][-half:])
            if early and (early - late) / early > TREND_ALERT:
                warnings.append({"metric": key, "earlier": early, "recent": late, "change": late / early - 1,
                                 "months": half})
    return {
        "quarter": plan["quarter_label"], "currency": plan["currency"], "target": target,
        "months_with_actuals": [r["month"] for r in actuals], "months_remaining": remaining,
        "lookback": [r["month"] for r in window], "pipeline_to_date": to_date, "planned_leads": planned,
        "scenarios": scenarios, "gap_to_target": gap, "levers": levers, "warnings": warnings,
        "series": series,
    }


# ---------- report ----------

def money(x: float, cur: str) -> str:
    return f"{cur}{x:,.0f}"


def fmt_value(key: str, x: float, cur: str) -> str:
    if key == VALUE_KEY:
        return money(x, cur)
    if key == "leads":
        return f"{x:,.0f}"
    return f"{x:.1%}"


def label(key: str) -> str:
    if key == VALUE_KEY:
        return "Average opportunity value"
    if key == "leads":
        return "Leads"
    return next(l for k, *_, l in RATES if k == key)


def render_markdown(r: dict) -> str:
    cur = r["currency"]
    base = r["scenarios"]["base"]
    lines = [f"# Pipeline forecast: {r['quarter']}", ""]
    status = "on track" if r["gap_to_target"] <= 0 else "short of target"
    lines += [
        f"**Target:** {money(r['target'], cur)}  ",
        f"**Base forecast:** {money(base['total'], cur)} ({base['vs_target']:.0%} of target, {status})  ",
    ]
    if r["gap_to_target"] > 0:
        lines.append(f"**Gap to close:** {money(r['gap_to_target'], cur)}")
    else:
        lines.append(f"**Headroom:** {money(-r['gap_to_target'], cur)}")
    lines += ["", f"Pipeline created so far this quarter ({', '.join(r['months_with_actuals']) or 'none yet'}): "
              f"{money(r['pipeline_to_date'], cur)}. Months still to come: {', '.join(r['months_remaining'])}, "
              f"with {r['planned_leads']:,.0f} leads planned.", ""]

    lines += ["## Scenarios", "",
              "| Scenario | Rates used | Pipeline still to come | Quarter total | Share of target |",
              "|---|---|---:|---:|---:|"]
    desc = {"low": "25th percentile of recent months", "base": "median of recent months",
            "high": "75th percentile of recent months"}
    for name in ("low", "base", "high"):
        s = r["scenarios"][name]
        lines.append(f"| {name.title()} | {desc[name]} | {money(s['remaining_value'], cur)} | "
                     f"{money(s['total'], cur)} | {s['vs_target']:.0%} |")
    lines += ["", "The low scenario puts every rate at a weak-month level at once, so treat it as a floor "
              "rather than a likely outcome.", ""]

    lines += ["## How the base forecast is built", "",
              f"Rates come from {len(r['lookback'])} months of history ({r['lookback'][0]} to {r['lookback'][-1]}).", "",
              "| Step | Volume | Rate used | Range in recent months |", "|---|---:|---:|---|"]
    f = base["funnel"]
    lines.append(f"| Leads planned | {f['leads']:,.0f} | | |")
    for key, a, b, lab in RATES:
        lo, hi = min(r["series"][key]), max(r["series"][key])
        lines.append(f"| {STAGE_LABELS[b]} | {f[b]:,.0f} | {base['rates'][key]:.1%} | {lo:.1%} to {hi:.1%} |")
    lo, hi = min(r["series"][VALUE_KEY]), max(r["series"][VALUE_KEY])
    lines.append(f"| Pipeline value | {money(f['pipeline_value'], cur)} | {money(base['rates'][VALUE_KEY], cur)} "
                 f"per opportunity | {money(lo, cur)} to {money(hi, cur)} |")
    lines.append("")

    if r["levers"]:
        lines += ["## What it would take to close the gap", "",
                  "Each row is one lever on its own, with everything else at the base rate. "
                  "\"Realistic\" means the level needed has been reached in at least one recent month.", "",
                  "| Lever | Now | Needed | Best recent month | Verdict |", "|---|---:|---:|---:|---|"]
        for lv in r["levers"]:
            key = lv["lever"]
            if key == "leads":
                now = f"{lv['current']:,.0f} total"
                needed = f"{lv['needed']:,.0f} total ({lv['needed_per_month']:,.0f} a month)"
                best = f"{lv['best_recent']:,.0f} in a month"
            else:
                now, needed, best = (fmt_value(key, lv[k], cur) for k in ("current", "needed", "best_recent"))
            verdict = "Realistic" if lv["achievable"] else "Beyond recent performance"
            lines.append(f"| {lv['label']} | {now} | {needed} (+{lv['change']:.0%}) | {best} | {verdict} |")
        realistic = [lv for lv in r["levers"] if lv["achievable"]]
        lines.append("")
        if realistic:
            lines.append(f"Start with: **{realistic[0]['label'].lower()}**. It needs the smallest stretch that "
                         "recent months show is possible. Combining two smaller moves is usually easier than one big one.")
        else:
            lines.append("No single lever closes the gap within recent performance. Either combine levers, "
                         "or reset the target with the evidence above.")
        lines.append("")

    if r["warnings"]:
        lines += ["## Warning signs", ""]
        for w in r["warnings"]:
            lines.append(f"- **{label(w['metric'])}** fell from {fmt_value(w['metric'], w['earlier'], cur)} to "
                         f"{fmt_value(w['metric'], w['recent'], cur)} ({w['change']:.0%}), comparing the first and "
                         f"last {w['months']} months of the window. If it keeps falling, the base forecast is too high.")
        lines += ["", "Find the cause before adding volume: extra leads at a falling conversion rate buy less "
                  "pipeline than this forecast assumes.", ""]

    lines += ["## Assumptions and limits", "",
              "- Rates are same-month ratios (for example, this month's opportunities divided by this month's sales "
              "qualified leads). That works when lead volume is steady; if volume swings sharply, use cohort data.",
              "- Leads created in the last weeks of the quarter often turn into opportunities after it ends, so the "
              "final month's contribution is optimistic.",
              "- The forecast is only as good as the stage definitions behind the numbers. If the definition of a "
              "qualified lead changed during the window, the rates are not comparable.", ""]
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--history", required=True, type=Path, help="CSV: month,leads,mqls,sqls,opportunities,pipeline_value")
    ap.add_argument("--plan", required=True, type=Path, help="JSON quarter plan")
    ap.add_argument("--out", type=Path, help="Write <out>.md and <out>.json (otherwise print the report)")
    args = ap.parse_args()
    result = forecast(load_history(args.history), load_plan(args.plan))
    report = render_markdown(result)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.with_suffix(".md").write_text(report, encoding="utf-8")
        args.out.with_suffix(".json").write_text(json.dumps(result, indent=2), encoding="utf-8")
        print(f"Wrote {args.out.with_suffix('.md')} and {args.out.with_suffix('.json')}")
    else:
        print(report)


if __name__ == "__main__":
    main()
