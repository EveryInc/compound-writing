---
name: cw-setup-project
description: Create or initialize a durable writing home with VOICE.md, STYLE.md, examples/, and drafts/. Use when Scribe identifies a first-time writer with no established writing context after resolving the target, or when the user explicitly asks to set up, scaffold, initialize, or migrate a self-contained writing folder.
---

# Set Up A Writing Home

Create one portable folder that can travel independently of the plugin and contains the context and working surfaces Compound Writing needs.

## Resolve The Target

- Use the path or folder name the user supplied.
- If the destination is unclear and choosing it would create the writing home in a materially different place, ask for the path.
- Read existing workspace instructions before writing.
- Never create writing-home files inside the installed plugin or runtime cache.

## Create The Writing Home

Create this exact minimum structure:

```text
writing-home/
├── VOICE.md
├── STYLE.md
├── examples/
│   └── README.md
└── drafts/
    └── README.md
```

Run the bundled creator by resolving it relative to this `SKILL.md`; do not assume the user's working directory is the plugin root:

```bash
python3 "<plugin-root>/skills/cw-setup-project/scripts/create_project.py" "/path/to/writing-home"
```

The script copies the canonical templates from `defaults/project-template/`. It may create a new folder or populate an empty folder. It refuses to modify a non-empty folder by default and never overwrites files.

For an existing folder, inspect it first. If the user explicitly wants the Compound Writing structure added, run:

```bash
python3 "<plugin-root>/skills/cw-setup-project/scripts/create_project.py" "/path/to/writing-home" --add-missing
```

`--add-missing` creates only absent items. Preserve every existing file and convention.

## Keep The Split Clear

- `VOICE.md` answers: **How should the sentences sound?** Put syntax, diction, and tone here, including cadence, rhythm, register, punctuation, and verbal tics.
- `STYLE.md` answers: **What must the article do, contain, and prove?** Put argument, evidence, article structure, substantive standards, audience promise, and publication-readiness criteria here.
- `examples/` holds curated positive and negative examples. Examples are evidence for the written rules, not rules by themselves.
- `drafts/` holds one folder per piece: `drafts/<piece-slug>/`. Keep that piece's notes, research, outline, draft versions, and reviews together.

Never put argument, evidence, structure, or publication-readiness rules in `VOICE.md`. Never put word choice, sentence construction, cadence, or tone rules in `STYLE.md`. Split mixed feedback into separate rules.

Do not create `TASTE.md`, `context.md`, `published/`, or `.status.yaml` as part of setup.

## Migrate A Legacy Project

When `TASTE.md` exists:

1. Read it with the existing project instructions.
2. Route syntax, diction, and tone rules to `VOICE.md`.
3. Route argument, evidence, article structure, substantive standards, and publication-readiness rules to `STYLE.md`.
4. Flag rules that mix both layers or conflict with maintained context.
5. Show the migration summary before changing ambiguous or high-authority guidance.
6. Preserve `TASTE.md` until the user explicitly approves its deletion or archival.

## Begin The Guides

After first-run setup, begin `cw-onboarding` so the writer can add a useful first version of both guides from a short conversation, existing writing, or the work already in progress. Do not block use of the writing home on completing either profile.

When the user invoked `cw-setup-project` manually for an additional folder, offer onboarding rather than assuming they want a new profile immediately.

## Handoff

Report the writing-home path, the four created surfaces, anything skipped because it already existed, and the next useful step.
