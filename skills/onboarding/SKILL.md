---
name: onboarding
description: Build or refresh a writing project's separate VOICE.md and STYLE.md guides from a short conversation, existing writing, or maintained context. Use when the user wants to define, calibrate, import, or update voice and style rules; use setup-project first when the project folder does not exist yet.
---

# Onboarding

Create the smallest durable voice and style guides that will make future work meaningfully better.

## Load Existing Context First

Read `../../references/context-contract.md`. Inspect the current workspace for maintained identity, voice, preference, and project-style files before asking questions.

- If authoritative context already exists, summarize it and ask only about genuine gaps.
- If the user needs a new project folder, run `setup-project` first so `VOICE.md`, `STYLE.md`, `examples/`, and `drafts/` exist together.
- Do not auto-trigger because either guide is sparse or because a legacy `TASTE.md` is absent.
- Do not duplicate global guidance into a project file unless the project needs an explicit local override.
- Do not overwrite an existing profile without explicit approval.

## Keep Two Destinations

Route each rule by what it governs:

- `VOICE.md` answers **How should the sentences sound?** Put syntax, diction, and tone here, including cadence, rhythm, register, punctuation, verbal tics, sentence moves, and phrases to favor or avoid.
- `STYLE.md` answers **What must the article do, contain, and prove?** Put argument, evidence, article structure, substantive standards, audience promise, openings, endings, formats, and publication-readiness criteria here.

Use this classification test:

- A rule that changes wording, sentence construction, or tone belongs in `VOICE.md`.
- A rule that changes the claim, support, organization, or readiness standard of the article belongs in `STYLE.md`.
- Feedback that changes both must become two atomic rules. Do not copy the combined instruction into both files.

Use project-local `VOICE.md` and `STYLE.md` for a self-contained project. Use an existing global voice guide only for truly cross-project rules. Tell the user where each class of guidance will live when the destination is not already obvious.

## Interview

Ask only what the existing context does not answer. Useful dimensions include:

- syntax, diction, tone, sentence architecture, rhythm, and recurring line-level moves;
- the project's argument standards and recurring substantive moves;
- evidence requirements, article structures, openings, endings, and publication-readiness criteria;
- what the project makes, for whom, and with what reader promise;
- verbal tics, structural anti-patterns, and AI tells to avoid;
- workflow preferences that materially affect the project.

Ask conversationally and follow the user's energy. Six fixed questions are not a requirement.

## Write The Profile

- Capture only specific, evidenced preferences.
- Keep syntax, diction, and tone in `VOICE.md`; keep argument, evidence, article structure, substantive standards, and publication readiness in `STYLE.md`.
- Phrase guidance as actionable rules, not personality adjectives alone.
- Put full exemplars in `examples/`; use short excerpts in the guides only when they clarify a rule.
- Mark published examples as directional and non-reusable.
- Show the proposed content before changing a high-authority or shared file when the governing rules require approval.

## Migrate TASTE.md

When a legacy `TASTE.md` exists, classify its rules into `VOICE.md` and `STYLE.md`. Flag mixed or conflicting rules for judgment. Do not keep adding new guidance to `TASTE.md`, and do not delete it without explicit approval.

## Handoff

Confirm:

- what was captured in voice versus style;
- where both files and any supporting examples were saved;
- which gaps remain intentionally open;
- how future Compound Writing skills will load it.
