# Every Editorial Edition

This folder reserves a clean place for an optional Every-specific layer on top
of public Compound Writing. It could eventually provide approved editorial
guidance for an audience allowed to receive it.

Status: proposed package boundary only. It intentionally contains no editorial
style guide, internal example, or publication workflow awaiting clearance.

## Why It Is Separate

The public core should teach any writer to create and own their workspace.
Every-specific guidance has a different distribution decision and a different
clearance burden. Keeping it in a separate package prevents publication
material from becoming a hidden default in the public product.

## Dependency Direction

| Rule | Reason |
| --- | --- |
| Public `compound-writing` must work independently. | No public user should need a subscriber or internal overlay. |
| This edition may assume the public workspace files and functional reviewer names. | An overlay can extend the shared product contract. |
| This edition must not add personal voice, private examples, internal analytics, or uncleared publication material. | Distribution must not expose private context or turn an individual's identity into a default. |

## What Could Eventually Live Here

```text
every-editorial-edition/
|-- .claude-plugin/
|-- .codex-plugin/
|-- style-guides/
|   `-- README.md
|-- skills/
|   `-- README.md
|-- examples/
|   `-- README.md
`-- release/
    `-- clearance-checklist.md
```

Examples of acceptable future material include an explicitly cleared
publication-level checklist or a synthetic example built for this edition.
Approval of the public core does not approve any content for this package.

## Before Populating This Folder

1. Define the intended audience and access model.
2. Clear every guide, example, and workflow for that audience.
3. Verify that no personal profile, unpublished material, analytics, or
   private communication has been embedded.
4. Run the [clearance checklist](release/clearance-checklist.md).
