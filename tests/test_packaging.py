"""Packaging invariants from ARCHITECTURE.md that this tree must keep.

- Every skill and compatibility command carries frontmatter with only the
  shared Agent Skills fields, `name` and `description`.
- Every declared `name` uses the `cw-<name>` convention and matches its skill
  folder or command file name.
- The writing-home scaffold stays the deliberate four-surface minimum.
"""

from __future__ import annotations

import json
import re
import shutil
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS = REPO_ROOT / "skills"
COMMANDS = REPO_ROOT / "commands"
PROJECT_TEMPLATE = REPO_ROOT / "defaults" / "project-template"
ALLOWLIST = REPO_ROOT / "release" / "allowlist.json"
CONFIG_TEMPLATE = REPO_ROOT / "skills" / "cw-packs" / "references" / "config-template.yaml"
CONFIG_EXAMPLE = REPO_ROOT / ".compound-writing" / "config.example.yaml"

NAME_RE = re.compile(r"^cw-[a-z0-9]+(?:-[a-z0-9]+)*$")
ALLOWED_FIELDS = {"name", "description"}


def read_frontmatter(path: Path) -> dict[str, str]:
    """Return the `key: value` pairs of the leading `---` block, or raise."""
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        raise AssertionError(f"{path}: missing opening frontmatter fence")
    fields: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return fields
        if not line.strip() or line.startswith((" ", "\t")):
            continue
        key, sep, value = line.partition(":")
        if not sep:
            raise AssertionError(f"{path}: frontmatter line without a key: {line!r}")
        fields[key.strip()] = value.strip().strip('"')
    raise AssertionError(f"{path}: frontmatter never closes")


def check_surface(path: Path, expected_name: str) -> None:
    fields = read_frontmatter(path)
    unexpected = set(fields) - ALLOWED_FIELDS
    if unexpected:
        raise AssertionError(f"{path}: frontmatter carries non-shared fields {sorted(unexpected)}")
    if fields.get("name") != expected_name:
        raise AssertionError(f"{path}: name {fields.get('name')!r} does not match {expected_name!r}")
    if not NAME_RE.match(expected_name):
        raise AssertionError(f"{path}: {expected_name!r} does not follow the cw-<name> convention")
    if not fields.get("description"):
        raise AssertionError(f"{path}: description is empty")


class SkillPackagingTests(unittest.TestCase):
    def test_every_skill_has_shared_frontmatter_and_matching_name(self) -> None:
        skill_dirs = sorted(p for p in SKILLS.iterdir() if p.is_dir())
        self.assertGreater(len(skill_dirs), 30)
        for skill_dir in skill_dirs:
            with self.subTest(skill=skill_dir.name):
                check_surface(skill_dir / "SKILL.md", skill_dir.name)

    def test_every_command_has_shared_frontmatter_and_matching_name(self) -> None:
        commands = sorted(COMMANDS.glob("*.md"))
        self.assertIn(COMMANDS / "cw-compound.md", commands)
        for command in commands:
            with self.subTest(command=command.name):
                check_surface(command, command.stem)

    def test_colon_separated_name_violates_the_convention(self) -> None:
        tmp = Path(tempfile.mkdtemp(prefix="cw-packaging-test-"))
        self.addCleanup(shutil.rmtree, tmp, True)
        for index, name in enumerate(("cr:compound", "cw:compound", "compound")):
            skill = tmp / f"rejected-{index}"
            skill.mkdir()
            (skill / "SKILL.md").write_text(f"---\nname: {name}\ndescription: alias\n---\n", encoding="utf-8")
            with self.subTest(name=name), self.assertRaises(AssertionError):
                check_surface(skill / "SKILL.md", name)
        ok = tmp / "cw-compound"
        ok.mkdir()
        (ok / "SKILL.md").write_text("---\nname: cw-compound\ndescription: alias\n---\n", encoding="utf-8")
        check_surface(ok / "SKILL.md", "cw-compound")

    def test_packs_skill_ships_its_resolver_and_templates(self) -> None:
        packs = SKILLS / "cw-packs"
        for relative in ("SKILL.md", "scripts/packs-resolve.py", "assets/pack-rule-template.md", "references/config-template.yaml"):
            self.assertTrue((packs / relative).is_file(), relative)
        self.assertTrue((REPO_ROOT / "references" / "packs.md").is_file())


class PublicAllowlistTests(unittest.TestCase):
    """release/allowlist.json is the explicit list of what the public package ships.

    The tree and the list must agree in both directions: a skill or command
    that is not listed does not belong in the public repository, and a listed
    name that has no folder or file is a stale entry.
    """

    allowlist = json.loads(ALLOWLIST.read_text(encoding="utf-8"))

    def test_skills_match_the_allowlist_exactly(self) -> None:
        on_disk = sorted(p.name for p in SKILLS.iterdir() if p.is_dir())
        self.assertEqual(on_disk, self.allowlist["skills"])

    def test_commands_match_the_allowlist_exactly(self) -> None:
        on_disk = sorted(p.stem for p in COMMANDS.glob("*.md"))
        self.assertEqual(on_disk, self.allowlist["commands"])

    def test_allowlist_is_sorted_and_unique(self) -> None:
        for key in ("skills", "commands"):
            names = self.allowlist[key]
            self.assertEqual(names, sorted(set(names)), key)

    def test_packs_surfaces_are_allowlisted(self) -> None:
        self.assertIn("cw-packs", self.allowlist["skills"])
        self.assertIn("cw-compound", self.allowlist["commands"])


class ConfigExampleTests(unittest.TestCase):
    def test_root_example_config_matches_the_template_cw_packs_copies(self) -> None:
        self.assertEqual(CONFIG_EXAMPLE.read_bytes(), CONFIG_TEMPLATE.read_bytes())

    def test_example_config_declares_nothing_live(self) -> None:
        live = [line for line in CONFIG_TEMPLATE.read_text(encoding="utf-8").splitlines() if line.strip() and not line.startswith("#")]
        self.assertEqual(live, [])


class WritingHomeScaffoldTests(unittest.TestCase):
    def test_project_template_is_the_four_surface_minimum(self) -> None:
        files = sorted(str(p.relative_to(PROJECT_TEMPLATE)) for p in PROJECT_TEMPLATE.rglob("*") if p.is_file())
        self.assertEqual(files, ["STYLE.md", "VOICE.md", "drafts/README.md", "examples/README.md"])


if __name__ == "__main__":
    unittest.main()
