"""
=============================================================================
SIMPLIFIED 2-WAY COMPARISON - Baseline vs Visual-Biased ASR
=============================================================================
Quick test script to validate the core thesis novelty:
Visual-Biased Whisper improves Technical Term Recall (TTR)

This removes the complexity of temporal bias and focuses on proving
the fundamental improvement from visual context.

Usage:
    python test_visual_bias_simple.py "path/to/video.mp4"
=============================================================================
"""

import sys
import json
import time
from pathlib import Path
from typing import List, Dict, Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

console = Console()


def run_simple_test(video_path: str, output_dir: str = "output/simple_test", low_vram: bool = False):
    """Run simplified 2-way comparison: Baseline vs Visual-Biased Whisper.
    
    Args:
        video_path: Path to the input video
        output_dir: Output directory for results
        low_vram: Use 4-bit quantization for GPUs with <16GB VRAM
    """
    
    from src.ingest_video import VideoIngestor
    from src.audio.transcriber import BanglishTranscriber
    from src.vision.whiteboard_ocr import WhiteboardVLM
    from src.evaluation.evaluator import BanglishEvaluator
    from src.model_registry import get_registry
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    console.print(Panel.fit(
        "[bold cyan]Simplified Visual Bias Test[/bold cyan]\n"
        "Comparing: Baseline Whisper vs Visual-Biased Whisper",
        border_style="blue"
    ))
    
    # Step 1: Ingest video
    console.print("\n[bold]Step 1: Video Ingestion[/bold]")
    ingestor = VideoIngestor(output_dir=str(output_path / "ingested"))
    result = ingestor.process(video_path, frame_interval=30)
    audio_path = result.audio_path
    frame_paths = [f.frame_path for f in result.frames]
    console.print(f"  ✓ {len(frame_paths)} frames, {result.duration:.0f}s audio")
    
    # Step 2: Extract visual keywords
    console.print("\n[bold]Step 2: VLM Keyword Extraction[/bold]")
    vlm = WhiteboardVLM(use_4bit=low_vram)
    all_keywords = []
    
    for frame_path in frame_paths:
        try:
            content = vlm.analyze_frame(frame_path)
            if content and len(content) > 10:
                # Simple keyword extraction
                import re
                words = re.findall(r'\b[A-Z][a-z]+(?:[A-Z][a-z]+)*\b|\b[A-Z]{2,}\b', content)
                all_keywords.extend(words)
        except Exception as e:
            pass
    
    # Deduplicate
    visual_keywords = list(dict.fromkeys(all_keywords))
    console.print(f"  ✓ {len(visual_keywords)} unique keywords extracted")
    
    # Unload VLM
    registry = get_registry()
    registry.unload("vlm")
    
    # Step 3: Transcribe (Baseline)
    console.print("\n[bold]Step 3A: Baseline Whisper (no bias)[/bold]")
    transcriber = BanglishTranscriber()
    baseline_result = transcriber.transcribe(audio_path, visual_context=None)
    console.print(f"  ✓ {len(baseline_result.text)} chars")
    
    # Step 3B: Transcribe (Visual-Biased)
    console.print("\n[bold]Step 3B: Visual-Biased Whisper[/bold]")
    biased_result = transcriber.transcribe(audio_path, visual_context=visual_keywords)
    console.print(f"  ✓ {len(biased_result.text)} chars")
    
    # Step 4: Evaluate
    console.print("\n[bold]Step 4: Evaluation[/bold]")
    evaluator = BanglishEvaluator(fuzzy_threshold=85)
    ground_truth = visual_keywords[:20]  # Top 20 terms
    
    baseline_eval = evaluator.evaluate_recall(ground_truth, baseline_result.text)
    biased_eval = evaluator.evaluate_recall(ground_truth, biased_result.text)
    
    improvement = (biased_eval['recall'] - baseline_eval['recall']) * 100
    
    # Print results
    table = Table(title="Visual Bias Impact on TTR", box=box.ROUNDED)
    table.add_column("Metric", style="cyan")
    table.add_column("Baseline", style="white")
    table.add_column("Visual-Biased", style="green")
    
    table.add_row(
        "Recall",
        f"{baseline_eval['recall']*100:.1f}%",
        f"{biased_eval['recall']*100:.1f}%"
    )
    table.add_row(
        "Found / Total",
        f"{len(baseline_eval['found'])} / {len(ground_truth)}",
        f"{len(biased_eval['found'])} / {len(ground_truth)}"
    )
    table.add_row(
        "Found Terms",
        ", ".join(baseline_eval['found'][:5]) + ("..." if len(baseline_eval['found']) > 5 else ""),
        ", ".join(biased_eval['found'][:5]) + ("..." if len(biased_eval['found']) > 5 else "")
    )
    
    console.print(table)
    
    if improvement > 0:
        console.print(f"\n[bold green]✓ Visual Bias Improvement: +{improvement:.1f}%[/bold green]")
    elif improvement < 0:
        console.print(f"\n[bold red]✗ Visual Bias Regression: {improvement:.1f}%[/bold red]")
    else:
        console.print(f"\n[bold yellow]→ No change[/bold yellow]")
    
    # Save results
    results = {
        "video": video_path,
        "keywords_extracted": len(visual_keywords),
        "ground_truth_terms": len(ground_truth),
        "baseline_recall": baseline_eval['recall'],
        "biased_recall": biased_eval['recall'],
        "improvement_pct": improvement,
        "baseline_found": baseline_eval['found'],
        "biased_found": biased_eval['found'],
    }
    
    with open(output_path / "results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    console.print(f"\n✓ Results saved to: {output_path / 'results.json'}")
    
    return results


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Simplified Visual Bias Test")
    parser.add_argument("video_path", help="Path to the input video")
    parser.add_argument("--output", "-o", default="output/simple_test",
                        help="Output directory")
    parser.add_argument("--low-vram", action="store_true",
                        help="Use 4-bit quantization for GPUs with <16GB VRAM")
    args = parser.parse_args()
    
    run_simple_test(args.video_path, args.output, low_vram=args.low_vram)
