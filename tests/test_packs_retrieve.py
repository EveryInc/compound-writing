"""packs-retrieve.py ranks a pack's before/after examples against one paragraph."""
import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "..", "skills", "cw-packs", "scripts", "packs-retrieve.py")


def run(pack_dir, text, k=6):
    proc = subprocess.run([sys.executable, SCRIPT, "--pack-dir", pack_dir, "--text", text, "--k", str(k)], capture_output=True, text=True)
    return json.loads(proc.stdout), proc.returncode


class PacksRetrieveTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.tmp, "examples"))

    def write(self, name, items):
        with open(os.path.join(self.tmp, "examples", name), "w") as fh:
            for item in items:
                fh.write(json.dumps(item) + "\n")

    def test_shared_changed_token_wins_and_topic_overlap_counts_for_nothing(self):
        self.write("moves.jsonl", [
            {"before": "The model is actually quite fast.", "after": "The model is quite fast.", "type": "insert_delete"},
            {"before": "The model shipped on Tuesday to great fanfare.", "after": "The model shipped on Tuesday to fanfare.", "type": "insert_delete"},
            {"before": "Our new model is the fastest one yet, they said.", "after": "Our new model is the fastest yet, they said.", "type": "insert_delete"},
        ])
        out, code = run(self.tmp, "Our new model is actually the fastest thing yet.")
        self.assertEqual(code, 0)
        self.assertEqual(out["examples_loaded"], 3)
        # "actually" was the whole change in the first example; the third shares the
        # topic words but the editor changed "one", which the paragraph lacks.
        self.assertEqual([e["before"] for e in out["examples"]], ["The model is actually quite fast."])
        self.assertEqual(set(out["examples"][0]), {"pack", "file", "before", "after", "type", "note", "score"})

    def test_no_shared_changed_token_returns_nothing(self):
        self.write("moves.jsonl", [{"before": "Zebras graze.", "after": "Zebras graze quietly."}])
        out, _ = run(self.tmp, "Zebras graze in the quarterly revenue report.")
        self.assertEqual(out["examples"], [])

    def test_malformed_line_is_a_warning_and_k_caps_results(self):
        self.write("moves.jsonl", [{"before": "It is very good.", "after": "It is good."}, {"before": "It is very bad.", "after": "It is bad."}])
        with open(os.path.join(self.tmp, "examples", "moves.jsonl"), "a") as fh:
            fh.write("not json\n")
        out, code = run(self.tmp, "It is very late.", k=1)
        self.assertEqual(code, 0)
        self.assertEqual(len(out["examples"]), 1)
        self.assertTrue(any("not JSON" in w for w in out["warnings"]))

    def test_pack_without_examples_yields_nothing(self):
        os.rmdir(os.path.join(self.tmp, "examples"))
        out, code = run(self.tmp, "anything")
        self.assertEqual((code, out["examples_loaded"], out["examples"]), (0, 0, []))


if __name__ == "__main__":
    unittest.main()
