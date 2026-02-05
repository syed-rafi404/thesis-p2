# Thesis Figure Creation Guide
## Multimodal Banglish Classroom Summarizer

This guide provides instructions for creating all thesis figures. Python-generated figures are already complete; manual diagrams need to be created using draw.io, Figma, or similar tools.

---

## ✅ COMPLETED (Python-Generated & Embedded in LaTeX)

Located in `P2/figures/` (PNG + PDF formats) and **already referenced in chapters**:

| Figure | File | Chapter | LaTeX Label | Section |
|--------|------|---------|-------------|---------|
| 5.7 | `fig_5_7_dataset_distribution` | Ch5 | `fig:dataset_distribution` | §5.4 (After Table 5.4) |
| 6.1 | `fig_6_1_per_video_f1` | Ch6 | `fig:per_video_f1` | §6.3 (After Table 6.3) |
| 6.2 | `fig_6_2_precision_recall` | Ch6 | `fig:precision_recall` | §6.3 (After Fig 6.1) |
| 6.3 | `fig_6_3_domain_comparison` | Ch6 | `fig:domain_comparison` | §6.4 (After Table 6.4) |
| 6.4 | `fig_6_4_ablation_study` | Ch6 | `fig:ablation_study` | §6.5 (After Table 6.5) |
| 6.5 | `fig_6_5_failure_modes` | Ch6 | `fig:failure_modes` | §6.6 (After Table 6.6) |
| 6.6 | `fig_6_6_visual_bias` | Ch6 | `fig:visual_bias` | §6.5 (After Table 6.7) |
| Bonus | `fig_summary_results` | — | N/A | For presentations |

---

## 📐 TO CREATE MANUALLY

---

### Figure 5.1: Research Methodology Framework

**LaTeX Label:** `fig:methodology`  
**Placement:** Chapter 5, Section 5.2 (line ~64), after "Figure~\ref{fig:methodology} illustrates the four-phase framework..."  
**File Name:** `fig_5_1_methodology.pdf`

**ASCII Layout:**
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│    PHASE 1      │    │    PHASE 2      │    │    PHASE 3      │    │    PHASE 4      │
│   Requirements  │───▶│ Data Collection │───▶│ Implementation  │───▶│  Evaluation     │
│    Analysis     │    │   & Annotation  │    │  & Integration  │    │ & Experiments   │
└────────┬────────┘    └────────┬────────┘    └────────┬────────┘    └────────┬────────┘
         ▼                      ▼                      ▼                      ▼
   ┌───────────┐          ┌───────────┐          ┌───────────┐          ┌───────────┐
   │ Literature│          │ 9 Videos  │          │ Functional│          │ Results & │
   │  Review   │          │ 73K chars │          │  System   │          │ Insights  │
   └───────────┘          └───────────┘          └───────────┘          └───────────┘
```

**🤖 Figma AI Prompt:**
```
Create a professional horizontal research methodology flowchart for an academic thesis with 4 connected phases:

Phase 1: "Requirements Analysis" - outputs "Literature Review, Architecture Design"
Phase 2: "Data Collection & Annotation" - outputs "9 Videos, 73K characters Ground Truth"  
Phase 3: "Implementation & Integration" - outputs "Functional System Codebase"
Phase 4: "Evaluation & Experiments" - outputs "Results & Insights (Chapter 6)"

Style: Clean academic look with rounded rectangles, blue gradient (#3498DB to #2980B9), white text, thick arrows connecting phases left-to-right. Each phase box should have a smaller output box below it connected by a downward arrow. Use sans-serif font (Arial/Helvetica). White background, professional look suitable for IEEE/ACM publication.
```

**LaTeX Code to Add (after line ~82 in chapter_5.tex):**
```latex
\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.95\textwidth]{figures/fig_5_1_methodology.pdf}
    \caption{Research methodology framework showing the four-phase iterative approach: requirements analysis, data collection, implementation, and evaluation.}
    \label{fig:methodology}
\end{figure}
```

---

### Figure 5.2: System Architecture Overview

**LaTeX Label:** `fig:architecture`  
**Placement:** Chapter 5, Section 5.3.1 (line ~99), after "Figure~\ref{fig:architecture} presents the complete system architecture..."  
**File Name:** `fig_5_2_architecture.pdf`

**ASCII Layout:**
```
┌─────────────┐    ┌─────────────────────────────────────────────────────┐    ┌─────────────┐
│             │    │              PROCESSING PIPELINE                    │    │             │
│   VIDEO     │    │  ┌─────────┐   ┌─────────┐   ┌─────────────────┐   │    │  STRUCTURED │
│   INPUT     │───▶│  │ Module 1│──▶│ Module 2│──▶│    Module 3     │   │───▶│   SUMMARY   │
│  (.mp4)     │    │  │   ASR   │   │   VLM   │   │ Cross-Modal     │   │    │   (JSON)    │
│             │    │  │ Whisper │   │Qwen2.5-VL   │ Fusion + LLM    │   │    │             │
└─────────────┘    │  └─────────┘   └─────────┘   └─────────────────┘   │    └─────────────┘
                   └─────────────────────────────────────────────────────┘
```

**🤖 Figma AI Prompt:**
```
Create a system architecture diagram for a multimodal lecture summarization pipeline:

INPUT (left): Video file icon with ".mp4" label, gray box
PROCESSING PIPELINE (center, large container box):
  - Module 1: "ASR" with "Whisper large-v3-turbo" subtitle, BLUE (#3498DB)
  - Module 2: "VLM" with "Qwen2.5-VL-7B" subtitle, GREEN (#27AE60)
  - Module 3: "Cross-Modal Fusion" with "Qwen2.5-7B" subtitle, PURPLE (#9B59B6)
  - Connect modules with thick arrows showing data flow
OUTPUT (right): Document icon with "Structured Summary (JSON)" label

Style: Modern tech diagram, rounded corners, subtle shadows, clean lines. Use icons for video (film icon) and output (document icon). Label each module clearly with model names in smaller text. White background, professional look.
```

**LaTeX Code to Add (after line ~151 in chapter_5.tex):**
```latex
\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.95\textwidth]{figures/fig_5_2_architecture.pdf}
    \caption{High-level system architecture showing the three-module pipeline: ASR processing (Whisper), visual keyword extraction (Qwen2.5-VL), and cross-modal fusion with summary generation (Qwen2.5).}
    \label{fig:architecture}
\end{figure}
```

---

### Figure 5.3: Whisper ASR Processing Pipeline

**LaTeX Label:** `fig:whisper_flow`  
**Placement:** Chapter 5, Section 5.3.2 (line ~292), after "Figure~\ref{fig:whisper_flow} illustrates the internal processing flow..."  
**File Name:** `fig_5_3_whisper_flow.pdf`

**ASCII Layout:**
```
┌──────────────┐
│ Audio Track  │
│  Extraction  │
└──────┬───────┘
       ▼
┌──────────────┐
│  16kHz Mono  │
│  Resampling  │
└──────┬───────┘
       ▼
┌──────────────┐
│  Log-Mel     │
│ Spectrogram  │
│  (80 bins)   │
└──────┬───────┘
       ▼
┌──────────────┐
│   Whisper    │
│large-v3-turbo│
│ (32L Encoder │
│ + 32L Decoder)│
└──────┬───────┘
       ▼
┌──────────────┐     ┌──────────────┐
│    Raw       │────▶│   Cleaning   │
│ Transcript   │     │   Pipeline   │
└──────────────┘     └──────┬───────┘
                            ▼
                     ┌──────────────┐
                     │   Cleaned    │
                     │  Transcript  │
                     └──────────────┘
```

**🤖 Figma AI Prompt:**
```
Create a vertical flowchart showing the Whisper ASR processing pipeline:

Steps (top to bottom):
1. "Audio Track Extraction" - input step, light gray
2. "16kHz Mono Resampling" - preprocessing, light blue
3. "Log-Mel Spectrogram (80 frequency bins)" - feature extraction, medium blue
4. "Whisper large-v3-turbo" - main model box (larger, highlighted), dark blue (#3498DB), include subtitle "32-layer Encoder + 32-layer Decoder"
5. "Raw Transcript" - output, splits into two paths
6. Side branch: "Cleaning Pipeline" box listing: "• Repetition removal (3+ consecutive)", "• Filler word filtering", "• Hallucination detection"
7. "Cleaned Transcript" - final output, green border

Style: Vertical flow with rounded rectangles, consistent spacing, thick downward arrows. Use blue gradient for Whisper box. Clean academic style with clear labels.
```

**LaTeX Code to Add (after line ~288 in chapter_5.tex):**
```latex
\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.7\textwidth]{figures/fig_5_3_whisper_flow.pdf}
    \caption{Whisper ASR processing pipeline showing audio preprocessing, feature extraction, model inference, and post-processing stages.}
    \label{fig:whisper_flow}
\end{figure}
```

---

### Figure 5.4: Keyframe Sampling Strategy

**LaTeX Label:** `fig:frame_sampling`  
**Placement:** Chapter 5, Section 5.3.3 (line ~379), after "Figure~\ref{fig:frame_sampling} illustrates the sampling strategy..."  
**File Name:** `fig_5_4_frame_sampling.pdf`

**ASCII Layout:**
```
Video Timeline (10 minutes)
├────┼────┼────┼────┼────┼────┼────┼────┼────┼────┤
0    1    2    3    4    5    6    7    8    9   10 min

Sampling Points (20-second intervals = 30 frames):
│    │    │    │    │    │    │    │    │    │    │
▼    ▼    ▼    ▼    ▼    ▼    ▼    ▼    ▼    ▼    ▼

Sample Keyframes:
[🖼️ Code]  [🖼️ Slide]  [🖼️ Whiteboard]  [🖼️ IDE]
  t=0:00      t=0:40       t=2:20         t=5:00
```

**🤖 Figma AI Prompt:**
```
Create a timeline diagram showing video keyframe sampling strategy:

TOP: Horizontal timeline bar from 0 to 10 minutes with minute markers, blue gradient bar
MIDDLE: Vertical tick marks at 20-second intervals showing sampling points (total 30 frames for 10-min video)
BOTTOM: 4 example keyframe thumbnails showing typical classroom content:
  - Frame 1: Code/IDE screenshot (t=0:00) - blue border
  - Frame 2: Slide with bullet points (t=0:40) - green border
  - Frame 3: Whiteboard with handwriting (t=2:20) - orange border
  - Frame 4: Terminal/console output (t=5:00) - purple border

Add label: "Uniform Sampling: 1 frame per 20 seconds"
Add annotation: "30 frames extracted from 10-minute lecture"

Style: Clean infographic style, use placeholder rectangles for thumbnails with icons representing content type. Include timestamps under each thumbnail.
```

**LaTeX Code to Add (after line ~377 in chapter_5.tex):**
```latex
\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.9\textwidth]{figures/fig_5_4_frame_sampling.pdf}
    \caption{Keyframe sampling strategy: uniform extraction at 20-second intervals produces 30 frames for a 10-minute lecture, capturing code, slides, whiteboard content, and terminal displays.}
    \label{fig:frame_sampling}
\end{figure}
```

---

### Figure 5.5: Visual Keyword Aggregation Process

**LaTeX Label:** `fig:visual_aggregation`  
**Placement:** Chapter 5, Section 5.3.3 (after line ~464), add reference in text  
**File Name:** `fig_5_5_visual_aggregation.pdf`

**ASCII Layout:**
```
┌─────────────────────────────────────────────────────────────┐
│                    KEYFRAMES (30 frames)                     │
│  [F1] [F2] [F3] [F4] [F5] ... [F30]                         │
└─────────────────────────┬───────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────┐
│              Qwen2.5-VL-7B Processing                        │
│  Prompt: "Extract programming terms from this image"         │
└─────────────────────────┬───────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  F1: ["variable", "int", "print"]                           │
│  F2: ["variable", "string", "input"]                        │
│  F3: ["loop", "for", "range"]                               │
│  F4: ["variable", "list", "append"]                         │
└─────────────────────────┬───────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  AGGREGATED: {"variable": 3, "loop": 1, "for": 1, ...}     │
└─────────────────────────────────────────────────────────────┘
```

**🤖 Figma AI Prompt:**
```
Create a process flow diagram showing visual keyword aggregation:

STEP 1 (top): Row of small frame thumbnails labeled F1, F2, F3... F30 representing keyframes, in a container box labeled "KEYFRAMES (30 frames)"
Arrow down to:

STEP 2: Green box (#27AE60) labeled "Qwen2.5-VL-7B Processing" with prompt text: "Extract programming/technical terms from this classroom image"
Arrow down to:

STEP 3: Box showing per-frame extraction results in monospace font:
  F1: ["variable", "int", "print"]
  F2: ["variable", "string", "input"]  
  F3: ["loop", "for", "range"]
  F4: ["variable", "list", "append"]
Arrow down to:

STEP 4: Final aggregation box titled "Frequency Aggregation" with:
  "variable": 3 occurrences → HIGH CONFIDENCE
  "loop": 1 occurrence → MEDIUM CONFIDENCE
  Output: {"variable": 3, "int": 1, "print": 1, ...}

Style: Vertical flow, use code-style monospace font for keywords, highlight high-frequency terms in green. Green color scheme (#27AE60) for VLM components.
```

**LaTeX Code to Add (after line ~464 in chapter_5.tex):**
```latex
\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.85\textwidth]{figures/fig_5_5_visual_aggregation.pdf}
    \caption{Visual keyword aggregation process: Qwen2.5-VL extracts terms from each keyframe, which are then aggregated by frequency to identify high-confidence visual keywords.}
    \label{fig:visual_aggregation}
\end{figure}
```

---

### Figure 5.6: Cross-Modal Verification Fusion

**LaTeX Label:** `fig:fusion_flow`  
**Placement:** Chapter 5, Section 5.3.4 (line ~507), after "Figure~\ref{fig:fusion_flow} illustrates the complete fusion workflow."  
**File Name:** `fig_5_6_fusion_flow.pdf`

**ASCII Layout:**
```
                    ┌─────────────────┐
                    │  ASR Keyword    │
                    │  Candidate (w)  │
                    └────────┬────────┘
                             ▼
              ┌──────────────────────────────┐
              │  Exact Match in Visual Set?  │
              │       w ∈ V_keywords         │
              └──────────────┬───────────────┘
                      ┌──────┴──────┐
                     YES            NO
                      ▼              ▼
              ┌───────────┐  ┌──────────────────────┐
              │   KEEP    │  │  Fuzzy Match > 0.85? │
              │   (HIGH)  │  │  max(sim(w,v))       │
              └───────────┘  └──────────┬───────────┘
                                  ┌─────┴─────┐
                                 YES         NO
                                  ▼           ▼
                          ┌───────────┐  ┌──────────┐
                          │   KEEP    │  │  REMOVE  │
                          │  (MEDIUM) │  │(Halluc.) │
                          └───────────┘  └──────────┘
```

**🤖 Figma AI Prompt:**
```
Create a decision flowchart for cross-modal verification fusion in ASR:

START: "ASR Keyword Candidate (w)" - input box at top, blue (#3498DB)

DECISION 1 (diamond shape, yellow #F1C40F): "Exact Match in Visual Keywords? w ∈ V"
  - YES branch → Green box (#27AE60) "KEEP (High Confidence)" 
  - NO branch → continues down

DECISION 2 (diamond shape, yellow #F1C40F): "Fuzzy Match Score > 0.85? max(similarity(w,v))"
  - YES branch → Light green box (#2ECC71) "KEEP (Medium Confidence)"
  - NO branch → Red box (#E74C3C) "REMOVE (Potential Hallucination)"

Color scheme:
- Decision diamonds: Yellow (#F1C40F) with black text
- KEEP boxes: Green shades (#27AE60 for high, #2ECC71 for medium)
- REMOVE box: Red (#E74C3C) with white text
- Input box: Blue (#3498DB)

Style: Clean flowchart with rounded rectangles for processes, diamonds for decisions, clear YES/NO labels on branches. Include the mathematical notation. Professional academic look.
```

**LaTeX Code to Add (after line ~559 in chapter_5.tex):**
```latex
\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.75\textwidth]{figures/fig_5_6_fusion_flow.pdf}
    \caption{Cross-modal verification fusion workflow: ASR keyword candidates are verified against visual keywords through exact matching and fuzzy matching (threshold 0.85) before being included in the final output.}
    \label{fig:fusion_flow}
\end{figure}
```

---

### Figure 5.8: Preprocessing Pipeline

**LaTeX Label:** `fig:preprocessing_pipeline`  
**Placement:** Chapter 5, Section 5.5.1 (line ~876), after "Figure~\ref{fig:preprocessing_pipeline} illustrates the complete preprocessing workflow."  
**File Name:** `fig_5_8_preprocessing.pdf`

**ASCII Layout:**
```
          ┌─────────────────────────────────┐
          │   INPUT: Raw Video File (.mp4)  │
          └───────────────┬─────────────────┘
                   ┌──────┴──────┐
                   │             │
                   ▼             ▼
          ┌─────────────┐ ┌─────────────┐
          │   AUDIO     │ │   VIDEO     │
          │ EXTRACTION  │ │  SAMPLING   │
          │  (ffmpeg)   │ │  (OpenCV)   │
          └──────┬──────┘ └──────┬──────┘
                 ▼               ▼
          ┌─────────────┐ ┌─────────────┐
          │  Resample   │ │   Extract   │
          │  to 16kHz   │ │   Frames    │
          │    Mono     │ │ @20s interval│
          └──────┬──────┘ └──────┬──────┘
                 ▼               ▼
          ┌─────────────┐ ┌─────────────┐
          │   Audio     │ │   30 JPG    │
          │   Tensor    │ │   Frames    │
          └─────────────┘ └─────────────┘
```

**🤖 Figma AI Prompt:**
```
Create a preprocessing pipeline diagram with parallel audio and video tracks:

INPUT (top center): "Raw Video File (.mp4)" with video icon, gray box

Split into two parallel paths:

LEFT PATH (Audio - Blue #3498DB):
1. "Audio Track Extraction" with "(ffmpeg)" subtitle
2. "Resample to 16kHz Mono" 
3. OUTPUT: "Audio Tensor" with waveform icon

RIGHT PATH (Video - Green #27AE60):
1. "Frame Sampling" with "(OpenCV)" subtitle
2. "Extract at 20-second intervals"
3. OUTPUT: "30 JPEG Keyframes" with image stack icon

Both paths should be visually parallel with matching box heights. Use icons: waveform for audio outputs, film strip/image for video outputs. Include tool names (ffmpeg, OpenCV) in smaller gray text.

Style: Clean dual-track diagram, arrows flowing downward, consistent spacing between boxes. White background, professional look.
```

**LaTeX Code to Add (after line ~920 in chapter_5.tex):**
```latex
\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.8\textwidth]{figures/fig_5_8_preprocessing.pdf}
    \caption{Preprocessing pipeline showing parallel audio and video processing tracks: audio is extracted and resampled to 16kHz mono, while video frames are sampled at 20-second intervals.}
    \label{fig:preprocessing_pipeline}
\end{figure}
```

---

### Figure 5.9: GPU Memory Timeline

**LaTeX Label:** `fig:memory_timeline`  
**Placement:** Chapter 5, Section 5.6.2 (line ~1132), after "Figure~\ref{fig:memory_timeline} illustrates GPU memory usage..."  
**File Name:** `fig_5_9_memory_timeline.pdf`

**ASCII Layout:**
```
VRAM Usage (GB)
24 |─────────────────────────────────────────────── MAX LIMIT (red dashed)
   |
18 |              ████████
   |              ██ VLM ██
16 |              █Qwen2.5█
   |              ██-VL-7B██
   |
 8 |  ████████              ████████
   |  █Whisper█             █Qwen2.5█
 6 |  █large-v3█            █  -7B  █
   |  █ turbo  █            █(4-bit)█
   |
 0 |──────────────────────────────────────────────
      Stage 1      Stage 2      Stage 3
      (ASR)        (Visual)     (Summary)
      ~2 min       ~5 min       ~1 min
```

**🤖 Figma AI Prompt:**
```
Create a GPU memory usage timeline chart showing sequential model loading:

X-axis: Processing stages with labels:
  - "Stage 1: ASR (~2 min)"
  - "Stage 2: Visual (~5 min)"  
  - "Stage 3: Summary (~1 min)"

Y-axis: VRAM usage in GB (0-24GB scale with gridlines at 6, 12, 18, 24)

Show three colored bars representing peak memory usage:
- Stage 1 (Whisper large-v3-turbo): 8GB peak, Blue (#3498DB), model name inside bar
- Stage 2 (Qwen2.5-VL-7B): 18GB peak, Green (#27AE60), model name inside bar
- Stage 3 (Qwen2.5-7B 4-bit): 8GB peak, Purple (#9B59B6), model name inside bar

Add horizontal dashed red line (#E74C3C) at 24GB labeled "GPU VRAM LIMIT (24GB)"

Between each stage, show memory dropping to near 0 (indicating model unloading)
Add annotation: "Sequential loading prevents OOM errors"

Style: Clean bar chart with gridlines, professional look, clear legend showing model names and memory usage.
```

**LaTeX Code to Add (after line ~1130 in chapter_5.tex):**
```latex
\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.85\textwidth]{figures/fig_5_9_memory_timeline.pdf}
    \caption{GPU memory usage timeline showing sequential model loading strategy. Peak VRAM never exceeds 18GB, staying within the 24GB limit by unloading models between stages.}
    \label{fig:memory_timeline}
\end{figure}
```

---

### Figure 5.10: Complete Processing Workflow

**LaTeX Label:** `fig:processing_workflow`  
**Placement:** Chapter 5, Section 5.6.3 (line ~1165), after "Figure~\ref{fig:processing_workflow} provides a detailed flowchart."  
**File Name:** `fig_5_10_workflow.pdf`

**🤖 Figma AI Prompt:**
```
Create a comprehensive end-to-end processing workflow diagram for a multimodal lecture summarizer:

LAYOUT: Large landscape diagram with clear phases

INPUT (top): Video file icon with ".mp4" label

PHASE 1 - INITIALIZATION (gray #95A5A6):
- "Load Configuration" → "Create Output Directory"

PHASE 2 - PARALLEL PROCESSING (split into two tracks):
  
  LEFT: AUDIO TRACK (Blue #3498DB):
  1. "Audio Extraction"
  2. "Whisper ASR (large-v3-turbo)" - larger box
  3. "Cleaning Pipeline"
  4. OUTPUT: "Cleaned Transcript"

  RIGHT: VIDEO TRACK (Green #27AE60):
  1. "Frame Sampling (30 frames)"
  2. "Qwen2.5-VL Processing" - larger box
  3. "Keyword Aggregation"
  4. OUTPUT: "Visual Keywords"

Show both tracks merging into:

PHASE 3 - FUSION (Purple #9B59B6):
- "Cross-Modal Verification"
- "Exact + Fuzzy Matching"
- "Anti-Hallucination Filter"

PHASE 4 - OUTPUT (Orange #E67E22):
- "Summary Generation (Qwen2.5-7B)"
- "JSON Output" containing: Topics, Keywords, Summary

Add timing annotations: "Total: ~8 minutes for 10-min video"
Show "Model Unload" indicators between phases

Style: Professional system architecture diagram, consistent color coding per module type, clear flow arrows, model names in smaller font. Rounded rectangles, subtle shadows.
```

**LaTeX Code to Add (after line ~1210 in chapter_5.tex):**
```latex
\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.95\textwidth]{figures/fig_5_10_workflow.pdf}
    \caption{Complete video processing workflow showing the four phases: initialization, parallel audio/video processing, cross-modal fusion, and summary generation. Total processing time is approximately 8 minutes for a 10-minute lecture.}
    \label{fig:processing_workflow}
\end{figure}
```

---

## 📋 MASTER CHECKLIST

### Chapter 5 Figures
| # | Figure | Label | File Name | Line | Status |
|---|--------|-------|-----------|------|--------|
| 5.1 | Research Methodology | `fig:methodology` | `fig_5_1_methodology.pdf` | ~64 | ⬜ TODO |
| 5.2 | System Architecture | `fig:architecture` | `fig_5_2_architecture.pdf` | ~99 | ⬜ TODO |
| 5.3 | Whisper ASR Pipeline | `fig:whisper_flow` | `fig_5_3_whisper_flow.pdf` | ~292 | ⬜ TODO |
| 5.4 | Keyframe Sampling | `fig:frame_sampling` | `fig_5_4_frame_sampling.pdf` | ~379 | ⬜ TODO |
| 5.5 | Visual Aggregation | `fig:visual_aggregation` | `fig_5_5_visual_aggregation.pdf` | ~464 | ⬜ TODO |
| 5.6 | Cross-Modal Fusion | `fig:fusion_flow` | `fig_5_6_fusion_flow.pdf` | ~507 | ⬜ TODO |
| **5.7** | **Dataset Distribution** | `fig:dataset_distribution` | `fig_5_7_dataset_distribution.pdf` | ~802 | ✅ DONE |
| 5.8 | Preprocessing Pipeline | `fig:preprocessing_pipeline` | `fig_5_8_preprocessing.pdf` | ~876 | ⬜ TODO |
| 5.9 | Memory Timeline | `fig:memory_timeline` | `fig_5_9_memory_timeline.pdf` | ~1132 | ⬜ TODO |
| 5.10 | Processing Workflow | `fig:processing_workflow` | `fig_5_10_workflow.pdf` | ~1165 | ⬜ TODO |

### Chapter 6 Figures (ALL COMPLETED ✅)
| # | Figure | Label | File Name | Status |
|---|--------|-------|-----------|--------|
| **6.1** | Per-Video F1 | `fig:per_video_f1` | `fig_6_1_per_video_f1.pdf` | ✅ DONE |
| **6.2** | Precision-Recall | `fig:precision_recall` | `fig_6_2_precision_recall.pdf` | ✅ DONE |
| **6.3** | Domain Comparison | `fig:domain_comparison` | `fig_6_3_domain_comparison.pdf` | ✅ DONE |
| **6.4** | Ablation Study | `fig:ablation_study` | `fig_6_4_ablation_study.pdf` | ✅ DONE |
| **6.5** | Failure Modes | `fig:failure_modes` | `fig_6_5_failure_modes.pdf` | ✅ DONE |
| **6.6** | Visual Bias Effect | `fig:visual_bias` | `fig_6_6_visual_bias.pdf` | ✅ DONE |

---

## 🎨 STYLE GUIDE

### Colors (Use Consistently Across All Figures)
| Element | Hex Code | RGB | Usage |
|---------|----------|-----|-------|
| ASR/Audio | `#3498DB` | 52,152,219 | Module 1, Whisper components |
| VLM/Visual | `#27AE60` | 39,174,96 | Module 2, Qwen2.5-VL components |
| Fusion/LLM | `#9B59B6` | 155,89,182 | Module 3, Qwen2.5 components |
| Success/Keep | `#2ECC71` | 46,204,113 | Correct outputs, verified items |
| Error/Remove | `#E74C3C` | 231,76,60 | Errors, hallucinations, warnings |
| Decision | `#F1C40F` | 241,196,15 | Decision diamonds, cautions |
| Neutral | `#95A5A6` | 149,165,166 | Backgrounds, borders |
| Output | `#E67E22` | 230,126,34 | Final outputs, results |

### Typography
- **Headings:** Arial Bold / Helvetica Neue Bold
- **Body:** Arial / Calibri (11-12pt)
- **Code/Keywords:** Consolas / Source Code Pro (10pt)
- **Labels:** Sans-serif, 9-10pt

### Export Settings for Overleaf
- **Format:** PDF (vector) preferred, PNG as backup
- **Resolution:** 300 DPI minimum for PNG
- **Width:** 6 inches for full-width, 4 inches for half-width
- **Color Mode:** RGB

---

## 📁 FILE NAMING CONVENTION

```
fig_[chapter]_[number]_[short_name].pdf
```

Place all files in: `P2/figures/`

---

## ⚠️ IMPORTANT NOTES

1. **After creating each figure**, add the corresponding `\begin{figure}` LaTeX code to the chapter file at the specified line number

2. **File location**: Place all figure PDFs in `P2/figures/` folder

3. **The `\graphicspath`** is already configured in `main.tex`: `\graphicspath{{images/}{figures/}}`

4. **Test compilation** in Overleaf after adding each figure

5. **Figure captions** should be descriptive but concise (1-2 sentences max)

6. **Consistent sizing**: Use `width=0.95\textwidth` for full-width, `width=0.75\textwidth` for medium, `width=0.5\textwidth` for small figures

---

## 🔗 RESOURCES

- **Figma:** https://www.figma.com/
- **Figma AI:** Use FigJam AI or the built-in Figma AI features
- **draw.io:** https://app.diagrams.net/
- **Color Reference:** https://flatuicolors.com/

---

*Last updated: February 5, 2026*
