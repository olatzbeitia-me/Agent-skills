# Growth and marketing agents

Claude skills and small agents I build and use for growth, demand generation and marketing operations work. Each one turns a recurring piece of marketing work into a repeatable method: the judgement written down as instructions for Claude, and, where the work is numerical, tested code.

## The agents

### Pipeline and planning

| Agent | The question it answers | Contains |
|---|---|---|
| [pipeline-forecast](pipeline-forecast/) | Will marketing hit this quarter's pipeline number, and which lever can realistically close the gap? | Python model, tests, example |

### Account-based marketing and demand generation

| Agent | The question it answers | Contains |
|---|---|---|
| [abm-account-prioritisation](abm-account-prioritisation/) | Which accounts should sales and marketing work this month, and how? | Python scoring, tests, example |
| [marketing-performance-audit](marketing-performance-audit/) | What is this company actually doing in marketing, judged from public evidence, and what should change? | Skill and research method |
| [field-marketing-event-strategy](field-marketing-event-strategy/) | Which events should we run, sponsor or skip in each region, and how do we turn them into pipeline with sales? | Skill and playbooks |

### Performance marketing

| Agent | The question it answers | Contains |
|---|---|---|
| [paid-media-budget-optimiser](paid-media-budget-optimiser/) | With the same budget, where should each pound go next week? | Python model, tests, example |
| [paid-media-strategist](paid-media-strategist/) | Which paid channels and ideas fit this business, backed by market and competitor evidence? | Skill and channel guides |

### Marketing operations and automation

| Agent | The question it answers | Contains |
|---|---|---|
| [martech-stack-audit](martech-stack-audit/) | Which marketing, sales and data tools sit behind this website, and how sure are we? | Skill and browser scripts |
| [hubspot-salesforce-architect](hubspot-salesforce-architect/) | How should lifecycle stages, scoring, the HubSpot and Salesforce sync and pipeline reporting be designed and kept healthy? | Skill and reference guides |
| [pardot-to-hubspot-migration](pardot-to-hubspot-migration/) | How do we move marketing automation from Pardot to HubSpot, with Salesforce staying, without losing data, consent or attribution? | Skill, checklists and templates |
| [gtm-automation-architect](gtm-automation-architect/) | Which go-to-market work should be automated, with which tool, and how do we build and test it? | Skill and workflow playbooks |

### Leadership and content

| Agent | The question it answers | Contains |
|---|---|---|
| [marketing-leadership-development](marketing-leadership-development/) | How does a marketing leader in a UK or European scale-up build presence, influence and a team that trusts them? | Coaching skill, 6 modules |
| [course-generator-handwritten](course-generator-handwritten/) | How do we turn a topic or a book into a narrated, hand-drawn explainer course? | Skill and video engine |

## How the agents are built

Every folder is a [Claude skill](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview):

- `SKILL.md`: the method. When to use it, what to ask for, how to reason, and the rules that keep the output honest (no invented data, assumptions stated).
- `references/`: the detailed knowledge the method draws on, loaded only when needed.
- `scripts/` and `tests/`: code for the numerical work, so the arithmetic is exact and checked rather than estimated by the model.
- `examples/`: sample inputs and the real output they produce. All example data is fictional.

## Install

```bash
git clone https://github.com/olatzbeitia-me/Agent-skills.git
mkdir -p ~/.claude/skills
cp -r Agent-skills/<agent-folder> ~/.claude/skills/
```

This makes the skill available in every Claude Code project. To install it for one project only, copy the folder into that project's `.claude/skills/` folder instead. Then ask Claude in plain language; it picks up the right skill from its description.

The Python agents need only Python 3.9 or later, with no packages to install. To run every test:

```bash
for d in pipeline-forecast abm-account-prioritisation paid-media-budget-optimiser; do python3 -m unittest discover -s $d/tests; done
```

The course generator has its own setup: see [its README](course-generator-handwritten/README.md).

## Licence

[MIT](LICENSE)
