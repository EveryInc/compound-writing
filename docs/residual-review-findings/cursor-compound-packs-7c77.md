# Residual Review Findings

Source run: `lfg` pipeline on branch `cursor/compound-packs-7c77` (plan `docs/plans/2026-09-10-001-feat-compound-packs-plan.md`), code review step 4 with four reviewers (correctness, security+adversarial, testing, agent-native+standards). Twenty-five findings; the eligible ones were applied in `fix(review): apply review findings`. No tracker sink was available to this run (the GitHub CLI is read-only for cloud agents), so every residual is inlined here.

## Residual Review Findings

- P3 (advisory, no_sink) `skills/cw-packs/scripts/packs-resolve.py` `resolve_entry` path-source branch: the `.git` guard covers only `<home>/.git`; a nested checkout's `.git/` under the home is a valid home-relative source if rule-shaped `.md` files are planted there. Needs local write access to `.git/`; identical to compound-engineering-plugin's resolver. Optional hardening: reject any realpath containing a `.git` component.
- P3 (advisory, no_sink) `skills/cw-packs/scripts/packs-resolve.py` `_home_root`: `--home` on a symlinked draft resolves the physical location's home, not the link's. No containment escape; documented in `references/packs.md` ("Where the config lives").
- P2 (manual, no_sink) `tests/test_packs_resolve.py`: the positive tree-URL parse (`.../tree/<ref>/<path>` resolving to a clone) has no test because the regex is GitHub-only and a positive case would need network access; the two conflict-error cases are covered.
- P3 (advisory, no_sink) `skills/cw-packs/scripts/packs-resolve.py` `_main`: entries with independent git sources resolve sequentially. A bounded thread pool would need to preserve entry order for duplicate-id and message ordering; not applied.
- P3 (advisory, no_sink) `skills/cw-packs/scripts/packs-resolve.py` `_within`: could use `pathlib.PurePath.is_relative_to`; kept as-is for byte-parity with the upstream resolver.
- P3 (advisory, no_sink) `skills/cw-voice-check/SKILL.md` authority list numbers pack rules as item 4 while the shared contract calls the same position layer 5; relative order agrees, so no change.
