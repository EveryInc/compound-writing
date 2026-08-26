---
name: cw-draft
description: Turn an outline, notes, source material, or partial prose into a complete draft while preserving the writer's voice, thesis ownership, and source provenance. Use when the user asks to draft a piece or section.
---

# Draft

## Purpose

Turn the available material into usable prose. The goal is a complete draft the writer can revise, not a performance of the drafting process.

## Load Context And Sources

Read `../../references/context-contract.md`. Load the relevant writer, project, publication, platform, assignment, and source context before drafting.

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
Apply the maintained writer and project voice guidance. Use plugin defaults only for gaps:
- Conversational but authoritative
- Accessible without dumbing down
- Confident with nuance
- Intellectually generous

### Sentence Structure
Apply the active syntax and diction guidance:
- Vary sentence length
- Active voice preferred
- Concrete nouns and verbs
- Front-load important information

### Things to Avoid
Check the active voice and style files for the writer's specific list. Common fallback checks:
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
- Apply all silent enforcement
- Return complete draft
- Flag any sections that felt weak or uncertain

## Lessons

[Skill-specific lessons will be added here as they're captured]
