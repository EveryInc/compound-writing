---
name: cw-panel
description: Convene a panel of reviewers to analyze a draft from multiple perspectives, then synthesize their feedback into consensus findings, productive tensions, and prioritized recommendations.
---

# Panel Review

Convene multiple reviewer agents to analyze a piece, then synthesize their perspectives into a unified analysis that surfaces consensus, tensions, and priorities.

## When to Use

- Before publishing something high-stakes
- When you want multiple perspectives without running reviewers manually
- When you suspect different aspects need different kinds of attention
- When you're too close to the work to know what feedback you need

## The Flow

### 1. Load Context

Read `../../references/context-contract.md`, the draft, and any available brief, outline, project instructions, feedback, or status metadata to understand:
- **piece_type** — essay, argument, explainer, narrative, etc.
- **audience** — general, specialist, insider
- **stage** — early draft, revision, near-final
- **goals** — if stated

Infer missing context from the draft and request. Do not require `.status.yaml`.

### 2. Propose Panel

Based on piece context, propose 4-6 reviewers.

**Selection heuristics:**

| Signal | Suggests Including |
|--------|-------------------|
| Personal/reflective content | sedaris, mom |
| Argumentative content | asshole, vonnegut |
| Technical or jargon-heavy | reader, mom, hemingway |
| Narrative structure | vonnegut, hitchcock, sorkin |
| Feels slow or wandering | sorkin |
| Feels bloated | hemingway |
| High-stakes / pre-publish | asshole, hemingway |
| Cold read, uncertain audience response, or missing setup | reader |
| General audience | reader |
| Non-expert accessibility | mom |
| Early stage | vonnegut (fundamentals) |
| Late stage | hemingway, asshole (polish, stress-test) |

**Check the active writer and project context for:**
- Preferred reviewers
- Reviewers to exclude
- Past patterns

**Present the proposal:**

```
## Proposed Panel

**Draft:** [title or slug]
**Context:** [piece_type] for [audience], currently at [stage]

Based on this context, I recommend:

| Reviewer | Why |
|----------|-----|
| **[name]** | [One-line rationale tied to piece context] |
| **[name]** | [Rationale] |
| **[name]** | [Rationale] |
| **[name]** | [Rationale] |

**Not including:**
- **[name]** — [Why not relevant for this piece]
- **[name]** — [Why not]

Proceed with this panel, or adjust?
```

Wait for user confirmation or modification.

### 3. Run Reviewers in Parallel

Once confirmed:

1. Run all selected reviewers in parallel when the active platform supports parallel workers and the user's explicit panel request authorizes them.
   - On Claude, use the matching `compound-writing:review:*` subagent when available.
   - On Codex or another runtime, use the matching reviewer skill or an isolated worker with that lens.
   - Give each reviewer the draft plus the minimum relevant context.
   - Each reviewer returns its standard prose output independently.
2. Collect all outputs

**Example spawning pattern:**

```
[Spawn in parallel:]
- Task: asshole-reviewer with draft
- Task: mom-reviewer with draft
- Task: hemingway-reviewer with draft
- Task: sorkin-reviewer with draft
```

### 4. Run Synthesizer

Use the panel-synthesizer agent when available; otherwise synthesize the outputs directly. Include:
- The draft
- Draft context from the active brief, instructions, metadata, or careful inference
- All reviewer outputs (full prose)

**Synthesizer prompt should include:**

```
## Draft

[full draft text]

## Context

piece_type: [from context or inference]
audience: [from context or inference]
stage: [from context or inference]
goals: [from context if present]

## Reviewer Outputs

### asshole-reviewer
[full output]

### mom-reviewer
[full output]

### hemingway-reviewer
[full output]

[etc.]
```

### 5. Return Synthesis

Present the synthesizer's output to the user.

## Panel Size

- **Minimum:** 3 reviewers (fewer than this, just run them individually)
- **Recommended:** 4-5 reviewers (good coverage without redundancy)
- **Maximum:** 8 reviewers (all of them—full stress test)

## Available Reviewers

| Reviewer | Subagent Type | Focus |
|----------|---------------|-------|
| asshole | compound-writing:review:asshole-reviewer | Logical rigor, unsupported claims |
| reader | compound-writing:review:reader-reviewer | First-time reading experience, missing setup, trust and friction |
| mom | compound-writing:review:mom-reviewer | Accessibility, jargon, general reader |
| hemingway | compound-writing:review:hemingway-reviewer | Economy, cutting, word-level |
| sedaris | compound-writing:review:sedaris-reviewer | Specificity, humor, voice |
| sorkin | compound-writing:review:sorkin-reviewer | Pacing, momentum, forward motion |
| vonnegut | compound-writing:review:vonnegut-reviewer | Story fundamentals, structure |
| hitchcock | compound-writing:review:hitchcock-reviewer | Tension, suspense, stakes |

## Default Panels by Piece Type

If the active context names a piece type, use it as a starting point:

| piece_type | Default Panel |
|------------|---------------|
| `essay` / `personal` | reader, sedaris, vonnegut, sorkin |
| `argument` / `opinion` | asshole, vonnegut, hemingway, reader |
| `explainer` / `technical` | reader, mom, hemingway, sorkin |
| `narrative` / `story` | vonnegut, hitchcock, sorkin, sedaris |
| `newsletter` | reader, sorkin, hemingway |

Always adjust based on specific signals in the draft.

## Example Session

```
User: /cw-panel

Agent: I'll convene a panel to review your draft. Let me read it and check the status.

[Reads draft]
[Loads the brief and project context: personal essay, general audience,
 revision stage, goal: "make it land emotionally without being sappy"]

## Proposed Panel

**Draft:** father-and-the-sea
**Context:** essay for general audience, revision stage

Based on the context—personal essay aiming for emotional impact without
sentimentality—I recommend:

| Reviewer | Why |
|----------|-----|
| **mom** | General audience check. Will flag where you lose non-insiders. |
| **sedaris** | Personal material that might benefit from more specificity or humor. |
| **sorkin** | Revision stage—check if pacing is tight. |
| **asshole** | The emotional claims need to be earned, not asserted. |

**Not including:**
- **hemingway** — The prose reads clean; economy isn't the issue here
- **hitchcock** — Not a tension-driven piece
- **vonnegut** — Structure is solid; this needs polish not fundamentals

Proceed with this panel, or adjust?

User: Add hemingway actually, I think it might be overwritten

Agent: Adding hemingway. Running the panel now.

[Spawns 5 reviewer agents in parallel]
[Collects outputs]
[Spawns panel-synthesizer with draft + context + all outputs]

## Panel Synthesis

**Panel:** asshole, hemingway, mom, sedaris, sorkin
**Piece context:** essay for general audience, revision stage, goal: emotional
impact without sappiness

---

### Consensus Findings

| Issue | Flagged By | Recommendation |
|-------|------------|----------------|
| Opening two paragraphs are slow | sorkin, hemingway, asshole | Cut or restructure—start closer to the boat |
| "He taught me everything" is unearned | asshole, sedaris | Show what he taught, don't declare it |
| Section 3 gets abstract | mom, sorkin | Ground it in a specific moment |

---

### Productive Tensions

**Tension: The fishing gear paragraph**

> "His tackle box was a museum of failures—rusted lures from the '70s, a reel
> that hadn't worked since Reagan, hooks that had never caught anything but
> his own thumb."

| Cut it | Keep it |
|--------|---------|
| **hemingway:** 47 words that could be 15. "His tackle box held decades of failure" does the job. | **sedaris:** This is the most alive moment in the piece. The specific details are doing real work. |

**What's at stake:** The piece aims for emotional impact without sappiness.
Specific, wry details (sedaris) might be the path there. But if they slow
momentum, they work against the goal.

---

### Unique Insights

- **sedaris:** "There's a joke hiding in the part about him never admitting he
  was wrong. You're circling it but won't commit."
- **asshole:** "Your ending asks the reader to feel something you haven't set
  up. The 'I finally understood' move is unearned."

---

### Recommended Priorities

1. **Restructure the opening** — Three reviewers flagged this. Start on the
   boat, not before it.
2. **Earn the ending** — The emotional payoff needs setup. Show what you
   finally understood through a scene, not a declaration.
3. **Decide on the tackle box** — Genuine tension. Your call based on what
   you're optimizing for.

---

### The Hard Question

> What specifically did you learn from him that you couldn't have learned from
> anyone else? Multiple reviewers noted you assert the relationship's importance
> without showing what made it irreplaceable.
```

## Error Handling

**If a reviewer fails to spawn:**
- Note which reviewer is missing
- Proceed with available outputs
- Mention the gap in synthesis

**If the draft has no metadata:**
- Infer what you can from the draft and request.
- State only assumptions that affect the panel or verdict.
- Do not create a status file merely to run the review.

**If user provides no draft:**
- Ask for the draft path or slug to load
- Or ask them to paste the draft

For tensions that deserve another round, offer `cw-debate`; do not automatically spend the extra time and context.

## Lessons

[Skill-specific lessons will be added here as they're captured]
