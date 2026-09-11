# Residual Review Findings

Source run: `lfg` pipeline on branch `cursor/compound-packs-7c77` (plan `docs/plans/2026-09-10-001-feat-compound-packs-plan.md`), code review step 4 with four reviewers (correctness, security+adversarial, testing, agent-native+standards). Twenty-five findings; the eligible ones were applied in `fix(review): apply review findings`. No tracker sink was available to this run (the GitHub CLI is read-only for cloud agents), so every residual is inlined here.

## Residual Review Findings

- P3 (advisory, no_sink) `skills/cw-packs/scripts/packs-resolve.py` `resolve_entry` path-source branch: the `.git` guard covers only `<home>/.git`; a nested checkout's `.git/` under the home is a valid home-relative source if rule-shaped `.md` files are planted there. Needs local write access to `.git/`; identical to compound-engineering-plugin's resolver. Optional hardening: reject any realpath containing a `.git` component.
- P3 (advisory, no_sink) `skills/cw-packs/scripts/packs-resolve.py` `_home_root`: `--home` on a symlinked draft resolves the physical location's home, not the link's. No containment escape; documented in `references/packs.md` ("Where the config lives").
- P2 (manual, no_sink) `tests/test_packs_resolve.py`: the positive tree-URL parse (`.../tree/<ref>/<path>` resolving to a clone) has no test because the regex is GitHub-only and a positive case would need network access; the two conflict-error cases are covered.
- P3 (advisory, no_sink) `skills/cw-packs/scripts/packs-resolve.py` `_main`: entries with independent git sources resolve sequentially. A bounded thread pool would need to preserve entry order for duplicate-id and message ordering; not applied.
- P3 (advisory, no_sink) `skills/cw-packs/scripts/packs-resolve.py` `_within`: could use `pathlib.PurePath.is_relative_to`; kept as-is for byte-parity with the upstream resolver.
- P3 (advisory, no_sink) `skills/cw-voice-check/SKILL.md` authority list numbers pack rules as item 4 while the shared contract calls the same position layer 5; relative order agrees, so no change.

## Deferred from the four tester matrices (2026-09-10)

Fixed with regression tests: two-hop symlink escape, FIFO hang, unreadable config layer, unvalidated `id:`, deleted cwd, README folder publishing its subfolder without a signal, entry outside the `packs:` block, nested-checkout home semantics, `cw-save` preview and selection rules, `cw-packs` verify signal. Deferred, one line each, all CE-identical unless noted:

- Hidden `.md` files count as rules (A10b): dotfiles are not part of the shared layout rule.
- Frontmatter detection is regex-only (A4b): a stricter parser would diverge from the shared format.
- No nested-rules hint when a sibling pack publishes (A14): firing per child would warn on storage dirs in legitimate multi-pack sources.
- Unreadable rule reported as missing frontmatter (A11c): cosmetic; the file is correctly skipped.
- `RULE.MD` / `.markdown` ignored silently (A3): the layout rule says `.md`.
- Unknown key errors but the entry still resolves (B7): failing the entry would drop a pack on a typo.
- `/`-in-branch hint on every tree-URL failure (D10, D11c): cosmetic.
- Credentials in a `source:` URL echoed in output (E9): the URL is the user's own config text; redaction deferred.
- Symlinked pack directory takes its realpath basename as id (A16): consistent with realpath containment.
- Unbounded config values in error text (E10): cosmetic.
- No rule count or 25-file signal from the resolver (A17): the cap is the consumer's contract.
- No cache refresh flag (D6): clearing the cache is the documented path.
- `path:` naming a file reports `does not exist` (D3): accurate for a non-directory.
- UTF-16 config parses as empty (B12): UTF-8 is the contract.
- Unclosed `[voice` and YAML anchors taken literally (B8): the documented subset is what the reader accepts.
- Ownership checked on the home directory only (C7c): a config dir inside an owned home is the owner's.
- Rules planted under a nested checkout's `.git/` publish (E5): documented residual.
- `home` key breaks CE's `toEqual` tests when pointed at this resolver: additive by design.
- `GIT_DIR`, `safe.directory`, `GIT_DISCOVERY_ACROSS_FILESYSTEM` not consulted: now documented; behavior deferred.
- No "behind upstream" staleness check (CE `check-health`): deferred feature.
- `.compound-writing -> .compound-engineering` symlink is followed: user-inflicted aliasing.
- Shared repo cloned once per plugin: isolation by design.
- Git cache is writable on disk (save N1): the read-only rule stays prose; `chmod` would break cache replacement.
- Unwritable path pack has no fallback wording (save N5): the write error surfaces at write time.
- Not loadable in Cursor (save N9): no Cursor manifest; pre-existing and out of scope.
- `name:` in command frontmatter is ignored by Claude Code (save N11): kept for the repo's own packaging test.
