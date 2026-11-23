#!/usr/bin/env python3
"""Measure surface features of a writer's gold examples, and optionally compare a draft.

Usage:
  python3 voice_stats.py EXAMPLES_DIR_OR_FILES... [--compare DRAFT] [--json]

Reads .md and .txt files. Files under a `negative/` folder or with `negative` in the
name are skipped. Each figure is reported as a range across the examples, so a draft
can be checked against the writer's own spread rather than one average.
Standard library only.
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
from collections import Counter
from pathlib import Path

STOPWORDS = set(
    """a an the and or but so if then than that this these those there here is are was were be been
    being am do does did done have has had having i me my mine we us our you your he him his she her
    it its they them their what which who whom whose when where why how not no nor of to in on at by
    for with from up down out over under again about into through after before as just also very can
    could would should will shall may might must one all any some more most other such only own same
    too s t don doesn didn isn aren wasn weren won wouldn couldn shouldn ve ll re d m like get got
    because while even still much many each every both few let lets i'm it's that's don't can't i've
    i'd you're they're we're there's what's isn't didn't doesn't wasn't""".split()
)

MACHINE_CONNECTORS = [
    "moreover", "furthermore", "additionally", "in conclusion", "ultimately", "delve",
    "crucial", "pivotal", "leverage", "utilize", "navigate", "landscape", "tapestry",
    "seamless", "robust", "it's worth noting", "in today's", "not just", "not only",
    "here's the thing", "the truth is", "let's be honest", "game-changer",
]

ABBREVIATIONS = r"(?:Mr|Mrs|Ms|Dr|Prof|Sr|Jr|St|vs|etc|e\.g|i\.e|U\.S|a\.m|p\.m)\."


def clean_markdown(text: str) -> str:
    text = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.DOTALL)  # front matter
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)  # code blocks
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)  # images
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)  # links -> text
    text = re.sub(r"https?://\S+", "", text)
    lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if re.match(r"^#{1,6}\s", stripped):  # headings are not prose sentences
            lines.append("")
            continue
        if re.match(r"^(\*\s*){3,}$|^-{3,}$|^_{3,}$", stripped):
            lines.append("")
            continue
        stripped = re.sub(r"^>\s?", "", stripped)
        stripped = re.sub(r"^([-*+]|\d+[.)])\s+", "", stripped)
        lines.append(stripped)
    return "\n".join(lines)


def paragraphs_of(text: str) -> list[str]:
    return [p.strip() for p in re.split(r"\n\s*\n", text) if re.search(r"[A-Za-z]", p)]


def sentences_of(paragraph: str) -> list[str]:
    flat = re.sub(r"\s+", " ", paragraph)
    flat = re.sub(ABBREVIATIONS, lambda m: m.group(0).replace(".", "<DOT>"), flat)
    parts = re.split(r"(?<=[.!?…])[\"”’)\]]*\s+(?=[\"“‘(\[]?[A-Z0-9])", flat)
    return [p.replace("<DOT>", ".").strip() for p in parts if re.search(r"[A-Za-z]", p)]


def words_of(text: str) -> list[str]:
    return re.findall(r"[A-Za-z]+(?:['’][A-Za-z]+)*", text)


def per_k(count: int, words: int) -> float:
    return round(1000 * count / words, 1) if words else 0.0


def measure(raw: str) -> dict:
    prose = clean_markdown(raw)
    paras = paragraphs_of(prose)
    sents = [s for p in paras for s in sentences_of(p)]
    words = words_of(prose)
    n = len(words) or 1
    lengths = [len(words_of(s)) for s in sents] or [0]
    para_sents = [len(sentences_of(p)) for p in paras] or [0]
    lower = [w.lower().replace("’", "'") for w in words]
    openers = [words_of(s)[0].lower() for s in sents if words_of(s)]
    lowered_prose = prose.lower().replace("’", "'")
    dashes = len(re.findall(r"—|–|(?<=\w) - (?=\w)|--", prose))
    return {
        "words": len(words),
        "sentences": len(sents),
        "paragraphs": len(paras),
        "sentence_words_mean": round(statistics.mean(lengths), 1),
        "sentence_words_median": statistics.median(lengths),
        "sentence_words_stdev": round(statistics.pstdev(lengths), 1),
        "share_sentences_6_words_or_fewer": round(sum(l <= 6 for l in lengths) / len(lengths), 2),
        "share_sentences_30_words_or_more": round(sum(l >= 30 for l in lengths) / len(lengths), 2),
        "paragraph_sentences_mean": round(statistics.mean(para_sents), 1),
        "share_one_sentence_paragraphs": round(sum(c == 1 for c in para_sents) / len(para_sents), 2),
        "dashes_per_1k": per_k(dashes, n),
        "parentheses_per_1k": per_k(prose.count("("), n),
        "colons_per_1k": per_k(len(re.findall(r":(?!//)", prose)), n),
        "semicolons_per_1k": per_k(prose.count(";"), n),
        "questions_per_1k": per_k(prose.count("?"), n),
        "exclamations_per_1k": per_k(prose.count("!"), n),
        "italics_per_1k": per_k(len(re.findall(r"(?<![*\w])[*_](?![*_\s])[^*_\n]+?(?<!\s)[*_](?![*\w])", prose)), n),
        "contractions_per_1k": per_k(sum("'" in w for w in lower), n),
        "i_per_1k": per_k(sum(w in {"i", "me", "my", "i'm", "i've", "i'd", "i'll", "mine"} for w in lower), n),
        "you_per_1k": per_k(sum(w in {"you", "your", "you're", "you've", "you'll", "yours"} for w in lower), n),
        "we_per_1k": per_k(sum(w in {"we", "us", "our", "we're", "we've", "ours"} for w in lower), n),
        "share_sentences_starting_and_but_so": round(
            sum(o in {"and", "but", "so"} for o in openers) / (len(openers) or 1), 2
        ),
        "_openers": Counter(openers),
        "_content_words": Counter(w for w in lower if w not in STOPWORDS and len(w) > 2),
        "_connectors": Counter(
            {c: len(re.findall(r"\b" + re.escape(c) + r"\b", lowered_prose)) for c in MACHINE_CONNECTORS}
        ),
    }


def gather(paths: list[str]) -> list[Path]:
    files: list[Path] = []
    for raw in paths:
        p = Path(raw).expanduser()
        candidates = sorted(p.rglob("*")) if p.is_dir() else [p]
        for f in candidates:
            if not f.is_file() or f.suffix.lower() not in {".md", ".txt", ".markdown"}:
                continue
            if f.name.lower() == "readme.md" or "negative" in f.name.lower():
                continue
            if any(part.lower() == "negative" for part in f.parts):
                continue
            files.append(f)
    return files


def numeric(m: dict) -> dict:
    return {k: v for k, v in m.items() if not k.startswith("_") and k not in {"words", "sentences", "paragraphs"}}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("examples", nargs="+", help="Example folders or files")
    parser.add_argument("--compare", help="A draft to check against the examples' ranges")
    parser.add_argument("--json", action="store_true", help="Print machine-readable output")
    args = parser.parse_args()

    files = gather(args.examples)
    if not files:
        raise SystemExit("No gold examples found (.md or .txt, excluding README and negative examples).")

    per_file = {}
    openers: Counter = Counter()
    content: Counter = Counter()
    connectors: Counter = Counter()
    files_with_word: Counter = Counter()
    total_words = 0
    for f in files:
        m = measure(f.read_text(encoding="utf-8", errors="replace"))
        if m["words"] < 50:
            continue
        per_file[f.name] = m
        openers.update(m["_openers"])
        content.update(m["_content_words"])
        connectors.update(m["_connectors"])  # update() keeps zero counts, so absences stay visible
        files_with_word.update(set(m["_content_words"]))
        total_words += m["words"]
    if not per_file:
        raise SystemExit("Examples were found but none had 50 or more words of prose.")

    keys = list(numeric(next(iter(per_file.values()))))
    ranges = {}
    for k in keys:
        vals = [numeric(m)[k] for m in per_file.values()]
        ranges[k] = {"min": min(vals), "median": statistics.median(vals), "max": max(vals)}

    min_files = 2 if len(per_file) > 1 else 1
    recurring = [
        (w, c) for w, c in content.most_common(400) if files_with_word[w] >= min(min_files, len(per_file))
    ][:30]
    result = {
        "examples": {name: m["words"] for name, m in per_file.items()},
        "total_words": total_words,
        "ranges": ranges,
        "top_sentence_openers": openers.most_common(12),
        "recurring_content_words": recurring,
        "machine_connectors_in_examples": {c: n for c, n in connectors.items()},
    }

    if args.compare:
        d = measure(Path(args.compare).expanduser().read_text(encoding="utf-8", errors="replace"))
        flags = []
        for k in keys:
            v, r = numeric(d)[k], ranges[k]
            span = max(r["max"] - r["min"], 0.0001)
            if v > r["max"] + 0.25 * span or v < r["min"] - 0.25 * span:
                flags.append({"feature": k, "draft": v, "examples_min": r["min"], "examples_max": r["max"]})
        result["draft"] = {
            "file": args.compare,
            "words": d["words"],
            "values": numeric(d),
            "outside_example_range": flags,
            "machine_connectors_in_draft": {c: n for c, n in d["_connectors"].items() if n},
        }

    if args.json:
        print(json.dumps(result, indent=2, default=str))
        return 0

    print(f"Gold examples: {len(per_file)} files, {total_words:,} words")
    for name, w in result["examples"].items():
        print(f"  - {name} ({w:,} words)")
    print("\nRange across examples (min / median / max):")
    for k, r in ranges.items():
        print(f"  {k:<38} {r['min']:>6} / {r['median']:>6} / {r['max']:>6}")
    print("\nMost common sentence openers:", ", ".join(f"{w} ({c})" for w, c in result["top_sentence_openers"]))
    print("\nRecurring content words (in 2+ examples):", ", ".join(f"{w} ({c})" for w, c in recurring))
    used = {c: n for c, n in connectors.items() if n}
    unused = [c for c, n in connectors.items() if not n]
    print("\nMachine connectors the examples use:", ", ".join(f"{c} ({n})" for c, n in used.items()) or "none")
    print("Machine connectors the examples never use:", ", ".join(unused))

    if args.compare:
        dr = result["draft"]
        print(f"\nDraft: {dr['file']} ({dr['words']:,} words)")
        if dr["outside_example_range"]:
            print("Outside the examples' range:")
            for f in dr["outside_example_range"]:
                print(f"  - {f['feature']}: draft {f['draft']} vs examples {f['examples_min']}–{f['examples_max']}")
        else:
            print("Every measured feature sits within the examples' range.")
        if dr["machine_connectors_in_draft"]:
            print("Machine connectors in the draft:", ", ".join(f"{c} ({n})" for c, n in dr["machine_connectors_in_draft"].items()))
    print("\nThese figures check a reading of the examples; they are not the voice.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
