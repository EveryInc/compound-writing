---
name: cw-help
description: Explain how to use Compound Writing and route the user to the right workflow.
---

# Compound Writing Help

Compound Writing loads the context that already governs the work, then routes to the smallest useful writing workflow.

Use `cw-scribe` when you want help starting, continuing, finishing, or improving a piece without choosing a skill first. The full toolbox is installed; `cw-scribe` keeps the user from having to learn it all before beginning.

On a first meaningful interaction, `cw-scribe` checks for a draft, active workspace, and useful writing context. If none exists, it briefly explains one writing home, asks where it should live, creates `VOICE.md`, `STYLE.md`, `examples/`, and `drafts/`, and helps begin the first two guides. If useful work is already in front of it, it starts there without making setup a gate.

You do not need to know the setup or onboarding tools by name. Use `cw-setup-project` directly only when you explicitly want to create or migrate a self-contained writing folder yourself.

## Common Routes

| You have | Start with |
|---|---|
| No writing home or useful starting context yet | `cw-scribe` |
| No idea | `cw-brainstorm` |
| A live idea | `cw-interview` |
| Notes or source material | `cw-outline` |
| An outline or partial draft | `cw-draft` |
| A buried, slow, or misleading opening | `cw-bluf` |
| A structurally weak draft | `cw-dev-edit` |
| Stable structure and rough prose | `cw-line-edit` |
| Generic or machine-smoothed copy | `cw-voice-check`, `cw-ai-check`, or `cw-tracks` |
| A fresh-eyes or first-time-reader check | `cw-reader` |
| A nearly publishable piece | `cw-final-pass` |
| A high-stakes piece | `cw-objections`, `cw-panel`, or `cw-debate` |

The classic flow is available but optional:

```text
cw-brainstorm -> cw-interview -> cw-outline -> cw-draft -> cw-dev-edit -> cw-line-edit -> cw-final-pass
```

Publication, workspace, and format standards come from the active `STYLE.md`, brief, template, or maintained workflow.

Use `cw-save` to turn a confirmed preference or recurring lesson into maintained context.

Ask "Show me the Compound Writing toolbox" for the complete tool catalog and one-line descriptions.
