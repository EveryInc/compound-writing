# Onboarding Contract

This document defines the first-run experience for users and the behavior the
`onboarding` and `scribe` skills must implement.

## Goal

Get a new user to a usable, accurate first workspace quickly:

- A sparse `voice.md` they have reviewed and approved.
- At most one immediately useful destination guide unless they ask for more.
- Optional strategy files only when their goal actually includes public
  positioning or cross-platform publishing.

## Entry Detection

Before onboarding, inspect the current writing-project folder.

| Files found | Behavior |
| --- | --- |
| No `voice.md`, no `TASTE.md` | Offer new-user onboarding. |
| `voice.md` exists | Use it; offer to inspect or update it only when requested. |
| `TASTE.md` exists but `voice.md` does not | Explain legacy fallback and offer `/migrate-workspace`. |
| Both exist | Use `voice.md`; offer legacy cleanup or comparison only when requested. |

## New-User Conversation

Ask one question at a time, with follow-ups only when an answer is too vague
to create useful guidance.

### Stage One: Immediate Use

Ask:

1. What are you trying to write right now?
2. Where will it appear, if you already know?
3. Who needs to understand or care about it?

This establishes destination and audience without converting those facts into
cross-format voice rules.

### Stage Two: Cross-Format Voice

Ask:

1. How should your writing feel to a reader?
2. What should it never sound like?
3. Do you tend toward concise sentences, accumulating sentences, or a mix?
4. What kinds of detail, register, or explanation feel natural to you?
5. What kind of humor, if any, fits your work?
6. Are there words, rhetorical habits, or assistant tics you want removed?

Optional: invite a short sample the user considers representative. Use it as
evidence for proposed guidance, not as permission to copy lines.

Do not ask for named writers to imitate. If a user volunteers a reference,
translate it into qualities they approve, such as plainness, compression, or
dry understatement.

### Stage Three: Preview `voice.md`

Generate only supported guidance from the user's answers. Leave unknown
sections sparse.

Show:

- The exact proposed contents of `voice.md`.
- A short note identifying any inference that needs confirmation.
- The question: "Should I create this `voice.md`, revise it, or leave it
  unsaved for now?"

Write `voice.md` only after approval.

### Stage Four: Destination Guide

If the user's immediate destination is known, offer one guide:

| Destination | File |
| --- | --- |
| Essay, newsletter, article, or longform draft | `style-guides/longform.md` |
| X post or thread | `style-guides/x.md` |
| LinkedIn post or article | `style-guides/linkedin.md` |

Ask up to three relevant questions about audience, preferred structure, and
what proof or action belongs in that destination. Preview the populated guide
and request approval before writing.

If no destination is known, skip this step and proceed to writing discovery.

### Stage Five: Optional Strategy

Only offer strategy setup when the user wants to build a public practice,
choose between platforms, adapt one work unit across destinations, or assess
what they should become known for.

Explain the two optional files:

- `strategy/professional-positioning.md`
- `strategy/platform-strategy.md`

Do not create them by default during voice setup.

### Stage Six: Transition Into Work

Summarize files created and give the user a direct next action based on their
initial purpose:

- Draft or develop a specific piece.
- Create the relevant destination guide if deferred.
- Begin optional strategy setup if requested.
- Review an existing draft against the new files.

## Existing User Migration

If legacy `TASTE.md` is present, do not silently trigger new-user setup.
Offer:

1. Continue using the legacy profile for now.
2. Preview a guided migration with `/migrate-workspace`.
3. Start a new `voice.md` without modifying the legacy file.

Migration writes only approved files and does not remove legacy material.

## Acceptance Criteria

- The user knows what files will be created and where.
- The first durable file is previewed before writing.
- Strategy is not mistaken for voice.
- Only relevant destination guidance is created.
- The user can begin a real writing task immediately after setup.

