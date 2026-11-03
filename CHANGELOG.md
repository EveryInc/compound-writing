# Changelog

## Unreleased

- Added optional `cw-tune`, which tests and tunes an existing `VOICE.md` and `STYLE.md` against the writer's own pieces for a chosen drafting model (Claude Code, Codex or Antigravity). A blind judge compares drafts with the real pieces, an autoresearch loop proposes edits to each file within the voice/style boundary, and the tuned guides are proposed for approval with a held-out score and a diff. Runs live in a visible `tuning/` folder in the writing home.

## 2.4.1 — 2026-09-15

- Renamed the least-charitable reviewer to `cw-nemesis` throughout the public plugin. Its behavior is unchanged.

## 2.4.0 — 2026-09-12

- Added a blank, optional `AUDIENCE.md` template covering scope, reader situations, knowledge and assumptions, wants and needs, a possible reader journey, resistance and trust, application guidance, and evidence and open questions.
- Added opt-in audience setup with `--with-audience`; existing guides and shared-source pointers are preserved.
- Updated onboarding, Scribe, reader reviews, hooks, promises, theses, and saving preferences to use maintained audience context. The current assignment takes precedence, and missing audience guidance never blocks writing.
- Retained the public 2.3.0 skill set. This release adds no new specialist skills and includes no publication-specific audience profile.
