#!/usr/bin/env python3
"""Run a declared pack's deterministic checks over a text.

A pack may carry a ``checks/`` directory of JSON files, each a list of
patterns::

    [{"id": "percent-symbol", "pattern": "(?<![/\\d])\\d+(?:\\.\\d+)?%",
      "replace": "\\g<0> percent", "note": "spell out percent in prose",
      "flags": "i"}]

``pattern`` is a Python regular expression; ``replace`` is optional and, when
present, is a ``re.sub`` replacement template applied to the match to produce
the suggested text; ``note`` is the one-line reason the step may quote;
``flags`` may contain ``i`` (ignore case) and ``m`` (multiline).

The step runs this before judgment and treats every finding as evidence at an
exact span: a house-style violation the pack has decided is mechanical. The
step still decides whether to apply it (quoted speech, code, and UI strings
are the usual reasons not to). Findings are never instructions.

Usage:
    python3 packs-check.py --home <home-or-draft> --text-file <path>
    python3 packs-check.py --home <home-or-draft> --text "..."
    python3 packs-check.py --pack-dir <dir> --text-file <path>   # one pack, no resolver

Prints one JSON object: {"findings": [{"pack", "check", "id", "start", "end",
"before", "after", "note"}], "checks_loaded": N, "warnings": [...]}.
Exit 0 whenever the script ran; a malformed check file is a warning, not a
failure, so one bad pattern cannot block a writing step.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FLAGS = {"i": re.IGNORECASE, "m": re.MULTILINE}


def resolve_roots(home: str) -> tuple[list[dict], list[str]]:
    proc = subprocess.run([sys.executable, os.path.join(HERE, "packs-resolve.py"), "--home", home],
                          capture_output=True, text=True, timeout=120)
    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return [], ["packs-resolve.py produced no JSON; no checks run"]
    return data.get("roots", []), list(data.get("warnings", [])) + list(data.get("errors", []))


def load_checks(pack_id: str, pack_dir: str, warnings: list[str]) -> list[tuple[str, str, dict, re.Pattern]]:
    checks_dir = os.path.join(pack_dir, "checks")
    out = []
    if not os.path.isdir(checks_dir):
        return out
    real_dir = os.path.realpath(pack_dir)
    for name in sorted(os.listdir(checks_dir)):
        if not name.endswith(".json"):
            continue
        path = os.path.join(checks_dir, name)
        if not os.path.realpath(path).startswith(real_dir + os.sep) or not os.path.isfile(path):
            warnings.append(f"{pack_id}/checks/{name}: not a regular file inside the pack; skipped")
            continue
        try:
            with open(path, encoding="utf-8-sig") as fh:
                items = json.load(fh)
        except (OSError, json.JSONDecodeError) as exc:
            warnings.append(f"{pack_id}/checks/{name}: unreadable ({exc}); skipped")
            continue
        if not isinstance(items, list):
            warnings.append(f"{pack_id}/checks/{name}: expected a JSON list; skipped")
            continue
        for item in items:
            if not isinstance(item, dict) or not isinstance(item.get("pattern"), str) or not isinstance(item.get("id"), str):
                warnings.append(f"{pack_id}/checks/{name}: check without string id and pattern; skipped")
                continue
            flags = 0
            for ch in str(item.get("flags", "")):
                flags |= FLAGS.get(ch, 0)
            try:
                rx = re.compile(item["pattern"], flags)
            except re.error as exc:
                warnings.append(f"{pack_id}/checks/{name}#{item['id']}: bad pattern ({exc}); skipped")
                continue
            out.append((pack_id, name, item, rx))
    return out


def run_checks(text: str, checks) -> list[dict]:
    findings = []
    for pack_id, file_name, item, rx in checks:
        for m in rx.finditer(text):
            if m.end() == m.start():
                continue
            after = None
            if isinstance(item.get("replace"), str):
                try:
                    after = m.expand(item["replace"])
                except (re.error, IndexError):
                    after = None
            findings.append({
                "pack": pack_id, "check": file_name, "id": item["id"],
                "start": m.start(), "end": m.end(), "before": m.group(0),
                "after": after, "note": item.get("note", ""),
            })
    findings.sort(key=lambda f: (f["start"], f["end"]))
    return findings


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--home", default=None)
    ap.add_argument("--pack-dir", default=None, help="run one pack directory's checks without resolving a home")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--text-file")
    src.add_argument("--text")
    a = ap.parse_args(argv)
    warnings: list[str] = []
    if a.pack_dir:
        roots = [{"id": os.path.basename(os.path.abspath(a.pack_dir)), "dir": os.path.abspath(a.pack_dir)}]
    else:
        roots, warnings = resolve_roots(a.home or os.getcwd())
    checks = []
    for r in roots:
        checks += load_checks(r["id"], r["dir"], warnings)
    text = a.text if a.text is not None else open(a.text_file, encoding="utf-8").read()
    print(json.dumps({"findings": run_checks(text, checks), "checks_loaded": len(checks), "warnings": warnings}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
