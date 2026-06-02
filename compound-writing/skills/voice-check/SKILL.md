---
name: voice-check
description: Review a passage against voice.md and any relevant destination-specific style guide.
user_invocable: true
---

# Voice Check

## Purpose

Identify whether a passage sounds like the user while respecting the intended
destination.

## Load

1. `defaults/SYSTEM.md`
2. User `voice.md`
3. Relevant `style-guides/{destination}.md`, if the destination is known

Do not load strategy unless the question is about public positioning rather
than line-level voice.

## Output

Report:

- The relevant voice and destination criteria.
- What aligns.
- What drifts and why.
- A suggested revision, if useful.
- Any possible preference observed during the exchange, clearly marked as
  provisional until the user chooses to save it.

