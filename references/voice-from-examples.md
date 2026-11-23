# Voice From Gold Examples

Use this procedure whenever a Compound Writing skill needs to know how the writer's sentences sound: drafting, line editing, voice checks, AI-residue cleanup, hooks, transitions, or any rewrite that will carry the writer's name.

In this edition, the writer's gold examples are the authority for sentence- and word-level voice. `VOICE.md` does not describe the voice. It holds only lessons the writer has confirmed that the examples did not already teach. Read the examples, work out what the sentences actually do, and write to that.

## 1. Find The Gold Set

- Look in the active writing home's or project's `examples/` folder, or the examples location its instructions name.
- Every piece in `examples/` is gold unless it sits in `examples/negative/` or its file name contains `negative`. Negative examples are counterexamples: use them only to see what to avoid, never to infer the voice.
- The writer may name specific examples for an assignment ("use the two newsletter pieces"). Their choice wins.
- If no gold examples exist, say so plainly. Ask for three to five pieces the writer thinks sound most like them, in the format they are about to write. If the work cannot wait, continue with the `VOICE.md` lessons and plugin defaults and label the result **not calibrated to examples**.

## 2. Choose What To Read

- Read every gold example when the set is small enough to hold comfortably (roughly 25,000 words or fewer).
- For a larger set, read the examples closest to the assignment in format, platform, length, and register. Read at least three, and name the ones you used.
- When no gold example matches the assignment's format (a tweet thread from essay examples, say), say so. Carry over sentence- and word-level habits; do not carry over length, paragraphing, or structure that belong to the other format.

## 3. Measure The Surface

Run the bundled counter on the gold set, resolving the path relative to the plugin root:

```bash
python3 "<plugin-root>/skills/cw-voice-check/scripts/voice_stats.py" "/path/to/examples"
```

It reports sentence and paragraph length, punctuation rates, contractions, pronouns, sentence openers, frequent words, and how often common machine connectors appear. It reports each figure as a range across the examples.

The numbers are a check on your reading, not the voice. Use them to catch drift you would otherwise rationalize: three times the writer's dash rate, uniform sentence lengths, paragraphs twice as long. If the script cannot run, estimate the same figures by hand from a sample of paragraphs.

## 4. Read For Patterns

Read the examples as a writer studying another writer's sentences. Build a **voice read**: a short working list of instructions drawn from the examples. Cover:

- **Sentence openings:** what the first words usually are (subject, conjunction, a clause, a time marker, "I"), and how often a sentence starts with "And," "But," or "So."
- **Sentence construction:** how sentences are built: accumulating, interrupted, compressed, list-like, qualified mid-stream. Where the stress falls at the end.
- **Length and placement:** the mix of short and long, and where the short ones land (after a build, at a paragraph's end, as a turn).
- **Paragraph cadence:** how paragraphs open and close; how often a paragraph is a single sentence; what the last sentence of a paragraph tends to do.
- **Verbs and nouns:** the kinds of verbs (plain, physical, technical, borrowed slang) and how concrete the nouns are.
- **Register mixing:** where a technical word sits beside a casual one, profanity, slang, or a formal word used for effect.
- **Hedges and intensifiers:** which ones the writer actually uses, and how often. Some writers hedge on purpose; do not strip what the examples show.
- **Pronouns and address:** I, you, we; how directly the reader is addressed.
- **Punctuation as voice:** dashes, parentheses, colons, semicolons, questions, italics, fragments, and their rough rate.
- **Turns:** how the writer qualifies, contradicts themselves, undercuts a claim, makes a joke, or takes an aside, at sentence level.
- **Recurring words and phrasings:** words that turn up across several examples.
- **Absences:** things that never appear in the gold set: certain connectors, exclamation points, rhetorical triplets, a particular register. An absence across many examples is as strong a signal as a presence.

Rules for the read:

- Write each item as an instruction an editor could follow ("End the paragraph on the short concrete sentence, not on a summary"), not an adjective ("punchy").
- Back each item with at least two short quoted instances from at least two different examples, with the file name. One instance is a note, not a pattern.
- Record rates where they matter ("about one dash every 150 words"; "roughly a third of paragraphs are one sentence").
- Keep the read to what changes sentences. Topic, argument, structure, and evidence standards belong to `STYLE.md` and the brief.

## 5. Layer In The Confirmed Lessons

Read the governing `VOICE.md` after the examples. Its lessons are explicit writer judgment: when a lesson conflicts with a pattern you found, the lesson wins. Note the conflict in the voice read so the writer can see it.

Read the more specific voice context too: a publication's or assignment's examples or lessons override the writer's general set for that work.

## 6. Apply It

- Match patterns at their observed density. If the examples use a move once every few paragraphs, use it once every few paragraphs, not in every sentence.
- Copy the patterns, not the sentences. Do not paste sentences from a gold example into a new piece as new prose, and do not borrow its anecdotes, personal details, or subject matter.
- The writer's own words in the current material (notes, interview answers, comments, a draft they wrote) are different. Use them, verbatim or close, when they work for the piece.
- Prefer the examples over generic craft advice. If the gold set uses fragments, hedges, long accumulating sentences, or the passive voice, keep doing so where it fits; generic rules in other skills ("vary sentence length," "cut hedges," "prefer active voice") apply only where the examples are silent.
- AI-residue checks still run. Where a flagged pattern also appears regularly in the gold set, keep it at the writer's rate and remove only the excess.

## 7. Record The Read

- When working in a piece folder, save the voice read as `voice-read.md` beside the draft, with the examples used and the date, so the writer can see what the draft was matched to. Reuse it for later passes on the same piece unless the examples or the format change.
- Otherwise, include a short version of the read in the output, or keep it in working notes when the output must be clean copy only.
- Never write the voice read into `VOICE.md`. A pattern becomes a lesson only through `cw-save` with the writer's confirmation (see below).

## What Belongs In VOICE.md

`VOICE.md` collects lessons on diction and syntax that the examples alone did not prevent. A lesson qualifies when:

- the writer corrected a draft that had already been matched to the examples, or stated a sentence-level preference explicitly;
- it governs wording, sentence construction, punctuation, or tone, not argument or structure;
- it is specific enough to change a sentence.

Record each lesson with a date, the line that went wrong (or a description of it), and the fix. Do not add a general description of the voice, a list of adjectives, or patterns already visible in the examples. When a lesson is really "the examples show this, the draft ignored it," the better fix is often a clearer example in `examples/`, not a new rule.
