#!/usr/bin/env python3
"""Build board.html: every screenshot in this folder, with its row from NOTES.md.

Run from anywhere:   python3 site/references/make_board.py
Then open site/references/board.html, or /references/board.html on the dev server.

The board reads NOTES.md so the two never disagree. A screenshot with no row in
NOTES.md is shown with a "no note yet" flag: write its line, run this again.
"""
import html
import pathlib
import re

HERE = pathlib.Path(__file__).parent
IMAGE_TYPES = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
SEPARATOR = re.compile(r"^\|[\s\-:|]+\|$")
URL = re.compile(r"https?://\S+")


def read_tables(markdown):
    """Return (section heading, cells) for every table row, and the coverage rows."""
    rows, section = [], ""
    for line in markdown.splitlines():
        if line.startswith("#"):
            section = line.lstrip("#").strip()
        elif line.startswith("|") and not SEPARATOR.match(line):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            rows.append((section, cells))
    return rows


def md_inline(text):
    """Bold, links and bare URLs, nothing more."""
    text = html.escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\[(.+?)\]\((https?://[^)]+)\)", r'<a href="\2">\1</a>', text)
    text = re.sub(r"(?<![\"=])(https?://[^\s<]+)", r'<a href="\1">\1</a>', text)
    return text


def main():
    notes_path = HERE / "NOTES.md"
    notes = notes_path.read_text() if notes_path.exists() else ""
    rows = read_tables(notes)
    title = notes.splitlines()[0].lstrip("#").strip() if notes else "References"

    images = sorted(
        p for p in HERE.rglob("*")
        if p.suffix.lower() in IMAGE_TYPES and p.name != "board.html"
    )

    cards = []
    for image in images:
        rel = image.relative_to(HERE).as_posix()
        match = next(((s, c) for s, c in rows if any(image.name in c for c in c)), None)
        if match:
            section, cells = match
            cells = [c for c in cells if image.name not in c and not c.isdigit()]
            urls = [c for c in cells if URL.fullmatch(c)]
            text = [c for c in cells if c not in urls]
            name = text[0] if text else image.stem
            note = " ".join(text[1:]) if len(text) > 1 else ""
            link = f'<a class="src" href="{html.escape(urls[0])}">{html.escape(urls[0])}</a>' if urls else ""
            tag = f'<span class="tag">{html.escape(section)}</span>'
        else:
            name, note, link = image.stem, "", ""
            tag = '<span class="tag gap">no note yet</span>'
        cards.append(f"""
      <figure>
        <a href="{html.escape(rel)}" title="Open full size"><img src="{html.escape(rel)}" alt="{html.escape(name)}" loading="lazy"></a>
        <figcaption>
          <div class="head">{tag}<code>{html.escape(rel)}</code></div>
          <h2>{html.escape(name)}</h2>
          <p>{md_inline(note) or '<em>Write the one thing to take from this in NOTES.md.</em>'}</p>
          {link}
        </figcaption>
      </figure>""")

    coverage = [c for s, c in rows if s.lower().startswith("coverage")]
    coverage_html = ""
    if coverage:
        head, *body = coverage
        coverage_html = "<table><thead><tr>" + "".join(f"<th>{html.escape(h)}</th>" for h in head) + "</tr></thead><tbody>"
        for cells in body:
            gap = any("gap" in c.lower() for c in cells)
            coverage_html += f'<tr class="{"gap" if gap else ""}">' + "".join(f"<td>{md_inline(c)}</td>" for c in cells) + "</tr>"
        coverage_html += "</tbody></table>"

    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} — board</title>
<style>
  :root {{ --ink: #1b1b1b; --muted: #6b6b6b; --line: #e4e1dc; --paper: #f7f5f1; --warn: #b4531a; }}
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; padding: 32px 24px 64px; background: var(--paper); color: var(--ink);
         font: 15px/1.45 -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; }}
  header {{ max-width: 1400px; margin: 0 auto 28px; }}
  header h1 {{ font-size: 22px; margin: 0 0 4px; font-weight: 600; }}
  header p {{ margin: 0; color: var(--muted); }}
  table {{ border-collapse: collapse; margin: 20px 0 0; width: 100%; max-width: 1400px; font-size: 14px; }}
  th, td {{ text-align: left; padding: 8px 12px 8px 0; border-bottom: 1px solid var(--line); vertical-align: top; }}
  th {{ color: var(--muted); font-weight: 500; }}
  tr.gap td:first-child::before {{ content: "●"; color: var(--warn); margin-right: 8px; }}
  main {{ max-width: 1400px; margin: 32px auto 0; display: grid; gap: 28px 24px;
          grid-template-columns: repeat(auto-fill, minmax(380px, 1fr)); }}
  figure {{ margin: 0; background: #fff; border: 1px solid var(--line); border-radius: 6px; overflow: hidden; }}
  figure a img {{ display: block; width: 100%; aspect-ratio: 16 / 10; object-fit: cover; object-position: top;
                 border-bottom: 1px solid var(--line); background: #fff; }}
  figcaption {{ padding: 14px 16px 16px; }}
  .head {{ display: flex; gap: 10px; align-items: center; margin-bottom: 8px; }}
  .tag {{ font-size: 11px; text-transform: uppercase; letter-spacing: .06em; color: var(--muted);
          border: 1px solid var(--line); border-radius: 3px; padding: 2px 6px; }}
  .tag.gap {{ color: var(--warn); border-color: var(--warn); }}
  code {{ font-size: 12px; color: var(--muted); }}
  h2 {{ font-size: 17px; margin: 0 0 6px; font-weight: 600; }}
  p {{ margin: 0 0 8px; }}
  .src {{ font-size: 12px; color: var(--muted); word-break: break-all; }}
  a {{ color: inherit; }}
</style>
</head>
<body>
<header>
  <h1>{html.escape(title)}</h1>
  <p>{len(images)} screenshot{"" if len(images) == 1 else "s"} in <code>references/</code>. Click an image to open it full size. Edit <code>NOTES.md</code>, then rerun <code>make_board.py</code>.</p>
  {coverage_html}
</header>
<main>{"".join(cards)}
</main>
</body>
</html>
"""
    (HERE / "board.html").write_text(page)
    print(f"board.html: {len(images)} images, {len(coverage) - 1 if coverage else 0} coverage rows")


if __name__ == "__main__":
    main()
