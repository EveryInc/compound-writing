# Getting Started

Compound Writing works inside a writing-project folder that you control. The
plugin supplies workflow and blank templates; your project stores your voice
and publishing guidance.

## Fastest First Run

1. Open the project folder where you want to write.
2. Run `/onboarding`.
3. Answer the voice questions conversationally.
4. Review the proposed `voice.md`.
5. Approve the file or revise it.
6. Choose whether to create a style guide for the destination you need now.
7. Start the actual piece through `/scribe`, `/longform`, `/x-post`, or
   `/linkedin-post`.

You do not need to set up every file on day one. For most users the smallest
useful start is:

```text
your-writing-project/
|-- voice.md
`-- style-guides/
    `-- {the destination you need now}.md
```

## Three Setup Paths

| Your situation | Start with | Result |
| --- | --- | --- |
| You want to write a specific piece now. | `/onboarding`, then the current destination guide. | A small voice profile and one relevant guide. |
| You are building a public writing practice across platforms. | `/onboarding`, then optional strategy setup. | Voice, current destination guides, and deliberate positioning files. |
| You used an earlier Compound Writing workspace with `TASTE.md`. | `/migrate-workspace`. | A previewed, user-approved split with legacy fallback preserved. |

## What Onboarding Will Ask

Onboarding asks only enough to improve immediate work:

- What are you writing now, and for whom?
- How should your writing feel?
- What sentence rhythm, register, specificity, or humor should persist across
  formats?
- What should the system avoid?
- What destination are you writing for now, if known?

It does not require a public brand strategy, ask you to imitate a named
writer, or claim to know your voice before you approve it.

## What Gets Written

| File | Created when | Purpose |
| --- | --- | --- |
| `voice.md` | First onboarding, after approval. | Stable cross-format voice preferences. |
| `style-guides/longform.md`, `x.md`, or `linkedin.md` | When the current destination needs one, after approval. | Format- and audience-specific behavior. |
| `strategy/*.md` | Only when you request positioning or platform strategy work. | Public territory and publishing decisions. |
| `context.md` | Once there is current work or a provisional learning worth tracking. | Non-durable working memory. |

## Privacy And Control

- Files are created in your working project, not in the plugin.
- You see proposed durable guidance before it is written.
- Observed behavior is not automatically turned into voice or strategy.
- Existing profiles are not deleted or moved during migration.

## Try It

After onboarding:

```text
/x-post Turn this result into one post with a concrete receipt.
```

```text
/linkedin-post Help me explain the professional implication of this experiment.
```

```text
/longform Outline an essay from these notes.
```

