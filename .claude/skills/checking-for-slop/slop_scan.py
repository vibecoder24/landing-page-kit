"""Scan a built landing page for the ship-checklist failures and the tells of a generated site.

Usage: python3 slop_scan.py <page.html> [more.html ...] [--facts site/FACTS.md]

Two kinds of output:
  FAIL  a ship-checklist item that is wrong by inspection (fix before deploy; exit code 1)
  TELL  a pattern that generated sites share; judge each one, a tell is not automatically wrong

Stdlib only. The script reads the HTML as text and as a parsed tree; it does not run JavaScript,
so content rendered by a framework must be scanned from the built output, not the source.
"""
import re, sys, os
from html.parser import HTMLParser

BLOCKLIST = [
    "elevate", "unleash", "seamless", "revolutioni", "all-in-one", "effortless", "empower",
    "next-level", "cutting-edge", "game-chang", "supercharge", "unlock", "world-class", "premium",
    "the finest", "with love", "you deserve", "changed my life", "best ever", "hassle-free",
    "handcrafted", "curated", "crafted with", "delight", "journey", "experience the", "discover the",
    "welcome to", "look no further", "we believe", "passion", "redefin", "transform your",
]
PURPLE = ["6366f1", "8b5cf6", "a855f7", "7c3aed", "4f46e5", "9333ea", "c084fc", "818cf8", "a78bfa", "d946ef", "ec4899"]
DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿\U0001F900-\U0001F9FF]")


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text, self.skip, self.h1 = [], 0, 0
        self.links, self.imgs, self.meta, self.link_rels, self.classes = [], [], {}, set(), []
        self.title, self.in_title, self.short = "", False, []  # short = text of small elements (eyebrows, labels, buttons)
        self.cur = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("script", "style", "noscript", "svg"): self.skip += 1
        if tag == "h1": self.h1 += 1
        if tag == "a": self.links.append(a.get("href", ""))
        if tag == "img": self.imgs.append(a)
        if tag == "meta": self.meta[a.get("name") or a.get("property") or ""] = a.get("content", "")
        if tag == "link": self.link_rels.add(a.get("rel", ""))
        if tag == "title": self.in_title = True
        if "class" in a: self.classes.append(a["class"])
        self.cur.append(tag)
    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript", "svg"): self.skip = max(0, self.skip - 1)
        if tag == "title": self.in_title = False
        if self.cur: self.cur.pop()
    def handle_data(self, d):
        if self.in_title: self.title += d
        if self.skip or not d.strip(): return
        self.text.append(d.strip())
        if len(d.strip()) < 60 and self.cur and self.cur[-1] in ("a", "button", "span", "small", "div", "p"):
            self.short.append(d.strip())


def numbers(s):
    # 4am, 9 am, ₹349, 500+, 71%, 2024, 1,240 — keep the digit core for matching
    return set(re.sub(r"[,\s]", "", m) for m in re.findall(r"\d[\d,]*(?:\.\d+)?", s))


def scan(path, facts_text):
    raw = open(path, encoding="utf-8", errors="replace").read()
    p = Page(); p.feed(raw)
    text = " ".join(p.text)
    low = text.lower()
    css = " ".join(re.findall(r"<style[^>]*>(.*?)</style>", raw, re.S | re.I)) + raw  # inline styles + style attrs
    fails, tells = [], []

    # ---- FAIL: ship checklist, checkable by inspection
    for m in re.findall(r"\[[^\]]{1,80}\]", text): fails.append(f"visible placeholder {m!r}")
    dead = [h for h in p.links if h in ("", "#") or h.startswith("javascript:")]
    if dead: fails.append(f"{len(dead)} link(s) go nowhere (href=\"#\", empty or javascript:)")
    if p.h1 != 1: fails.append(f"{p.h1} <h1> elements (need exactly 1)")
    if not p.title.strip(): fails.append("no <title>")
    if not p.meta.get("description"): fails.append("no meta description")
    if not p.meta.get("og:image"): fails.append("no og:image")
    if not any("icon" in r for r in p.link_rels): fails.append("no favicon <link rel=icon>")
    noalt = [i.get("src", "?") for i in p.imgs if not i.get("alt", "").strip() and i.get("role") != "presentation"]
    if noalt: fails.append(f"{len(noalt)} <img> without alt: {', '.join(noalt[:3])}")
    if facts_text is not None:
        fnums = numbers(facts_text)
        missing = sorted(n for n in numbers(text) if n not in fnums)
        for n in missing:
            where = next((t for t in p.text if n in re.sub(r"[,\s]", "", t)), "")
            fails.append(f"number {n} is not in FACTS.md: {where[:70]!r}")
        fdays = [d for d in DAYS if d in facts_text.lower()]
        pdays = [d for d in DAYS if d in low]
        bad = [d for d in pdays if d not in fdays]
        if bad: fails.append(f"days named on the page but not in FACTS.md: {', '.join(bad)}")

    # ---- TELL: patterns generated sites share; each one needs a reason
    hits = sorted({w for w in BLOCKLIST if w in low})
    if hits: tells.append(f"copy blocklist words: {', '.join(hits)}")
    dashes = re.findall(r"\s—\s", text)
    if dashes: tells.append(f"{len(dashes)} spaced em dash(es) in copy")
    dots = [s for s in p.short if " · " in s]
    if dots: tells.append(f"middle-dot meta strings: {dots[0]!r}" + (f" (+{len(dots)-1})" if len(dots) > 1 else ""))
    arrows = [s for s in p.short if "→" in s]
    if arrows: tells.append(f"'→' appended to link/button text: {arrows[0]!r}")
    caps = [s for s in p.short if len(s) > 8 and s.upper() == s and re.search(r"[A-Z]{3}", s)]
    if caps or "text-transform:uppercase" in css.replace(" ", ""): tells.append(f"all-caps labels or eyebrows: {(caps or ['via CSS text-transform'])[0]!r}")
    if re.search(r"<h1[^>]*>[^<]*<(em|span|strong|b|i)\b", raw, re.I): tells.append("one word in the headline accented (em/span inside <h1>)")
    fonts = [f for f in ("Inter", "Roboto", "system-ui", "Arial", "Helvetica") if re.search(rf"font-family\s*:[^;]*\b{f}\b", css)]
    if fonts: tells.append(f"default typeface as a primary font: {', '.join(fonts)}")
    grads = re.findall(r"linear-gradient\([^)]*\)", css, re.I)
    purple = [g for g in grads if any(h in g.lower() for h in PURPLE)]
    if purple: tells.append(f"purple/indigo gradient: {purple[0][:60]}")
    elif len(grads) >= 2: tells.append(f"{len(grads)} gradient backgrounds")
    em = EMOJI.findall(raw)
    if em: tells.append(f"{len(em)} emoji used in markup: {''.join(em[:5])}")
    radii = re.findall(r"border-radius\s*:\s*([^;}]+)", css)
    shadows = re.findall(r"box-shadow\s*:\s*([^;}]+)", css)
    if len(radii) >= 3 and len(set(r.strip() for r in radii)) == 1 and shadows:
        tells.append(f"one border-radius ({radii[0].strip()}) and a soft shadow on every surface")
    if "rgba(0,0,0,.1)" in css.replace(" ", "") or "rgba(0,0,0,0.1)" in css.replace(" ", ""): tells.append("the default soft grey shadow rgba(0,0,0,.1)")
    reveal = [c for c in p.classes if re.search(r"\b(reveal|fade|aos|animate|fade-up|slide-up)\b", c)]
    if len(reveal) >= 3: tells.append(f"{len(reveal)} elements share the same scroll-reveal class (everything fades up the same way)")
    if re.search(r"repeat\(\s*3\s*,", css): tells.append("a three-equal-column grid (hero → 3 feature cards is the template)")
    if re.search(r"(transition|animation)\s*:", css) and "prefers-reduced-motion" not in css: tells.append("motion present but no prefers-reduced-motion rule")
    # opacity:0 at rest is fine when a script-added class gates it (.motion .x, html.js .x) or it is a hover/pseudo decoration
    gates = set(re.findall(r"classList\.(?:add|toggle|remove)\(\s*['\"]([\w-]+)", raw))
    hidden = re.findall(r"([^{}]+)\{([^}]*\bopacity\s*:\s*0(?![.\d])[^}]*)\}", css)
    ungated = [s.strip().split(",")[0][:50] for s, _ in hidden
               if not any(f".{g}" in s for g in gates) and "::" not in s and ":hover" not in s and ":focus" not in s
               and not re.match(r"\s*(@|from\b|to\b|\d+%)", s)]
    if ungated and "<noscript" not in raw.lower() and "no-js" not in raw:
        tells.append(f"{len(ungated)} rule(s) hide content at rest with no script-gating class or <noscript>: {ungated[0]!r}. Check the page with JavaScript off")
    if re.search(r"repeat\(\s*[2-9]\s*,", css) and "@media" not in css:
        fails.append("a fixed multi-column grid and no @media rule: it will overflow at 375 px")
    if re.search(r"\b(happy|satisfied|verified) (customer|user|client)\b", low): tells.append("an anonymous testimonial attribution")
    return fails, tells


def main(argv):
    facts = None
    if "--facts" in argv:
        i = argv.index("--facts"); facts = open(argv[i + 1], encoding="utf-8").read(); del argv[i:i + 2]
    pages = [a for a in argv if not a.startswith("--")]
    if not pages: sys.exit(__doc__)
    bad = 0
    for path in pages:
        fails, tells = scan(path, facts)
        print(f"\n{path}")
        for f in fails: print(f"  FAIL  {f}")
        for t in tells: print(f"  TELL  {t}")
        if not fails and not tells: print("  clean: no checklist failures, no tells found (the critics still run)")
        print(f"  {len(fails)} fail(s), {len(tells)} tell(s)")
        bad += len(fails)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main(sys.argv[1:])
