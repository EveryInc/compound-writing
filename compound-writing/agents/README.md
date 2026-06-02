# Agent Map

Users should usually encounter skills, not an organizational chart of agents.
This folder defines supporting roles for moments when one request benefits
from several editorial perspectives: a review panel, a structured debate, or
a guided writing session.

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

## Review Roles

| Role | The question it asks |
| --- | --- |
| `trim` | What can be removed without losing meaning or voice? |
| `tension` | Where does the reader need sharper stakes, uncertainty, or contrast? |
| `momentum` | Where does the draft stall or repeat itself? |
| `humor` | Where could wit, surprise, or self-awareness help without forcing a joke? |
| `general-reader` | Where is the intended reader likely to lose the thread? |
| `stress-test` | What claim or assumption is easiest to challenge? |
| `story-check` | Does the piece deliver an arc, consequence, or earned payoff? |

## Naming Rule

Agent prompts are named for their editorial job. They should not ask the
system to imitate real writers, directors, or personalities. A user can
understand what a lens does before deciding to run it.
