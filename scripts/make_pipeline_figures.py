"""Pipeline and methodology figures, drawn in TikZ.

The supervisor asked for a pipeline figure with more detail in it, and for
separate figures showing how the parts work: the board reconstruction, and how
the two halves of the system meet. These are drawn rather than photographed,
so they are generated here and compiled to standalone PDFs.

Three figures:

  fig-pipeline-full          the whole system, one lecture video in, two notes out,
                             with the artefact passed between every pair of stages
                             named on the arrow
  fig-board-reconstruction   how a clean board is built out of a video: erase
                             detection splits the recording into eras, a person
                             mask removes the lecturer, and the surviving tiles
                             are assembled
  fig-notes-assembly         how one board and the matching minutes of transcript
                             become one section of a note, including the two checks
                             that can delete text

Counts and measured values that appear in the figures come from RESULTS.md and
are listed in NUMBERS below, in one place, so they can be checked against it.

    python scripts/make_pipeline_figures.py
"""
import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(os.environ.get("THESIS_REPO") or Path(__file__).resolve().parents[1])

# Every figure number in one place. Source: RESULTS.md sections named beside each.
NUMBERS = {
    "recordings": 44,          # 1.9
    "hours_total": "8.33",     # 1.9
    "transcribed": 28,         # 1.9
    "hours_tr": "5.15",        # 1.9
    "segments": 609,           # 1.9
    "boards": 145,             # 1.9
    "tiles_clear": "97.7",     # 4.1
    "cer": "15.8",             # 1.8
    "wer": "42.5",             # 1.8
    "board_recall": "88.8",    # 5.0
    "notes_recall": "89.1",    # 5.4
}

PREAMBLE = r"""
\documentclass[border=10pt]{standalone}
\usepackage{times}
\usepackage{tikz}
\usepackage{amssymb}
\usetikzlibrary{arrows.meta,positioning,fit,backgrounds,calc,shapes.geometric,decorations.pathreplacing}
\begin{document}
\begin{tikzpicture}[
  font=\sffamily\small,
  node distance=6mm,
  stage/.style={rectangle, rounded corners=2pt, draw=black!55, fill=#1,
                minimum height=9mm, inner xsep=4pt, align=center, text=black!88},
  data/.style={rectangle, rounded corners=6pt, draw=black!35, fill=black!4,
               minimum height=8mm, inner xsep=5pt, align=center,
               font=\sffamily\footnotesize, text=black!80},
  model/.style={stage=#1, font=\sffamily\small\bfseries},
  flow/.style={-{Stealth[length=2.2mm]}, draw=black!55, thick, rounded corners=2.5pt},
  thin flow/.style={-{Stealth[length=1.8mm]}, draw=black!40},
  lbl/.style={font=\sffamily\scriptsize, text=black!60, align=center,
              inner sep=1.5pt, fill=white, fill opacity=0.85, text opacity=1},
  grp/.style={rectangle, rounded corners=3pt, draw=black!22, dashed, inner sep=3.5mm},
  grplab/.style={font=\sffamily\footnotesize\bfseries, text=black!55},
  out/.style={stage=#1, font=\sffamily\small\bfseries, minimum height=11mm},
]
"""

CLOSE = r"""
\end{tikzpicture}
\end{document}
"""

# House colours, matching scripts/make_result_figures.py
AUDIO = "blue!8"
VISION = "green!9"
MODELM = "orange!16"
OUTPUT = "green!22"
CHECK = "red!9"
TRAIN = "black!6"


def pipeline_full(n):
    """Laid out top to bottom in two columns.

    The obvious left-to-right chain comes out about five times wider than it is
    tall, which on a portrait page shrinks to the point where none of the labels
    can be read. Running the two halves downwards side by side gives a figure
    close to square that fills a thesis page at full width.
    """
    return PREAMBLE + r"""
\node[data] (video) {Lecture video\\\scriptsize %(recordings)s recordings, %(hours_total)s h};

\node[stage=%(AUDIO)s, below left=11mm and 6mm of video] (audio)
  {Extract audio\\\scriptsize 16 kHz mono};
\node[stage=%(VISION)s, below right=11mm and 6mm of video] (frames)
  {Extract frames\\\scriptsize One every 2 s};

\node[stage=%(AUDIO)s, below=7mm of audio] (seg)
  {Split at quiet points\\\scriptsize 10--25 s, never over 30};
\node[stage=%(VISION)s, below=7mm of frames] (era)
  {Split into board eras\\\scriptsize On erase events};

\node[model=%(MODELM)s, below=7mm of seg] (asr)
  {Whisper large-v3-turbo\\\scriptsize {+} LoRA $r{=}16$, the only trained weights};

%% Where the adapter comes from. Drawn apart and dashed because it happens once,
%% before any lecture is processed, and not for each video that goes through.
\node[stage=%(TRAIN)s, left=11mm of asr, text width=30mm] (train)
  {Corpus\\\scriptsize %(transcribed)s lectures hand-transcribed,\\\scriptsize %(hours_tr)s h,
   %(segments)s timed segments};
\node[stage=%(TRAIN)s, above=6mm of train, text width=30mm] (trainrun)
  {LoRA training\\\scriptsize done once, offline};
\draw[flow, dashed] (train) -- (trainrun);
\draw[flow, dashed] (trainrun.east) to[out=0,in=180] (asr.west);
\node[lbl, below=1.5mm of train, text width=32mm]
  {Built once, not per lecture.\\Section 4.3 describes it.};
\node[stage=%(VISION)s, below=7mm of era] (mosaic)
  {Tile mosaic {+} person mask\\\scriptsize %(tiles_clear)s\%% of tiles clear};

\node[data, below=7mm of asr] (tr)
  {Banglish transcript\\\scriptsize Timed, CER %(cer)s\%%, WER %(wer)s\%%};
\node[stage=%(VISION)s, below=7mm of mosaic] (boxes)
  {Find regions,\\draw numbered boxes};

\node[model=%(MODELM)s, below=7mm of boxes] (vlm)
  {Qwen2.5-VL-7B\\\scriptsize Names and reads each box};
\node[data, below=7mm of vlm] (btxt)
  {Board text per box\\\scriptsize Recall %(board_recall)s\%%};

\node[model=%(MODELM)s, below=24mm of $(tr)!0.5!(btxt)$, text width=46mm,
      minimum height=13mm, inner ysep=5pt] (llm)
  {Qwen2.5-7B-Instruct\\\scriptsize One call per board};

\node[stage=%(CHECK)s, below left=9mm and 3mm of llm] (qc)
  {Quote check\\\scriptsize Word for word,\\\scriptsize else deleted};
\node[stage=%(CHECK)s, below right=9mm and 3mm of llm] (bc)
  {Box reference check\\\scriptsize Must point at\\\scriptsize a box that exists};

\node[out=%(OUTPUT)s, below=9mm of llm, yshift=-15mm, text width=54mm] (notes)
  {Lecture note, Banglish and English\\\scriptsize One section per board, recall %(notes_recall)s\%%};

%% Orthogonal routing throughout. Curved "to[out=..,in=..]" paths between two nodes
%% that share a start anchor loop back over the node they leave, and a path leaving a
%% wide node's south at a shallow angle cuts straight through its own text.
\draw[flow] (video.south) -- ++(0,-3.5mm) -| (audio.north);
\draw[flow] (video.south) -- ++(0,-3.5mm) -| (frames.north);
\draw[flow] (audio) -- (seg);
\draw[flow] (seg) -- (asr);
\draw[flow] (asr) -- (tr);
\draw[flow] (frames) -- (era);
\draw[flow] (era) -- (mosaic);
\draw[flow] (mosaic) -- (boxes);
\draw[flow] (boxes) -- (vlm);
\draw[flow] (vlm) -- (btxt);
\draw[flow] (tr.south) |- (llm.west);
\draw[flow] (btxt.south) |- (llm.east);
\draw[flow] (llm.south) -- ++(0,-4mm) -| (qc.north);
\draw[flow] (llm.south) -- ++(0,-4mm) -| (bc.north);
\draw[flow] (qc.south) |- (notes.west);
\draw[flow] (bc.south) |- (notes.east);

\begin{scope}[on background layer]
  \node[grp, fit=(audio)(seg)(asr)(tr), label={[grplab]above left:Speech}] {};
  \node[grp, fit=(frames)(era)(mosaic)(boxes)(vlm)(btxt),
        label={[grplab]above right:Vision}] {};
\end{scope}
""" % dict(n, AUDIO=AUDIO, VISION=VISION, MODELM=MODELM, OUTPUT=OUTPUT, CHECK=CHECK,
         TRAIN=TRAIN) + CLOSE


def board_reconstruction(n):
    return PREAMBLE + r"""
\node[data] (frames) {Frames of one lecture\\\scriptsize One every 2 s};

\node[stage=%(VISION)s, right=13mm of frames] (erase)
  {Detect erases\\\scriptsize A large drop in ink between\\\scriptsize consecutive frames};
\node[data, right=13mm of erase] (eras)
  {Board eras\\\scriptsize One per whole-board state};

\node[stage=%(VISION)s, below=13mm of eras] (grid)
  {Cut each frame into tiles};
\node[stage=%(CHECK)s, left=13mm of grid] (mask)
  {Person mask\\\scriptsize DeepLabV3 {+} shadow};
\node[stage=%(VISION)s, left=13mm of mask] (score)
  {For every tile, keep the frame\\\scriptsize Where the lecturer is not in it,
   so writing hidden\\\scriptsize in one frame is taken from another};

\node[data, below=13mm of score] (mos)
  {Mosaic of one era\\\scriptsize Every pixel is real camera output};
\node[stage=%(VISION)s, right=13mm of mos] (clean)
  {Display clean-up\\\scriptsize Whitens the background};
\node[out=%(OUTPUT)s, right=13mm of clean, text width=30mm] (final)
  {Clean board\\\scriptsize %(boards)s produced, %(tiles_clear)s\%% of tiles clear};

\draw[flow] (frames) -- (erase);
\draw[flow] (erase) -- (eras);
\draw[flow] (eras) -- (grid);
\draw[flow] (grid) -- (mask);
\draw[flow] (mask) -- (score);
\draw[flow] (score) -- (mos);
\draw[flow] (mos) -- (clean);
\draw[flow] (clean) -- (final);

\node[lbl, below=1mm of clean] {The strokes stay\\camera pixels;\\only the background\\is replaced};
""" % dict(n, VISION=VISION, CHECK=CHECK, OUTPUT=OUTPUT) + CLOSE


def notes_assembly(n):
    return PREAMBLE + r"""
\node[data] (board) {One clean board\\\scriptsize With numbered boxes};
\node[data, below=9mm of board] (btxt) {The box text\\\scriptsize Read by the vision model};
\node[data, below=9mm of btxt] (tr) {The transcript\\\scriptsize Cut at this board's start and end};

\node[model=%(MODELM)s, right=15mm of btxt, text width=36mm, minimum height=12mm] (llm)
  {Qwen2.5-7B-Instruct\\\scriptsize One call for this board};

\node[data, right=15mm of llm] (draft) {Draft section};

\node[stage=%(CHECK)s, right=14mm of draft, yshift=11mm] (q)
  {Every quotation is searched for\\\scriptsize In the transcript, word for word};
\node[stage=%(CHECK)s, right=14mm of draft, yshift=-11mm] (b)
  {Every box number is checked\\\scriptsize Against the boxes that exist};

\node[out=%(OUTPUT)s, right=14mm of q, yshift=-11mm, text width=30mm] (sec)
  {One section of the note};

\draw[flow] (board.east) to[out=0,in=160] (llm.north west);
\draw[flow] (btxt) -- (llm);
\draw[flow] (tr.east) to[out=0,in=-160] (llm.south west);
\draw[flow] (llm) -- (draft);
\draw[flow] (draft.east) to[out=0,in=180] (q.west);
\draw[flow] (draft.east) to[out=0,in=180] (b.west);
\draw[flow] (q.east) to[out=0,in=160] (sec.north west);
\draw[flow] (b.east) to[out=0,in=-160] (sec.south west);

\node[lbl, above=1.5mm of q, text width=38mm]
  {A quotation that is not found\\is deleted, not corrected};
\node[lbl, below=1.5mm of b, text width=38mm]
  {Both counts are written into\\the output file for every page};
\node[lbl, below=2mm of llm, text width=32mm]
  {The model is given the board\\as text, never the answer key};
""" % dict(n, MODELM=MODELM, CHECK=CHECK, OUTPUT=OUTPUT) + CLOSE


def build(name, body, workdir, outdir):
    workdir.mkdir(parents=True, exist_ok=True)
    tex = workdir / (name + ".tex")
    tex.write_text(body, encoding="utf-8")
    for _ in range(2):
        subprocess.run(["pdflatex", "-interaction=nonstopmode", tex.name],
                       cwd=workdir, capture_output=True, text=True, errors="replace")
    pdf = workdir / (name + ".pdf")
    if not pdf.exists():
        log = workdir / (name + ".log")
        errs = ""
        if log.exists():
            errs = "\n".join(l for l in log.read_text(errors="replace").splitlines()
                             if l.startswith("!"))[:700]
        print("  FAILED %s\n%s" % (name, errs))
        return False
    outdir.mkdir(parents=True, exist_ok=True)
    shutil.copy(pdf, outdir / (name + ".pdf"))
    print("  wrote %s" % (outdir / (name + ".pdf")))
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(REPO / "Thesis Defense P3" / "drafts" / "thesis" / "images"))
    ap.add_argument("--work", default=str(Path(os.environ.get("TEMP", ".")) / "pipe_figs"))
    args = ap.parse_args()
    work, out = Path(args.work), Path(args.out)
    ok = True
    ok &= build("fig-pipeline-full", pipeline_full(NUMBERS), work, out)
    ok &= build("fig-board-reconstruction", board_reconstruction(NUMBERS), work, out)
    ok &= build("fig-notes-assembly", notes_assembly(NUMBERS), work, out)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
