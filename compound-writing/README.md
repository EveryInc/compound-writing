# Compound Writing

Compound Writing is a writing plugin designed to learn how you write without
deciding who you are for you. It helps you develop ideas, shape work for its
destination, review drafts from specific editorial angles, and save useful
patterns only when you approve them.

Status: proposed public-core package for review. The skill contracts and
workspace design are here; this is not the currently released plugin.

## How It Feels To Use

You bring a real assignment: an essay idea, a draft, an X post, a LinkedIn
post, or an artifact you want to explain. Compound Writing can:

- set up a small voice profile from your answers;
- create guidance for the destination you are using right now;
- help develop, adapt, or review the work;
- notice repeated preferences and propose a saved update; and
- keep anything durable under your review and in your project folder.

The plugin supplies workflow and blank templates. Your project stores your
voice, destination guides, strategy, context, drafts, and published work.

## Your Workspace

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

Start small. Most writers need only `voice.md` and one destination guide for
their first piece. Strategy files are optional and appear only when the work
actually involves positioning or cross-platform publishing.

## First Session

1. Install or enable the plugin in the supported host.
2. Open the folder where your writing work should live.
3. Run `/onboarding` to create a minimal `voice.md`, or run `/scribe` with a
   real writing request and accept its onboarding prompt.
4. Add a destination guide only for the kind of work you are doing now:
   longform, X, or LinkedIn.
5. Add strategy files only when you want help with public positioning or
   cross-platform publishing.
6. Review, draft, or adapt a real piece with the files you approved.

Onboarding previews each durable file before writing it. It does not infer
professional strategy, create a prefabricated voice, or convert an existing
`TASTE.md` without review.

Continue with:

- [Getting started](docs/GETTING-STARTED.md) for the new-user path.
- [Onboarding contract](docs/ONBOARDING.md) for setup behavior and approval rules.
- [Workspace files](docs/WORKSPACE-FILES.md) for what each user-owned file controls.
- [Independent researcher example](examples/independent-researcher/) for a fully
  fictional, populated workspace.

## What The Public Core Includes

| You want to... | Capabilities |
| --- | --- |
| Set up or improve your workspace | `onboarding`, `migrate-workspace`, `save`, `voice-check` |
| Move from an idea to a developed piece | `scribe`, `panel`, `debate` |
| Shape work for where it will appear | `longform`, `x-post`, `linkedin-post` |
| Put a draft under editorial pressure | `cut`, `tension`, `momentum`, `humor`, `general-reader`, `stress-test`, `story-check` |

Existing drafting, editing, structural, and AI-pattern capabilities can be
ported from the current product after their loading rules use this workspace
contract.

## What It Will Not Do By Default

- It will not supply a writing identity or professional strategy as a default.
- It will not treat one draft choice as a permanent preference.
- It will not rewrite durable guidance without approval.
- It will not require an Every-specific package in order to work.

Templates and synthetic examples may ship in public core. An optional
editorial edition may depend on the public core; the public core never depends
on it.

## For Existing Users

Existing users with `TASTE.md` keep working through legacy fallback while the
system offers a guided, reviewable split into the new files. See
[the onboarding contract](docs/ONBOARDING.md),
[the migration test](tests/migration-contract.md), and
[the migration skill](skills/migrate-workspace/SKILL.md).

## For Reviewers And Implementers

- [`skills/`](skills/) defines the behaviors that change in the external version.
- [`agents/`](agents/) maps composed reviewer and workflow roles.
- [`tests/`](tests/) states the user promises that should pass before release.
- [`release/`](release/) lists decisions still required before external distribution.
