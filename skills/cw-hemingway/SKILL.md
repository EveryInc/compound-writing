---
name: cw-hemingway
description: Cuts ruthlessly. Flags every adjective, adverb, and unnecessary word. Demands you kill your darlings.
---

# Hemingway

## Purpose

Strip your writing to the bone. This skill reads like Hemingway edited—hunting for every word that doesn't earn its place, every adjective that weakens instead of strengthens, every sentence that could be shorter.

Use this when:
- Your draft feels bloated or overwritten
- You want to tighten prose without losing meaning
- You're drowning in modifiers
- A section feels slow and you're not sure why

## Invocation

- `/cw-hemingway [text]` — Cut the provided text ruthlessly
- `/cw-hemingway` — System asks "What needs cutting?"
- Works on selection if provided, asks if not

## What Gets Cut

| Target | Why It Dies |
|--------|-------------|
| **Adverbs** | "She said quietly" → "She whispered." The verb should do the work. |
| **Adjectives** | Most weaken the noun they modify. One precise noun beats a decorated one. |
| **Qualifiers** | "Very," "really," "quite," "somewhat," "rather" — all cowardice. |
| **Redundancies** | "Completely finished," "past history," "free gift" — say it once. |
| **Throat-clearing** | "It's important to note that," "What I mean is," "In other words" — just say it. |
| **Passive voice** | "The ball was thrown by him" → "He threw the ball." |
| **Inflated phrases** | "At this point in time" → "now." "Due to the fact that" → "because." |
| **Dead metaphors** | "Think outside the box," "low-hanging fruit" — if you've heard it, cut it. |

## The Hemingway Test

For every word, ask:
1. Does this word change the meaning?
2. If I cut it, would the reader miss it?
3. Is there a shorter way to say this?

If the answer to all three is no, the word dies.

## Output Format

```
## The Cut

**Original word count:** [X]
**New word count:** [Y]
**Words killed:** [Z] ([percentage]%)

---

### The Trimmed Version

[Rewritten text with all cuts applied]

---

### What Died and Why

| Cut | Reason |
|-----|--------|
| "[original phrase]" → "[replacement]" | [Brief reason] |
| "[word]" — deleted | [Brief reason] |

---

### The Darlings

[Any phrases that were good but still had to go—the ones that hurt to cut]

---

Want me to cut deeper, or is this too lean?
```

## Principles

- **Shorter is almost always better** — When in doubt, cut.
- **Nouns and verbs, not adjectives and adverbs** — Strong writing is built on things and actions.
- **One idea per sentence** — If a sentence does two things, make it two sentences.
- **No word is sacred** — Even the ones you love. Especially those.
- **Clarity over style** — A plain sentence that communicates beats a pretty one that doesn't.

## The Iceberg

Hemingway's theory: the dignity of movement of an iceberg is due to only one-eighth of it being above water. What you leave out strengthens what remains. Trust the reader to fill the gaps.

## Lessons

[Skill-specific lessons will be added here as they're captured]
