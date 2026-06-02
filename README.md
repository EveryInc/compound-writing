# Proposed Repository Shape

Status: Architecture scaffold for review, not live plugin source.

This directory makes the proposed external Compound Writing distribution
concrete without changing the maintained repository.

```text
proposed-repository/
|-- compound-writing/          # Public core package
`-- every-editorial-edition/   # Optional subscriber package boundary
```

## Package Boundary

| Package | Intended use | Current scaffold content |
| --- | --- | --- |
| `compound-writing/` | The public, broadly adoptable writing system. | Dual manifests, newcomer documentation, generic defaults, starter workspace, synthetic example, changed skill contracts, agent map, commands, and verification plan. |
| `every-editorial-edition/` | Optional distribution for approved subscriber-facing editorial material. | Manifest and boundary documentation only; no unapproved editorial content. |

The public package retains the product name `compound-writing`. It is complete
without installing the optional editorial edition.

## Review Path

1. Read `compound-writing/README.md`.
2. Test the newcomer path in `compound-writing/docs/GETTING-STARTED.md` and
   `compound-writing/docs/ONBOARDING.md`.
3. Review the user file contract in `compound-writing/defaults/workspace/`.
4. Inspect the changed skill contracts in `compound-writing/skills/`.
5. Review the synthetic example in
   `compound-writing/examples/independent-researcher/`.
6. Review tests and release questions in `compound-writing/tests/` and
   `compound-writing/release/`.

## Implementation Boundary

This structure is intended to be approved before changes are migrated into
the canonical Compound Writing source repository.
