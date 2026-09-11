# What the pack layer can and cannot do for a line edit, measured against kate bench

Source run: `ce-optimize` `kate-bench-cw-line-edit-v2` in `EveryInc/compound-packs` (round 2; stacked PR on the kate-bench pack branch), September 11, 2026. The writer step was this plugin's `cw-line-edit` on branch `cursor/compound-packs-7c77` at `2490123`, reading the `kate-bench-writing` pack through `packs-resolve.py`, run one subagent per batch of ten paragraphs; the scorer was kate bench's own KatePatch target logic on experimenter-safe rows. Numbers are development-set results on training and internal-validation rows, one model family, one writer run per candidate. The measured integration arms live on `cursor/kate-bench-pack-integration-arms-cf0e` (`9aed8b6` I3, `90a7c5c` I3 fix, `f82f491`+`e4f274f` I6, `aa8f65a` I2); this branch carries only what the numbers support, which is the learnings.

## Setup in one paragraph

Sixty tuning opportunities (45 paragraphs Kate edited, stratified to her opportunity-type mix; 15 she left alone), three never-inspected 40-row check slices, and a 34-opportunity document-disjoint holdout. Primary metric `action_recall`: the share of Kate's recorded edits the step reproduces at the site. Selection: paired per-opportunity flips against the incumbent on the same rows, net ≥ +2 on dev and ≥ 0 on the check slice, gates on KEEP abstention, volume (18–36 edits per 1,000 words), matched-hunk share, and serious errors. The comparison arm was the plugin unchanged (I0) with the pack's three round-1 rules (P1) and whole-document context (H2): **0.400 / 0.417** on dev over two runs, 0.294 / 0.353 on holdout.

## What was tried on the plugin side

| arm | change to the plugin | dev action_recall | paired vs I0 | check slice | kept |
|---|---|---|---|---|---|
| I2 | context contract and `cw-line-edit`: a matching pack rule may narrow the step's default checklist | 0.367 | −2 / −3 | — | no |
| I3 | `packs-check.py`; packs may carry `checks/` the step runs before judgment and cites | 0.383 | −1 / −2 | −2 | no |
| I6 | `packs-retrieve.py`; packs may carry `examples/` before/after pairs the step retrieves per paragraph | 0.400 | 0 / −1 | 0 | no |

Two pack-side arms in the same round (two new rule families; a minimal-diff rule) read 0.417 and 0.400, +1 / 0 and 0 / −1. A diagnostic arm that marked the neighborhood of each of Kate's sites without the fix read **0.533** (+8, p = 0.021).

## Learnings

1. **Rule text changes what the step does at a site, not which sites it finds.** Every arm that told the step how to edit — a rule, pack authority over the checklist, retrieved examples — was cited on 10 to 44 of 60 rows and raised precision (KEEP abstention 0.47 → 0.73, edits at no Kate site 77 → 51, matched-hunk share 0.28 → 0.36 on dev and 0.45 → 0.69 on a check slice) while recall stayed within ±1 of 60. The step already names these faults when it sees them. A house that wants a general-purpose step to edit *less* gets that from a pack today; a house that wants it to find *more* of its editor's edits does not.

2. **Input beat instruction.** The one change in the round that raised recall gave the step the whole document instead of a three-paragraph window (+5 of 60 on dev, +2–3 of 34 on the holdout; product casing from the rest of the draft, names, tense, referents). In whole-draft use the step has this already; a harness or a paragraph-at-a-time integration that withholds it costs recall that no rule recovers.

3. **Deterministic checks in a pack have a headroom question before a design question.** With the pattern bug fixed (below), nineteen house-style checks fired on 3 of 60 paragraphs Kate edited — one the step had already fixed, two on paragraphs she left alone. Her mechanical edits here are a comma or a dash in a particular place, not a regex shape. If packs ever carry checks, the consuming step should report how many fired before anyone reads a recall number.

4. **A check's `replace` is its test.** The pack's `spaced-em-dash` pattern made both spaces optional and reported every closed em dash — correct Every copy — as a violation on 15 of 17 flagged paragraphs; the step treated the findings as noise and mechanical recall slipped. The arm found it; inspection had not. Any check runner should drop a finding whose replacement equals the match (`90a7c5c` does), and pack authors should run their checks over a page of known-good copy before shipping them.

5. **Lexical retrieval of the editor's own before/after pairs is not a finding mechanism at this scale.** Three scoring passes were needed before the retrieval was worth measuring (topic overlap dominated; then long rewrites crowded out one-word moves; scoring only the tokens the editor changed, divided by the size of the change, returned a mix close to the editor's move mix). The step cited the pairs on 10 rows and netted zero on dev and on the check slice. The pairs show the step moves it already makes.

6. **Where the remaining misses are.** Of 36 baseline misses, about 8 were finding (fixed Kate's way once the site was marked), about 16 were a different action at a found site (rewording 0.86 site / 0.14 action; one-or-two-word swaps 0.44 / 0.22; content 0.5 / 0.25), and 12 were sites the step did not touch even when marked, mostly swaps. Exact-action agreement on rewording, swap, and content looks like a ceiling for any editor that is not the house's editor; a rubric or judge lane, not a stricter match, is the instrument there. Finding has about eight opportunities of headroom, and none of the pack-layer mechanisms above reached it.

## What this changes in the plugin

Nothing in code. `references/packs.md` gains a short measured note on what a pack changes in an editing step; `cw-line-edit`'s Lessons record the two step-level lessons (1 and 2). The three arms stay on the arms branch with their tests, for anyone who wants to re-run them against a different editor or a larger examples store. The pack-side record is in `EveryInc/compound-packs`, `packs/kate-bench/research/provenance/2026-09-11-compound-writing-optimize-round-2.md`.
