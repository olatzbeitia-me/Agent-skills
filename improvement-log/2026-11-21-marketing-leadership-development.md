# 2026-11-21: marketing-leadership-development

**Date:** 21 November 2026
**Agent:** [marketing-leadership-development](../marketing-leadership-development/)
**Why this agent:** 7 agents had never been reviewed and no `improve/` pull requests were open; broken alphabetically, this one comes first.

## What changed

1. **A follow-up loop between sessions (missing method step).** The skill is offered as a programme of eight to twelve weeks and ends every session with same-week actions, but nothing told it to come back to them. The session pattern now opens any second or later session by reviewing the previous actions (done, partly done, not done; what happened; keep, change or drop) and acknowledging progress, and closes every session with a commitments record the learner can copy and keep. Because an assistant may not remember earlier conversations, the skill now says so and asks the learner to bring the record back.
2. **Ask before telling (sharper method).** Before offering research-based options, the skill now asks what the learner has already tried and what options they see, then lets them choose. It stays directive for quick answers, drafts, factual questions and time-critical situations, and holds back the answer on decisions only the learner can make.
3. **Protecting colleagues' information, and when to suggest a person (new guardrails).** Learners describe founders, peers and team members, and modules 00 and 02 ask for feedback and support plans about named people. The skill now suggests roles rather than names, does not ask for a colleague's health or other sensitive details, and keeps such details out of any artefact. Its boundaries now include suggesting a qualified human coach or a mentor for complex, long-running or emotionally heavy situations.

The detail sits in a new reference file, `references/coaching-method.md` (85 lines): an evidence table on coaching and on coaching by a chatbot, with honest labels; the review steps; guidance on when to ask and when to tell; the commitments record template; the colleagues' information rules; and when to suggest a human coach. `SKILL.md` gains a routing row, an extended core guidance point 4, a new point 10, one sentence in point 9 and a revised session pattern, growing from 83 to 90 lines. The description is unchanged.

## Why

- The International Coaching Federation's updated competency model (September 2025) asks coaches to partner with the client on goals, actions and accountability, to support the client's own choices, to invite the client's own ideas about how to move forward, and to acknowledge progress. The skill set actions but never followed them up, and it led with research before hearing the learner's options.
- The Federation's standards for artificial intelligence coaching systems (2024) add reminders of commitments, recognition of progress, a balance between guided and exploratory conversation, a route to a human coach, and data minimisation. The skill had a strong referral boundary for crises but no route to a human coach for ordinary complex situations, and nothing on minimising data about third parties.
- In Terblanche and colleagues' two ten-month randomised trials (2022), a scripted goal-attainment chatbot matched accredited human coaches on self-reported goal attainment, and the authors credit part of this to the chatbot always asking about progress, keeping a record and having people write goals down. Follow-through is the part of coaching an assistant can do reliably, so it is the part most worth building in. The same authors name empathy and complex situations as the limits, which supports suggesting a person when those dominate.
- Jones, Woods and Guillaume's UK meta-analysis of workplace coaching (2016) found positive effects on organisational outcomes that did not depend on the format or number of sessions. It gives the skill an honest evidence label for coaching itself, which it previously lacked, while showing the evidence base is small (17 studies) and about human coaches.
- The Global Code of Ethics for coaches, mentors and supervisors (December 2025 edition) asks practitioners to promote the learner's independence and self-reliance and to protect client information in line with data protection law. The Information Commissioner's Office explains that health data, including mental health, and characteristics such as ethnicity, religion and sexual orientation are special category data needing extra protection under UK law. Together these justify the colleagues' information guardrail; the skill's own routing already sends "a support plan for someone struggling" to module 02.
- Anthropic's skill authoring guidance keeps `SKILL.md` as an overview with detail one level down, which is why the method lives in a new reference file linked directly from `SKILL.md`.

## Considered and rejected

- **Rewriting the description to mention the new method.** It is 1,020 characters against Anthropic's 1,024-character limit, and the triggers it lists are still right, so it was left alone. Any future addition must cut something first.
- **A full model such as GROW (goal, reality, options, way forward).** It would fit, but the sources read in this run were competency and ethics standards rather than the model's own literature, and the 8-step session pattern already covers the same ground without adding a new acronym.
- **Re-verifying dated figures elsewhere in the skill** (Institute of Practitioners in Advertising Bellwether, Marketing Week survey, the EU Artificial Intelligence Act dates). Each is dated and labelled already; checking them properly needs its own review rather than a quick pass.
- **The detail of how Jones and colleagues define affective outcomes and how many studies sit behind each outcome type.** The full text could not be read in this run, so the reference file reports only the figures from the abstract and uses the authors' own term.
- **Stating that no published trials yet test conversational assistants as leadership coaches.** No systematic search was done, so the reference file says only that the evidence it cites says little about this.

## Noticed outside this agent

- `pardot-to-hubspot-migration/SKILL.md` has a 1,035-character description, above Anthropic's documented 1,024-character limit; it is due for review in a few days and should be shortened then.
- The repository `README.md` opens with "reussable" (should be "reusable").

## Sources

- International Coaching Federation, *2025 ICF Core Competencies* (released September 2025): https://coachingfederation.org/wp-content/uploads/2025/09/icf-cs-core-competencies-2025.pdf, and *Artificial Intelligence Coaching Framework and Standards*, version 1.01 (October 2024): https://coachingfederation.org/app/uploads/2024/11/ICF-AI-Reports-Framework-Standards.pdf
- European Mentoring and Coaching Council and co-signatories, *Global Code of Ethics for Coaches, Mentors and Supervisors* (December 2025 edition): https://www.emccfrance.org/wp-content/uploads/GLOBAL-CODE-OF-ETHICS-EMCC-December-2025.pdf
- Terblanche, N., Molyn, J., de Haan, E. and Nilsson, V. O. (2022), *Comparing artificial intelligence and human coaching goal attainment efficacy*, PLOS ONE 17(6): https://doi.org/10.1371/journal.pone.0270255 (read via https://radar.brookes.ac.uk/radar/file/4aca9bc6-4c00-4bc1-9fde-74a184b87101/1/journal.pone.0270255.pdf)
- Jones, R. J., Woods, S. A. and Guillaume, Y. R. F. (2016), *The effectiveness of workplace coaching: a meta-analysis of learning and performance outcomes from coaching*, Journal of Occupational and Organizational Psychology 89(2): https://centaur.reading.ac.uk/74522/
- Information Commissioner's Office, *What is special category data?*: https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/lawful-basis/special-category-data/what-is-special-category-data
- Anthropic, *Skill authoring best practices*: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
