---
name: dev-edit
description: Review a draft for big-picture issues in argument, structure, stakes, evidence, and payoff. Use when a piece needs developmental editing, a top-level diagnosis, or substantial restructuring before sentence polish.
---

# Developmental Edit

## Purpose

Review a draft for big-picture issues: argument, structure, stakes, and payoff. Focus on whether the piece *works*, not whether the sentences are polished.

Read `../../references/context-contract.md` and load the relevant assignment, project, publication, source, and voice context before judging the draft.

Keep the writer in the loop on thesis development. Surface evidence and counterarguments that pressure the thesis, present possible moves, and do not quietly replace the core argument.

## Entry Points

- After completing a draft through the workflow
- Directly with any draft from anywhere
- As part of a composed "make this better" request

## What to Look For

Questions to consider (not all apply to every piece):

| Area | Questions |
|------|-----------|
| **Structure** | Does each section earn its place? Does the order make sense? |
| **Argument** | Is it logically clear and supported? Any holes? |
| **Evidence** | What backs each major claim? Personal experience? A linked study? A specific example? Where is the support thin or missing? |
| **Outsider read** | If a reader who doesn't know the writer or publication picked this up cold, what would they push back on? What would feel like in-group shorthand? |
| **Opening** | Does the hook work? Is the thesis clear? Is there a promise? |
| **Stakes** | Why should the reader care? Why does the writer care? |
| **Payoff** | Does the piece deliver on what it promises? |

**Use judgment.** A personal essay doesn't need argument scrutiny. A how-to doesn't need stakes analysis. Focus on what matters for this piece.

## The Structural Tests

Two diagnostic tests for whether the piece holds together. Run both when the structure feels off — or proactively for any piece with subheads.

### The Subsection Summary Test

For each subsection: write a one-sentence summary of what it argues. Then re-read the subsection. Anything not in service of that one sentence — cut it.

When invoked by the agent:
1. Identify each subsection (subhead-defined or paragraph-cluster).
2. Generate a one-sentence argument summary per subsection.
3. Flag paragraphs, examples, or asides that don't serve their subsection's summary.
4. Report the summaries alongside the flagged content so the writer can decide what stays.

This test catches: orphaned good lines that belong elsewhere, padding from earlier drafts, two arguments tangled inside one subsection.

### The 20-Second Pitch Test

If someone stopped the writer in a hallway, could they explain the piece in 20 seconds? Now compare that pitch to the thesis/promise as stated in the intro.

When invoked by the agent:
1. Generate a 20-second pitch from the piece as written (what it's actually about, end to end).
2. Pull the thesis/promise from the intro as stated.
3. Show both side by side. Flag the gap.

If the pitch and the intro don't match, one of them is wrong. Usually the intro drifted during revision and needs to catch up to what the piece became.

## Evidence Check

For each major claim, ask: what is this backed by?

| Support type | Verdict |
|--------------|---------|
| Personal experience the writer lived through | Strong — let it stand |
| A linked study, dataset, or named source | Strong — let it stand |
| An expert quote or named practitioner | Strong — let it stand |
| A specific named example (company, person, moment) | Strong — let it stand |
| "Studies show…" / "experts agree…" / "many people say…" without specifics | Weak — flag |
| Only the writer's authority, when the writer isn't established on this specific thing | Weak — flag |
| Nothing — assertion floats free | Weak — flag |

It's fine to write about something the writer isn't an expert in. It's not fine to make claims without support and rely on confident tone to carry them. Flag floating claims explicitly — the writer can add evidence, soften the claim, or remove it.

## Output Options

### Full Report (default for comprehensive review)

```
## Developmental Edit Report

### Opening
🔴 **Critical:** [Issue]
[Why it matters]

🟡 **Consider:** [Issue]
[Explanation]

### [Section Name]
🟢 **Minor:** [Issue]
[Explanation]

---

Where would you like to start?
```

**Severity:**
- 🔴 Critical — Piece doesn't work without fixing
- 🟡 Consider — Would strengthen significantly
- 🟢 Minor — Nice to have

### Quick Assessment (for faster feedback)

```
## Quick Dev Edit

**Working well:** [2-3 things]

**Needs attention:**
1. [Main issue + why]
2. [Second issue + why]

**Overall:** [Ready for line edit / Needs another pass / Major restructure needed]
```

Use quick assessment for shorter pieces, time pressure, or when invoked as part of a composition.

## Collaborative Fixing

After the report:
1. Writer picks where to start (or skip straight to line edit)
2. Offer fixes: "Here's how I'd address this—[fix]. Want me to make this change?"
3. Writer accepts, revises themselves, or skips
4. Repeat as needed

**Don't force resolution of every issue.** The writer decides what matters.

## Flexibility

- Writer can ask for specific focus ("Just look at the structure")
- Writer can skip dev-edit entirely
- Writer can run multiple passes
- Can be combined with other feedback (asshole read, objections) for stress testing

## For Agents

When invoked programmatically:
- Accept draft as input
- Return structured assessment (issues + severity)
- Include "overall readiness" indicator
- Can be composed with other review skills

## Lessons

[Skill-specific lessons will be added here as they're captured]
