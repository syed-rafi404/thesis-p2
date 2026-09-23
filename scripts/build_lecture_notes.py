#!/usr/bin/env python
"""
=============================================================================
ANNOTATED LECTURE NOTES: TRANSCRIPT + NAMED BOARD BOXES -> NOTES THAT POINT AT THE BOARD
=============================================================================
Step 3 of the final deliverable (CLAUDE.md, "The final deliverable"). For each lecture:

  1. The boards, in time order, with their numbered, named boxes from label_boards.py
     (board_boxes.json).
  2. What the lecturer said while each board was up: the transcript is cut at the times the
     boards change. Each transcript chunk goes to exactly one board.
  3. One LLM call per board writes that board's section, pointing at the boxes.
  4. Checks, applied to every section, and counted in the .json beside the notes:
       - every quote of the lecturer must appear word for word in the transcript (after
         lower-casing and ignoring punctuation); any that does not is deleted, with its
         translation line;
       - every "box N" must be a box on that board; references to boxes that do not exist
         are counted.
  5. One last call writes the title, key takeaways and check-yourself questions.
  6. Markdown and a self-contained HTML page (notes_page.py).

TRANSCRIPTS AND LEAKAGE
-----------------------
For any lecture scored against an answer key, the transcript must come from a Whisper adapter
that never heard that lecture's lecturer (CLAUDE.md, leakage rule): the leave-one-speaker-out
adapters, transcribed with --timestamps, saved as transcript_loso.txt (NEXT_STEPS stage B).
--transcript-file auto takes transcript_loso.txt when present, else transcript_finetuned_v2.txt,
whose adapter was trained on lectures 1-5; the .json records a warning for those. A transcript
without [m:ss-m:ss] stamps is spread evenly over the lecture, and the .json says the times are
approximate.

The answer key data/board_truth is never read (guard()).

Usage:
    python scripts/build_lecture_notes.py --lecture BanglaASR7_004 --mock          # no model
    python scripts/build_lecture_notes.py --lecture BanglaASR7_004 --dry-run       # print prompts
    python scripts/build_lecture_notes.py --all --language both --model Qwen/Qwen3-32B --quant 4bit
Outputs, in each lecture's run folder:
    notes_annotated_<language>.md / .html / .json      (_MOCK in the name with --mock)
=============================================================================
"""

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import notes_common as nc                                         # noqa: E402
import notes_page                                                 # noqa: E402

# By file path: importing the src.summarizer package would pull in torch via generator.py.
_spec = importlib.util.spec_from_file_location(
    "annotated_prompts", nc.REPO / "src" / "summarizer" / "annotated_prompts.py")
ap_ = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ap_)

DEFAULT_MODEL = "Qwen/Qwen2.5-7B-Instruct"
STAMP_LINE = re.compile(r"^\[(\d+:\d{2}(?::\d{2})?)\s*-\s*(\d+:\d{2}(?::\d{2})?)\]\s*(.*)$")
# Any blockquote line (also "> >") holding a double-quoted span, labelled "Lecturer:" or not.
# The 2026-09-22 smoke test showed an unlabelled '> > "..."' quote slipping past a check that
# required the label.
QUOTE_LINE = re.compile(r'^\s*(?:>\s*)+.*?["“](.+?)["”]', re.I)
TRANSLATION_LINE = re.compile(r"^\s*(?:>\s*)+\(?\s*(?:\*)?In English", re.I)
INLINE_QUOTE = re.compile(r'["“]([^"”]{20,}?)["”]')
BOX_NUMBER = re.compile(r"\b[Bb]ox(?:es)?\s+(\d+)\b")
COLOUR_WORD = r"(red|blue|orange|green|purple|pink|brown|teal|olive|navy|yellow|black|grey|gray|violet|cyan)"
COLOUR_BEFORE = re.compile(rf"\b{COLOUR_WORD}(\s+)([Bb]ox\s+(\d+))\b", re.I)
COLOUR_AFTER = re.compile(rf"\b([Bb]ox\s+(\d+))(\s*\(\s*){COLOUR_WORD}(\s*\))", re.I)
PLACEHOLDER = re.compile(r"<[^>]{6,}>")


# ---------------------------------------------------------------------------
# Transcript
# ---------------------------------------------------------------------------

def load_transcript(run_dir, choice):
    run_dir = Path(run_dir)
    names = ["transcript_loso.txt", "transcript_finetuned_v2.txt"] if choice == "auto" else [choice]
    for name in names:
        path = nc.guard(run_dir / name)
        if path.exists():
            return name, path.read_text(encoding="utf-8", errors="ignore")
    return None, ""


def transcript_chunks(text, duration):
    """[(start_s, end_s, text)]. Unstamped lines are spread evenly over the lecture."""
    lines = [ln.strip() for ln in text.splitlines() if ln.strip() and not ln.startswith("#")]
    stamped = [STAMP_LINE.match(ln) for ln in lines]
    if lines and all(stamped):
        return [(nc.secs(m.group(1)), nc.secs(m.group(2)), m.group(3)) for m in stamped], False
    step = duration / max(1, len(lines))
    return [(k * step, (k + 1) * step, ln) for k, ln in enumerate(lines)], True


def excerpts_for_boards(chunks, boards):
    """Each chunk goes to the board that was up when the chunk started.

    Board k owns [its start, the next board's start); the first board also owns anything said
    before it, the last one everything after it.
    """
    starts = [nc.secs(b["from"]) for b in boards]
    out = [[] for _ in boards]
    for a, b, text in chunks:
        k = 0
        for j, s in enumerate(starts):
            if a >= s:
                k = j
        out[k].append(f"[{nc.stamp(a)}-{nc.stamp(b)}] {text}")
    return ["\n".join(x) for x in out]


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def norm(text):
    return " ".join(re.sub(r"[^\w]+", " ", text.lower()).split())


# The literal example text inside the QUOTES block of the prompt. A model that
# has nothing worth quoting sometimes copies it out instead of leaving the quote
# out, and it then reads as: The lecturer mentioned, "exact words from the
# transcript". Three of the 26 notes built on 2026-09-23 did this. It is not a
# real quote, so check_quotes cannot catch it by looking in the transcript, and
# two of the three were not blockquotes, so QUOTE_LINE never saw them.
PROMPT_PLACEHOLDERS = ["exact words from the transcript", "your translation"]
PLACEHOLDER_QUOTE = re.compile(
    r'[^.!?\n]*?["“](?:' + "|".join(re.escape(p) for p in PROMPT_PLACEHOLDERS) + r')["”][.,]?',
    re.I)


def strip_prompt_placeholders(section):
    """Remove text the model copied out of the prompt's own example.

    Whole lines go if nothing but the placeholder is left; otherwise only the
    clause introducing it is cut, so the sentence around it survives.
    """
    out, removed = [], 0
    for line in section.splitlines():
        if not PLACEHOLDER_QUOTE.search(line):
            out.append(line)
            continue
        removed += 1
        cleaned = PLACEHOLDER_QUOTE.sub("", line)
        # What remains of a line that was only the quote: ">", "Lecturer:",
        # "**", and the brackets around a translation line.
        if not re.sub(r'[>*\s:,.()\[\]\-]|Lecturer|In English', "", cleaned, flags=re.I):
            continue
        out.append(re.sub(r"\s{2,}", " ", cleaned).rstrip())
    return "\n".join(out), removed


# Rule 7 of the prompt bans LaTeX, but the 7B model reached for it anyway on the NOR truth table
# (2026-09-23), giving "\(A\)" and "\(\overline{A + B}\)" in the middle of a sentence. The page is
# plain HTML with no maths renderer, so the student sees the backslashes. This is the net under the
# prompt: it rewrites what the model emits into the plain text the rule asked for.
LATEX_PATTERNS = [
    (re.compile(r"\\overline\s*\{([^{}]*)\}"), r"(\1)'"),
    (re.compile(r"\\bar\s*\{([^{}]*)\}"), r"(\1)'"),
    (re.compile(r"\\(?:text|mathrm|mathit)\s*\{([^{}]*)\}"), r"\1"),
    (re.compile(r"\\[\(\)\[\]]"), ""),          # \( \) \[ \]
    (re.compile(r"\\times"), "x"),
    (re.compile(r"\\cdot"), "."),
    (re.compile(r"\$+"), ""),
]


def strip_latex(section):
    """Plain text for anything the model wrote as LaTeX. Returns (text, how many rewrites)."""
    n = 0
    for pattern, repl in LATEX_PATTERNS:
        section, k = pattern.subn(repl, section)
        n += k
    return section, n


def count_quote_lines(section):
    """Blockquote lines holding a quoted span: the quotes of the lecturer in this section."""
    return [m.group(1) for m in (QUOTE_LINE.match(ln) for ln in section.splitlines()) if m]


def check_quotes(section, transcript_norm, min_words=3):
    """Delete quotes that are not word for word in the transcript. Returns (text, kept, dropped)."""
    lines, out, kept, dropped = section.splitlines(), [], [], []
    skip_translation = False
    for line in lines:
        if TRANSLATION_LINE.match(line):          # never checked against the Banglish transcript
            if not skip_translation:
                out.append(line)
            skip_translation = False
            continue
        skip_translation = False
        m = QUOTE_LINE.match(line)
        if m:
            q = norm(m.group(1))
            if len(q.split()) >= min_words and q in transcript_norm:
                kept.append(m.group(1))
            else:
                dropped.append(m.group(1))
                skip_translation = True
                continue
        out.append(line)
    return "\n".join(out), kept, dropped


def check_box_refs(section, box_ids):
    refs = [int(n) for n in BOX_NUMBER.findall(section)]
    invalid = sorted({n for n in refs if n not in box_ids})
    mentioned = sorted({n for n in refs if n in box_ids})
    return invalid, mentioned


def fix_colours(section, colour_of):
    """Make every "orange box 3" / "box 3 (orange)" name box 3's real colour. Returns (text, fixes)."""
    fixes = []

    def before(m):
        real = colour_of.get(int(m.group(4)))
        if real and m.group(1).lower() != real:
            fixes.append(f"{m.group(1)} -> {real} (box {m.group(4)})")
            return f"{real}{m.group(2)}{m.group(3)}"
        return m.group(0)

    def after(m):
        real = colour_of.get(int(m.group(2)))
        if real and m.group(4).lower() != real:
            fixes.append(f"{m.group(4)} -> {real} (box {m.group(2)})")
            return f"{m.group(1)}{m.group(3)}{real}{m.group(5)}"
        return m.group(0)

    section = COLOUR_BEFORE.sub(before, section)
    section = COLOUR_AFTER.sub(after, section)
    return section, fixes


def unverified_inline_quotes(section, transcript_norm, box_texts_norm):
    """Quoted spans inside paragraphs that are neither in the transcript nor on the board."""
    out = []
    for line in section.splitlines():
        if line.lstrip().startswith(">"):
            continue
        for q in INLINE_QUOTE.findall(line):
            n = norm(q)
            if len(n.split()) >= 4 and n not in transcript_norm and n not in box_texts_norm:
                out.append(q)
    return out


def fix_headings(section, fallback):
    """Replace a heading the model copied from the format ("<a short heading ...>")."""
    lines = section.splitlines()
    for i, ln in enumerate(lines):
        if ln.startswith("## ") and (PLACEHOLDER.search(ln) or ln[3:].lower().startswith("in one line")):
            lines[i] = f"## {fallback}"
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

class Llm:
    def __init__(self, model_id, quant):
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
        kwargs = {"device_map": "auto"}
        if quant in ("4bit", "8bit"):
            from transformers import BitsAndBytesConfig
            kwargs["quantization_config"] = (
                BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4",
                                   bnb_4bit_compute_dtype=torch.bfloat16)
                if quant == "4bit" else BitsAndBytesConfig(load_in_8bit=True))
        else:
            kwargs["dtype"] = torch.bfloat16 if torch.cuda.is_available() else torch.float32
        self.model_id = model_id
        self.tok = AutoTokenizer.from_pretrained(model_id)
        self.model = AutoModelForCausalLM.from_pretrained(model_id, **kwargs).eval()

    def chat(self, messages, max_new_tokens):
        import torch
        try:        # Qwen3: answer directly, no hidden reasoning block
            text = self.tok.apply_chat_template(messages, tokenize=False, add_generation_prompt=True,
                                                enable_thinking=False)
        except TypeError:
            text = self.tok.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = self.tok(text, return_tensors="pt").to(self.model.device)
        with torch.no_grad():
            out = self.model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=False,
                                      repetition_penalty=1.05)
        reply = self.tok.decode(out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True)
        return re.sub(r"<think>.*?</think>", "", reply, flags=re.S).strip()


class MockLlm:
    """Deterministic stand-in so the whole pipeline can be tested without a GPU model.

    It deliberately writes one real quote (kept by the checker), one invented quote (removed)
    and one reference to a box that does not exist (counted), so the checks are exercised.
    """
    model_id = "MOCK (no language model)"

    def chat(self, messages, max_new_tokens):
        user = messages[-1]["content"]
        if "THE SECTIONS" in user:
            heads = re.findall(r"^## (.+)$", user, flags=re.M)
            return ("# Mock lecture title\nOne sentence about the lecture (mock).\n\n## Key takeaways\n"
                    + "".join(f"- {h}\n" for h in heads[:5]) + f"\n{ap_.SPLIT_MARK}\n\n## Check yourself\n"
                    "1. A mock question?\n2. Another mock question?\n\n### Answers\n1. Mock answer.\n2. Mock answer.")
        boxes = re.findall(r"^Box (\d+) \((\w+)\), (.*?):", user, flags=re.M)
        said = user.split("WHAT THE LECTURER SAID", 1)[-1]
        real = ""
        for line in said.splitlines():
            if not line.startswith("["):
                continue
            words = re.sub(r"^\[[^\]]*\]\s*", "", line).split()
            if len(words) >= 8:
                real = " ".join(words[:8])
                break
        body = [f"## {boxes[0][2] if boxes else 'Board'} (mock heading)",
                "**In one line:** a mock summary of this board.", "", "[[BOARD]]", ""]
        body += [f"Look at the {c} box {n}: the {name}." for n, c, name in boxes]
        body += ["", "Box 99 does not exist on this board (mock check).", ""]
        if real:
            body += [f'> Lecturer: "{real}"', "> (In English: mock translation)"]
        body += ['> Lecturer: "ei quote ta transcript e nei, mock"', "> (In English: invented)", "",
                 "**Remember:** the mock point."]
        return "\n".join(body)


# ---------------------------------------------------------------------------

def figure_block(board, k, vlm_name):
    legend = " · ".join(f"{b['id']} {b.get('name') or '?'}" for b in board["boxes"])
    source = ("reconstructed with the lecturer removed; background whitened for readability "
              "(the writing is the camera's own pixels)") if board.get("clean") else \
        "reconstructed with the lecturer removed"
    return [f"![Board {k}: {board['from']}-{board['to']}]({board['figure']})", "",
            f"*Figure {k}. The whiteboard during {board['from']}–{board['to']}, {source}. "
            f"Boxes found from the ink; names by {vlm_name}.*", "",
            f"**Boxes:** {legend}" if legend else "", ""]


def build(name, info, llm, language, args):
    run_dir = info["run_dir"]
    if args.boxes_file:
        boxes_path = run_dir / args.boxes_file
    else:
        boxes_path = nc.boxes_file(run_dir, mock=args.mock)
        if args.dry_run and not boxes_path.exists():
            boxes_path = nc.boxes_file(run_dir, mock=True)  # prompts can be shown with mock boxes
    if not boxes_path.exists():
        print(f"{name:<16} skipped: no {boxes_path.name}; run label_boards.py first")
        return None
    boxes_doc = json.loads(boxes_path.read_text(encoding="utf-8"))
    boards = boxes_doc["boards"]
    vlm_name = boxes_doc.get("model") or "position (mock)"

    tfile, ttext = load_transcript(run_dir, args.transcript_file)
    duration = nc.lecture_duration(name, nc.board_eras(info["board_dir"]))
    chunks, approx = transcript_chunks(ttext, duration)
    excerpts = excerpts_for_boards(chunks, boards)
    tnorm = norm(" ".join(c[2] for c in chunks))

    board_text = {}
    if args.board_text_file:
        p = nc.guard(run_dir / args.board_text_file)
        if p.exists():
            for entry in json.loads(p.read_text(encoding="utf-8")).get("boards", []):
                board_text[entry["era"]] = entry.get("text", "")

    # The lecture's own title, from the first box the VLM called a title, if any.
    titles = [b.get("text", "") for bd in boards for b in bd["boxes"]
              if "title" in str(b.get("name", "")).lower() and b.get("text")]
    lecture_label = " ".join(titles[0].split()) if titles else name
    mock_output = args.mock or boxes_doc.get("mock", False)
    # english_via_banglish: write the section in Banglish, then translate it, so the two routes to
    # an English note (straight from the board, or translated) can be scored against each other.
    via_banglish = language == ap_.ENGLISH_VIA_BANGLISH
    write_lang = "banglish" if via_banglish else language
    english_like = language != "banglish"
    sections, report, prev, frame_source = [], [], "", []
    for k, board in enumerate(boards, 1):
        msgs = ap_.section_messages(write_lang, lecture=lecture_label, board_no=k, board_count=len(boards),
                                    time_range=f"{board['from']}-{board['to']}", boxes=board["boxes"],
                                    transcript_excerpt=excerpts[k - 1], previous_heading=prev,
                                    board_text=board_text.get(board["era"], ""))
        if args.dry_run:
            print("=" * 72 + f"\n{name} board {k} ({language})\n" + "=" * 72)
            for m in msgs:
                print(f"\n----- {m['role'].upper()} -----\n{m['content']}")
            return None
        raw = llm.chat(msgs, args.max_new_tokens)
        if via_banglish:            # the section was written in Banglish; translate it
            frame_source.append(raw)
            raw = llm.chat(ap_.translate_messages(raw), args.max_new_tokens)
        raw, placeholders = strip_prompt_placeholders(raw)
        raw, latex_fixes = strip_latex(raw)
        # The english version quotes the lecturer in translation (the user, 2026-09-23: an
        # English-medium reader cannot read Banglish), so there is nothing to match against the
        # Banglish transcript. Those quotes are counted and labelled, never checked; the
        # word-for-word check stays on the banglish version, where the quotes are the real words.
        if english_like:
            text, kept, dropped, translated = raw, [], [], count_quote_lines(raw)
        else:
            text, kept, dropped = check_quotes(raw, tnorm)
            translated = []
        ids = {b["id"] for b in board["boxes"]}
        invalid, mentioned = check_box_refs(text, ids)
        text, colour_fixes = fix_colours(text, {b["id"]: b["colour"] for b in board["boxes"]})
        text = fix_headings(text, f"Board {k}, {board['from']}–{board['to']}")
        inline_bad = unverified_inline_quotes(
            text, tnorm, norm(" ".join(str(b.get("text", "")) for b in board["boxes"])))
        heading = next((ln[3:].strip() for ln in text.splitlines() if ln.startswith("## ")), "")
        prev = heading or prev
        figure = figure_block(board, k, vlm_name)
        colours = " ".join(f"{b['id']}={b['hex']}" for b in board["boxes"])
        body = text.splitlines()
        if any(ln.strip() == "[[BOARD]]" for ln in body):
            out = []
            for ln in body:
                out += figure if ln.strip() == "[[BOARD]]" else [ln]
            body = out
        else:                                   # model left the marker out: figure after the heading
            cut = next((i + 1 for i, ln in enumerate(body) if ln.startswith("## ")), 0)
            body = body[:cut] + [""] + figure + body[cut:]
        sections.append([f"<!-- boxes: {colours} -->"] + body)
        report.append({"board": k, "era": board["era"], "from": board["from"], "to": board["to"],
                       "transcript_chars": len(excerpts[k - 1]), "boxes": len(ids),
                       "boxes_mentioned": mentioned, "invalid_box_refs": invalid,
                       "colour_fixes": colour_fixes, "inline_quotes_unverified": inline_bad,
                       "prompt_placeholders_removed": placeholders, "latex_rewritten": latex_fixes,
                       "quotes_translated": translated,
                       "quotes_kept": kept, "quotes_dropped": dropped})

    sections_md = "\n\n".join("\n".join(s) for s in sections)
    # The frame is written in the language the sections were written in - for english_via_banglish
    # that is Banglish, from the Banglish sections kept above, not from their translations - and is
    # then translated like everything else.
    frame_md = "\n\n".join(frame_source) if via_banglish else re.sub(r"<!--.*?-->", "", sections_md)
    frame = llm.chat(ap_.frame_messages(write_lang, lecture=lecture_label,
                                        sections_markdown=frame_md), args.max_new_tokens)
    if via_banglish:
        frame = llm.chat(ap_.translate_messages(frame), args.max_new_tokens)
    if ap_.SPLIT_MARK in frame:
        head, tail = frame.split(ap_.SPLIT_MARK, 1)
    else:
        idx = frame.find("## Check yourself")
        head, tail = (frame[:idx], frame[idx:]) if idx >= 0 else (frame, "")

    kept_n = sum(len(r["quotes_kept"]) for r in report)
    dropped_n = sum(len(r["quotes_dropped"]) for r in report)
    invalid_n = sum(len(r["invalid_box_refs"]) for r in report)
    colour_n = sum(len(r["colour_fixes"]) for r in report)
    inline_n = sum(len(r["inline_quotes_unverified"]) for r in report)
    placeholder_n = sum(r["prompt_placeholders_removed"] for r in report)
    translated_n = sum(len(r["quotes_translated"]) for r in report)
    latex_n = sum(r["latex_rewritten"] for r in report)
    leak = ""
    if tfile == "transcript_finetuned_v2.txt" and nc.lecture_number(name) <= 5:
        leak = ("transcript_finetuned_v2.txt comes from an adapter trained on lectures 1-5, "
                "this lecture included: not valid for evaluation")
    # The 13 scored lectures live in run folders named with the OLD numbering, so a note made from
    # output/.../BanglaASR8 is the dataset's BanglaASR12. Without this line two different lectures
    # answer to "BanglaASR8": the old one here and the new one in output/lectures/.
    dataset_name = nc.dataset_lecture_name(name)
    renamed = dataset_name != name
    footer = ["---", "",
              (f"*This lecture is `{dataset_name}` in the dataset "
               f"(`{name}` is its old number, kept because the answer keys use it).*\n"
               if renamed else ""),
              f"*How these notes were made. Speech: {tfile or 'no transcript'}"
              + (" (times approximate)" if approx and tfile else "") + ". "
              f"Boards: {boxes_doc.get('boxes_from', 'ink')} boxes, named by {vlm_name}. "
              f"Notes written by {llm.model_id}. "
              + ((("These notes were written in Banglish from the board and the transcript, then "
                   "translated into English by the same model. " if via_banglish else "")
                  + f"The lecturer's words are given in English translation ({translated_n} quotes); "
                  "the Banglish version of these notes has the originals, checked word for word "
                  "against the transcript. ")
                 if english_like else
                 f"Quotes checked word for word against the transcript: {kept_n} kept, "
                 f"{dropped_n} removed. ")
              + f"References to boxes that do not exist: {invalid_n}.*"]
    markdown = "\n".join([head.strip(), "", sections_md, "", "---", "", tail.strip(), ""] + footer) + "\n"

    stem = (f"notes_annotated_{language}" + (f"_{args.tag}" if args.tag else "")
            + ("_MOCK" if mock_output else ""))
    (run_dir / f"{stem}.md").write_text(markdown, encoding="utf-8")
    title = next((ln[2:].strip() for ln in head.splitlines() if ln.startswith("# ")), name)
    (run_dir / f"{stem}.html").write_text(notes_page.render(markdown, run_dir, title), encoding="utf-8")
    meta = {"lecture": name, "dataset_lecture": dataset_name,
            "language": language, "model": llm.model_id, "mock": mock_output,
            "transcript_file": tfile, "times_approximate": approx, "leakage_warning": leak,
            "boxes_file": boxes_path.name, "board_text_file": args.board_text_file if board_text else None,
            "quotes_kept": kept_n, "quotes_dropped": dropped_n, "invalid_box_refs": invalid_n,
            "quotes_translated": translated_n, "quotes_word_for_word_checked": not english_like,
            "written_in": write_lang, "translated_to_english": via_banglish,
            "latex_rewritten": latex_n,
            "colour_fixes": colour_n, "inline_quotes_unverified": inline_n, "sections": report}
    (run_dir / f"{stem}.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"{name:<16} {language:<8} {len(boards)} sections, quotes {kept_n} kept / {dropped_n} removed, "
          f"bad box refs {invalid_n}, colours fixed {colour_n}, unverified inline quotes {inline_n}"
          f"{'  [times approximate]' if approx else ''}"
          f"{'  [LEAK: ' + leak + ']' if leak else ''}\n{'':<16} -> {run_dir / (stem + '.html')}")
    return meta


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--lecture", action="append")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--language", choices=ap_.LANGUAGES + ("both", ap_.ENGLISH_VIA_BANGLISH, "all"),
                    default="english",
                    help="english and banglish are each written straight from the board and the "
                         "transcript; english_via_banglish writes the Banglish note and translates "
                         "it, for the comparison in RESULTS 5.4. both = the two direct ones, "
                         "all = those plus the translated one")
    ap.add_argument("--transcript-file", default="auto",
                    help="auto = transcript_loso.txt if present, else transcript_finetuned_v2.txt")
    ap.add_argument("--boxes-file", default=None,
                    help="Override the boxes JSON (default board_boxes.json, or _MOCK with --mock)")
    ap.add_argument("--board-text-file", default="board_text_clean.json",
                    help="Whole-board VLM transcription to add, if present in the run folder")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--quant", choices=("none", "8bit", "4bit"), default="none")
    ap.add_argument("--max-new-tokens", type=int, default=1400)
    ap.add_argument("--tag", default="",
                    help="Added to the output names, e.g. 7b or 32b, so runs do not overwrite each other")
    ap.add_argument("--mock", action="store_true", help="No model; uses board_boxes_MOCK.json")
    ap.add_argument("--dry-run", action="store_true", help="Print the first prompt; load no model")
    ap.add_argument("--run-dir", default=None,
                    help="One lecture outside the standard folders (run_lecture.py)")
    ap.add_argument("--board-dir", default=None, help="With --run-dir: its mosaic.json folder")
    args = ap.parse_args()
    nc.utf8_console()

    if args.run_dir:
        if not args.board_dir:
            sys.exit("--run-dir needs --board-dir")
        lectures = {Path(args.board_dir).name: {"run_dir": Path(args.run_dir),
                                                "board_dir": Path(args.board_dir)}}
    else:
        lectures = nc.discover_lectures()
        if args.lecture:
            missing = [n for n in args.lecture if n not in lectures]
            if missing:
                sys.exit(f"no boards for {missing}; known: {', '.join(lectures)}")
            lectures = {n: lectures[n] for n in args.lecture}
        elif not args.all:
            sys.exit("pass --lecture <name>, --all, or --run-dir with --board-dir")
    languages = {"both": ap_.LANGUAGES,
                 "all": ap_.LANGUAGES + (ap_.ENGLISH_VIA_BANGLISH,)}.get(args.language,
                                                                         (args.language,))

    llm = MockLlm() if (args.mock or args.dry_run) else Llm(args.model, args.quant)
    for name, info in lectures.items():
        if info["run_dir"] is None:
            print(f"{name:<16} skipped: no run folder")
            continue
        for language in languages:
            build(name, info, llm, language, args)
            if args.dry_run:
                return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
