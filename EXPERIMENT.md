# Experiment: voice from gold examples

Started 21 November 2026 by Katie Parrott. A fork of Compound Writing 2.4.1 (commit `90f043c`), on the branch `experiment/gold-examples-voice`. This is an experiment branch, not a release: it renames the plugin `compound-writing-gold` so it can't be mistaken for the published one, and it isn't meant to merge into `main` as is.

## The question

Do drafts sound more like the writer when the model reads the writer's best pieces and works out the sentence- and word-level patterns itself, instead of following a written description of the voice in `VOICE.md`?

## What changed

| | Compound Writing 2.4.1 | This edition |
|---|---|---|
| Where voice comes from | `VOICE.md`, a written "vocal score" describing cadence, diction, moves and tics | The gold pieces in `examples/`, read fresh before each voice-sensitive task |
| `VOICE.md` | The voice description, plus confirmed lessons at the bottom | Lessons only: dated corrections on diction and syntax that the examples did not teach. No description |
| `examples/` | Evidence that clarifies the written rules, "not language to imitate" | The authority for sentence sound. Copy the patterns, not the sentences |
| Onboarding | Interview plus samples, then write a voice profile | Collect three to ten gold pieces, show the writer a sample voice read, record only stated preferences as lessons |
| Generic craft rules ("vary sentence length", "cut hedges") | Fallbacks | Fallbacks that give way when the examples consistently do otherwise |

New files:

- `references/voice-from-examples.md`: the procedure every voice-sensitive skill follows. Find the gold set, choose what to read, measure, read for patterns (each backed by quotes from two or more examples), layer in lessons, apply at the examples' rate, save the read as `voice-read.md` beside the draft.
- `skills/cw-voice-check/scripts/voice_stats.py`: counts surface features across the examples (sentence and paragraph length, punctuation rates, contractions, pronouns, openers, recurring words, machine connectors the writer never uses) and, with `--compare draft.md`, flags anything in a draft outside the examples' range.

Skills changed: `cw-draft`, `cw-line-edit`, `cw-voice-check`, `cw-ai-check` (one line), `cw-onboarding`, `cw-save`, `cw-setup-project`, `cw-scribe`, the `voice-matcher` agent, the context contract, templates, README and architecture notes. Every other skill inherits the change through the context contract. The branch's diff against `main` shows all of it.

## How to try it

Load it for one session only, without installing it:

```bash
git clone -b experiment/gold-examples-voice https://github.com/EveryInc/compound-writing.git compound-writing-gold
claude --plugin-dir ./compound-writing-gold
```

Its skills are named `compound-writing-gold:cw-draft` and so on, so they do not collide with the installed `compound-writing`. Run it from a writing home whose `examples/` folder holds the gold pieces.

## What's been tested so far (22 November 2026)

One writer (Katie), Working Overtime essays drafted from briefs with Claude Opus 5.5, ranked blind against the published essay by Claude Opus 5.5, GPT-6 and Gemini 4 Neon. The judges score resemblance to published prose, not quality.

- **With briefs that carried the writer's phrasing, one draft per setup:** drafts from gold examples came first in 76 of 96 verdicts, ahead of a written voice guide in 86 of 96 and of no guide in 47 of 48. The writer's own blind read of 8 pairs picked gold 6 times.
- **With style-free briefs and three drafts per setup** (a What Would Mike Do review flagged the earlier design), the lead over a long, quote-heavy written guide plus the same examples, and over bare Opus, fell within noise on four practice essays.
- **On five sealed essays,** a gold-reading rebuild of the writer's personal skill beat its previous version narrowly (79% of comparisons, interval 59–96%, against a ±27-point tie band) and tied bare Opus.
- **A short lessons file in `VOICE.md`** hasn't helped yet: gold without lessons led on 3 of 4 essays, within noise.
- **Not tested:** other writers, other formats, and the changed voice-check, line-edit and AI-check skills.

To test it yourself: draft held-out pieces from briefs that keep the facts but none of the writer's wording, write several drafts per setup, include a bare-model setup, clean every draft the same way before judging, and calibrate the judge against the writer's own blind picks.

Things to watch:

- Does it copy sentences or anecdotes from the examples? The procedure forbids it; check anyway.
- Does it overdo signature moves (dashes, one-line paragraphs) even with the rates in front of it?
- Cost: reading 12 essays (about 23,000 words) before every draft adds context and time.
- Format transfer: essay examples may not help with an X thread or a brief.
