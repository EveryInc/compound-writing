# Compound Writing Home Convention

Use this convention when first-run Scribe has confirmed that the writer has no established writing context and resolved a target folder, or when the user explicitly asks to create a self-contained writing folder. Existing workspace conventions always win unless the user asks to migrate them.

```text
writing-home/
├── VOICE.md                  # confirmed lessons on syntax, diction, and tone
├── STYLE.md                  # argument, evidence, article structure, and publication readiness
├── examples/                 # gold examples: the source of the voice (counterexamples in negative/)
└── drafts/
    └── piece-slug/
        ├── research.md       # sources, claims, tensions, and provenance
        ├── notes.md          # raw material
        ├── outline.md        # current structure
        ├── draft-version-one.md
        └── review.md         # optional editorial findings
```

## Rules

- Create all four top-level surfaces together through `cw-setup-project`.
- Treat the gold examples (read through `references/voice-from-examples.md`) plus `VOICE.md` lessons as sentence-sound authority and `STYLE.md` as substantive article authority; do not recombine them into `TASTE.md`.
- Route wording, sentence-construction, and tone rules to `VOICE.md`. Route claim, support, organization, and readiness rules to `STYLE.md`. Split mixed feedback.
- Learn the voice from the gold examples; copy their patterns, not their sentences.
- Create one piece folder inside `drafts/` and create only the files that piece needs.
- Keep one authoritative research/source file unless the workspace defines another pattern.
- Preserve links and attribution with the claims they support.
- Use `version one`, `version two`, and so on for draft iterations; avoid `final` and `clean` labels.
- Read before writing and preserve user-authored changes.
- Do not move, rename, archive, or publish artifacts without the approval required by the workspace.
- Do not create `context.md`, `published/`, `.status.yaml`, or another memory system unless the workspace explicitly needs one.
