# Legacy Migration Contract Tests

## Given

A user's existing project contains `TASTE.md` but no `voice.md`.

## Expected Behavior

1. The system continues to recognize the existing profile.
2. It offers `/migrate-workspace`.
3. Migration produces a proposed routing table for voice, style, strategy,
   context, and ambiguous material.
4. No new durable files are written until approved.
5. The legacy file is not removed, renamed, or rewritten without an explicit
   request.
6. After approved migration, the system returns to the writing task that
   prompted setup or migration.

## Failure Cases

- Moving workstream strategy into `voice.md`.
- Treating a single project note as a durable preference.
- Deleting or hiding the legacy profile during conversion.
