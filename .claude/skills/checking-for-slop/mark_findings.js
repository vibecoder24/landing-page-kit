/* Mark findings on the live page: a numbered badge and a dashed outline on each element.
   Paste into the browser's JavaScript tool (or Playwright page.evaluate) on the deployed page,
   after editing FINDINGS below. Each entry: { n, text } finds the smallest element containing that
   text; { n, selector } uses a CSS selector. Returns each marker's page y, which review_page.html needs.
   Then turn off smooth scrolling and screenshot every 720 px from the top: those are the review page's shots. */
(() => {
  const FINDINGS = [
    { n: 1, selector: "h1" },
    { n: 2, text: "Start your subscription" },
  ];
  document.querySelectorAll(".rv-badge").forEach(b => b.remove());
  document.documentElement.style.scrollBehavior = "auto"; document.body.style.scrollBehavior = "auto";
  const byText = (t, tags = "*") => [...document.querySelectorAll(tags)]
    .filter(el => (el.innerText || "").includes(t) && el.getBoundingClientRect().height < 400)
    .sort((a, b) => a.innerText.length - b.innerText.length)[0];
  const mark = (n, el) => {
    if (!el) return { n, y: null, note: "not found" };
    const r = el.getBoundingClientRect();
    const b = document.createElement("div"); b.className = "rv-badge"; b.textContent = n;
    b.style.cssText = `position:absolute;left:${Math.max(4, r.left + scrollX - 32)}px;top:${r.top + scrollY - 4}px;width:26px;height:26px;border-radius:50%;background:#d6336c;color:#fff;font:700 13px/26px system-ui;text-align:center;z-index:99999;box-shadow:0 0 0 2px #fff;pointer-events:none`;
    document.body.appendChild(b);
    el.style.outline = "2px dashed #d6336c"; el.style.outlineOffset = "3px";
    return { n, y: Math.round(r.top + scrollY) };
  };
  const out = FINDINGS.map(f => mark(f.n, f.selector ? document.querySelector(f.selector) : byText(f.text)));
  scrollTo(0, 0);
  return { markers: out, pageHeight: document.body.scrollHeight, viewport: innerHeight, shotStep: 720 };
})();
