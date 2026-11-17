#!/usr/bin/env python3
"""Tune a writing home's VOICE.md and STYLE.md against the writer's real pieces.

The writer's existing guides are the baseline. Each step:

  prepare   copy the guides as the seed, load the writer's pieces, split them learn / tune / test,
            then run `check`
  check     confirm each CLI is installed, signed in and on the writer's subscription, not an API key
  briefs    extract a style-free brief from every piece: the substance, none of the style, and
            re-extract any brief that copies runs of the writer's wording
  baseline  do the writer's guides beat no guides at all? Answered before any tuning
  optimize  autoresearch scored by an Elo ratchet: propose one change to VOICE.md and/or STYLE.md,
            draft the tuning pieces with it, and play each draft against that piece's ladder of
            every draft written for it so far. Keep the change if its drafts rate higher
  evaluate  the tuned guides head to head against the original guides and no guides, on held-out
            pieces nothing was tuned on
  propose   write the tuned guides, a diff and a report (every rule removed or reworded) for review
  adopt     after the writer approves, back up the live guides and replace them

The metric is the Elo ratchet from the write-like-Mike experiment (the `ladder` metric in Every
Checks, ArenaMetric in DSPy). A blind judge compares two drafts against the real piece, in both
orders. Each piece keeps a ladder of every draft ever written for it; the original guides' draft is
pinned at 1000. A new draft plays the piece's best draft first and steps down while it loses, then
every rating on the piece is refit from all its games. The bar rises whenever something beats it,
so the score has no ceiling and there is no "perfect" round to stop on.

Model calls go through headless CLIs on the writer's own subscription. A model is named
"<cli>:<model>": claude:claude-opus-5-5, codex:gpt-6.1-sol, agy:default ("default" uses the CLI's
default model). Every call is cached in the run folder, so re-running a step resumes it.
Python 3.9+, standard library only.
"""

from __future__ import annotations

import argparse
import concurrent.futures as cf
import datetime as dt
import difflib
import hashlib
import json
import math
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

# ---------------------------------------------------------------- prompts

BRIEF_SPEC = """# Brief extraction spec

A brief is everything a competent writer would need to reconstruct the substance of a piece, with
none of its style. It must carry every idea, fact, example and structural beat, and nothing about
how the author phrases or frames them.

Write one JSON object, exactly these keys:

{
  "topic": "One neutral sentence: what the piece is about.",
  "audience": "Who the piece is for, in a few words.",
  "thesis": "The core claim or takeaway, stated flatly in one or two sentences.",
  "outline": ["Ordered beats of the piece, one string per section or major move, each listing the substantive points made in it as terse neutral notes."],
  "facts": ["Every specific fact, number, study, product, tool, company, person or source the piece cites, with enough detail to reuse it accurately."],
  "author_experiences": ["First-person facts the author draws on (jobs, projects, anecdotes, results), stated as plain facts."],
  "artifacts": ["Any prompts, code, tables, templates, charts or images the piece includes, described by what they contain."],
  "format": {"approx_words": 0, "uses_headings": true, "uses_lists": false, "includes_code_or_prompts": false}
}

Rules:
1. Substance, completely. Someone holding only the brief should be able to make every point the
   piece makes, in the same order, with the same evidence.
2. No style. No verbatim run longer than five words, except proper names, titles, numbers and
   technical terms. Paraphrase every sentence you summarise, the opening and closing lines
   included. Do not describe tone, voice, humor or rhythm.
3. No rhetorical devices. Leave out the hook, jokes, asides, metaphors, coined phrases, rhetorical
   questions and the closing flourish. If an anecdote or analogy is part of the argument, keep it
   as a neutral fact.
4. Neutral register: flat, telegraphic notes.
5. No title.
6. Ignore boilerplate (newsletter plugs, calls to action, captions) unless the piece is about it."""

DRAFT_SYSTEM = """You are drafting with Compound Writing. Two guides govern this writer's work.
VOICE.md is the authority for how the sentences sound: syntax, diction and tone. STYLE.md is the
authority for what the piece must do: argument, evidence, structure and standards. Follow both.

<VOICE.md>
{voice}
</VOICE.md>

<STYLE.md>
{style}
</STYLE.md>"""

WRITE_INSTRUCTION = ("Write the complete piece described in the brief below. "
                     "Output only the body in Markdown, with no title and no commentary.\n\n")

JUDGE_CRITERIA = """Decide which draft is closer to the reference piece, meaning it reads more like the
same author wrote it. Both drafts were written from the same content brief, so do not reward a
draft for covering more facts. Compare authorship: voice and tone, how the piece opens and closes,
structure and pacing, paragraph and sentence habits, word choice, formatting, how evidence, sources
and personal experience are introduced, and how much the draft sounds like generic AI prose versus
this particular writer."""

JUDGE_PROMPT = """You are judging writing against a reference.

{criteria}

<reference_piece>
{gold}
</reference_piece>

<draft_A>
{a}
</draft_A>

<draft_B>
{b}
</draft_B>

Reply with only a JSON object. In the notes, refer to the draft as "this draft", never by its
letter, and quote the reference where it helps. Voice notes cover how sentences sound (syntax,
word choice, tone, rhythm, punctuation). Style notes cover what the piece does (openings and
endings, structure, argument, how evidence and personal experience are used, formatting).
{{"A_voice": "how draft A's sentences differ from the reference",
  "A_style": "how draft A's structure, argument and evidence differ from the reference",
  "B_voice": "how draft B's sentences differ from the reference",
  "B_style": "how draft B's structure, argument and evidence differ from the reference",
  "closer": "A" or "B"}}"""

PROGRAM = """You are an autonomous researcher improving a writer's Compound Writing guides. You run one
experiment per turn: form a hypothesis about what would make drafts read more like {name}'s real
writing, edit VOICE.md and/or STYLE.md to test it, and the harness evaluates it. If the score
beats the current best it is kept; otherwise it is reverted.

How the guides are used for real: {name} drafts with {writer} from their own notes, outlines,
conversations or a rough draft, with no brief. The brief in this test is only scaffolding that
supplies the substance of a past piece so drafts can be compared with it. So the guides must stand
alone: they supply everything about how {name} writes, and they never mention a brief, a judge, a
reference piece, drafts A and B, or anything else about this test. A rule that only makes sense
inside the test is a failed experiment.

Keep the boundary between the files. It is how the writer maintains them:
- VOICE.md: how sentences sound. Syntax, diction and tone: cadence, rhythm, register,
  punctuation, paragraph shape, verbal tics, sentence-level moves, phrases to favour or avoid.
- STYLE.md: what the piece must do. Argument, evidence, how sources and personal experience are
  used, structure (openings, sections, endings), formatting conventions, readiness standards.
If a rule changes wording, sentence construction or tone, it goes in VOICE.md. If it changes the
claim, support, organisation or standard of the piece, it goes in STYLE.md. Split mixed rules.
The judge's voice notes usually point at VOICE.md and its style notes at STYLE.md.

These are the writer's own files, and many rules in them are deliberate choices, not guesses. Keep
their existing structure and headings, keep rules that are working, and prefer adding, sharpening
or replacing specific rules over rewriting everything. Remove or reverse a rule the writer wrote
only when the judge's notes clearly show it pulls drafts away from their real writing, and list
every rule you remove or reverse in <removed> with the reason. Back material rules with a short cue
of the observed move rather than long quotations, and never turn the writer's sentences into a
phrase bank to copy.

About the score: it is an Elo rating, the chess kind. Every tuning piece keeps a ladder of every
draft ever written for it. The draft written with the writer's original guides is fixed at 1000; a
new draft plays the best draft on the ladder first, steps down while it loses, and is rated from
those games. The score is the mean rating across tuning pieces. There is no ceiling: once a version
of the guides is kept, its drafts become the bar the next experiment has to beat. Look for general
patterns in the judge's notes rather than patching individual pieces. Change one idea at a time
when you can. Simplifications that keep the score are good. If recent experiments failed, try a
different direction."""

TURN = """## Experiment log
{log}

## Current best guides (Elo {best_score:.0f})
<VOICE.md>
{voice}
</VOICE.md>

<STYLE.md>
{style}
</STYLE.md>

## Judge notes on the current best guides' drafts (lowest-rated first)
{notes}
{last_attempt}
## Real pieces from the learning set, for study
{study}

Propose the next experiment. Reply in exactly this format. Give each file you change in full; write
UNCHANGED inside the tags of a file you leave as it is, and "none" inside <removed> if you removed
or reversed nothing.
<hypothesis>one or two sentences</hypothesis>
<target>voice, style or both</target>
<removed>each rule removed or reversed, one per line, with the reason</removed>
<voice_md>
the complete VOICE.md, or UNCHANGED
</voice_md>
<style_md>
the complete STYLE.md, or UNCHANGED
</style_md>"""

# Words that only make sense inside the test. A candidate that adds them is rejected unscored.
TEST_ONLY = re.compile(r"\b(?:the|a|each|this|every|your) brief\b|\bbriefs\b|\bjudge[sd]?\b|"
                       r"\breference piece\b|\bdraft [AB]\b", re.I)

# ---------------------------------------------------------------- model calls

CALLS = {"live": 0, "cached": 0}
_lock = threading.Lock()


class UsageLimit(RuntimeError):
    pass


class Models:
    """Headless claude / codex / agy calls with a disk cache."""

    def __init__(self, work: Path):
        self.cache = work / "cache"
        self.cache.mkdir(parents=True, exist_ok=True)
        self.sandbox = work / "sandbox"  # empty cwd, so no project files, skills or memory leak in
        self.sandbox.mkdir(parents=True, exist_ok=True)

    def chat(self, spec, user, system="", sample=0):
        key = hashlib.sha256(json.dumps([spec, system, user, sample]).encode()).hexdigest()[:32]
        path = self.cache / f"{key}.json"
        if path.exists():
            with _lock:
                CALLS["cached"] += 1
            return json.loads(path.read_text())["text"]
        backend, _, model = spec.partition(":")
        fn = {"claude": self._claude, "codex": self._codex, "agy": self._agy}.get(backend)
        if not fn:
            sys.exit(f"Unknown model {spec!r}: use claude:<model>, codex:<model> or agy:<model>")
        text = fn(model, system, user)
        path.write_text(json.dumps({"spec": spec, "text": text}))
        with _lock:
            CALLS["live"] += 1
        return text

    def _claude(self, model, system, user, attempts=5):
        model, _, effort = model.partition("@")
        cmd = ["claude", "-p", "--system-prompt", system or "You are a careful writer and editor.",
               "--tools", "", "--setting-sources", "", "--strict-mcp-config", "--output-format", "json"]
        if model and model != "default":
            cmd += ["--model", model]
        if effort:
            cmd += ["--effort", effort]
        last = ""
        for i in range(attempts):
            try:
                r = subprocess.run(cmd, input=user, capture_output=True, text=True, cwd=self.sandbox, timeout=3600)
            except subprocess.TimeoutExpired:
                last = "timed out"
                continue
            try:
                d = json.loads(r.stdout)
            except json.JSONDecodeError:
                d = {"is_error": True, "result": (r.stdout or r.stderr)[-400:]}
            if not d.get("is_error") and d.get("result"):
                return d["result"]
            last = str(d.get("result", ""))[:400]
            if re.search(r"usage limit|limit reached|out of extra usage|session limit|hit your .*limit", last, re.I):
                raise UsageLimit(f"Claude usage limit: {last}")
            time.sleep(min(120, 2 ** i * 10))
        raise RuntimeError(f"claude -p failed: {last}")

    def _codex_home(self):
        # A clean CODEX_HOME: no AGENTS.md, memories or skills, just a link to the login.
        home = self.sandbox / "codex_home"
        with _lock:  # parallel workers share one home; set it up once
            home.mkdir(exist_ok=True)
            auth = home / "auth.json"
            real = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")) / "auth.json"
            if not auth.is_symlink() and real.exists():
                auth.symlink_to(real)
            if not (home / "config.toml").exists():
                (home / "config.toml").write_text("notify = []\n")
        return home

    def _codex(self, model, system, user, attempts=4):
        prompt = ((f"Follow these instructions exactly:\n\n<instructions>\n{system}\n</instructions>\n\n" if system else "")
                  + user + "\n\nDo not run any commands or read any files. Reply with the answer only.")
        cmd = ["codex", "exec", "--skip-git-repo-check", "-s", "read-only", "--ephemeral", "-c", "notify=[]"]
        if model and model != "default":
            cmd += ["-m", model]
        last = ""
        for i in range(attempts):
            with tempfile.NamedTemporaryFile("r", suffix=".txt", dir=self.sandbox) as out:
                r = subprocess.run(cmd + ["-o", out.name, "-"], input=prompt, capture_output=True, text=True,
                                   cwd=self.sandbox, timeout=1800, env={**os.environ, "CODEX_HOME": str(self._codex_home())})
                text = out.read().strip()
            if text:
                return text
            last = (r.stdout + r.stderr)[-400:]
            if re.search(r"usage limit|rate limit", last, re.I):
                raise UsageLimit(f"Codex usage limit: {last}")
            time.sleep(min(120, 2 ** i * 10))
        raise RuntimeError(f"codex exec failed: {last}")

    def _agy(self, model, system, user, attempts=4):
        prompt = ((f"Follow these instructions exactly:\n\n<instructions>\n{system}\n</instructions>\n\n" if system else "")
                  + user + "\n\nDo not use any tools or read any files. Reply with the answer only.")
        cmd = ["agy", "-p", prompt, "--output-format", "json", "--disable-slash-commands"]
        if model and model != "default":
            cmd += ["--model", model]
        last = ""
        for i in range(attempts):
            try:
                r = subprocess.run(cmd, capture_output=True, text=True, cwd=self.sandbox, timeout=3600)
                out = json.loads(r.stdout)
                if out.get("status") == "SUCCESS" and out.get("response", "").strip():
                    return out["response"].strip()
                last = str(out)[:400]
            except subprocess.TimeoutExpired:
                last = "timed out"
            except (json.JSONDecodeError, ValueError):
                last = (r.stdout + r.stderr)[-400:]
            if re.search(r"quota|rate limit|resource exhausted|limit reached", last, re.I) and i == attempts - 1:
                raise UsageLimit(f"Antigravity usage limit: {last}")
            time.sleep(min(120, 2 ** i * 10))
        raise RuntimeError(f"agy failed: {last}")


def pmap(fn, items, workers):
    with cf.ThreadPoolExecutor(max_workers=workers) as ex:
        return list(ex.map(fn, items))


def workers_for(cfg, *specs):
    return cfg["workers"]


# ---------------------------------------------------------------- sign-in and billing check

def preflight(cfg, models):
    """Before a long run: every CLI installed, signed in, and billing the writer's subscription."""
    problems = []
    specs = sorted({cfg[k] for k in ("writer", "judge", "optimizer", "brief_model")})
    for spec in specs:
        backend, _, model = spec.partition(":")
        exe = {"claude": "claude", "codex": "codex", "agy": "agy"}.get(backend)
        if not exe:
            problems.append(f"{spec}: unknown CLI; use claude:<model>, codex:<model> or agy:<model>")
            continue
        if not shutil.which(exe):
            problems.append(f"{spec}: `{exe}` is not installed")
            continue
        if backend == "claude" and os.environ.get("ANTHROPIC_API_KEY"):
            problems.append("ANTHROPIC_API_KEY is set, so `claude -p` would bill that API key instead of the "
                            "writer's subscription. Unset it for this run.")
        if backend == "codex":
            for var in ("CODEX_API_KEY", "OPENAI_API_KEY"):
                if os.environ.get(var):
                    problems.append(f"{var} is set, so `codex exec` may bill that API key. Unset it for this run.")
            auth_file = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")) / "auth.json"
            try:
                auth = json.loads(auth_file.read_text())
            except (OSError, json.JSONDecodeError):
                auth = {}
            if str(auth.get("auth_mode", "")).lower() in ("apikey", "api_key") or (
                    auth.get("OPENAI_API_KEY") and not auth.get("tokens")):
                problems.append("Codex is signed in with an API key, so every call would be billed to it. "
                                "Run `codex login` with the writer's ChatGPT account first.")
        print(f"  checking {spec}...")
        try:
            fn = {"claude": models._claude, "codex": models._codex, "agy": models._agy}[backend]
            fn(model, "", "Reply with the single word OK.", attempts=1)
        except Exception as e:  # noqa: BLE001 - any failure here means the long run would fail too
            problems.append(f"{spec}: a test call failed ({str(e)[:200]}). Sign in to `{exe}` and try again.")
    return problems


def run_check(cfg, models):
    problems = preflight(cfg, models)
    if problems:
        print("Fix these before the long steps, then run `check` again:\n" + "\n".join(f"- {p}" for p in problems))
        sys.exit(3)
    print("All CLIs are installed, signed in and on a subscription.")


# ---------------------------------------------------------------- run folder

def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-") or "run"


def load_cfg(work):
    p = work / "config.json"
    if not p.exists():
        sys.exit(f"{work} has no config.json: run `prepare` first.")
    return json.loads(p.read_text())


def save_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=1))


def guides(folder):
    return {"voice": (folder / "VOICE.md").read_text(), "style": (folder / "STYLE.md").read_text()}


def system_for(g):
    return DRAFT_SYSTEM.format(voice=g["voice"].strip(), style=g["style"].strip())


def pieces(work, split=None):
    out = []
    for row in json.loads((work / "manifest.json").read_text()):
        if split and row["split"] not in split.split("+"):
            continue
        bp = work / "briefs" / f"{row['id']}.json"
        out.append({**row, "gold": (work / "pieces" / f"{row['id']}.md").read_text(),
                    "brief": json.loads(bp.read_text()) if bp.exists() else None})
    return [p for p in out if p["brief"]] if split else out


def render_brief(p):
    b, fmt = p["brief"], p["brief"].get("format", {})

    def bullets(items):
        return "\n".join(f"- {x}" for x in items) if items else "- (none)"

    head = "".join(f"**{k}:** {p[k.lower()]}\n" for k in ("Publication", "Date") if p.get(k.lower()))
    return f"""# Brief

{head}**Target length:** about {fmt.get('approx_words', p['words'])} words
**Format:** {'uses section headings' if fmt.get('uses_headings') else 'no section headings'}; {'uses lists' if fmt.get('uses_lists') else 'mostly prose'}; {'includes code or prompts' if fmt.get('includes_code_or_prompts') else 'no code'}

**Topic:** {b.get('topic', '')}
**Audience:** {b.get('audience', '')}
**Thesis:** {b.get('thesis', '')}

## Outline (in order)
{bullets(b.get('outline', []))}

## Facts, sources and examples to use
{bullets(b.get('facts', []))}

## Author's own experience to draw on
{bullets(b.get('author_experiences', []))}

## Artifacts to include (prompts, code, tables, images)
{bullets(b.get('artifacts', []))}
"""


def draft(models, g, p, writer):
    return models.chat(writer, WRITE_INSTRUCTION + render_brief(p), system=system_for(g) if g else "")


# ---------------------------------------------------------------- brief leak check

def _words(text):
    return re.findall(r"[a-z0-9]+(?:'[a-z]+)?", text.lower())


def _strings(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from _strings(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from _strings(v)


def leaks(brief, gold, n=6):
    """Runs of n+ words the brief shares with the piece, merged into phrases. Rule 2 of the spec
    allows names and titles, so a few hits can be fine; most are the writer's phrasing leaking in."""
    gw = _words(gold)
    grams = {tuple(gw[i:i + n]) for i in range(len(gw) - n + 1)}
    found = []
    for s in _strings(brief):
        w = _words(s)
        i = 0
        while i <= len(w) - n:
            if tuple(w[i:i + n]) in grams:
                j = i + n
                while j < len(w) and tuple(w[j - n + 1:j + 1]) in grams:
                    j += 1
                found.append(" ".join(w[i:j]))
                i = j
            else:
                i += 1
    return found


# ---------------------------------------------------------------- judge

def _parse_judge(text):
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        raise ValueError(f"judge returned no JSON: {text[:200]}")
    try:
        out = {k.strip(): v for k, v in json.loads(m.group(0)).items()}
    except json.JSONDecodeError:
        body = m.group(0)  # notes quote the reference and sometimes break the JSON
        closer = re.search(r'"\s*closer\s*"\s*:\s*"?([AB])', body)
        out = {"closer": closer.group(1) if closer else ""}
        keys = ["A_voice", "A_style", "B_voice", "B_style", "closer"]
        for key, nxt in zip(keys, keys[1:]):
            n = re.search(rf'"\s*{key}\s*"\s*:\s*"(.*?)"\s*,\s*"\s*{nxt}\s*"', body, re.S)
            out[key] = n.group(1) if n else ""
    closer = str(out.get("closer", "")).strip().upper()[:1]
    if closer not in ("A", "B"):
        raise ValueError(f"judge gave no verdict: {text[:200]}")
    return closer, out


def compare(models, judge, gold, a, b):
    prompt = JUDGE_PROMPT.format(criteria=JUDGE_CRITERIA, gold=gold, a=a, b=b)
    for attempt in range(3):
        try:
            return _parse_judge(models.chat(judge, prompt, sample=attempt))
        except ValueError:
            continue
    return random.choice("AB"), {}


def triad(models, judge, gold, x, y):
    """Judge both orderings to cancel position bias. Returns x's score in [0, 1] (0.5 is a split:
    the judge followed the position) and the judge's voice and style notes on each draft."""
    c1, o1 = compare(models, judge, gold, x, y)
    c2, o2 = compare(models, judge, gold, y, x)
    score = ((c1 == "A") + (c2 == "B")) / 2

    def notes(first, second):
        return {k: " ".join(n for n in (o1.get(f"{first}_{k}", ""), o2.get(f"{second}_{k}", "")) if n)
                for k in ("voice", "style")}
    return score, notes("A", "B"), notes("B", "A")


# ---------------------------------------------------------------- the Elo ratchet (the eval metric)

ANCHOR, PRIOR_SD, DEPTH = 1000.0, 800.0, 3
_C = math.log(10) / 400


def _expected(d):
    return 1 / (1 + 10 ** (-d / 400))


def _fit(results, start=ANCHOR):
    """Rating from (opponent rating, score) pairs with a Gaussian prior at 1000; Newton steps."""
    r = start
    for _ in range(30):
        g, h = -(r - ANCHOR) / PRIOR_SD ** 2, -1 / PRIOR_SD ** 2
        for ro, s in results:
            e = _expected(r - ro)
            g += _C * (s - e)
            h -= _C * _C * e * (1 - e)
        step = max(-300.0, min(300.0, g / h))
        r -= step
        if abs(step) < 0.1:
            break
    return r


def text_key(text):
    return hashlib.sha256(text.encode()).hexdigest()[:16]


class Ladders:
    """Per piece, every draft ever written for it, each with an Elo rating and its games.

    Settings from the write-like-Mike experiment (simulated per-piece ladders, Oct 2026): three
    games, top-down, find a piece's true best draft about half the time against 8-19% for other
    orders; every new draft starts from 1000; and ratings are refit from all games and compared as
    they stand now, never as they were stored, so a kept change is judged on today's ladder."""

    def __init__(self, work):
        self.path, self.drafts = work / "ladders.json", work / "drafts"
        self.drafts.mkdir(exist_ok=True)
        self.data = json.loads(self.path.read_text()) if self.path.exists() else {}
        self.lock, self.locks = threading.Lock(), {}

    def save(self):
        with self.lock:
            save_json(self.path, self.data)

    def _piece(self, pid):
        with self.lock:
            self.locks.setdefault(pid, threading.Lock())
            return self.data.setdefault(pid, {"anchor": None, "drafts": {}, "games": []})

    def _text(self, key):
        return (self.drafts / f"{key}.md").read_text()

    def _add(self, lad, text, label, rating):
        key = text_key(text)
        (self.drafts / f"{key}.md").write_text(text)
        lad["drafts"][key] = {"labels": [label], "rating": rating}
        return key

    def pin(self, p, text, label):
        """Fix the original guides' draft for this piece at 1000. Every rating is relative to it."""
        lad = self._piece(p["id"])
        with self.locks[p["id"]]:
            if lad["anchor"] is None:
                lad["anchor"] = self._add(lad, text, label, ANCHOR)

    def rating(self, pid, text):
        d = self.data.get(pid, {}).get("drafts", {}).get(text_key(text))
        return None if d is None else d["rating"]

    def notes(self, pid, text):
        """The judge's notes on this draft from its games, nearest-rated opponent first."""
        lad, key = self.data[pid], text_key(text)
        out = []
        for a, b, s, na, nb in lad["games"]:
            if key in (a, b):
                opp = b if key == a else a
                out.append((abs(lad["drafts"][opp]["rating"] - lad["drafts"][key]["rating"]), na if key == a else nb))
        return [n for _, n in sorted(out, key=lambda x: x[0])]

    def _refit(self, lad):
        for _ in range(6):
            for d in lad["drafts"]:
                if d == lad["anchor"]:
                    continue
                res = [(lad["drafts"][b]["rating"], s) for a, b, s, *_ in lad["games"] if a == d]
                res += [(lad["drafts"][a]["rating"], 1 - s) for a, b, s, *_ in lad["games"] if b == d]
                if res:
                    lad["drafts"][d]["rating"] = _fit(res, start=lad["drafts"][d]["rating"])

    @staticmethod
    def _pick(lad, played, history, est):
        """Top-down: the best draft first; while losing, step down in doubling steps; then the nearest rating."""
        rating = {d: v["rating"] for d, v in lad["drafts"].items()}
        pool = [d for d in rating if d not in played]
        if not pool:
            return None
        ranked = sorted(rating, key=lambda d: -rating[d])
        if not history:
            return next(d for d in ranked if d in pool)
        if all(s < 0.5 for _, s in history):
            last = ranked.index(history[-1][0])
            below = [d for d in ranked[min(len(ranked) - 1, last + 2 ** len(history) - 1):] if d in pool]
            if below:
                return below[0]
        return min(pool, key=lambda d: abs(rating[d] - est))

    def place(self, models, judge, p, text, label, versus=None, depth=DEPTH):
        """Put a draft on the piece's ladder. It plays `depth` games top-down (or exactly the drafts in
        `versus`), every rating on the piece is refit, and the games are returned as
        (opponent key, score, notes on this draft)."""
        lad, key = self._piece(p["id"]), text_key(text)
        with self.locks[p["id"]]:
            if lad["anchor"] is None:
                sys.exit(f"{p['id']} has no anchor: pin the original guides' draft first.")
            if key in lad["drafts"]:
                if label not in lad["drafts"][key]["labels"]:
                    lad["drafts"][key]["labels"].append(label)
                if key == lad["anchor"]:
                    return []
            else:
                self._add(lad, text, label, ANCHOR)
            done = {b: s for a, b, s, *_ in lad["games"] if a == key}
            done.update({a: 1 - s for a, b, s, *_ in lad["games"] if b == key})
            played, history, out = set(done), [(o, s) for o, s in done.items()], []
            targets = [text_key(v) for v in versus] if versus is not None else None
            est = _fit([(lad["drafts"][o]["rating"], s) for o, s in history]) if history else ANCHOR
            while True:
                if targets is not None:
                    opp = next((t for t in targets if t not in played and t != key), None)
                else:
                    opp = None if len(played) >= depth else self._pick(
                        {**lad, "drafts": {d: v for d, v in lad["drafts"].items() if d != key}}, played, history, est)
                if opp is None:
                    break
                played.add(opp)
                s, mine, theirs = triad(models, judge, p["gold"], text, self._text(opp))
                lad["games"].append([key, opp, s, mine, theirs])
                history.append((opp, s))
                out.append((opp, s, mine))
                est = _fit([(lad["drafts"][o]["rating"], x) for o, x in history])
            lad["drafts"][key]["rating"] = est
            self._refit(lad)
            return out

    def head_to_head(self, pid, text, opp_text):
        """x's score against y on this piece from their game: 1 closer, 0 further, 0.5 split."""
        a, b = text_key(text), text_key(opp_text)
        for x, y, s, *_ in self.data[pid]["games"]:
            if (x, y) == (a, b):
                return s
            if (x, y) == (b, a):
                return 1 - s
        return None


def tally(scores):
    n = len(scores)
    w = sum(s == 1.0 for s in scores)
    l = sum(s == 0.0 for s in scores)
    line = f"closer on {w} of {n}, further on {l}, {n - w - l} split"
    if n >= 10:  # with fewer pieces a percentage reads as more certain than it is
        line += f" ({sum(scores) / n:.0%} overall)"
    return {"n": n, "closer": w, "further": l, "split": n - w - l, "line": line}


def mean(xs):
    return sum(xs) / len(xs) if xs else 0.0


def place_guides(models, cfg, lad, g, label, items, versus=None):
    """Draft each piece with these guides (None = no guides) and put the drafts on the ladders."""
    def one(p):
        text = draft(models, g, p, cfg["writer"])
        lad.place(models, cfg["judge"], p, text, label, versus=versus(p) if versus else None)
        return text
    texts = pmap(one, items, workers_for(cfg, cfg["writer"], cfg["judge"]))
    lad.save()
    return dict(zip((p["id"] for p in items), texts))


def pin_seed(models, cfg, lad, seed, items):
    texts = pmap(lambda p: draft(models, seed, p, cfg["writer"]), items, workers_for(cfg, cfg["writer"]))
    for p, t in zip(items, texts):
        lad.pin(p, t, "original guides")
    lad.save()
    return dict(zip((p["id"] for p in items), texts))


def standing(lad, texts):
    """Current ratings of one version's drafts: refits after later games move them, and this reads them now."""
    return {pid: lad.rating(pid, t) for pid, t in texts.items()}


# ---------------------------------------------------------------- steps

def read_corpus(path):
    files = [path] if path.is_file() else sorted(
        f for f in path.rglob("*") if f.suffix.lower() in (".md", ".markdown", ".txt") and f.is_file()
        and f.name.lower() != "readme.md")
    out = []
    for f in files:
        text = f.read_text(errors="ignore")
        meta = {}
        fm = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
        if fm:
            for line in fm.group(1).splitlines():
                k, _, v = line.partition(":")
                if v.strip():
                    meta[k.strip().lower()] = v.strip().strip("'\"")
            text = text[fm.end():]
        text = text.strip()
        out.append({"file": str(f), "text": text, "meta": meta, "words": len(text.split())})
    return out


def cmd_prepare(a):
    home = Path(a.home).expanduser().resolve()
    for f in ("VOICE.md", "STYLE.md"):
        if not (home / f).exists():
            sys.exit(f"{home} has no {f}. Create the guides with cw-onboarding first; they are the baseline.")
    work = Path(a.work).expanduser().resolve() if a.work else home / "tuning" / slugify(a.writer)
    if (work / "config.json").exists() and not a.force:
        sys.exit(f"{work} already holds a run. Continue it with the next step, or pass --force to start over.")
    corpus = read_corpus(Path(a.corpus).expanduser())
    kept = [c for c in corpus if a.min_words <= c["words"] <= a.max_words]
    print(f"Found {len(corpus)} files; {len(kept)} are {a.min_words}-{a.max_words} words.")
    if len(kept) < 8:
        sys.exit("Need at least 8 pieces of the writer's own work (ideally 20+) to tune and test fairly.")
    n = len(kept)
    test = a.test if a.test is not None else min(10, max(3, round(n * 0.3)))
    tune = a.tune if a.tune is not None else min(8, max(3, round(n * 0.25)))
    if n - test - tune < 2:
        sys.exit(f"{n} pieces is too few for {test} test + {tune} tune; pass smaller --test/--tune.")
    random.Random(a.seed).shuffle(kept)
    (work / "pieces").mkdir(parents=True, exist_ok=True)
    (work / "seed").mkdir(exist_ok=True)
    for f in ("VOICE.md", "STYLE.md"):
        shutil.copy(home / f, work / "seed" / f)
    manifest, seen = [], set()
    for i, c in enumerate(kept):
        base = slugify(c["meta"].get("title") or Path(c["file"]).stem)[:60]
        pid = base if base not in seen else f"{base}-{i}"
        seen.add(pid)
        (work / "pieces" / f"{pid}.md").write_text(c["text"])
        manifest.append({"id": pid, "file": c["file"], "words": c["words"],
                         "split": "test" if i < test else "tune" if i < test + tune else "learn",
                         "publication": c["meta"].get("publication") or c["meta"].get("source") or "",
                         "date": c["meta"].get("date", "")})
    save_json(work / "manifest.json", manifest)
    cfg = {"home": str(home), "name": a.name, "writer": a.writer, "judge": a.judge, "optimizer": a.optimizer,
           "brief_model": a.brief_model, "workers": a.workers, "created": dt.date.today().isoformat()}
    save_json(work / "config.json", cfg)
    print(f"Split: {n - test - tune} learn / {tune} tune / {test} test.\nRun folder: {work}")
    if test < 10:
        print(f"Note: {test} held-out pieces is a small test. Results will be reported as counts, not percentages.")
    if not a.skip_check:
        run_check(cfg, Models(work))


def cmd_check(a):
    work = Path(a.work).expanduser()
    run_check(load_cfg(work), Models(work))


def cmd_briefs(a):
    work = Path(a.work).expanduser()
    cfg, models = load_cfg(work), Models(work)
    todo = [p for p in pieces(work) if not p["brief"]]
    print(f"Extracting {len(todo)} briefs with {cfg['brief_model']}...")
    leak_path = work / "briefs" / "leaks.json"

    def one(p):
        base = (f"{BRIEF_SPEC}\n\nApproximate word count: {p['words']}\n\n<piece>\n{p['gold']}\n</piece>\n\n"
                "Return only the JSON object.")
        best, prompt = None, base
        for attempt in range(4):
            m = re.search(r"\{.*\}", models.chat(cfg["brief_model"], prompt, sample=attempt), re.S)
            try:
                brief = json.loads(m.group(0))
            except (AttributeError, json.JSONDecodeError):
                continue
            found = leaks(brief, p["gold"])
            if best is None or len(found) < len(best[1]):
                best = (brief, found)
            if not found:
                break
            # Re-extract with the copied runs named, so the brief carries the substance and not the wording.
            prompt = base + ("\n\nYour last attempt copied these runs of the author's own wording. Restate each "
                             "in neutral words of your own (names and titles may stay):\n"
                             + "\n".join(f"- {x}" for x in found[:20]))
        if best is None:
            print(f"  could not extract a brief for {p['id']}; it will be skipped")
            return p["id"], None
        save_json(work / "briefs" / f"{p['id']}.json", best[0])
        return p["id"], best[1]

    results = pmap(one, todo, workers_for(cfg, cfg["brief_model"]))
    record = json.loads(leak_path.read_text()) if leak_path.exists() else {}
    record.update({pid: found for pid, found in results if found is not None})
    save_json(leak_path, record)
    print(f"Briefs ready: {sum(1 for p in pieces(work) if p['brief'])} of {len(pieces(work))}.")
    leaky = {pid: f for pid, f in record.items() if f}
    if leaky:
        print(f"{len(leaky)} brief(s) still share runs of 6+ words with their piece. Names and titles are fine; "
              f"anything else is the writer's phrasing and makes the test too easy. See {leak_path}:")
        for pid, f in sorted(leaky.items()):
            print(f"  {pid}: " + " | ".join(f[:3]) + (" ..." if len(f) > 3 else ""))


def cmd_baseline(a):
    """Do the writer's guides beat no guides at all? Answered on the tune and test pieces before tuning."""
    work = Path(a.work).expanduser()
    cfg, models = load_cfg(work), Models(work)
    items = pieces(work, "tune+test")
    if not items:
        sys.exit("No pieces with briefs: run `briefs` first.")
    seed, lad = guides(work / "seed"), Ladders(work)
    print(f"Do the guides beat no guides? {len(items)} pieces, writer {cfg['writer']}, judge {cfg['judge']}")
    orig = pin_seed(models, cfg, lad, seed, items)
    none = place_guides(models, cfg, lad, None, "no guides", items, versus=lambda p: [orig[p["id"]]])
    per = {p["id"]: lad.head_to_head(p["id"], orig[p["id"]], none[p["id"]]) for p in items}
    t = tally([s if s is not None else 0.5 for s in per.values()])
    out = {**t, "per_piece": per, "date": dt.date.today().isoformat()}
    save_json(work / "baseline.json", out)
    print(f"  original guides vs no guides: {t['line']}")
    if t["closer"] <= t["further"]:
        print("  The guides do not yet make drafts sound more like the writer than no guides do. Tuning starts\n"
              "  from here, but say so plainly: the first job is guides that beat nothing at all.")
    return out


def cmd_optimize(a):
    work = Path(a.work).expanduser()
    cfg, models = load_cfg(work), Models(work)
    if not a.skip_check:
        run_check(cfg, models)
    if not (work / "baseline.json").exists():
        cmd_baseline(a)
    seed = guides(work / "seed")
    tune, study_pool = pieces(work, "tune"), pieces(work, "learn")
    if not tune:
        sys.exit("No tuning pieces with briefs: run `briefs` first.")
    lad = Ladders(work)
    hist_path = work / "history.json"
    history = json.loads(hist_path.read_text()) if hist_path.exists() else []

    def drafts_of(g):
        return {p["id"]: draft(models, g, p, cfg["writer"]) for p in tune}  # cached after the first time

    def score(texts):
        return mean([r for r in standing(lad, texts).values() if r is not None])

    def notes(texts, limit=8):
        rows = sorted(standing(lad, texts).items(), key=lambda kv: kv[1])
        out = []
        for pid, r in rows[:limit]:
            n = (lad.notes(pid, texts[pid]) or [{}])[0]
            out.append(f"- [{pid}] Elo {r:.0f}\n  Voice: {n.get('voice') or '-'}\n  Style: {n.get('style') or '-'}")
        return "\n".join(out)

    def log():
        return "\n".join(["round\telo\tstatus\ttarget\thypothesis"] + [
            f"{h['round']}\t{h['score']:.0f}\t{h['status']}\t{h['target']}\t{h['hypothesis']}" for h in history])

    def save():
        save_json(hist_path, history)
        (work / "results.tsv").write_text(log() + "\n")
        (work / "best").mkdir(exist_ok=True)
        (work / "best" / "VOICE.md").write_text(history[-1]["best"]["voice"])
        (work / "best" / "STYLE.md").write_text(history[-1]["best"]["style"])

    # The original guides' drafts are pinned at 1000 on every tuning piece's ladder, and the
    # no-guides drafts from `baseline` are already on it, so every rating reads against both.
    pin_seed(models, cfg, lad, seed, tune)
    if not history:
        history.append({"round": 0, "score": ANCHOR, "status": "seed", "target": "-", "removed": "",
                        "hypothesis": "the writer's original guides", "guides": seed, "best": seed})
        save()
    best = history[-1]["best"]
    best_texts = drafts_of(best)
    last_attempt = ""
    stale = 0
    for h in reversed(history[1:]):
        if h["status"] == "keep":
            break
        stale += 1
    rng = random.Random(len(history))
    print(f"Tuning for {cfg['writer']}: starting at round {len(history)}, best Elo {score(best_texts):.0f}")
    for r in range(len(history), a.rounds + 1):
        if a.patience and stale >= a.patience:
            print(f"Stopping: {stale} rounds without improvement (--patience {a.patience}).")
            break
        best_score = score(best_texts)
        study = rng.sample(study_pool, min(2, len(study_pool)))
        prompt = PROGRAM.format(name=cfg["name"], writer=cfg["writer"]) + "\n\n" + TURN.format(
            log=log(), best_score=best_score, voice=best["voice"], style=best["style"],
            notes=notes(best_texts), last_attempt=last_attempt,
            study="\n\n".join(f"<brief>\n{render_brief(p)}\n</brief>\n<real_piece>\n{p['gold']}\n</real_piece>"
                              for p in study))
        reply = models.chat(cfg["optimizer"], prompt, sample=r)
        v = re.search(r"<voice_md>\s*(.*?)\s*</voice_md>", reply, re.S)
        s = re.search(r"<style_md>\s*(.*?)\s*</style_md>", reply, re.S)
        if not (v and s):
            print(f"  round {r}: the optimizer returned no guides; skipping")
            continue
        cand = {"voice": best["voice"] if v.group(1).strip() == "UNCHANGED" else v.group(1) + "\n",
                "style": best["style"] if s.group(1).strip() == "UNCHANGED" else s.group(1) + "\n"}
        if cand == best:
            print(f"  round {r}: no change proposed; skipping")
            continue
        m_hyp = re.search(r"<hypothesis>(.*?)</hypothesis>", reply, re.S)
        hyp = re.sub(r"\s+", " ", m_hyp.group(1)).strip() if m_hyp else ""
        m_rem = re.search(r"<removed>(.*?)</removed>", reply, re.S)
        removed = m_rem.group(1).strip() if m_rem and m_rem.group(1).strip().lower() != "none" else ""
        target = "+".join(k for k in ("voice", "style") if cand[k] != best[k])
        entry = {"round": r, "target": target, "hypothesis": hyp, "removed": removed, "guides": cand}

        added = [m.group(0) for m in TEST_ONLY.finditer(cand["voice"] + cand["style"])]
        if len(added) > len(TEST_ONLY.findall(best["voice"] + best["style"])):
            stale += 1
            last_attempt = (f"\n## Last experiment (rejected unscored)\nHypothesis: {hyp}\nIt wrote rules about the "
                            f"test itself ({', '.join(sorted(set(added)))}). The guides are used without a brief or a "
                            "judge, so such rules do nothing for the writer.\n")
            history.append({**entry, "score": best_score, "status": "rejected", "best": best})
            save()
            print(f"  round {r}: rejected unscored, it wrote rules about the test ({', '.join(sorted(set(added)))})")
            continue

        cand_texts = place_guides(models, cfg, lad, cand, f"round {r}", tune)
        # Ratings move as new games refit the ladders, so compare both versions as they stand now.
        cand_score, best_score = score(cand_texts), score(best_texts)
        kept = cand_score > best_score
        stale = 0 if kept else stale + 1
        if kept:
            best, best_texts, last_attempt = cand, cand_texts, ""
        else:
            last_attempt = (f"\n## Last experiment (reverted, Elo {cand_score:.0f})\nHypothesis: {hyp}\n"
                            f"Judge notes on its drafts:\n{notes(cand_texts, 4)}\n")
        history.append({**entry, "score": cand_score, "best_score": max(cand_score, best_score),
                        "status": "keep" if kept else "discard", "best": best})
        save()
        print(f"  round {r}: Elo {cand_score:.0f} vs best {best_score:.0f} ({'keep' if kept else 'discard'}, "
              f"{target}) | {hyp[:90]}")
    final = score(best_texts)
    save_json(work / "standing.json", {"best_elo": final, "per_piece": standing(lad, best_texts)})
    print(f"Best guides: {work / 'best'} (Elo {final:.0f} on the tuning pieces; the original guides are 1000)")


def cmd_evaluate(a):
    work = Path(a.work).expanduser()
    cfg, models = load_cfg(work), Models(work)
    if not (work / "best" / "VOICE.md").exists():
        sys.exit("Run `optimize` first.")
    tuned, seed = guides(work / "best"), guides(work / "seed")
    test, lad = pieces(work, "test"), Ladders(work)
    print(f"Held-out test: {len(test)} pieces, writer {cfg['writer']}, judge {cfg['judge']}")
    orig = pin_seed(models, cfg, lad, seed, test)
    none = place_guides(models, cfg, lad, None, "no guides", test, versus=lambda p: [orig[p["id"]]])
    mine = place_guides(models, cfg, lad, tuned, "tuned guides", test,
                        versus=lambda p: [orig[p["id"]], none[p["id"]]])
    out = {"writer": cfg["writer"], "judge": cfg["judge"], "n": len(test), "date": dt.date.today().isoformat()}
    for label, opp in (("original guides", orig), ("no guides", none)):
        per = {p["id"]: lad.head_to_head(p["id"], mine[p["id"]], opp[p["id"]]) for p in test}
        t = tally([s if s is not None else 0.5 for s in per.values()])
        out[label] = {**t, "per_piece": per}
        print(f"  tuned vs {label}: {t['line']}")
    out["elo"] = {label: mean([lad.rating(pid, t) for pid, t in texts.items()])
                  for label, texts in (("original guides", orig), ("no guides", none), ("tuned guides", mine))}
    print("  Elo on held-out pieces: " + ", ".join(f"{k} {v:.0f}" for k, v in out["elo"].items()))
    save_json(work / "eval.json", out)


def rule_changes(old, new):
    """Every line of the writer's guide that is gone from the tuned one, as removed or reworded."""
    new_lines = [l.strip() for l in new.splitlines() if l.strip()]
    have = set(new_lines)
    out = []
    for l in (x.strip() for x in old.splitlines()):
        if not l or l in have:
            continue
        m = difflib.get_close_matches(l, new_lines, n=1, cutoff=0.6)
        out.append(("reworded", l, m[0]) if m else ("removed", l, None))
    return out


def cmd_propose(a):
    work = Path(a.work).expanduser()
    cfg = load_cfg(work)
    seed, tuned = guides(work / "seed"), guides(work / "best")
    history = json.loads((work / "history.json").read_text())

    def opt(name):
        p = work / name
        return json.loads(p.read_text()) if p.exists() else None
    base, ev, st = opt("baseline.json"), opt("eval.json"), opt("standing.json")
    prop = work / "proposed"
    prop.mkdir(exist_ok=True)
    (prop / "VOICE.md").write_text(tuned["voice"])
    (prop / "STYLE.md").write_text(tuned["style"])
    diff = "".join(
        "".join(difflib.unified_diff(seed[k].splitlines(True), tuned[k].splitlines(True),
                                     f"original/{f}", f"tuned/{f}"))
        for k, f in (("voice", "VOICE.md"), ("style", "STYLE.md")))
    (prop / "changes.diff").write_text(diff)
    kept = [h for h in history if h["status"] == "keep"]
    lines = [f"# Tuning report: {cfg['name']}", "",
             f"Tuned for **{cfg['writer']}** (judge {cfg['judge']}, optimizer {cfg['optimizer']}).", "",
             "## Do your original guides beat no guides?", ""]
    if base:
        lines.append(f"Drafts with your original guides against drafts with no guides, on {base['n']} pieces: "
                     f"{base['line']}.")
        if base["closer"] <= base["further"]:
            lines.append("Your guides did not yet make drafts sound more like you than no guides at all.")
    else:
        lines.append("Not measured: run `baseline`.")
    lines += ["", "## Held-out result", ""]
    if ev:
        lines += [f"On {ev['n']} pieces nothing was tuned on, the tuned guides' drafts against:",
                  f"- your original guides: {ev['original guides']['line']}",
                  f"- no guides: {ev['no guides']['line']}",
                  "- Elo: " + ", ".join(f"{k} {v:.0f}" for k, v in ev["elo"].items())]
        if ev["n"] < 10:
            lines.append(f"\n{ev['n']} pieces is a small test: read these as counts, not as a rate.")
    else:
        lines.append("Not run yet: run `evaluate`.")
    lines += ["", "## Every rule removed or reworded", ""]
    changes = [(f, c) for k, f in (("voice", "VOICE.md"), ("style", "STYLE.md")) for c in rule_changes(seed[k], tuned[k])]
    if changes:
        lines.append("Check each one. Some may be rules you wrote on purpose.")
        lines.append("")
        for f, (kind, old, new) in changes:
            lines.append(f"- **{kind}** in {f}: \"{old}\"" + (f"\n  now: \"{new}\"" if new else ""))
    else:
        lines.append("None: every line of your guides is still there.")
    reasons = [h for h in kept if h.get("removed")]
    if reasons:
        lines += ["", "The optimizer's reasons:", ""] + [f"- round {h['round']}: {h['removed']}" for h in reasons]
    lines += ["", "## Changes that were kept", "",
              f"{len(history) - 1} rounds, {len(kept)} kept"
              + (f"; best Elo {st['best_elo']:.0f} on the tuning pieces (your original guides are 1000)" if st else ""),
              ""]
    lines += [f"{i}. ({h['target']}, round {h['round']}, Elo {h['score']:.0f}) {h['hypothesis']}"
              for i, h in enumerate(kept, 1)] or ["None: no change beat the original guides."]
    rejected = sum(h["status"] == "rejected" for h in history)
    if rejected:
        lines.append(f"\n{rejected} round(s) were rejected unscored for writing rules about the test itself.")
    lines += ["", "The full proposed files are in this folder; `changes.diff` shows every line that changed.",
              "Nothing in the writing home has changed. Run `adopt` once the writer approves."]
    (prop / "REPORT.md").write_text("\n".join(lines) + "\n")
    print(f"Proposal: {prop}\n" + (prop / "REPORT.md").read_text())


def cmd_adopt(a):
    work = Path(a.work).expanduser()
    cfg = load_cfg(work)
    home, prop = Path(cfg["home"]), work / "proposed"
    if not (prop / "VOICE.md").exists():
        sys.exit("Run `propose` first.")
    seed = guides(work / "seed")
    live = guides(home)
    if live != seed and not a.force:
        sys.exit("The live VOICE.md or STYLE.md changed since this run started. Merge by hand, or pass --force.")
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = work / f"previous-{stamp}"
    backup.mkdir()
    for f in ("VOICE.md", "STYLE.md"):
        shutil.copy(home / f, backup / f)
        shutil.copy(prop / f, home / f)
    print(f"Adopted the tuned guides into {home}. The previous versions are in {backup}.")


def cmd_status(a):
    work = Path(a.work).expanduser()
    cfg = load_cfg(work)
    m = json.loads((work / "manifest.json").read_text())
    nb = len(list((work / "briefs").glob("*.json"))) - (work / "briefs" / "leaks.json").exists() \
        if (work / "briefs").exists() else 0
    h = json.loads((work / "history.json").read_text()) if (work / "history.json").exists() else []
    base = json.loads((work / "baseline.json").read_text()) if (work / "baseline.json").exists() else {}
    ev = json.loads((work / "eval.json").read_text()) if (work / "eval.json").exists() else {}
    print(f"{cfg['name']} for {cfg['writer']}: {len(m)} pieces, {nb} briefs"
          + (f"; guides vs no guides: {base['line']}" if base else "")
          + (f"; {len(h) - 1} round{'s' if len(h) != 2 else ''}, {sum(x['status'] == 'keep' for x in h)} kept" if h else "")
          + (f"; held-out vs original: {ev['original guides']['line']}" if ev else ""))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("prepare", help="copy the guides as the seed, split the writer's pieces, check the CLIs")
    p.add_argument("--home", required=True, help="the writing home holding VOICE.md and STYLE.md")
    p.add_argument("--corpus", required=True, help="folder of the writer's own pieces, one .md/.txt file each")
    p.add_argument("--name", required=True, help="the writer's name")
    p.add_argument("--writer", required=True, help="the model the guides are tuned for, e.g. claude:claude-opus-5-5")
    p.add_argument("--work", help="run folder (default: <home>/tuning/<writer>)")
    p.add_argument("--judge", default="claude:claude-opus-5-5")
    p.add_argument("--optimizer", default="claude:claude-opus-5-5", help="proposes the edits")
    p.add_argument("--brief-model", default="claude:claude-sonnet-5-5")
    p.add_argument("--workers", type=int, default=4)
    p.add_argument("--test", type=int)
    p.add_argument("--tune", type=int)
    p.add_argument("--min-words", type=int, default=300)
    p.add_argument("--max-words", type=int, default=8000)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--force", action="store_true")
    p.add_argument("--skip-check", action="store_true", help="skip the sign-in and billing check")
    p.set_defaults(fn=cmd_prepare)

    for name, fn, hlp in (("check", cmd_check, "check each CLI is installed, signed in and not billing an API key"),
                          ("briefs", cmd_briefs, "extract style-free briefs"),
                          ("baseline", cmd_baseline, "do the original guides beat no guides?"),
                          ("evaluate", cmd_evaluate, "the tuned guides against the original and no guides, held out"),
                          ("propose", cmd_propose, "write the tuned guides, a diff and a report for review"),
                          ("status", cmd_status, "show progress")):
        p = sub.add_parser(name, help=hlp)
        p.add_argument("--work", required=True)
        p.set_defaults(fn=fn)

    p = sub.add_parser("optimize", help="autoresearch VOICE.md and STYLE.md, scored by the Elo ratchet")
    p.add_argument("--work", required=True)
    p.add_argument("--rounds", type=int, default=10)
    p.add_argument("--patience", type=int, default=0,
                   help="stop after this many rounds without improvement (default 0: run every round)")
    p.add_argument("--skip-check", action="store_true", help="skip the sign-in and billing check")
    p.set_defaults(fn=cmd_optimize)

    p = sub.add_parser("adopt", help="replace the live guides with the proposal, keeping a backup")
    p.add_argument("--work", required=True)
    p.add_argument("--force", action="store_true", help="adopt even if the live guides changed during the run")
    p.set_defaults(fn=cmd_adopt)

    a = ap.parse_args()
    sys.stdout.reconfigure(line_buffering=True)  # progress shows up when run in the background
    t = time.time()
    try:
        a.fn(a)
    except UsageLimit as e:
        print(f"\nStopped: {e}\nEverything finished so far is saved. Re-run the same command later to resume.")
        sys.exit(2)
    finally:
        print(f"[{CALLS['live']} model calls, {CALLS['cached']} from cache, {time.time() - t:.0f}s]")


if __name__ == "__main__":
    main()
