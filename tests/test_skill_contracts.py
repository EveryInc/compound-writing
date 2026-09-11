"""Prose contracts the pack tests on PR #3 found missing or ambiguous.

Skills are prose an agent follows, so these pin the load-bearing sentences:
a rewrite that drops one of them would reopen the reported bug.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    return (REPO_ROOT / relative).read_text(encoding="utf-8")


class SaveSkillContracts(unittest.TestCase):
    text = read("skills/cw-save/SKILL.md")

    def test_pack_writes_are_always_previewed_even_for_explicit_requests(self) -> None:
        self.assertIn("always show the complete file first", self.text)
        self.assertIn("even when the request was explicit", self.text)

    def test_two_writable_packs_require_a_choice(self) -> None:
        self.assertIn("With more than one writable pack, name each with its existing rules and ask", self.text)
        self.assertIn("never choose silently", self.text)

    def test_non_interactive_is_defined_and_never_writes_a_pack(self) -> None:
        self.assertIn("`mode:non-interactive`", self.text)
        self.assertIn("A non-interactive run never writes into a pack", self.text)

    def test_rule_files_get_short_names_and_yaml_safe_titles(self) -> None:
        self.assertIn("short kebab-case name", self.text)
        self.assertIn("revise that file instead of adding a second", self.text)
        self.assertIn("double quotes", self.text)


class PacksSkillContracts(unittest.TestCase):
    text = read("skills/cw-packs/SKILL.md")

    def test_scaffold_is_done_only_when_the_pack_line_appears(self) -> None:
        self.assertIn("only when the output contains a `pack <id>` line", self.text)
        self.assertIn("outside the packs: block", self.text)

    def test_empty_packs_list_is_replaced_before_appending(self) -> None:
        self.assertIn("When the live key is `packs: []`, replace it with `packs:`", self.text)

    def test_previews_name_the_home_and_config_path(self) -> None:
        self.assertIn("names the resolved home and the absolute path of the config file", self.text)

    def test_home_rule_matches_the_resolver(self) -> None:
        self.assertIn("A checkout nested inside a home inherits the home", self.text)


class ConsumerContracts(unittest.TestCase):
    def test_voice_check_reports_resolution_problems_once(self) -> None:
        self.assertIn("belong in the handoff only, not in the sources list", read("skills/cw-voice-check/SKILL.md"))

    def test_contract_names_only_matched_rules_and_carves_out_onboarding(self) -> None:
        contract = read("references/context-contract.md")
        self.assertIn("Name only the rules that matched", contract)
        self.assertIn("except `cw-onboarding`", contract)
        self.assertIn("a consuming step needs only this section", contract)

    def test_guide_example_fires_while_drafting(self) -> None:
        guide = read("references/packs.md")
        example = re.search(r"earn-the-ending\.md -->\n---\n(.*?)\n---", guide, re.S)
        self.assertIsNotNone(example)
        self.assertIn("writing the ending of an argumentative piece", example.group(1))

    def test_alias_is_documented_as_claude_code_only(self) -> None:
        self.assertIn("Claude Code command", read("commands/cw-compound.md"))
        self.assertIn("Codex packages skills only", read("README.md"))


if __name__ == "__main__":
    unittest.main()
