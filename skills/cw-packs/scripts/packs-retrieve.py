#!/usr/bin/env python3
"""Retrieve a few before/after examples from declared packs for one paragraph.

A pack may carry an ``examples/`` directory of JSONL files, one example per
line::

    {"before": "It's actually a very simple idea.", "after": "It's a simple idea.",
     "type": "insert_delete", "note": "cut the intensifier"}

``examples/`` is storage: the step never reads it whole. This script scores
every example against the paragraph in front of the step and returns the top
``--k``. Scoring is lexical and deterministic: a token the paragraph shares
with an example's ``before`` counts by its rarity across the store, and counts
three times more when the editor *changed* that token in the example (so a
paragraph containing "actually" finds the examples where "actually" was cut).

The step treats a retrieved example as evidence of how the editor handled a
similar sentence, cites it as ``(pack: <id>, examples/<file>)``, and still
decides for itself. Examples are never instructions.

Usage:
    python3 packs-retrieve.py --home <home-or-draft> --text-file <path> [--k 6]
    python3 packs-retrieve.py --home <home-or-draft> --text "..." [--k 6]
    python3 packs-retrieve.py --pack-dir <dir> --text "..."        # one pack, no resolver

Prints one JSON object: {"examples": [{"pack", "file", "before", "after",
"type", "note", "score"}], "examples_loaded": N, "warnings": [...]}.
Exit 0 whenever the script ran; a malformed examples file is a warning.
"""
from __future__ import annotations

import argparse
import difflib
import json
import math
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TOKEN = re.compile(r"[a-z0-9][a-z0-9'’-]*|[—–…;:]")
CHANGED_WEIGHT = 3.0


def resolve_roots(home: str) -> tuple[list[dict], list[str]]:
    proc = subprocess.run([sys.executable, os.path.join(HERE, "packs-resolve.py"), "--home", home],
                          capture_output=True, text=True, timeout=120)
    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return [], ["packs-resolve.py produced no JSON; no examples retrieved"]
    return data.get("roots", []), list(data.get("warnings", [])) + list(data.get("errors", []))


def tokens(text: str) -> list[str]:
    return TOKEN.findall(text.lower())


def changed_tokens(before: str, after: str) -> set[str]:
    a, b = tokens(before), tokens(after)
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    out: set[str] = set()
    for tag, i1, i2, _j1, _j2 in sm.get_opcodes():
        if tag != "equal":
            out.update(a[i1:i2])
    return out


def load_examples(pack_id: str, pack_dir: str, warnings: list[str]) -> list[dict]:
    ex_dir = os.path.join(pack_dir, "examples")
    out: list[dict] = []
    if not os.path.isdir(ex_dir):
        return out
    real_dir = os.path.realpath(pack_dir)
    for name in sorted(os.listdir(ex_dir)):
        if not name.endswith(".jsonl"):
            continue
        path = os.path.join(ex_dir, name)
        if not os.path.realpath(path).startswith(real_dir + os.sep) or not os.path.isfile(path):
            warnings.append(f"{pack_id}/examples/{name}: not a regular file inside the pack; skipped")
            continue
        try:
            with open(path, encoding="utf-8-sig") as fh:
                for n, line in enumerate(fh, 1):
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        item = json.loads(line)
                    except json.JSONDecodeError:
                        warnings.append(f"{pack_id}/examples/{name}:{n}: not JSON; skipped")
                        continue
                    if not isinstance(item, dict) or not isinstance(item.get("before"), str) or not isinstance(item.get("after"), str):
                        warnings.append(f"{pack_id}/examples/{name}:{n}: example without string before/after; skipped")
                        continue
                    toks = tokens(item["before"])
                    out.append({
                        "pack": pack_id, "file": name, "before": item["before"], "after": item["after"],
                        "type": item.get("type", ""), "note": item.get("note", ""),
                        "_tokens": set(toks), "_changed": changed_tokens(item["before"], item["after"]),
                    })
        except OSError as exc:
            warnings.append(f"{pack_id}/examples/{name}: unreadable ({exc}); skipped")
    return out


def rank(text: str, examples: list[dict], k: int) -> list[dict]:
    if not examples:
        return []
    df: dict[str, int] = {}
    for ex in examples:
        for t in ex["_tokens"]:
            df[t] = df.get(t, 0) + 1
    n = len(examples)
    para = set(tokens(text))
    scored = []
    for ex in examples:
        shared = para & ex["_tokens"]
        # A candidate shares a token the editor changed, or at least two tokens.
        if not (shared & ex["_changed"]) and len(shared) < 2:
            continue
        score = 0.0
        for t in shared:
            idf = math.log((n + 1) / (df[t] + 1)) + 0.1
            score += idf * (CHANGED_WEIGHT if t in ex["_changed"] else 1.0)
        # Long examples share tokens by chance; scale by the example's length.
        score /= math.sqrt(len(ex["_tokens"]) or 1)
        scored.append((score, ex))
    scored.sort(key=lambda s: (-s[0], s[1]["before"]))
    picked, seen = [], set()
    for score, ex in scored:
        key = (ex["before"], ex["after"])
        if key in seen:
            continue
        seen.add(key)
        picked.append({k_: ex[k_] for k_ in ("pack", "file", "before", "after", "type", "note")} | {"score": round(score, 3)})
        if len(picked) >= k:
            break
    return picked


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--home", default=None)
    ap.add_argument("--pack-dir", default=None, help="one pack directory, without resolving a home")
    ap.add_argument("--k", type=int, default=6)
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--text-file")
    src.add_argument("--text")
    a = ap.parse_args(argv)
    warnings: list[str] = []
    if a.pack_dir:
        roots = [{"id": os.path.basename(os.path.abspath(a.pack_dir)), "dir": os.path.abspath(a.pack_dir)}]
    else:
        roots, warnings = resolve_roots(a.home or os.getcwd())
    examples: list[dict] = []
    for r in roots:
        examples += load_examples(r["id"], r["dir"], warnings)
    text = a.text if a.text is not None else open(a.text_file, encoding="utf-8").read()
    print(json.dumps({"examples": rank(text, examples, a.k), "examples_loaded": len(examples), "warnings": warnings}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
