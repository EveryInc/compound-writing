---
name: cw-simplify
description: Rewrite complex text in plainer language. Invoke with /cw-simplify or /cw-simplify [paste text].
---

# Simplify

## Purpose

Rewrite something complex in plainer, more accessible language without losing meaning.

## Invocation

- `/cw-simplify [text]` — Simplify the provided text
- `/cw-simplify` — System asks "What section do you want me to simplify?"
- Works on selection if provided, asks if not

## How to Simplify

1. **Identify the core meaning** — What is this actually saying?

2. **Strip jargon** — Replace technical terms with plain equivalents, or define them briefly on first use.

3. **Shorten sentences** — Break long, complex sentences into shorter ones.

4. **Use concrete language** — Swap abstractions for specific examples.

5. **Front-load the point** — Lead with the main idea, then explain.

6. **Preserve precision** — Don't oversimplify to the point of inaccuracy.

## Output Format

```
## Simplified Version

[The rewritten text]

---

**What changed:**
- [Brief note on key simplifications]

Does this capture it? Or did I lose something important?
```

## Principles

- **Short words over long** — "use" not "utilize," "help" not "facilitate"
- **Active over passive** — "We built" not "It was built by us"
- **One idea per sentence** — Break up compound ideas
- **Concrete over abstract** — "a 10% increase" not "significant growth"
- **Reader-first** — Write for someone encountering this idea for the first time

## Simplification Moves

| Complex Pattern | Simplified Version |
|-----------------|-------------------|
| Nominalization (the utilization of) | Verb form (using) |
| Passive voice (was implemented by) | Active voice (we implemented) |
| Jargon (synergize, leverage) | Plain verbs (combine, use) |
| Long sentence with multiple clauses | Multiple short sentences |
| Abstract noun (implementation) | Concrete action (we built) |
| Hedge words (somewhat, perhaps) | Direct statement or cut |

## What to Preserve

- Technical accuracy
- Important nuance
- The writer's voice
- Necessary qualifications

## Lessons

[Skill-specific lessons will be added here as they're captured]
