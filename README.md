# Compound Writing: Externalization Proposal

This repository is a working proposal for making Compound Writing available
outside its original setting. The product idea is simple: give writers useful
AI-assisted workflows without shipping somebody else's voice, career strategy,
or private examples as their starting point.

Status: architecture scaffold for Every review, not a released plugin.

## What Is Here

| Package | What it would become | What reviewers can inspect now |
| --- | --- | --- |
| [`compound-writing/`](compound-writing/) | A portable public-core writing plugin. | Dual manifests, onboarding, blank workspace templates, synthetic example, functional review lenses, and release tests. |
| [`every-editorial-edition/`](every-editorial-edition/) | An optional layer of approved Every editorial guidance. | A deliberately empty package boundary and clearance checklist. No editorial material has been preloaded. |

The public core stands on its own. The optional Every package can add cleared
guidance later, but the core should never require it.

## The Proposal In One Minute

- Replace a single catch-all writing profile with user-owned files:
  `voice.md`, destination `style-guides/`, optional `strategy/`, and
  provisional `context.md`.
- Support longform, X, and LinkedIn without pretending those destinations need
  the same writing behavior.
- Rename persona-based reviewers by their editorial job: `cut`, `tension`,
  `momentum`, `humor`, `general-reader`, `stress-test`, and `story-check`.
- Let the system propose improvements over time, while requiring approval
  before it changes durable user guidance.
- Ship blank templates and fictional examples, not extracted personal context.

## Suggested Tour

For a quick review:

1. Read the [public-core introduction](compound-writing/README.md).
2. Walk through the [first-run experience](compound-writing/docs/GETTING-STARTED.md)
   and [onboarding contract](compound-writing/docs/ONBOARDING.md).
3. Open the [fictional researcher example](compound-writing/examples/independent-researcher/)
   to see what a populated workspace looks like.
4. Inspect the [workspace templates](compound-writing/defaults/workspace/)
   and [review skills](compound-writing/skills/).
5. Check the [release gates](compound-writing/release/) and the
   [Every-edition boundary](every-editorial-edition/).

## Repository Layout

```text
.
|-- compound-writing/          # Proposed public-core plugin
`-- every-editorial-edition/   # Optional, clearance-gated editorial layer
```

## What This Is Not Yet

This repository does not claim that the live Compound Writing plugin has
already migrated to this structure. It is the reviewable shape of the next
version: the file contract, user experience, package boundary, and tests to
approve before implementation and release.
