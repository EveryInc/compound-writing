---
name: ai-check
description: Scan text for AI writing patterns and produce cleaned copy. Auto-runs during Draft; invoke manually with /ai-check [text].
---

# AI Check

## Purpose

Identify common linguistic patterns that signal AI-generated writing and rewrite them to sound more natural and human.

## Invocation

- **Auto-invoked** during Draft stage on all generated copy (silent enforcement)
- `/ai-check [text]` — Manually scan provided text
- `/ai-check` — System asks "What do you want me to check?"

## Behavior by Context

### During Draft (Auto-Invoked)
- Scan all generated copy
- Catch and rewrite AI tells silently
- User sees clean copy only—no explanations

### Manual Invocation (/ai-check)
- Scan the provided text
- Output cleaned copy first
- Then explain what was changed

## Core Detection Categories

### 1. Openers (High Severity)
Stock contextless openings:
- "In today's fast-paced world"
- "In the ever-evolving landscape of [X]"
- "In the realm of [X]"
- "Let's dive in" / "Let's break it down"
- "At its core, [X] is [Y]"
- "It is important/worth noting that [X]"

**Fix:** Start with a concrete fact, date, scene, or proper noun.

### 2. AI-Scent Vocabulary (Medium-High Severity)
Puffery and corporate abstraction:
- delve, delved, delving
- deep dive
- leverage, utilize, harness, unlock, unleash, empower
- pivotal, crucial, significant, noteworthy
- groundbreaking, cutting-edge, revolutionary
- navigate the complexities of
- explore the intricacies of

**Fix:** Use plain verbs (use, try, test, make). Swap abstractions for specifics.

### 2b. MBA / Corporate Abstraction Nouns (Medium-High Severity)
Business-school nouns that puff a plain word into something self-important:
- "problem space" → "problem" or "issue"
- "solution space" → "options" or "approaches"
- "value proposition" → "offer" or "what it does for you"
- "go-to-market motion," "north star metric," "operating cadence"
- "frameworks for thinking about [X]" → "how to think about X" or just make the point
- "mental models around [X]" → "how to think about X"
- Pattern: `noun + "space"`, `noun + "motion"`, `noun + "around"`

**Fix:** Use the plain word the abstraction is hiding. If the writer can't say what "problem space" means in plain English, they don't yet know what they're arguing about.

### 3. Filler Words (Medium Severity)
- "just" (when used as emphasis, not temporal)
- "actually" (when used as emphasis, not contradictory)

**Fix:** Delete unless serving essential function.

### 4. Transitions (Medium Severity)
Formal academic connectors:
- moreover, furthermore, additionally
- consequently, thus, hence, therefore
- not only...but also

**Fix:** Use looser transitions (and, but, so, though, yet) or restructure.

### 5. Vague Authority (Medium Severity)
- "Studies show that [X]" (without citation)
- "Experts agree that [X]" (without names)
- "Research indicates [X]"
- "According to recent reports, [X]"

**Fix:** Name the study, link it, include dates—or delete the claim.

### 6. Correlatives & Negative Parallelisms (High Severity)
- "not X but Y" / "not X, but Y"
- "not just X, also Y"
- "not because X, but because Y"
- Consecutive "It's not about X. It's about Y." patterns

**Fix:** Rewrite with simple contrast or direct statement.

### 7. Structural Patterns (Medium-High Severity)
- "No X. No Y. Just Z." — formulaic three-beat structure
- Staccato declarative triads (three parallel short sentences)
- **Triplet sentences where one strong sentence would do** — three short parallel sentences doing the work of one. If the second and third just rephrase the first for rhythm, collapse them.
- Excessive rule of threes
- Overly symmetric lists and paragraphs
- **Dropped "and" in serial lists (asyndeton)** — "She opened the laptop, ran the script, watched it fail." LLMs reach for this for "rhythm." Humans usually keep the "and." Restore the conjunction unless you're deliberately reaching for staccato effect — and even then, use it once, not as the default.

**Fix:** Vary rhythm, break parallel structure, expand at least one element. Default to a single strong sentence over a triplet. Default to keeping the "and."

### 7b. Aphoristic Equations / AI Cleverisms (High Severity)
Symmetrical, quotable lines that sound like insight but are just shapes:
- "X without Y is just Z" — "A coach without context is just a chatbot."
- "X is Y for Z" — "Prompts are the new code."
- "What gets X gets Y" — "What gets named gets measured."
- "The best X is the X that doesn't [verb]"
- Any line that reads like a tweet pretending to be a thesis

**Why it reads as AI:** The shape is doing the persuading, not the content. The line is portable because it's empty — it would work for any topic with the right two nouns swapped in.

**Fix:** Either back it with the specific evidence or example that made the writer say it, or cut. If the aphorism is genuinely earned, prove it. If it isn't, it's just a quotable hole.

### 8. Closers (High Severity)
- "In conclusion"
- "Overall"
- "Ultimately"
- "To sum up"

**Fix:** End on a sharp implication, next step, or specific unanswered question.

## Output Format (Manual Invocation)

```
## Cleaned Copy

[The rewritten text with all AI tells removed]

---

## What Changed

**[Category] ([N] instances)**
1. **Original:** "[phrase]"
   **Changed to:** "[revision]"
   **Why:** [brief explanation]

[Continue for all changes...]

**Summary:** [X] AI tells found and fixed. Primary issues: [top patterns].
```

## References

See `references/ai_tells_lexicon.csv` for the complete pattern library with:
- 170+ patterns across all categories
- Severity ratings
- Regex patterns for detection
- Human alternatives

## User Extensions

Users can add their own AI tells via `/save` or in-flow capture. These get added to the lexicon and checked in future sessions.

## Lessons

[Skill-specific lessons will be added here as they're captured]
