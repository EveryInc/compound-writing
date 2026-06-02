# Repository Tree

```text
proposed-repository/
|-- README.md
|-- REPOSITORY-TREE.md
|-- compound-writing/
|   |-- .claude-plugin/plugin.json
|   |-- .codex-plugin/plugin.json
|   |-- AGENTS.md
|   |-- CLAUDE.md
|   |-- CODEX.md
|   |-- CHANGELOG.md
|   |-- README.md
|   |-- commands/
|   |-- docs/
|   |   |-- GETTING-STARTED.md
|   |   |-- ONBOARDING.md
|   |   `-- WORKSPACE-FILES.md
|   |-- defaults/
|   |   |-- SYSTEM.md
|   |   `-- workspace/
|   |       |-- voice.md
|   |       |-- context.md
|   |       |-- style-guides/
|   |       `-- strategy/
|   |-- examples/
|   |   `-- independent-researcher/
|   |-- agents/
|   |   |-- feedback/
|   |   |-- review/
|   |   `-- workflow/
|   |-- skills/
|   |-- tests/
|   `-- release/
`-- every-editorial-edition/
    |-- .claude-plugin/plugin.json
    |-- .codex-plugin/plugin.json
    |-- README.md
    |-- AGENTS.md
    |-- style-guides/
    |-- skills/
    |-- examples/
    `-- release/
```

The `compound-writing` package contains working design contracts for the
behaviors being changed. Generic existing skills that do not define the new
contract should be ported during implementation rather than copied into this
architecture artifact.
