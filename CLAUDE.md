# CLAUDE.md — A landing page, built the right way

*A process for building one landing page with Claude Code that looks professionally designed rather than generated. It was written while building a series of practice sites and revised after each one; the examples in it come from those sites. The things it asks you to do are the things that were skipped and paid for later.*

## How to work on this project

This repo holds one site, in `site/`. The documents in that folder are the project's memory; the page is the output. Read this file and `site/BRIEF.md` before anything else.

- **The process matters as much as the output.** Don't jump to a finished page. Each stage below exists for a reason, and skipping a stage is how sites end up generic.
- **Explain your reasoning.** When you make a design choice (a typeface, a layout, a motion), say why in one or two lines. The owner needs to understand it well enough to repeat it.
- **Show options, not a single answer**, at the decision points marked 🛑 below. Then stop and wait for a pick.
- **Record decisions** in `site/DECISIONS.md`: what was chosen, what was rejected, and why. That log is how the owner learns what worked.
- **Each stage has a done-gate.** Don't move on until it's met. Every gate skipped on earlier sites was paid for later as rework.
- **Address the owner as "you".** They are the client, the reviewer and the learner at once.

## The site

Fill this in during Stage 0 (it is a copy of what `site/BRIEF.md` decides):

| | |
|---|---|
| Site | [name] |
| Type | [D2C / B2B SaaS / big purchase / portfolio / other] |
| Signature move | [the one thing this page does exceptionally] |

Examples of a signature move from earlier sites, to set the bar: a coffee subscription whose hero cup scrolls into a seven-day freshness dial and then into estate cards; a voice-agent SaaS with a simulated call that plays and transcribes itself on the page; an electric motorcycle with a rotatable 3D model and a range calculator; a portfolio with a short Remotion-built video intro. Each site is **one strong landing page**, not a multi-page site.

## Repo structure

```
/site/
  BRIEF.md          ← the brief: audience, the one job, USP, name, hero object, stack. Frozen after Stage 0.
  FACTS.md          ← every number, day, place name, price and count the page may state. One source of truth.
  references/       ← screenshots + NOTES.md naming the one thing to take from each
  DECISIONS.md      ← running log of choices and reasons (the only document that grows)
  LEARNINGS.md      ← written once, at the end: the retrospective
  assets/           ← generated images and video; PROMPTS.md logs every generation
  scripts/          ← asset generation scripts (see Asset kit)
  .env.local        ← API keys; never committed
  (app code)
```

Every other document (copy, storyboard, asset brief) holds **current state only**. When one is superseded, fold it in or delete it; don't stack drafts. One earlier site ended with nine documents and no single place to find the current truth.

## The process (follow in order, don't skip stages)

### Stage 0 — Brief
**What:** `BRIEF.md` defines the audience, the page's one job, the USP, the positioning, the tone, the sections, the signature move, **the name, the hero object or motif, and the stack.** The template in `site/BRIEF.md` has a heading for each.
**Why:** Generic sites come from having no point of view. If the brief could describe any company in the category, the site will look like any company in the category. On the coffee site, the brief was rewritten on day 2 because the USP was a fact ("grown on one hill") and not a benefit; that rewrite cascaded into the name, the copy and the hero.
**Your job:** Read it before anything else. If it's vague, contradictory, or missing something you need, ask; don't fill gaps silently. Ask one question at a time. Run the **"so what?" test** on the USP: for each claim, say why a buyer cares. If you can't, the brief isn't done.
**Done when:**
- The USP survives "so what?"
- The name is chosen, or a naming step is scheduled before Stage 2
- The hero object or motif is named (coffee site: the cup and the mist)
- The headline's job is decided: sell first or feel first
- `FACTS.md` exists with every number the page will state (placeholders are fine, marked `[ ]`)
- The stack for this site is written down (static HTML is allowed when it's the decision, not a deferral)

After this gate the brief is **frozen**. A change goes through `DECISIONS.md` with a note of what it invalidates.

### Stage 1 — References
**What:** The owner collects 6–8 screenshots in `references/`, each with a note in `NOTES.md` naming the *specific* thing to take from it ("this headline serif", "how the image bleeds off the edge").
**Why:** Taste is borrowed before it is owned. Specific references give you a target. "Make it look premium" gives you the statistical average of every website, which is exactly the generic look we're trying to escape. The coffee site's references were mostly motion and structure; the missing ones (product card, photography) arrived mid-build and caused new design boards each time.
**Your job:** Study every reference and its note. Summarise the patterns you see across them. Point out any references that contradict each other. Name the gaps using the coverage table in `NOTES.md`.
**Done when:** every section and every asset type has at least one reference: the hero, the product or card, the photography style, the type, the tone of voice, the signature move. At least half come from outside the category. A reference that arrives after this gate goes into `references/NOTES.md` under **Parked for the next site**, unless it fixes a problem that has been named.

### Stage 2 — Design directions 🛑
**What:** Propose **two contrasting directions**. For each, give:
- Type pairing (real font names, available via Google Fonts or `next/font`), with a type scale
- Palette: 1 background, 1–2 neutrals, **one** accent colour, as hex values
- Spacing and radius approach
- Motion personality, in one sentence
- A rendered static hero section, so the direction can be seen and not just described

**Why:** The first idea is usually the average idea. Two genuinely different directions force real choices, and comparing them is how taste develops.
**Your job:** Make them *actually* different, not the same thing in two colours. Tie each choice back to the brief or a reference. Stop and wait for a pick.
**Rules learned the hard way:**
- Diverge at **hero level only**. Never build more than one full-page mockup. The coffee site kept five boards in sync for a day.
- Once a direction is picked, make **one storyboard** of the whole page (section by section, what the reader sees and the line that ties it). The storyboard was the most useful artifact on the coffee site; it's where the story, the sections and the motif get agreed cheaply.
- The **signature move gets its own storyboard** before any code: the object that carries across sections, its three key frames, and what the sequence says. The coffee site prototyped its opening eight times because this was skipped.
- **One motif.** It may appear at most three times, at different weights (full, light, hairline). The same device at the same weight on every section is a template.

### Stage 3 — Structure and copy 🛑
**What:** Write the real copy for every section, plus a simple wireframe of the layout per section.
**Why:** Lorem ipsum hides weak thinking. Real words change the layout: a 4-word headline and a 14-word headline need different designs. Copy is also the biggest giveaway of AI-generated sites.
**Your job:** Write in the tone set by the brief. Keep it short and specific. Stop for review before building.
**Voice rule: the fact alone.** Draft the line, then remove every clause that isn't a fact about the product, the place, the people or the process. No framing clause before it, no emotional landing after it. If a line could be deleted without losing a fact, delete it. Lead with specifics: the estate, the altitude, the roast day, the cups per bag.
**Done when:** the headline passes a 5-second test with a fresh-context reader (what does it sell, why is it different), every number in the copy matches `FACTS.md`, and every placeholder is in `[brackets]`.
**After this gate, the page is the copy's source of truth.** Any copy document retires once the build starts; edits happen on the page and the facts sheet, not in a seventh draft.

### Stage 4 — Build
**What:** Build the page using the chosen direction.
**Order:**
1. Design tokens first (colours, type scale, spacing) as CSS variables or Tailwind theme values
2. **The conversion path next:** the CTA, the picker or form it leads to, and the price. Before any motion. The coffee site finished with six "Start your subscription" buttons and nothing behind them.
3. Then the sections, top to bottom, static. The page must read as a normal document with JavaScript off.
4. Mobile-first: every section must work at 375 px before you style it for desktop
5. Deploy at the end of the first pass and run Lighthouse. Fix the baseline before adding motion.

**Why:** Tokens first makes the page consistent by construction. Conversion first means the page does its one job before it does anything else. Mobile-first catches layout problems while they're still cheap to fix.

### Stage 5 — Signature move
**What:** Build the one standout feature named in the brief, properly, **from its storyboard.**
**Why:** One thing done exceptionally well beats five effects done adequately. A page full of tricks reads as a template showcase.
**Your job:** Polish it: easing, timing, the mobile fallback, `prefers-reduced-motion`. Two prototypes at most before going back to the storyboard; if the second one doesn't land, the storyboard is wrong, not the code. If the brief's signature move is replaced, say so in `DECISIONS.md` rather than letting it fade out.

### Stage 6 — Critique and polish 🛑
**What:** Review the page honestly before calling it done.
- **Start with the one job:** can a visitor do the thing the page exists for, end to end?
- Review the **deployed URL in a real browser** (Chrome, 1440 px) and on a **real phone**, not only in an in-app preview pane
- Compare the result against the references and the brief
- Run the **swap test**: could you swap in a competitor's logo and the page still works? If yes, it's not specific enough.
- Use a **fresh-context critic** (a reader or a new session that hasn't seen the history) for copy and first impressions; the builder cannot see its own drift
- Go through the checklists below

**Your job:** Report what's weak, not just what's done. List the top 3 improvements by impact.

### Stage 7 — Retrospective
**What:** Write `LEARNINGS.md`: the journey in numbers, what the page got right, where the time went and the rule each lesson gives, the lessons for teaching, and what carries into the next site. Then revise this file.
**Why:** The process is as much the product as the page. If the lessons stay in a 100 KB log, the next site repeats them.

## How review rounds work

- **The owner reviews the whole deployed page once per round** and sends all notes together. One line of feedback at a time produced eleven page versions on the coffee site.
- **Claude asks what problem a note points at** before rebuilding. "I don't like the beans" may mean too many, too decorative, or the wrong motif; each has a different fix.
- **Separate taste notes from problem notes.** A taste note ("not this colour") is applied. A problem note ("this doesn't tell me what it costs") gets two options.
- **One version per round.** Keep the previous file, exclude it from deploys, log the round in `DECISIONS.md`.
- **Run the ship checklist at every deploy**, not once at the end.

## Ship checklist (every deploy)

- The one job works end to end, and every CTA leads to it; no `href="#"`
- No visible `[brackets]`; every number, day, place and price matches `FACTS.md`
- One story told one way (the coffee site told "7 days" seven ways)
- One h1; title, meta description, favicon, Open Graph image present
- Works at 375 px with no horizontal scroll; no tap target under 44 px
- Colour contrast meets WCAG AA; visible focus states; keyboard navigable
- `prefers-reduced-motion` respected; the page reads with JavaScript off
- Images optimised, sized, with alt text; no layout shift on load
- Lighthouse performance and accessibility both 90+
- No console errors; no failed requests
- Images read as one shoot (same light, palette, lens); nothing generated that claims to be a real person

## Signs of a generic AI-built site (avoid these by default)

- Purple-to-blue gradients, gradient blobs, glowing orbs
- Inter or system fonts for everything; no typographic contrast
- Centred hero, then 3 feature cards with icons, then a testimonial carousel, then a CTA band
- Emoji or generic line icons used as decoration
- Every card with the same rounded corners and soft shadow
- Glassmorphism by default
- Everything fading up on scroll the same way
- A fade to white between sections (it's a cut with extra steps; depth needs something nearer passing in front)
- The same separator or texture at the top of every section
- Copy like "Elevate", "Unleash", "Seamless", "Revolutionise", "Your all-in-one solution"
- A framing clause before the fact or an emotional landing after it ("Four roasts… One of them is your cup.")
- Placeholder people, logos and stats that are obviously fake

If a reference or the brief deliberately calls for one of these, that's fine. The rule is: no defaults without a reason.

## What makes a site look professionally made

- **Typographic hierarchy:** a clear type scale, real contrast between headline and body, comfortable line lengths (roughly 60–75 characters), three type levels per component at most
- **Colour restraint:** neutrals do most of the work, and one accent colour is used sparingly and on purpose
- **A consistent spacing rhythm:** generous whitespace, applied consistently; hierarchy by size and space, never by lines or boxes
- **Consistent imagery:** the images look like they come from one shoot, with the same light, palette and lens feel
- **One motif, at weights:** a shape or device that comes from the brand, used where it carries meaning, lighter each time it returns
- **Motion with purpose:** it guides attention or explains something; it isn't decoration. A scrubbed sequence starts from rest.
- **Details:** hover and focus states, active states on controls, a favicon, a title and meta description, an Open Graph image, no layout shift as the page loads

## Default stack

- **Next.js (App Router) + Tailwind CSS**; fonts via `next/font`. A single static HTML file is acceptable for a one-page site **if the brief says so**; decide in Stage 0, don't defer a port.
- **Scroll and motion:** GSAP + ScrollTrigger, or Motion (Framer Motion)
- **3D:** three.js via React Three Fiber + drei
- **Video:** Remotion
- API keys go in `site/.env.local`. Never commit them.
- Ask before adding any heavy dependency not on this list, and say what it costs in bundle size.

## Asset kit

The two scripts in `site/scripts/` call models on Replicate and need `REPLICATE_API_TOKEN` in `site/.env.local` (copy `.env.example`). Both append every run to `site/assets/PROMPTS.md`.

- **Stills:** `scripts/gen_image_openai.py` runs GPT Image 2. Draft at `low` quality (about $0.01 an image); low quality is usually fine for the page. Offer a high-quality pass once, near the end, for the images that ship.
- **Video:** `scripts/gen_video_replicate.py` runs Seedance 2.5. Use 480p, with first and last frame matched so it loops. Separate 16:9 and 9:16 compositions; phones get a poster, not the video.
- **Consistency:** one master per set, every other image an *edit* of the master (same light, framing, object), passed as a reference image. Two fixed style blocks (studio, location) with the same light direction, pasted into every prompt.
- **No text or logos in generated images.** Blank panels, labels as live HTML. A name change should never cost a regeneration.
- **No generated people presented as real.** Placeholders are labelled as such in the alt text and replaced before launch.
- **Log every generation** (prompt, model, refs, cost, keeper or reject) in `assets/PROMPTS.md`.
- **Never run a paid generation, drafts included, until the owner says go for that batch.** State what, how many and the cost, then wait.

## Conventions

- Match the target market's conventions in on-page copy: currency, units, date format, spelling
- No straight-edged blocks or ruled lines as section separators or grounds unless the direction calls for them; hairlines inside components are fine
- Keep components simple and readable. The owner should be able to walk through the code with a learner.
- Verify in a real browser tab with a real viewport; an in-app preview pane may be hidden, throttled or 0 × 0
- At the end of each stage, summarise what was done, what was decided and what's next, and add those decisions to `DECISIONS.md`
