---
name: cw-save
description: Capture a confirmed writing preference, editorial lesson, recurring failure pattern, or workflow improvement in the right durable context file. Use when the user asks to save, remember, codify, or turn a repeated correction into a rule.
---

# Save

Turn a confirmed observation into maintained context so future work can use it. Do not claim memory unless a real file or system is updated.

## Load The Context Contract

Read `../../references/context-contract.md` and inspect the active project's instruction and style files before choosing a destination.

## Classify The Learning

| Learning | Preferred destination |
|---|---|
| Syntax, diction, tone, cadence, register, punctuation, verbal tic, or sentence-construction correction that the gold examples did not prevent | A dated lesson in the governing `VOICE.md`. If the writer's own writing already shows the right move, offer to add that piece to `examples/` instead |
| A piece the writer says sounds like them, or no longer does | Add it to, or remove it from, `examples/` (counterexamples go in `examples/negative/`) |
| Argument, evidence, article structure, substantive standard, audience promise, format, or publication-readiness criterion | The governing `STYLE.md` |
| Confirmed reader situation, knowledge, interest, want, resistance, or audience research finding | The resolved `AUDIENCE.md`, including a named shared source; retain source, date, and scope |
| Repeated editorial failure | Relevant guardrail or review reference |
| Reusable workflow improvement | Workflow or architecture file |
| Piece-specific decision or open loop | The active draft, notes, or project status artifact |

Never save durable learning into an installed plugin/cache copy. Do not append lessons to a skill's `SKILL.md` merely because the skill was active.

If a legacy `TASTE.md` is still present, route new learning to `VOICE.md`, `STYLE.md`, or the governing `AUDIENCE.md` and offer migration. Do not delete or archive `TASTE.md` without explicit approval.

When one correction mixes sentence craft and substantive standards, split it into two atomic rules. Do not duplicate the combined rule across both files.

## Decide Whether It Should Generalize

Distinguish:

- an explicit enduring preference;
- a repeated pattern supported by several examples;
- a one-off choice for this piece;
- an inference that still needs confirmation.

If the user explicitly says to save an enduring preference, proceed once the destination is clear and permitted. If the lesson is inferred, show the proposed rule and ask the user to confirm before making it durable.

For audience learning, a piece-specific assumption stays with the assignment. Do not promote positioning or an editorial inference to observed reader behavior. A shared audience guide may affect multiple publications; preserve its scope and update it only within the user's authorization. Follow the existing shared source rather than creating a competing local copy.

## Write Precisely

1. Read the destination file before editing.
2. Add or revise the narrowest relevant rule.
3. Preserve existing user-authored context, examples, and avoid duplicate guidance.
4. Record the mechanism or consequence, not only a vague preference.
5. For a voice lesson, record the date, the piece, the line that went wrong (or a description of it), and the fix. Never write a general description of the voice into `VOICE.md`.

## Confirm

Report the exact rule captured and the file or system updated. If a higher-authority destination requires approval, provide the proposed wording and wait instead of pretending it was saved.
