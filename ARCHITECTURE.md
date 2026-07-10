# Compound Writing Architecture

Compound Writing is a context-first writing system. It can initialize one self-contained writing project when the user asks, but it does not seize an existing workspace, invent a parallel memory system, or force every piece through one pipeline. It loads the context that governs the work, routes to the smallest useful workflow, and leaves durable artifacts in the project's authoritative location.

## Design Principles

1. **Context before craft** — Load identity, preferences, project rules, voice, assignment context, and source material before applying a writing workflow.
2. **Authority before accumulation** — Prefer maintained source-of-truth files over inferred memory or plugin defaults.
3. **Outcome routing** — Start from what the user is trying to accomplish, not from a mandatory stage sequence.
4. **Human ownership** — Preserve the writer's thesis, voice, and judgment. The system can pressure an argument; it should not quietly replace it.
5. **Provenance in the workflow** — Keep claims attached to sources and mark unsupported or model-added material explicitly.
6. **Durable artifacts** — Put notes, outlines, drafts, reviews, and research where the active project expects them. Do not create a second workspace by default.
7. **Progressive disclosure** — Load only the skill and references needed for the current task.
8. **One source, two packages** — `skills/` is the cross-runtime behavior layer. Claude and Codex packaging may expose it differently, but should not fork the editorial logic.
9. **Full toolbox, light front door** — Ship every generic tool in the public package while letting `scribe` protect first-time users from choosing among them prematurely.

## Project Setup Contract

`setup-project` creates one portable project folder with a deliberate minimum:

```text
project-name/
├── VOICE.md
├── STYLE.md
├── examples/
└── drafts/
```

- `VOICE.md` governs how sentences sound: syntax, diction, and tone, including cadence, register, punctuation, and verbal tics.
- `STYLE.md` governs what an article must do, contain, and prove: argument, evidence, article structure, substantive standards, and publication readiness.
- `examples/` holds curated positive and negative examples that clarify the written rules without replacing them.
- `drafts/` holds one folder per piece, with that piece's notes, research, outline, versions, and reviews together.

Project setup is explicit, never inferred from missing files. Existing projects retain their own structure and authority. A legacy `TASTE.md` may be migrated into the two guides, but it is not created for new projects and is never silently deleted.

The boundary is operational: rules that change wording, sentence construction, or tone go in `VOICE.md`; rules that change the claim, support, organization, or readiness standard go in `STYLE.md`. Mixed feedback becomes two atomic rules rather than one instruction duplicated across both files.

## Runtime Layers

### 1. Context layer

The context contract lives in `references/context-contract.md`. It defines the authority order, project routing, source handling, and write-safety rules that orchestration and voice-sensitive skills inherit.

### 2. Orchestration layer

`scribe` is the front door. It inspects the request and available artifacts, then chooses the smallest useful route:

- **Explore** — `brainstorm`, `interview`
- **Shape** — `thesis`, `promise`, `outline`
- **Draft** — `draft` using the active `VOICE.md`, `STYLE.md`, brief, and sources
- **Revise** — `dev-edit`, then `line-edit` when structure is stable
- **Validate** — `ai-check`, `voice-check`, `final-pass`
- **Stress-test** — `reader`, `objections`, `asshole`, `panel`, `debate`, or a named lens

The familiar brainstorm-to-final-pass sequence remains available, but it is a map rather than a gate.

### 3. Craft layer

Portable skills handle general writing operations: idea development, outlining, drafting, developmental editing, line editing, hooks, transitions, objections, first-time-reader reviews, and other reviewer lenses.

The public package contains the full generic toolbox. Progressive disclosure comes from routing and context loading, not from withholding specialist skills.

## Artifact Contract

- Respect the current project's folder structure and local instructions.
- Treat attached or named drafts as the active artifact; do not require `drafts/{slug}/`.
- In a project initialized by `setup-project`, create or reuse `drafts/<piece-slug>/` before producing draft versions or support material.
- In any other project, create or reuse a dedicated piece folder where its existing convention requires it. Do not impose the Compound Writing scaffold retroactively.
- Keep notes, outlines, research, reviews, and every named draft iteration for one piece together so parent folders remain navigable.
- Use local Markdown as the default project source of truth unless the user names another destination.
- Use an existing `research.md`, source room, claim ledger, status file, or project tracker when present. Do not create parallel versions without need.
- Use version labels (`version one`, `version two`, and so on) rather than `final`, `clean`, or `final draft` when producing named draft iterations.
- Do not publish, send, schedule, or modify shared systems without the approval required by the governing project rules.

## Learning Contract

Compound learning means updating a maintained context surface, not claiming private memory.

- Cross-project voice preferences belong in the user's global voice guide.
- Project syntax, diction, and tone preferences belong in `VOICE.md`; project argument, evidence, article-structure, and publication-readiness standards belong in `STYLE.md`.
- Recurring editorial failures belong in the relevant review checklist or skill reference.
- Workflow improvements belong in the workflow or architecture docs.
- One-off observations stay with the current piece unless the user confirms they should generalize.
- Never edit an installed plugin/cache copy to "remember" a lesson.

`save` proposes the right destination and follows its write-safety rules. It does not silently append lessons to plugin files.

## Packaging Contract

- `skills/` is canonical across Claude and Codex.
- `.codex-plugin/plugin.json` packages the shared skills for Codex.
- `.claude-plugin/` and `agents/` provide Claude compatibility and optional subagent execution.
- `commands/` is a compatibility/help surface, not a second implementation of the skills.
- Public releases are assembled from an explicit allowlist containing the full generic toolbox. Publication-, company-, writer-, column-, and platform-specific extensions are excluded from the published package.
- Runtime cache or installed plugin folders are derived copies, never source of truth.
- Cross-platform `SKILL.md` frontmatter uses only the shared Agent Skills fields: `name` and `description`.
- Platform-specific invocation or UI metadata belongs in platform-specific packaging, not shared skill frontmatter.

## Architecture Tests

An architecture change is ready when:

1. Both plugin manifests describe the same product and public version.
2. Every skill passes the Codex skill validator.
3. The Codex plugin passes plugin validation.
4. Skill descriptions state clear triggers and boundaries.
5. Core workflows load the context contract before voice-sensitive work.
6. Existing-project workflows do not require the Compound Writing scaffold, and `setup-project` reliably creates `VOICE.md`, `STYLE.md`, `examples/`, and `drafts/` when explicitly invoked.
7. New workflows do not create or depend on `TASTE.md`, `context.md`, `published/`, or `.status.yaml`.
8. Documentation does not advertise hand-maintained component counts as product behavior.
9. Existing user changes and project-local conventions remain authoritative.
10. The public build contains only allowlisted generic skills and no references to excluded editorial or personal overlays.
