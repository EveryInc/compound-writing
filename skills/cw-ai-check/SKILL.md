---
name: cw-ai-check
description: Scan or clean prose for AI-generated residue, including unsupported connective tissue, epistemic inflation, over-completed arguments, performed voice, formulaic structure, empty figurative language, stock phrasing, corporate abstraction, hedging, and false enthusiasm. Use for AI-smell cleanup, humanizing model-assisted prose, source-faithful drafting validation, writing polish, or pre-publication checks; enforce silently when composed into drafting or line editing.
---

# AI Check

## Purpose

Identify linguistic, structural, and epistemic patterns that make prose sound generated, then remove them without flattening the writer's meaning, voice, humor, or useful weirdness.

Generated prose often reveals itself through **overcompletion** before vocabulary: it supplies causality, symmetry, emotional meaning, and resolution that the source did not earn. Treat fidelity to the writer's knowledge as the first defense against AI smell.

For a full or source-based scan, read `references/structural-overcompletion.md` first. Then read `references/ai_tells_lexicon.csv` for lexical and sentence-pattern residue. Treat the lexicon as a pattern library, not a mechanical ban list.

## Behavior

### Silent Enforcement

When composed into Draft or Line Edit:

- Scan generated or revised copy.
- Repair clear AI tells without narrating the pass.
- Preserve meaning, provenance, and the active voice context.
- Show the user usable copy only.

### Manual Cleanup

When the user asks to clean or remove AI smell:

1. Provide the cleaned copy first.
2. Follow with a concise audit trail in document order.
3. Omit categories, severity labels, and confidence scores unless requested.

When the user explicitly asks for diagnosis only, do not rewrite. Return a sequential checklist with the quoted problem and a suggested fix.

## Scan Order

Run the passes in this order. Do not start with a word blacklist.

1. **Provenance:** Remove or flag details, motives, scenes, causes, and outcomes that the source does not establish.
2. **Epistemic fidelity:** Restore the writer's actual degree of certainty and distinguish observation from interpretation.
3. **Causal and argumentative closure:** Reopen contradictions or unknowns the draft resolved for elegance.
4. **Argument self-commentary:** Cut sentences that rate the evidence, signpost the structure, label a claim's status, or interpret a quote before delivering it.
5. **Structure and voice performance:** Find imposed symmetry, framework compliance, sustained conceits, and over-supplied signature moves.
6. **Reader and research posture:** Stop unsupported universalization and decorative authority.
7. **Lexical and sentence residue:** Apply the categories and lexicon below.

When only finished prose is available, do not invent a source mismatch. Phrase provenance concerns as questions or conditional flags. The self-commentary pass is the exception — it needs no source and runs at full confidence on finished copy.

## Detection Categories

### 0. Structural Overcompletion

Read `references/structural-overcompletion.md` when any of these conditions apply:

- prose was drafted or substantially revised by a model;
- notes, transcripts, research, or earlier human drafts are available for comparison;
- the draft avoids stock AI vocabulary but still feels generated (this is the signature condition for §11, argument self-commentary);
- the user asks whether the writing sounds human, over-written, too polished, or unlike them; or
- a full AI-residue scan is requested.

Flag unsupported connective tissue, strengthened certainty, neat causal explanations, examples forced into one taxonomy, voice moves supplied at implausible density, metaphors extended for continuity, reader experiences assigned without evidence, and endings that settle more than the writer settled.

**Fix:** Return to the source boundary. Separate observation from interpretation, preserve contradictions, let structure follow the material, ration conspicuous voice moves, and end on the strongest earned consequence or open question.

### 1. Generic Frames And Openers

Flag contextless setup such as:

- "In today's fast-paced world"
- "In the ever-evolving landscape of [X]"
- "In a world/an era where [X]"
- "With the rise of [X]"
- "As [trend] continues to [X]"
- "In the realm of [X]"
- "Let's dive/break it down/delve into [X]"
- "At its core, [X] is [Y]"
- "It is important/worth noting that [X]"
- "Join us as we [X]"

**Fix:** Start with a concrete fact, date, scene, action, or proper noun.

### 2. AI-Scent Vocabulary And Unnecessary Formality

Flag puffery, vague praise, and elevated substitutes for plain words, including:

- delve, tapestry used metaphorically, reimagined, nuanced, multifaceted
- leverage, utilize, harness, unlock, unleash, empower
- pivotal, crucial, vital, significant, noteworthy, transformative
- robust, seamless, comprehensive, meticulous, bespoke
- foster, underscore, illuminate, endeavor, embark
- elevate, amplify, optimize, spearhead, revolutionize
- plethora, myriad, commence, facilitate, optimal, prior to, whilst, amongst

**Fix:** Prefer plain verbs and specific nouns. Do not replace a precise domain term merely because it appears in the lexicon.

### 3. Corporate And MBA Abstraction

Flag business language that hides a plain claim:

- problem space, solution space, value proposition
- go-to-market motion, north star metric, operating cadence
- frameworks for thinking about [X], mental models around [X]
- pain points, actionable insights, key takeaways, move the needle
- low-hanging fruit, circle back, touch base, strategic alignment
- stakeholders, deliverables, digital transformation, paradigm shift

**Fix:** Name the actual problem, action, person, decision, metric, or result.

### 4. Stock Templates And Empty Emphasis

Flag general-purpose scaffolding such as:

- "When it comes to [X]"
- "The truth is [X]"
- "Now more than ever [X]"
- "Has emerged as [X]"
- "Represents a significant milestone"
- "Serves/stands as a testament to [X]"
- "At the end of the day"
- "One thing is clear"
- "Moving forward"
- "The bottom line is"

**Fix:** Delete the frame and state the concrete claim.

### 5. Empty Analogies And Figurative Language

Flag figurative language when the image supplies polish without adding meaning. Apply these tests:

- **Deletion test:** Removing the comparison leaves the meaning intact.
- **Mapping test:** The prose never identifies the shared mechanism, relationship, or structure between the two things.
- **Swap test:** Different topic nouns could be dropped into the image with no meaningful change.
- **Restatement test:** The figurative line merely repeats the literal sentence before or after it.
- **Payoff test:** The image adds no consequence, inference, stakes, or felt understanding.
- **Callback test:** An extended metaphor is maintained for literary continuity but stops helping the reader reason.

Also flag exhausted metaphors such as "tapestry of," "treasure trove," "double-edged sword," "tip of the iceberg," "uncharted waters," "beacon of hope," "standing at a crossroads," "blueprint for success," and "symphony/mosaic of."

**Fix:** Cut the ornament, state the literal claim, or make the comparison earn its place by naming the exact correspondence and what it helps the reader understand.

**Protect:** Keep fresh or tactile figurative language when it clarifies a mechanism, makes an abstraction graspable, produces a distinct inference, sharpens stakes, or carries the writer's specific point of view. Do not treat all metaphor as an AI tell.

### 6. Filler, Hedging, False Enthusiasm, And Perpetual Balance

Flag:

- "just" used as emphasis and "actually" used as filler
- reflexive uncertainty clusters: might, could, perhaps, generally, arguably, potentially, somewhat, often
- "Generally speaking," "It can be argued," "To some extent," "It depends on"
- "Based on the information provided"
- "Absolutely!" "Certainly!" "Great question!" "I'd be happy to help"
- "Both sides present valid points," "There are pros and cons," "Reasonable people may disagree"

**Fix:** Delete empty softening and enthusiasm. Make the strongest supportable claim and state real uncertainty precisely.

### 7. Formal Transitions And Vague Authority

Flag overused academic connectors and anonymous evidence claims:

- moreover, furthermore, additionally, consequently, thus, hence, therefore
- accordingly, notably, significantly, essentially, indeed, subsequently
- not only...but also, whether...or
- "Studies show," "Experts agree," "Research indicates," "According to recent reports"

**Fix:** Use a natural connector or restructure. Name and link the evidence, including dates and numbers, or remove the unsupported claim.

### 8. Correlatives And Negative Parallelisms

Flag repeated or formulaic contrasts:

- "not X but Y"
- "not just X, but also Y"
- "not because X, but because Y"
- "It's not about X. It's about Y."

**Fix:** State the positive claim directly or use a simple contrast. Preserve an isolated construction only when it is clearly the strongest sentence for the active voice.

### 9. Formulaic Structure And Manufactured Drama

Flag:

- "No X. No Y. Just Z."
- staccato declarative triads and redundant triplet sentences
- repeated fragments that manufacture urgency
- excessive rule of threes
- overly symmetric lists, bullets, and paragraph lengths
- uniform sentence length across a passage
- repeated `subject + verb + object, present participle + detail` constructions
- serial lists that drop the final "and" by default
- dramatic reveals that inflate an ordinary finding
- vague transformation statements that do not say what changed

**Fix:** Collapse repetition, vary rhythm, restore conjunctions, and replace drama with the specific event, finding, or change.

### 10. Aphoristic Equations And AI Cleverisms

Flag symmetrical, portable lines whose shape substitutes for proof:

- "X without Y is just Z"
- "X is Y for Z"
- "What gets X gets Y"
- "The best X is the X that doesn't [verb]"
- any line that reads like a tweet pretending to be a thesis

**Fix:** Back the line with the example or evidence that earned it, make the claim directly, or cut it.

### 11. Formulaic Closers

Flag:

- "In conclusion," "In summary," "To summarize," "To sum up"
- "Overall," "Ultimately"
- conclusions that merely repeat the article
- generic "one thing is clear" endings

**Fix:** End on the strongest implication, a concrete next step, or a specific unresolved question.

### 12. Argument Self-Commentary

Also called rhetorical scaffolding. The prose describes its own argument instead of making it. Plain words, short sentences, nothing from the lexicon — which is why this survives every other category here. Full treatment in `references/structural-overcompletion.md` §11.

Flag four subtypes:

- **Evidence self-rating:** "the cleanest thing we found," "the good part is measurable," "the artifact that convinced me," "the benchmarks are less charming"
- **Structural signposting:** "the other half of the read," "then there's the map," "verbosity is only the surface of it," "X sets the boundary on this"
- **Epistemic labeling:** "the open question is," "two things stay provisional," "one result complicates the picture"
- **Quote characterization:** "Mike put it best," "the complaint was unanimous"

Two tests, either sufficient:

- **Deletion test.** Cut it. If the argument stands and only reader guidance is lost, it was scaffolding.
- **Referent test.** Flag nouns pointing at the piece rather than the subject: *the read, the section, the picture, the case, the evidence, the takeaway, the boundary.*

**Fix:** Delete, or convert commentary into the thing it described. Uncertainty becomes the fact that limits it. A turn becomes one word. A quote gets a person and a task.

**Protect:** Adjudication between two-sided findings is a claim about the world and often required — "Mike's construction check could change the hotel choice. The HTML page could not" stays; "the construction check is the stronger finding" goes. Publication handoff conventions stay.

## Context Guardrails

Not every match is a problem. Check intent and domain before changing it:

- Do not confuse coherence with overcompletion; flag structure only when it outruns or distorts the material.
- Do not confuse adjudication with self-commentary; deciding between findings is a claim, describing that decision is scaffolding.
- Do not preserve errors, repetition, or disorder merely to make prose seem human.
- Do not manufacture quirky specificity as an antidote to generic prose; specificity must come from the source.
- Keep temporal "just" and corrective "actually."
- Keep warranted uncertainty; remove only reflexive or vague hedging.
- Keep standard domain language when it is precise.
- Keep formal transitions when the genre genuinely calls for them.
- Keep intentional irony or quotation.
- Keep meaning-bearing analogies and metaphors.
- Preserve source certainty and do not make a cautious claim stronger than its evidence.

## Output Formats

### Cleanup

```text
## Cleaned Copy

[Rewritten text]

---

## What Changed

1. Line/paragraph [N]: "[original]" -> "[revision]"
   Why: [brief explanation]

Summary: [X] AI tells removed. Primary patterns: [short list].
```

### Diagnosis Only

```text
## Sequential Editing Checklist

□ Line/paragraph [N]: "[quoted problem]"
  -> [suggested fix]
```

## User Extensions

Use `/cw-save` or an explicit in-flow request to route confirmed recurring tells into the maintained lexicon or governing voice context. Never edit an installed cache as the source of truth.
