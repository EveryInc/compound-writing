# Changelog

## Unreleased

- Added optional `cw-tune`, which tests and tunes an existing `VOICE.md` against the writer's own pieces for a chosen drafting model (Claude Code, Codex or Antigravity). Pieces are cut into sections so a dozen pieces give dozens of test cases, and each section is drafted from notes for it, as the writer would draft for real. It first reports whether the guides beat no guides at all, then an autoresearch loop proposes edits to `VOICE.md`, scored by an Elo ratchet: a blind voice judge plays each draft against a ladder of every earlier draft of the same section, so the score never maxes out. The tuned `VOICE.md` is proposed for approval with held-out counts, a diff and a list of every rule removed or reworded. `STYLE.md` is never edited. A preflight check catches signed-out CLIs and API-key billing.

## 2.4.1 — 2026-09-15

- Renamed the least-charitable reviewer to `cw-nemesis` throughout the public plugin. Its behavior is unchanged.

## 2.4.0 — 2026-09-12

- Added a blank, optional `AUDIENCE.md` template covering scope, reader situations, knowledge and assumptions, wants and needs, a possible reader journey, resistance and trust, application guidance, and evidence and open questions.
- Added opt-in audience setup with `--with-audience`; existing guides and shared-source pointers are preserved.
- Updated onboarding, Scribe, reader reviews, hooks, promises, theses, and saving preferences to use maintained audience context. The current assignment takes precedence, and missing audience guidance never blocks writing.
- Retained the public 2.3.0 skill set. This release adds no new specialist skills and includes no publication-specific audience profile.
