---
name: scribe
description: Route writing requests through the user's voice, destination guidance, and appropriate workflow stage.
user_invocable: true
---

# Scribe

## Purpose

Act as the main entry point for Compound Writing.

For first-run behavior, follow `../../docs/ONBOARDING.md`.

## Context Loading

1. Load `defaults/SYSTEM.md`.
2. Detect `voice.md` and legacy `TASTE.md`:
   - Neither exists: tell the user a brief setup will improve this work and
     offer `/onboarding`.
   - Only legacy `TASTE.md` exists: offer to use it for now or preview
     `/migrate-workspace`.
   - `voice.md` exists: load it.
3. Continue without personal voice guidance only if the user chooses to skip
   setup for the current request.
4. Identify the destination and load its style guide when present.
5. Load strategy files only if the task concerns public positioning,
   adaptation across destinations, or performance review.
6. Load `context.md` and piece-specific files when relevant.

## Routing

| User intent | Route |
| --- | --- |
| Essay, article, newsletter, or longer draft | `longform` plus the relevant workflow stage. |
| X post or thread | `x-post`. |
| LinkedIn post | `linkedin-post`. |
| General critique | Select or propose functional reviewer lenses. |
| Voice or preference learning | `voice-check` or `save`. |

If a legacy `TASTE.md` exists and `voice.md` does not, offer
`migrate-workspace` rather than silently reorganizing it.

If a destination is clear but its style guide does not exist, proceed with
generic destination behavior or offer to create the guide; do not stall an
urgent writing request.
