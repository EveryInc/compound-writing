# Changelog

## Unreleased

- Added optional `cw-tune`, which tests and tunes an existing `VOICE.md` and `STYLE.md` against the writer's own pieces for a chosen drafting model (Claude Code, Codex or Antigravity). It first reports whether the guides beat no guides at all, then an autoresearch loop proposes edits to each file within the voice/style boundary, scored by an Elo ratchet: a blind judge plays each draft against a ladder of every earlier draft of the same piece, so the score never maxes out. The tuned guides are proposed for approval with held-out counts, a diff and a list of every rule removed or reworded. Drafts are written from notes for each piece, as the writer would draft for real, and a preflight check catches signed-out CLIs and API-key billing. Runs live in a visible `tuning/` folder in the writing home.

## 2.4.1 — 2026-09-15

- Renamed the least-charitable reviewer to `cw-nemesis` throughout the public plugin. Its behavior is unchanged.

## 2.4.0 — 2026-09-12

- Added a blank, optional `AUDIENCE.md` template covering scope, reader situations, knowledge and assumptions, wants and needs, a possible reader journey, resistance and trust, application guidance, and evidence and open questions.
- Added opt-in audience setup with `--with-audience`; existing guides and shared-source pointers are preserved.
- Updated onboarding, Scribe, reader reviews, hooks, promises, theses, and saving preferences to use maintained audience context. The current assignment takes precedence, and missing audience guidance never blocks writing.
- Retained the public 2.3.0 skill set. This release adds no new specialist skills and includes no publication-specific audience profile.
