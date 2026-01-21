# Multimodal Banglish Classroom Summarizer

## Master's Thesis Project

A multimodal AI system that processes **Audio (Speech)** and **Visuals (Whiteboard)** from classroom recordings to automatically generate comprehensive lecture notes.

---

## 🖥️ Hardware Specifications

- **OS**: Windows 11
- **GPU**: NVIDIA RTX 3090 (24GB VRAM)
- **Quantization**: AWQ (AutoGPTQ) - No bitsandbytes (unstable on Windows)

---

## 📦 Phase 1: Environment Setup

### Step 1: Create Conda Environment

```powershell
# Create fresh conda environment with Python 3.10
conda create -n thesis_v2 python=3.10 -y

# Activate the environment
conda activate thesis_v2
```

### Step 2: Install PyTorch with CUDA 12.4

```powershell
# Install PyTorch with CUDA 12.4 support
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
```

### Step 3: Install AutoGPTQ (Windows-Compatible AWQ Support)

```powershell
# Install AutoGPTQ for 4-bit quantized model loading
pip install auto-gptq --extra-index-url https://huggingface.github.io/autogptq-index/whl/cu124/
```

### Step 4: Install Core Dependencies

```powershell
# Transformers & Acceleration
pip install transformers accelerate optimum

# Audio Processing
pip install librosa soundfile

# Vision Processing
pip install opencv-python pillow

# Video Processing
pip install moviepy

# Utilities
pip install tqdm pyyaml python-dotenv rich
```

### Step 5: Verify Installation

```powershell
# Run the hardware verification script
python verify_stack.py
```

---

## 📁 Project Structure

```
thesisP2/
├── README.md                    # This file
├── requirements.txt             # Pinned dependencies
├── verify_stack.py              # Hardware & library verification
├── config/
│   └── config.yaml              # Global configuration
├── src/
│   ├── __init__.py
│   ├── audio/                   # Audio/Speech processing module
│   │   ├── __init__.py
│   │   ├── transcriber.py       # Whisper-based transcription
│   │   └── preprocessor.py      # Audio cleaning & segmentation
│   ├── vision/                  # Visual processing module
│   │   ├── __init__.py
│   │   ├── frame_extractor.py   # Extract frames from video
│   │   ├── vlm_analyzer.py      # VLM for whiteboard understanding (NO OCR!)
│   │   └── preprocessor.py      # Image enhancement
│   ├── fusion/                  # Multimodal fusion module
│   │   ├── __init__.py
│   │   └── aligner.py           # Align audio & visual streams
│   ├── summarizer/              # LLM summarization module
│   │   ├── __init__.py
│   │   └── generator.py         # AWQ model inference
│   └── utils/
│       ├── __init__.py
│       └── helpers.py           # Common utilities
├── data/
│   ├── raw/                     # Original lecture recordings
│   ├── processed/               # Preprocessed data
│   │   ├── audio/               # Extracted audio files
│   │   ├── frames/              # Extracted video frames
│   │   └── transcripts/         # ASR outputs
│   └── outputs/                 # Generated summaries
├── experiments/
│   ├── logs/                    # Training/inference logs
│   ├── checkpoints/             # Model checkpoints
│   └── results/                 # Experiment results
├── notebooks/
│   └── exploration.ipynb        # Jupyter notebooks for EDA
├── tests/
│   └── test_pipeline.py         # Unit tests
└── scripts/
    ├── run_pipeline.py          # Main execution script
    └── batch_process.py         # Batch processing script
```

---

## 🚀 Quick Start

1. Clone/navigate to this directory
2. Run setup commands from Phase 1
3. Execute `python verify_stack.py` to confirm GPU setup
4. **Process a lecture video:**

```powershell
# Extract audio + frames from a video
python src/ingest_video.py path/to/lecture.mp4 --interval 30

# Output:
#   temp/full_audio.wav          (16kHz mono - ready for Whisper)
#   temp/frames/frame_*.jpg      (one per 30 seconds)
#   temp/ingest_metadata.json    (timestamps for alignment)
```

---

## 📋 Research Pipeline (Batch Processing)

```
┌─────────────────────────────────────────────────────────────────┐
│                    INPUT: LECTURE VIDEO                         │
│                     📹 lecture.mp4                              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   VIDEO INGESTION                               │
│  ─────────────────────────────────────────────────────────────  │
│  📁 src/ingest_video.py                                         │
│  • Extract audio (16kHz mono WAV)                               │
│  • Extract frames (every N seconds)                             │
└─────────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
┌─────────────────────────┐     ┌─────────────────────────┐
│    AUDIO OUTPUTS        │     │    VIDEO OUTPUTS        │
│  ─────────────────────  │     │  ─────────────────────  │
│  📁 full_audio.wav      │     │  📁 frames/*.jpg        │
│  (16kHz mono)           │     │  (every 30 seconds)     │
└─────────────────────────┘     └─────────────────────────┘
              │                               │
              ▼                               ▼
┌─────────────────────────┐     ┌─────────────────────────┐
│  DUAL-STREAM ASR        │     │    VLM WHITEBOARD OCR   │
│  ─────────────────────  │     │  ─────────────────────  │
│  📁 src/audio/          │     │  📁 src/vision/         │
│     dual_transcribe.py  │     │     whiteboard_ocr.py   │
│                         │     │                         │
│  Model: Whisper         │     │  Model: Qwen2.5-VL-7B   │
│  large-v3-turbo         │     │  (FP16, 15GB VRAM)      │
│                         │     │                         │
│  Stream 1: English      │     │  Prompt: "Transcribe    │
│  Stream 2: Bengali      │     │  all text, formulas,    │
│  (with Bengali prompt)  │     │  diagrams on board"     │
└─────────────────────────┘     └─────────────────────────┘
              │                               │
              ▼                               ▼
┌─────────────────────────┐     ┌─────────────────────────┐
│  📄 transcript_en.json  │     │  📄 vision_context.json │
│  📄 transcript_bn.json  │     │  (per-frame analysis)   │
└─────────────────────────┘     └─────────────────────────┘
              │                               │
              └───────────────┬───────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   MULTIMODAL FUSION + LLM                       │
│  ─────────────────────────────────────────────────────────────  │
│  📁 src/summarizer/generator.py                                 │
│                                                                 │
│  Model: Qwen2.5-7B-Instruct (FP16, 14GB VRAM)                   │
│                                                                 │
│  Strategy:                                                      │
│  • Use VISUAL text as source of truth for technical terms       │
│  • Correct audio errors (e.g., "A-Store" → "A*")                │
│  • Use audio for flow and explanations                          │
│  • Generate structured Markdown notes                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   📄 final_lecture_notes.md                     │
│  ─────────────────────────────────────────────────────────────  │
│  • Corrected technical terms                                    │
│  • Accurate formulas from whiteboard                            │
│  • Structured Markdown format                                   │
└─────────────────────────────────────────────────────────────────┘
```

### Models Used

| Component | Model | Precision | VRAM |
|-----------|-------|-----------|------|
| ASR | `openai/whisper-large-v3-turbo` | FP16 | ~1.5 GB |
| VLM | `Qwen/Qwen2.5-VL-7B-Instruct` | FP16 | ~15 GB |
| LLM | `Qwen/Qwen2.5-7B-Instruct` | FP16 | ~14 GB |

> **Note**: AWQ quantization was originally planned but had Windows compatibility issues. FP16 models work reliably on RTX 3090 (24GB VRAM).

### Quick Pipeline Execution

```powershell
# Step 1: Ingest video (extract audio + frames)
python src/ingest_video.py data/raw/lecture.mp4 --interval 30 --output-dir temp_output

# Step 2: Dual-stream audio transcription
python src/audio/dual_transcribe.py temp_output/full_audio.wav --output-dir temp_output

# Step 3: VLM whiteboard analysis
python src/vision/whiteboard_ocr.py temp_output/frames --output temp_output/vision_context.json

# Step 4: Generate final lecture notes
python src/summarizer/generator.py --output final_lecture_notes.md
```

---

## 📄 License

This project is part of academic research for a Master's Thesis.

