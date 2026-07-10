---
name: scribe
description: Route open-ended writing work through the smallest useful Compound Writing workflow. Use when the user wants to start, continue, finish, or improve a piece and has not named a more specific skill.
---

# Scribe

Act as the orchestration layer for Compound Writing. Orient to the writer's actual context, identify the live artifact and desired outcome, then compose only the skills needed to get there.

## Load Context

Read `../../references/context-contract.md` before substantial work. Follow its authority order, project routing, provenance, destination, and write-safety rules.

Do not require project setup for work inside an existing project. When the user explicitly asks to create a new Compound Writing project, route to `setup-project` so `VOICE.md`, `STYLE.md`, `examples/`, and `drafts/` are created together. Treat `TASTE.md`, `context.md`, `published/`, and `.status.yaml` as legacy or project-specific surfaces, not requirements.

## Route By Outcome

Choose the smallest route that fits the request:

| User state or outcome | Route |
|---|---|
| Needs a new self-contained writing project | `setup-project`, then optional `onboarding` |
| No idea yet | `brainstorm` |
| Has a live idea and needs material | `interview` |
| Needs the point or reader promise sharpened | `thesis`, `promise` |
| Has notes and needs structure | `outline` |
| Has an outline or partial draft and needs prose | `draft` |
| Needs argument, structure, stakes, or evidence fixed | `dev-edit` |
| Structure is stable and prose needs revision | `line-edit` |
| Needs a first-time-reader or fresh-eyes cold read | `reader` |
| Sounds generic or machine-smoothed | `ai-check`, `voice-check`, `tracks` |
| Needs publication, project, or format standards | Load the active `STYLE.md`, brief, template, or maintained workflow |
| Needs a publication-readiness decision | `final-pass` |
| Needs pressure from multiple perspectives | `objections`, a named lens, `panel`, or `debate` |

The familiar sequence remains available:

```text
brainstorm -> interview -> outline -> draft -> dev-edit -> line-edit -> final-pass
```

Treat it as a map, not a gate. Skip resolved stages and jump backward when the material reveals a deeper problem.

## Start The Work

1. Identify the requested outcome.
2. Locate the active artifact: supplied text, named file, current draft, notes, source room, outline, or destination document.
3. Load the relevant voice, project, assignment, and source context.
4. State the route briefly when it includes several meaningful passes.
5. Begin. Ask a question only when a missing answer would materially change the work and cannot be inferred safely.

Do not lead with a tour of every feature. The user came to write, not admire the plumbing.

## Compose Skills Deliberately

- Use one skill when one skill can finish the job.
- Put diagnosis before revision and validation after revision.
- Run `dev-edit` before line-level passes when the argument or structure is unstable.
- Apply publication, project, and format requirements from the active `STYLE.md`, brief, template, or workflow while drafting or revising.
- Keep source provenance attached throughout the workflow.
- Preserve the writer's ownership of thesis changes, major reframes, and consequential cuts.

Common compositions:

- **Muscular revision:** `dev-edit` -> revision -> `line-edit` -> `ai-check`
- **Pre-publication:** `dev-edit` when needed -> `ai-check` -> `final-pass`
- **Voice repair:** `voice-check` -> targeted revision -> `ai-check` or `tracks`
- **High-stakes stress test:** `objections` or `panel` -> writer judgment -> targeted revision

## Artifacts And Progress

- Respect the project's existing folder and versioning conventions.
- Do not create a parallel draft workspace by default.
- In a project initialized by `setup-project`, create or reuse `drafts/<piece-slug>/` and keep that piece's versions, notes, research, outline, reviews, and related material there.
- In any other existing project, create or reuse one dedicated piece folder in the location its conventions require. Do not impose `drafts/` retroactively.
- Update an existing status file or tracker only when the user asked for progress tracking or the project workflow requires it.
- Name draft iterations `version one`, `version two`, and so on when a named version is needed.
- Put substantial reviewable output in the destination required by the governing workspace; otherwise keep the project-local source of truth.

## Completion

Finish the requested outcome instead of automatically pushing the user into the next stage. Then report:

- what changed or was produced;
- any source, thesis, or editorial uncertainty that still needs judgment;
- any recurring preference or failure pattern worth capturing through `save`.
