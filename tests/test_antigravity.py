"""Check native Antigravity packaging without installing or calling a model.

Run with: python3 -m unittest discover -s tests -p 'test_antigravity.py' -v
The loader check is skipped when the optional `agy` CLI is unavailable.
"""

import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
AGY = shutil.which("agy")


class AntigravityPackagingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix="cw-antigravity-")
        cls.addClassCleanup(cls.temp.cleanup)
        cls.workspace = Path(cls.temp.name).resolve() / "writer workspace"
        cls.workspace.mkdir()
        cls.plugin = cls.workspace / ".agents" / "plugins" / "compound-writing"
        shutil.copytree(ROOT, cls.plugin, ignore=shutil.ignore_patterns(".git", "__pycache__"))
        cls.skills = sorted((cls.plugin / "skills").glob("*/SKILL.md"))
        cls.manifest = json.loads(
            (cls.plugin / ".antigravity-plugin" / "plugin.json").read_text(encoding="utf-8")
        )

    def test_native_manifest_preserves_product_identity(self):
        for host in (".claude-plugin", ".codex-plugin"):
            manifest = json.loads((self.plugin / host / "plugin.json").read_text(encoding="utf-8"))
            for field in ("name", "version", "description", "repository", "license"):
                with self.subTest(host=host, field=field):
                    self.assertEqual(self.manifest[field], manifest[field])

        # Catch host-specific metadata accidentally copied into the native schema.
        allowed_fields = {
            "$schema", "name", "displayName", "description", "version", "disabled",
            "logo", "suggestedPrompts", "skills", "author", "homepage", "repository",
            "license", "keywords", "extensions",
        }
        self.assertFalse(set(self.manifest) - allowed_fields)
        self.assertEqual(self.manifest["$schema"], "https://antigravity.google/schemas/v1/plugin.json")
        self.assertNotIn("skills", self.manifest, "The canonical skills/ directory is discovered by default")
        prompts = self.manifest["suggestedPrompts"]
        self.assertGreater(len(prompts), 0)
        self.assertLessEqual(len(prompts), 3)
        self.assertTrue(all(isinstance(prompt, str) and prompt.strip() for prompt in prompts))
        logo = (self.plugin / self.manifest["logo"]).resolve()
        self.assertTrue(logo.is_relative_to(self.plugin.resolve()))
        self.assertTrue(logo.is_file())

    def test_canonical_skills_have_portable_discovery_metadata(self):
        self.assertTrue(self.skills)
        for skill in self.skills:
            with self.subTest(skill=skill.parent.name):
                text = skill.read_text(encoding="utf-8")
                match = re.match(r"\A---\n(.*?)\n---(?:\n|$)", text, re.DOTALL)
                self.assertIsNotNone(match, "Skill needs YAML frontmatter")
                fields = dict(re.findall(r"^([a-z][a-z-]*):[ \t]*(.*)$", match.group(1), re.MULTILINE))
                self.assertEqual(set(fields), {"name", "description"})
                name = fields["name"].strip("\"'")
                self.assertRegex(name, r"^cw-[a-z0-9]+(?:-[a-z0-9]+)*$")
                self.assertLessEqual(len(name), 64)
                self.assertEqual(name, skill.parent.name)
                self.assertTrue(fields["description"].strip())
                self.assertLessEqual(len(fields["description"]), 1024)

    def test_relocated_skills_keep_shared_and_nested_resources(self):
        shared = set()
        nested = set()
        for skill in self.skills:
            references = re.findall(
                r"`((?:\.\./)*(?:references|assets|scripts)/[^`\s<>]+)`",
                skill.read_text(encoding="utf-8"),
            )
            for relative in references:
                with self.subTest(skill=skill.parent.name, reference=relative):
                    resolved = (skill.parent / relative).resolve()
                    self.assertTrue(resolved.is_relative_to(self.plugin.resolve()))
                    self.assertTrue(resolved.is_file(), str(resolved))
                    (shared if relative.startswith("../") else nested).add(resolved)
        self.assertIn(self.plugin / "references" / "context-contract.md", shared)
        self.assertIn(self.plugin / "skills" / "cw-ai-check" / "references" / "ai_tells_lexicon.csv", nested)

    def test_relocated_setup_creates_home_and_preserves_writer_files(self):
        script = self.plugin / "skills" / "cw-setup-project" / "scripts" / "create_project.py"
        target = self.workspace / "writing home"

        def setup(*flags):
            return subprocess.run(
                [sys.executable, str(script), str(target), *flags],
                cwd=self.workspace, capture_output=True, text=True, timeout=30,
            )

        result = setup()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual({item.name for item in target.iterdir()}, {"VOICE.md", "STYLE.md", "examples", "drafts"})
        voice = target / "VOICE.md"
        voice.write_text("Writer-owned voice instructions.\n", encoding="utf-8")
        result = setup("--with-audience")
        self.assertNotEqual(result.returncode, 0, "Existing homes require --add-missing")
        self.assertFalse((target / "AUDIENCE.md").exists())

        result = setup("--add-missing", "--with-audience")
        self.assertEqual(result.returncode, 0, result.stderr)
        audience = target / "AUDIENCE.md"
        self.assertEqual(audience.read_bytes(), (self.plugin / "defaults/project-template/AUDIENCE.md").read_bytes())
        audience.write_text("Writer-owned reader observations.\n", encoding="utf-8")
        result = setup("--add-missing", "--with-audience")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(voice.read_text(encoding="utf-8"), "Writer-owned voice instructions.\n")
        self.assertEqual(audience.read_text(encoding="utf-8"), "Writer-owned reader observations.\n")

    @unittest.skipUnless(AGY, "Antigravity CLI is not installed; static packaging checks still run")
    def test_native_loader_discovers_all_skills_without_unexpected_findings(self):
        result = subprocess.run(
            [AGY, "plugin", "validate", "--json", str(self.plugin)],
            cwd=self.workspace, capture_output=True, text=True, timeout=30,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["manifest"], ".antigravity-plugin/plugin.json")
        self.assertEqual(report["components"]["skills"], len(self.skills))
        # Nested Claude execution adapters are not native Antigravity agents.
        self.assertEqual(report["components"]["agents"], 0)
        unexpected = [
            finding for finding in report["findings"]
            if finding["severity"] == "error"
            or (finding["severity"] == "warning" and not (
                finding["file"] == "commands"
                and finding["message"].startswith("never loaded: plugins have no commands.")
            ))
        ]
        self.assertEqual(unexpected, [], json.dumps(unexpected, indent=2))


if __name__ == "__main__":
    unittest.main()
