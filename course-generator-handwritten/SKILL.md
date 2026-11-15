---
name: course-generator-handwritten
description: Make narrated, hand-drawn whiteboard explainer videos and multi-lecture courses (black canvas, neon doodles drawn stroke by stroke, rough handwriting, ~1.2x voiceover) from a topic, a book/PDF, or research. Use when asked for an explainer video, a video lecture or course, or to turn a book, PDF or notes into lectures.
---

# Course Generator: Handwritten Explainer Videos

Output: one or more 1920x1080 30fps H.264+AAC MP4s with embedded subtitles plus .srt, styled like someone teaching on a black iPad with neon markers (Caleb Eom style). Each lecture is written as a compact **spec.js** (narration + visuals together); the engine lays it out, times every drawing to the spoken word, and renders.

```
research → spec.js per lecture → build.sh (extract → TTS → scenes.js) → qa.sh (stills) → fix → render_lecture.sh → zip + deliver
```

## Style rules (non-negotiable)

1. **Pace ≈ 1.2x, never faster.** API voices: trim silence, then `ATEMPO=1.05` (expressive voice) to `1.12` (slow voice). 0.2s gap between beats. 1.25x+ sounds rushed.
2. **Handmade look.** Reenie Beanie font with per-letter jitter; rough.js lines (roughness ≥1.4) plus an SVG turbulence wobble. Only "printed" evidence cards (tables, real numbers) are clean sans-serif.
3. **Black background, neon roles:** `w` main, `g` good/works, `p` problem/warning, `v` concept, `o` actions/analogies, `y` highlights/numbers, `b` secondary, `gr` citations/asides.

## Teaching structure (every lecture)

1. **Hook (20–40s):** a relatable situation, then a surprising fact, then a question. Then a title beat that previews the framework.
2. **Framework (`LAYERS`, 3–7 items):** the spine. Each section shows a mini copy top-right with its layer bracketed.
3. **Sections:** 1–3 beats each. One idea and one visual per beat. Name sources out loud and in grey on screen.
4. **Intuition:** at least one `analogy` per section for anything abstract ("a smoke detector, not a fire brigade"). Gloss jargon in plain words immediately.
5. **Recap and up next:** the framework, ticked lines, then the next lecture's title, so a course chains together.

Voice: a peer explaining over coffee. Short sentences, "So,", "And here's the thing.", "Remember the X?". Write numbers the way they should be spoken ("twenty twenty six", "one point seven seconds"). Avoid symbols in `say`.

**Beginner-friendly mode** (when asked to make it understandable to newcomers): supplement the source with your own web research, add an analogy per concept, and slow the idea density (≈500–650 words per 3–4 min lecture).

## Accuracy

Web-search every number, date and name. Prefer primary sources. Keep numbers from one experiment together. Label vendor claims ("vendor's numbers: verify"). Never invent an example a book didn't give; quote the book's own. Ship a Sources list.

## Setup

Work in `~/course`, a copy of this skill's `engine/` folder, so audio and videos stay out of the skills folder. Skip the copy if `~/course` already exists.

```bash
cp -r <this skill's folder>/engine ~/course && cd ~/course   # e.g. ~/.claude/skills/course-generator-handwritten/engine
npm i && npm run browsers        # Playwright + Chromium (needs Node 20+)
pip install --break-system-packages soundfile numpy
cp .env.example .env             # fill TTS_* in .env (never commit it)
```
ffmpeg must be installed. Lecture folders (`~/course/L02_Architecture/spec.js`) sit next to the scripts; the scripts can be called from any directory.

**TTS is pluggable** (`tts.py`): any OpenAI-compatible `POST /audio/speech` that returns `response_format: "pcm"` (24 kHz s16le). Configure `TTS_URL`, `TTS_API_KEY`, `TTS_MODEL` and `TTS_VOICE` via env or `.env`. Pick a voice by testing 2–3 voices on one beat and choosing the most expressive one (highest pitch variance), not the first. Audio is cached per beat with a text sidecar, so only edited beats are re-voiced. Never hard-code keys or model names in committed files.

## Writing a lecture: `<Dir>/spec.js`

```js
const LECT = { label: 'Lecture 2 · behind the scenes', title: 'The Seven-Layer Architecture' };
const LAYERS = ['Channels + triggers', 'Gateway', 'Durable orchestrator', 'Agent loop'];
say({ hook: "…", title: "…", recap: "…", outro: "Next, …" });          // registry for intro/recap beats
intro('S01_Intro', 'hook', 'title', [ items… ]);
section('S02_Gateway', 1 /*layer idx*/, 'v' /*colour*/, [
  { b: 'ga1', t: 'The front door', cite: 'Source, 2026', say: "Narration…", v: [ items… ] },
]);
recap('S06_Recap', 'recap', 'outro', ['line', 'line'], 'Next lecture title');
```
Each beat gets its own panel, and the camera pans between panels. Layout auto-scales to fit.

**Items** `[type, ...args, opts?]`:
| type | args |
|---|---|
| `big` / `text` | `str, colour, size` |
| `note` | `str, colour` (arrow-prefixed aside) |
| `analogy` | `null, str, 'o'` (boxed "think of it like…") |
| `list` | `[lines], colour, {num|tick}` |
| `col` | `title, colour, [lines]` (use inside `row`) |
| `row` | `[[item],[item]…], {vs, gap}` (side by side) |
| `flow` | `[labels], [colours]` (boxes with arrows) |
| `stack` | `[labels], {rh,size,w,cols,step}` |
| `tokens` | `[words], colour, {step, cols}` (wraps) |
| `bars` / `hbars` | `[[label, value, colour, valueLabel]…], {h | lw}` |
| `eq` | `str, colour` (underlined headline number) |
| `card` | `title, rows[][], {w, hi:[rowIdx], hit:[time]}` (printed table; row 0 is the header) |
| `chart` | `[[[x,y]…], colour, label]…], {h, xl, yl}` |
| `timeline` / `grid` / `gpus` / `people` / `down` | see `dsl.js` |

**Timing opts** (last object): `at: 'word'` starts the item when that word is spoken (`occ: 2` for the second occurrence); `times: [[beat, frac, 'f'], …]` sets per-part timing as a fraction of the beat; `step` staggers parts. Starts are clamped so drawing finishes ≥2.6s before the beat ends. Allowed opt keys are whitelisted in `dsl.js` (`OPTK`); an unknown key is treated as data, so add new keys there.

## Build, QA, render

```bash
./build.sh L02_Architecture            # beats.json, TTS, scenes.js; prints speech minutes
./qa.sh L02_Architecture               # end-of-beat stills tiled to L02_Architecture/qa/sheet*.jpg
./render_lecture.sh L02_Architecture "02 - The Seven-Layer Architecture"   # 2 parallel lanes → out/*.mp4 + .srt
```
Run QA on every lecture before rendering and **look at every sheet**. Fix:
- labels overflowing boxes (the engine shrinks fonts, but long labels still need shortening);
- a card highlight on the wrong row (count the header as row 0);
- content past the frame;
- an `at` word that doesn't exist (`WORDMISS` in the log).

For many lectures, use a queue: a `READY` flag per directory, one render at a time, re-render when `scenes.js` is newer than the MP4. In the cloud, finished lectures take about 3–4 min each to render. Background jobs must be harness-tracked (not `nohup` on a VM that may sleep).

## Deliver

Zip `out/*.mp4 + *.srt` with numbered, labelled filenames ("00 - Title.mp4"). In the reply give a runtime table, one line on approach, and Sources.

## Examples

`examples/agents-L00-spec.js` (concept lecture) and `examples/inference-B4-spec.js` (evidence-heavy lecture) are complete, rendered specs to copy from.
