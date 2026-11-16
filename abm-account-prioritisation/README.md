# Account prioritisation for account-based marketing

**Which accounts should sales and marketing work this month, and how?**

Most target account lists are too long to act on and ranked by gut feel. This agent scores every account on two separate questions, sorts them into tiers capped at what sales can actually handle, and explains each score in a line.

## What it does

- **Fit score (0 to 100)**: should we want this account? Industry, size, region, technology, weighted to your ideal customer profile.
- **Engagement score (0 to 100)**: is the account showing interest now? Intent data, website visits, engaged contacts, event attendance.
- **Tiers from the 2 scores together:**

| | Low engagement | High engagement |
|---|---|---|
| **High fit** | Warm up: marketing builds awareness | Pursue now: sales and marketing together |
| **Low fit** | Hold: no proactive spend | Check fit: qualify before investing |

- **Capacity cap**: Pursue now is limited to what sales can work properly. The overflow is labelled "Pursue next" rather than quietly diluting attention.
- **Buying group check**: business purchases involve many people, so a Pursue now account whose interest comes from a single contact is flagged. The next step there is mapping the rest of the buying group, not a sales call.
- **Deals in progress** are kept out of prospecting and flagged for deal support instead.
- **Data gaps** are listed, because a missing value scores zero and pushes a good account down the list.

## Example output

30 fictional European financial services accounts, configuration in [`examples/icp.json`](examples/icp.json). Full report: [`examples/output/account-tiers.md`](examples/output/account-tiers.md).

> | Account | Fit | Engagement | Why |
> |---|---:|---:|---|
> | Tidewren Analytics | 94 | 60 | fits on industry and company size; engaged via event attendance and intent data |
> | Kestrelbay Investments | 88 | 66 | fits on industry and region; engaged via engaged contacts and intent data |
>
> **Pursue next (over capacity):** Quillstone Capital: same profile, but beyond what sales can work this period.
>
> **Buying group check:** Velloway Bank: engagement from 1 person, below the minimum of 2; map the buying group first.

## How it works, in plain terms

Fit is the shape of the key; engagement is whether the door is open right now. A perfect-fit account with no interest needs warming up, not a sales call. An interested account that does not fit needs a quick check, not a campaign. Only accounts where both are true get the expensive, personal treatment, and only as many as the team can actually give it to.

Expect the Warm up tier to be the largest. Research from the Ehrenberg-Bass Institute shows why: where companies change supplier about every 5 years, only around 5% are in the market in any quarter, so most good-fit accounts are simply not buying yet. The evidence behind this and the buying group check is in [`references/buying-groups-and-timing.md`](references/buying-groups-and-timing.md).

## Run it

Python 3.9 or later, no packages to install.

```bash
python3 scripts/prioritise.py --accounts examples/accounts.csv --config examples/icp.json --out output/tiers
python3 -m unittest discover -s tests
```

The scoring configuration is described in [`SKILL.md`](SKILL.md). With Claude Code, install the folder as a skill and ask, for example: *"Here's our target account list with intent scores. Which accounts should we work this month?"*

## Limits

- Scores are relative rankings under the weights you choose, not probabilities of buying. Agree the weights with sales before acting on the list.
- Intent data varies by provider. Calibrate each signal's maximum to what "high" means for your business.
- The buying group check counts engaged people. It cannot tell whether they hold the roles that decide the purchase; that needs a person to look.
- All account names in `examples/` are fictional.
