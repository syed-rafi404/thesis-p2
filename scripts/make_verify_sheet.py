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
the drafter was unsure about are flagged. Tick an item that is wrong and type
what the board really says; list anything missing; tick "I checked this board".
The "Copy my corrections" button turns all of that into plain text to hand
back, so nobody has to edit JSON by hand. Progress is kept in the browser.

The page references the images by relative path and needs no server, no
network and no upload. It travels with a copy of the folder.

Usage:
    python scripts/make_verify_sheet.py
    python scripts/make_verify_sheet.py --truth data/board_truth data/board_truth/draft_lectures1to6
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
.folder{max-width:1200px;margin:34px auto 0;font-size:20px}
.wrong{font-size:13px;color:var(--muted);white-space:nowrap;margin-left:6px}
.fix{display:none;margin:4px 0 2px;width:100%;padding:5px 7px;border:1px solid var(--line);
     border-radius:6px;background:var(--bg);color:var(--fg);font:inherit;font-size:14px}
li.is-wrong .fix{display:block}
li.is-wrong code{text-decoration:line-through}
.checkrow{display:flex;flex-wrap:wrap;gap:10px 18px;align-items:center;padding:10px 16px;
          border-top:1px solid var(--line)}
.checkrow textarea{flex:1 1 320px;min-height:38px;padding:6px 8px;border:1px solid var(--line);
                   border-radius:6px;background:var(--bg);color:var(--fg);font:inherit;font-size:14px}
.board.done{border-color:var(--accent)}
.board.done h2::after{content:"  \\2713 checked";color:var(--accent);font-size:13px;font-weight:500}
.bar{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;max-width:1200px;margin:0 auto;
     padding:10px 0;background:var(--bg);display:flex;flex-wrap:wrap;gap:10px;align-items:center}
button{font:inherit;padding:7px 14px;border-radius:8px;border:1px solid var(--accent);
       background:var(--accent);color:#fff;cursor:pointer}
button.ghost{background:transparent;color:var(--accent)}
#out{display:none;width:100%;max-width:1200px;margin:8px auto;min-height:160px;padding:8px;
     border:1px solid var(--line);border-radius:8px;background:var(--card);color:var(--fg);
     font:13px/1.45 ui-monospace,Consolas,monospace}
"""

SCRIPT = r"""
// v2: boards checked in an earlier round come from the JSON ("checked"), and
// item ticks from v1 are dropped because corrections can shift item positions.
const KEY = "boardcheck:v2";
let state = {};
try { state = JSON.parse(localStorage.getItem(KEY) || "{}"); } catch (e) { state = {}; }
function save() { try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) {} }
function refresh() {
  const boards = document.querySelectorAll(".board");
  let done = 0;
  boards.forEach(b => { const d = !!(state[b.dataset.id] || {}).done; b.classList.toggle("done", d); if (d) done++; });
  document.getElementById("progress").textContent = done + " of " + boards.length + " boards checked";
}
document.querySelectorAll(".board").forEach(b => {
  const s = state[b.dataset.id] = state[b.dataset.id] || {items: {}};
  s.items = s.items || {};
  if (b.dataset.checked && s.done === undefined) s.done = true;
  const done = b.querySelector(".done-box"), miss = b.querySelector(".missing");
  done.checked = !!s.done; miss.value = s.missing || "";
  done.addEventListener("change", () => { s.done = done.checked; save(); refresh(); });
  miss.addEventListener("input", () => { s.missing = miss.value; save(); });
  b.querySelectorAll("li[data-i]").forEach(li => {
    const it = s.items[li.dataset.i] = s.items[li.dataset.i] || {};
    const box = li.querySelector(".wrong-box"), fix = li.querySelector(".fix");
    box.checked = !!it.wrong; fix.value = it.fix || ""; li.classList.toggle("is-wrong", box.checked);
    box.addEventListener("change", () => { it.wrong = box.checked; li.classList.toggle("is-wrong", box.checked); save(); });
    fix.addEventListener("input", () => { it.fix = fix.value; save(); });
  });
});
refresh();
function report() {
  const lines = ["Board answer-key corrections", ""];
  let checked = [], unchecked = [];
  document.querySelectorAll(".board").forEach(b => {
    const s = state[b.dataset.id] || {items: {}}, label = b.dataset.label;
    (s.done ? checked : unchecked).push(label);
    b.querySelectorAll("li[data-i]").forEach(li => {
      const it = (s.items || {})[li.dataset.i];
      if (it && it.wrong) lines.push(label + ': WRONG "' + li.dataset.text + '" -> ' +
                                     (it.fix ? '"' + it.fix + '"' : "(remove, not on the board)"));
    });
    if (s.missing && s.missing.trim()) lines.push(label + ": MISSING " + s.missing.trim().replace(/\n+/g, " | "));
  });
  if (lines.length === 2) lines.push("No corrections.");
  lines.push("", "Checked (" + checked.length + "): " + (checked.join(", ") || "none"));
  lines.push("Not checked yet (" + unchecked.length + "): " + (unchecked.join(", ") || "none"));
  return lines.join("\n");
}
document.getElementById("copy").addEventListener("click", () => {
  const text = report(), out = document.getElementById("out");
  out.style.display = "block"; out.value = text; out.select();
  const note = document.getElementById("copied");
  const ok = () => { note.textContent = "Copied. Paste it into the Claude chat."; };
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(text).then(ok, () => { document.execCommand("copy"); ok(); });
  } else { document.execCommand("copy"); ok(); }
});
document.getElementById("flagged").addEventListener("click", e => {
  const on = e.target.dataset.on !== "1"; e.target.dataset.on = on ? "1" : "0";
  e.target.textContent = on ? "Show all boards" : "Show only boards with red items";
  document.querySelectorAll(".board").forEach(b => { b.hidden = on && !b.querySelector(".flag"); });
});
"""


def render_items(items):
    by_kind = {}
    for i, it in enumerate(items):
        by_kind.setdefault(it.get("kind", "term"), []).append((i, it))
    out = []
    for kind in KIND_ORDER:
        group = by_kind.get(kind)
        if not group:
            continue
        out.append(f'<div class="kind">{kind} '
                   f'<span>&mdash; {html.escape(KIND_NOTE.get(kind, ""))}</span></div><ul>')
        for i, it in group:
            text = html.escape(it["text"])
            alts = it.get("alt") or []
            extra = (f' <span class="counts">also accepts: '
                     f'{html.escape(", ".join(alts))}</span>') if alts else ""
            control = ('<label class="wrong"><input type="checkbox" class="wrong-box"> wrong</label>'
                       '<input class="fix" placeholder="What does the board actually say? '
                       'Leave empty if it is not on the board at all.">')
            attrs = f'data-i="{i}" data-text="{html.escape(it["text"], quote=True)}"'
            if it.get("verify"):
                out.append(f'<li class="flag" {attrs}><b>CHECK THIS:</b> <code>{text}</code>'
                           f' &mdash; the drafter was unsure{extra}{control}</li>')
            else:
                out.append(f"<li {attrs}><code>{text}</code>{extra}{control}</li>")
        out.append("</ul>")
    return "".join(out)


def main():
    ap = argparse.ArgumentParser(description="Build a board ground-truth verification page")
    ap.add_argument("--truth", nargs="+", default=["data/board_truth"],
                    help="One or more folders of answer-key JSON")
    ap.add_argument("--out", default="output/annotation_demo/verify_board_truth.html")
    args = ap.parse_args()

    folders = [(t, sorted((REPO / t).glob("*.json"))) for t in args.truth]
    if not any(files for _, files in folders):
        raise SystemExit(f"no ground truth JSON in {args.truth}")

    out_path = REPO / args.out
    out_path.parent.mkdir(parents=True, exist_ok=True)

    boards_html, total_items, total_flagged, total_boards = [], 0, 0, 0
    for folder, files in folders:
        if len(folders) > 1:
            boards_html.append(f'<h2 class="folder">{html.escape(folder)}</h2>')
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
                label = f"{lecture} era {board.get('era')}"
                checked = board.get("checked", "")
                done_note = (f'<small> &middot; checked {html.escape(str(checked))}, corrections '
                             f'already applied</small>') if checked else ""
                boards_html.append(f"""
<section class="board" data-id="{html.escape(folder + '|' + label, quote=True)}" data-label="{html.escape(label, quote=True)}" data-checked="{html.escape(str(checked), quote=True)}">
  <h2>{html.escape(lecture)} &middot; era {board.get('era')}
      <small>&mdash; {len(items)} items{', ' + str(flagged) + ' flagged' if flagged else ''}</small>{done_note}</h2>
  <div class="row">
    <div class="imgwrap">{'<img loading="lazy" src="' + html.escape(rel) + '" alt="board">'
                          if rel else '<p class="counts">no image</p>'}</div>
    <div class="items">{render_items(items)}</div>
  </div>
  {'<p class="note">' + html.escape(note) + '</p>' if note else ''}
  <div class="checkrow">
    <label><input type="checkbox" class="done-box"> <b>I checked this board</b></label>
    <textarea class="missing" placeholder="Anything written on this board that is missing from the list? One per line."></textarea>
  </div>
</section>""")

    page = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Board Truth Check</title><style>{CSS}</style></head>
<body>
<header>
  <h1>Board ground truth &mdash; verification sheet</h1>
  <p class="sub">For each board: look at the picture, read the list beside it.
  If an item is wrong, tick <b>wrong</b> and type what the board really says (leave it
  empty if the item is not on the board at all). Add anything missing in the box at
  the bottom. Then tick <b>I checked this board</b>. Items in red are the ones the
  drafter could not read confidently; start there. Numbers and names matter most.
  When you are done, or want to stop, press <b>Copy my corrections</b> and paste the
  text into the Claude chat. Your ticks are saved in this browser.</p>
  <p class="counts">{total_boards} boards &middot; {total_items} items &middot;
  {total_flagged} flagged for checking</p>
</header>
<div class="bar">
  <button id="copy">Copy my corrections</button>
  <button id="flagged" class="ghost">Show only boards with red items</button>
  <span id="progress" class="counts"></span> <span id="copied" class="counts"></span>
</div>
<textarea id="out" readonly></textarea>
{''.join(boards_html)}
<script>{SCRIPT}</script>
</body></html>"""

    out_path.write_text(page, encoding="utf-8")
    print(f"wrote {out_path}")
    print(f"{total_boards} boards, {total_items} items, {total_flagged} flagged")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
