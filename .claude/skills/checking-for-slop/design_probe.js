/* Design probe: the tells of a generated page that only a rendered layout can show.
   Plain browser JavaScript, no dependencies. Returns a JSON report.

   Desktop app: paste the whole file into the browser pane's JavaScript tool on the deployed page,
   once at desktop width and once at 375 px (resize the pane first).
   CLI: node -e with Playwright: page.evaluate(fs.readFileSync('design_probe.js','utf8')).

   Each check reports a count and the first offender. A count is a measurement, not a verdict:
   judge each one against the brief, and record a kept tell with its reason in DECISIONS.md. */
(() => {
  const DEFAULT_FONTS = /^(inter|arial|helvetica|georgia|times|roboto|system-ui|-apple-system|segoe ui|sans-serif|serif|ui-sans-serif|ui-serif)$/i;
  const vis = el => { const r = el.getBoundingClientRect(); const s = getComputedStyle(el); return r.width > 0 && r.height > 0 && s.visibility !== "hidden" && s.display !== "none"; };
  const all = [...document.body.querySelectorAll("*")].filter(el => !["SCRIPT","STYLE","NOSCRIPT","SVG","PATH"].includes(el.tagName));
  const textEls = all.filter(el => [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim().length > 1) && vis(el));
  const desc = el => `<${el.tagName.toLowerCase()}${el.className && typeof el.className === "string" ? "." + el.className.trim().split(/\s+/).slice(0, 2).join(".") : ""}> "${(el.innerText || "").trim().slice(0, 40)}"`;
  const report = { width: innerWidth, checks: [] };
  const size = el => { const r = el.getBoundingClientRect(); return `${Math.round(r.width)}x${Math.round(r.height)}`; };
  const add = (check, items, note, detail) => report.checks.push({ check, count: items.length, examples: items.slice(0, 3).map(el => desc(el) + (detail ? " " + detail(el) : "")), note });

  // ---- colour maths (WCAG 2.1)
  const parse = c => { const m = c && c.match(/rgba?\(([\d.]+),\s*([\d.]+),\s*([\d.]+)(?:,\s*([\d.]+))?\)/); return m ? [+m[1], +m[2], +m[3], m[4] === undefined ? 1 : +m[4]] : null; };
  const lum = ([r, g, b]) => { const f = v => { v /= 255; return v <= .03928 ? v / 12.92 : ((v + .055) / 1.055) ** 2.4; }; return .2126 * f(r) + .7152 * f(g) + .0722 * f(b); };
  const ratio = (a, b) => { const [x, y] = [lum(a), lum(b)].sort((p, q) => q - p); return (x + .05) / (y + .05); };
  const bgOf = el => { // walk up to the first opaque background; null when a gradient or image intervenes
    for (let e = el; e; e = e.parentElement) {
      const s = getComputedStyle(e);
      if (s.backgroundImage !== "none") return null;
      const c = parse(s.backgroundColor); if (c && c[3] >= .99) return c;
    }
    return [255, 255, 255, 1];
  };

  // 1 contrast
  const contrastOf = el => { const s = getComputedStyle(el), fg = parse(s.color), bg = bgOf(el); return (!fg || !bg || fg[3] < .99) ? null : ratio(fg, bg); };
  const lowContrast = textEls.filter(el => !el.closest("[aria-hidden='true']")).filter(el => {
    const s = getComputedStyle(el), r = contrastOf(el); if (r === null) return false;
    const big = parseFloat(s.fontSize) >= 24 || (parseFloat(s.fontSize) >= 18.66 && +s.fontWeight >= 700);
    return r < (big ? 3 : 4.5);
  }).sort((a, b) => contrastOf(a) - contrastOf(b));
  add("text below WCAG AA contrast", lowContrast, "text on gradients and images is skipped; check those by eye", el => `${contrastOf(el).toFixed(2)}:1 at ${getComputedStyle(el).fontSize}`);

  // 2 tap targets (standalone controls only; links inside running text are exempt)
  const controls = all.filter(el => vis(el) && (["A","BUTTON","INPUT","SELECT","TEXTAREA"].includes(el.tagName) || el.getAttribute("role") === "button"));
  const small = controls.filter(el => { const r = el.getBoundingClientRect(); const inline = getComputedStyle(el).display.startsWith("inline") && el.closest("p, li, td"); return !inline && (r.width < 44 || r.height < 44); });
  add("tap targets under 44 px", small, "", size);

  // 3 line length
  const longLines = textEls.filter(el => /^(P|LI|DD|BLOCKQUOTE)$/.test(el.tagName)).filter(el => { const s = getComputedStyle(el); const chars = el.getBoundingClientRect().width / (parseFloat(s.fontSize) * .5); return chars > 80 && (el.innerText || "").length > chars; });
  add("body text wider than 80 characters", longLines);

  // 4 headings
  const hs = [...document.querySelectorAll("h1,h2,h3,h4,h5,h6")].filter(vis);
  const skips = hs.filter((h, i) => i && +h.tagName[1] > +hs[i - 1].tagName[1] + 1);
  add("heading levels skipped", skips, `${document.querySelectorAll("h1").length} h1 on the page`, (h) => { const i = hs.indexOf(h); return `${hs[i - 1].tagName} → ${h.tagName}`; });

  // 5 cards, and cards in cards
  const isCard = el => { const s = getComputedStyle(el); const r = el.getBoundingClientRect(); return r.width > 120 && r.height > 60 && ((s.boxShadow !== "none") || (parseFloat(s.borderTopWidth) > 0 && parse(s.borderTopColor)?.[3] > 0)); };
  const cards = all.filter(el => vis(el) && isCard(el));
  const nested = cards.filter(el => { let p = el.parentElement; while (p && p !== document.body) { if (isCard(p)) return true; p = p.parentElement; } return false; });
  add("cards inside cards", nested, `${cards.length} bordered or shadowed boxes in all`);
  const pairs = {}; cards.forEach(el => { const s = getComputedStyle(el); if (s.boxShadow === "none") return; const k = s.borderRadius + " | " + s.boxShadow.slice(0, 40); (pairs[k] = pairs[k] || []).push(el); });
  const top = Object.entries(pairs).sort((a, b) => b[1].length - a[1].length)[0];
  if (top) add("same radius and shadow pair repeated", top[1], top[0]);

  // 6 eyebrows and icon tiles
  const caps = textEls.filter(el => { const s = getComputedStyle(el); const t = (el.innerText || "").trim(); return t.length >= 6 && t.length <= 60 && (s.textTransform === "uppercase" || (t === t.toUpperCase() && /[A-Z]{3}/.test(t))) && parseFloat(s.letterSpacing) > 0; });
  const eyebrowed = hs.filter(h => { const p = h.previousElementSibling; return p && caps.includes(p); });
  add("tracked all-caps labels", caps, `${eyebrowed.length} of ${hs.length} headings have one directly above`);
  const tiles = hs.filter(h => { const p = h.previousElementSibling; if (!p) return false; const r = p.getBoundingClientRect(); const s = getComputedStyle(p); return r.width >= 24 && r.width <= 72 && Math.abs(r.width - r.height) < 6 && (s.backgroundColor !== "rgba(0, 0, 0, 0)" || s.borderTopWidth !== "0px"); });
  add("icon tile above a heading", tiles);

  // 7 motion
  const bounce = all.filter(el => { const s = getComputedStyle(el); const f = s.transitionTimingFunction + " " + s.animationTimingFunction; return /cubic-bezier\(\s*[^)]*?(-\d|1\.\d|[2-9]\d*\.?\d*)\s*\)/.test(f) || /back|elastic|bounce/.test(f); });
  add("bounce or elastic easing", bounce);
  const hidden = all.filter(el => vis(el) === false && getComputedStyle(el).opacity === "0" && el.getBoundingClientRect().width > 0 && !el.closest("[aria-hidden='true']"));
  add("elements still at opacity 0 after load", hidden, "scroll-reveal that never fired, or content hidden without a fallback");

  // 8 colour defaults
  const pureBlack = textEls.filter(el => getComputedStyle(el).color === "rgb(0, 0, 0)");
  add("pure black text", pureBlack, "untinted #000 is a default, not a choice");
  const grads = all.filter(el => vis(el) && /gradient/.test(getComputedStyle(el).backgroundImage));
  add("gradient backgrounds", grads, grads.some(el => /(139, 92, 246|99, 102, 241|168, 85, 247|124, 58, 237)/.test(getComputedStyle(el).backgroundImage)) ? "includes a purple/indigo gradient" : "");

  // 9 fonts actually rendered
  const fonts = {}; textEls.forEach(el => { const f = getComputedStyle(el).fontFamily.split(",")[0].replace(/["']/g, "").trim(); fonts[f] = (fonts[f] || 0) + 1; });
  report.fonts = Object.entries(fonts).sort((a, b) => b[1] - a[1]).map(([f, n]) => ({ font: f, elements: n, default: DEFAULT_FONTS.test(f) }));

  // 10 overflow
  report.horizontalOverflow = document.documentElement.scrollWidth > document.documentElement.clientWidth ? `${document.documentElement.scrollWidth} > ${document.documentElement.clientWidth}` : false;
  return report;
})();
