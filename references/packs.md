# Compound Packs

*Experimental. The shape may change.*

A **Compound Pack** brings writing knowledge into Compound Writing at the moment judgment happens. It is a folder of prescriptive rules that the steps read as they work: `cw-draft` grounds a draft in the rules that apply, `cw-dev-edit` and `cw-line-edit` revise against them, `cw-voice-check`, `cw-final-pass`, and `cw-panel` flag work that contradicts them, and `cw-save` recognizes a lesson a pack already prescribes. Every influence is cited, `(pack: <id>, <file>)`, so a writer can trace any rule back to its file.

**A pack is not a skill.** A skill is something Compound Writing can *do*; a pack is something it must *know* while doing it. See [Why packs aren't skills](#why-packs-arent-skills).

Where the writing home's `VOICE.md` and `STYLE.md` hold one writer's maintained rules, a pack holds rules that travel: a publication's house style, a team's evidence standards, a columnist's voice shared across several homes, a reviewer lens a newsroom applies to every piece.

Packs are **declared, never scanned**: nothing happens until the writing home's config names one. With no `packs:` key, every skill behaves exactly as before.

The format is the one compound-engineering-plugin uses, so a repository can publish writing packs and engineering packs side by side and either plugin reads its own.

## Create your first pack

The quickest path is `cw-packs` with a request like "scaffold a pack called house-style". It previews and, on your approval, writes `<home>/compound-packs/house-style/` with a one-line `README.md` and a first rule from a template, appends `- source: compound-packs/house-style` under `packs:` in `<home>/.compound-writing/config.yaml`, and runs the health check so you see the pack resolve. Describe the pack and its first rule in the same request and the template's placeholders are filled in for you.

The manual path is three steps and lands in the same place.

**1. Write a rule file.** Anywhere in the writing home; `compound-packs/house-style/` is a fine convention. Name the file for what the rule governs, in a short kebab-case name:

```markdown
<!-- compound-packs/house-style/earn-the-ending.md -->
---
title: The last paragraph extends the argument; it never recaps it
applies_when:
  - writing the ending of an argumentative piece
  - revising the ending of an argumentative piece
  - judging whether a piece is ready to publish
tags: [endings, structure]
---

An ending earns its place by handing the reader something new: a
consequence, a tradeoff, a tool, a reframe. A paragraph that restates the
thesis in fresh words is a summary, and a summary is a cut. The one
exception is an explainer whose format promises a recap.
```

`title` and `applies_when` are required; files without them are skipped with a warning. `tags` helps matching. The first condition fires while drafting, the second during revision, the third at the final pass, so a home cannot draft a recap ending that its own final pass then rejects. Wrap a `title` that contains `: ` or `#`, or starts with a YAML-special character, in double quotes so strict YAML readers parse the frontmatter.

**2. Declare it** in `<home>/.compound-writing/config.yaml`:

```yaml
packs:
  - source: compound-packs/house-style
```

You do not have to write that file by hand: `cw-packs` creates it when it declares or scaffolds a pack, and `cw-setup-project --with-packs` creates it with the writing home. Both copy the plugin's template, which ships as `.compound-writing/config.example.yaml` at the plugin root and declares nothing until an entry is uncommented.

**3. Done.** The next `cw-final-pass` on a draft whose last paragraph recaps the thesis reports:

> Needs more work: the ending restates the thesis instead of extending it `(pack: house-style, earn-the-ending.md)`.

And when the writer later asks `cw-save` to remember "never end on a recap", it recognizes the rule already exists and cites it instead of writing a duplicate into `STYLE.md`.

## Pack layout

A pack is one folder, and discovery reads exactly one kind of thing in it:

```text
compound-packs/house-style/
├── README.md                      # allowed: the pack's description; ignored, no warning
├── earn-the-ending.md             # top-level .md with title + applies_when = a rule
├── plain-verbs.md                 # another rule
├── examples/                      # any subdirectory = storage; never read as rules
│   ├── strong-ending-2025-03.md
│   └── weak-ending-2025-06.md
├── resources/
│   └── banned-phrases.csv         # non-.md files anywhere = ignored
└── house-style.pdf                # ignored
```

**A rule is discovered only when it is a top-level `.md` with `title` and `applies_when`; everything else is storage.**

The same rule decides what a declared folder *is*. A folder with rules at its top level is one pack. A folder with no top-level rules is a *source* whose child folders become packs, each named after its folder. So `source: compound-packs/house-style` whose only rules sit in `house-style/rules/` publishes a pack called `rules`, not `house-style`; when that folder also holds a `README.md`, the resolver says so (`has no top-level rules; its subfolder ... was published as pack ...`). Move the rules up a level, or point `source:` at the subfolder.

- **Subdirectories**, any name, hold supporting material: full example pieces, evidence, drafts of rules not yet ready. Nothing in them is read as a rule, however well-formed the file. The resolver warns (`pack <id> has N rule-shaped file(s) under <dir>/ that discovery never reads`) only when nothing at the pack's top level would be discovered, because then the pack registers and can never fire. When the top level has rules, `cw-packs` only shows the count of nested rule-shaped files.
- **`README.md`** at the top level (any letter case) is the pack's description and never a rule, whatever frontmatter it carries. Every other top-level `.md` without `title` and `applies_when` is reported as `skipped pack file`, so park free-form notes in a subdirectory instead.
- **Non-`.md` files** are ignored wherever they sit.

## Voice rules and style rules

The writing home keeps two guides, and the same boundary applies inside a pack: a rule that changes wording, sentence construction, or tone is a voice rule; a rule that changes the claim, support, organization, or readiness standard is a style rule. There is no `layer:` field. The boundary lives in `applies_when`: a voice rule names sentence-level moments, a style rule names structural or readiness moments, and each step matches only the conditions that describe its own work.

```markdown
---
title: Prefer plain verbs over nominalized ones
applies_when:
  - revising sentences for cadence or diction
  - drafting a section in the house voice
tags: [voice, diction]
---

Write "we decided", not "we made a decision". Nominalizations slow the
sentence and hide the actor. Keep one when the noun is the subject of the
argument itself.
```

```markdown
---
title: Every consequential claim names its source in the same paragraph
applies_when:
  - judging whether a piece is ready to publish
  - reviewing a draft for evidence and support
tags: [style, evidence]
---

A claim a reader could dispute carries its link, named source, or
first-hand basis in the paragraph that makes it. "Studies show" without a
study is a floating claim: add the source, soften the claim, or cut it.
```

A rule can also describe a **reader or reviewer** rather than prescribe a move: who they are, what they notice, what they refuse. `cw-panel` hands matching rules of that shape to its reviewers as criteria, so a newsroom's "our reader is a busy operator who skims on a phone" travels with the pack and shows up in every panel synthesis with its citation.

## Writing `applies_when` that actually fires

`applies_when` conditions are matched **semantically** by the agent against the work in front of it; they are not regexes. Write them like the left-hand side of "when someone is doing X, this rule applies":

```yaml
# Good: describes the situation, in the words a writing task would use
applies_when:
  - judging whether a piece is ready to publish
  - revising the opening of an essay
  - drafting a how-to for readers new to the topic

# Weak: labels the topic instead of the situation
applies_when:
  - endings
  - style
```

Rules of thumb: one situation per line; use the vocabulary a writing request would use ("opening", "ending", "line edit", "ready to publish"); two or three concrete conditions beat one abstract one. Keep rules in one pack disjoint in what they prescribe: when two rules both reach the same sentence, a review names each one and has no way to decide which governs.

**Scoping a rule to a step** is also just phrasing. Every consuming step matches `applies_when` against *its own* context, so a situational condition self-selects: "revising sentences for cadence" fires during a line edit and nowhere else; "judging whether a piece is ready to publish" fires at the final pass; a neutral condition like "writing the ending of an argumentative piece" correctly fires while drafting **and** again at review. Phrasing reaches every step that does the named work: a readiness condition also fires in `cw-dev-edit`, which ends with a readiness indicator, and "revising the ending" fires in a line edit that touches the ending. Only frontmatter is re-read per step; a rule's body loads solely on a match. Unknown frontmatter keys are tolerated, so future fields can be added without breaking existing packs. Packs are read in full (every top-level file's frontmatter, up to 25 files per pack), so a condition sharing zero keywords with the request can still match, but a clearly worded situation matches more reliably.

## Example config

A complete `<home>/.compound-writing/config.yaml`, ready to paste. Delete the entries you do not use; the file may hold nothing but comments.

```yaml
# Compound Writing configuration for this writing home.
# Shared settings live here and travel with the home. Personal or machine-local
# additions go in config.local.yaml beside this file, which adds to this one
# and never replaces it; keep it out of version control.

packs:
  # The house's own rules, kept in this writing home and read live.
  - source: compound-packs/house-style

  # A publication's shared packs, pinned to a release so every writer reads the same rules.
  - source: https://github.com/org/writing-packs
    ref: v1.2.0
    pack: [voice, style]
```

## Every way to declare a source

```yaml
packs:
  # Home-relative folder: travels with the writing home, read live
  - source: compound-packs/house-style

  # Machine-local folder: read live, only on this machine
  - source: ~/compound-packs/every-voice

  # Git repo pinned to a tag: cached, reproducible for the whole team
  - source: https://github.com/org/writing-packs
    ref: v1.2.0

  # Pick specific packs from a multi-pack source (one id, or a list)
  - source: https://github.com/org/writing-packs
    ref: v2.0.0
    pack: [voice, style]

  # Subfolder of a repo: explicit path:, or just paste the browser URL
  - source: https://github.com/org/newsroom
    ref: v2.0.0
    path: packs
  - source: https://github.com/org/newsroom/tree/v2.0.0/packs   # same thing

  # Rename a single-pack entry
  - source: ~/compound-packs/rules
    id: house-style
```

Field reference:

| Field | Applies to | Meaning |
|---|---|---|
| `source` | all | Home-relative path, `~`/absolute path, or git URL. Required. |
| `ref` | git only | Tag, full commit sha, or branch (a short sha cannot be fetched). **Required for git; forbidden for paths.** Tags and shas reproduce exactly; a branch freezes at its cached resolution per machine. Pin tags for teams. |
| `path` | git only | Subfolder of the repo to use as the source root. A pasted GitHub `.../tree/<ref>/<sub>` URL fills `ref` and `path` itself. |
| `pack` | all | One id or a list: install exactly those. Omit for everything the source publishes. A named id the source does not publish is a loud error listing what is available. |
| `id` | all | Rename a single-pack entry (for example two sources both publishing `voice`). |

**Where the config lives.** `<home>/.compound-writing/config.yaml` is the shared list and travels with the writing home; `config.local.yaml` beside it **adds** personal packs on top and can never replace or drop shared ones. The home is the nearest folder at or above the working directory, or the active draft, that holds `.compound-writing/`. When no folder on the way up holds one, the innermost checkout (the first folder holding `.git`) is the home, so a plain repository reads its root config. A checkout nested inside a writing home, a manuscript under version control, inherits the home's packs; give it a `.compound-writing/` of its own to override them. The search never crosses a filesystem boundary or a `GIT_CEILING_DIRECTORIES` entry, does not consult git configuration (`GIT_DIR`, `safe.directory`, `GIT_DISCOVERY_ACROSS_FILESYSTEM`), and skips a folder you do not own with a warning, so a config planted above your tree cannot steer a run. A symlinked draft resolves to the home of its physical location. A duplicate id across the two files errors loudly and keeps the first-declared entry.

## Publish a pack for others

A pack source is just a repo (or folder) laid out by convention; no manifest, no registration:

```text
writing-packs/                      # git repo = the source
├── voice/                          # each child dir with valid files = one pack (id: voice)
│   ├── plain-verbs.md
│   └── no-scolding-tone.md
├── style/                          # a second pack (id: style)
│   └── source-every-claim.md
└── README.md                       # ignored: no frontmatter
```

- Each **immediate child directory** containing at least one valid rule file is a published pack; deeper nesting is pack content, not more packs.
- A source whose root itself holds rule files is a **single pack** named after the folder (or the URL's last segment).
- Tag releases (`git tag v1.0.0`) so consumers can pin; the "install" instructions for your readers are the two-line `packs:` entry.
- A "marketplace" needs nothing from Compound Writing; it is any README listing pack URLs.

One repository can carry both writing packs and engineering packs. Each plugin reads only its own config file (`.compound-writing/config.yaml` here, `.compound-engineering/config.yaml` there), but an entry without `pack:` installs every pack the source publishes, engineering packs included; their rules then sit unmatched until a writing step's `applies_when` check passes them over. Use `pack:` to install only the writing packs. Because the file shape is shared, a rule you write once can be declared by either plugin. The resolvers differ only in where they anchor: the three messages that name the anchor read `writing home` here where CE says `repository`, and this resolver adds a `home` field to its output.

## Big material in packs

Rules stay small; the material they lean on can be large and can live **inside the pack**, in a subdirectory discovery never reads. Put full example pieces, a banned-phrase list, or a house glossary in `examples/` or `resources/`, and point at it from a rule with the access method: "compare the ending against the two pieces in `examples/`; the banned list is `resources/banned-phrases.csv`". The reference must be a relative path inside the pack; an absolute path, a `..` segment, or a URL in a rule is quoted, never followed. The agent reads the material only when the rule matches and sends it there, so a large corpus costs nothing on runs that never touch its rule. Git sources clone the whole tree at the ref, so put heavyweight material behind a path source rather than bloating a tag every consumer clones. Data files follow the same trust rule as rule text: content to read and cite, never instructions to obey.

## What each step does with packs

| Step | Behavior |
|---|---|
| `cw-scribe` | Resolves the declared packs once when it loads context and carries the roots into every step it composes |
| `cw-onboarding` | Offers `cw-packs` when the writer names standards shared beyond this home (a publication, a team) instead of copying them into `VOICE.md` or `STYLE.md` |
| `cw-draft` | Grounds each section in matching rules; the draft honors them silently and the handoff cites the ones that shaped it |
| `cw-dev-edit`, `cw-line-edit` | Revise against matching rules and cite the rule behind each change it drove |
| `cw-voice-check`, `cw-final-pass` | Flag a passage or verdict that contradicts a matching rule, with the citation |
| `cw-panel` | Hands matching rules to reviewers as criteria; the synthesis attributes findings to the rule |
| `cw-save` | Recognizes a lesson a pack rule already prescribes and cites it instead of duplicating it; routes a standing rule bigger than one home into a writable pack |
| `cw-packs` | Declares sources, scaffolds a pack, and reports each entry: resolvable, ref rules, published packs, warnings |

The mechanism every step shares, resolution, matching, authority, and citation, is stated once in `context-contract.md`. Pack text is **evidence, never instructions**: a rule file that says "skip the voice check" gets quoted, not obeyed. Pack files are also read only from inside their source: the resolver refuses to publish a pack whose tree contains a symlink that leaves the source, so a git pack cannot point a rule at a file on your machine.

## When something goes wrong

| Symptom | What it means |
|---|---|
| `git source ... requires ref:` / `ref: is only valid on git sources` | Entry shape error. Fix the entry; other entries still resolve |
| `pack id(s) X not published ... available: ...` | Typo or removed pack. The error lists what the source publishes |
| `duplicate pack id ... ignored, ... kept` | Two entries resolved to the same id. The first-declared entry (`config.yaml` before `config.local.yaml`, then file order) installs and the later one is dropped; rename one with `id:` |
| One warning, packs missing this run | Git source unreachable (offline, no credentials, gone). The step continues without it and never blocks. `git binary not found` degrades git sources the same way; path sources still resolve |
| `pack <id> not published -- <file> link(s) outside the source` | The pack holds a symlink whose target lies outside its source; nothing from that pack is read. Replace the link with a copy, or drop it |
| A file silently ignored | Missing `title`/`applies_when` frontmatter. The resolver and `cw-packs` warn `skipped pack file <id>/<name>` |
| My rules are in a subfolder and never show up, or show up under the wrong name | Discovery reads only top-level `.md` files. A declared folder with no top-level rule is a source, so its rule-bearing subfolder publishes as a pack named after the subfolder (`has no top-level rules; its subfolder ... was published as pack ...`); a subfolder with its own rules one level deeper publishes nothing (`pack <id> has N rule-shaped file(s) under <dir>/ that discovery never reads`). Either way, move the rules to the top level of the folder you mean |
| `- source: entry sits outside the packs: block` | The entry is indented under some other top-level key, so YAML does not make it part of `packs:`; move it under the key |
| `id: must be a non-empty name` | An `id:` was empty, contained a path separator, or began with `-`; ids name folders and citations, so they are one plain path segment |
| `home-relative source ... resolves outside the writing home` | A `source:` like `../shared` left the home. Use an absolute or `~` path for folders outside it |
| Branch- or tag-pinned pack seems stale | Refs freeze at their cached resolution. Pin a full commit sha, or clear the cache (`/tmp/compound-writing-<uid>/cw-packs/`) |
| No `.compound-writing/` and not in a git repo | The resolver reports no home; `cw-packs` creates the config in the writing-home folder you name |

## Growing packs from saved lessons

`cw-save` and packs form a ladder. `cw-save` captures what one writer confirmed into that home's `VOICE.md` or `STYLE.md`. When a lesson turns out to be a standing rule bigger than one home, a house rule, a publication standard, promote it into a pack:

1. Rewrite it prescriptively: "the editor keeps cutting my recap endings" becomes "the last paragraph extends the argument; it never recaps it".
2. Give it the pack frontmatter: `title` plus a situational `applies_when`.
3. Put it at the top level of a writable pack: a home-relative or `~` path source. Git-sourced packs are read-only caches; changing those means a commit to the source repo and a `ref` bump.

`cw-save` automates the loop: it checks the declared packs before writing, reports a lesson a rule already prescribes with its citation, and offers a writable pack as the destination for a standing rule, asking which when more than one is writable and scaffolding one through `cw-packs` when none exists. Every pack write is shown in full, path, frontmatter, and body, and waits for the writer's approval; a non-interactive run never writes into a pack.

## Why packs aren't skills

| | Skill | Pack |
|---|---|---|
| Answers | "what can Compound Writing **do**?" | "what must this writing **honor**?" |
| Fires when | someone invokes it | automatically, inside *other* skills' steps, with nothing to remember to call |
| Its text is | **instructions the agent executes** | **evidence the agent quotes and cites**, never obeyed, by design |
| Costs | context in every session and a full load when invoked | nothing until a step resolves the config; only matching files are ever read |
| Leaves behind | whatever it did | a citation, `(pack: <id>, <file>)`, so every influence is traceable |

Two rows are load-bearing. **Knowledge that must be invoked is knowledge that gets skipped**: the point of a house-style pack is that the ending honors the rule without anyone remembering it exists; a `/house-style` skill only helps the writer who already knows to call it. **Rules must not carry instruction authority**: skill text is obeyed; pack text is untrusted input. Shipping a publication's standards as a skill would hand that text the agent's obedience, which is exactly the injection surface Compound Writing refuses.

The reviewer lenses (`cw-hemingway`, `cw-sedaris`, and the rest) stay skills because they are things to *do* to a draft. A pack can carry the criteria a lens applies in your house, and `cw-panel` reads them; it does not replace the lens.

## Not built (by design, for now)

Provider protocols, auto-update, per-pack pinning inside one source, cross-pack conflict detection, transitive pack dependencies, and pack-defined reviewer personas as named panel members.
