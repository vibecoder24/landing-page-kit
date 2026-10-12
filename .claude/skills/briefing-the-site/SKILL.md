---
name: briefing-the-site
description: Use when starting Stage 0, when site/BRIEF.md or site/FACTS.md is blank or mostly placeholders, when the owner describes their product in a few lines, or when the owner asks to "fill in the brief" or "just draft it".
---

# Briefing the site

The brief is written from the owner's answers, not from what Claude knows about the category. The interview produces it; Claude's job is to ask the right questions in the right order and write down the answers.

## The first question is always the same

**"Is this a real product, or a fictional one for the exercise?"** Ask it before anything else, including when the owner is in a hurry.

| Answer | What it means for every later step |
|---|---|
| **Real** | Every fact comes from the owner. Claude invents nothing: no prices, no counts, no process times, no "standard" category facts. An unknown is `[ ]`, never a plausible guess. |
| **Fictional** | Claude may propose figures, marked **Proposed, invented** in `FACTS.md`, with the guardrails: specific not round, fictional businesses only, no generated faces as real people, a footer line saying the site is a demo. |

## The interview, in order

One question per message. Offer two to four options where you can, the recommended one first with its reason. If an answer already exists in the brief or in an earlier message, restate it for confirmation instead of asking again.

1. Real or fictional (above)
2. The one job: what should a visitor be able to do, end to end?
3. The three things they would never change about the product (these become the claims)
4. For each claim, the "so what?": why does a buyer care? If neither of you can say, the claim is parked, not deleted
5. Who buys, and where are they when they read this?
6. What the buyer is weighing it against (the positioning lines)
7. What proof exists today: numbers, names, photos, none
8. Name: chosen, or a naming step before Stage 2
9. Headline job: sell first or feel first
10. The hero object or motif: one object or shape from the product or the place
11. The signature move, in one sentence
12. Stack, decided now
13. Facts: every number, day, price and place name the answers mentioned, read back once for confirmation

Questions about fonts, colours and layout belong to Stage 2. Do not ask them here.

## When the owner says "just fill it in"

Ask the five questions whose answers change everything, in **one** message, then stop and wait:

1. Real or fictional?
2. The one job?
3. The one thing you would never change about the product?
4. Who buys it?
5. Static HTML or Next.js, and does this site become a template for later ones?

Draft only after the answers arrive. In the draft, every line is labelled **Given** (the owner said it), **Proposed** (Claude's default, one line of reason) or `[ ]`. Keep the brief under 120 lines. End with at most six open questions, ordered by how much each one changes.

## What the pass writes

- `site/BRIEF.md`: every heading filled or marked `[ ]`; the status line stays **draft**. Only the owner changes it to Frozen.
- `site/FACTS.md`: every number, day, price and place the brief mentions, with a Status column entry. The brief never states a number that is not here.
- `site/DECISIONS.md`: a Stage 0 entry with what was decided, what was rejected and why, and the open questions.
- `CLAUDE.md`: the three-row site table at the top.

## Common mistakes

- Treating a category fact as a product fact ("sourdough has four ingredients", "coffee is best within 7 days of roasting"). If the owner did not say it, it is `[ ]`.
- Writing the draft first and listing the questions after. The questions come first; the draft is made of their answers.
- Inventing proof for a real business "to show the layout". Use `[ ]` and a note of what the owner needs to supply.
- Freezing the brief yourself because the gate items are met by proposals. Met by proposal is not met.
