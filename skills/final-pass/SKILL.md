---
name: final-pass
description: Run a publication-readiness check on a nearly complete piece and deliver a clear ready, almost-ready, or needs-work verdict. Use when the user asks for a final pass, quality gate, or pre-publication check.
---

# Final Pass

## Purpose

The final quality check before publishing. This is the last look before it ships.

Read `../../references/context-contract.md` and load the relevant project, publication, platform, source, and destination requirements before judging readiness.

Do not interpret a passing verdict as permission to publish, send, schedule, or move files.

## What to Check

### Content Quality
Questions to consider (weight by piece type):
- Does the piece deliver on its promise?
- Is the thesis clear and supported?
- Do the sections earn their place?
- Are stakes visible?
- Is there a clear transformation or takeaway?
- **Evidence check** — every major claim backed by experience, named source, or specific example? Any floating assertions?
- **Provenance check** — citations, links, quotes, and attribution still support the claims they are attached to? Any model-added assumption presented as sourced fact?
- **20-second pitch** — can the piece be explained in 20 seconds, and does that explanation match the intro's stated thesis/promise?

### Surface Polish
- Typos and spelling
- Punctuation consistency
- Formatting consistency
- Awkward phrasing

### Speed-Read Test

Read only:
- Headline
- First two sentences
- Subheads
- First sentence of each section
- Conclusion

Does it still make sense and compel? A skim-reader should:
- Feel the problem quickly
- Want the answer
- Understand what they'll gain

### The 20-Second Pitch Test

Generate a 20-second pitch of the piece (what it actually argues, end to end). Pull the thesis/promise from the intro as stated. Compare them.

If they don't match, the intro drifted — usually because the piece evolved during revision and the opening didn't catch up. Flag it before publishing. The fix is almost always rewriting the intro to match where the piece actually lands.

## Output

### Assessment Options

**Full verdict (default):**
```
## ✅ Ready

What's working:
- [Strength #1]
- [Strength #2]
- [Strength #3]

Ship it.
```

or

```
## ⚠️ Almost Ready

Minor issues to consider:
1. [Issue] — [Quick explanation]

These won't break the piece, but fixing them would help.
Fix them, or ship as-is?
```

or

```
## ❌ Needs More Work

Issues that should be addressed:
1. **[Issue #1]** — [Why it matters]
2. **[Issue #2]** — [Why it matters]

Want to fix these together?
```

**Quick check (for fast turnaround):**
```
## Quick Final Check

✅ Content delivers on promise
✅ Surface polish clean
⚠️ One note: [minor issue]

Ready to ship.
```

## Your Judgment

**Pass/fail is a recommendation, not a gate.** The writer decides when to publish. Your job is to surface anything they might have missed and give them confidence (or appropriate caution).

- Some pieces are ready with minor imperfections
- Some writers want perfection; others want "good enough"
- Context matters: blog post vs. flagship article vs. quick take

## Collaborative Fixing

If there are issues:
1. List them clearly
2. Offer: "Want to fix these together?"
3. Work through collaboratively
4. Re-check if requested

**Don't force multiple passes.** One thorough check is usually enough.

## For Agents

When invoked programmatically:
- Accept draft as input
- Return pass/fail assessment with reasoning
- Include list of any issues found
- Can be composed with other quality checks (ai-check, voice-check)

## Lessons

[Skill-specific lessons will be added here as they're captured]
