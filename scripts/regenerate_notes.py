#!/usr/bin/env python
"""
=============================================================================
REGENERATE THE LECTURE NOTES, WITHOUT RE-RUNNING THE WHOLE PIPELINE
=============================================================================
Rebuilds final_lecture_notes from what a finished run already produced: a
transcript, whatever the vision model extracted from the board, and the
reconstructed board figures. Only the language model runs, so on the larger GPU
this takes about a minute per lecture instead of re-running speech recognition
and vision from scratch.

It exists for two reasons. The original notes read like a textbook chapter
recited from memory, and the grounded prompts in src/summarizer/prompts.py fix
that. And the before-and-after comparison needs notes built from new inputs,
the fine-tuned transcript and the vision model's reading of the reconstructed
boards, while holding everything else fixed.

INPUTS, AND WHERE EACH COMES FROM
---------------------------------
--transcript-file   which transcript to use. The baseline is
                    transcript_whisper_baseline.txt, which is Whisper's English
                    translation. The fine-tuned one is written by
                    scripts/transcribe_finetuned.py.

--board-source      keywords    visual_keywords.json, what the original pipeline
                                had: fragments pulled from occluded frames.
                    boards      board_text.json, the vision model's full reading
                                of each reconstructed board, written by
                                scripts/transcribe_boards.py.

THE ONE THING THIS MUST NEVER DO
--------------------------------
It never reads data/board_truth. That folder is the answer key for
score_board_recall.py. Feeding it to the generator and then scoring recall
against it would measure nothing, so the path is refused outright.

FIGURES
-------
The model is told which boards exist and what time range each covers, and it
places each one itself by writing a marker such as [[FIGURE 2]] on a line of its
own. That is better than placing figures by position in the notes, because the
model knows what each section is about. Markers are then replaced by the image
and a caption stating the time range and how clear the board is.

Usage:
    python scripts/regenerate_notes.py --run-dir <dir> --language mixed --dry-run
    python scripts/regenerate_notes.py --all --language mixed --board-source boards \\
        --transcript-file transcript_finetuned.txt
=============================================================================
"""

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

# Loaded by file path rather than as src.summarizer.prompts, because the package
# __init__ imports the generator and with it torch. Going through the package
# would make --dry-run need a GPU environment just to print a prompt.
import importlib.util                                               # noqa: E402

_spec = importlib.util.spec_from_file_location(
    "note_prompts", REPO / "src" / "summarizer" / "prompts.py")
_prompts = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_prompts)
LANGUAGES, build_messages = _prompts.LANGUAGES, _prompts.build_messages

RUNS = REPO / "output" / "live_focused" / "no_gaze" / "interval_10s"
BOARDS = REPO / "output" / "annotation_demo" / "all9"
FORBIDDEN = (REPO / "data" / "board_truth").resolve()
MIN_CLEAR = 0.95
# The model sometimes writes words after the marker ("[[FIGURE 1]] board during
# 1:10-10:50:"), occasionally a whole board transcription on the same line. The
# first version required the marker alone on its line, so those figures were
# silently dropped (10 of 58 across the 2026-09-21 notes). Now the marker becomes
# the picture and everything after it is kept as text, minus a leading
# "board during m:ss-m:ss:" label, which the caption repeats.
# A marker can also sit after a model-written label ("**Figure 3** [[FIGURE 3]]");
# such a label is dropped too, anything else before the marker is kept.
FIGURE_MARK = re.compile(r"^(.*?)\[\[\s*FIGURE\s+(\d+)\s*\]\](.*)$", re.IGNORECASE)
BOARD_LABEL = re.compile(r"^\s*board\s+during\s+\d+:\d+\s*[-–]\s*\d+:\d+\s*:?", re.IGNORECASE)
FIGURE_LABEL = re.compile(r"^\s*(\*\*|\*)?\s*figure\s+\d+\s*[.:]?\s*(\*\*|\*)?\s*$", re.IGNORECASE)


def marker_number(match):
    return int(match.group(2))


def marker_rest(match):
    """Text around a figure marker worth keeping: not a bare "Figure n" label
    before it, and not the redundant time label after it."""
    before = "" if FIGURE_LABEL.match(match.group(1)) else match.group(1).strip()
    after = BOARD_LABEL.sub("", match.group(3)).strip()
    # A one-line board dump sometimes carries ``` marks; on a line of its own they
    # would open a code block that swallows the rest of the notes.
    after = re.sub(r"```\w*", "", after).strip()
    return " ".join(t for t in (before, after) if t)


def guard(path):
    """Refuse to read the evaluation answer key."""
    resolved = Path(path).resolve()
    if resolved == FORBIDDEN or FORBIDDEN in resolved.parents:
        sys.exit(f"refusing to read {path}: that is the board-recall answer key, "
                 "and using it as input would make the evaluation circular")
    return resolved


def load_transcript(run_dir, name):
    path = guard(Path(run_dir) / name)
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8", errors="ignore").strip()


def load_board_content(run_dir, source):
    """Board text from the vision model, never from the ground truth."""
    run_dir = Path(run_dir)
    if source == "keywords":
        path = guard(run_dir / "visual_keywords.json")
        if not path.exists():
            return "", {}
        words = json.loads(path.read_text(encoding="utf-8"))
        return "Keywords read from the board: " + ", ".join(str(w) for w in words), {}
    path = guard(run_dir / "board_text.json")
    if not path.exists():
        sys.exit(f"{path} not found. Run scripts/transcribe_boards.py first, "
                 "or use --board-source keywords")
    data = json.loads(path.read_text(encoding="utf-8"))
    blocks, per_era = [], {}
    for entry in data.get("boards", []):
        text = entry.get("text", "").strip()
        if not text:
            continue
        per_era[entry["era"]] = text
        blocks.append(f"Board during {entry['from']}-{entry['to']}:\n{text}")
    return "\n\n".join(blocks), per_era


def load_figures(run_dir, boards_dir, min_clear, per_era_text):
    """Boards clean enough to show, copied beside the notes, numbered in time order."""
    mosaic_json = Path(boards_dir) / "mosaic.json"
    if not mosaic_json.exists():
        return []
    mosaic = json.loads(mosaic_json.read_text(encoding="utf-8"))
    usable = [e for e in mosaic if e.get("clear_fraction", 0) >= min_clear]
    fig_dir = Path(run_dir) / "figures_board"
    fig_dir.mkdir(parents=True, exist_ok=True)
    figures = []
    for n, board in enumerate(usable, 1):
        src = Path(board["image"])
        src = src if src.is_absolute() else REPO / src
        if not src.exists():
            continue
        dest = fig_dir / f"board_{n:02d}_era{board['era']}.jpg"
        shutil.copyfile(src, dest)
        summary = per_era_text.get(board["era"], "")
        summary = " ".join(summary.split())[:160]
        figures.append({
            "n": n, "era": board["era"], "from": board["from"], "to": board["to"],
            "clear": board["clear_fraction"], "frames": board.get("distinct_frames_used"),
            "image": dest.relative_to(Path(run_dir)).as_posix(),
            "summary": summary,
        })
    return figures


def place_figures(markdown, figures):
    """Swap each [[FIGURE n]] marker for the image and an honest caption."""
    by_n = {f["n"]: f for f in figures}
    placed, out = set(), []
    for line in markdown.splitlines():
        m = FIGURE_MARK.match(line)
        if not m:
            out.append(line)
            continue
        n = marker_number(m)
        fig = by_n.get(n)
        rest = marker_rest(m)
        if not fig or n in placed:
            if rest:
                out.append(rest)           # unknown or repeated marker: keep its text
            continue
        placed.add(n)
        out.append(f"![Board {fig['from']}-{fig['to']}]({fig['image']})")
        out.append("")
        out.append(f"*Figure {n}. The whiteboard during {fig['from']}–{fig['to']}, "
                   f"reconstructed from {fig['frames']} video frames with the lecturer "
                   f"removed; {fig['clear']*100:.0f}% of the board is unobstructed.*")
        if rest:
            out += ["", rest]
    if figures:
        out += ["", "---", "",
                "*Figures are reconstructed whiteboards assembled from moments when the "
                "lecturer was not standing in front of each part of the board. Every pixel "
                "is unmodified video; nothing in them is generated. Each shows the board "
                "across the time range given, not a single instant.*"]
    return "\n".join(out), placed


def topic_hint(run_dir):
    notes = Path(run_dir) / "final_lecture_notes.md"
    if notes.exists():
        for line in notes.read_text(encoding="utf-8", errors="ignore").splitlines():
            if line.startswith("# "):
                return line[2:].replace("Lecture Notes:", "").strip()
    return ""


def main():
    ap = argparse.ArgumentParser(description="Regenerate lecture notes from a finished run")
    ap.add_argument("--run-dir", default=None)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--language", default="mixed", choices=LANGUAGES)
    ap.add_argument("--transcript-file", default="transcript_whisper_baseline.txt")
    ap.add_argument("--board-source", default="keywords", choices=("keywords", "boards"))
    ap.add_argument("--min-clear", type=float, default=MIN_CLEAR)
    ap.add_argument("--model", default="Qwen/Qwen2.5-7B-Instruct")
    ap.add_argument("--max-new-tokens", type=int, default=3072)
    ap.add_argument("--four-bit", action="store_true")
    ap.add_argument("--out-name", default=None,
                    help="Defaults to final_lecture_notes_<language>.md")
    ap.add_argument("--dry-run", action="store_true",
                    help="Print the prompt for the first lecture; load no model")
    args = ap.parse_args()

    # The Windows console defaults to cp1252 and chokes on the transcripts.
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass

    if args.all:
        runs = [d for d in sorted(RUNS.iterdir()) if d.is_dir()]
    elif args.run_dir:
        runs = [Path(args.run_dir)]
    else:
        sys.exit("pass --run-dir <dir> or --all")

    generator = None
    for run_dir in runs:
        transcript = load_transcript(run_dir, args.transcript_file)
        if transcript is None:
            print(f"{run_dir.name:<18} skipped: no {args.transcript_file}")
            continue
        board_text, per_era = load_board_content(run_dir, args.board_source)
        figures = load_figures(run_dir, BOARDS / run_dir.name, args.min_clear, per_era)
        hint = topic_hint(run_dir)

        if args.language == "legacy":
            from src.summarizer.generator import MultimodalContext
            ctx = MultimodalContext(english_transcript=transcript, bengali_transcript="",
                                    visual_content=board_text, frames_summary="")
            messages = build_messages("legacy", prompt_context=ctx.to_prompt_context())
        else:
            messages = build_messages(args.language, transcript=transcript,
                                      board_content=board_text, figures=figures,
                                      topic_hint=hint)

        if args.dry_run:
            print("=" * 72)
            print(f"{run_dir.name}  |  language={args.language}  |  "
                  f"transcript={args.transcript_file}  |  board={args.board_source}")
            print(f"{len(transcript)} transcript chars, {len(board_text)} board chars, "
                  f"{len(figures)} figures")
            print("=" * 72)
            for msg in messages:
                body = msg["content"]
                if len(body) > 4000:
                    body = body[:2600] + "\n\n   [... middle trimmed for display ...]\n\n" + body[-1200:]
                print(f"\n----- {msg['role'].upper()} -----\n{body}")
            return 0

        if generator is None:
            from src.summarizer.generator import LectureNoteGenerator
            generator = LectureNoteGenerator(model_name=args.model, use_4bit=args.four_bit)
            generator.load_model()
        tok, model = generator.tokenizer, generator.model
        text = tok.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        import torch
        inputs = tok(text, return_tensors="pt").to(model.device)
        with torch.no_grad():
            out = model.generate(**inputs, max_new_tokens=args.max_new_tokens,
                                 do_sample=False, repetition_penalty=1.05)
        raw = tok.decode(out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True)

        notes, placed = place_figures(raw, figures)
        name = args.out_name or f"final_lecture_notes_{args.language}.md"
        (run_dir / name).write_text(notes, encoding="utf-8")
        meta = {"language": args.language, "transcript_file": args.transcript_file,
                "board_source": args.board_source, "model": args.model,
                "figures_available": len(figures), "figures_placed": sorted(placed)}
        (run_dir / (Path(name).stem + ".json")).write_text(json.dumps(meta, indent=2),
                                                           encoding="utf-8")
        print(f"{run_dir.name:<18} {len(placed)}/{len(figures)} figures placed  "
              f"-> {run_dir / name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
