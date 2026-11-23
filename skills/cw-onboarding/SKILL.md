---
name: cw-onboarding
description: Begin or refresh a writer's gold examples, STYLE.md, and optional AUDIENCE.md in their durable writing home from existing writing, a short conversation, or maintained context. Use during first-run writing-home setup and when the user wants to define, calibrate, import, or update voice, style, or audience context.
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

## Keep The Destinations Distinct

Route each rule by what it governs:

- `examples/` answers **How do the sentences sound?** It holds the writer's gold pieces. Every voice-sensitive skill reads the voice from them; nobody writes a description of it.
- `VOICE.md` answers **What has the writer corrected that the examples did not teach?** It starts nearly empty and collects dated lessons on syntax, diction, and tone.
- `STYLE.md` answers **What must the article do, contain, and prove?** Put argument, evidence, article structure, substantive standards, audience promise, openings, endings, formats, and publication-readiness criteria here.

- Optional `AUDIENCE.md` answers **Who are we writing for, and what may engage them?** Put reader situations, prior knowledge, wants, interests, resistance, and source evidence here. Follow a maintained shared source named by the project; do not create a local duplicate.

Use this classification test:

- A rule that changes wording, sentence construction, or tone is either shown by a gold example or recorded as a lesson in `VOICE.md`.
- A rule that changes the claim, support, organization, or readiness standard of the article belongs in `STYLE.md`.
- Reader knowledge belongs in the governing `AUDIENCE.md`; the writing's obligations to that reader remain in `STYLE.md`. Split mixed feedback without duplicating it across guides.

Use the writing home's `examples/`, `VOICE.md`, and `STYLE.md` as its portable context. Use an existing global voice guide when it is already the maintained authority. Tell the user where each class of guidance will live when the destination is not already obvious.

## Begin Or Refresh Audience Context

When the user requests audience setup or calibration, resolve the audience source through the context contract. Use an existing shared guide when named; otherwise create `AUDIENCE.md` in the established writing home if useful. The optional starter is `defaults/project-template/AUDIENCE.md` relative to the plugin root. Missing audience context never blocks the immediate writing task or triggers onboarding by itself.

Start with known situations, knowledge, interests, and resistance. Ask only consequential gaps. Label reader evidence, positioning, explicit writer intent, and editorial hypotheses; keep source, date, and scope. Do not invent a demographic profile, assume personal stakes, or turn a publication's intended relationship into measured reader behavior. The assignment can select a narrower reader without changing the shared guide.

Make the guide legible to both the writer and the agent: begin with a short reader portrait, distinguish wants (outcomes or experiences sought) from needs (what may help the reader get there), and connect them to what the writing can offer. Include a possible hero's journey when useful: starting situation, call, obstacles, guidance, trials, and what the reader carries back. Label it as an editorial model unless supported by reader evidence; do not force a transformation story or invent motives to fill its stages. Close with concise instructions for applying the guide to a piece, with sources and uncertainties easy to find.

## Interview

Ask only what the existing context does not answer. During first-run setup, ask one to three conversational questions at a time or invite the writer to share representative samples. Useful dimensions include:

- for voice: which of their pieces sound most like them (ask for the pieces, not a description), and any sentence-level preferences they state outright;
- the writer's argument standards and recurring substantive moves;
- evidence requirements, article structures, openings, endings, and publication-readiness criteria;
- what the writer makes, for whom, and with what reader promise;
- verbal tics, structural anti-patterns, and AI tells to avoid;
- workflow preferences that materially affect the project.

Ask conversationally and follow the user's energy. Six fixed questions are not a requirement.

For a quick first version, capture a few high-signal rules in each guide and leave unknowns open. If the writer arrived with an immediate task, calibrate from that work where possible instead of pausing for a separate interview.

## Collect The Gold Examples

Voice setup in this edition is choosing examples, not writing a profile.

- Ask the writer for three to ten pieces that sound most like them, in the formats they write most. Five is a good start. Their own drafts or lightly edited published pieces are best; a piece an editor rewrote heavily teaches the editor's voice.
- Save each as a Markdown or plain-text file in `examples/`, one piece per file, with a clear name. Pieces that sound wrong go in `examples/negative/`.
- Run `../cw-voice-check/scripts/voice_stats.py` on the set and read the examples once by following `../../references/voice-from-examples.md`. Show the writer a short sample of the voice read, five or six patterns with quoted evidence, and ask whether anything there is wrong or missing.
- If the writer says a pattern is wrong ("I only do that in newsletters"), the fix is usually the example set: split it by format or swap a piece. Record a lesson in `VOICE.md` only when the examples cannot show it.
- Do not save the voice read as a guide. It is rebuilt from the examples each time, so it stays current when the examples change.
- If the writer states sentence-level preferences directly during setup ("never 'utilize'", "I hate semicolons"), record each as a dated lesson in `VOICE.md`.

When a writer already has a descriptive `VOICE.md`, leave it in place. Offer to move its descriptive sections into a separate archived file so the examples can carry the voice, and keep any concrete, confirmed corrections as lessons. Do not make that change without approval.

## Write The Guides

- Capture only specific, evidenced preferences.
- Keep `VOICE.md` to lessons. Keep argument, evidence, article structure, substantive standards, and publication readiness in `STYLE.md`.
- Phrase guidance as actionable rules, not personality adjectives alone.
- Show the proposed content before changing a high-authority or shared file when the governing rules require approval.

## Migrate TASTE.md

When a legacy `TASTE.md` exists, classify its rules into `VOICE.md` lessons, `STYLE.md`, and an authorized audience guide when useful. Flag mixed or conflicting rules for judgment. Do not keep adding new guidance to `TASTE.md`, and do not delete it without explicit approval.

## Handoff

Confirm:

- which gold examples were saved, what the sample voice read showed, and any lessons recorded;
- what was captured in style and audience context when requested;
- where the guides and supporting examples were saved, including any shared audience source;
- which gaps remain intentionally open;
- how future Compound Writing skills will load the writing home.
