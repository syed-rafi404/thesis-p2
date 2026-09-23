#!/usr/bin/env python
"""
=============================================================================
HAVE THE VISION-LANGUAGE MODEL READ EACH WHITEBOARD IN FULL
=============================================================================
The original pipeline asked Qwen2.5-VL for keywords from raw frames. For the
DBMS lecture that produced "Istrat", "Istr", "Istro" and "Srat" as four broken
fragments of one name, "Nasir", "Ali", "Physics" and "Degree", none of which is
on the board, and not a single CGPA or student ID. A keyword prompt discards
numbers by design, and a raw frame has the lecturer standing in front of a
quarter of the board. The summariser never received the content, which is why
the notes carried 8.5% of the board's numbers.

This script asks the same model to transcribe everything written on the board,
keeping tables as tables, code as code, and every number exactly, and to write
[illegible] rather than guess.

THE EXPERIMENT IT ENABLES
-------------------------
--source mosaic   read the reconstructed board for each era (the lecturer removed)
--source frame    read one raw video frame from each era, the last one, where the
                  board is fullest but the lecturer is still in front of it
--source clean    read the 2026-09-22 boards (learned lecturer mask + whiteboard
                  clean-up, RESULTS.md 4.1.2) for lectures 1-13; writes
                  board_text_clean.json/.md, which build_lecture_notes.py also uses

Same model, same prompt, same boards; only the input image changes. Each run
also writes board_text_<source>.md, which score_board_recall.py can score
directly, so the question "does reconstruction help the vision model read the
board?" becomes a paired comparison over the 10 held-out boards:

    python scripts/score_board_recall.py --notes-name board_text_frame.md
    python scripts/score_board_recall.py --notes-name board_text_mosaic.md

That isolates the vision contribution from everything downstream of it, which
the end-to-end notes comparison cannot do.

Usage:
    python scripts/transcribe_boards.py --all --source mosaic
    python scripts/transcribe_boards.py --all --source frame
    python scripts/transcribe_boards.py --show-prompt
=============================================================================
"""

import argparse
import glob
import json
import os
import sys
from pathlib import Path

REPO = Path(os.environ.get("THESIS_REPO") or Path(__file__).resolve().parents[1])
RUNS = REPO / "output" / "live_focused" / "no_gaze" / "interval_10s"
BOARDS = REPO / "output" / "annotation_demo" / "all9"
DEFAULT_MODEL = os.environ.get("THESIS_QWEN") or "Qwen/Qwen2.5-VL-7B-Instruct"

PROMPT = """This is a photograph of a classroom whiteboard during a university lecture.

Transcribe everything written on the whiteboard, exactly as written.

- Copy every number, name, identifier, date and symbol exactly. Do not round,
  correct or reformat values.
- Write tables as Markdown tables with the same rows and columns as the board.
- Write code, SQL and program text inside ``` fences, keeping line breaks.
- Write formulas as they appear. For a bar over a term write it as NOT(...),
  for example NOT(A+B).
- Keep diagrams short: name what they are and copy any labels on them, for
  example "Gate diagram: inputs A, B into a box labelled NAND, output NOT(AB)".
- If part of the board cannot be read, write [illegible]. Never guess, and never
  add anything that is not written on the board.
- Ignore any person in the picture. Describe only what is written.

Output only the transcription."""


def load_vlm(model_id, max_pixels):
    import torch
    from transformers import AutoModelForImageTextToText, AutoProcessor
    kwargs = {}
    if max_pixels:
        kwargs["max_pixels"] = max_pixels
    processor = AutoProcessor.from_pretrained(model_id, **kwargs)
    dtype = torch.bfloat16 if torch.cuda.is_available() and torch.cuda.is_bf16_supported() \
        else torch.float16
    model = AutoModelForImageTextToText.from_pretrained(
        model_id, torch_dtype=dtype, device_map="auto")
    return model.eval(), processor


def trim_runaway(text, max_repeats=3):
    """Collapse a decode loop into its first few lines.

    Greedy decoding can fall into a repetition loop, the same failure that made
    the Whisper safeguard necessary. Lecture 10's TTL board did it here: the
    model read the board correctly, then tried to draw the diagram's diagonal
    and emitted the same backslash line 512 times, 42,037 characters in all.

    The repeated lines carry no board content, so this does not change any
    recall score. It matters because the text is pasted into the notes prompt,
    where 42,000 characters of one character would crowd out the lecture.

    Only runs of the same line are collapsed, so a board that legitimately
    repeats a line a few times survives intact. Returns the text and how many
    lines were dropped, which the caller records.
    """
    lines = text.split("\n")
    kept, removed, run, previous = [], 0, 0, None
    for line in lines:
        key = line.strip()
        run = run + 1 if key and key == previous else 1
        previous = key
        if run <= max_repeats:
            kept.append(line)
        else:
            removed += 1
    if removed:
        kept.append(f"[{removed} repeated lines removed: the model looped here]")
    return "\n".join(kept).strip(), removed


def read_board(model, processor, image, max_new_tokens):
    import torch
    messages = [{"role": "user", "content": [
        {"type": "image", "image": image},
        {"type": "text", "text": PROMPT}]}]
    prompt = processor.apply_chat_template(messages, tokenize=False,
                                           add_generation_prompt=True)
    inputs = processor(text=[prompt], images=[image], return_tensors="pt").to(model.device)
    with torch.no_grad():
        out = model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=False,
                             repetition_penalty=1.05)
    raw = processor.decode(out[0][inputs["input_ids"].shape[1]:],
                           skip_special_tokens=True).strip()
    return trim_runaway(raw)


def clean_era_images(run_dir):
    """(era record, clean board path) from the 2026-09-22 boards (notes_common.py)."""
    import notes_common as nc
    info = nc.discover_lectures().get(run_dir.name)
    if not info:
        return []
    return [({"era": e["era"], "from": e["from"], "to": e["to"],
              "clear_fraction": e["clear_fraction"]}, e["clean"])
            for e in nc.board_eras(info["board_dir"]) if e["clean"] is not None]


def era_images(run_dir, source):
    """(era record, image path) for each era of a lecture."""
    if source == "clean":
        return clean_era_images(run_dir)
    mosaic_json = BOARDS / run_dir.name / "mosaic.json"
    if not mosaic_json.exists():
        return []
    eras = json.loads(mosaic_json.read_text(encoding="utf-8"))
    frames = sorted(glob.glob(str(run_dir / "ingested" / "frames" / "*.jpg")))
    out = []
    for era in eras:
        if source == "mosaic":
            path = Path(era["image"])
            path = path if path.is_absolute() else REPO / path
        else:
            # The last frame of the era: the board is at its fullest, with the
            # lecturer wherever they happened to be standing.
            def secs(stamp):
                m, s = stamp.split(":")
                return int(m) * 60 + int(s)
            index = min(len(frames) - 1, secs(era["to"]) // 10) if frames else -1
            path = Path(frames[index]) if index >= 0 else None
        if path and path.exists():
            out.append((era, path))
    return out


def main():
    ap = argparse.ArgumentParser(description="Transcribe each whiteboard with Qwen2.5-VL")
    ap.add_argument("--run-dir", default=None)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--source", default="mosaic", choices=("mosaic", "frame", "clean"))
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--max-pixels", type=int, default=1920 * 1080,
                    help="Cap on image pixels given to the model; handwriting needs resolution")
    ap.add_argument("--max-new-tokens", type=int, default=1500)
    ap.add_argument("--show-prompt", action="store_true", help="Print the prompt and exit")
    ap.add_argument("--tag", default="",
                    help="suffix for the output files, so a second model does not overwrite the "
                         "first: --tag 3b writes board_text_<source>_3b.json/.md")
    args = ap.parse_args()

    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass

    if args.show_prompt:
        print(PROMPT)
        return 0
    if args.all and args.source == "clean":
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import notes_common as nc
        runs = [i["run_dir"] for i in nc.discover_lectures().values() if i["run_dir"] is not None]
    elif args.all:
        runs = [d for d in sorted(RUNS.iterdir()) if d.is_dir()]
    elif args.run_dir:
        runs = [Path(args.run_dir)]
    else:
        sys.exit("pass --run-dir <dir>, --all or --show-prompt")

    from PIL import Image
    print(f"model  : {args.model}")
    print(f"source : {args.source}\n")
    model, processor = load_vlm(args.model, args.max_pixels)

    for run_dir in runs:
        jobs = era_images(run_dir, args.source)
        if not jobs:
            print(f"{run_dir.name:<18} skipped: no mosaic.json; run board_mosaic.py first")
            continue
        boards, md = [], [f"# Board transcription ({args.source})", ""]
        for era, path in jobs:
            text, looped = read_board(model, processor,
                                      Image.open(path).convert("RGB"),
                                      args.max_new_tokens)
            boards.append({"era": era["era"], "from": era["from"], "to": era["to"],
                           "clear_fraction": era.get("clear_fraction"),
                           "image": str(path), "text": text,
                           "runaway_lines_removed": looped})
            md += [f"## Board {era['from']}-{era['to']}", "", text, ""]
            note = f"   [looped: {looped} repeated lines removed]" if looped else ""
            print(f"{run_dir.name:<18} era {era['era']}: {len(text)} chars{note}")

        payload = {"lecture": run_dir.name, "model": args.model, "source": args.source,
                   "prompt": PROMPT, "boards": boards}
        stem = f"board_text_{args.source}" + (f"_{args.tag}" if args.tag else "")
        (run_dir / f"{stem}.json").write_text(
            json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
        (run_dir / f"{stem}.md").write_text("\n".join(md), encoding="utf-8")
        if args.source == "mosaic" and not args.tag:
            # regenerate_notes.py --board-source boards reads this name
            (run_dir / "board_text.json").write_text(
                json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
