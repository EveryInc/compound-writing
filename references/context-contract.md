# Context Contract

Use this contract whenever a Compound Writing skill needs voice, audience, project, assignment, source, or destination context.

## Load Order

Load only the layers that exist and matter to the task, in this order:

1. Explicit user instructions and supplied material.
2. Repository or workspace instructions such as `AGENTS.md`, `CLAUDE.md`, `CODEX.md`, or `GEMINI.md`, plus applicable rules supplied by the active host. Respect each rule's scope and activation conditions.
3. Global identity, preference, rule, and voice files named by those instructions.
4. The active writing home's or project's `AGENTS.md`, `VOICE.md` (confirmed voice lessons), `STYLE.md`, optional `AUDIENCE.md` (including a shared audience guide named by its instructions), brief, template, workflow, or checklist.
5. The gold examples in the active writing home's or project's `examples/` folder. They are the source of sentence- and word-level voice: read them by following `voice-from-examples.md` in this folder.
6. Assignment-specific notes, sources, research, outline, draft, feedback, and destination requirements.
7. A legacy `TASTE.md`, only when the project still maintains it.
8. Plugin defaults, only as a fallback for gaps not resolved above.

Higher-authority context wins when two layers conflict. Do not merge incompatible rules into a vague compromise.

## Routing

- Infer the active project from the working directory, named file, or user request.
- Respect the project's existing artifact locations and naming conventions.
- If the user supplies a draft, selection, link, or file, work from that artifact directly.
- At the first meaningful Scribe interaction, inspect the request, supplied material, current workspace, and maintained context before deciding whether setup is useful.
- Treat an active writing workspace, maintained writing context, or useful live artifact as an established starting point even when `VOICE.md`, `STYLE.md`, `examples/`, or `drafts/` is absent.
- If a draft, notes, sources, or useful workspace context exists, do the immediate writing work. Do not block on setup or onboarding; offer calibration only when it would materially improve future work.
- If no established writing context or useful artifact exists, briefly explain the benefit of one durable writing home, resolve its target folder, then route to `cw-setup-project` and `cw-onboarding`.
- Never create the writing-home scaffold until its destination is explicit or safely resolved. Do not use plugin-owned persistent state to record onboarding.
- Keep one writing home as the normal first-run model. Route an explicit later request for another self-contained writing folder to `cw-setup-project` without presenting multiple homes as a required system.
- Do not infer that an existing project needs setup merely because `VOICE.md`, `STYLE.md`, `examples/`, or `drafts/` is absent.
- Do not run onboarding merely because a guide is sparse or a legacy `TASTE.md` is absent.
- Ask only when a missing choice would materially change the work and cannot be inferred safely.

## Voice, Style, And Audience Boundary

Keep the files conceptually separate:

| File | Governing question | Belongs here | Does not belong here |
|---|---|---|---|
| `examples/` | How do the writer's sentences actually sound? | Gold pieces by the writer, the source the voice is read from; optional counterexamples in `examples/negative/` | Pieces the writer does not consider representative, or heavily edited by someone else |
| `VOICE.md` | What has the writer corrected that the examples did not teach? | Dated, confirmed lessons on syntax, diction, and tone, including cadence, register, punctuation, and verbal tics | A general description of the voice, adjectives, patterns already visible in the examples, or argument, evidence, structure, and readiness criteria |
| `STYLE.md` | What must the article do, contain, and prove? | Argument, evidence, article structure, substantive standards, audience promise, and publication-readiness criteria | Word choice, sentence construction, cadence, or tone |
| `AUDIENCE.md` | Who are we writing for, and what may engage them? | Reader situations, knowledge, wants, interests, resistance, and evidence or hypotheses about the audience | Sentence sound, article requirements, or a predetermined angle for every piece |

Classify a rule by what it changes:

- If it changes wording, sentence construction, or tone, put it in `VOICE.md` as a confirmed lesson, or add a gold example that shows it.
- If it changes the claim, support, organization, or readiness standard of the article, put it in `STYLE.md`.
- If it describes the reader's situation, knowledge, interests, wants, or resistance, put it in the governing `AUDIENCE.md` when that durable audience context is useful and authorized.
- Split feedback that spans these concerns into separate observations or rules; do not duplicate the combined instruction across guides.

This edition does not keep a written description of the voice. The voice is read from the gold examples each time voice-sensitive work starts, following `voice-from-examples.md`. `VOICE.md` holds only lessons on diction and syntax that the writer confirmed after the examples alone did not get a draft right. Lessons override the examples where they conflict.

Project argument, rigor, evidence, structure, and obligations to readers belong in `STYLE.md` or the assignment brief. Knowledge about readers' curiosity, situations, or interests belongs in `AUDIENCE.md` when one is maintained. Sentence-level expression remains in `VOICE.md`.

Examples:

- `VOICE.md`: "2026-11-03, newsletter draft: the writer twice replaced *unlock* with a plain verb. Do not use it."
- `STYLE.md`: state the thesis early; source every consequential claim; earn the ending; do not call a piece publication-ready while the central counterargument is unanswered.
- `AUDIENCE.md`: readers have used the tool but may not know its evaluation vocabulary; label the source and scope of that observation.

## Resolve Audience Context

- Start with the explicit audience in the current request or assignment. It takes precedence over shared audience defaults.
- Follow the audience source named by the active project's instructions. A named shared guide is authoritative for that shared audience; do not create a competing local profile merely because it lives elsewhere.
- Otherwise use a maintained local `AUDIENCE.md` if present. Existing audience notes in `STYLE.md` or a brief remain usable when no separate audience guide exists. Do not migrate them without authorization.
- If a shared guide has a local pointer file, read the referenced source. Resolve relative paths from the file containing the link. If the source is missing or pointers form a loop, stop following the links, state the gap, and proceed with available assignment context; ask only if it changes the work materially.
- A narrower assignment may focus on a particular reader situation without rewriting the shared guide. Surface unresolved audience conflicts rather than averaging incompatible assumptions.
- `AUDIENCE.md` is optional. Its absence or sparseness never triggers setup, blocks writing, or requires a connector, audience study, or detailed persona.
- Distinguish audience evidence, positioning, writer intent, and editorial inference. Preserve source, date, and scope; audience assumptions do not become facts about all readers.
- Use the guide to refine or challenge an angle, hook, promise, explanation, or reader review. Start from the piece's material; do not preassign it a motive or fill it with brand language.
- In a cold-reader review, audience context establishes plausible prior knowledge only. Do not use private writer notes or source material to repair gaps on the page.

## Applying The Context

- Treat the gold examples, read through `voice-from-examples.md`, as the authority for syntax, diction, and tone. Treat `VOICE.md` lessons as confirmed corrections that win where they conflict with a pattern in the examples.
- Treat `STYLE.md` as the authority for argument, evidence, article structure, substantive standards, and publication readiness.
- Use the resolved `AUDIENCE.md` for reader context, with assignment-specific audience instructions taking precedence.
- Learn sentence patterns from the gold examples and match them at the rate they occur. Copy patterns, not sentences.
- Back every voice pattern you act on with quoted instances from at least two examples; one instance is a note, not a pattern.
- Where a generic craft rule in a skill conflicts with what the gold examples consistently do, follow the examples.
- Treat a legacy personal preference file as lower-authority context unless the project explicitly says otherwise.
- Preserve distinctive syntax, humor, priors, and useful weirdness while tightening.
- Do not paste sentences from a gold example into new prose as if they were new. The writer's own words in the current material (notes, interview answers, comments, their own draft) are different: use them, verbatim or close, when they work.

## Sources And Claims

- Keep factual claims attached to their source links or named provenance.
- Separate confirmed source material, reasonable inference, and model-added assumptions.
- Flag unsupported claims instead of smoothing them into certainty.
- Surface evidence that complicates the thesis; do not rebuild the thesis without the writer's ownership.

## Destinations And Writes

- Default to the active project's local source-of-truth format and location.
- Use a named destination when the user requests one.
- In a project initialized by `cw-setup-project`, create or reuse `drafts/<piece-slug>/`. Store draft versions, notes, research, review output, and related support material for that piece there.
- In other projects, create or reuse a dedicated piece folder where the project's existing convention requires it. Do not impose `drafts/` retroactively.
- Follow the governing workspace's approval rules before editing shared files, connected apps, public surfaces, or high-authority context.
- Read before writing and preserve user-authored changes.
- Never write durable preferences into an installed plugin or cache directory.

## Handoff

For substantial work, report:

- What changed or was produced.
- What remains uncertain or needs the writer's judgment.
- What should become durable context, a checklist item, or a reusable workflow.
