# Compound Writing

A context-first writing toolbox for developing ideas, drafting, revising, stress-testing, and preparing work for publication without sanding off the writer.

Compound Writing is packaged for both Claude and Codex from one canonical source tree. The full toolbox is available from the start, but users do not need to learn every tool: `cw-scribe` loads the governing context, helps a first-time writer establish one durable writing home when needed, and chooses the smallest useful workflow. Specialist skills remain available when the user wants a precise instrument.

## Start With Scribe

Describe what you want to write or paste in the work you already have. You do not need to choose a skill or ask for onboarding.

On a first meaningful interaction, Scribe looks for a draft, an active workspace, and useful writing context. If none exists, it briefly explains the benefit of one writing home, asks where it should live, creates the portable structure below, and helps begin `VOICE.md` and `STYLE.md`. If useful work is already in front of it, Scribe starts there and offers calibration only when it would help later sessions.

The system:

- gives a first-time writer one portable writing home with `VOICE.md`, `STYLE.md`, `examples/`, and `drafts/`;
- keeps syntax, diction, and tone in `VOICE.md` while routing argument, evidence, article structure, substantive standards, and publication readiness to `STYLE.md`;
- preserves existing workspaces and active drafts rather than imposing the scaffold retroactively;
- follows repository, global, project, assignment, and voice context in authority order;
- routes from the user's outcome instead of forcing a seven-stage pipeline;
- treats source provenance as part of writing rather than cleanup at the end;
- saves durable learning into maintained context, style guides, checklists, or workflows;
- keeps shared skill frontmatter valid across Claude and Codex.

See [ARCHITECTURE.md](ARCHITECTURE.md) for the full contract.

## The System

### Front door

All Compound Writing commands use the `cw-` prefix. Use `cw-scribe` for open-ended work: starting a piece, continuing from notes, finishing a draft, or figuring out which pass will help. Describe the outcome in ordinary language and let it route the work. On first use, Scribe can guide the writing-home setup without making the user learn the catalog. Name a specialist skill directly when you already know the exact tool you want.

Use `cw-setup-project` directly only when you explicitly want to create or migrate a self-contained writing folder yourself.

### Writing home

```text
writing-home/
├── VOICE.md
├── STYLE.md
├── examples/
└── drafts/
    └── piece-slug/
```

`VOICE.md` answers how the sentences should sound: syntax, diction, and tone. `STYLE.md` answers what the writing must do, contain, and prove: argument, evidence, article structure, substantive standards, and publication readiness. `examples/` holds curated evidence for those rules. `drafts/` keeps each piece's notes, research, outline, versions, and reviews together.

A rule that changes wording, sentence construction, or tone goes in `VOICE.md`. A rule that changes the claim, support, organization, or readiness standard goes in `STYLE.md`. Mixed feedback is split into two rules.

The setup workflow never creates the writing home inside the plugin or overwrites an existing file. It resolves the target first. Existing workspaces keep their own conventions unless the user explicitly asks to add or migrate the scaffold.

### Outcome map

| Outcome | Skills |
|---|---|
| Establish a writing home on first use | `cw-scribe` -> `cw-setup-project` -> `cw-onboarding` |
| Find or develop the idea | `cw-brainstorm`, `cw-interview` |
| Sharpen the point and reader promise | `cw-thesis`, `cw-promise`, `cw-outline` |
| Produce prose | `cw-draft` |
| Find a buried or misplaced lede | `cw-bluf` |
| Fix argument, structure, stakes, or evidence | `cw-dev-edit` |
| Revise sentences while preserving voice | `cw-line-edit` |
| Remove machine residue or voice drift | `cw-ai-check`, `cw-voice-check`, `cw-tracks` |
| See the piece through a first-time reader's eyes | `cw-reader` |
| Pressure-test the piece | `cw-objections`, `cw-asshole`, `cw-panel`, `cw-debate`, reviewer lenses |
| Check publication readiness | `cw-final-pass` |

The classic flow still works:

```text
cw-brainstorm -> cw-interview -> cw-outline -> cw-draft -> cw-dev-edit -> cw-line-edit -> cw-final-pass
```

It is a map, not a gate.

## The Full Toolbox

### Writing Home And Navigation

| Tool | Job |
|---|---|
| `cw-setup-project` | Manually create a portable writing home with `VOICE.md`, `STYLE.md`, `examples/`, and `drafts/`. |
| `cw-onboarding` | Begin or refresh the writing home's voice and style rules. |
| `cw-scribe` | Choose and compose the smallest useful workflow for an open-ended request. |
| `cw-save` | Turn a confirmed preference or lesson into durable project context. |

### Develop The Idea

| Tool | Job |
|---|---|
| `cw-brainstorm` | Surface promising raw material when no clear idea exists yet. |
| `cw-interview` | Draw out the material, stakes, and thinking behind a live idea. |
| `cw-thesis` | Generate possible central claims. |
| `cw-promise` | Clarify what the reader should anticipate or receive. |
| `cw-outline` | Organize notes and interview material into a workable structure. |
| `cw-hook` | Generate opening options for the current material. |
| `cw-transition` | Build a natural bridge between sections or ideas. |
| `cw-analogy` | Find concrete ways to explain a difficult concept. |
| `cw-simplify` | Rewrite complex material in plainer language. |

### Draft And Revise

| Tool | Job |
|---|---|
| `cw-draft` | Turn notes, sources, an outline, or partial prose into a complete draft. |
| `cw-bluf` | Find the most important idea and judge whether it appears where it belongs. |
| `cw-dev-edit` | Fix the argument, structure, stakes, evidence, and payoff. |
| `cw-line-edit` | Revise sentences and words without flattening the writer's voice. |
| `cw-voice-check` | Diagnose voice drift and produce a closer revision. |
| `cw-ai-check` | Remove common patterns that make prose sound machine-generated. |
| `cw-tracks` | Remove scaffolding, process narration, and residue from earlier thinking. |
| `cw-final-pass` | Decide whether a piece is ready, almost ready, or still needs work. |

### Pressure-Test And Add A Lens

| Tool | Job |
|---|---|
| `cw-objections` | Surface the strongest reader resistance and counterarguments. |
| `cw-panel` | Convene several reviewer perspectives and synthesize their feedback. |
| `cw-debate` | Let reviewers challenge one another until tensions resolve or become clear choices. |
| `cw-emergent` | Compose a custom workflow when no single tool fits the job. |
| `cw-asshole` | Apply the least charitable reading and attack weak claims or assumptions. |
| `cw-hemingway` | Cut unnecessary words and demand economy. |
| `cw-hitchcock` | Review suspense, tension, and what the reader knows when. |
| `cw-reader` | Trace the first-time reading experience and flag confusion, missing setup, and off-putting friction. |
| `cw-mom` | Find where a smart general reader may become confused or lose the thread. |
| `cw-sedaris` | Find missed opportunities for specificity, humor, and self-implication. |
| `cw-sorkin` | Review pacing, momentum, and forward motion. |
| `cw-vonnegut` | Apply story fundamentals: wants, stakes, character, and purposeful sentences. |

Publication, project, and format standards belong in the active project's `STYLE.md`, brief, or maintained workflow rather than in hard-coded publication-specific skills.

## Context And Learning

Compound Writing loads context in this order:

1. Explicit user instructions and supplied material.
2. Repository or workspace instructions.
3. Global identity, preference, rule, and voice files named by those instructions.
4. Active writing-home or project `VOICE.md`, `STYLE.md`, brief, template, workflow, or checklist.
5. Relevant curated examples from its `examples/` folder.
6. Assignment notes, sources, research, outline, draft, and destination requirements.
7. A legacy `TASTE.md`, only when the project still maintains it.
8. Plugin defaults for unresolved gaps only.

`cw-save` routes confirmed syntax, diction, and tone learning to `VOICE.md`; it routes argument, evidence, article-structure, and publication-readiness learning to `STYLE.md`. It does not silently edit an installed plugin, create hidden onboarding state, or claim private memory.

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
