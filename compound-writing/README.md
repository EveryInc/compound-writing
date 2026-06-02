# Compound Writing

Status: Proposed public-core repository scaffold. This is an architecture
artifact, not the current released plugin.

Compound Writing is a user-owned writing system for defining a voice,
adapting it to different destinations, and improving its guidance over time
through approved learnings.

## Product Contract

The plugin ships capabilities and blank workspace templates. A user's project
stores their voice, destination guides, strategy, context, and drafts.

```text
compound-writing/
|-- .claude-plugin/
|-- .codex-plugin/
|-- commands/
|-- docs/
|-- defaults/
|   |-- SYSTEM.md
|   `-- workspace/
|-- examples/
|-- agents/
|-- skills/
|-- tests/
`-- release/
```

```text
user-writing-project/
|-- voice.md
|-- context.md
|-- style-guides/
|   |-- longform.md
|   |-- x.md
|   `-- linkedin.md
|-- strategy/
|   |-- professional-positioning.md
|   `-- platform-strategy.md
|-- drafts/
`-- published/
```

## Getting Started

1. Install or enable the plugin in the supported host.
2. Open the folder where your writing work should live.
3. Run `/onboarding` to create a minimal `voice.md`, or run `/scribe` with a
   real writing request and accept its onboarding prompt.
4. Add a destination guide only for the kind of work you are doing now:
   longform, X, or LinkedIn.
5. Add strategy files only when you want help with public positioning or
   cross-platform publishing.

Onboarding previews each durable file before writing it. It does not infer
professional strategy, create a prefabricated voice, or convert an existing
`TASTE.md` without review.

Read:

- `docs/GETTING-STARTED.md` for the new-user path.
- `docs/ONBOARDING.md` for the setup conversation and file-writing rules.
- `docs/WORKSPACE-FILES.md` for what each user-owned file controls.

## First-Release Surfaces

| Area | Capabilities |
| --- | --- |
| Set up and memory | `onboarding`, `migrate-workspace`, `save`, `voice-check` |
| Workflow | `scribe`, `panel`, `debate` |
| Destinations | `longform`, `x-post`, `linkedin-post` |
| Review lenses | `trim`, `tension`, `momentum`, `humor`, `general-reader`, `stress-test`, `story-check` |

Existing drafting, editing, structural, and AI-pattern capabilities can be
ported from the current product after their loading rules use this workspace
contract.

## Important Boundaries

- No user's writing identity is supplied as a default.
- Templates and synthetic examples may ship in public core.
- An optional editorial edition must depend on the public core, never the
  reverse.
- A durable update to voice, style, or strategy requires user approval.

## Proposed Migration

Existing users with `TASTE.md` keep working through legacy fallback while the
system offers a guided, reviewable split into the new files. See
`docs/ONBOARDING.md`, `tests/migration-contract.md`, and
`skills/migrate-workspace/SKILL.md`.
