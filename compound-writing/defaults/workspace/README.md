# Default User Workspace Templates

These are the blank files Compound Writing can offer during setup. They are
prompts and containers, not a prewritten personality. A new user's approved
answers belong in their own project, never in the distributed plugin.

## A Small Useful Start

Do not create every file just because it exists. For a first assignment,
onboarding can produce:

```text
your-project/
|-- voice.md
`-- style-guides/
    `-- {destination-needed-now}.md
```

Additional files become useful when the user has active work, is adapting
across destinations, or explicitly wants strategy help.

## Available Templates

```text
user-writing-project/
|-- voice.md
|-- context.md
|-- style-guides/
|   |-- longform.md
|   |-- x.md
|   `-- linkedin.md
`-- strategy/
    |-- professional-positioning.md
    `-- platform-strategy.md
```

| Template | Use it when... | Avoid putting here... |
| --- | --- | --- |
| `voice.md` | A preference should travel across formats. | A rule that applies only to one platform or one draft. |
| `style-guides/*.md` | A destination changes structure, proof, length, or tone. | General claims about the user's identity. |
| `strategy/*.md` | The user requests public positioning or platform planning. | Assumptions inferred during basic setup. |
| `context.md` | A current project detail or provisional lesson may help the next step. | An unapproved permanent rule. |

## Learning Rule

The system may notice a pattern. It may record a provisional note in
`context.md` or propose an edit to a durable file. It must show the proposed
change and obtain the user's approval before updating voice, style, or
strategy.

Read next:

- [Onboarding behavior](../../docs/ONBOARDING.md)
- [File boundaries and precedence](../../docs/WORKSPACE-FILES.md)
- [Fictional filled-in example](../../examples/independent-researcher/)
