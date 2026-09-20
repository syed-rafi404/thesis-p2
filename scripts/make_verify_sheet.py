#!/usr/bin/env python
"""
=============================================================================
BUILD A VERIFICATION SHEET FOR THE BOARD GROUND TRUTH
=============================================================================
The board ground truth in data/board_truth was drafted by reading the
reconstructed boards, and a draft is not ground truth until a person has
checked it. Checking it by flipping between a JSON file and an image folder is
tedious enough that it would not get done, so this writes a single page with
each board shown next to the items claimed to be on it.

Open the page in a browser, look at the board, read the list beside it. Items
the drafter was unsure about are flagged. Write corrections anywhere convenient
and hand them back; the JSON is the thing that has to end up right.

The page references the images by relative path and needs no server, no
network and no upload. It travels with a copy of the folder.

Usage:
    python scripts/make_verify_sheet.py
    python scripts/make_verify_sheet.py --out output/verify.html
=============================================================================
"""

import argparse
import html
import json
import os
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
KIND_ORDER = ["number", "name", "code", "phrase", "term"]
KIND_NOTE = {
    "number": "Unguessable. These matter most.",
    "name": "Unguessable.",
    "code": "Partly guessable.",
    "phrase": "The lecturer's own wording.",
    "term": "Mostly generic; the model may know these anyway.",
}

CSS = """
:root{--bg:#f6f7f9;--fg:#15181d;--muted:#5b6472;--card:#fff;--line:#dde1e7;
      --flag:#b3261e;--flagbg:#fdecea;--accent:#1b6ef3}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --bg:#12151a;--fg:#e8ecf1;--muted:#98a2b3;--card:#1a1f27;--line:#2b323d;
  --flag:#ff8a80;--flagbg:#3a1f1d;--accent:#7aa7ff}}
*{box-sizing:border-box}
body{margin:0;padding:0 16px 64px;background:var(--bg);color:var(--fg);
     font:15px/1.55 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}
header{max-width:1200px;margin:0 auto;padding:28px 0 8px}
h1{font-size:26px;margin:0 0 6px}
.sub{color:var(--muted);max-width:70ch}
.board{max-width:1200px;margin:22px auto;background:var(--card);
       border:1px solid var(--line);border-radius:12px;overflow:hidden}
.board h2{font-size:17px;margin:0;padding:12px 16px;border-bottom:1px solid var(--line)}
.board h2 small{color:var(--muted);font-weight:400}
.row{display:grid;grid-template-columns:1.35fr 1fr;gap:0}
@media (max-width:860px){.row{grid-template-columns:1fr}}
.imgwrap{padding:14px;border-right:1px solid var(--line)}
@media (max-width:860px){.imgwrap{border-right:none;border-bottom:1px solid var(--line)}}
img{width:100%;height:auto;border-radius:8px;display:block;background:#0003}
.items{padding:14px 16px}
.kind{margin:12px 0 4px;font-size:12px;letter-spacing:.06em;text-transform:uppercase;
      color:var(--muted)}
.kind span{text-transform:none;letter-spacing:0;font-size:12px}
ul{list-style:none;margin:0;padding:0}
li{padding:3px 0;border-bottom:1px dotted var(--line)}
li:last-child{border-bottom:none}
code{background:#8883;padding:1px 5px;border-radius:4px;font-size:13px}
.flag{background:var(--flagbg);color:var(--flag);border-radius:6px;padding:3px 6px}
.flag b{font-weight:600}
.note{color:var(--muted);font-size:13px;padding:8px 16px;border-top:1px solid var(--line)}
.counts{color:var(--muted);font-size:13px}
"""


def render_items(items):
    by_kind = {}
    for it in items:
        by_kind.setdefault(it.get("kind", "term"), []).append(it)
    out = []
    for kind in KIND_ORDER:
        group = by_kind.get(kind)
        if not group:
            continue
        out.append(f'<div class="kind">{kind} '
                   f'<span>&mdash; {html.escape(KIND_NOTE.get(kind, ""))}</span></div><ul>')
        for it in group:
            text = html.escape(it["text"])
            alts = it.get("alt") or []
            extra = (f' <span class="counts">also accepts: '
                     f'{html.escape(", ".join(alts))}</span>') if alts else ""
            if it.get("verify"):
                out.append(f'<li class="flag"><b>CHECK THIS:</b> <code>{text}</code>'
                           f' &mdash; the drafter was unsure{extra}</li>')
            else:
                out.append(f"<li><code>{text}</code>{extra}</li>")
        out.append("</ul>")
    return "".join(out)


def main():
    ap = argparse.ArgumentParser(description="Build a board ground-truth verification page")
    ap.add_argument("--truth", default="data/board_truth")
    ap.add_argument("--out", default="output/annotation_demo/verify_board_truth.html")
    args = ap.parse_args()

    files = sorted((REPO / args.truth).glob("*.json"))
    if not files:
        raise SystemExit(f"no ground truth JSON in {args.truth}")

    out_path = REPO / args.out
    out_path.parent.mkdir(parents=True, exist_ok=True)

    boards_html, total_items, total_flagged, total_boards = [], 0, 0, 0
    for path in files:
        data = json.loads(path.read_text(encoding="utf-8"))
        lecture = data["lecture"]
        for board in data["boards"]:
            total_boards += 1
            items = board.get("items", [])
            total_items += len(items)
            flagged = sum(1 for it in items if it.get("verify"))
            total_flagged += flagged
            img = board.get("image", "")
            rel = os.path.relpath(REPO / img, out_path.parent).replace(os.sep, "/") if img else ""
            note = board.get("note", "")
            boards_html.append(f"""
<section class="board">
  <h2>{html.escape(lecture)} &middot; era {board.get('era')}
      <small>&mdash; {len(items)} items{', ' + str(flagged) + ' flagged' if flagged else ''}</small></h2>
  <div class="row">
    <div class="imgwrap">{'<img loading="lazy" src="' + html.escape(rel) + '" alt="board">'
                          if rel else '<p class="counts">no image</p>'}</div>
    <div class="items">{render_items(items)}</div>
  </div>
  {'<p class="note">' + html.escape(note) + '</p>' if note else ''}
</section>""")

    page = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Board Truth Check</title><style>{CSS}</style></head>
<body>
<header>
  <h1>Board ground truth &mdash; verification sheet</h1>
  <p class="sub">Look at each board, read the list beside it. Mark anything that is
  wrong, missing, or not actually on that board. Items in red are ones the drafter
  could not read confidently. The numbers and names matter most, because those are
  the items a language model cannot invent, which is what the measurement depends on.</p>
  <p class="counts">{total_boards} boards &middot; {total_items} items &middot;
  {total_flagged} flagged for checking &middot; corrections go into
  <code>data/board_truth/*.json</code></p>
</header>
{''.join(boards_html)}
</body></html>"""

    out_path.write_text(page, encoding="utf-8")
    print(f"wrote {out_path}")
    print(f"{total_boards} boards, {total_items} items, {total_flagged} flagged")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
