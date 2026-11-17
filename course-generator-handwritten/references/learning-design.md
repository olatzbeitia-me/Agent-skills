# Learning design: the evidence behind the teaching rules

Read this when planning a course, when a client asks why lectures are short or why there is a quick check, or when deciding whether to bend a rule. `SKILL.md` holds the rules; this file holds the reasons, the limits of the evidence and the sources.

## Contents

1. Keep each lecture to 6 minutes of speech or less
2. Ask the viewer to recall before the recap
3. Show key words, say everything
4. What the evidence already supports in this skill
5. Sources

## 1. Keep each lecture to 6 minutes of speech or less

**Evidence.** Guo, Kim and Rubin studied 6.9 million viewing sessions across 4 edX courses from autumn 2012. The median time a viewer spent on a video was never more than about 6 minutes, however long the video was, and on videos longer than 9 minutes viewers often stopped before the halfway point. Their recommendation to producers was to plan lessons as chunks of under 6 minutes. Brame's review of the cognitive load research reaches the same guide: segment content into videos of 6 minutes or less, because shorter pieces manage how much is new at once and are more likely to be watched to the end.

**How the skill applies it.**

- Aim for 6 minutes of speech or less per lecture. At the engine's estimate of 2.65 words a second, that is about 950 words of narration.
- `extract.js` prints a `LONG` warning when a lecture's estimated speech goes over 6 minutes, before any text to speech is paid for. The warning does not stop the build. Set `LECTURE_MAX_MIN` (for example `LECTURE_MAX_MIN=8 ./build.sh L03_Topic`) only when the client has asked for longer lectures.
- Fix a long lecture by splitting it at a section boundary into 2 lectures, each with its own hook, framework and recap, and chain them with "up next". Do not fix it by speeding up the voice: the pace rule in `SKILL.md` still applies.

**Limits.** Watch time is a proxy for attention, not proof of learning, and the authors say so. The courses were mathematics and science, the learners were early adopters of online courses, and the study is observational. Treat 6 minutes as a strong default, not a law.

## 2. Ask the viewer to recall before the recap

**Evidence.** Szpunar, Khan and Schacter ran 2 experiments with 80 students learning a 21-minute statistics lecture split into 4 segments of about 5.5 minutes. In the second experiment, students who answered short questions after each segment got 89% of questions on the final segment right, against 70% for students who did arithmetic instead and 65% for students who saw the same questions with the answers. The tested students also reported mind wandering on 19% of attention checks, against roughly 40% in the other 2 groups, took more notes and felt less anxious about the final test. The detail that matters for video design: seeing questions with their answers gave no benefit. The gain came from the effort of recalling. Brame's review lists packaging videos with questions as one of the main ways to turn watching into active learning.

**How the skill applies it.**

- Add a quick check beat after the last section and before the recap: 1 or 2 short questions about the lecture's framework.
- In the narration, ask the viewer to pause and answer from memory, and say that the recap has the answers.
- Do not show the answers in the same beat. The recap, which already ticks off each point, is the reveal.
- Use `section(id, null, 'y', [beat], 'Quick check')`. Passing `null` as the layer shows the whole framework in the corner with nothing highlighted, which signals "this covers the whole lecture".
- Keep it to 1 short beat (a question, the pause prompt and a pointer to the recap) so it does not eat into the length guide.
- If the course will sit in a learning platform, give the client the same questions to place after each video, where viewers actually have to answer.

**Limits.** The experiment used questions answered outside the video, by undergraduates in a laboratory. A spoken "pause the video" in a plain video file only invites recall; viewers can carry on watching. It is still the closest a non-interactive video can get, and it costs one short beat.

## 3. Show key words, say everything

**Evidence.**

- *On screen, key words rather than sentences.* Brame, drawing on Mayer's multimedia learning research, recommends that pictures and narration carry complementary information, and notes that putting printed text next to a narrated animation overloads the visual channel and hurts learning. Highlighting 2 or 3 key words, a colour change or an arrow (signalling) helps viewers see what matters.
- *In the narration, everything that matters on screen.* The World Wide Web Consortium's accessibility guidance (updated September 2024) says a video whose visuals carry information needed to understand it needs a description of those visuals for people who cannot see them; the Web Content Accessibility Guidelines require this at level AA for pre-recorded video (success criterion 1.2.5). For new instructional videos, the guidance prefers integrated description: the speaker's script covers the relevant visual information, including any text on screen, so no separate described version is needed. The wording does not have to match the screen exactly, but the information does. The guidance also suggests checking, before the video is finalised, that every relevant visual is covered in the audio.

**How the skill applies it.**

- Visual items are labels, key words, numbers and diagrams, never the narration copied onto the screen.
- Every number, name, setting, table row that is highlighted, and on-screen claim is also said in the narration, in words that can be spoken (no symbols).
- The QA pass checks for anything shown that is never said. Fix it by saying it or by cutting it.
- Subtitles are already embedded in each MP4 and written as `.srt`, which covers captions for viewers who cannot hear.

## 4. What the evidence already supports in this skill

These parts of the skill were checked against the same sources and left unchanged:

- **The hand-drawn style.** Guo and colleagues found that tutorials drawn freehand on a tablet held viewers 1.5 to 2 times as long as slide or code screencast tutorials. They also observed that the best drawn tutorials had careful layout so the canvas did not get crowded, which is what the QA sheets check.
- **Pace and trimmed silence.** Faster speakers held attention better in the same study (speaking rates ranged from 48 to 254 words a minute, mean 156), but the authors put this down to enthusiasm, not speed itself. Their advice was not to slow down artificially and to edit out pauses and filler. The skill already trims silence and sets a lively but unrushed pace.
- **Conversational voice.** Brame cites Mayer's personalisation principle: a conversational style, addressing the viewer as "you", improves learning. This matches the "peer explaining over coffee" voice.
- **One idea per beat and a framework on screen.** Segmenting and signalling (Brame) match short beats and the mini framework in the corner.

## 5. Sources

- Philip J. Guo, Juho Kim and Rob Rubin, *How Video Production Affects Student Engagement: An Empirical Study of MOOC Videos*, Proceedings of the First ACM Conference on Learning at Scale, 2014: https://up.csail.mit.edu/other-pubs/las2014-pguo-engagement.pdf
- Cynthia J. Brame, *Effective Educational Videos: Principles and Guidelines for Maximizing Student Learning from Video Content*, CBE Life Sciences Education 15(4), 2016: https://pmc.ncbi.nlm.nih.gov/articles/PMC5132380/
- Karl K. Szpunar, Novall Y. Khan and Daniel L. Schacter, *Interpolated memory tests reduce mind wandering and improve learning of online lectures*, Proceedings of the National Academy of Sciences 110(16), 2013: https://pmc.ncbi.nlm.nih.gov/articles/PMC3631699/
- World Wide Web Consortium, Web Accessibility Initiative, *Description of Visual Information* (updated 17 September 2024): https://www.w3.org/WAI/media/av/description/
