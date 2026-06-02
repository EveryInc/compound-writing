# Release Checklist

This package describes the intended public-core experience, but it is not yet
a release candidate. Before it can move from architecture review to external
distribution, the team needs to complete the following work.

## Product Completion

- Replace proposal-status language with approved product copy.
- Migrate retained generic skills from the current repository after updating
  their workspace-loading behavior.
- Decide whether the optional editorial edition ships at all, and for whom.

## Trust And Distribution

- Add approved license, privacy, and terms materials.
- Confirm examples and templates contain only public-safe or synthetic material.
- Define the access model for any Every-specific package or guidance.

## Technical Verification

- Validate both `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json`.
- Test onboarding, legacy migration, destination routing, reviewer names, and
  the approval-based learning loop.
- Have a new user locate `docs/GETTING-STARTED.md` and complete the
  preview-before-write onboarding path without explanation from the builder.

## Release Decision

A release owner should be able to answer three questions before distribution:

1. Can a new user begin useful work without importing someone else's identity?
2. Does every durable learning require a visible approval step?
3. Has every distributed editorial example or guide been cleared for its audience?
