---
name: cw-onboarding
description: Begin or refresh the separate VOICE.md and STYLE.md guides in a writer's durable writing home from a short conversation, existing writing, or maintained context. Use during first-run writing-home setup and when the user wants to define, calibrate, import, or update voice and style rules.
---

# Onboarding

Create the smallest useful first version of the writer's durable voice and style guides. Help them start; do not make them finish an exhaustive profile before they can write.

## Load Existing Context First

Read `../../references/context-contract.md`. Inspect the current workspace for maintained identity, voice, preference, and project-style files before asking questions.

- If authoritative context already exists, summarize it and ask only about genuine gaps.
- If the user needs a writing-home folder, resolve the target and run `cw-setup-project` first so `VOICE.md`, `STYLE.md`, `examples/`, and `drafts/` exist together.
- Do not auto-trigger because either guide is sparse or because a legacy `TASTE.md` is absent.
- Do not duplicate global guidance into the writing home unless a local override is needed.
- Do not overwrite an existing profile without explicit approval.

## Keep Two Destinations

Route each rule by what it governs:

- `VOICE.md` answers **How should the sentences sound?** Put syntax, diction, and tone here, including cadence, rhythm, register, punctuation, verbal tics, sentence moves, and phrases to favor or avoid.
- `STYLE.md` answers **What must the article do, contain, and prove?** Put argument, evidence, article structure, substantive standards, audience promise, openings, endings, formats, and publication-readiness criteria here.

Use this classification test:

- A rule that changes wording, sentence construction, or tone belongs in `VOICE.md`.
- A rule that changes the claim, support, organization, or readiness standard of the article belongs in `STYLE.md`.
- Feedback that changes both must become two atomic rules. Do not copy the combined instruction into both files.

Use the writing home's `VOICE.md` and `STYLE.md` as its portable context. Use an existing global voice guide when it is already the maintained authority. Tell the user where each class of guidance will live when the destination is not already obvious.

## Interview

Ask only what the existing context does not answer. During first-run setup, ask one to three conversational questions at a time or invite the writer to share representative samples. Useful dimensions include:

- syntax, diction, tone, sentence architecture, rhythm, and recurring line-level moves;
- the writer's argument standards and recurring substantive moves;
- evidence requirements, article structures, openings, endings, and publication-readiness criteria;
- what the writer makes, for whom, and with what reader promise;
- verbal tics, structural anti-patterns, and AI tells to avoid;
- workflow preferences that materially affect the project.

Ask conversationally and follow the user's energy. Six fixed questions are not a requirement.

For a quick first version, capture a few high-signal rules in each guide and leave unknowns open. If the writer arrived with an immediate task, calibrate from that work where possible instead of pausing for a separate interview.

## Calibrating A Voice Profile From Examples

When the writer supplies a fresh sample set or asks to refresh `VOICE.md`, make the deliverable a **sentence-level vocal score**, not a writing philosophy.

First, compare the examples for repeatable line-level behavior. Capture only patterns that recur across the sample set or that the writer explicitly confirms. Separate patterns that belong to a particular publication, assignment, or subject from portable voice guidance.

The resulting `VOICE.md` should normally cover:

- the overall sentence-level sound in a few concrete sentences;
- cadence and sentence-length variation;
- syntax and recurring sentence turns, such as accumulation, qualification, correction, release, or fragments;
- diction and register, including words, constructions, and generic phrasing to avoid;
- punctuation, emphasis, and paragraph-level texture only when they affect sentence sound;
- humor, self-awareness, or verbal tics when they are evidenced in the samples;
- practical revision instructions that help an agent align a draft without imitating the examples.

Do **not** put curiosity, intellectual rigor, uncertainty, point of view, reader relationship, argument, evidence, structure, or publication standards in this profile unless the instruction changes the wording, syntax, cadence, or tone of a sentence. Route those concerns to the active project's `STYLE.md`, brief, or source material.

For every material voice rule, attach either a short sourced excerpt or a concise description of the observed move. Full examples belong in `examples/`; published language is directional and non-reusable. Avoid broad labels such as “warm,” “smart,” or “authentic” unless they are translated into observable writing behavior.

## Write The Profile

- Capture only specific, evidenced preferences.
- Keep syntax, diction, and tone in `VOICE.md`; keep argument, evidence, article structure, substantive standards, and publication readiness in `STYLE.md`.
- Phrase guidance as actionable rules, not personality adjectives alone.
- Put full exemplars in `examples/`; use short excerpts in the guides only when they clarify a rule.
- Mark published examples as directional and non-reusable.
- When writing from examples, make rules operational: tell the agent how a sentence gathers, turns, qualifies, lands, or sounds false.
- Include a concise revision checklist for preserving the writer's sentence-level sound without copying their phrases or inventing personal detail.
- Show the proposed content before changing a high-authority or shared file when the governing rules require approval.

## Migrate TASTE.md

When a legacy `TASTE.md` exists, classify its rules into `VOICE.md` and `STYLE.md`. Flag mixed or conflicting rules for judgment. Do not keep adding new guidance to `TASTE.md`, and do not delete it without explicit approval.

## Handoff

Confirm:

- what was captured in voice versus style;
- where both files and any supporting examples were saved;
- which gaps remain intentionally open;
- how future Compound Writing skills will load the writing home.
