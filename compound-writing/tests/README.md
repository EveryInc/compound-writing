# Verification Plan

The external-facing architecture needs contract tests before release:

- `onboarding-flow.md`: a new user can understand setup, approve files, and
  begin real work without being pushed into unnecessary strategy setup.
- `workspace-loading.md`: context files are loaded only when relevant.
- `migration-contract.md`: legacy users can adopt the new structure without
  losing material or receiving silent reclassification.
- `improvement-loop.md`: durable learning always requires user approval.
- `public-boundary.md`: public core contains only portable defaults and
  synthetic or cleared examples.
