# Context Contract

Use this contract whenever a Compound Writing skill needs voice, project, assignment, source, or destination context.

## Load Order

Load only the layers that exist and matter to the task, in this order:

1. Explicit user instructions and supplied material.
2. Repository or workspace instructions such as `AGENTS.md`, `CLAUDE.md`, or `CODEX.md`.
3. Global identity, preference, rule, and voice files named by those instructions.
4. The active writing home's or project's `AGENTS.md`, `VOICE.md`, `STYLE.md`, brief, template, workflow, or checklist.
5. Relevant curated examples from the active writing home's or project's `examples/` folder.
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

## Voice And Style Boundary

Keep the two files conceptually separate:

| File | Governing question | Belongs here | Does not belong here |
|---|---|---|---|
| `VOICE.md` | How should the sentences sound? | Syntax, diction, and tone, including cadence, rhythm, register, punctuation, and verbal tics | Argument, evidence standards, article structure, substantive requirements, or publication-readiness criteria |
| `STYLE.md` | What must the article do, contain, and prove? | Argument, evidence, article structure, substantive standards, audience promise, and publication-readiness criteria | Word choice, sentence construction, cadence, or tone |

Classify a rule by what it changes:

- If it changes wording, sentence construction, or tone, put it in `VOICE.md`.
- If it changes the claim, support, organization, or readiness standard of the article, put it in `STYLE.md`.
- If feedback contains both, split it into two atomic rules rather than storing the combined instruction in both files.

When creating or refreshing `VOICE.md` from examples, treat it as a **sentence-level vocal score**. It should describe observable cadence, syntax, diction, register, punctuation, humor, verbal tics, and revision moves. It should not become a personal philosophy, project strategy, or editorial brief.

Project-specific curiosity, rigor, uncertainty, reader relationship, argument, evidence, and structure belong in `STYLE.md`, an assignment brief, or source material unless they directly change how a sentence sounds.

Examples:

- `VOICE.md`: favor plain verbs; use long accumulating sentences sparingly; avoid a scolding tone.
- `STYLE.md`: state the thesis early; source every consequential claim; earn the ending; do not call a piece publication-ready while the central counterargument is unanswered.

## Applying The Context

- Treat `VOICE.md` as the authority for syntax, diction, and tone.
- Treat `STYLE.md` as the authority for argument, evidence, article structure, substantive standards, and publication readiness.
- Use curated examples to interpret written rules, not as language to imitate.
- For sample-based voice calibration, record only evidenced, reusable sentence-level patterns; keep a short source cue or observed move with each material rule.
- Treat a phrase that could be copied from the writer as evidence, not a reusable phrase bank.
- Treat a legacy personal preference file as lower-authority context unless the project explicitly says otherwise.
- Preserve distinctive syntax, humor, priors, and useful weirdness while tightening.
- Do not copy illustrative voice-guide examples verbatim.

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
