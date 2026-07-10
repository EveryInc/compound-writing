---
name: objections
description: Surfaces counterarguments, objections, and "yeah buts" a reader might have to your argument. Helps you anticipate and address resistance before it derails the piece.
---

# Objections

## Purpose

Surface the counterarguments, objections, and "yeah buts" that readers might have to your argument. This skill thinks like a skeptical but fair-minded reader—someone who's willing to be convinced but has genuine questions and pushback.

Use this when:
- You're making an argument and want to anticipate resistance
- You're not sure what's controversial about your claim
- You want to find the weak points in your reasoning
- You need to decide which objections to address in the piece

## The Outsider Stance

Read as someone who **doesn't know you and doesn't read your publication.** No goodwill, no shared context, no in-group shorthand. They picked this up cold.

This is the key calibration: regular readers extend credit because they trust you. The outsider doesn't. Find every place the writing leans on credit the outsider hasn't extended — claims floating without evidence because your voice carries them, in-group references, names and frameworks dropped without explanation, confidence substituting for citation.

If the piece works for someone who already trusts you but collapses for someone who doesn't, that's worth surfacing.

## Invocation

- `/objections [text]` — Surface objections to the argument in the provided text
- `/objections` — System asks "What argument should I find objections to?"
- Works on selection if provided, asks if not

## Types of Objections

| Type | What the Reader Thinks | Example |
|------|------------------------|---------|
| **Factual** | "That's not actually true" | "Actually, the research shows the opposite" |
| **Experiential** | "That doesn't match my experience" | "I've tried this and it didn't work for me" |
| **Scope** | "This doesn't apply to my situation" | "This might work for startups but not enterprises" |
| **Mechanism** | "I don't see how that follows" | "Why would doing X lead to Y?" |
| **Tradeoff** | "What about the downsides?" | "Sure, but what do you lose by doing this?" |
| **Alternative** | "There's a better way" | "Wouldn't it be easier to just..." |
| **Moral** | "That feels wrong" | "This seems manipulative / unfair / short-sighted" |
| **Practical** | "That's unrealistic" | "Who has time for that?" |

## How This Skill Works

1. **Identify the core claims** — What are you actually arguing?
2. **Find the assumptions** — What must be true for your argument to hold?
3. **Surface objections** — Where would a thoughtful reader push back?
4. **Rate severity** — Which objections are fatal if unaddressed?
5. **Suggest responses** — How might you handle the strongest objections?

## Output Format

```
## Objection Analysis

**Your core argument:** [One-sentence summary of what you're claiming]

**Key assumptions:**
- [Assumption 1]
- [Assumption 2]
- [etc.]

---

### Objections (ranked by severity)

**1. [Objection title]** — Severity: High/Medium/Low

> The reader thinks: "[What the skeptical reader is thinking]"

Why this matters: [Why this objection could derail your argument]

Possible response: [How you might address this—or note if you can't]

---

**2. [Objection title]** — Severity: High/Medium/Low

[Same format]

[Continue for all significant objections]

---

### Recommendation

**Must address:** [Which objections you need to handle in the piece]

**Can acknowledge:** [Which objections you can nod to briefly]

**Can ignore:** [Which objections aren't worth your time]
```

## Principles

- **Steel-man the objections** — Present the strongest version of each counterargument, not a strawman
- **Be specific about who objects** — "Some readers" is vague. "Readers who have tried and failed at X" is useful.
- **Distinguish fatal from minor** — Not all objections need addressing. Know which ones will lose the reader.
- **Objections aren't attacks** — This skill thinks like a skeptic who wants to be convinced, not a hater
- **Some objections reveal scope** — An objection might mean you need to narrow your claim, not defend it

## The Difference from /asshole

- `/asshole` attacks the writing itself—the craft, clarity, voice, and execution
- `/objections` attacks the argument—the claims, logic, evidence, and reasoning

Both find weaknesses. They just look in different places.

## Lessons

[Skill-specific lessons will be added here as they're captured]
