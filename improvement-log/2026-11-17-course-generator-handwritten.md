# 2026-11-17: course-generator-handwritten

**Date:** 17 November 2026
**Agent:** [course-generator-handwritten](../course-generator-handwritten/)
**Why this agent:** 11 agents had never been reviewed; broken alphabetically, this one comes first.

## What changed

1. **Lecture length guide (code, tests).** `engine/extract.js` now prints a `LONG` warning when a lecture's estimated speech is over 6 minutes, before any text to speech is paid for. It does not stop the build, and `LECTURE_MAX_MIN` overrides it when a client wants longer lectures. `SKILL.md` adds the rule (6 minutes of speech or less, split at a section boundary rather than speeding up the voice). The agent had no tests; `tests/test_extract.py` adds 9 (all passing), covering beat extraction, the existing "missing say" and duplicate beat checks, the warning, the override, the quick check pattern and both shipped examples (3.2 and 2.6 minutes, both inside the guide).
2. **Quick check before the recap.** New teaching step 5: 1 beat asking 1 or 2 recall questions, telling the viewer to pause and answer from memory, with no answers on screen until the recap. It uses the existing engine (`section(id, null, …)` shows the whole framework with nothing highlighted), so no engine change was needed. Checked by rendering stills in a scratch copy with stand-in timings: no page errors, layout as intended.
3. **Show key words, say everything.** New style rule 4 and a QA checklist item: on screen, labels and key words rather than narration copied onto the screen; in the narration, every number, name, setting and highlighted row shown, so the narration doubles as audio description. One example beat (`examples/inference-B4-spec.js`, "Why pay for it?") showed a setting name that was never said; its narration now names it. That example was not re-rendered, because this environment has no text to speech key.
4. **New reference file.** `references/learning-design.md` holds the evidence, its limits and the sources for all 3 changes, and records which existing rules the same sources already support. `SKILL.md` links to it and stays at 110 lines. The agent README gains short "How the lectures are designed" and "Tests" sections.

## Why

- Guo, Kim and Rubin (6.9 million viewing sessions, 4 edX courses) found median watch time topped out at about 6 minutes whatever the video length; Brame's review recommends videos of 6 minutes or less. The skill set no limit except in beginner mode, and a long lecture is costly to voice and render before anyone notices.
- Szpunar, Khan and Schacter found that answering questions between lecture segments improved scores on the final segment (89% against 70% untested and 65% for seeing questions with answers) and roughly halved reported mind wandering. Seeing the answers gave no benefit, which is why the quick check holds the answers back for the recap.
- Brame, summarising Mayer, warns that printed text alongside narrated visuals overloads the visual channel, while a few highlighted key words help. The World Wide Web Consortium's accessibility guidance says videos whose visuals carry needed information need description, and prefers integrated description (in the speaker's script) for new instructional videos. Together they give one rule that is both better teaching and more accessible.

## Considered and rejected

- **Making the length guide a hard failure.** Rejected: some clients want longer lectures, and the evidence is about attention, not a fixed limit. A warning with an override keeps the decision with the person.
- **A quick check after every section,** closer to the experiment's design of a test after each segment of about 5.5 minutes. Rejected: with lectures of 6 minutes or less, one check before the recap already sits at segment level, and more checks would eat the length budget.
- **A new `check()` helper in the engine.** Rejected: the existing `section()` already renders the pattern correctly, so new code would add risk without adding capability.
- **Raising the narration pace.** Guo and colleagues found faster speakers held attention better, but they attribute it to enthusiasm and advise against forcing speed. The skill already trims silence; no change.
- **Embedded chapter markers in the MP4.** Brame cites evidence that chapters give learners useful control. Worth doing, but it needs readable scene titles from the extractor and player support varies; left for a future review.
- **Rewriting the skill description in the third person or adding marketing trigger terms.** Anthropic's guidance prefers the third person, but its own examples use the imperative and the current description already says what the skill does and when to use it. With no evidence of the skill being missed, this would be cosmetic.
- **Adding this agent to the top-level README test command.** Left out: that loop is for the Python-only agents, and this test needs Node. The agent README documents its own command instead.

## Sources

The source list in the review brief is aimed at marketing agents; for a learning video engine the nearest equivalents are peer-reviewed learning research, the World Wide Web Consortium's accessibility guidance and Anthropic's skill documentation.

- Philip J. Guo, Juho Kim and Rob Rubin, *How Video Production Affects Student Engagement: An Empirical Study of MOOC Videos* (ACM Conference on Learning at Scale, 2014): https://up.csail.mit.edu/other-pubs/las2014-pguo-engagement.pdf
- Cynthia J. Brame, *Effective Educational Videos: Principles and Guidelines for Maximizing Student Learning from Video Content* (CBE Life Sciences Education, 2016): https://pmc.ncbi.nlm.nih.gov/articles/PMC5132380/
- Karl K. Szpunar, Novall Y. Khan and Daniel L. Schacter, *Interpolated memory tests reduce mind wandering and improve learning of online lectures* (Proceedings of the National Academy of Sciences, 2013): https://pmc.ncbi.nlm.nih.gov/articles/PMC3631699/
- World Wide Web Consortium, Web Accessibility Initiative, *Description of Visual Information* (updated 17 September 2024): https://www.w3.org/WAI/media/av/description/
- Anthropic, *Skill authoring best practices* (used to check the description, the length of `SKILL.md` and the split into `references/`): https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
