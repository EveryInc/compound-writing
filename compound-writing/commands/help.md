---
name: help
description: Overview of the proposed public Compound Writing workflow.
---

# Compound Writing

Compound Writing helps you define how you sound, decide how a piece should
behave in its destination, and improve the system from your approved choices.

## Start

### New User

Run `/onboarding`. You will answer a short set of questions about how your
writing should sound. The system previews a sparse `voice.md`, writes it only
after you approve it, and then helps you create the one destination guide you
need now.

### Ready To Write

Use `/scribe` with an idea, draft, or destination. If setup is missing, it
will offer onboarding before applying personal voice guidance.

### Existing `TASTE.md` User

Run `/migrate-workspace`. The system shows how your existing guidance could
split into voice, destination style, strategy, and context files. Nothing is
moved or rewritten without approval.

## Your Workspace

| File | Purpose |
| --- | --- |
| `voice.md` | Cross-format diction, syntax, rhythm, and stable preferences. |
| `style-guides/*.md` | Rules for longform, X, LinkedIn, or your own destinations. |
| `strategy/*.md` | Positioning and platform roles when public strategy is relevant. |
| `context.md` | Working observations and candidates for later promotion. |

Start minimally: a `voice.md` plus the guide for the destination you are
working in is enough. Strategy files are optional.

## How It Learns

The system may observe a repeated choice and suggest where it belongs. It
does not update durable voice or strategy guidance without your approval.

Use `/commands` for the full capability list. See `docs/GETTING-STARTED.md`
for the full setup path.
