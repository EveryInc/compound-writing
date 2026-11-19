---
name: cw-tune
description: Optionally tune an existing VOICE.md against the writer's own published pieces for the model they draft with, a section at a time, using a blind voice judge, an Elo ratchet and an autoresearch loop, then propose the tuned VOICE.md for approval. Use when the writer asks to tune, optimize, test or calibrate their voice guide, asks whether their guides actually make drafts sound like them, or wants their voice tuned for Claude, Codex/GPT or Antigravity/Gemini. Requires guides from cw-onboarding and at least six of the writer's own pieces; not for first-run setup.
---

# Tune

Test whether the writing home's guides make drafts sound like the writer, and improve `VOICE.md` where they don't. The first answer, before any tuning, is whether the guides beat no guides at all. This is an optional step after `cw-onboarding`: onboarding writes `VOICE.md` and `STYLE.md` the normal way, and tuning treats the writer's `VOICE.md` as the baseline to beat.

Read `../../references/context-contract.md` first. The voice/style boundary in it governs every edit this skill proposes.

## What it tunes, and why sections

`VOICE.md` is how the writer's sentences sound: cadence, syntax, word choice, register, punctuation, tics. That shows up in a few paragraphs, so each piece is cut into sections of a few hundred words (at its headings where it has them) and every section is a test case. A dozen pieces give dozens of cases instead of a handful, which is what makes the result trustworthy.

`STYLE.md` is loaded when drafting, as in real use, but never edited. Its subject (argument, structure, openings and endings) only shows up across a whole piece, and it is often a shared publication or column standard rather than one writer's own, so tuning it against one writer's pieces could pull a house standard toward them.

## How it measures

A guide written from reading someone's work can sound right and still barely change a model's drafts. Tuning measures that directly. Each section is drafted from the notes the writer might have had for it (what it says, with its facts and stories, plus what the whole piece is about and where the section sits), the way they would draft with Compound Writing for real. A blind judge sees the real section and two drafts, in both orders, and picks the one whose sentences sound more like the writer. It judges voice only, and ignores what the drafts cover and how they are organised.

The score is an Elo ratchet, the metric behind the write-like-Mike experiments (the `ladder` metric in Every Checks). Each section keeps a ladder of every draft ever written for it. The draft from the writer's original guides is pinned at 1000, the no-guides draft sits on the same ladder, and each new draft plays the section's best draft first and steps down while it loses. Every rating is refit from all the games, so the bar rises whenever something beats it. Unlike a fixed baseline it cannot max out, so there is no "perfect" round and no early stop. An autoresearch loop proposes one change to `VOICE.md` per round and keeps it only if its drafts rate higher than the current best's, both read from the ladders as they stand now.

Pieces are split into tune, test and learn sets before they are cut into sections, so no piece has sections on both sides of the test.

Tuning is model-specific. A voice guide tuned for one model is not automatically the best for another, so tune for the model the writer actually drafts with.

## Before starting

Resolve, asking only what cannot be inferred:

- **The writing home** with `VOICE.md` and `STYLE.md`. If either is missing or still the blank template, route to `cw-onboarding` first. Tuning improves guides; it does not create them.
- **The writer's own pieces:** at least 6 (ideally 15+) finished pieces of 600+ words, one `.md` or `.txt` file each. Use a folder the writer names. `examples/` qualifies only if it holds full positive examples of the writer's own work; never tune toward negative examples, co-written or ghostwritten pieces, or other writers.
- **The drafting model**, named `<cli>:<model>`: `claude:claude-opus-5-5`, `codex:gpt-6.1-sol` or `agy:default`. Check which CLIs are installed and signed in (`claude`, `codex`, `agy`).
- **Judge and optimizer:** default to `claude:claude-opus-5-5`. Without Claude Code, use the strongest model the writer's CLI offers for both.

`prepare` ends with `check`, which makes a tiny call to every CLI the run uses and stops if one is signed out or would bill an API key (`ANTHROPIC_API_KEY` set, or Codex signed in with a key rather than a ChatGPT account). Fix what it names before the long steps; `optimize` runs it again.

Tell the writer what it costs before starting: everything runs on their own subscriptions. Each round drafts the tuning sections (20 by default, `--tune-sections`) and judges each in up to three games, so a round is roughly 150 short calls and a 10-round run is 1,500-2,000. Calls run in parallel batches (`--workers`, default 4); raise it if the writer's plan allows more concurrent requests, or lower `--tune-sections` for a cheaper run. A usage limit stops a step cleanly; re-running resumes from the cache.

## Run

The script is `scripts/tune.py` in this skill's folder. Each run lives in a visible folder inside the writing home, `tuning/<model>/` by default, holding the seed copy of the guides, the pieces, their sections and notes, every round, the cache and the report. Run the long steps (`notes`, `baseline`, `optimize`, `evaluate`) in the background and report as rounds finish.

```bash
python3 scripts/tune.py prepare --home <writing-home> --corpus <pieces> --name "<writer>" --writer claude:claude-opus-5-5
python3 scripts/tune.py notes    --work <writing-home>/tuning/claude-claude-opus-5-5
python3 scripts/tune.py baseline --work <writing-home>/tuning/claude-claude-opus-5-5
python3 scripts/tune.py optimize --work <writing-home>/tuning/claude-claude-opus-5-5
python3 scripts/tune.py evaluate --work <writing-home>/tuning/claude-claude-opus-5-5
python3 scripts/tune.py propose  --work <writing-home>/tuning/claude-claude-opus-5-5
```

Check the work between steps:

- **After `prepare`:** open one file in `sections/`. Sections should be a few hundred words of prose each, cut at natural breaks. Sections that are mostly code or tables are skipped.
- **After `notes`:** open two or three files in `notes/`. They should read like a writer's plan for each section. Some of the writer's own phrases are fine; a writer's real notes have them too.
- **After `baseline`:** tell the writer first whether their original guides beat no guides, as counts ("closer on 21 of 34 sections"). If they don't, say so plainly: that is the most useful finding of the run, and tuning starts from there.
- **During `optimize`:** each round prints its Elo, the current best's Elo and its hypothesis. The original guides are 1000. The best's rating drifts as new games refit the ladders; that is the ratchet working.
- **After `evaluate`:** this is the result to trust, measured on sections of pieces nothing was tuned on, head to head against both the original guides and no guides. Below 10 held-out sections it reports counts only. A clear win is closer on most sections against both. Mostly splits or losses means the changes did not generalise: say so plainly and suggest more pieces or rounds rather than adopting.

## Review and adopt

`propose` writes `tuning/<model>/proposed/` with the tuned `VOICE.md`, `changes.diff` and `REPORT.md`. The report leads with whether the original guides beat no guides, then the held-out counts, then every line of the writer's `VOICE.md` that was removed or reworded, with the optimizer's reasons. Nothing in the writing home changes until the writer approves.

Before asking for approval, read the diff yourself and check that:

- every removed or reworded rule in the report is one the writer would let go. Writers keep some rules on purpose ("Many paragraphs have none"); put those back unless the writer agrees;
- every new rule is about how sentences sound. Move anything about argument, structure, openings or endings out, and offer it to the writer as a possible `STYLE.md` note instead;
- no rule mentions the judge or anything else about the scoring;
- no rule is a phrase bank of the writer's sentences, and nothing invents experiences or facts;
- the file keeps the writer's own structure and headings.

Show the writer the held-out result, the kept changes from `REPORT.md`, and the two or three diffs that matter most. On their approval, run `adopt --work ...`: it backs up the live `VOICE.md` into the run folder and replaces it, and refuses if the live file changed during the run. `STYLE.md` is never touched. Then offer to record the tuning in `VOICE.md`'s Confirmed lessons (date, model, held-out counts) so future sessions know the voice guide was tuned and for which model.

## Boundaries

- Never overwrite `VOICE.md` without explicit approval, never edit `STYLE.md`, and never edit guides in an installed plugin or cache folder.
- The tuned guide is still the writer's guide. Treat the proposal as editorial suggestions they can accept in part; apply a partial adoption by hand rather than with `adopt`.
- Tuning measures closeness to past work. If the writer wants their voice to change, the guide they write by hand outranks what tuning prefers.
- The pieces in `tuning/` are copies for testing. Do not move them into `examples/` or quote them in the guides without the writer's say-so.
