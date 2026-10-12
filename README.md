# Landing Page Kit

A starter repo for building **one landing page with Claude Code** that looks professionally designed rather than generated.

It is not a theme or a component library. It is a process: a `CLAUDE.md` that walks Claude through seven stages with a done-gate on each, and a set of blank documents (brief, facts sheet, references, decisions log) that give the page a point of view before any code is written. The process was written while building a series of practice sites and revised after each one. The rules in it are the things that were skipped and paid for later.

## What you get

```
CLAUDE.md               the process Claude follows: 7 stages, review etiquette, ship checklist
.claude/                skills Claude uses at the stages (see below) and a dev-server entry for the preview pane
site/
  BRIEF.md              the brief, with a prompt under each heading
  FACTS.md              every number, day, name and price the page may state
  DECISIONS.md          a running log of what was chosen and why
  LEARNINGS.md          the retrospective, written at the end
  references/NOTES.md   6–8 screenshots and the one thing to take from each
  assets/PROMPTS.md     a log of every generated image or video
  scripts/              two Python scripts for generating stills and video (optional, paid)
  .env.example          where the API key goes
```

## Quick start

1. Click **Use this template** on GitHub and clone your copy.
2. Open the folder in Claude Code (the CLI or the desktop app's Code tab).
3. Say: **"Read CLAUDE.md and start Stage 0."** Claude will read the brief template and ask you questions, one at a time, until the brief passes its gate.
4. Collect 6–8 screenshots into `site/references/` and note what to take from each. This is the one stage Claude cannot do for you.
5. Follow the stages. Claude stops at the 🛑 points for your pick.

Nothing here needs installing until Stage 4. The stack is decided in Stage 0 and written into the brief; the default is Next.js + Tailwind, and a single static HTML file is fine for a one-page site if you choose it.

## The stages

| Stage | What happens | Gate |
|---|---|---|
| 0 Brief | Audience, the one job, USP, name, hero object, stack | USP survives "so what?"; facts sheet exists |
| 1 References | You collect 6–8 screenshots with a specific note each | Every section and asset type has one |
| 2 Directions 🛑 | Two contrasting hero renders; you pick one; one storyboard | A direction picked, signature move storyboarded |
| 3 Copy 🛑 | Real words for every section, in the fact-alone voice | Headline passes a 5-second test |
| 4 Build | Tokens, then the conversion path, then sections, mobile-first | Deployed, Lighthouse 90+ |
| 5 Signature move | The one thing the page does exceptionally | Works, with a reduced-motion fallback |
| 6 Critique 🛑 | One job, swap test, fresh-context reader, checklists | Top 3 improvements listed |
| 7 Retrospective | `LEARNINGS.md`, then revise `CLAUDE.md` | |

## The skills

Two skills live in `.claude/skills/` and load automatically when the repo is opened in Claude Code:

- **briefing-the-site** runs the Stage 0 interview: one question at a time, real-or-fictional first, and it writes the brief, the facts sheet and the decisions entry from your answers. If you ask Claude to "just fill it in", it asks the five questions that matter and then drafts, with every guess labelled.
- **checking-for-slop** is the review step. A Python script scans the built page for ship-checklist failures (placeholders, dead links, missing meta, numbers and weekdays that are not in `FACTS.md`) and for the tells of a generated site (banned words, purple gradients, Inter, emoji, three equal cards, everything fading up). A second script, run in the browser against the deployed page, measures what only a rendered layout shows: contrast, tap targets, line length, heading order, cards inside cards, eyebrows above every heading, and the fonts actually rendered. Then two fresh-context readers judge the copy, because the context that wrote a page cannot see its own drift.

Run the scanner by hand any time:

```bash
python3 .claude/skills/checking-for-slop/slop_scan.py site/index.html --facts site/FACTS.md
```

Two optional plugins pair well with the kit: the official **frontend-design** skill (a designer's eye for defaults that read as generated) and **superpowers** (brainstorming and planning discipline). Neither is required.

## Generating images and video (optional)

The two scripts in `site/scripts/` call GPT Image 2 and Seedance 2.5 on [Replicate](https://replicate.com). They cost money: about $0.01 for a low-quality still, more for high quality and for video. To use them:

```bash
cp site/.env.example site/.env.local
```

Then add your Replicate token to `site/.env.local`. The file is git-ignored. Claude will not run a paid generation until you say go for that batch, and every run is logged in `site/assets/PROMPTS.md`.

Both scripts need Python 3 and nothing else.

## Requirements

- [Claude Code](https://claude.com/claude-code)
- Python 3 (for the preview server and the asset scripts)
- Node.js, if the brief picks Next.js in Stage 0

## Licence

MIT. Use it, change it, teach with it.
