# Compound Writing Public Core Instructions

This proposed package is public-safe by default.

## Workspace Loading

For writing work, load in this order when the files exist:

1. `defaults/SYSTEM.md`
2. User project `voice.md`
3. The relevant user project `style-guides/{destination}.md`
4. Relevant strategy files only for selection, positioning, adaptation, or
   performance review
5. User project `context.md` and piece source material
6. The user's immediate instruction

## First Run

- If neither `voice.md` nor legacy `TASTE.md` exists in the user's project,
  offer onboarding before voice-dependent drafting or review.
- If `voice.md` exists, do not rerun setup by default; use it and offer an
  update only if requested.
- If only legacy `TASTE.md` exists, explain that it still works as fallback
  and offer a reviewed migration.
- Onboarding writes a durable file only after previewing the proposed content
  and receiving approval.

## Improvement Rules

- Record provisional observations in `context.md`.
- Propose durable changes with destination and evidence named.
- Write to `voice.md`, `style-guides/`, or `strategy/` only after approval.
- Do not preserve personal facts, anecdotes, or metrics as generalized
  guidance without the user's explicit decision.

## Product Boundaries

- Public core uses functional reviewer names.
- Public core examples must be synthetic or cleared for external use.
- Subscriber-edition material may layer on core; core must not require it.
