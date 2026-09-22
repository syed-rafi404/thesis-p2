#!/usr/bin/env python
"""
A page for checking by hand that each reconstructed board kept all of its writing.

For every board of the lectures made by run_lecture.py (output/lectures/<name>/), the page shows
the clean board large and two real video frames from the end of that board's time (the lecturer
is in them, but the board is at its fullest there). The checker marks each board "all there" or
"something missing" and says what. That turns "the new boards look clean" (judged by Claude, by
eye; RESULTS.md 4.1.2) into a count checked by a person.

Answers are kept in the browser (localStorage) and "Copy my results" puts them on the clipboard
to paste to Claude, who records them. Images are embedded (downscaled), so the page is one file
that works on any PC.

    python scripts/make_board_check_sheet.py
    -> output/lectures/board_completeness_check.html
"""
import base64
import html
import io
import json
import re
import sys
from pathlib import Path

from PIL import Image

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "output" / "lectures"
OUT = ROOT / "board_completeness_check.html"


def secs(stamp):
    m, s = stamp.split(":")
    return int(m) * 60 + int(s)


def uri(path, width, quality):
    img = Image.open(path).convert("RGB")
    if img.width > width:
        img = img.resize((width, round(img.height * width / img.width)), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=quality)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def frames_near(frames_dir, end_s, back_s=20):
    """The last frame of the era and one about back_s seconds earlier."""
    frames = []
    for f in frames_dir.glob("frame_*.jpg"):
        m = re.search(r"_(\d+)s\.jpg$", f.name)
        if m:
            frames.append((int(m.group(1)), f))
    frames.sort()
    before = [f for s, f in frames if s <= end_s]
    earlier = [f for s, f in frames if s <= end_s - back_s]
    picks = [before[-1]] if before else []
    if earlier and (not picks or earlier[-1] != picks[0]):
        picks.insert(0, earlier[-1])
    return picks


def main():
    boards = []
    for lecture in sorted(ROOT.iterdir(), key=lambda p: int(re.sub(r"\D", "", p.name) or 0)):
        mosaic = lecture / "boards" / lecture.name / "mosaic.json"
        if not mosaic.exists():
            continue
        for era in json.loads(mosaic.read_text(encoding="utf-8")):
            stem = Path(era["image"]).stem
            clean = lecture / "boards" / "clean" / f"{lecture.name}_{stem}_clean.jpg"
            if not clean.exists():
                continue
            raw = frames_near(lecture / "frames", secs(era["to"]))
            boards.append({"id": f"{lecture.name}/{stem}", "lecture": lecture.name, "era": era["era"],
                           "from": era["from"], "to": era["to"], "clean": uri(clean, 1280, 70),
                           "raw": [uri(f, 800, 60) for f in raw]})
    cards = []
    for k, b in enumerate(boards, 1):
        raws = "".join(f'<img src="{r}" alt="video frame">' for r in b["raw"])
        cards.append(f"""
<section class="card" data-id="{html.escape(b['id'])}">
  <h2>{k}. {html.escape(b['lecture'])}, board {b['era']} <span>{b['from']}-{b['to']}</span></h2>
  <img class="clean" src="{b['clean']}" alt="reconstructed board">
  <div class="raw">{raws}</div>
  <div class="ask">
    <label><input type="radio" name="r{k}" value="ok"> All the writing is there</label>
    <label><input type="radio" name="r{k}" value="missing"> Something is missing or unreadable</label>
    <input type="text" placeholder="What is missing, and where (e.g. the number at the bottom right)">
  </div>
</section>""")
    page = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Board completeness check</title>
<style>
:root {{ --bg:#f6f7f9; --card:#fff; --fg:#1f2328; --muted:#5b6472; --line:#e1e4e8; --ok:#2a9d4f; --bad:#d62828; }}
@media (prefers-color-scheme: dark) {{ :root {{ --bg:#15171b; --card:#1d2026; --fg:#e8ebef; --muted:#9aa3ae; --line:#2c313a; }} }}
* {{ box-sizing:border-box }}
body {{ margin:0; background:var(--bg); color:var(--fg); font:16px/1.5 "Segoe UI", system-ui, sans-serif; padding:0 16px 80px }}
main {{ max-width:1000px; margin:0 auto }}
h1 {{ font-size:26px; margin:24px 0 6px }}
.intro {{ background:var(--card); border:1px solid var(--line); border-radius:10px; padding:12px 16px }}
.card {{ background:var(--card); border:1px solid var(--line); border-radius:12px; padding:12px; margin:18px 0 }}
.card.done-ok {{ border-color:var(--ok) }} .card.done-missing {{ border-color:var(--bad) }}
.card h2 {{ font-size:18px; margin:2px 0 10px }} .card h2 span {{ color:var(--muted); font-weight:400 }}
img.clean {{ width:100%; height:auto; border-radius:8px; display:block; background:#fff }}
.raw {{ display:grid; grid-template-columns:repeat(auto-fit, minmax(260px, 1fr)); gap:8px; margin-top:8px }}
.raw img {{ width:100%; height:auto; border-radius:6px; display:block }}
.ask {{ display:flex; flex-wrap:wrap; gap:10px 18px; align-items:center; margin-top:10px }}
.ask input[type=text] {{ flex:1 1 320px; padding:6px 8px; border:1px solid var(--line); border-radius:6px; background:var(--bg); color:var(--fg) }}
.bar {{ position:fixed; left:0; right:0; bottom:0; background:var(--card); border-top:1px solid var(--line);
  padding:10px 16px; display:flex; gap:14px; align-items:center; justify-content:center }}
button {{ padding:8px 14px; border-radius:8px; border:1px solid var(--line); background:var(--bg); color:var(--fg); cursor:pointer }}
</style></head><body><main>
<h1>Board completeness check</h1>
<div class="intro">
<p><b>{len(boards)} boards.</b> For each one, the big picture is the board rebuilt with the lecturer
removed and whitened. The small pictures are real video frames from the end of that board's time,
with the lecturer still in them.</p>
<p><b>The question:</b> is any writing you can see in the real frames missing or unreadable in the
big picture? Pick an answer; if something is missing, say what and where. About 20 seconds a board.
Faint grey smudges and the board's edge do not count.</p>
<p>Your answers are saved in this browser. When you are done, press <b>Copy my results</b> and paste
them to Claude.</p>
</div>
{''.join(cards)}
</main>
<div class="bar"><span id="progress"></span><button id="copy">Copy my results</button></div>
<script>
const KEY = "boardcomplete:v1";
let saved = {{}};
try {{ saved = JSON.parse(localStorage.getItem(KEY) || "{{}}"); }} catch (e) {{}}
const cards = [...document.querySelectorAll(".card")];
function store() {{ try {{ localStorage.setItem(KEY, JSON.stringify(saved)); }} catch (e) {{}} }}
function paint() {{
  let done = 0, missing = 0;
  cards.forEach(c => {{
    const a = saved[c.dataset.id];
    c.classList.remove("done-ok", "done-missing");
    if (a && a.v) {{ done++; c.classList.add(a.v === "ok" ? "done-ok" : "done-missing"); if (a.v === "missing") missing++; }}
  }});
  document.getElementById("progress").textContent = done + " of " + cards.length + " checked, " + missing + " with something missing";
}}
cards.forEach(c => {{
  const id = c.dataset.id, a = saved[id] || {{}};
  const text = c.querySelector("input[type=text]");
  c.querySelectorAll("input[type=radio]").forEach(r => {{
    if (a.v === r.value) r.checked = true;
    r.addEventListener("change", () => {{ saved[id] = {{ v: r.value, t: text.value }}; store(); paint(); }});
  }});
  if (a.t) text.value = a.t;
  text.addEventListener("input", () => {{ saved[id] = {{ v: (saved[id] || {{}}).v || "missing", t: text.value }}; store(); paint(); }});
}});
document.getElementById("copy").addEventListener("click", async () => {{
  const lines = ["Board completeness check (" + cards.length + " boards):"];
  cards.forEach(c => {{ const a = saved[c.dataset.id]; lines.push(c.dataset.id + ": " + (a && a.v ? (a.v === "ok" ? "ok" : "MISSING: " + (a.t || "(not described)")) : "not checked")); }});
  const text = lines.join("\\n");
  try {{ await navigator.clipboard.writeText(text); alert("Copied. Paste it to Claude."); }}
  catch (e) {{ prompt("Copy this:", text); }}
}});
paint();
</script></body></html>
"""
    OUT.write_text(page, encoding="utf-8")
    print(f"{len(boards)} boards -> {OUT} ({OUT.stat().st_size / 1e6:.1f} MB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
