"""
=============================================================================
BATCH EVALUATION - Run Visual Bias Test on All Videos
=============================================================================
Quick batch script to evaluate Visual-Biased ASR improvement across
multiple lecture videos and compile statistics.

This gives consistent data for P2 thesis report.
=============================================================================
"""

import sys
import json
import time
from pathlib import Path
from typing import List, Dict, Any

from rich.console import Console
from rich.table import Table
from rich import box

console = Console()


def find_videos(data_dir: str = "data/raw") -> List[str]:
    """Find all video files in the data directory."""
    data_path = Path(data_dir)
    videos = []
    
    for ext in ['*.mp4', '*.avi', '*.mkv', '*.mov']:
        videos.extend(data_path.glob(ext))
    
    return sorted([str(v) for v in videos])


def run_batch_evaluation(max_videos: int = 5, low_vram: bool = False):
    """Run visual bias evaluation on multiple videos.
    
    Args:
        max_videos: Maximum number of videos to process
        low_vram: Use 4-bit quantization for GPUs with <16GB VRAM
    """
    
    from src.ingest_video import VideoIngestor
    from src.audio.transcriber import BanglishTranscriber
    from src.vision.whiteboard_ocr import WhiteboardVLM
    from src.evaluation.evaluator import BanglishEvaluator
    from src.model_registry import get_registry
    
    console.print("[bold cyan]" + "="*60 + "[/bold cyan]")
    console.print("[bold cyan]BATCH VISUAL BIAS EVALUATION[/bold cyan]")
    if low_vram:
        console.print("[yellow]Low VRAM mode: Using 4-bit quantization[/yellow]")
    console.print("[bold cyan]" + "="*60 + "[/bold cyan]\n")
    
    # Find videos
    videos = find_videos()
    if not videos:
        console.print("[red]No videos found in data/raw/[/red]")
        return
    
    videos = videos[:max_videos]
    console.print(f"Found {len(videos)} videos to process\n")
    
    results = []
    
    for i, video_path in enumerate(videos):
        video_name = Path(video_path).stem[:50]
        console.print(f"\n[bold]{'='*60}[/bold]")
        console.print(f"[bold]Video {i+1}/{len(videos)}: {video_name}...[/bold]")
        console.print(f"[bold]{'='*60}[/bold]")
        
        try:
            # Ingest
            output_dir = f"output/batch_eval/video_{i+1}"
            ingestor = VideoIngestor(output_dir=f"{output_dir}/ingested")
            ingest_result = ingestor.process(video_path, frame_interval=30)
            audio_path = ingest_result.audio_path
            frame_paths = [f.frame_path for f in ingest_result.frames]
            
            console.print(f"  ✓ Ingested: {len(frame_paths)} frames, {ingest_result.duration:.0f}s")
            
            # VLM extraction (use 4-bit for low VRAM GPUs)
            vlm = WhiteboardVLM(use_4bit=low_vram)
            all_keywords = []
            
            import re
            for frame_path in frame_paths:
                try:
                    content = vlm.analyze_frame(frame_path)
                    if content and len(content) > 10:
                        words = re.findall(r'\b[A-Z][a-z]+(?:[A-Z][a-z]+)*\b|\b[A-Z]{2,}\b', content)
                        all_keywords.extend(words)
                except:
                    pass
            
            visual_keywords = list(dict.fromkeys(all_keywords))
            console.print(f"  ✓ VLM: {len(visual_keywords)} keywords")
            
            # Unload VLM
            registry = get_registry()
            registry.unload("vlm")
            
            # Transcribe baseline
            console.print("  → Transcribing baseline...")
            transcriber = BanglishTranscriber()
            baseline_result = transcriber.transcribe(audio_path, visual_context=None)
            
            # Transcribe with visual bias
            console.print("  → Transcribing with visual bias...")
            biased_result = transcriber.transcribe(audio_path, visual_context=visual_keywords)
            
            # Evaluate
            evaluator = BanglishEvaluator(fuzzy_threshold=85)
            ground_truth = visual_keywords[:20]
            
            baseline_eval = evaluator.evaluate_recall(ground_truth, baseline_result.text)
            biased_eval = evaluator.evaluate_recall(ground_truth, biased_result.text)
            
            improvement = (biased_eval['recall'] - baseline_eval['recall']) * 100
            
            result = {
                'video': video_name,
                'keywords': len(visual_keywords),
                'duration': ingest_result.duration,
                'baseline_recall': baseline_eval['recall'] * 100,
                'biased_recall': biased_eval['recall'] * 100,
                'improvement': improvement,
            }
            results.append(result)
            
            # Print per-video result
            if improvement > 0:
                console.print(f"  [green]✓ Result: {baseline_eval['recall']*100:.1f}% → {biased_eval['recall']*100:.1f}% (+{improvement:.1f}%)[/green]")
            elif improvement < 0:
                console.print(f"  [red]✗ Result: {baseline_eval['recall']*100:.1f}% → {biased_eval['recall']*100:.1f}% ({improvement:.1f}%)[/red]")
            else:
                console.print(f"  [yellow]→ Result: {baseline_eval['recall']*100:.1f}% → {biased_eval['recall']*100:.1f}% (no change)[/yellow]")
                
        except Exception as e:
            console.print(f"  [red]Error: {e}[/red]")
            results.append({
                'video': video_name,
                'error': str(e)
            })
    
    # Summary table
    console.print("\n\n[bold cyan]" + "="*60 + "[/bold cyan]")
    console.print("[bold cyan]BATCH EVALUATION SUMMARY[/bold cyan]")
    console.print("[bold cyan]" + "="*60 + "[/bold cyan]\n")
    
    table = Table(title="Visual Bias Evaluation Results", box=box.ROUNDED)
    table.add_column("Video", style="cyan", max_width=30)
    table.add_column("Baseline TTR", style="white")
    table.add_column("Biased TTR", style="green")
    table.add_column("Improvement", style="yellow")
    
    total_baseline = 0
    total_biased = 0
    count = 0
    
    for r in results:
        if 'error' in r:
            table.add_row(r['video'][:30], "Error", "-", "-")
        else:
            imp_str = f"+{r['improvement']:.1f}%" if r['improvement'] >= 0 else f"{r['improvement']:.1f}%"
            table.add_row(
                r['video'][:30],
                f"{r['baseline_recall']:.1f}%",
                f"{r['biased_recall']:.1f}%",
                imp_str
            )
            total_baseline += r['baseline_recall']
            total_biased += r['biased_recall']
            count += 1
    
    console.print(table)
    
    if count > 0:
        avg_baseline = total_baseline / count
        avg_biased = total_biased / count
        avg_improvement = avg_biased - avg_baseline
        
        console.print(f"\n[bold]Average Results (n={count}):[/bold]")
        console.print(f"  Baseline TTR: {avg_baseline:.1f}%")
        console.print(f"  Biased TTR:   {avg_biased:.1f}%")
        if avg_improvement >= 0:
            console.print(f"  [bold green]Average Improvement: +{avg_improvement:.1f}%[/bold green]")
        else:
            console.print(f"  [bold red]Average Change: {avg_improvement:.1f}%[/bold red]")
    
    # Save results
    output_path = Path("output/batch_eval")
    output_path.mkdir(parents=True, exist_ok=True)
    with open(output_path / "batch_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    console.print(f"\n✓ Results saved to: {output_path / 'batch_results.json'}")
    
    return results


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Batch Visual Bias Evaluation")
    parser.add_argument("--max-videos", "-n", type=int, default=5,
                        help="Maximum number of videos to process")
    parser.add_argument("--low-vram", action="store_true",
                        help="Use 4-bit quantization for GPUs with <16GB VRAM")
    args = parser.parse_args()
    
    run_batch_evaluation(args.max_videos, low_vram=args.low_vram)
