"""Architecture diagrams for the three models this thesis runs, in PlotNeuralNet style.

The supervisor asked for a drawing of each model so the team can see what is
happening inside it and decide which to keep. PlotNeuralNet draws the familiar
stack of labelled 3D blocks; this script emits its TikZ and compiles it.

Every dimension in these figures is read from the model's own config.json, not
typed in, so a figure cannot drift from the model it claims to describe. The
sources are:

  whisper-large-v3-turbo   the snapshot in the local HF cache
  Qwen2.5-VL-7B-Instruct   config.json fetched to scratch (see --qwen-config-dir)
  Qwen2.5-7B-Instruct      the same
  the LoRA adapter         artifacts/ft_work_final5h_lr1e3/lora_lr1e3

Each diagram carries a real example travelling through it, because a block
diagram with no data in it does not show what the model does. The example is the
same lecture clip and the same board throughout, so the three figures read as one
pipeline.

PlotNeuralNet's own to_head() uses \\subimport, which needs import.sty, and this
machine's MiKTeX cannot fetch it. So the style files are copied next to the
generated .tex and pulled in with \\input instead.

    python scripts/make_arch_figures.py --out "Thesis Defense P3/drafts/thesis/images"
"""
import argparse
import json
import glob
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(os.environ.get("THESIS_REPO") or Path(__file__).resolve().parents[1])
PNN = Path(os.environ.get("PLOTNEURALNET") or r"F:\thesisP2\PlotNeuralNet")
sys.path.insert(0, str(PNN))

from pycore.tikzeng import (to_Conv, to_ConvConvRelu, to_ConvRes, to_Pool,  # noqa: E402
                            to_SoftMax, to_connection, to_input, to_skip)


# ----------------------------------------------------------------- dimensions

def whisper_dims():
    hits = glob.glob(str(Path(os.environ.get("HF_HOME", r"F:\thesisP2\hf_cache")) /
                         "hub/models--openai--whisper-large-v3-turbo/snapshots/*/config.json"))
    if not hits:
        raise SystemExit("whisper config not found in the HF cache")
    return json.loads(Path(hits[0]).read_text(encoding="utf-8"))


def lora_dims():
    hits = glob.glob(str(REPO.parent / "ft_work_final5h_lr1e3" / "*" / "adapter_config.json"))
    if not hits:
        raise SystemExit("LoRA adapter_config.json not found")
    return json.loads(Path(sorted(hits)[0]).read_text(encoding="utf-8"))


def qwen_dims(cfg_dir, name):
    p = Path(cfg_dir) / ("cfg_%s.json" % name)
    if not p.exists():
        raise SystemExit("missing %s; fetch it with curl from the model repo" % p)
    return json.loads(p.read_text(encoding="utf-8"))


# ----------------------------------------------------------------- boilerplate

def head():
    """PlotNeuralNet's preamble without \\subimport, so import.sty is not needed."""
    return r"""
\documentclass[border=8pt, multi, tikz]{standalone}
\usepackage{times}
\usetikzlibrary{positioning}
\usetikzlibrary{3d}
\input{init.tex}
"""


def colours():
    return r"""
\def\ConvColor{rgb:yellow,5;red,2.5;white,5}
\def\ConvReluColor{rgb:yellow,5;red,5;white,5}
\def\PoolColor{rgb:red,1;black,0.3}
\def\UnpoolColor{rgb:blue,2;green,1;black,0.3}
\def\FcColor{rgb:blue,5;red,2.5;white,5}
\def\FcReluColor{rgb:blue,5;red,5;white,4}
\def\SoftmaxColor{rgb:magenta,5;black,7}
\def\SumColor{rgb:blue,5;green,15}
\def\VisionColor{rgb:green,5;blue,2;white,6}
\def\LoraColor{rgb:red,5;yellow,2;white,4}
\def\TextColor{rgb:blue,3;green,4;white,7}
"""


def begin():
    return r"""
\newcommand{\copymidarrow}{\tikz \draw[-Stealth,line width=0.8mm,draw={rgb:blue,4;red,1;green,1;black,3}] (-0.3,0) -- ++(0.3,0);}
\begin{document}
%% scale shrinks the coordinates but not the text, because transform shape is off.
%% That is the point: the drawing gets narrower in centimetres while the labels stay the
%% same number of points, so the figure needs far less shrinking to fit the text width
%% of a portrait page, and the labels survive at print size.
\begin{tikzpicture}[scale=0.62]
\tikzstyle{connection}=[ultra thick,every node/.style={sloped,allow upside down},draw=\edgecolor,opacity=0.7]
\tikzstyle{copyconnection}=[ultra thick,every node/.style={sloped,allow upside down},draw={rgb:blue,4;red,1;green,1;black,3},opacity=0.7]
\tikzstyle{note}=[font=\small, align=center, text=black!75]
\tikzstyle{example}=[font=\small\itshape, align=left, text=black!80,
                     fill=black!4, rounded corners=2pt, inner sep=4pt]
"""


def end():
    return r"""
\end{tikzpicture}
\end{document}
"""


# Annotation is kept deliberately thin. PlotNeuralNet already prints a caption
# under each block and the tensor sizes on its edges, so anything more collides
# with them. One short line per block, all on the same baseline so they read as a
# row, and the real explanation goes in the figure's caption in the thesis.

def input_picture(pathfile, name, x, width_cm, caption, cap_width="6.0cm"):
    """The real input, drawn flat to the left of the stack.

    Not PlotNeuralNet's to_input: that puts the picture on the zy plane, and the view
    transform then mirrors it and turns it upside down. A spectrogram survives that
    badly and a photograph of handwriting does not survive it at all, since the board
    came out reversed, with the handwriting on the board running right to left. A plain node keeps the image
    the right way round, which is the whole point of showing our own data.
    """
    return (r"""
\node[anchor=east, inner sep=0pt] (%s) at (%.2f,0) {\includegraphics[width=%.1fcm]{%s}};
\node[anchor=north, font=\sffamily\scriptsize, text=black!65, align=center,
      text width=%s] at (%s.south) [yshift=-2mm] {%s};
""" % (name, x, width_cm, pathfile, cap_width, name, caption))


def note(anchor, text, y=-9.8, width="2.9cm"):
    """One short line, hung from a fixed depth below the whole stack."""
    return (r"\node[note, text width=%s, anchor=north] at (%s-south |- 0,%s) {%s};"
            % (width, anchor, y, text)) + "\n"


def example(anchor, text, y=7.4, width="4.8cm", anchor_side="south"):
    """The worked example, parked well above the stack so it clears the blocks."""
    return (r"\node[example, text width=%s, anchor=%s] at (%s-north |- 0,%s) {%s};"
            % (width, anchor_side, anchor, y, text)) + "\n"


def fig_whisper(cfg, lora):
    d = cfg["d_model"]
    mel, src = cfg["num_mel_bins"], cfg["max_source_positions"]
    enc, dec = cfg["encoder_layers"], cfg["decoder_layers"]
    heads, ffn = cfg["encoder_attention_heads"], cfg["encoder_ffn_dim"]
    vocab, tgt = cfg["vocab_size"], cfg["max_target_positions"]
    r, alpha = lora["r"], lora["lora_alpha"]
    # Module names carry underscores, which are a subscript in LaTeX text mode.
    targets = ", ".join(t.replace("_", r"\_") for t in sorted(lora["target_modules"]))

    a = [head(), colours(), begin()]
    # The real input: 17.1 s of one held-out lecture clip, and the log-Mel array
    # Whisper's own feature extractor makes of it.
    a.append(input_picture(
        "input-mel.png", "melimg", -2.2, 6.4,
        r"The log-Mel array of one held-out clip,\\BanglaASR11 clip 41, 17.1 s, exactly "
        r"as Whisper's own feature extractor produces it", cap_width="6.4cm"))
    a.append(to_Conv("mel", "", mel, offset="(0,0,0)", to="(0,0,0)",
                     width=2, height=44, depth=22, caption="Mel"))
    a.append(note("mel", y=-11.0, text=r"%d mel bins\\$\times$ %d frames" % (mel, src * 2)))

    a.append(to_ConvConvRelu("conv", "", ("", ""), offset="(3.0,0,0)", to="(mel-east)",
                             width=(2, 2), height=36, depth=26, caption="Conv1d $\\times$2"))
    a.append(to_connection("mel", "conv"))
    a.append(note("conv", r"Stride 2, so\\%d become %d" % (src * 2, src)))

    a.append(to_Conv("enc", "", d, offset="(3.2,0,0)", to="(conv-east)",
                     width=9, height=36, depth=20, caption="Encoder"))
    a.append(to_connection("conv", "enc"))
    a.append(note("enc", r"%d layers\\%d heads, FFN %d" % (enc, heads, ffn)))

    a.append(to_Conv("dec", "", d, offset="(3.6,0,0)", to="(enc-east)",
                     width=3, height=26, depth=16, caption="Decoder"))
    a.append(to_connection("enc", "dec"))
    a.append(note("dec", r"Only %d layers,\\cross-attends" % dec))

    a.append(to_SoftMax("out", "", offset="(3.0,0,0)", to="(dec-east)",
                        width=1.5, height=26, depth=16, caption="Token"))
    a.append(to_connection("dec", "out"))
    a.append(note("out", r"Vocabulary\\%d" % vocab))

    # What the fine-tuned model really returned for this clip, from eval_lr1e3.json.

    # LoRA is the only thing trained, so it is drawn as a separate small path in
    # its own colour rather than reusing the encoder's.
    a.append(r"""
\pic[shift={(0,-12.6,0)}] at (enc-west)
    {Box={
        name=lora, caption=LoRA,
        fill=\LoraColor, height=10, width=1.2, depth=10
        }
    };
""")
    a.append(r"""
\node[note, text width=6.0cm, anchor=west] at (lora-east |- 0,-13.3)
  {\textbf{The only trained weights.} Rank $r=%d$, $\alpha=%d$, on %s of every attention
   block in the encoder and the decoder. Everything else stays frozen.};
%% The risers are pushed sideways off the block centres, because the size labels
%% under each block sit exactly there and a dashed line through them is unreadable.
\draw[->,thick,draw=\LoraColor,dashed,rounded corners]
  (lora-north) -- (lora-north |- 0,-11.4) -| ([xshift=-2.9cm] enc-south);
\draw[->,thick,draw=\LoraColor,dashed,rounded corners]
  (lora-north) -- (lora-north |- 0,-11.4) -| ([xshift=2.6cm] dec-south);
""" % (r, alpha, targets))
    a.append(end())
    return "".join(a)


# ----------------------------------------------------------------- figure two

def fig_qwen_vl(cfg, board_img):
    v = cfg["vision_config"]
    d = cfg["hidden_size"]
    layers, heads = cfg["num_hidden_layers"], cfg["num_attention_heads"]
    kv, ffn = cfg["num_key_value_heads"], cfg["intermediate_size"]
    patch, merge, depth = v["patch_size"], v["spatial_merge_size"], v["depth"]
    vhid, vout_dim = v["hidden_size"], v["out_hidden_size"]

    a = [head(), colours(), begin()]
    if board_img:
        # The real board this lecture left behind, with the boxes our code drew
        # and numbered. This is the image the model is actually sent.
        a.append(input_picture(
            Path(board_img).name, "boardimg", -2.2, 8.4,
            r"The rebuilt board of BanglaASR11 with the numbered boxes drawn by our "
            r"code,\\which is the image the model is actually sent", cap_width="8.4cm"))
    # No corner labels on this block. PlotNeuralNet draws the depth label rotated along
    # the box's receding edge, where it collides with the horizontal label and reads as
    # broken type. The note underneath gives both numbers in plain text.
    a.append(to_Conv("patch", "", "",
                     offset="(0,0,0)", to="(0,0,0)", width=2, height=40, depth=24,
                     caption="Patches"))
    a.append(note("patch", r"%d$\times$%d pixel patches,\\3 colour channels"
                  % (patch, patch)))

    a.append(to_Conv("vit", "", vhid, offset="(3.2,0,0)", to="(patch-east)",
                     width=7, height=36, depth=20, caption="Vision encoder"))
    a.append(to_connection("patch", "vit"))
    a.append(note("vit", r"%d layers,\\width %d" % (depth, vhid)))

    a.append(to_Pool("merge", offset="(3.2,0,0)", to="(vit-east)", width=2, height=26,
                     depth=16, caption="Merge"))
    a.append(to_connection("vit", "merge"))
    a.append(note("merge", r"%d$\times$%d patches merged,\\projected to %d"
                  % (merge, merge, vout_dim)))

    a.append(to_Conv("llm", "", d, offset="(3.4,0,0)", to="(merge-east)",
                     width=8, height=34, depth=20, caption="Language model"))
    a.append(to_connection("merge", "llm"))
    a.append(note("llm", r"%d layers, width %d,\\%d heads over %d\\key-value heads"
                  % (layers, d, heads, kv)))

    a.append(to_SoftMax("vout", "", offset="(3.2,0,0)", to="(llm-east)", width=1.5,
                        height=26, depth=16, caption="Text"))
    a.append(to_connection("llm", "vout"))
    a.append(note("vout", r"One answer per box,\\returned as JSON"))

    a.append(example("patch", r"\textbf{The prompt joins the image here:} \emph{``for each "
                     r"numbered box, give a short name and transcribe exactly what is "
                     r"written''}", anchor_side="south west", width="5.4cm"))
    a.append(end())
    return "".join(a)


# --------------------------------------------------------------- figure three

def fig_qwen_llm(cfg):
    d = cfg["hidden_size"]
    layers, heads = cfg["num_hidden_layers"], cfg["num_attention_heads"]
    kv, ffn = cfg["num_key_value_heads"], cfg["intermediate_size"]
    vocab, ctx = cfg["vocab_size"], cfg["max_position_embeddings"]

    a = [head(), colours(), begin()]
    # The real input: the transcript of these minutes and the board text the
    # vision model returned for the same lecture.
    a.append(input_picture(
        "input-prompt.png", "promptimg", -2.2, 7.4,
        r"The real transcript and board text for one board of BanglaASR11",
        cap_width="7.4cm"))
    a.append(to_Conv("tok", "", vocab, offset="(0,0,0)", to="(0,0,0)", width=2,
                     height=40, depth=20, caption="Tokens"))
    a.append(note("tok", r"Vocabulary %d,\\context %d tokens" % (vocab, ctx)))

    a.append(to_Conv("body", "", d, offset="(4.4,0,0)", to="(tok-east)", width=10,
                     height=36, depth=20, caption="Decoder stack"))
    a.append(to_connection("tok", "body"))
    a.append(note("body", r"%d layers, width %d,\\%d heads over %d key-value\\heads, FFN %d"
                  % (layers, d, heads, kv, ffn), width="4.0cm"))

    a.append(to_SoftMax("nout", "", offset="(4.4,0,0)", to="(body-east)", width=1.5,
                        height=26, depth=16, caption="Note"))
    a.append(to_connection("body", "nout"))
    a.append(note("nout", r"Markdown, one section\\per board"))

    a.append(example("tok", r"\textbf{Plus the instruction:} \emph{``write the note for "
                     r"this board, quoting the lecturer word for word and pointing at the "
                     r"boxes by number''}", anchor_side="south west", width="5.2cm"))
    a.append(r"""
\node[note, text width=8.4cm, anchor=north] at (body-south |- 0,-12.6)
  {This model never sees the board. It receives only the text the vision model returned,
   which is what makes the note checkable: every fact in it can be traced to a line of
   that text or to the transcript.};
""")
    a.append(end())
    return "".join(a)


# ----------------------------------------------------------------------- main

def build(name, body, workdir, outdir, images=()):
    workdir.mkdir(parents=True, exist_ok=True)
    for f in ["init.tex", "Box.sty", "RightBandedBox.sty", "Ball.sty"]:
        shutil.copy(PNN / "layers" / f, workdir / f)
    # The images live under a path with spaces in it, which pdflatex will not
    # take, so they are copied in and referenced by bare filename.
    for img in images:
        src = Path(img)
        if src.exists():
            shutil.copy(src, workdir / src.name)
        else:
            print("  missing input image: %s" % src)
    tex = workdir / (name + ".tex")
    tex.write_text(body, encoding="utf-8")
    for _ in range(2):
        proc = subprocess.run(["pdflatex", "-interaction=nonstopmode", tex.name],
                              cwd=workdir, capture_output=True, text=True, errors="replace")
    pdf = workdir / (name + ".pdf")
    if not pdf.exists():
        log = (workdir / (name + ".log"))
        msg = ""
        if log.exists():
            msg = "\n".join(l for l in log.read_text(errors="replace").splitlines()
                            if l.startswith("!"))[:600]
        print("  FAILED %s\n%s" % (name, msg))
        return False
    outdir.mkdir(parents=True, exist_ok=True)
    shutil.copy(pdf, outdir / (name + ".pdf"))
    print("  wrote %s" % (outdir / (name + ".pdf")))
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(REPO / "Thesis Defense P3" / "drafts" / "thesis" / "images"))
    ap.add_argument("--work", default=str(Path(os.environ.get("TEMP", ".")) / "arch_figs"))
    ap.add_argument("--qwen-config-dir", required=True,
                    help="directory holding cfg_Qwen2.5-VL-7B-Instruct.json and cfg_Qwen2.5-7B-Instruct.json")
    ap.add_argument("--board-image", default=None,
                    help="an annotated board image to show as the example input")
    args = ap.parse_args()

    work, out = Path(args.work), Path(args.out)
    w, l = whisper_dims(), lora_dims()
    vl = qwen_dims(args.qwen_config_dir, "Qwen2.5-VL-7B-Instruct")
    llm = qwen_dims(args.qwen_config_dir, "Qwen2.5-7B-Instruct")

    print("dimensions read from the model configs:")
    print("  whisper  d_model %d, encoder %d, decoder %d, mel %d, vocab %d"
          % (w["d_model"], w["encoder_layers"], w["decoder_layers"],
             w["num_mel_bins"], w["vocab_size"]))
    print("  lora     r %d, alpha %d, on %s" % (l["r"], l["lora_alpha"],
                                                ",".join(sorted(l["target_modules"]))))
    print("  qwen-vl  vision depth %d width %d, llm %d layers width %d"
          % (vl["vision_config"]["depth"], vl["vision_config"]["hidden_size"],
             vl["num_hidden_layers"], vl["hidden_size"]))
    print("  qwen-llm %d layers, width %d, ctx %d"
          % (llm["num_hidden_layers"], llm["hidden_size"], llm["max_position_embeddings"]))

    ok = True
    # The worked example travelling through all three figures is one moment of one
    # lecture: clip 11 of BanglaASR11 and the board that lecture left behind.
    imgs = Path(args.out)
    ok &= build("fig-arch-whisper", fig_whisper(w, l), work, out,
                images=[imgs / "input-mel.png", imgs / "input-waveform.png"])
    ok &= build("fig-arch-qwen-vl", fig_qwen_vl(vl, args.board_image), work, out,
                images=[args.board_image] if args.board_image else ())
    ok &= build("fig-arch-qwen-llm", fig_qwen_llm(llm), work, out,
                images=[imgs / "input-prompt.png"])
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
