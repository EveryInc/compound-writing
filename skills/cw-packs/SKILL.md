---
name: cw-packs
description: Declare, scaffold, and check Compound Packs for a writing home so shared voice, style, publication, and lens rules load into every writing step. Use when the user wants to add, create, list, or troubleshoot a pack or a packs entry.
---

# Compound Packs

Manage the packs a writing home declares. A pack is a folder of prescriptive writing rules that every Compound Writing step reads at the moment it matters and cites as `(pack: <id>, <file>)`. The format and the resolver mirror Compound Engineering's packs, so one pack repository can serve both plugins. Read `../../references/packs.md` for the full guide before changing anything.

Packs are declared, never scanned. Nothing happens until `<home>/.compound-writing/config.yaml` (or `config.local.yaml`) names a source under a live `packs:` key.

## Resolve The Home

The writing home is found the way git finds a repository: the nearest directory at or above the working directory, or the named draft, that holds `.compound-writing/`, else the first that holds `.git`. The search never crosses a filesystem boundary and skips a folder the user does not own. When nothing qualifies, this skill's writes target the writing-home folder the user names or that `cw-setup-project` would use, and `.compound-writing/` is created there. Never write inside the installed plugin or a runtime cache.

Every preview in this skill names the resolved home and the absolute path of the config file it would change, so a home found above the working directory is visible before anything is written.

## Check Packs

Run the bundled resolver from the plugin, resolving the path relative to this `SKILL.md`:

```bash
python3 "<plugin-root>/skills/cw-packs/scripts/packs-resolve.py" --home "<home-or-draft-path>"
```

Render the JSON for the writer, one line per entry:

- each `roots` item as `pack <id> -> <dir>`, plus `(<url>@<ref>)` when git-sourced and `N rule-shaped file(s) in subfolders kept as storage` when `nested_rule_shaped` is non-zero;
- each `errors` item as `Pack config error: ...`;
- each `warnings` item as `Pack warning: ...`;
- `entries: 0` with no errors as `No packs declared`.

When the command yields no JSON (no interpreter, script not found), report that packs could not be resolved and stop; do not guess at pack contents.

## Declare An Existing Source

When the user names a folder or git URL that already holds rules, draft the entry in the shape the guide documents (`source`, plus `ref` for git, optional `path`, `pack`, `id`), show it with the resolved home, the absolute config path, and its exact placement in that file, and write it only on approval. Shared packs belong in `config.yaml`; a machine-local or personal pack belongs in `config.local.yaml`. Create a missing `config.yaml` from `references/config-template.yaml` under the same approval. Run the check afterwards and report the new `pack <id>` line.

## Scaffold A New Pack

**Outcome:** a pack the resolver publishes on the next run: `<home>/compound-packs/<id>/` holding a one-line `README.md` and one first rule at the top level, plus a `packs:` entry pointing at it.

**Safe failure direction:** write nothing rather than write into a folder or config the user has not seen. A target folder that exists and is not empty, a source the config already declares, or a run that cannot ask the user each stop the scaffold with a report of what it would have written.

1. **Resolve the target.** The id is kebab-case ASCII (`a-z`, `0-9`, `-`); it names the folder and appears in every citation. Take it from the request, or ask. The default folder is `<home>/compound-packs/<id>/`; honor another home-relative folder when the user names one.
2. **Draft the two files.** `README.md`: no frontmatter, one line saying what the pack governs. The first rule comes from `assets/pack-rule-template.md`, saved as `<kebab-case of the title>.md` beside the README. When the user described the rule, fill `title`, `applies_when`, `tags`, and the body from that description and route it by the voice/style boundary in `../../references/context-contract.md`; otherwise keep the placeholders, which still publish the pack and show what to replace. Keep the template's layout-reminder paragraph.
3. **Draft the config change.** Append `  - source: compound-packs/<id>` as the last item of the live `packs:` list, matching its indentation. When there is no live key, append a `packs:` block at the end of the file. When `config.yaml` is missing, create it from `references/config-template.yaml` first. Leave every existing line as it is.
4. **Ask once, showing everything.** Preview the resolved home, the folder, both files in full, the absolute config path, and the exact config lines with their placement, then ask whether to write them. Write only on approval. When no question can reach the user, print the preview, say nothing was written, and stop.
5. **Verify.** Run the check above and report the `pack <id>` line. A `Pack config error` or `publishes no packs` line about this pack means the scaffold is not done; fix the cause and check again.
6. **Tell the writer the layout rule** in one sentence: a rule is discovered only when it is a top-level `.md` with `title` and `applies_when`; `README.md` is the description; subfolders and other files are storage. Point at `../../references/packs.md`, "Pack layout".

## Handoff

Report the home, the packs that resolve, any error or warning verbatim, and what was written or skipped. Do not run onboarding or start a draft from here; suggest the next writing step only when the user asked for one.
