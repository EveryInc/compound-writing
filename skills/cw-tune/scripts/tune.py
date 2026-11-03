#!/usr/bin/env python3
"""Tune a writing home's VOICE.md and STYLE.md against the writer's real pieces.

The writer's existing guides are the baseline. Each step:

  prepare   copy the guides as the seed, load the writer's pieces, split them learn / tune / test
  briefs    extract a style-free brief from every piece: the substance, none of the style
  optimize  autoresearch: propose one change to VOICE.md and/or STYLE.md, draft the tuning
            pieces from their briefs with the candidate guides, and keep the change only if a
            blind judge more often finds the drafts closer to the writer's real pieces
  evaluate  the tuned guides against the original guides on held-out pieces
  propose   write the tuned guides, a diff and a report into the run folder for review
  adopt     after the writer approves, back up the live guides and replace them

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
   technical terms. Do not describe tone, voice, humor or rhythm.
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

How the guides are used: both files are given to {writer} as its instructions, with a brief that
carries the substance of a piece (topic, thesis, outline, facts, the author's experiences) and none
of the style. The guides must supply everything about how {name} writes.

Keep the boundary between the files. It is how the writer maintains them:
- VOICE.md: how sentences sound. Syntax, diction and tone: cadence, rhythm, register,
  punctuation, paragraph shape, verbal tics, sentence-level moves, phrases to favour or avoid.
- STYLE.md: what the piece must do. Argument, evidence, how sources and personal experience are
  used, structure (openings, sections, endings), formatting conventions, readiness standards.
If a rule changes wording, sentence construction or tone, it goes in VOICE.md. If it changes the
claim, support, organisation or standard of the piece, it goes in STYLE.md. Split mixed rules.
The judge's voice notes usually point at VOICE.md and its style notes at STYLE.md.

These are the writer's own files. Keep their existing structure and headings, keep rules that are
working, and prefer adding, sharpening or replacing specific rules over rewriting everything. Back
material rules with a short cue of the observed move rather than long quotations, and never turn
the writer's sentences into a phrase bank to copy.

About the score: each tuning brief is drafted with your guides, and a blind judge compares the
draft with the real piece and with a fixed comparison draft written with the writer's original
guides. The score is the fraction of briefs where your draft is judged closer to the real piece
(0.5 on a split decision; the original guides score 0.5). Look for general patterns in the judge's
notes rather than patching individual pieces. Change one idea at a time when you can.
Simplifications that keep the score are good. If recent experiments failed, try a different
direction."""

TURN = """## Experiment log
{log}

## Current best guides (score {best_score:.3f})
<VOICE.md>
{voice}
</VOICE.md>

<STYLE.md>
{style}
</STYLE.md>

## Judge notes on the current best guides' drafts (lowest-scoring first)
{notes}
{last_attempt}
## Real pieces from the learning set, for study
{study}

Propose the next experiment. Reply in exactly this format. Give each file you change in full; write
UNCHANGED inside the tags of a file you leave as it is.
<hypothesis>one or two sentences</hypothesis>
<target>voice, style or both</target>
<voice_md>
the complete VOICE.md, or UNCHANGED
</voice_md>
<style_md>
the complete STYLE.md, or UNCHANGED
</style_md>"""

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
        home.mkdir(exist_ok=True)
        auth = home / "auth.json"
        real = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")) / "auth.json"
        if not auth.exists() and real.exists():
            auth.symlink_to(real)
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
    # Antigravity runs one request at a time.
    return 1 if any(s.startswith("agy:") for s in specs) else cfg["workers"]


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
        if split and row["split"] != split:
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


# ---------------------------------------------------------------- judge (the eval metric)

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


def triad(models, judge, gold, candidate, opponent):
    """Judge both orderings to cancel position bias. Returns a score in [0, 1] and the
    judge's voice and style notes on the candidate."""
    c1, o1 = compare(models, judge, gold, candidate, opponent)
    c2, o2 = compare(models, judge, gold, opponent, candidate)
    score = ((c1 == "A") + (c2 == "B")) / 2
    voice = " ".join(x for x in (o1.get("A_voice", ""), o2.get("B_voice", "")) if x)
    style = " ".join(x for x in (o1.get("A_style", ""), o2.get("B_style", "")) if x)
    return score, voice, style


def score_guides(models, cfg, g, opponent, items):
    """Draft each piece with both sets of guides and judge them. Opponent drafts are cached, so
    a fixed opponent costs nothing after the first round."""
    def one(p):
        mine, theirs = draft(models, g, p, cfg["writer"]), draft(models, opponent, p, cfg["writer"])
        s, voice, style = triad(models, cfg["judge"], p["gold"], mine, theirs)
        return {"id": p["id"], "score": s, "voice": voice, "style": style}
    return pmap(one, items, workers_for(cfg, cfg["writer"], cfg["judge"]))


def mean(results):
    return sum(r["score"] for r in results) / len(results) if results else 0.0


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
    save_json(work / "config.json", {
        "home": str(home), "name": a.name, "writer": a.writer, "judge": a.judge, "optimizer": a.optimizer,
        "brief_model": a.brief_model, "workers": a.workers, "created": dt.date.today().isoformat()})
    print(f"Split: {n - test - tune} learn / {tune} tune / {test} test.\nRun folder: {work}")


def cmd_briefs(a):
    work = Path(a.work).expanduser()
    cfg, models = load_cfg(work), Models(work)
    todo = [p for p in pieces(work) if not p["brief"]]
    print(f"Extracting {len(todo)} briefs with {cfg['brief_model']}...")

    def one(p):
        prompt = (f"{BRIEF_SPEC}\n\nApproximate word count: {p['words']}\n\n<piece>\n{p['gold']}\n</piece>\n\n"
                  "Return only the JSON object.")
        for attempt in range(3):
            m = re.search(r"\{.*\}", models.chat(cfg["brief_model"], prompt, sample=attempt), re.S)
            try:
                save_json(work / "briefs" / f"{p['id']}.json", json.loads(m.group(0)))
                return
            except (AttributeError, json.JSONDecodeError):
                continue
        print(f"  could not extract a brief for {p['id']}; it will be skipped")

    pmap(one, todo, workers_for(cfg, cfg["brief_model"]))
    print(f"Briefs ready: {sum(1 for p in pieces(work) if p['brief'])} of {len(pieces(work))}.")


def cmd_optimize(a):
    work = Path(a.work).expanduser()
    cfg, models = load_cfg(work), Models(work)
    seed = guides(work / "seed")
    tune, study_pool = pieces(work, "tune"), pieces(work, "learn")
    if not tune:
        sys.exit("No tuning pieces with briefs: run `briefs` first.")
    hist_path = work / "history.json"
    history = json.loads(hist_path.read_text()) if hist_path.exists() else []

    def notes(results, limit=8):
        return "\n".join(f"- [{r['id']}] score {r['score']:.2f}\n  Voice: {r['voice'] or '-'}\n  Style: {r['style'] or '-'}"
                         for r in sorted(results, key=lambda r: r["score"])[:limit])

    def log():
        return "\n".join(["round\tscore\tstatus\ttarget\thypothesis"] + [
            f"{h['round']}\t{h['score']:.3f}\t{h['status']}\t{h['target']}\t{h['hypothesis']}" for h in history])

    def save():
        save_json(hist_path, history)
        (work / "results.tsv").write_text(log() + "\n")
        (work / "best").mkdir(exist_ok=True)
        (work / "best" / "VOICE.md").write_text(history[-1]["best"]["voice"])
        (work / "best" / "STYLE.md").write_text(history[-1]["best"]["style"])

    # The writer's own guides are the seed and the fixed opponent, so every score reads as "how
    # often these guides beat the ones you started with".
    if not history:
        print(f"Drafting the tuning pieces with the original guides ({cfg['writer']})...")
        history.append({"round": 0, "score": 0.5, "best_score": 0.5, "status": "seed", "target": "-",
                        "hypothesis": "the writer's original guides", "guides": seed, "best": seed})
        save()
    best, best_score = history[-1]["best"], history[-1]["best_score"]
    # Notes on the seed come from judging it against drafts with no guides at all.
    best_results = score_guides(models, cfg, best, seed if best != seed else None, tune)
    last_attempt = ""
    stale = 0
    for h in reversed(history[1:]):
        if h["status"] == "keep":
            break
        stale += 1
    rng = random.Random(len(history))
    print(f"Tuning for {cfg['writer']}: starting at round {len(history)}, best {best_score:.3f}")
    for r in range(len(history), a.rounds + 1):
        if best_score >= 1.0 or stale >= a.patience:
            print(f"Stopping: {'perfect score' if best_score >= 1.0 else f'{stale} rounds without improvement'}.")
            break
        study = rng.sample(study_pool, min(2, len(study_pool)))
        prompt = PROGRAM.format(name=cfg["name"], writer=cfg["writer"]) + "\n\n" + TURN.format(
            log=log(), best_score=best_score, voice=best["voice"], style=best["style"],
            notes=notes(best_results), last_attempt=last_attempt,
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
        target = "+".join(k for k in ("voice", "style") if cand[k] != best[k])
        results = score_guides(models, cfg, cand, seed, tune)
        score = mean(results)
        kept = score > best_score
        stale = 0 if kept else stale + 1
        if kept:
            best, best_score, best_results, last_attempt = cand, score, results, ""
        else:
            last_attempt = (f"\n## Last experiment (reverted, score {score:.3f})\nHypothesis: {hyp}\n"
                            f"Judge notes on its drafts:\n{notes(results, 4)}\n")
        history.append({"round": r, "score": score, "best_score": best_score, "status": "keep" if kept else "discard",
                        "target": target, "hypothesis": hyp, "guides": cand, "best": best})
        save()
        print(f"  round {r}: {score:.3f} ({'keep' if kept else 'discard'}, {target}), best {best_score:.3f} | {hyp[:90]}")
    print(f"Best guides: {work / 'best'} (tuning score {best_score:.3f}; the original guides score 0.500)")


def cmd_evaluate(a):
    work = Path(a.work).expanduser()
    cfg, models = load_cfg(work), Models(work)
    if not (work / "best" / "VOICE.md").exists():
        sys.exit("Run `optimize` first.")
    tuned, seed = guides(work / "best"), guides(work / "seed")
    test = pieces(work, "test")
    print(f"Held-out test: {len(test)} pieces, writer {cfg['writer']}, judge {cfg['judge']}")
    out = {"writer": cfg["writer"], "judge": cfg["judge"], "n": len(test), "date": dt.date.today().isoformat()}
    for label, opp in [("original guides", seed)] + ([("no guides", None)] if a.vs_none else []):
        res = score_guides(models, cfg, tuned, opp, test)
        wins, losses = sum(r["score"] == 1.0 for r in res), sum(r["score"] == 0.0 for r in res)
        out[label] = {"score": mean(res), "wins": wins, "losses": losses, "splits": len(res) - wins - losses,
                      "per_piece": res}
        print(f"  tuned vs {label}: {mean(res):.0%} (won {wins}, lost {losses}, split {len(res) - wins - losses})")
    save_json(work / "eval.json", out)


def cmd_propose(a):
    work = Path(a.work).expanduser()
    cfg = load_cfg(work)
    seed, tuned = guides(work / "seed"), guides(work / "best")
    history = json.loads((work / "history.json").read_text())
    ev = json.loads((work / "eval.json").read_text()) if (work / "eval.json").exists() else None
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
             f"- Tuned for: **{cfg['writer']}** (judge {cfg['judge']}, optimizer {cfg['optimizer']})",
             f"- Rounds: {len(history) - 1}, kept {len(kept)}; tuning score {history[-1]['best_score']:.2f} "
             "against the original guides (0.50 = no better)"]
    if ev:
        o = ev["original guides"]
        lines.append(f"- Held-out test, {ev['n']} pieces nothing was tuned on: the tuned guides' drafts were closer to "
                     f"the real piece {o['score']:.0%} of the time (won {o['wins']}, lost {o['losses']}, split {o['splits']})")
        if "no guides" in ev:
            lines.append(f"- Against drafts with no guides at all: {ev['no guides']['score']:.0%}")
    else:
        lines.append("- Held-out test: not run yet")
    lines += ["", "## Changes that were kept", ""]
    lines += [f"{i}. ({h['target']}, round {h['round']}, {h['score']:.2f}) {h['hypothesis']}"
              for i, h in enumerate(kept, 1)] or ["None: no change beat the original guides."]
    lines += ["", "The full proposed files are in this folder; `changes.diff` shows every line that changed.",
              "Nothing in the writing home has changed. Run `adopt` once the writer approves."]
    (prop / "REPORT.md").write_text("\n".join(lines) + "\n")
    print(f"Proposal: {prop}\n" + "\n".join(lines[2:6]))


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
    nb = len(list((work / "briefs").glob("*.json"))) if (work / "briefs").exists() else 0
    h = json.loads((work / "history.json").read_text()) if (work / "history.json").exists() else []
    ev = json.loads((work / "eval.json").read_text()) if (work / "eval.json").exists() else {}
    print(f"{cfg['name']} for {cfg['writer']}: {len(m)} pieces, {nb} briefs, "
          + (f"{len(h) - 1} round{'s' if len(h) != 2 else ''}, tuning best {h[-1]['best_score']:.3f}" if h else "not tuned yet")
          + (f", held-out vs original {ev['original guides']['score']:.0%}" if ev else ""))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("prepare", help="copy the guides as the seed and split the writer's pieces")
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
    p.set_defaults(fn=cmd_prepare)

    for name, fn, hlp in (("briefs", cmd_briefs, "extract style-free briefs"),
                          ("propose", cmd_propose, "write the tuned guides, a diff and a report for review"),
                          ("status", cmd_status, "show progress")):
        p = sub.add_parser(name, help=hlp)
        p.add_argument("--work", required=True)
        p.set_defaults(fn=fn)

    p = sub.add_parser("optimize", help="autoresearch VOICE.md and STYLE.md")
    p.add_argument("--work", required=True)
    p.add_argument("--rounds", type=int, default=10)
    p.add_argument("--patience", type=int, default=4, help="stop after this many rounds without improvement")
    p.set_defaults(fn=cmd_optimize)

    p = sub.add_parser("evaluate", help="score the tuned guides on held-out pieces")
    p.add_argument("--work", required=True)
    p.add_argument("--vs-none", action="store_true", help="also compare against drafts with no guides")
    p.set_defaults(fn=cmd_evaluate)

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
