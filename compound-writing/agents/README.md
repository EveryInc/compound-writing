# Agent Map

The public interface is skill-first. Agents support composed workflows where
multiple perspectives are useful.

```text
agents/
|-- feedback/
|   `-- voice-matcher.md
|-- review/
|   |-- trim-reviewer.md
|   |-- tension-reviewer.md
|   |-- momentum-reviewer.md
|   |-- humor-reviewer.md
|   |-- general-reader-reviewer.md
|   |-- stress-test-reviewer.md
|   `-- story-check-reviewer.md
`-- workflow/
    |-- scribe-orchestrator.md
    |-- panel-synthesizer.md
    `-- debate-moderator.md
```

Agent prompts should remain functional rather than asking the system to
imitate real people.

