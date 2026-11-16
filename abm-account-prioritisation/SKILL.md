---
name: abm-account-prioritisation
description: Scores a list of target accounts on fit (should we want them?) and engagement (are they interested now?), sorts them into tiers capped at sales capacity, flags accounts whose interest comes from too few people in the buying group, explains each score, and recommends the play for each tier. Use when building or refreshing an account-based marketing target list, deciding which accounts sales and marketing should work this month, combining intent data with firmographics, or agreeing an ideal customer profile with sales.
---

# Account prioritisation

Turn a long account list into a short, defensible answer to **"which accounts do we work this month, and how?"**

The scoring lives in `scripts/prioritise.py` (Python 3, standard library only). Your job is to agree the scoring model with the user, run it, and turn the result into a plan sales will accept.

## 1. Agree the model first

The ranking is only as credible as the weights. Before scoring, draft `icp.json` with the user and confirm it:

- **Fit criteria**: what makes an account worth winning. Usually industry, company size, region, and one technology or maturity signal. Base the values on closed-won history if the user has it; otherwise say the weights are a starting hypothesis.
- **Engagement criteria**: signals of current interest, such as intent data scores, website visits, engaged contacts and event attendance. Set each `max` at a level that genuinely means "high" for this business, so one noisy signal cannot dominate. Make every engagement column cover the same recent window (for example the last 30 days), or a stale signal will look current.
- **Thresholds and capacity**: the fit and engagement scores that count as "high", and how many accounts sales can properly work at once (`pursue_now_capacity`).
- **Buying group minimum** (optional): the column that counts engaged people at each account and the fewest that should be engaged before sales outreach (`buying_group`). Agree the number with sales; it is a floor, not a target.

See `examples/icp.json` for the format: categorical criteria use `values` with a `default`, numeric ones use `bands` or `max`, and every criterion has a `weight`.

## 2. Run it

```bash
python3 scripts/prioritise.py --accounts accounts.csv --config icp.json --out output/tiers --title "Account prioritisation: <segment>"
```

`accounts.csv` needs an `account` column plus one column per criterion and, optionally, `open_opportunity` (yes/no). Output: `tiers.md` (report) and `tiers.csv` (every account with tier, scores, buying group note and the reason).

## 3. Write the answer

1. **The list for this month**: the Pursue now accounts, why each is there in one line, and who should own the next step. For any account in the buying group check, the next step is finding and engaging the other people involved in the decision, not a sales call to the one interested contact.
2. **What marketing does with Warm up accounts**: those accounts are the future pipeline, so give them a programme, not a holding pattern. Most of them are simply not buying this quarter; set expectations with the category's typical time between purchases and judge the programme over quarters, not by this month's pipeline.
3. **Check fit accounts**: name the quick qualification step, so interest from poor-fit accounts does not absorb sales time.
4. **Data to fix**: missing values score zero and push accounts down. List them and who can fill the gaps.
5. **When to re-score**: engagement decays, so normally monthly.

For the evidence behind steps 1 and 2, and how to map these inputs to HubSpot fields, see [references/buying-groups-and-timing.md](references/buying-groups-and-timing.md).

## Rules

- Never invent account data, intent scores or weights. If a signal is missing, leave it out of the model and say so.
- Present scores as relative rankings under the agreed weights, not probabilities of buying.
- Respect capacity. Recommending more Pursue now accounts than sales can work is how account-based marketing turns into spray and pray.
- Keep open opportunities out of prospecting tiers; recommend deal support instead.
- Treat interest from a single person as a lead into the account, not proof the account is in market.
