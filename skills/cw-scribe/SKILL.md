---
name: cw-scribe
description: Route open-ended writing work through the smallest useful Compound Writing workflow. Use when the user wants to start, continue, finish, or improve a piece and has not named a more specific skill.
---

# Scribe

Act as the orchestration layer for Compound Writing. Orient to the writer's actual context, identify the live artifact and desired outcome, then compose only the skills needed to get there.

## Find The Writer's Starting Point

Read `../../references/context-contract.md` before substantial work. Follow its authority order, project routing, provenance, destination, and write-safety rules.

At the first meaningful Compound Writing interaction, inspect the request, supplied material, current workspace, and maintained context before choosing a route.

- Treat an existing writing workspace, maintained voice or style context, or useful live artifact as a real starting point even when the Compound Writing scaffold is absent.
- If the user brings a draft, notes, sources, an active workspace, or enough context to begin, do the immediate writing work. Do not block on setup or a calibration interview. Offer to strengthen durable context only when it would materially improve future work.
- If there is no established writing context and no useful artifact to work from, briefly explain the benefit of one writing home: it keeps how the writer sounds, what their writing needs to do, examples, and drafts together so future sessions can start with less re-explaining.
- Guide that writer through one simple setup without requiring them to know the skill catalog. Resolve the target folder first, then route to `cw-setup-project` and begin `cw-onboarding` for `VOICE.md` and `STYLE.md`.

Do not create files until the destination is explicit or safely resolved from the user's request. Do not present multiple homes or a project system during normal first use. Another self-contained folder remains an optional manual capability only when the user explicitly asks for it later.

Treat `TASTE.md`, `context.md`, `published/`, and `.status.yaml` as legacy or workspace-specific surfaces, not requirements.

## Route By Outcome

Choose the smallest route that fits the request:

| User state or outcome | Route |
|---|---|
| First meaningful interaction with no writing home or useful artifact | Brief orientation, resolve the target, `cw-setup-project`, then `cw-onboarding` |
| Explicitly asks for another self-contained writing folder | `cw-setup-project`, then optional `cw-onboarding` |
| No idea yet | `cw-brainstorm` |
| Has a live idea and needs material | `cw-interview` |
| Needs the point or reader promise sharpened | `cw-thesis`, `cw-promise` |
| Needs the most important idea or real opening found and placed | `cw-bluf` |
| Has notes and needs structure | `cw-outline` |
| Has an outline or partial draft and needs prose | `cw-draft` |
| Needs argument, structure, stakes, or evidence fixed | `cw-dev-edit` |
| Structure is stable and prose needs revision | `cw-line-edit` |
| Needs a first-time-reader or fresh-eyes cold read | `cw-reader` |
| Sounds generic or machine-smoothed | `cw-ai-check`, `cw-voice-check`, `cw-tracks` |
| Needs publication, project, or format standards | Load the active `STYLE.md`, brief, template, or maintained workflow |
| Needs a publication-readiness decision | `cw-final-pass` |
| Needs pressure from multiple perspectives | `cw-objections`, a named lens, `cw-panel`, or `cw-debate` |

The familiar sequence remains available:

```text
cw-brainstorm -> cw-interview -> cw-outline -> cw-draft -> cw-dev-edit -> cw-line-edit -> cw-final-pass
```

Treat it as a map, not a gate. Skip resolved stages and jump backward when the material reveals a deeper problem.

## Start The Work

1. Identify the requested outcome and whether there is a useful artifact or established writing context.
2. Locate the active artifact: supplied text, named file, current draft, notes, source room, outline, or destination document.
3. Load the relevant voice, workspace, assignment, and source context.
4. Handle first-run setup only when the starting-point check shows it is needed.
5. State the route briefly when it includes several meaningful passes.
6. Begin. Ask a question only when a missing answer would materially change the work and cannot be inferred safely.

Do not lead with a tour of every feature. The user came to write, not admire the plumbing.

## Compose Skills Deliberately

- Use one skill when one skill can finish the job.
- Put diagnosis before revision and validation after revision.
- Run `cw-dev-edit` before line-level passes when the argument or structure is unstable.
- Apply publication, project, and format requirements from the active `STYLE.md`, brief, template, or workflow while drafting or revising.
- Keep source provenance attached throughout the workflow.
- Preserve the writer's ownership of thesis changes, major reframes, and consequential cuts.

Common compositions:

- **Lede repair:** `cw-bluf` -> targeted structural revision -> optional `cw-line-edit`
- **Muscular revision:** `cw-dev-edit` -> revision -> `cw-line-edit` -> `cw-ai-check`
- **Pre-publication:** `cw-dev-edit` when needed -> `cw-ai-check` -> `cw-final-pass`
- **Voice repair:** `cw-voice-check` -> targeted revision -> `cw-ai-check` or `cw-tracks`
- **High-stakes stress test:** `cw-objections` or `cw-panel` -> writer judgment -> targeted revision

## Artifacts And Progress

- Respect the project's existing folder and versioning conventions.
- Do not create a parallel draft workspace by default.
- In a writing home initialized by `cw-setup-project`, create or reuse `drafts/<piece-slug>/` and keep that piece's versions, notes, research, outline, reviews, and related material there.
- In any other existing project, create or reuse one dedicated piece folder in the location its conventions require. Do not impose `drafts/` retroactively.
- Update an existing status file or tracker only when the user asked for progress tracking or the project workflow requires it.
- Name draft iterations `version one`, `version two`, and so on when a named version is needed.
- Put substantial reviewable output in the destination required by the governing workspace; otherwise keep the project-local source of truth.

## Completion

Finish the requested outcome instead of automatically pushing the user into the next stage. Then report:

- what changed or was produced;
- any source, thesis, or editorial uncertainty that still needs judgment;
- any recurring preference or failure pattern worth capturing through `cw-save`.
