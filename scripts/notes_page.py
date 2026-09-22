"""Render annotated lecture notes (Markdown) as one self-contained HTML page.

No Markdown library is installed on either machine, so this handles the subset the notes use:
headings, paragraphs, bold/italic/code, bullet and numbered lists, blockquotes, pipe tables,
code fences, horizontal rules, images with a caption line below, and a "### Answers" block that
becomes a click-to-reveal. Two extras for the annotated notes:
  - "<!-- boxes: 1=#d62828 2=#1d4ed8 -->" (invisible in Markdown) sets the box colours of the
    section that follows, and every "box 3" / "orange box 3" in the text becomes a coloured tag;
  - images are embedded as data URIs, so the page is one file that can be sent as it is.
The page styles follow Temp/MOCKUP_lecture_note.html, with a dark mode.
"""
import base64
import html
import re
from pathlib import Path

CSS = """
:root { --bg:#f7f7f8; --card:#fff; --fg:#1f2328; --muted:#5b6472; --line:#e3e6ea; --accent:#1d4ed8; }
@media (prefers-color-scheme: dark) { :root { --bg:#15171b; --card:#1d2026; --fg:#e8ebef;
  --muted:#9aa3ae; --line:#2c313a; --accent:#7aa2ff; } }
* { box-sizing:border-box }
body { margin:0; background:var(--bg); color:var(--fg);
  font:17px/1.65 "Segoe UI", system-ui, -apple-system, Roboto, sans-serif; padding:0 16px 60px }
main { max-width:880px; margin:0 auto }
h1 { font-size:30px; margin:28px 0 6px; line-height:1.25 } h2 { font-size:23px; margin:30px 0 8px }
h3 { font-size:18px; margin:22px 0 6px }
hr { border:0; border-top:1px solid var(--line); margin:30px 0 }
figure { margin:16px 0; background:var(--card); border:1px solid var(--line); border-radius:12px; padding:10px }
figure img { width:100%; height:auto; border-radius:8px; display:block }
figcaption { color:var(--muted); font-size:14px; margin-top:8px }
.tag { font-weight:600; padding:1px 7px; border-radius:6px; color:#fff; white-space:nowrap }
blockquote { margin:14px 0; padding:10px 14px; border-left:4px solid var(--line);
  background:var(--card); border-radius:0 8px 8px 0 }
blockquote .en { color:var(--muted); font-size:15px }
table { border-collapse:collapse; margin:10px 0; display:block; overflow-x:auto; max-width:100% }
td, th { border:1px solid var(--line); padding:5px 12px; text-align:center }
th { background:var(--card) }
pre { background:var(--card); border:1px solid var(--line); border-radius:8px; padding:10px 12px;
  overflow-x:auto; font-size:14px } code { font-family:Consolas, "Cascadia Mono", monospace; font-size:0.92em }
details { margin:8px 0 } summary { cursor:pointer; color:var(--accent) }
.muted { color:var(--muted); font-size:14px }
"""

COLOUR_WORDS = r"(?:red|blue|orange|green|purple|pink|brown|teal|olive|navy)"
BOX_REF = re.compile(rf"\b((?:{COLOUR_WORDS}\s+)?[Bb]ox\s+(\d+))\b")


def data_uri(path):
    path = Path(path)
    mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()


def inline(text, box_colours):
    """Escape, then bold/italic/code, then coloured box tags."""
    codes = []

    def keep_code(m):
        codes.append(f"<code>{html.escape(m.group(1))}</code>")
        return f"\x00{len(codes) - 1}\x00"

    text = re.sub(r"`([^`]+)`", keep_code, text)
    text = html.escape(text, quote=False)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", text)

    def tag(m):
        colour = box_colours.get(int(m.group(2)))
        return f'<span class="tag" style="background:{colour}">{m.group(1)}</span>' if colour else m.group(1)

    text = BOX_REF.sub(tag, text)
    return re.sub(r"\x00(\d+)\x00", lambda m: codes[int(m.group(1))], text)


def render(markdown, base_dir, title="Lecture notes"):
    lines = markdown.splitlines()
    out, para, boxes = [], [], {}
    i = 0
    in_answers = False

    def flush():
        if para:
            out.append(f"<p>{inline(' '.join(para), boxes)}</p>")
            para.clear()

    def close_answers():
        nonlocal in_answers
        if in_answers:
            out.append("</details>")
            in_answers = False

    while i < len(lines):
        line = lines[i]
        s = line.strip()
        m = re.match(r"<!--\s*boxes:(.*?)-->", s)
        if m:
            flush()
            boxes = {int(k): v for k, v in re.findall(r"(\d+)=(#[0-9a-fA-F]{6})", m.group(1))}
            i += 1
            continue
        if not s:
            flush()
            i += 1
            continue
        if s.startswith("```"):
            flush()
            code = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code.append(lines[i])
                i += 1
            out.append(f"<pre><code>{html.escape(chr(10).join(code))}</code></pre>")
            i += 1
            continue
        hm = re.match(r"^(#{1,4})\s+(.*)$", s)
        if hm:
            flush()
            level = len(hm.group(1))
            if level <= 2:
                close_answers()
            if level == 3 and hm.group(2).strip().lower().rstrip(":") in ("answers", "uttor"):
                close_answers()
                out.append("<details><summary>Show answers</summary>")
                in_answers = True
            else:
                out.append(f"<h{level}>{inline(hm.group(2), boxes)}</h{level}>")
            i += 1
            continue
        if re.match(r"^(-{3,}|\*{3,})$", s):
            flush()
            close_answers()
            out.append("<hr>")
            i += 1
            continue
        im = re.match(r"^!\[(.*?)\]\((.+?)\)$", s)
        if im:
            flush()
            src = Path(base_dir) / im.group(2)
            img = data_uri(src) if src.exists() else html.escape(im.group(2))
            caption = ""
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines) and re.match(r"^\*(Figure|Fig\.)", lines[j].strip()):
                caption = inline(lines[j].strip().strip("*"), boxes)
                i = j
            out.append(f'<figure><img src="{img}" alt="{html.escape(im.group(1))}">'
                       + (f"<figcaption>{caption}</figcaption>" if caption else "") + "</figure>")
            i += 1
            continue
        if s.startswith(">"):
            flush()
            quote = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                body = re.sub(r"^(?:>\s*)+", "", lines[i].strip()).strip()
                if body:
                    cls = ' class="en"' if body.startswith("(") else ""
                    quote.append(f"<div{cls}>{inline(body, boxes)}</div>")
                i += 1
            out.append("<blockquote>" + "".join(quote) + "</blockquote>")
            continue
        if s.startswith("|") and i + 1 < len(lines) and re.match(r"^\|?\s*:?-{2,}", lines[i + 1].strip()):
            flush()
            head = [c.strip() for c in s.strip("|").split("|")]
            rows = []
            i += 2
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            t = ["<table><tr>" + "".join(f"<th>{inline(c, boxes)}</th>" for c in head) + "</tr>"]
            t += ["<tr>" + "".join(f"<td>{inline(c, boxes)}</td>" for c in r) + "</tr>" for r in rows]
            out.append("".join(t) + "</table>")
            continue
        lm = re.match(r"^(\s*)([-*]|\d+[.)])\s+(.*)$", line)
        if lm:
            flush()
            ordered = lm.group(2)[0].isdigit()
            items = []
            while i < len(lines):
                lm = re.match(r"^(\s*)([-*]|\d+[.)])\s+(.*)$", lines[i])
                if lm and (lm.group(2)[0].isdigit()) == ordered:
                    items.append(lm.group(3))
                elif lines[i].startswith("   ") and lines[i].strip() and items:
                    items[-1] += " " + lines[i].strip()          # continuation line
                else:
                    break
                i += 1
            tag_ = "ol" if ordered else "ul"
            out.append(f"<{tag_}>" + "".join(f"<li>{inline(t, boxes)}</li>" for t in items) + f"</{tag_}>")
            continue
        para.append(s)
        i += 1
    flush()
    close_answers()
    return ("<!DOCTYPE html>\n<html lang=\"en\"><head><meta charset=\"utf-8\">\n"
            "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">\n"
            f"<title>{html.escape(title)}</title>\n<style>{CSS}</style></head>\n"
            "<body><main>\n" + "\n".join(out) + "\n</main></body></html>\n")
