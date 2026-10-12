---
name: checking-for-slop
description: Use when a landing page, prototype or hero board is about to be deployed, shown to the owner, or called done; at every review round; and whenever the copy or layout "reads fine" to the same context that wrote it.
---

# Checking for slop

A built page is checked by a script and by readers who did not write it. The builder's own read does not count.

## Step 1 — Run the scanner

```bash
python3 .claude/skills/checking-for-slop/slop_scan.py <built page.html> --facts site/FACTS.md
```

Scan the **built output** (the deployed HTML or the framework's build), not the source. The script prints two kinds of line:

| Line | Meaning | What to do |
|---|---|---|
| `FAIL` | A ship-checklist item wrong by inspection: visible `[brackets]`, dead links, h1 count, missing title/description/og:image/favicon, images without alt, **numbers or weekdays on the page that are not in `FACTS.md`** | Fix before deploy. Exit code 1 until clean. |
| `TELL` | A pattern generated sites share: blocklist words, spaced em dashes, `A · B · C` strings, `→` on buttons, all-caps eyebrows, an accented word in the h1, Inter or system fonts, purple gradients, emoji, one radius and shadow on every surface, everything fading up the same way, three equal columns, motion without `prefers-reduced-motion`, anonymous testimonials | Judge each one. Keep it only with a reason that comes from the brief or a reference; write that reason in `DECISIONS.md`. A tell with no reason is removed. |

A number the script flags that is on `FACTS.md` under a different spelling (e.g. "1,240" vs "1240") is noise; everything else it flags is a fact drift.

## Step 2 — Two fresh-context readers

Dispatch two subagents with no project history. Give each **only** the rendered page text: the tab title, every visible string in page order, with buttons and links written as `[button: label]`. Not the source, not `FACTS.md`, not the brief.

1. **First visitor:** "In five seconds: what does this sell, why is it different, what does it cost, what do I do next? Then list every line you would call filler." Also ask the **swap test**: "Replace the brand name with a competitor's. What stops making sense?"
2. **Copy critic:** "For every sentence, quote the clause that is not a fact about the product, the place, the people or the process. List every number and claim you cannot verify from the text alone."

Report their findings quoted, not paraphrased. The builder's own copy read does not count.

## Step 3 — Report

This pass **reports; it does not edit the page.** Fixes are decided with the owner at the review round (CLAUDE.md: ask what problem a note points at before rebuilding).

Lead with the one job: can a visitor do it end to end? Then the FAILs, then the tells with a keep/remove verdict each, then the readers' quotes, then the top three improvements by impact. Log the round in `site/DECISIONS.md`. If the Stage 0 entry there is still the template, say so in the report: a page built without a brief is the finding, not the numbers.

## Common mistakes

- Running the scanner on a prototype before Stage 4 and treating missing `og:image` as a finding. Before deploy, only the TELLs and the number check matter.
- Fixing the numbers and shipping. If the brief and references are blank, the numbers were not the problem.
- Treating every TELL as a defect. A gradient that is the mist in the brief stays; a gradient that is there because gradients look premium goes.
