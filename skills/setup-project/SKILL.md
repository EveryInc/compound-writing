---
name: setup-project
description: Create or initialize one self-contained writing project with VOICE.md, STYLE.md, examples/, and drafts/. Use when the user asks to set up, start, scaffold, initialize, or migrate a Compound Writing project or wants a discrete folder containing its voice rules, structural rules, exemplars, and draft workspace.
---

# Set Up A Writing Project

Create one project folder that can travel independently of the plugin and contains the context and working surfaces Compound Writing needs.

## Resolve The Target

- Use the path or project name the user supplied.
- If the destination is unclear and choosing it would create the project in a materially different place, ask for the path.
- Read existing workspace instructions before writing.
- Never create project files inside the installed plugin or runtime cache.

## Create The Project

Create this exact minimum structure:

```text
project-name/
├── VOICE.md
├── STYLE.md
├── examples/
│   └── README.md
└── drafts/
    └── README.md
```

Run the bundled creator by resolving it relative to this `SKILL.md`; do not assume the user's working directory is the plugin root:

```bash
python3 "<plugin-root>/skills/setup-project/scripts/create_project.py" "/path/to/project-name"
```

The script copies the canonical templates from `defaults/project-template/`. It may create a new folder or populate an empty folder. It refuses to modify a non-empty folder by default and never overwrites files.

For an existing folder, inspect it first. If the user explicitly wants the Compound Writing structure added, run:

```bash
python3 "<plugin-root>/skills/setup-project/scripts/create_project.py" "/path/to/project-name" --add-missing
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

## Offer Onboarding

After setup, offer to use `onboarding` to fill the two guides from a short conversation or existing writing. Do not block project creation on completing the profiles.

## Handoff

Report the project path, the four created surfaces, anything skipped because it already existed, and the next useful step.
