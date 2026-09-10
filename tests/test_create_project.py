"""Behavior of skills/cw-setup-project/scripts/create_project.py.

The script owns the writing-home scaffold, so its tests pin the four-surface
minimum, the never-overwrite rule, and the opt-in packs config.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "skills" / "cw-setup-project" / "scripts" / "create_project.py"
PACKS_TEMPLATE = REPO_ROOT / "skills" / "cw-packs" / "references" / "config-template.yaml"
FOUR_SURFACES = ["STYLE.md", "VOICE.md", "drafts/README.md", "examples/README.md"]


def files_under(root: Path) -> list[str]:
    return sorted(str(p.relative_to(root)) for p in root.rglob("*") if p.is_file())


class CreateProjectTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="cw-create-project-"))
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.home = self.tmp / "home"

    def run_script(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(self.home), *args],
            capture_output=True,
            text=True,
            timeout=60,
        )

    def test_default_scaffold_is_the_four_surfaces_and_nothing_else(self) -> None:
        proc = self.run_script()
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(files_under(self.home), FOUR_SURFACES)
        self.assertFalse((self.home / ".compound-writing").exists())

    def test_with_packs_adds_the_config_from_the_template(self) -> None:
        proc = self.run_script("--with-packs")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        config = self.home / ".compound-writing" / "config.yaml"
        self.assertEqual(config.read_bytes(), PACKS_TEMPLATE.read_bytes())
        self.assertEqual(files_under(self.home), [".compound-writing/config.yaml", *FOUR_SURFACES])
        self.assertIn(".compound-writing/config.yaml", proc.stdout)

    def test_non_empty_target_is_refused_without_add_missing(self) -> None:
        self.home.mkdir()
        (self.home / "notes.md").write_text("mine\n", encoding="utf-8")
        proc = self.run_script("--with-packs")
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("--add-missing", proc.stderr)
        self.assertEqual(files_under(self.home), ["notes.md"])

    def test_add_missing_with_packs_never_overwrites(self) -> None:
        self.home.mkdir()
        (self.home / "VOICE.md").write_text("# mine\n", encoding="utf-8")
        (self.home / ".compound-writing").mkdir()
        (self.home / ".compound-writing" / "config.yaml").write_text("packs:\n  - source: house\n", encoding="utf-8")
        proc = self.run_script("--add-missing", "--with-packs")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual((self.home / "VOICE.md").read_text(encoding="utf-8"), "# mine\n")
        self.assertEqual((self.home / ".compound-writing" / "config.yaml").read_text(encoding="utf-8"), "packs:\n  - source: house\n")
        self.assertIn("Preserved existing:", proc.stdout)
        self.assertIn(".compound-writing/config.yaml", proc.stdout)
        self.assertTrue((self.home / "STYLE.md").is_file())


if __name__ == "__main__":
    unittest.main()
