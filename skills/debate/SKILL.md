---
name: debate
description: Run a multi-round deliberation between reviewers. Unlike /panel (which synthesizes), /debate has reviewers respond to each other's arguments across rounds until tensions resolve or reach acknowledged stalemate.
---

# Debate Review

Orchestrate a structured deliberation between reviewer agents. Reviewers don't just give feedback in parallel—they engage with each other's perspectives, challenge each other's recommendations, and work toward resolution (or acknowledged stalemate).

## When to Use /debate vs /panel

| Use | When |
|-----|------|
| `/panel` | You want multiple perspectives synthesized. Fast. Tensions surfaced for you to decide. |
| `/debate` | You want reviewers to actually argue it out. More thorough. Tensions may resolve through deliberation. |

**Choose /debate when:**
- The piece is high-stakes and worth the extra rounds
- You want to see how perspectives hold up under challenge
- You suspect some tensions might resolve if reviewers engaged each other
- You want proposals and compromises, not just "you decide"

**Choose /panel when:**
- You want comprehensive feedback quickly
- You're comfortable resolving tensions yourself
- Time/tokens are a concern

## The Deliberation Flow

### Round 1: Initial Positions

Same as /panel—all reviewers analyze the draft independently.

### Round 2: Challenges

The moderator identifies tensions and sends challenges to involved reviewers:

```
## Challenge: The fishing gear paragraph

**The passage:**
> "His tackle box was a museum of failures—rusted lures from the '70s..."

**hemingway said:**
> "47 words that could be 15. Cut it."

**sedaris said:**
> "This is the most alive moment in the piece. Keep every word."

---

**hemingway:** sedaris argues the specificity earns its place. How do you respond?

**sedaris:** hemingway argues this slows momentum. How do you respond?
```

### Round 3: Responses

Reviewers respond in character. They may:

- **Concede** — "On reflection, the detail does earn its place. I withdraw."
- **Hold** — "The momentum problem remains. Even good details hurt here."
- **Propose** — "Keep the first image, cut the extended list. Satisfies both."

### Round 4: Resolution

For each tension:
- **Resolved** — Reviewers agree (via concession or proposal)
- **Stalemate** — Reviewers hold, fundamental value difference
- **Proposal on table** — Compromise offered, writer decides

The moderator may run additional rounds if proposals generate new discussion, but caps at 4 rounds.

## The Flow in Practice

### 1. Load Context

Read `../../references/context-contract.md`, the draft, and any available brief, outline, project instructions, feedback, or status metadata. Establish:
- piece_type
- audience
- stage
- goals

Infer missing context from the draft and request. Do not require `.status.yaml`.

### 2. Propose Panel

Same as /panel—propose 4-6 reviewers based on context.

```
## Proposed Panel for Debate

**Draft:** [title]
**Context:** [piece_type] for [audience], [stage]

| Reviewer | Why |
|----------|-----|
| **[name]** | [Rationale] |
| **[name]** | [Rationale] |

**Note:** Debate works best with reviewers who have natural tensions.
Consider including pairs like:
- hemingway + sedaris (economy vs. specificity)
- reader + hitchcock (orientation vs. mystery)
- sorkin + vonnegut (speed vs. depth)

Proceed with this panel, or adjust?
```

Wait for user confirmation.

### 3. Round 1: Run Reviewers

Run all reviewers in parallel when the active platform supports isolated workers and the user's explicit debate request authorizes them. On Claude, use the matching reviewer agents when available; on Codex or another runtime, use the reviewer skills or isolated workers with those lenses. Collect independent outputs.

### 4. Round 2: Identify Tensions and Generate Challenges

Analyze outputs for conflicts. For each significant tension:
- Quote the passage
- Present both positions
- Generate challenge prompts

Spawn challenged reviewers with the challenge context.

### 5. Round 3: Collect Responses

Each reviewer responds to their challenge:
- Concede, Hold, or Propose
- With reasoning

### 6. Round 4: Resolution and Additional Rounds

Determine resolution status. If proposals warrant further discussion, run another round (max 4 total).

### 7. Final Synthesis

Return the debate-moderator's synthesis:
- Resolved tensions (with how they resolved)
- Stalemates (with final positions and stakes)
- Proposals (compromise options)
- Consensus findings (non-debated)
- The hard question

## Panel Selection for Debate

Debate is most valuable when the panel includes natural tensions:

| Pairing | Tension Type | Good For |
|---------|--------------|----------|
| hemingway + sedaris | Economy vs. Specificity | Deciding what earns its length |
| reader + hitchcock | Orientation vs. Mystery | Distinguishing strategic withholding from accidental confusion |
| reader + hemingway | Context vs. Brevity | Deciding what setup a first-time reader needs |
| reader + sorkin | Orientation vs. Momentum | Giving readers footing without slowing the piece |
| mom + hemingway | Accessibility vs. Brevity | Deciding what a non-expert audience needs explained |
| sorkin + sedaris | Momentum vs. Observation | Pacing of descriptive passages |
| sorkin + vonnegut | Speed vs. Depth | When to slow for character |
| asshole + sedaris | Rigor vs. Voice | Tone of argument pieces |

**Recommendation:** Include at least one natural tension pair in your panel.

## Example Session

```
User: /debate

Agent: I'll run a deliberation on your draft. Let me read it and propose a panel.

[Reads draft]
[Loads the brief and project context: personal essay, general audience, revision stage]

## Proposed Panel for Debate

**Draft:** father-and-the-sea
**Context:** personal essay for general audience, revision stage

| Reviewer | Why |
|----------|-----|
| **hemingway** | Check economy—personal essays can get overwritten |
| **sedaris** | Find the specific, human, funny moments |
| **sorkin** | Verify pacing through emotional beats |
| **reader** | Trace the first-time reading experience |

**Natural tensions:** hemingway/sedaris (economy vs. specificity),
sorkin/sedaris (momentum vs. observation)

Proceed with this panel, or adjust?

User: yes

Agent: Running Round 1—each reviewer analyzing independently.

[Spawns 4 reviewers in parallel]
[Collects outputs]

Round 1 complete. Analyzing for tensions.

## Tensions Identified

### Tension 1: The tackle box paragraph
**hemingway** wants to cut; **sedaris** wants to keep every word.

### Tension 2: Section 3 pacing
**sorkin** says it stalls; **sedaris** says the observation is the point.

### Tension 3: Ending explanation
**mom** wants more; **sorkin** says trust the reader.

Proceeding to Round 2 with 3 challenges.

[Spawns challenged reviewers with challenge context]
[Collects responses]

## Round 2 Responses

**Tension 1:**
- hemingway: HOLD — "Momentum matters more than any single detail."
- sedaris: PROPOSE — "Keep 'museum of failures' and the pug. Cut the Reagan line."

**Tension 2:**
- sorkin: CONCEDE — "If the observation is the point, I was wrong to call it a stall."
- sedaris: (no concession needed)

**Tension 3:**
- mom: HOLD — "I still don't know what he learned. That's a real gap."
- sorkin: PROPOSE — "One specific image of the lesson. Not explanation—scene."

Proceeding to final synthesis.

## Debate Synthesis

**Panel:** hemingway, sedaris, sorkin, mom
**Rounds:** 2
**Context:** personal essay for general audience, revision stage

---

### Resolved Tensions

**Section 3 pacing**

> [The observation passage]

**Resolution:** Sorkin conceded. The slow pace is intentional and earns its place.
**Recommendation:** Keep as-is. The observation is the point.

---

### Stalemates

*None—all tensions reached resolution or proposal.*

---

### Proposals

**The tackle box paragraph**

> "His tackle box was a museum of failures—rusted lures from the '70s,
> a reel that hadn't worked since Reagan, hooks that had never caught
> anything but his own thumb."

**Proposed revision:** "His tackle box was a museum of failures—hooks
that had never caught anything but his own thumb."

**Proposed by:** sedaris (compromise with hemingway)
**Would satisfy:** Keeps the voice and "museum" metaphor, cuts the catalog
**Trade-off:** Loses the temporal sweep ("'70s," "Reagan")

---

**The ending**

**Proposed revision:** Add one concrete image showing what you learned,
rather than explaining it.

**Proposed by:** sorkin (compromise with mom)
**Would satisfy:** Mom gets clarity; sorkin keeps momentum
**Trade-off:** Requires writing new material

---

### Consensus Findings

| Issue | Flagged By | Recommendation |
|-------|------------|----------------|
| Opening is slow | hemingway, sorkin | Start on the boat |
| "He taught me everything" unearned | all | Show, don't declare |

---

### The Deliberation Summary

**Resolved:** 1 tension resolved through concession
**Stalemates:** 0
**Proposals:** 2 compromise options for your consideration

---

### The Hard Question

> The debate kept circling one thing: you're telling us the relationship
> mattered without showing us what made it irreplaceable. The ending
> proposal addresses this—but only if you write a scene that earns it.
```

## Cost And Scope

Debate is materially slower and more context-intensive than panel because reviewers receive follow-up challenges. Use it for consequential tensions, cap the number of rounds, and prefer `panel` for routine coverage.

## Error Handling

**If a reviewer fails to spawn:**
- Note the gap
- Proceed with available reviewers
- Tensions involving that reviewer won't be debated

**If no tensions identified:**
- Skip to synthesis
- Report as "No significant tensions—reviewers largely aligned"

**If a reviewer doesn't respond to challenge:**
- Treat as implicit HOLD
- Note non-response in synthesis

**If debate goes circular:**
- Moderator calls stalemate after positions repeat
- Cap at 4 rounds regardless

## Relationship to /panel

`/panel` and `/debate` share infrastructure:
- Same reviewer agents
- Same context loading from the active project and artifact
- Same panel proposal logic

The difference:
- `/panel` → synthesizer (one pass, tensions surfaced)
- `/debate` → moderator (multiple rounds, tensions engaged)

A natural workflow: run `/panel` first for quick feedback, then `/debate` on specific tensions if you want them argued out.

## Lessons

[Skill-specific lessons will be added here as they're captured]
