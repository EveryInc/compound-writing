---
name: emergent
description: Compose existing Compound Writing skills and runtime capabilities for open-ended writing outcomes that no single skill covers, such as cross-draft analysis, source-to-outline comparison, or multi-pass revision.
---

# Emergent Capability

## Purpose

Enable the agent to handle requests that don't map directly to a specific skill by composing primitives and existing skills into novel solutions.

This is what makes the system agent-native: the ability to figure out how to accomplish an outcome, not just execute predefined workflows.

Read `../../references/context-contract.md` before composing a multi-artifact workflow. Respect the active project's source-of-truth files, provenance, destinations, and approval rules.

## When This Applies

Use emergent composition when:
- Request spans multiple drafts or files
- Request requires pattern analysis across the body of work
- Request combines multiple types of feedback
- No single skill handles the full request
- User describes an outcome, not a command

Do NOT use when:
- A skill directly handles the request (use the skill)
- The request is a simple file operation
- The user invokes a specific command

## The Composition Loop

When a request doesn't map to a skill:

1. **Understand the outcome**
   - What does success look like?
   - What would the user see/know when this is done?

2. **Identify capabilities needed**
   - What artifacts must be found, read, compared, or revised?
   - What maintained context or connected source must be loaded?
   - What draft, source, or destination operations are authorized?
   - What analysis operations? (compare, analyze voice, check AI)

3. **Identify skills that help**
   - Which existing skills apply to parts of the request?
   - Can skills be chained for the full solution?

4. **Compose a solution**
   - Chain primitives and skills together
   - Plan the sequence of operations

5. **Execute in a loop**
   - Work through the plan
   - Adapt if something unexpected comes up
   - Continue until outcome achieved or blocked

6. **Report results**
   - Summarize what was found/done
   - Offer next steps if applicable

## Example Requests and Approaches

| Request | Primitives | Skills | Approach |
|---------|-----------|--------|----------|
| "Compare voice in my last 3 drafts" | Find and read the relevant pieces | `voice-check` | Analyze each against the same live voice sources, then compare |
| "Find patterns in my hooks" | Find and read the relevant pieces | — | Extract openings, classify moves, and report with examples |
| "What objections keep coming up?" | Read the relevant drafts and reviews | `objections` | Compare repeated resistance and distinguish writer pattern from topic pattern |
| "Am I overusing certain transitions?" | Search the requested corpus | `transition` | Count, inspect context, and report only meaningful repetition |
| "Make this article better" | Load the draft, brief, voice, and sources | `dev-edit`, `line-edit`, `ai-check` | Diagnose, revise, then validate |
| "Help me finish this piece" | Inspect the active artifact and open decisions | varies | Route to the smallest unfinished outcome |
| "Cross-reference notes with outline" | Read both authoritative artifacts | — | Compare claims, examples, sources, and omissions |

## Judgment: When to Compose

**Good candidates for composition:**
- "Compare X across Y" — Analysis pattern
- "Find patterns in Z" — Discovery pattern
- "Check if A matches B" — Validation pattern
- "Make this better" — Improvement pattern
- "Help me with X" (vague) — Needs investigation first

**Not good candidates:**
- "Give me a hook" → Use /hook directly
- "Check my voice" → Use /voice-check directly
- "Run the asshole read" → Use /asshole directly

## The Ultimate Test

Can the agent accomplish tasks you didn't explicitly design for?

**Example:** User asks "Cross-reference my meeting notes with my task list and tell me what I've committed to but haven't scheduled."

This wasn't designed as a feature. But if the agent can:
1. Read the meeting notes
2. Read the task list
3. Extract commitments from notes
4. Compare against tasks
5. Report the gaps

...then it's agent-native.

## Failure Modes

If composition fails:
- **Missing capability or access:** Report what is unavailable
- **Skill not available:** Suggest manual alternative
- **Too complex:** Break into smaller requests
- **Ambiguous:** Ask for clarification

Never say "I don't have a feature for that" when composition could work.

## Reporting Results

When composition completes, report:
1. What was requested
2. What was done (briefly)
3. What was found/achieved
4. Suggested next steps (if applicable)

Keep reports focused on insights, not process details.

## Lessons

[Skill-specific lessons will be added here as they're captured]
