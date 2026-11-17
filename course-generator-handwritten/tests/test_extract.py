"""Tests for engine/extract.js: narration extraction, spec checks and the lecture length guide.

Run from the repository root:
    python3 -m unittest discover -s course-generator-handwritten/tests

The tests call Node, so they are skipped when `node` is not installed.
"""
import json
import os
import shutil
import subprocess
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
AGENT = os.path.dirname(HERE)
EXTRACT = os.path.join(AGENT, "engine", "extract.js")
EXAMPLES = os.path.join(AGENT, "examples")


def words(n):
    return " ".join(["word"] * n)


def spec(beat_words=40, check=False):
    """A minimal, valid lecture spec. `beat_words` sets the length of the one section beat."""
    lines = [
        "const LECT = { label: 'Lecture 1 · test', title: 'A Test Lecture' };",
        "const LAYERS = ['First', 'Second'];",
        "say({ hook: 'A hook.', title: 'A title.', recap: 'A recap.', outro: 'Next, more.' });",
        "intro('S01_Intro', 'hook', 'title', [['big', 'Hook', 'y', 70]]);",
        "section('S02_First', 0, 'v', [",
        f"  {{ b: 'fi1', t: 'First idea', say: '{words(beat_words)}', v: [['text', 'one idea', 'w']] }},",
        "]);",
    ]
    if check:
        lines += [
            "section('S03_Check', null, 'y', [",
            "  { b: 'ck1', t: 'Quick check', say: 'Pause the video and answer: what is the first idea?', v: [['big', 'What is the first idea?', 'y', 64]] },",
            "], 'Quick check');",
        ]
    lines.append("recap('S04_Recap', 'recap', 'outro', ['one line'], 'Next lecture');")
    return "\n".join(lines) + "\n"


@unittest.skipUnless(shutil.which("node"), "node is not installed")
class ExtractTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp)

    def run_extract(self, text, env_extra=None, lecture="L01_Test"):
        os.makedirs(os.path.join(self.tmp, lecture), exist_ok=True)
        with open(os.path.join(self.tmp, lecture, "spec.js"), "w", encoding="utf-8") as f:
            f.write(text)
        env = dict(os.environ)
        env.pop("LECTURE_MAX_MIN", None)
        env.update(env_extra or {})
        return subprocess.run(["node", EXTRACT, lecture], cwd=self.tmp, env=env,
                              capture_output=True, text=True)

    def beats(self, lecture="L01_Test"):
        with open(os.path.join(self.tmp, lecture, "beats.json"), encoding="utf-8") as f:
            return json.load(f)

    def test_writes_beats_in_order(self):
        r = self.run_extract(spec())
        self.assertEqual(r.returncode, 0, r.stderr)
        rows = self.beats()
        self.assertEqual([row[1] for row in rows], ["hook", "title", "fi1", "recap", "outro"])
        self.assertEqual([row[0] for row in rows],
                         ["S01_Intro", "S01_Intro", "S02_First", "S04_Recap", "S04_Recap"])
        self.assertEqual(rows[0][2], "A hook.")

    def test_short_lecture_has_no_length_warning(self):
        r = self.run_extract(spec(beat_words=40))
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertNotIn("LONG", r.stdout)

    def test_long_lecture_warns(self):
        # 1,000 words at the engine's 2.65 words a second is about 6.3 minutes of speech.
        r = self.run_extract(spec(beat_words=1000))
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("LONG L01_Test", r.stdout)
        self.assertIn("6 min guide", r.stdout)

    def test_warning_does_not_block_the_build(self):
        r = self.run_extract(spec(beat_words=1000))
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertTrue(os.path.exists(os.path.join(self.tmp, "L01_Test", "beats.json")))

    def test_length_guide_can_be_overridden(self):
        r = self.run_extract(spec(beat_words=1000), {"LECTURE_MAX_MIN": "8"})
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertNotIn("LONG", r.stdout)

    def test_quick_check_section_without_a_layer(self):
        r = self.run_extract(spec(check=True))
        self.assertEqual(r.returncode, 0, r.stderr)
        rows = self.beats()
        self.assertIn(["S03_Check", "ck1", "Pause the video and answer: what is the first idea?"], rows)
        self.assertEqual([row[1] for row in rows][-3:], ["ck1", "recap", "outro"])

    def test_missing_narration_fails(self):
        r = self.run_extract(spec().replace("say: '", "sayx: '", 1))
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("missing say", r.stderr)

    def test_duplicate_beat_ids_fail(self):
        text = spec().replace("]);\nrecap", "  { b: 'fi1', t: 'Again', say: 'Again.', v: [] },\n]);\nrecap", 1)
        r = self.run_extract(text)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("dup beat ids", r.stderr)

    def test_shipped_examples_extract_and_fit_the_length_guide(self):
        for name in ("agents-L00-spec.js", "inference-B4-spec.js"):
            with self.subTest(example=name):
                lecture = "Ex_" + name.split("-")[0]
                with open(os.path.join(EXAMPLES, name), encoding="utf-8") as f:
                    r = self.run_extract(f.read(), lecture=lecture)
                self.assertEqual(r.returncode, 0, r.stderr)
                self.assertNotIn("LONG", r.stdout)
                self.assertGreater(len(self.beats(lecture)), 5)


if __name__ == "__main__":
    unittest.main()
