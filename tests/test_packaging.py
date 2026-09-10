"""Packaging invariants from ARCHITECTURE.md that this tree must keep.

- Every skill and compatibility command carries frontmatter with only the
  shared Agent Skills fields, `name` and `description`.
- Every declared `name` uses the `cw-<name>` convention and matches its skill
  folder or command file name.
- The writing-home scaffold stays the deliberate four-surface minimum.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS = REPO_ROOT / "skills"
COMMANDS = REPO_ROOT / "commands"
PROJECT_TEMPLATE = REPO_ROOT / "defaults" / "project-template"

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
        self.assertIsNone(NAME_RE.match("cr:compound"))
        self.assertIsNone(NAME_RE.match("cw:compound"))
        self.assertIsNotNone(NAME_RE.match("cw-compound"))

    def test_packs_skill_ships_its_resolver_and_templates(self) -> None:
        packs = SKILLS / "cw-packs"
        for relative in ("SKILL.md", "scripts/packs-resolve.py", "assets/pack-rule-template.md", "references/config-template.yaml"):
            self.assertTrue((packs / relative).is_file(), relative)
        self.assertTrue((REPO_ROOT / "references" / "packs.md").is_file())


class WritingHomeScaffoldTests(unittest.TestCase):
    def test_project_template_is_the_four_surface_minimum(self) -> None:
        files = sorted(str(p.relative_to(PROJECT_TEMPLATE)) for p in PROJECT_TEMPLATE.rglob("*") if p.is_file())
        self.assertEqual(files, ["STYLE.md", "VOICE.md", "drafts/README.md", "examples/README.md"])


if __name__ == "__main__":
    unittest.main()
