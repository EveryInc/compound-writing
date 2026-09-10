"""Behavioral tests for skills/cw-packs/scripts/packs-resolve.py.

The script has a hyphenated name, so every test drives it through a
subprocess and parses the single JSON object it prints.
"""

from __future__ import annotations

import functools
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
RESOLVER = REPO_ROOT / "skills" / "cw-packs" / "scripts" / "packs-resolve.py"
IS_ROOT = hasattr(os, "geteuid") and os.geteuid() == 0
GIT_ISOLATION = {"GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_SYSTEM": os.devnull}

# Loads the hyphen-named script as a module for the few in-process probes
# (regex groups, cache-root repair); everything else goes through a subprocess.
IMPORT_RESOLVER = (
    "import importlib.util\n"
    f"spec = importlib.util.spec_from_file_location('pr', {str(RESOLVER)!r})\n"
    "m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)\n"
)

RULE = textwrap.dedent(
    """\
    ---
    title: {title}
    applies_when:
      - judging whether a piece is ready to publish
    tags: [endings]
    ---

    {title}. The last paragraph must extend the argument, not recap it.
    """
)

NOTE_WITHOUT_FRONTMATTER = "Just a note, not a rule.\n"


@functools.lru_cache(maxsize=None)
def git_supports_end_of_options() -> bool:
    if shutil.which("git") is None:
        return False
    proc = subprocess.run(["git", "--version"], capture_output=True, text=True)
    parts = proc.stdout.strip().split()[-1].split(".")
    try:
        major, minor = int(parts[0]), int(parts[1])
    except (IndexError, ValueError):
        return False
    return (major, minor) >= (2, 24)


class ResolverHarness(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="cw-packs-test-"))
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.home = self.tmp / "home"
        self.home.mkdir()
        self.cache = self.tmp / "cache"

    def write(self, relative: str, content: str) -> Path:
        path = self.home / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def config(self, body: str, name: str = "config.yaml") -> Path:
        return self.write(f".compound-writing/{name}", textwrap.dedent(body))

    def pack(self, relative: str, *rules: str, readme: bool = True) -> Path:
        directory = self.home / relative
        directory.mkdir(parents=True, exist_ok=True)
        if readme:
            (directory / "README.md").write_text("House style pack.\n", encoding="utf-8")
        for title in rules:
            slug = title.lower().replace(" ", "-")
            (directory / f"{slug}.md").write_text(RULE.format(title=title), encoding="utf-8")
        return directory

    def resolver_env(self, env_extra: dict | None = None) -> dict:
        env = dict(os.environ)
        env["CW_PACKS_CACHE_ROOT"] = str(self.cache)
        env["CW_PACKS_GIT_TIMEOUT"] = "30"
        # Keep home discovery inside the sandbox even when the system tempdir
        # itself sits under a git checkout.
        env["GIT_CEILING_DIRECTORIES"] = str(self.tmp.resolve())
        env.update(GIT_ISOLATION)
        if env_extra:
            env.update(env_extra)
        return env

    def parse_output(self, proc: subprocess.CompletedProcess) -> dict:
        self.assertEqual(proc.returncode, 0, proc.stderr)
        lines = [line for line in proc.stdout.splitlines() if line.strip()]
        self.assertEqual(len(lines), 1, f"expected one JSON line, got: {proc.stdout!r}")
        return json.loads(lines[0])

    def run_resolver(self, *args: str, cwd: Path | None = None, env_extra: dict | None = None) -> dict:
        proc = subprocess.run(
            [sys.executable, str(RESOLVER), *args],
            cwd=str(cwd or self.home),
            env=self.resolver_env(env_extra),
            capture_output=True,
            text=True,
            timeout=60,
        )
        return self.parse_output(proc)

    def run_probe(self, code: str, cwd: Path | None = None) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, "-c", IMPORT_RESOLVER + code],
            cwd=str(cwd or self.home),
            env=self.resolver_env(),
            capture_output=True,
            text=True,
            timeout=60,
        )

    def git(self, cwd: Path, *args: str) -> str:
        proc = subprocess.run(
            ["git", "-c", "user.name=t", "-c", "user.email=t@example.com", "-C", str(cwd), *args],
            env={**os.environ, **GIT_ISOLATION},
            capture_output=True,
            text=True,
            check=True,
        )
        return proc.stdout.strip()

    def make_pack_repo(self, name: str, packs: dict, subfolder: str = "") -> Path:
        """A git repo tagged v1 publishing `packs` ({pack dir: [rule titles]}) under `subfolder`."""
        repo = self.tmp / name
        repo.mkdir()
        for pack, titles in packs.items():
            target = repo / subfolder / pack if pack else repo / subfolder
            target.mkdir(parents=True, exist_ok=True)
            for title in titles:
                slug = title.lower().replace(" ", "-")
                (target / f"{slug}.md").write_text(RULE.format(title=title), encoding="utf-8")
        self.git(repo, "init", "-q")
        self.git(repo, "add", "-A")
        self.git(repo, "commit", "-q", "-m", "packs")
        self.git(repo, "tag", "v1")
        return repo

    def recommit(self, repo: Path, message: str) -> None:
        self.git(repo, "add", "-A")
        self.git(repo, "commit", "-q", "-m", message)
        self.git(repo, "tag", "-f", "v1")

    @staticmethod
    def file_url(repo: Path) -> str:
        return repo.resolve().as_uri()


class NoConfigTests(ResolverHarness):
    def test_no_home_and_no_repo_yields_empty_result(self) -> None:
        bare = self.tmp / "bare"
        bare.mkdir()
        result = self.run_resolver(cwd=bare)
        self.assertEqual(result["roots"], [])
        self.assertEqual(result["entries"], 0)
        self.assertEqual(result["errors"], [])
        self.assertIsNone(result["home"])
        self.assertEqual(len(result["warnings"]), 1)
        self.assertIn("no writing home", result["warnings"][0])

    def test_home_without_packs_key_is_silent(self) -> None:
        self.config("docs_root: notes\n")
        result = self.run_resolver()
        self.assertEqual(result, {"roots": [], "warnings": [], "errors": [], "entries": 0, "home": str(self.home.resolve())})

    def test_checkout_toplevel_is_the_fallback_home(self) -> None:
        repo = self.tmp / "repo"
        (repo / "sub" / "deeper").mkdir(parents=True)
        (repo / ".git").mkdir()
        result = self.run_resolver(cwd=repo / "sub" / "deeper")
        self.assertEqual(result["home"], str(repo.resolve()))
        self.assertEqual(result["entries"], 0)
        self.assertEqual(result["warnings"], [])

    def test_worktree_git_file_marks_the_checkout(self) -> None:
        repo = self.tmp / "worktree"
        (repo / "sub").mkdir(parents=True)
        (repo / ".git").write_text("gitdir: /elsewhere/.git/worktrees/x\n", encoding="utf-8")
        result = self.run_resolver(cwd=repo / "sub")
        self.assertEqual(result["home"], str(repo.resolve()))

    def test_config_inside_checkout_wins_over_checkout_root(self) -> None:
        repo = self.tmp / "repo"
        nested = repo / "writing"
        (nested / ".compound-writing").mkdir(parents=True)
        (repo / ".git").mkdir()
        result = self.run_resolver(cwd=nested)
        self.assertEqual(result["home"], str(nested.resolve()))

    def test_ceiling_directory_stops_the_walk(self) -> None:
        above = self.tmp / "above"
        (above / ".compound-writing").mkdir(parents=True)
        below = above / "work" / "deep"
        below.mkdir(parents=True)
        result = self.run_resolver(cwd=below, env_extra={"GIT_CEILING_DIRECTORIES": str(above.resolve())})
        self.assertIsNone(result["home"])


class PathSourceTests(ResolverHarness):
    def test_home_relative_pack_publishes_rules_and_ignores_readme(self) -> None:
        self.pack("compound-packs/house-style", "Earn the ending", "Name the counterargument")
        self.config("packs:\n  - source: compound-packs/house-style\n")
        result = self.run_resolver()
        self.assertEqual(result["errors"], [])
        self.assertEqual(result["warnings"], [])
        self.assertEqual(len(result["roots"]), 1)
        root = result["roots"][0]
        self.assertEqual(root["id"], "house-style")
        self.assertEqual(Path(root["dir"]), (self.home / "compound-packs" / "house-style").resolve())
        self.assertEqual(root["nested_rule_shaped"], 0)
        self.assertNotIn("url", root)

    def test_note_without_frontmatter_is_reported_skipped(self) -> None:
        pack = self.pack("compound-packs/house-style", "Earn the ending")
        (pack / "notes.md").write_text(NOTE_WITHOUT_FRONTMATTER, encoding="utf-8")
        self.config("packs:\n  - source: compound-packs/house-style\n")
        result = self.run_resolver()
        self.assertEqual(len(result["roots"]), 1)
        self.assertTrue(any("skipped pack file `house-style/notes.md`" in w for w in result["warnings"]))

    def test_rules_only_in_subfolder_warn_and_publish_nothing(self) -> None:
        self.pack("compound-packs/house-style/research", "Earn the ending", readme=False)
        (self.home / "compound-packs" / "house-style" / "README.md").write_text("desc\n", encoding="utf-8")
        self.config("packs:\n  - source: compound-packs\n")
        result = self.run_resolver()
        self.assertEqual(result["roots"], [])
        joined = "\n".join(result["warnings"])
        self.assertIn("publishes no packs", joined)
        self.assertIn("rule-shaped file(s) under `research/`", joined)
        self.assertIn("references/packs.md", joined)

    def test_nested_rule_shaped_files_are_counted_not_warned(self) -> None:
        self.pack("compound-packs/house-style", "Earn the ending")
        self.pack("compound-packs/house-style/research", "Draft observation", readme=False)
        self.config("packs:\n  - source: compound-packs/house-style\n")
        result = self.run_resolver()
        self.assertEqual(result["warnings"], [])
        self.assertEqual(result["roots"][0]["nested_rule_shaped"], 1)

    def test_multi_pack_source_publishes_each_child(self) -> None:
        self.pack("packs/voice", "Plain verbs")
        self.pack("packs/style", "Earn the ending")
        self.config("packs:\n  - source: packs\n")
        result = self.run_resolver()
        self.assertEqual(sorted(r["id"] for r in result["roots"]), ["style", "voice"])

    def test_pack_selection_and_id_override(self) -> None:
        self.pack("packs/voice", "Plain verbs")
        self.pack("packs/style", "Earn the ending")
        self.config("packs:\n  - source: packs\n    pack: voice\n    id: every-voice\n")
        result = self.run_resolver()
        self.assertEqual([r["id"] for r in result["roots"]], ["every-voice"])
        self.assertEqual(Path(result["roots"][0]["dir"]), (self.home / "packs" / "voice").resolve())

    def test_id_override_requires_a_single_selected_pack(self) -> None:
        self.pack("packs/voice", "Plain verbs")
        self.pack("packs/style", "Earn the ending")
        self.config("packs:\n  - source: packs\n    pack: [voice, style]\n    id: both\n")
        result = self.run_resolver()
        self.assertEqual(result["roots"], [])
        self.assertTrue(any("requires the entry to install exactly one pack" in e for e in result["errors"]))

    def test_empty_pack_selection_installs_nothing_with_a_warning(self) -> None:
        self.pack("packs/voice", "Plain verbs")
        self.config("packs:\n  - source: packs\n    pack: []\n")
        result = self.run_resolver()
        self.assertEqual(result["roots"], [])
        self.assertEqual(result["errors"], [])
        self.assertTrue(any("lists no ids; nothing installed" in w for w in result["warnings"]))

    def test_zero_indent_list_items_parse(self) -> None:
        self.pack("compound-packs/house-style", "Earn the ending")
        self.config("packs:\n- source: compound-packs/house-style\n")
        result = self.run_resolver()
        self.assertEqual(result["entries"], 1)
        self.assertEqual([r["id"] for r in result["roots"]], ["house-style"])

    def test_bom_and_crlf_config_parses(self) -> None:
        self.pack("compound-packs/house-style", "Earn the ending")
        path = self.home / ".compound-writing" / "config.yaml"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"\xef\xbb\xbfpacks:\r\n  - source: compound-packs/house-style\r\n")
        result = self.run_resolver()
        self.assertEqual(result["errors"], [])
        self.assertEqual([r["id"] for r in result["roots"]], ["house-style"])

    def test_tree_url_conflicting_ref_and_path_are_errors(self) -> None:
        self.config(
            "packs:\n"
            "  - source: https://github.com/org/pack/tree/v1.0.0/packs\n"
            "    ref: v2.0.0\n"
            "  - source: https://github.com/org/pack/tree/v1.0.0/packs\n"
            "    path: other\n"
        )
        result = self.run_resolver()
        self.assertEqual(result["roots"], [])
        self.assertFalse(self.cache.exists() and any(self.cache.iterdir()))
        joined = "\n".join(result["errors"])
        self.assertIn("tree URL pins ref `v1.0.0` but entry says `ref: v2.0.0`", joined)
        self.assertIn("tree URL path `packs` conflicts with `path: other`", joined)

    def test_unpublished_selection_lists_available(self) -> None:
        self.pack("packs/voice", "Plain verbs")
        self.config("packs:\n  - source: packs\n    pack: [voice, missing]\n")
        result = self.run_resolver()
        self.assertEqual(result["roots"], [])
        self.assertTrue(any("missing not published" in e and "available: voice" in e for e in result["errors"]))

    def test_ref_on_path_source_is_an_error(self) -> None:
        self.pack("compound-packs/house-style", "Earn the ending")
        self.config("packs:\n  - source: compound-packs/house-style\n    ref: v1\n")
        result = self.run_resolver()
        self.assertEqual(result["roots"], [])
        self.assertTrue(any("`ref:` is only valid on git sources" in e for e in result["errors"]))

    def test_source_escaping_the_home_is_an_error(self) -> None:
        outside = self.tmp / "outside"
        outside.mkdir()
        (outside / "rule.md").write_text(RULE.format(title="Escaped"), encoding="utf-8")
        self.config("packs:\n  - source: ../outside\n")
        result = self.run_resolver()
        self.assertEqual(result["roots"], [])
        self.assertTrue(any("resolves outside the writing home" in e for e in result["errors"]))

    def test_absolute_source_outside_the_home_is_allowed(self) -> None:
        shared = self.tmp / "shared-packs" / "team"
        shared.mkdir(parents=True)
        (shared / "rule.md").write_text(RULE.format(title="Team rule"), encoding="utf-8")
        self.config(f"packs:\n  - source: {shared}\n")
        result = self.run_resolver()
        self.assertEqual([r["id"] for r in result["roots"]], ["team"])

    @unittest.skipIf(os.name == "nt", "symlinks need privileges on Windows")
    def test_symlink_leaving_the_source_refuses_the_pack(self) -> None:
        pack = self.pack("compound-packs/house-style", "Earn the ending")
        secret = self.tmp / "secret.md"
        secret.write_text(RULE.format(title="Secret"), encoding="utf-8")
        os.symlink(secret, pack / "resources-link.md")
        self.config("packs:\n  - source: compound-packs/house-style\n")
        result = self.run_resolver()
        self.assertEqual(result["roots"], [])
        joined = "\n".join(result["errors"] + result["warnings"])
        self.assertIn("links outside the source", joined)

    def test_duplicate_id_keeps_first_declared(self) -> None:
        self.pack("compound-packs/house-style", "Earn the ending")
        self.pack("personal/house-style", "Plain verbs")
        self.config("packs:\n  - source: compound-packs/house-style\n")
        self.config("packs:\n  - source: personal/house-style\n", name="config.local.yaml")
        result = self.run_resolver()
        self.assertEqual(len(result["roots"]), 1)
        self.assertEqual(Path(result["roots"][0]["dir"]), (self.home / "compound-packs" / "house-style").resolve())
        self.assertTrue(any("duplicate pack id `house-style`" in e and "config.local.yaml" in e for e in result["errors"]))

    def test_home_flag_accepts_a_nested_file_path(self) -> None:
        nested = self.tmp / "repo" / "writing"
        nested.mkdir(parents=True)
        (nested / ".compound-writing").mkdir()
        (nested / ".compound-writing" / "config.yaml").write_text("packs:\n  - source: house\n", encoding="utf-8")
        (nested / "house").mkdir()
        (nested / "house" / "rule.md").write_text(RULE.format(title="Nested rule"), encoding="utf-8")
        draft = nested / "drafts" / "piece" / "draft.md"
        draft.parent.mkdir(parents=True)
        draft.write_text("# Draft\n", encoding="utf-8")
        result = self.run_resolver("--home", str(draft), cwd=self.tmp)
        self.assertEqual(result["home"], str(nested.resolve()))
        self.assertEqual([r["id"] for r in result["roots"]], ["house"])


class DeclaredOnlyTests(ResolverHarness):
    def test_malformed_packs_line_is_declared_with_error(self) -> None:
        self.config("packs: compound-packs/house-style\n")
        result = self.run_resolver("--declared-only")
        self.assertTrue(result["declared"])
        self.assertEqual(result["entries"], 0)
        self.assertTrue(any("must be a block list" in e for e in result["errors"]))
        self.assertEqual(result["home"], str(self.home.resolve()))
        self.assertFalse(self.cache.exists())

    def test_git_entry_is_shape_checked_without_cloning(self) -> None:
        self.config("packs:\n  - source: https://github.com/org/pack\n    ref: v1\n")
        result = self.run_resolver("--declared-only")
        self.assertTrue(result["declared"])
        self.assertEqual(result["entries"], 1)
        self.assertEqual(result["errors"], [])
        self.assertFalse(self.cache.exists())

    def test_no_declaration_is_false(self) -> None:
        self.config("docs_root: notes\n")
        result = self.run_resolver("--declared-only")
        self.assertFalse(result["declared"])

    def test_unknown_key_is_an_error(self) -> None:
        self.config("packs:\n  - source: compound-packs/x\n    stage: draft\n")
        result = self.run_resolver("--declared-only")
        self.assertTrue(any("unknown packs entry key `stage:`" in e for e in result["errors"]))


class GitSourceTests(ResolverHarness):
    def setUp(self) -> None:
        super().setUp()
        if not git_supports_end_of_options():
            self.skipTest("git >= 2.24 required")
        self.remote = self.tmp / "remote-pack"
        self.remote.mkdir()
        (self.remote / "rails").mkdir()
        (self.remote / "rails" / "rule.md").write_text(RULE.format(title="Remote rule"), encoding="utf-8")
        (self.remote / "README.md").write_text("Pack repo\n", encoding="utf-8")
        self.git(self.remote, "init", "-q")
        self.git(self.remote, "add", ".")
        self.git(self.remote, "commit", "-q", "-m", "pack")
        self.git(self.remote, "tag", "v1.0.0")
        self.url = self.remote.resolve().as_uri()

    def test_git_source_without_ref_is_an_error_and_siblings_resolve(self) -> None:
        self.pack("compound-packs/house-style", "Earn the ending")
        self.config(f"packs:\n  - source: {self.url}\n  - source: compound-packs/house-style\n")
        result = self.run_resolver()
        self.assertEqual([r["id"] for r in result["roots"]], ["house-style"])
        self.assertTrue(any("requires `ref:`" in e for e in result["errors"]))

    def test_tagged_git_source_is_cloned_then_cached(self) -> None:
        self.config(f"packs:\n  - source: {self.url}\n    ref: v1.0.0\n")
        first = self.run_resolver()
        self.assertEqual(first["errors"], [])
        self.assertEqual([r["id"] for r in first["roots"]], ["rails"])
        root = first["roots"][0]
        self.assertEqual(root["url"], self.url)
        self.assertEqual(root["ref"], "v1.0.0")
        self.assertTrue(Path(root["dir"]).is_relative_to(self.cache.resolve()))
        cached_dirs = [p for p in self.cache.iterdir() if p.is_dir()]
        self.assertEqual(len(cached_dirs), 1)
        second = self.run_resolver()
        self.assertEqual(second["roots"][0]["dir"], root["dir"])
        self.assertEqual(len([p for p in self.cache.iterdir() if p.is_dir()]), 1)

    def test_path_escaping_the_checkout_is_an_error(self) -> None:
        self.config(f"packs:\n  - source: {self.url}\n    ref: v1.0.0\n    path: ../../etc\n")
        result = self.run_resolver()
        self.assertEqual(result["roots"], [])
        self.assertTrue(any("escapes the source checkout" in e for e in result["errors"]))

    def test_path_selects_a_subfolder_of_the_checkout(self) -> None:
        self.config(f"packs:\n  - source: {self.url}\n    ref: v1.0.0\n    path: rails\n")
        result = self.run_resolver()
        self.assertEqual(result["errors"], [])
        self.assertEqual([r["id"] for r in result["roots"]], ["rails"])

    @unittest.skipIf(os.name == "nt", "symlinks need privileges on Windows")
    def test_symlink_planted_at_the_cache_key_is_replaced(self) -> None:
        self.cache.mkdir()
        key = hashlib.sha256(f"{self.url}\nv1.0.0".encode()).hexdigest()
        decoy = self.tmp / "decoy"
        decoy.mkdir()
        (decoy / "rule.md").write_text(RULE.format(title="Planted"), encoding="utf-8")
        os.symlink(decoy, self.cache / key)
        self.config(f"packs:\n  - source: {self.url}\n    ref: v1.0.0\n")
        result = self.run_resolver()
        self.assertTrue(any("is a symlink or not owned by this user; refetching" in w for w in result["warnings"]))
        self.assertEqual([r["id"] for r in result["roots"]], ["rails"])
        self.assertFalse((self.cache / key).is_symlink())
        self.assertTrue((decoy / "rule.md").exists())

    def test_leading_dash_ref_is_rejected(self) -> None:
        self.config(f"packs:\n  - source: {self.url}\n    ref: --upload-pack=echo\n")
        result = self.run_resolver()
        self.assertEqual(result["roots"], [])
        self.assertTrue(any("may not begin with `-`" in e for e in result["errors"]))

    def test_unreachable_git_source_degrades_to_a_warning(self) -> None:
        missing = (self.tmp / "nowhere").resolve().as_uri()
        self.config(f"packs:\n  - source: {missing}\n    ref: v1\n")
        result = self.run_resolver()
        self.assertEqual(result["roots"], [])
        self.assertEqual(result["errors"], [])
        self.assertTrue(any("source skipped" in w for w in result["warnings"]))

    @unittest.skipIf(os.name == "nt", "symlinks need privileges on Windows")
    def test_two_hop_symlink_escape_refuses_the_pack_in_a_git_source(self) -> None:
        repo = self.make_pack_repo("two-hop", {"voice": ["Plain verbs"], "other": ["Other rule"]})
        shared = repo / "other" / "deep" / "shared"
        shared.mkdir(parents=True)
        os.symlink(Path(os.devnull), shared / "leak.md")
        (repo / "voice" / "examples").mkdir()
        os.symlink(Path("..") / ".." / "other" / "deep" / "shared", repo / "voice" / "examples" / "shared")
        self.recommit(repo, "two hop")
        self.config(f"packs:\n  - source: {self.file_url(repo)}\n    ref: v1\n    pack: voice\n")
        result = self.run_resolver()
        self.assertEqual(result["roots"], [])
        self.assertTrue(any("pack `voice` not published" in e and "leak.md" in e for e in result["errors"]))

class HardeningTests(ResolverHarness):
    """Regressions from the pack-resolution test matrix on PR #3."""

    @unittest.skipIf(os.name == "nt", "symlinks need privileges on Windows")
    def test_two_hop_symlink_escape_refuses_the_pack_in_a_path_source(self) -> None:
        pack = self.pack("compound-packs/house-style", "Earn the ending")
        shared = self.home / "shared"
        shared.mkdir()
        os.symlink(Path(os.devnull), shared / "leak.md")
        (pack / "examples").mkdir()
        os.symlink(shared, pack / "examples" / "shared")
        self.config("packs:\n  - source: compound-packs/house-style\n")
        result = self.run_resolver()
        self.assertEqual(result["roots"], [])
        self.assertTrue(any("pack `house-style` not published" in e and "examples/shared/leak.md" in e for e in result["errors"]))

    @unittest.skipIf(os.name == "nt", "symlinks need privileges on Windows")
    def test_directory_link_cycle_inside_a_pack_terminates(self) -> None:
        pack = self.pack("compound-packs/house-style", "Earn the ending")
        os.symlink(pack, pack / "self")
        self.config("packs:\n  - source: compound-packs/house-style\n")
        result = self.run_resolver()
        self.assertEqual([r["id"] for r in result["roots"]], ["house-style"])

    @unittest.skipUnless(hasattr(os, "mkfifo"), "FIFOs are POSIX-only")
    def test_fifo_named_md_is_never_opened(self) -> None:
        pack = self.pack("compound-packs/house-style", "Earn the ending")
        os.mkfifo(pack / "0pipe.md")
        (pack / "dir.md").mkdir()
        self.config("packs:\n  - source: compound-packs/house-style\n")
        result = self.run_resolver()
        self.assertEqual([r["id"] for r in result["roots"]], ["house-style"])
        self.assertEqual(result["warnings"], [])

    @unittest.skipIf(IS_ROOT or os.name == "nt", "permission bits do not stop root or Windows")
    def test_unreadable_config_layer_is_its_own_error(self) -> None:
        self.pack("personal/house-style", "Earn the ending")
        locked = self.config("packs:\n  - source: x\n")
        locked.chmod(0)
        self.addCleanup(locked.chmod, 0o644)
        self.config("packs:\n  - source: personal/house-style\n", name="config.local.yaml")
        result = self.run_resolver()
        self.assertEqual([r["id"] for r in result["roots"]], ["house-style"])
        self.assertEqual(result["home"], str(self.home.resolve()))
        self.assertEqual(len(result["errors"]), 1)
        self.assertIn("config.yaml: cannot read config file", result["errors"][0])

    def test_id_override_is_validated(self) -> None:
        self.pack("packs/voice", "Plain verbs")
        bad = ["", "'   '", "../../etc", "a/b/c", "-rf", "'.'"]
        entries = "".join(f"  - source: packs\n    pack: voice\n    id: {value}\n" for value in bad)
        self.config("packs:\n" + entries)
        result = self.run_resolver()
        self.assertEqual(result["roots"], [])
        self.assertEqual(len(result["errors"]), len(bad))
        self.assertTrue(all("`id:` must be a non-empty name" in e for e in result["errors"]))

    def test_id_with_a_space_is_still_accepted(self) -> None:
        self.pack("packs/voice", "Plain verbs")
        self.config("packs:\n  - source: packs\n    pack: voice\n    id: 'house rules'\n")
        result = self.run_resolver()
        self.assertEqual([r["id"] for r in result["roots"]], ["house rules"])

    @unittest.skipIf(os.name == "nt", "needs a POSIX shell to delete the working directory")
    def test_deleted_working_directory_warns_instead_of_erroring(self) -> None:
        gone = self.tmp / "gone"
        gone.mkdir()
        proc = subprocess.run(
            ["bash", "-c", f'cd "$1" && rmdir "$1" && exec "$2" "$3"', "_", str(gone), sys.executable, str(RESOLVER)],
            env=self.resolver_env(),
            capture_output=True,
            text=True,
            timeout=60,
        )
        result = self.parse_output(proc)
        self.assertEqual(result["errors"], [])
        self.assertIsNone(result["home"])
        self.assertEqual(len(result["warnings"]), 1)
        self.assertIn("no writing home", result["warnings"][0])

    def test_readme_folder_with_rules_one_level_down_publishes_the_subfolder_and_says_so(self) -> None:
        self.pack("compound-packs/house-style/rules", "Plain verbs", readme=False)
        (self.home / "compound-packs" / "house-style" / "README.md").write_text("House style.\n", encoding="utf-8")
        self.config("packs:\n  - source: compound-packs/house-style\n")
        result = self.run_resolver()
        self.assertEqual([r["id"] for r in result["roots"]], ["rules"])
        self.assertEqual(len(result["warnings"]), 1)
        self.assertIn("has no top-level rules; its subfolder `rules/` was published as pack `rules`", result["warnings"][0])
        self.assertIn("references/packs.md", result["warnings"][0])

    def test_multi_pack_source_without_a_readme_publishes_children_silently(self) -> None:
        self.pack("packs/voice", "Plain verbs")
        self.config("packs:\n  - source: packs\n")
        result = self.run_resolver()
        self.assertEqual([r["id"] for r in result["roots"]], ["voice"])
        self.assertEqual(result["warnings"], [])

    def test_entry_indented_under_another_key_is_a_loud_error(self) -> None:
        self.pack("compound-packs/house-style", "Earn the ending")
        self.pack("compound-packs/team-evidence", "Name the source")
        self.config(
            "packs:\n  - source: compound-packs/house-style\nfuture_key: value\n  - source: compound-packs/team-evidence\n"
        )
        result = self.run_resolver()
        self.assertEqual([r["id"] for r in result["roots"]], ["house-style"])
        self.assertEqual(len(result["errors"]), 1)
        self.assertIn("config.yaml:4", result["errors"][0])
        self.assertIn("outside the `packs:` block", result["errors"][0])

    def test_checkout_nested_inside_a_home_does_not_hide_the_home(self) -> None:
        self.pack("compound-packs/house-style", "Earn the ending")
        self.config("packs:\n  - source: compound-packs/house-style\n")
        book = self.home / "drafts" / "book"
        (book / "ch").mkdir(parents=True)
        (book / ".git").mkdir()
        result = self.run_resolver(cwd=book / "ch")
        self.assertEqual(result["home"], str(self.home.resolve()))
        self.assertEqual([r["id"] for r in result["roots"]], ["house-style"])

    def test_nested_checkout_with_its_own_config_overrides_the_home(self) -> None:
        self.pack("compound-packs/house-style", "Earn the ending")
        self.config("packs:\n  - source: compound-packs/house-style\n")
        book = self.home / "drafts" / "book"
        (book / ".git").mkdir(parents=True)
        (book / ".compound-writing").mkdir()
        (book / ".compound-writing" / "config.yaml").write_text("packs:\n  - source: rules\n", encoding="utf-8")
        (book / "rules").mkdir()
        (book / "rules" / "r.md").write_text(RULE.format(title="Book rule"), encoding="utf-8")
        result = self.run_resolver(cwd=book)
        self.assertEqual(result["home"], str(book.resolve()))
        self.assertEqual([r["id"] for r in result["roots"]], ["rules"])



if __name__ == "__main__":
    unittest.main()
