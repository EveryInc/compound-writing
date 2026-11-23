---
name: cw-voice-check
description: Diagnose whether writing matches the active writer, project, publication, and platform voice context, then offer a closer revision. Use when the user asks whether text sounds like them, feels generic, or has drifted from an established voice.
---

# Voice Check

Evaluate the passage against the voice context that actually governs the assignment.

## Load Voice Context

Read `../../references/context-contract.md`, then follow `../../references/voice-from-examples.md` to read the writer's gold examples and build a voice read before judging the passage.

Use this authority order for voice work:

1. Explicit instructions for the current passage.
2. The `VOICE.md` lessons that govern the writer and project (confirmed corrections).
3. The gold examples in the active project's `examples/` folder, read through the voice read. More specific examples (a publication's or format's) beat the writer's general set.
4. Project, publication, column, or platform `STYLE.md` and more specific guides, for anything they say about the format.
5. Legacy `TASTE.md`, only when the project still maintains it.
6. Plugin defaults only when no gold examples exist, and say so.

Name the examples and lessons used. Do not treat plugin defaults as the writer's identity.

Run the counter with `--compare` on the passage when it is long enough to measure (a few hundred words or more): `scripts/voice_stats.py` in this skill's folder.

## Diagnose

Compare the passage with the gold examples, not with a description of them. For each item, quote the passage and a matching or contrasting line from an example. Check for:

- sentence openings, construction, length mix, and where short sentences land;
- paragraph cadence and how paragraphs end;
- features the counter puts outside the examples' range;
- things the passage does that the examples never do;
- sentence architecture and cadence;
- diction and register;
- specificity, scenes, examples, and stakes;
- humor, vulnerability, priors, and distinctive asides;
- publication or platform fit;
- smoothing, generic symmetry, scaffolding, and other AI residue;
- sentences lifted from a gold example rather than written to its patterns.

Preserve intentional rule-breaking when it carries the writer's point of view.
Match the examples' patterns, not their sentences or subject matter.

## Output

Provide:

1. **Voice sources used** — the gold examples read, the lessons applied, and any supplied instructions.
2. **Aligned** — the strongest specific matches, each beside the example line it matches.
3. **Drift** — the few highest-impact mismatches, quoted precisely, each beside the example pattern it departs from, with counter figures where they help.
4. **Closer revision** — a usable rewrite that preserves meaning and authorship.
5. **Judgment call** — any tension between writer voice and publication/platform constraints.

Do not turn the result into a generic style checklist. The test is whether this piece sounds like the writer's gold examples in this context.

If a drift recurs and the examples do not show the right move, suggest saving it as a lesson with `cw-save`, or adding an example that shows it.
