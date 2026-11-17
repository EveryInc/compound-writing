---
name: cw-tune
description: Optionally tune an existing VOICE.md and STYLE.md against the writer's own published pieces for the model they draft with, using a blind judge, an Elo ratchet and an autoresearch loop, then propose the tuned guides for approval. Use when the writer asks to tune, optimize, test or calibrate their voice and style guides, asks whether their guides actually make drafts sound like them, or wants guides tuned for Claude, Codex/GPT or Antigravity/Gemini. Requires guides from cw-onboarding and at least eight of the writer's own pieces; not for first-run setup.
---

# Tune

Test whether the writing home's guides make drafts sound like the writer, and improve them where they don't. The first answer, before any tuning, is whether the guides beat no guides at all. This is an optional step after `cw-onboarding`: onboarding writes `VOICE.md` and `STYLE.md` the normal way, and tuning treats those files as the baseline to beat.

Read `../../references/context-contract.md` first. The voice/style boundary in it governs every edit this skill proposes.

## Why tune

A guide written from reading someone's work can sound right and still barely change a model's drafts. Tuning measures that directly. For each held-back piece, the model drafts it from a style-free brief, the way a test needs; in real use the guides work without one. A blind judge sees the real piece and two drafts, in both orders, and picks the one closer to how the writer actually wrote it. The judge's notes come back split into voice notes and style notes, so a fix lands in the right file.

The score is an Elo ratchet, the metric behind the write-like-Mike experiments (the `ladder` metric in Every Checks). Each piece keeps a ladder of every draft ever written for it. The draft from the writer's original guides is pinned at 1000, the no-guides draft sits on the same ladder, and each new draft plays the piece's best draft first and steps down while it loses. Every rating is refit from all the games, so the bar rises whenever something beats it. Unlike a fixed baseline, it cannot max out, so there is no "perfect" round and no early stop. An autoresearch loop proposes one change per round to `VOICE.md`, `STYLE.md` or both, and keeps it only if its drafts rate higher than the current best's, both read from the ladders as they stand now.

Tuning is model-specific. Guides tuned for one model are not automatically the best guides for another, so tune for the model the writer actually drafts with.

## Before starting

Resolve, asking only what cannot be inferred:

- **The writing home** with `VOICE.md` and `STYLE.md`. If either is missing or still the blank template, route to `cw-onboarding` first. Tuning improves guides; it does not create them.
- **The writer's own pieces:** at least 8 (ideally 20-40) finished pieces of 600+ words, one `.md` or `.txt` file each. Use a folder the writer names. `examples/` qualifies only if it holds full positive examples of the writer's own work; never tune toward negative examples, co-written or ghostwritten pieces, or other writers.
- **The drafting model**, named `<cli>:<model>`: `claude:claude-opus-5-5`, `codex:gpt-6.1-sol` or `agy:default`. Check which CLIs are installed and signed in (`claude`, `codex`, `agy`).
- **Judge and optimizer:** default to `claude:claude-opus-5-5`. Without Claude Code, use the strongest model the writer's CLI offers for both.

`prepare` ends with `check`, which makes a tiny call to every CLI the run uses and stops if one is signed out or would bill an API key (`ANTHROPIC_API_KEY` set, or Codex signed in with a key rather than a ChatGPT account). Fix what it names before the long steps; `optimize` runs it again.

Tell the writer what it costs before starting: everything runs on their own subscriptions, roughly a few hundred model calls and 1-3 hours. Calls run in parallel batches (`--workers`, default 4); raise it if the writer's plan allows more concurrent requests. A usage limit stops a step cleanly; re-running resumes from the cache.

## Run

The script is `scripts/tune.py` in this skill's folder. Each run lives in a visible folder inside the writing home, `tuning/<model>/` by default, holding the seed copy of the guides, the pieces and briefs, every round, the cache and the report. Run the long steps (`briefs`, `optimize`, `evaluate`) in the background and report as rounds finish.

```bash
python3 scripts/tune.py prepare --home <writing-home> --corpus <pieces> --name "<writer>" --writer claude:claude-opus-5-5
python3 scripts/tune.py briefs   --work <writing-home>/tuning/claude-claude-opus-5-5
python3 scripts/tune.py baseline --work <writing-home>/tuning/claude-claude-opus-5-5
python3 scripts/tune.py optimize --work <writing-home>/tuning/claude-claude-opus-5-5
python3 scripts/tune.py evaluate --work <writing-home>/tuning/claude-claude-opus-5-5
python3 scripts/tune.py propose  --work <writing-home>/tuning/claude-claude-opus-5-5
```

Check the work between steps:

- **After `briefs`:** the step re-extracts any brief that shares a run of six or more words with its piece, and lists the ones that still do in `briefs/leaks.json`. Names and titles are fine; anything else, especially opening and closing lines, is the writer's phrasing leaking into the drafts and makes the test too easy. Open those briefs and two or three others.
- **After `baseline`:** tell the writer first whether their original guides beat no guides, as counts ("closer on 5 of 7"). If they don't, say so plainly: that is the most useful finding of the run, and tuning starts from there.
- **During `optimize`:** each round prints its Elo, the current best's Elo, which file it changed and its hypothesis. The original guides are 1000. The best's rating drifts as new games refit the ladders; that is the ratchet working. A round that writes rules about the test itself (the brief, the judge, the reference piece) is rejected unscored, since the guides are used without any of them.
- **After `evaluate`:** this is the result to trust, measured on pieces nothing was tuned on, head to head against both the original guides and no guides. With fewer than 10 held-out pieces it reports counts only; never turn 3 of 4 into "75%". A clear win is closer on most pieces against both. Mostly splits or losses means the changes did not generalise: say so plainly and suggest more pieces or rounds rather than adopting.

## Review and adopt

`propose` writes `tuning/<model>/proposed/` with the tuned `VOICE.md` and `STYLE.md`, `changes.diff` and `REPORT.md`. The report leads with whether the original guides beat no guides, then the held-out counts, then every line of the writer's guides that was removed or reworded, with the optimizer's reasons. Nothing in the writing home changes until the writer approves.

Before asking for approval, read the diff yourself and check that:

- every removed or reworded rule in the report is one the writer would let go. Writers keep some rules on purpose ("Many paragraphs have none"); put those back unless the writer agrees;
- no rule mentions the brief, the judge or anything else that exists only in the test;
- every changed rule sits on the right side of the voice/style boundary; move or split any that don't;
- no rule is a phrase bank of the writer's sentences, and nothing invents experiences or facts;
- the files keep the writer's own structure and headings.

Show the writer the held-out result, the kept changes from `REPORT.md`, and the two or three diffs that matter most. On their approval, run `adopt --work ...`: it backs up the live guides into the run folder and replaces them, and refuses if the live files changed during the run. Then offer to record the tuning in `VOICE.md`'s Confirmed lessons (date, model, held-out counts) so future sessions know the guides were tuned and for which model.

## Boundaries

- Never overwrite `VOICE.md` or `STYLE.md` without explicit approval, and never edit guides in an installed plugin or cache folder.
- The tuned guides are still the writer's guides. Treat the proposal as editorial suggestions they can accept in part; apply a partial adoption by hand rather than with `adopt`.
- Tuning measures closeness to past work. If the writer wants their voice to change, the guides they write by hand outrank what tuning prefers.
- The pieces in `tuning/` are copies for testing. Do not move them into `examples/` or quote them in the guides without the writer's say-so.
