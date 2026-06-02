# Workspace Files

Compound Writing stores user-specific guidance in the user's project. The
plugin package contains templates only.

## Durable And Provisional Layers

| File | Durable? | What it controls | Example of appropriate content |
| --- | --- | --- | --- |
| `voice.md` | Yes, after approval | Sentence-level choices that apply across destinations. | Prefer dry understatement to forced enthusiasm. |
| `style-guides/x.md` | Yes, after approval | X-specific entry points, length, evidence, and tone. | Lead build posts with the artifact. |
| `style-guides/linkedin.md` | Yes, after approval | LinkedIn-specific professional framing. | Include the professional consequence before the takeaway. |
| `style-guides/longform.md` | Yes, after approval | Longer-form structure and payoff. | Show the failure before extracting a lesson. |
| `strategy/professional-positioning.md` | Yes, after deliberate strategy work | Public territory and reader promise. | Be useful to operators testing AI inside consequential work. |
| `strategy/platform-strategy.md` | Yes, after deliberate strategy work | Jobs assigned to publishing destinations. | X shows receipts; LinkedIn develops professional consequence. |
| `context.md` | No | Current work and provisional observations. | This post's visual artifact made the explanation clearer. |

## Precedence

For an individual task:

1. Safety and product defaults.
2. Approved `voice.md`.
3. Approved guide for the intended destination.
4. Strategy files only when the assignment concerns strategy or public
   adaptation.
5. Provisional `context.md` and source material.
6. The user's instruction for the task.

An immediate user instruction can override ordinary style preferences for a
piece. It does not silently rewrite durable guidance.

## How A Learning Moves

```text
edit or choice -> observation -> context.md -> proposed durable update ->
user approval -> voice, style, or strategy file
```

The system should say what it observed, why it believes the pattern matters,
and which file an approved update would change.

