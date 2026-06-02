---
name: migrate-workspace
description: Propose a reviewed migration from legacy TASTE.md into voice, style, strategy, and context files.
user_invocable: true
---

# Migrate Workspace

## Purpose

Support existing users without losing preferences or silently reclassifying
their material.

Use `../../docs/ONBOARDING.md` for the relationship between migration and
first-run setup.

## Workflow

1. Read the project's `TASTE.md` and any nearby context or workstream guide.
2. Classify candidate material:

| Scope | Proposed destination |
| --- | --- |
| Stable cross-format diction, syntax, rhythm, and humor | `voice.md` |
| Destination or workstream structure and reader rules | `style-guides/*.md` |
| Public territory, audience, platform job, or measurement rule | `strategy/*.md` |
| Current piece fact, provisional note, or single observation | `context.md` |

3. Present a migration table with excerpts summarized, destinations, and any
   ambiguous items.
4. Continue reading legacy `TASTE.md` as fallback unless and until the user
   approves new files.
5. Write approved files and leave the original untouched unless deletion or
   archival is explicitly requested.

## After Migration

Summarize which new files were created, what remains only in legacy form, and
which destination or writing task the user wants to continue with.
