# Skill Inventory

Skills are the actions a user invokes: set up a workspace, adapt a piece for a
destination, or ask for a specific kind of editorial pressure. This proposed
package includes contracts for the behaviors that change when Compound
Writing becomes portable.

## Included In This Proposal

| A user wants to... | Skills |
| --- | --- |
| Start writing with a small, accurate setup | `onboarding`, `scribe` |
| Move an existing profile to the new file model | `migrate-workspace` |
| Save or test a preference | `save`, `voice-check` |
| Make work fit its destination | `longform`, `x-post`, `linkedin-post` |
| Request one precise editorial lens | `trim`, `tension`, `momentum`, `humor`, `general-reader`, `stress-test`, `story-check` |
| Compare several readings of a draft | `panel`, `debate` |

## Not Yet Ported

The live repository also contains useful generic capabilities such as
brainstorming, interviewing, outlining, developmental editing, line editing,
AI-pattern review, hooks, theses, promises, transitions, analogies, and
simplification. Those can be carried forward once their context-loading
language is updated to this workspace contract.

## Contract For Every Skill

- Load only the user context relevant to the current request.
- Treat `voice.md`, style guides, and strategy as distinct layers.
- Use functional reviewer names instead of named-person imitations.
- Preview durable updates before writing them.
