---
name: cw-bluf
description: Diagnose whether the most important idea in an article, essay, post, memo, section, paragraph, or sentence appears where it best serves the reader. Use for BLUF checks, buried or misplaced ledes, slow or misleading openings, intro drift, competing main ideas, and requests to get to the point or find the real opening. Compare what the opening foregrounds with what the artifact actually delivers, judge whether any delay is earned, and recommend the smallest structural move. Diagnose by default; rewrite only when asked.
---

# BLUF

## Purpose

Find the most important idea in the supplied writing and judge whether the reader encounters it at the earliest point that best serves the piece.

Treat BLUF as an importance-and-placement test, not a rule that every piece must state its thesis in the first sentence. Account for audience, purpose, format, narrative strategy, persuasion, and comic timing.

Read `../../references/context-contract.md` and load the relevant project, publication, assignment, audience, and format context before judging placement.

Preserve the writer's ownership of the thesis. Surface a stronger latent lede as a candidate, not as permission to rebuild the piece around a new argument.

## Establish The Scope

Identify:

- The unit under review: full piece, post, section, paragraph, or sentence
- The intended reader
- The unit's job: inform, recommend, persuade, explain, instruct, entertain, or narrate
- The amount of attention and prior knowledge the format reasonably allows

Read the full supplied artifact before judging its opening. Do not infer the bottom line from the introduction alone.

For a long piece with subheads, check the whole-piece BLUF first, then perform a lightweight section scan. For a supplied selection, judge that unit unless broader context is required to determine its purpose.

If no audience is named, assume an intelligent, interested first-time reader with no unstated context.

## Extract The Three BLUFs

Distinguish among:

| Layer | Question |
|---|---|
| **Declared BLUF** | What do the headline, opening, or first beat tell the reader is important? |
| **Delivered BLUF** | What idea does the complete artifact actually spend its weight supporting, demonstrating, or concluding? |
| **Latent lede** | Is a more consequential idea hiding later that deserves greater prominence? |

State when the layers align.

Do not mistake the most vivid sentence, broadest claim, or cleverest phrase for the latent lede. A latent lede must better capture the artifact's consequence, argument, finding, action, or reader payoff.

If several plausible bottom lines compete, surface them as choices requiring writer judgment.

## Determine The Placement Mode

Use the artifact's function to determine what "up front" should mean.

| Mode | Placement expectation |
|---|---|
| **Decision, recommendation, memo, news, or report** | State the conclusion, change, finding, or required action immediately. |
| **Essay, analysis, or explainer** | Allow a hook to lead, but surface the thesis, stakes, or governing idea within the opening movement. |
| **Narrative or feature** | Allow a scene or anecdote to lead when it carries the central tension. Surface the larger meaning before curiosity becomes confusion. |
| **Short post** | Use either an immediate point or an earned setup and payoff. Judge whether the landing repays the delay. |
| **Persuasion for a resistant audience** | Permit strategic delay when immediate disclosure would close the reader before the case can be made. |
| **Process or instructions** | State the purpose or outcome early, then organize the body in usable sequence. |
| **Section or paragraph** | Place the contribution near the opening unless a deliberate reveal improves comprehension or force. |
| **Sentence** | Put the conceptual and grammatical payload before secondary context unless delayed syntax creates a purposeful landing. |

Do not apply a universal paragraph or word-count threshold. Judge delay relative to the artifact's length, reader, and function.

## Run The Placement Tests

### Stop-Reading Test

Stop at the end of the natural preview:

- Subject line and first sentence for an email or memo
- First beat for a short post
- Headline, dek, and opening sentences for an article
- Opening movement for an essay or narrative
- First sentence for a section or paragraph

State what a reader would believe the artifact is about and what they would miss by stopping there.

### Alignment Test

Compare the declared and delivered BLUFs.

Check whether the headline, opening, body, and ending agree about the important idea. Flag an opening that is clear but foregrounds the wrong thing.

### Delay Test

Inspect everything that appears before the delivered or latent BLUF.

Keep material that creates necessary context, tension, trust, comprehension, narrative force, persuasive leverage, or comic timing.

Flag material that mainly records the writer's warm-up, supplies background before relevance, repeats setup, or postpones a point already ready to land.

Every delay must earn itself.

### Hierarchy Test

Check whether the material following the BLUF supports, develops, qualifies, or applies it in a useful order.

Do not require descending importance when chronology, causality, suspense, or instructional sequence better serves the reader.

### Compression Test

Express the delivered BLUF in one or two sentences.

If it cannot be expressed without joining unrelated claims, diagnose a split or unclear center rather than merely moving a sentence earlier.

## Choose A Verdict

| Verdict | Meaning |
|---|---|
| **Front and center** | The right idea appears where it best serves the artifact. |
| **Delayed but earned** | The point arrives later, but the preceding material improves its comprehension, force, or payoff. |
| **Buried** | The right idea exists, but unnecessary material delays it. |
| **Wrong lede** | The opening clearly foregrounds a secondary idea while a more consequential one appears later. |
| **Unclear or split** | The artifact does not establish one governing idea, or several ideas compete without hierarchy. |

Add a secondary diagnosis only when useful:

- **Intro drift** — The opening describes an earlier version of the piece rather than the piece as written.
- **Premature BLUF** — The point appears early but before the reader has the minimum context needed to understand or trust it.
- **Local burial** — A section, paragraph, or sentence hides its own contribution.
- **Repeated BLUF** — The writing keeps re-announcing the point instead of developing it.

## Report The Diagnosis

For articles, essays, or substantial sections, use:

```markdown
## BLUF Check

**Scope:** [Full piece / section / post / paragraph / sentence]

**Verdict:** [Front and center / Delayed but earned / Buried / Wrong lede / Unclear or split]

**Declared BLUF:** [What the opening foregrounds]

**Delivered BLUF:** [What the artifact actually supports or concludes]

**Latent lede:** [Stronger idea found later, if present]

**Current location:** [Exact paragraph, section, or quoted sentence]

**Best location:** [Where the important idea belongs]

### Placement Diagnosis

[Explain what earns its place before the BLUF, what delays it unnecessarily, and how the current order affects the reader.]

### Smallest Effective Move

[Move, cut, promote, combine, reframe, or preserve.]

### What To Protect

[Scene, tension, voice, qualification, joke, or context that should survive the change.]
```

Omit the latent-lede and protection fields when they do not apply.

For a short post, paragraph, or sentence, compress the output:

```markdown
**Verdict:** [Verdict]

**BLUF:** [Most important idea]

**Placement:** [Where it is and where it belongs]

**Smallest move:** [Specific recommendation]
```

Quote the relevant language and identify its exact location. Do not give a generic instruction to "get to the point."

## Revise Only When Asked

Diagnose and recommend placement by default.

When asked to fix the artifact:

1. Preserve the writer's intended claim and voice.
2. Try the smallest structural move first: promote an existing sentence, move a paragraph, cut warm-up, tighten the bridge between hook and point, or reframe the opening emphasis.
3. Rewrite the opening only when rearrangement cannot solve the problem.
4. Adjust transitions created by the move.
5. Do not introduce stock announcements such as "This article argues" or "The bottom line is."
6. Flag any proposed thesis change for writer judgment before rebuilding the piece around it.

## Boundaries

- Use `cw-hook` to generate an attention-getting opening. A strong hook can still bury or misrepresent the lede.
- Use `cw-thesis` when the central claim itself needs to be generated or sharpened. BLUF judges the hierarchy and placement of ideas already present.
- Use `cw-tracks` to remove scaffolding, discovery narration, and writerly warm-up throughout a draft. BLUF focuses on where the important idea belongs.
- Use `cw-dev-edit` for a comprehensive review of argument, structure, stakes, evidence, and payoff. BLUF is a narrower placement lens.
- Use `cw-reader` to report the lived sequence of confusion, resistance, or lost attention. BLUF makes an editorial judgment about importance and order.
- Use `cw-final-pass` for a publication-readiness verdict. A BLUF check can happen at any stage and on incomplete material.

## Principles

- Put reader value before writer chronology.
- Distinguish attention from importance.
- Treat a clear but secondary opening as a placement failure.
- Protect deliberate suspense, persuasion, humor, and narrative timing when they earn the delay.
- Do not confuse directness with formulaic thesis announcements.
- Prefer the smallest move that reveals the piece already present.
- Keep consequential thesis choices with the writer.
