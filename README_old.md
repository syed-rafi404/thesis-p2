# Multimodal Banglish Classroom Summarizer

## Master's Thesis Project

A multimodal AI system that processes **Audio (Speech)** and **Visuals (Whiteboard)** from classroom recordings to automatically generate comprehensive lecture notes. Designed specifically for **Banglish** (Bengali + English code-mixed) academic content.

---

## 🎯 Research Contributions

| # | Novelty | Description |
|---|---------|-------------|
| 1 | **Visual-Biased ASR** | Bias Whisper's logits toward whiteboard keywords during decoding |
| 2 | **Spatio-Temporal Gaze Tracking** | Detect lecturer hand-pointing at whiteboard terms using YOLOv8-Pose |
| 3 | **Multimodal Fusion** | Combine audio + visual + gaze signals for LLM summarization |

---

## 🖥️ Hardware Requirements

| Component | Specification |
|-----------|---------------|
| **OS** | Windows 11 (tested) / Linux |
| **GPU** | NVIDIA RTX 3090 (24GB VRAM) or equivalent |
| **CUDA** | 12.4+ |
| **Python** | 3.10 |

---

## 📦 Installation

### Step 1: Create Conda Environment

```powershell
# Create fresh conda environment with Python 3.10
conda create -n thesis_v2 python=3.10 -y
conda activate thesis_v2
```

### Step 2: Install PyTorch with CUDA 12.4

```powershell
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
```

### Step 3: Install All Dependencies

```powershell
pip install -r requirements.txt
```

### Step 4: Download Pose Model

```powershell
# YOLOv8n-Pose for gaze tracking (auto-downloads on first run)
# Or manually place yolov8n-pose.pt in project root
```

### Step 5: Verify Installation

```powershell
python verify_stack.py
```

---

## 📁 Project Structure

```
thesisP2/
├── run_thesis.py                # 🚀 Main entry point - full pipeline
├── batch_process.py             # Process multiple videos automatically
├── verify_stack.py              # Hardware & library verification
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── yolov8n-pose.pt              # YOLOv8 pose model for gaze tracking
│
├── config/
│   ├── config.yaml              # Global configuration (batch mode)
│   └── live_config.yaml         # Live mode configuration (4-bit LLM)
│
├── src/
│   ├── ingest_video.py          # Extract audio + frames from video
│   ├── live_ingest.py           # Live/streaming ingestion
│   ├── model_registry.py        # Singleton GPU model management
│   │
│   ├── audio/
│   │   ├── transcriber.py       # Whisper-based ASR (with visual bias)
│   │   ├── transcriber_specialized.py  # BanglaASR for Bengali
│   │   ├── visual_bias_processor.py    # ★ NOVELTY 1: LogitsProcessor
│   │   ├── dual_transcribe.py   # Dual-pass transcription
│   │   └── preprocessor.py      # Audio cleaning
│   │
│   ├── vision/
│   │   ├── whiteboard_ocr.py    # Qwen2.5-VL whiteboard extraction
│   │   ├── vlm_analyzer.py      # VLM analysis utilities
│   │   ├── frame_extractor.py   # Video frame extraction
│   │   └── preprocessor.py      # Image enhancement
│   │
│   ├── research/
│   │   └── gaze_tracker.py      # ★ NOVELTY 2: YOLOv8-Pose pointing detection
│   │
│   ├── fusion/
│   │   └── aligner.py           # Align audio & visual streams
│   │
│   ├── summarizer/
│   │   └── generator.py         # ★ NOVELTY 3: Multimodal LLM fusion
│   │
│   ├── evaluation/
│   │   └── evaluator.py         # TTR + WER metrics
│   │
│   └── utils/
│       └── helpers.py           # Common utilities
│
├── data/
│   ├── raw/                     # Input: lecture video files (.mp4)
│   ├── processed/               # Intermediate processed data
│   └── outputs/                 # Legacy output location
│
├── output/                      # Generated outputs per video
│   └── <video_name>/
│       ├── final_lecture_notes.md     # ✨ Final structured notes
│       ├── transcript_whisper_baseline.txt
│       ├── transcript_whisper_visual_biased.txt
│       ├── transcript_bangla.txt
│       ├── visual_keywords.json
│       ├── text_boxes.json
│       ├── gaze_events.json
│       └── evaluation.json
│
├── experiments/                 # Experiment logs and results
├── notebooks/                   # Jupyter notebooks for analysis
├── scripts/                     # Utility scripts
└── tests/                       # Unit tests
```

---

## 🚀 Quick Start

### Process a Single Video

```powershell
# Full pipeline with all 3 novelties
python run_thesis.py "data/raw/lecture.mp4" -o "output/my_lecture"

# Live mode (4-bit quantized LLM, fits in 24GB VRAM with all models)
python run_thesis.py "data/raw/lecture.mp4" --live --interval 45

# Fast demo (mock VLM, skip gaze tracking)
python run_thesis.py "data/raw/lecture.mp4" --mock --skip-gaze
```

### Batch Process All Videos

```powershell
# Process all videos in data/raw/
python batch_process.py

# With live mode and custom interval
python batch_process.py --live --interval 45 --limit 5
```

### CLI Options

| Flag | Description |
|------|-------------|
| `-o, --output` | Output directory |
| `--interval` | Frame extraction interval in seconds (default: 30) |
| `--live` | Enable live mode (4-bit LLM quantization) |
| `--mock` | Use mock VLM (faster testing) |
| `--skip-gaze` | Skip gaze tracking (faster) |
| `--limit` | Max videos to process (batch mode) |

---

## 🧠 Models Used

| Component | Model | Precision | VRAM | Purpose |
|-----------|-------|-----------|------|---------|
| **ASR (Whisper)** | `openai/whisper-large-v3-turbo` | FP16 | ~3 GB | English/Banglish speech-to-text |
| **ASR (Bengali)** | `bangla-speech-processing/BanglaASR` | FP16 | ~0.5 GB | Pure Bengali speech (fine-tuned Whisper-small) |
| **VLM** | `Qwen/Qwen2.5-VL-7B-Instruct` | FP16 | ~15 GB | Whiteboard text extraction |
| **LLM** | `Qwen/Qwen2.5-7B-Instruct` | FP16/4-bit | ~14 GB / ~5 GB | Multimodal fusion & summarization |
| **Pose** | `YOLOv8n-Pose` | FP32 | ~0.5 GB | Hand/body pose for gaze tracking |

> **Note**: In `--live` mode, LLM uses 4-bit quantization to fit all models in 24GB VRAM simultaneously.

---

## 📋 Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    INPUT: LECTURE VIDEO (.mp4)                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   VIDEO INGESTION                               │
│  📁 src/ingest_video.py                                         │
│  • Extract audio (16kHz mono WAV)                               │
│  • Extract frames (every N seconds)                             │
└─────────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┴───────────────┐
              │                               │
              ▼                               ▼
┌─────────────────────────────┐   ┌─────────────────────────────┐
│   TRACK A: AUDIO            │   │   TRACK B: VISION           │
│                             │   │                             │
│  📁 src/audio/transcriber.py│   │  📁 src/vision/             │
│                             │   │     whiteboard_ocr.py       │
│  Model: Whisper             │   │                             │
│  large-v3-turbo             │   │  Model: Qwen2.5-VL-7B       │
│                             │   │  (FP16, ~15GB VRAM)         │
│  ┌─────────────────────┐    │   │                             │
│  │ ★ NOVELTY 1:        │    │   │  Output:                    │
│  │ Visual-Biased ASR   │◄───┼───┤  • visual_keywords[]        │
│  │                     │    │   │  • text_bounding_boxes[]    │
│  │ LogitsProcessor     │    │   │                             │
│  │ biases toward       │    │   ├─────────────────────────────┤
│  │ whiteboard terms    │    │   │                             │
│  └─────────────────────┘    │   │  📁 src/research/           │
│                             │   │     gaze_tracker.py         │
│                             │   │                             │
│                             │   │  Model: YOLOv8n-Pose        │
│                             │   │                             │
│                             │   │  ┌─────────────────────┐    │
│                             │   │  │ ★ NOVELTY 2:        │    │
│                             │   │  │ Gaze Tracking       │    │
│                             │   │  │                     │    │
│                             │   │  │ Detects hand        │    │
│                             │   │  │ pointing at terms   │    │
│                             │   │  └─────────────────────┘    │
└─────────────────────────────┘   └─────────────────────────────┘
              │                               │
              │ transcript_*.txt              │ gaze_events.json
              │                               │ visual_keywords.json
              └───────────────┬───────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│               TRACK C: EVALUATION                               │
│  📁 src/evaluation/evaluator.py                                 │
│                                                                 │
│  BanglishEvaluator:                                             │
│  • Technical Term Recall (TTR) with fuzzy matching              │
│  • Word Error Rate (WER) using jiwer                            │
│  • Compare baseline vs visual-biased transcription              │
│                                                                 │
│  Output: evaluation.json (TTR improvement %)                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   ★ NOVELTY 3: MULTIMODAL FUSION + LLM          │
│  📁 src/summarizer/generator.py                                 │
│                                                                 │
│  Model: Qwen2.5-7B-Instruct (FP16 or 4-bit)                     │
│                                                                 │
│  Inputs:                                                        │
│  • Visual-biased transcript (corrected technical terms)         │
│  • Whiteboard content (formulas, diagrams, code)                │
│  • Gaze events (attention-weighted importance)                  │
│                                                                 │
│  Strategy:                                                      │
│  • Use VISUAL text as source of truth for technical terms       │
│  • Weight content by gaze attention                             │
│  • Generate structured Markdown notes                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   📄 OUTPUT FILES                               │
│                                                                 │
│  output/<video_name>/                                           │
│  ├── final_lecture_notes.md          ✨ Structured lecture notes│
│  ├── transcript_whisper_baseline.txt    Standard Whisper        │
│  ├── transcript_whisper_visual_biased.txt  With visual bias     │
│  ├── transcript_bangla.txt              Bengali-optimized       │
│  ├── visual_keywords.json               Whiteboard terms        │
│  ├── text_boxes.json                    Bounding boxes          │
│  ├── gaze_events.json                   Pointing timestamps     │
│  └── evaluation.json                    TTR/WER metrics         │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📊 Evaluation Metrics

The pipeline evaluates transcription quality using:

| Metric | Description | Implementation |
|--------|-------------|----------------|
| **TTR** | Technical Term Recall - % of whiteboard terms found in transcript | Fuzzy matching (thefuzz, threshold > 85) |
| **WER** | Word Error Rate - standard ASR quality metric | jiwer library |
| **Improvement %** | Relative improvement of visual-biased over baseline | `(biased_TTR - baseline_TTR) / baseline_TTR` |

### Sample Results

| Video | Baseline TTR | Visual-Biased TTR | Improvement |
|-------|--------------|-------------------|-------------|
| L1 Java OOP | 35% | 45% | +28.6% |
| L2 Java OOP | 40% | 50% | +25.0% |
| CSE443 Lec 14 | 30% | 42% | +40.0% |

---

## 🔧 Configuration

### config/config.yaml (Batch Mode - FP16)

```yaml
models:
  asr:
    name: "openai/whisper-large-v3-turbo"
  vlm:
    name: "Qwen/Qwen2.5-VL-7B-Instruct"
    precision: "float16"
  llm:
    name: "Qwen/Qwen2.5-7B-Instruct"
    precision: "float16"
```

### config/live_config.yaml (Live Mode - 4-bit LLM)

```yaml
models:
  llm:
    name: "Qwen/Qwen2.5-7B-Instruct"
    precision: "4bit"  # Uses bitsandbytes
```

---

## 📄 License

This project is part of academic research for a Master's Thesis.

---

## 🙏 Acknowledgments

- [OpenAI Whisper](https://github.com/openai/whisper) for speech recognition
- [Qwen2.5-VL](https://github.com/QwenLM/Qwen2-VL) for vision-language understanding
- [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics) for pose estimation
- [Hugging Face Transformers](https://huggingface.co/transformers/) for model infrastructure

