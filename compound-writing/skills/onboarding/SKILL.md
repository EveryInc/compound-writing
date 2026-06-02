---
name: onboarding
description: Create a sparse user-owned voice guide and optional destination or strategy guides through conversation.
user_invocable: true
---

# Onboarding

## Purpose

Help a writer get a useful first `voice.md` without forcing a full identity or
publishing strategy setup before they write.

Use `../../docs/ONBOARDING.md` as the complete first-run contract.

## Before Starting

Inspect the current user project:

| Found | Action |
| --- | --- |
| Neither `voice.md` nor `TASTE.md` | Begin new-user onboarding. |
| `voice.md` | Ask whether they want to view or update it; do not overwrite it as first-run setup. |
| Only `TASTE.md` | Offer legacy fallback or `/migrate-workspace`; do not silently convert it. |
| Both files | Use `voice.md`; discuss the legacy file only if requested. |

## Files

Create user files in the current project directory, never in the plugin:

- `voice.md` during first-time voice setup.
- `style-guides/{destination}.md` when a user wants to write for a
  destination.
- `strategy/*.md` only when positioning or platform strategy is requested.
- `context.md` when there is provisional work or observed learning to record.

Copy structure from `defaults/workspace/`, then populate only what the user
actually states.

## New-User Conversation

Ask one question at a time. Establish:

1. What they are trying to write now, where it will appear if known, and who
   needs to understand it.
2. How the writing should feel and what it should never sound like.
3. Preferred sentence rhythm, register, specificity, translation of technical
   material, and humor across formats.
4. Words, phrases, or generic assistant habits they want removed.

If the user offers a writer as a reference point, translate that reference
into approved characteristics. Do not store an instruction to imitate a real
person.

## Preview And Approval

Generate a sparse `voice.md` only from stated or confirmed preferences.
Preview its exact contents and ask whether to create it, revise it, or leave
it unsaved. Write only after approval.

## Destination Overlay

After `voice.md` is approved, offer only the guide needed for the immediate
destination:

| Destination | Guide |
| --- | --- |
| Essay, newsletter, article, or longform piece | `style-guides/longform.md` |
| X post or thread | `style-guides/x.md` |
| LinkedIn post or article | `style-guides/linkedin.md` |

Ask briefly about destination reader, shape, and evidence. Preview and get
approval before creating the guide.

## Strategy Is Optional

Offer `strategy/professional-positioning.md` and
`strategy/platform-strategy.md` only when the user asks to develop a public
presence, make platform decisions, or repurpose work across destinations.
Never treat strategy setup as required voice onboarding.

## Finish

Report the files created, note any intentionally deferred files, and route
directly into the user's initial writing task.
