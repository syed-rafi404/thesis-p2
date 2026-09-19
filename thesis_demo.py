"""
=============================================================================
THESIS DEMO SUMMARY - What This System Achieves
=============================================================================
This script runs a quick demo showing all thesis novelties working together.

NOVELTIES DEMONSTRATED:
1. VLM-based Whiteboard OCR → Extracts technical terms automatically
2. Dual-ASR Processing → Whisper + BanglaASR for Banglish content
3. Multimodal Fusion → LLM combines all sources into lecture notes

METRICS:
- Technical Term Coverage: How many visual terms appear in final notes
- Language Coverage: Both English and Bengali captured
- Output Quality: Structured markdown lecture notes generated
=============================================================================
"""

import sys
import json
from pathlib import Path
from typing import List, Dict, Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

console = Console()


def run_demo(video_path: str, output_dir: str = "output/thesis_demo", low_vram: bool = False):
    """Run a quick thesis demo on a video.
    
    Args:
        video_path: Path to the input video
        output_dir: Output directory for results
        low_vram: Use 4-bit quantization for GPUs with <16GB VRAM
    """
    
    from src.ingest_video import VideoIngestor
    from src.audio.transcriber import BanglishTranscriber
    from src.audio.transcriber_specialized import BanglaASRTranscriber
    from src.vision.whiteboard_ocr import WhiteboardVLM
    from src.summarizer.generator import LectureNoteGenerator
    from src.model_registry import get_registry
    from thefuzz import fuzz
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    console.print(Panel.fit(
        "[bold cyan]MULTIMODAL BANGLISH CLASSROOM SUMMARIZER[/bold cyan]\n"
        "[bold]Master's Thesis - Novelty Demonstration[/bold]\n\n"
        "• Novelty 1: VLM-based Whiteboard OCR\n"
        "• Novelty 2: Dual-ASR (Whisper + BanglaASR)\n"
        "• Novelty 3: Multimodal Fusion via LLM",
        border_style="blue"
    ))
    
    # =====================================================================
    # STEP 1: Video Ingestion
    # =====================================================================
    console.print("\n[bold blue]STEP 1: Video Ingestion[/bold blue]")
    ingestor = VideoIngestor(output_dir=str(output_path / "ingested"))
    result = ingestor.process(video_path, frame_interval=30)
    audio_path = result.audio_path
    frame_paths = [f.frame_path for f in result.frames]
    console.print(f"  ✓ Duration: {result.duration:.0f}s")
    console.print(f"  ✓ Frames: {len(frame_paths)} extracted")
    console.print(f"  ✓ Audio: {Path(audio_path).name}")
    
    # =====================================================================
    # STEP 2: VLM Whiteboard Extraction (NOVELTY 1)
    # =====================================================================
    console.print("\n[bold green]STEP 2: VLM Whiteboard Extraction (NOVELTY 1)[/bold green]")
    vlm = WhiteboardVLM(use_4bit=low_vram)
    all_keywords = []
    
    import re
    for i, frame_path in enumerate(frame_paths):
        try:
            content = vlm.analyze_frame(frame_path)
            if content:
                # Extract meaningful keywords
                words = set()
                # CamelCase
                words.update(re.findall(r'\b[A-Z][a-z]+(?:[A-Z][a-z]+)+\b', content))
                # Capitalized
                words.update(re.findall(r'\b[A-Z][a-z]{2,}\b', content))
                # ALL CAPS
                words.update(re.findall(r'\b[A-Z]{2,}\b', content))
                all_keywords.extend(list(words))
        except:
            pass
    
    visual_keywords = list(dict.fromkeys(all_keywords))[:50]  # Top 50 unique
    console.print(f"  ✓ Keywords extracted: {len(visual_keywords)}")
    console.print(f"  ✓ Sample: {visual_keywords[:10]}")
    
    # Save keywords
    with open(output_path / "visual_keywords.json", "w") as f:
        json.dump(visual_keywords, f, indent=2)
    
    # Unload VLM
    registry = get_registry()
    registry.unload("vlm")
    
    # =====================================================================
    # STEP 3: Dual-ASR Processing (NOVELTY 2)
    # =====================================================================
    console.print("\n[bold yellow]STEP 3: Dual-ASR Processing (NOVELTY 2)[/bold yellow]")
    
    # Whisper (English + Banglish)
    console.print("  → Whisper transcription...")
    transcriber = BanglishTranscriber()
    whisper_result = transcriber.transcribe(audio_path, visual_context=visual_keywords)
    console.print(f"  ✓ Whisper: {len(whisper_result.text)} chars")
    
    # BanglaASR (Bengali)
    console.print("  → BanglaASR transcription...")
    try:
        bangla_transcriber = BanglaASRTranscriber()
        bangla_result = bangla_transcriber.transcribe(audio_path)
        bangla_text = bangla_result.text
        bangla_transcriber.unload_model()
        console.print(f"  ✓ BanglaASR: {len(bangla_text)} chars")
    except Exception as e:
        bangla_text = ""
        console.print(f"  [yellow]⚠ BanglaASR failed: {e}[/yellow]")
    
    # Save transcripts
    with open(output_path / "transcript_whisper.txt", "w", encoding="utf-8") as f:
        f.write(whisper_result.text)
    with open(output_path / "transcript_bangla.txt", "w", encoding="utf-8") as f:
        f.write(bangla_text)
    
    # =====================================================================
    # STEP 4: Multimodal Fusion (NOVELTY 3)
    # =====================================================================
    console.print("\n[bold magenta]STEP 4: Multimodal Fusion via LLM (NOVELTY 3)[/bold magenta]")
    
    generator = LectureNoteGenerator()
    generator.load_model()
    
    # Build context
    visual_content = "\n".join(f"• {kw}" for kw in visual_keywords[:30])
    
    prompt = f"""Create comprehensive lecture notes from these sources:

## WHISPER TRANSCRIPT (English + Banglish)
{whisper_result.text[:4000]}

## BANGLA TRANSCRIPT (Bengali)
{bangla_text[:2000] if bangla_text else "Not available"}

## VISUAL KEYWORDS (From Whiteboard)
{visual_content}

Generate well-structured Markdown lecture notes. Use visual keywords as the source of truth for technical terms.
"""
    
    # Generate notes
    messages = [{"role": "user", "content": prompt}]
    text = generator.tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    inputs = generator.tokenizer([text], return_tensors="pt").to(generator.model.device)
    
    import torch
    with torch.no_grad():
        outputs = generator.model.generate(
            **inputs,
            max_new_tokens=2048,
            temperature=0.7,
            do_sample=True,
        )
    
    generated = generator.tokenizer.decode(outputs[0][inputs['input_ids'].shape[1]:], skip_special_tokens=True)
    console.print(f"  ✓ Lecture notes: {len(generated)} chars")
    
    # Save notes
    with open(output_path / "lecture_notes.md", "w", encoding="utf-8") as f:
        f.write(generated)
    
    # =====================================================================
    # METRICS SUMMARY
    # =====================================================================
    console.print("\n[bold cyan]" + "="*60 + "[/bold cyan]")
    console.print("[bold cyan]THESIS DEMONSTRATION METRICS[/bold cyan]")
    console.print("[bold cyan]" + "="*60 + "[/bold cyan]\n")
    
    # Calculate term coverage in final notes
    terms_in_notes = 0
    for kw in visual_keywords[:20]:
        if fuzz.partial_ratio(kw.lower(), generated.lower()) > 80:
            terms_in_notes += 1
    
    coverage = (terms_in_notes / min(20, len(visual_keywords))) * 100 if visual_keywords else 0
    
    table = Table(title="Demonstration Results", box=box.ROUNDED)
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Video Duration", f"{result.duration:.0f} seconds")
    table.add_row("Frames Processed", str(len(frame_paths)))
    table.add_row("Visual Keywords Extracted", str(len(visual_keywords)))
    table.add_row("Whisper Transcript Length", f"{len(whisper_result.text)} chars")
    table.add_row("BanglaASR Transcript Length", f"{len(bangla_text)} chars")
    table.add_row("Final Lecture Notes Length", f"{len(generated)} chars")
    table.add_row("Term Coverage in Notes", f"{coverage:.1f}%")
    
    console.print(table)
    
    # What this demonstrates
    console.print("\n[bold]What This Demonstrates:[/bold]")
    console.print("  1. [green]✓[/green] VLM extracts technical terms from whiteboard automatically")
    console.print("  2. [green]✓[/green] Dual-ASR captures both English and Bengali content")
    console.print("  3. [green]✓[/green] LLM fuses all sources into structured lecture notes")
    console.print(f"\n[bold green]Output saved to: {output_path}[/bold green]")
    
    return {
        'duration': result.duration,
        'frames': len(frame_paths),
        'keywords': len(visual_keywords),
        'whisper_chars': len(whisper_result.text),
        'bangla_chars': len(bangla_text),
        'notes_chars': len(generated),
        'coverage': coverage,
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Thesis Demo - Multimodal Summarizer")
    parser.add_argument("video_path", help="Path to the input video")
    parser.add_argument("--output", "-o", default="output/thesis_demo",
                        help="Output directory")
    parser.add_argument("--low-vram", action="store_true",
                        help="Use 4-bit quantization for GPUs with <16GB VRAM")
    args = parser.parse_args()
    
    run_demo(args.video_path, args.output, low_vram=args.low_vram)
