# Compound Writing Project Convention

Use this convention when the user explicitly asks to create a new self-contained writing project. Existing project conventions always win unless the user asks to migrate them.

```text
project-name/
├── VOICE.md                  # syntax, diction, and tone
├── STYLE.md                  # argument, evidence, article structure, and publication readiness
├── examples/                 # curated positive and negative exemplars
└── drafts/
    └── piece-slug/
        ├── research.md       # sources, claims, tensions, and provenance
        ├── notes.md          # raw material
        ├── outline.md        # current structure
        ├── draft-version-one.md
        └── review.md         # optional editorial findings
```

## Rules

- Create all four top-level surfaces together through `setup-project`.
- Treat `VOICE.md` as sentence-sound authority and `STYLE.md` as substantive article authority; do not recombine them into `TASTE.md`.
- Route wording, sentence-construction, and tone rules to `VOICE.md`. Route claim, support, organization, and readiness rules to `STYLE.md`. Split mixed feedback.
- Use examples to clarify named rules, not as language to copy.
- Create one piece folder inside `drafts/` and create only the files that piece needs.
- Keep one authoritative research/source file unless the project defines another pattern.
- Preserve links and attribution with the claims they support.
- Use `version one`, `version two`, and so on for draft iterations; avoid `final` and `clean` labels.
- Read before writing and preserve user-authored changes.
- Do not move, rename, archive, or publish artifacts without the approval required by the workspace.
- Do not create `context.md`, `published/`, `.status.yaml`, or another memory system unless the project explicitly needs one.
