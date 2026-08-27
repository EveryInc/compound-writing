---
name: cw-line-edit
description: Revise prose at the sentence and word level while preserving voice, meaning, source accuracy, and useful weirdness. Use when the structure is stable and the user asks for a line edit, polish, tightening pass, or usable rewrite.
---

# Line Edit

## Purpose

A deep, rigorous pass for sentence- and word-level issues. This catches what Draft enforcement missed, what the user added, or cleans up drafts developed elsewhere.

Read `../../references/context-contract.md` and load the relevant writer, project, publication, and platform voice sources before editing.

## Entry Points

This skill can be invoked:
1. After completing a developmental edit
2. Directly by the user with any draft

## What to Check

Apply a thorough review for:

### Sentence Mechanics
- Vary sentence length
- Active voice (flag passive constructions)
- Concrete nouns and verbs
- Front-load sentences with important information

### Things to Avoid
- Hedge words ("perhaps," "maybe," "somewhat," "might")
- Correlatives and negative parallelisms ("not X, but Y")
- Throat-clearing (delayed starts, excessive setup)
- Echo statements (saying the same thing multiple ways)
- Weasel words ("some people say," "studies show" without citation)
- Empty intensifiers ("very," "really," "extremely")
- Cliché metaphors
- Hyperbolic or overblown claims
- Inflated language
- Technical, business, or academic jargon

### AI Tells
Run `cw-ai-check` in its required order. When source material or earlier human drafts are available, scan for structural overcompletion before running the full lexicon. Flag and fix:
- Stock openers ("In today's fast-paced world...")
- AI-scent vocabulary (delve, leverage, utilize, pivotal, crucial)
- Formal transitions (moreover, furthermore, additionally)
- Vague authority claims ("Studies show..." without citation)
- Formulaic closers ("In conclusion...")
- Structural patterns ("No X. No Y. Just Z.")
- All patterns in the ai-check lexicon

### Voice Alignment
Check the prose against the active writer and project voice sources. Do not make a sentence cleaner by erasing intent, humor, rhythm, priors, or a distinctive aside.

### Meaning And Provenance
- Preserve the scope and certainty of factual claims.
- Do not sever citations or source attribution from the claims they support.
- Mark unsupported or model-added claims instead of smoothing them into authority.

## Output

### Part 1: Revised Draft

Deliver the full draft with all fixes applied. Present it ready-to-use.

### Part 2: Summary of Changes

After the revised draft, summarize material changes in order of appearance. Do not bury the usable copy beneath a diagnostic preamble.

```
---

## Changes Made

1. **Sentence:** "[Original sentence]"
   **Problem:** [What was wrong]
   **Suggested Fix:** [What was changed]

2. **Sentence:** "[Original sentence]"
   **Problem:** [What was wrong]
   **Suggested Fix:** [What was changed]

[Continue for all changes...]
```

## Reverting Changes

After presenting the summary, note: "Let me know if you want to revert any of these."

Writer can revert by:
- **Number:** "Revert #3 and #7"
- **Natural language:** "Put back the original for the one about hedging"

System handles either format.

## Transition

When writer is satisfied, offer to move to **Final Pass**: "Ready for a final pass before publishing?"

## Lessons

[Skill-specific lessons will be added here as they're captured]
