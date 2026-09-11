"""packs-check.py runs a pack's deterministic checks and never blocks a step."""
import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "..", "skills", "cw-packs", "scripts", "packs-check.py")


def run(pack_dir, text):
    proc = subprocess.run([sys.executable, SCRIPT, "--pack-dir", pack_dir, "--text", text], capture_output=True, text=True)
    return json.loads(proc.stdout), proc.returncode


class PacksCheckTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.tmp, "checks"))

    def write(self, name, content):
        with open(os.path.join(self.tmp, "checks", name), "w") as fh:
            fh.write(content)

    def test_findings_carry_span_suggestion_and_citation_fields(self):
        self.write("house.json", json.dumps([{"id": "percent", "pattern": r"(\d+)%", "replace": r"\1 percent", "note": "spell out"}]))
        out, code = run(self.tmp, "Only 95% agree.")
        self.assertEqual(code, 0)
        self.assertEqual(out["checks_loaded"], 1)
        f = out["findings"][0]
        self.assertEqual((f["id"], f["before"], f["after"], f["start"], f["end"]), ("percent", "95%", "95 percent", 5, 8))
        self.assertEqual(f["check"], "house.json")

    def test_bad_pattern_is_a_warning_not_a_failure(self):
        self.write("bad.json", json.dumps([{"id": "broken", "pattern": "("}, {"id": "ok", "pattern": "x"}]))
        out, code = run(self.tmp, "x marks")
        self.assertEqual(code, 0)
        self.assertEqual(out["checks_loaded"], 1)
        self.assertTrue(any("bad pattern" in w for w in out["warnings"]))

    def test_pack_without_checks_yields_nothing(self):
        os.rmdir(os.path.join(self.tmp, "checks"))
        out, code = run(self.tmp, "anything")
        self.assertEqual((code, out["checks_loaded"], out["findings"]), (0, 0, []))


if __name__ == "__main__":
    unittest.main()
