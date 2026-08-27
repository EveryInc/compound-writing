---
name: cw-tracks
description: Finds where the writing shows its tracks—scaffolding, throat-clearing, process narration, and arrival sequences that should be erased now that the destination is clear.
---

# Tracks

## Purpose

Find where the writing shows its tracks. Annie Dillard: "Process is nothing; erase your tracks." This skill hunts for the scaffolding still visible in a draft—the exploratory thinking, the arrival sequences, the "how I got here" that helped the writer but slows the reader.

Use this when:
- A draft reads like a journey log instead of a destination
- You can see the writer thinking on the page
- Sections narrate the process of figuring something out rather than presenting what was found
- The piece feels like it's warming up for too long before it arrives
- You've revised heavily and want to check for leftover scaffolding

## Invocation

- `/cw-tracks [text]` — Find the tracks in the provided text
- `/cw-tracks` — System asks "What needs its tracks erased?"
- Works on selection if provided, asks if not

## Track Types

| Track | What It Looks Like | Why It Should Go |
|-------|-------------------|------------------|
| **The Arrival Sequence** | "After much research, I realized..." "It took me a while to see that..." | The reader doesn't need your travel itinerary. Start where you landed. |
| **The Scaffolding** | Transitional paragraphs that connect old thinking to new thinking. | These helped you build the argument. The argument can stand without them now. |
| **The Thinking-Out-Loud** | "What if we consider..." "One might wonder..." "This raises the question..." | You already answered the question. Just give the answer. |
| **The Hedge Trail** | "It seems like," "I think," "perhaps," "it's possible that" — accumulated over drafts. | Hedges multiply during revision. Most can go once you know what you believe. |
| **The Deleted Argument's Ghost** | A rebuttal to a point no longer in the piece. A transition to a section that was cut. | Old structure leaves phantom limbs. Find and amputate them. |
| **The Discovery Narration** | "I didn't expect to find..." "Surprisingly..." "What I learned was..." | The reader experiences discovery through the idea itself, not through being told you discovered it. |
| **The Warm-Up** | First 1-3 paragraphs that exist because the writer needed a running start. | Your real opening is buried somewhere in paragraph 3 or 4. |
| **The Belt-and-Suspenders** | Making the same point twice in different words, because you weren't sure the first version landed. | Trust your first swing. If it didn't land, fix it—don't repeat it. |

## The Dillard Test

For every passage, ask:
1. Is this here for the reader or for the writer?
2. Does this describe the process of thinking, or the thought itself?
3. If I cut this, would the argument still stand?
4. Is this the destination, or the road I took to get there?

If the passage is road, not destination—erase the track.

## Output Format

```
## Track Report

**Tracks found:** [count]
**Severity:** [Light — a few fingerprints / Moderate — scaffolding visible / Heavy — the draft reads like a process log]

---

### The Tracks

1. **[Track type]** — [Location/quote]
   Why it's showing: [Brief explanation]
   Erase it by: [Specific suggestion]

2. **[Track type]** — [Location/quote]
   Why it's showing: [Brief explanation]
   Erase it by: [Specific suggestion]

[Continue for each track found]

---

### The Warm-Up Check

**Does the real piece start where the draft starts?**
[Yes / No — the piece actually begins at: "[quote from where the real opening lives]"]

---

### The Clean Version

[Rewrite of the most track-heavy section with tracks erased]

---

**What changed:**
- [How erasing tracks improved the passage]

Is the path clear now, or are there tracks I missed?
```

## Principles

- **Process is nothing; erase your tracks** — The reader should experience the destination, not the journey you took to find it.
- **The writer's discovery is not the reader's discovery** — You found the insight by wandering. The reader should find it by being led.
- **Scaffolding is for building, not for living in** — Once the structure stands, take down the scaffolding.
- **Trust arrival** — If you've arrived at a strong point, you don't need to narrate the arrival.
- **Revision leaves residue** — Every round of revision can leave traces of earlier versions. The last pass should clean the glass.

## The Box Canyon

Dillard describes writing as following a path into a box canyon—you dispatch reports from new territory. The reports are the writing. The path you took to get there is not. If your draft reads like a trail map, you're publishing the wrong thing.

## Lessons

[Skill-specific lessons will be added here as they're captured]
