"""Gather every board image that has our numbered boxes drawn on it, in one place.

They are scattered. Nine lectures kept loose files in figures_annotated/, the rest only
exist inside the generated notes pages, because notes_page.py embeds each board as a
base64 data URI and the loose copies were produced on the other machine. Checking them
by hand meant opening 31 HTML pages.

This writes one folder of jpgs named <lecture>_<board>.jpg, and a contact sheet that
shows all of them on one scrollable page with the lecture and board under each.

    python scripts/collect_board_boxes.py
    start output\\board_boxes_review\\index.html
"""
import base64
import html
import os
import re
import shutil
import sys
from pathlib import Path

REPO = Path(os.environ.get("THESIS_REPO") or Path(__file__).resolve().parents[1])
OUT = REPO / "output" / "board_boxes_review"
DATA_URI = re.compile(r'src="data:image/(png|jpe?g);base64,([^"]+)"')


def from_loose_files():
    """The lectures that kept figures_annotated/ on this machine."""
    found = {}
    for d in sorted(REPO.glob("output/**/figures_annotated")):
        lecture = d.parent.name
        for img in sorted(d.glob("*.jpg")) + sorted(d.glob("*.png")):
            found.setdefault((lecture, img.stem), ("file", img))
    return found


def from_notes_pages():
    """Everything else, unpacked from the base64 in the notes pages."""
    found = {}
    for page in sorted(REPO.glob("output/lectures/*/notes_annotated_banglish*.html")):
        if "MOCK" in page.name:
            continue
        lecture = page.parent.name
        text = page.read_text(encoding="utf-8", errors="replace")
        # the board each image belongs to, in document order
        names = re.findall(r'figures_annotated/([^"\')]+?)\.(?:jpg|png)', text)
        for i, m in enumerate(DATA_URI.finditer(text)):
            stem = names[i] if i < len(names) else "board_%02d" % (i + 1)
            found.setdefault((lecture, stem), ("b64", m.group(2)))
    return found


def main():
    # Clear the contents rather than the folder itself: on Windows an open shell or a
    # file browser sitting in it makes rmtree fail, and the folder is the thing someone
    # is most likely to have open when they rerun this.
    OUT.mkdir(parents=True, exist_ok=True)
    for old in list(OUT.glob("*.jpg")) + list(OUT.glob("*.png")) + list(OUT.glob("*.html")):
        try:
            old.unlink()
        except OSError:
            pass

    items = from_loose_files()
    for key, val in from_notes_pages().items():
        items.setdefault(key, val)          # a real file beats an embedded copy

    written = []
    for (lecture, stem), (kind, payload) in sorted(items.items()):
        name = "%s_%s.jpg" % (lecture, stem)
        dest = OUT / name
        if kind == "file":
            shutil.copy(payload, dest)
        else:
            try:
                dest.write_bytes(base64.b64decode(payload))
            except Exception:                                   # noqa: BLE001
                continue
        written.append((lecture, stem, name))

    # Some figures_annotated folders were produced by the --mock run that tested the
    # plumbing with a stand-in model. Those boxes were not named by Qwen and must not be
    # reviewed as if they were real output, so they go in their own section at the end.
    real, mock = {}, {}
    for lecture, stem, name in written:
        (mock if "MOCK" in stem.upper() else real).setdefault(lecture, []).append((stem, name))
    by_lecture = real

    rows = []
    for lecture in sorted(by_lecture, key=lambda s: (len(s), s)):
        boards = by_lecture[lecture]
        rows.append('<h2>%s <small>%d boards</small></h2><div class="grid">'
                    % (html.escape(lecture), len(boards)))
        for stem, name in boards:
            rows.append('<figure><a href="%s" target="_blank">'
                        '<img src="%s" loading="lazy"></a>'
                        '<figcaption>%s</figcaption></figure>'
                        % (name, name, html.escape(stem)))
        rows.append("</div>")

    if mock:
        n = sum(len(v) for v in mock.values())
        rows.append('<h2 class="warn">Not real output: %d boards from the stand-in model'
                    '</h2><p class="warn">These came from the <code>--mock</code> runs that '
                    'tested the pipeline before Qwen was available. The boxes are drawn by '
                    'our code, but nothing named or read them. Do not judge the system by '
                    'these.</p>' % n)
        for lecture in sorted(mock, key=lambda s: (len(s), s)):
            rows.append('<h3>%s</h3><div class="grid">' % html.escape(lecture))
            for stem, name in mock[lecture]:
                rows.append('<figure><a href="%s" target="_blank">'
                            '<img src="%s" loading="lazy"></a>'
                            '<figcaption>%s</figcaption></figure>'
                            % (name, name, html.escape(stem)))
            rows.append("</div>")

    page = """<!doctype html><meta charset="utf-8">
<title>Board boxes to check</title>
<style>
 body{font:15px/1.5 system-ui,sans-serif;margin:24px;background:#fbfbfc;color:#1f2933}
 h1{font-size:20px} h2{font-size:16px;margin:28px 0 8px;border-bottom:1px solid #dde}
 small{font-weight:400;color:#7b8794}
 .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:14px}
 figure{margin:0;background:#fff;border:1px solid #e3e6ea;border-radius:6px;padding:8px}
 img{width:100%%;display:block;border-radius:3px}
 figcaption{font-size:12px;color:#52606d;margin-top:6px;text-align:center}
 h2.warn{color:#b4232c;border-bottom-color:#f0c2c5} p.warn{color:#b4232c;max-width:60em}
 code{background:#eef1f4;padding:1px 4px;border-radius:3px}
</style>
<h1>Every board with our numbered boxes drawn on it</h1>
<p>%d boards from %d lectures. Click any board to open it full size. Boards that only
existed inside a notes page were unpacked from it, so this is every one the project has
on this machine. Anything produced by a stand-in model is separated at the bottom.</p>
%s
""" % (len(written), len(by_lecture), "\n".join(rows))
    (OUT / "index.html").write_text(page, encoding="utf-8")

    print("%d boards from %d lectures" % (len(written), len(by_lecture)))
    print("folder      %s" % OUT)
    print("contact sheet %s" % (OUT / "index.html"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
