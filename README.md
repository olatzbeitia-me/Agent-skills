# agent-skills

Reusable skills for Claude Code.

| Skill | What it does |
|---|---|
| [`course-generator-handwritten`](course-generator-handwritten/SKILL.md) | Turns a topic, book/PDF or research into narrated, hand-drawn whiteboard explainer videos and courses. |

## How The Agent works

```mermaid
flowchart LR
    A["Source<br/>topic / PDF / research"]:::src --> B["Research<br/>verify facts"]:::research
    B --> C["spec.js<br/>narration + visuals"]:::spec
    C --> D["Voiceover<br/>TTS, ~1.2x pace"]:::voice
    D --> E["Engine<br/>hand-drawn, word-synced"]:::engine
    E --> F{"QA stills<br/>layout OK?"}:::qa
    F -- no --> C
    F -- yes --> G["Render<br/>Playwright + ffmpeg"]:::render
    G --> H["Course<br/>MP4 + subtitles"]:::out

    classDef src fill:#6fb7ff,stroke:#1e3a5f,color:#0000
    classDef research fill:#8c7dff,stroke:#2e2470,color:#fff
    classDef spec fill:#f2ef6a,stroke:#6b6a10,color:#000
    classDef voice fill:#ff5ad9,stroke:#6b1059,color:#000
    classDef engine fill:#ffa53d,stroke:#6b3f05,color:#000
    classDef qa fill:#ffffff,stroke:#ff5ad9,stroke-width:3px,color:#000
    classDef render fill:#8af07a,stroke:#1f5a17,color:#000
    classDef out fill:#000000,stroke:#8af07a,stroke-width:3px,color:#8af07a
```

## Install

```bash
git clone https://github.com/yasir-khalid/agent-skills
mkdir -p ~/.claude/skills
cp -r agent-skills/course-generator-handwritten ~/.claude/skills/
```

To install for a single project only, copy the skill into that project's `.claude/skills/` folder instead.

Requirements: Node 18+, Python 3, ffmpeg, Playwright with Chromium, and an OpenAI-compatible text-to-speech API key.

## Configure

```bash
cd ~/.claude/skills/course-generator-handwritten/engine
npm i
cp .env.example .env   # set TTS_API_KEY, TTS_MODEL, TTS_VOICE (optionally TTS_URL)
```

`.env` is gitignored. Never commit keys.

## Use

In Claude Code, either call the skill directly:

```
/course-generator-handwritten Make a 3-lecture course on vector databases
```

or just ask, and Claude picks the skill up automatically:

```
Turn the attached PDF into a handwritten explainer course, one video per chapter.
```

Claude researches the topic, writes the lecture specs, voices them, checks the layouts and renders. You get numbered MP4s with subtitles.
