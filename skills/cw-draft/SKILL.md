---
name: cw-draft
description: Turn an outline, notes, source material, or partial prose into a complete draft while preserving the writer's voice, thesis ownership, and source provenance. Use when the user asks to draft a piece or section.
---

# Draft

## Purpose

Turn the available material into usable prose. The goal is a complete draft the writer can revise, not a performance of the drafting process.

## Load Context And Sources

Read `../../references/context-contract.md`. Load the relevant writer, project, publication, platform, assignment, and source context before drafting.

Before writing any prose, read the writer's gold examples by following `../../references/voice-from-examples.md` and build a voice read. Then read the `VOICE.md` lessons. Draft to the voice read; do not draft first and adjust afterwards.

- Treat maintained voice and project guides as authoritative.
- If creating a new local draft file in a project initialized by `cw-setup-project`, use `drafts/<piece-slug>/` and keep its versions plus support material together. In other projects, follow the existing artifact convention and do not impose `drafts/` retroactively.
- Keep factual claims attached to their sources.
- Mark model-added assumptions or unsupported bridges instead of inventing certainty.
- Preserve the writer's thesis; surface a materially different thesis for judgment before rebuilding the piece around it.

## Your Approach

**Default:** Section by section with casual check-ins.
**Alternative:** All at once if the writer prefers or the piece is short.

Use judgment about pacing. Some writers want to see each section before moving on. Others want a complete draft to react to. Ask if unclear, or infer from context.

## Silent Enforcement

Produce usable copy that reflects the active context without narrating every rule being applied.

### Voice
Write every sentence to the voice read from the gold examples: their openings, construction, length mix, paragraph endings, verbs, register, punctuation, and absences, at the rates the examples show. Apply `VOICE.md` lessons on top.

Before handing off each section, compare it with the examples. When a section runs long, check it with the counter (`--compare`, see the procedure) and bring any feature outside the examples' range back in line.

When no gold examples exist, say so once, draft with the `VOICE.md` lessons and these fallbacks, and label the draft **not calibrated to examples**:
- Vary sentence length
- Concrete nouns and verbs
- Front-load important information

### Things to Avoid
Avoid what the gold examples never do, plus anything in the `VOICE.md` lessons. Common fallback checks, which yield to the examples where they consistently do otherwise:
- Hedge words, weasel words
- Throat-clearing, echo statements
- Cliché metaphors, empty intensifiers
- Jargon without explanation

### AI Pattern Removal
Silently apply `cw-ai-check` in its required order: preserve source boundaries and epistemic temperature before removing lexical or sentence-pattern residue. User sees clean copy only.

## Structural Moves

Apply these where appropriate (not as requirements):

| Element | Guidance |
|---------|----------|
| **Hook** | Select from Hook Arsenal based on content |
| **Thesis** | Ensure it appears clearly and is arguable |
| **Promise** | Opening should create anticipation |
| **Transitions** | Natural bridges, avoid academic connectors |

**Hook Arsenal** (use judgment):
- The Already-Happened, The Paradigm Flip, The Visceral Moment
- The Time Stamp, The Failed Expert, The Future Glimpse
- The Contradiction, The Vulnerability Drop
- The Stats Shock, The Definitional Challenge

## Section Handoffs

Keep it casual:
- "Here's the intro—thoughts before I move on?"
- "Section 2 is ready. Take a look?"
- "Here's the conclusion. How does it land?"

**Don't block on approval.** If the writer doesn't respond to a handoff, continue. They can circle back.

## Flexibility

- Writer can skip sections ("Just draft the middle")
- Writer can provide partial content ("Here's the intro I wrote, draft the rest")
- Writer can request rewrites mid-stream
- Writer can draft themselves and use this skill for specific sections

## Completion

The requested drafting work is done when:
- All sections exist in some form, OR
- Writer says it's done

Offer the next pass only when it would help. Do not force a full pipeline after finishing the requested draft.

## For Agents

When invoked programmatically:
- Accept outline (any depth) as input
- Build the voice read from the gold examples first, and save it as `voice-read.md` in the piece folder when there is one
- Apply all silent enforcement
- Return complete draft
- Name the gold examples the voice read came from
- Flag any sections that felt weak or uncertain

## Lessons

[Skill-specific lessons will be added here as they're captured]
