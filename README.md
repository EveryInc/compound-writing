# Compound Writing

A context-first writing toolbox for developing ideas, drafting, revising, stress-testing, and preparing work for publication without sanding off the writer.

Compound Writing is packaged for both Claude and Codex from one canonical source tree. The full toolbox is available from the start, but users do not need to learn every tool: `scribe` loads the governing context and chooses the smallest useful workflow. Specialist skills remain available when the user wants a precise instrument.

## What Changed In 2.1

Compound Writing now has an explicit project-setup path. Instead of combining every preference in `TASTE.md`, a new project separates sentence-level voice from project-level style and keeps the working material beside both.

The current system:

- creates one portable project with `VOICE.md`, `STYLE.md`, `examples/`, and `drafts/` when the user asks for setup;
- keeps syntax, diction, and tone in `VOICE.md` while routing argument, evidence, article structure, substantive standards, and publication readiness to `STYLE.md`;
- preserves existing project layouts rather than imposing the scaffold retroactively;
- follows repository, global, project, assignment, and voice context in authority order;
- routes from the user's outcome instead of forcing a seven-stage pipeline;
- treats source provenance as part of writing rather than cleanup at the end;
- saves durable learning into maintained context, style guides, checklists, or workflows;
- keeps shared skill frontmatter valid across Claude and Codex.

See [ARCHITECTURE.md](ARCHITECTURE.md) for the full contract.

## The System

### Front door

Use `scribe` for open-ended work: starting a piece, continuing from notes, finishing a draft, or figuring out which pass will help. Describe the outcome in ordinary language and let it route the work. Name a specialist skill directly when you already know the exact tool you want.

Use `setup-project` when you want a new self-contained writing folder. Use `onboarding` afterward to fill or refine its two guides.

### Project setup

```text
project-name/
├── VOICE.md
├── STYLE.md
├── examples/
└── drafts/
    └── piece-slug/
```

`VOICE.md` answers how the sentences should sound: syntax, diction, and tone. `STYLE.md` answers what the article must do, contain, and prove: argument, evidence, article structure, substantive standards, and publication readiness. `examples/` holds curated evidence for those rules. `drafts/` keeps each piece's notes, research, outline, versions, and reviews together.

A rule that changes wording, sentence construction, or tone goes in `VOICE.md`. A rule that changes the claim, support, organization, or readiness standard goes in `STYLE.md`. Mixed feedback is split into two rules.

The setup workflow never creates the project inside the plugin or overwrites an existing file. Existing projects keep their own conventions unless the user explicitly asks to add or migrate the scaffold.

### Outcome map

| Outcome | Skills |
|---|---|
| Set up a self-contained writing project | `setup-project`, `onboarding` |
| Find or develop the idea | `brainstorm`, `interview` |
| Sharpen the point and reader promise | `thesis`, `promise`, `outline` |
| Produce prose | `draft` |
| Fix argument, structure, stakes, or evidence | `dev-edit` |
| Revise sentences while preserving voice | `line-edit` |
| Remove machine residue or voice drift | `ai-check`, `voice-check`, `tracks` |
| See the piece through a first-time reader's eyes | `reader` |
| Pressure-test the piece | `objections`, `asshole`, `panel`, `debate`, reviewer lenses |
| Check publication readiness | `final-pass` |

The classic flow still works:

```text
brainstorm -> interview -> outline -> draft -> dev-edit -> line-edit -> final-pass
```

It is a map, not a gate.

## The Full Toolbox

### Project And Navigation

| Tool | Job |
|---|---|
| `setup-project` | Create a portable project with `VOICE.md`, `STYLE.md`, `examples/`, and `drafts/`. |
| `onboarding` | Define or refresh the project's voice and style rules. |
| `scribe` | Choose and compose the smallest useful workflow for an open-ended request. |
| `save` | Turn a confirmed preference or lesson into durable project context. |

### Develop The Idea

| Tool | Job |
|---|---|
| `brainstorm` | Surface promising raw material when no clear idea exists yet. |
| `interview` | Draw out the material, stakes, and thinking behind a live idea. |
| `thesis` | Generate possible central claims. |
| `promise` | Clarify what the reader should anticipate or receive. |
| `outline` | Organize notes and interview material into a workable structure. |
| `hook` | Generate opening options for the current material. |
| `transition` | Build a natural bridge between sections or ideas. |
| `analogy` | Find concrete ways to explain a difficult concept. |
| `simplify` | Rewrite complex material in plainer language. |

### Draft And Revise

| Tool | Job |
|---|---|
| `draft` | Turn notes, sources, an outline, or partial prose into a complete draft. |
| `dev-edit` | Fix the argument, structure, stakes, evidence, and payoff. |
| `line-edit` | Revise sentences and words without flattening the writer's voice. |
| `voice-check` | Diagnose voice drift and produce a closer revision. |
| `ai-check` | Remove common patterns that make prose sound machine-generated. |
| `tracks` | Remove scaffolding, process narration, and residue from earlier thinking. |
| `final-pass` | Decide whether a piece is ready, almost ready, or still needs work. |

### Pressure-Test And Add A Lens

| Tool | Job |
|---|---|
| `objections` | Surface the strongest reader resistance and counterarguments. |
| `panel` | Convene several reviewer perspectives and synthesize their feedback. |
| `debate` | Let reviewers challenge one another until tensions resolve or become clear choices. |
| `emergent` | Compose a custom workflow when no single tool fits the job. |
| `asshole` | Apply the least charitable reading and attack weak claims or assumptions. |
| `hemingway` | Cut unnecessary words and demand economy. |
| `hitchcock` | Review suspense, tension, and what the reader knows when. |
| `reader` | Trace the first-time reading experience and flag confusion, missing setup, and off-putting friction. |
| `mom` | Find where a smart general reader may become confused or lose the thread. |
| `sedaris` | Find missed opportunities for specificity, humor, and self-implication. |
| `sorkin` | Review pacing, momentum, and forward motion. |
| `vonnegut` | Apply story fundamentals: wants, stakes, character, and purposeful sentences. |

Publication, project, and format standards belong in the active project's `STYLE.md`, brief, or maintained workflow rather than in hard-coded publication-specific skills.

## Context And Learning

Compound Writing loads context in this order:

1. Explicit user instructions and supplied material.
2. Repository or workspace instructions.
3. Global identity, preference, rule, and voice files named by those instructions.
4. Active project `VOICE.md`, `STYLE.md`, brief, template, workflow, or checklist.
5. Relevant curated examples from the project's `examples/` folder.
6. Assignment notes, sources, research, outline, draft, and destination requirements.
7. A legacy `TASTE.md`, only when the project still maintains it.
8. Plugin defaults for unresolved gaps only.

`save` routes confirmed syntax, diction, and tone learning to `VOICE.md`; it routes argument, evidence, article-structure, and publication-readiness learning to `STYLE.md`. It does not silently edit an installed plugin or claim private memory.

## Repository Layout

```text
compound-writing/
├── .claude-plugin/      # Claude manifest and marketplace metadata
├── .codex-plugin/       # Codex manifest
├── agents/              # Claude subagent adapters for panels and specialist work
├── commands/            # Claude compatibility/help surfaces
├── defaults/            # Optional fallback templates
├── references/          # Shared architecture and context contracts
├── skills/              # Canonical cross-runtime workflows
├── ARCHITECTURE.md
└── README.md
```

`skills/` is the source of truth for writing behavior. Installed plugin directories and caches are derived runtime copies.

Public releases are built from an explicit generic-skill allowlist. Internal or publication-specific extensions are not included in the published package.

## Installation

The repository root is the installable plugin. Clone it locally, then point the local-plugin or marketplace configuration for your runtime at that folder.

For Codex, [codex-marketplace.example.json](codex-marketplace.example.json) shows the expected local marketplace entry. For Claude, use the manifest in `.claude-plugin/`. Start a new session after installing so the toolbox and its skills are loaded.

The public repository contains only the generic toolbox. Publication-, company-, writer-, column-, and platform-specific extensions are maintained separately.

## License

MIT
