"""
=============================================================================
BATCH PROCESSOR - Automatically process all videos in data/raw/
=============================================================================
Master's Thesis - Batch Processing Script

Finds all video files in data/raw/ and runs the full thesis pipeline on each.
Each video gets its own output folder in output/<video_name>/

Usage:
    python batch_process.py                    # Process all videos
    python batch_process.py --mock             # Fast mode (mock VLM)
    python batch_process.py --interval 60      # Custom frame interval
=============================================================================
"""

import sys
import time
import argparse
from pathlib import Path
from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

# ModelRegistry for preloading GPU models
try:
    from src.model_registry import ModelRegistry
    REGISTRY_AVAILABLE = True
except ImportError:
    REGISTRY_AVAILABLE = False

console = Console()

# Supported video extensions
VIDEO_EXTENSIONS = {'.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v'}


def find_videos(input_dir: Path) -> list[Path]:
    """Find all video files in the input directory."""
    videos = []
    for ext in VIDEO_EXTENSIONS:
        videos.extend(input_dir.glob(f"*{ext}"))
        videos.extend(input_dir.glob(f"*{ext.upper()}"))
    return sorted(set(videos))


def process_video(
    video_path: Path,
    output_base: Path,
    interval: int,
    mock: bool,
    skip_gaze: bool,
    live_mode: bool = False,
) -> dict:
    """
    Process a single video through the thesis pipeline.
    
    Returns:
        Dict with status, output_dir, duration, and any error message
    """
    from run_thesis import ThesisPipeline
    
    # Create output directory based on video name (without extension)
    video_name = video_path.stem
    output_dir = output_base / video_name
    
    console.print(f"\n[bold blue]{'='*60}[/bold blue]")
    console.print(f"[bold]Processing:[/bold] {video_path.name}")
    console.print(f"[bold]Output to:[/bold] {output_dir}")
    if live_mode:
        console.print(f"[bold yellow]Mode:[/bold yellow] LIVE (4-bit LLM)")
    console.print(f"[bold blue]{'='*60}[/bold blue]\n")
    
    start_time = time.time()
    
    try:
        pipeline = ThesisPipeline(
            video_path=str(video_path),
            output_dir=str(output_dir),
            frame_interval=interval,
            use_mock_vlm=mock,
            skip_gaze=skip_gaze,
            live_mode=live_mode,
        )
        
        result = pipeline.run()
        
        duration = time.time() - start_time
        
        return {
            'status': 'success',
            'video': video_path.name,
            'output_dir': str(output_dir),
            'duration': duration,
            'video_duration': result.video_duration,
            'ttr_improvement': result.ttr_improvement,
            'visual_keywords': len(result.visual_keywords),
            'gaze_events': len(result.gaze_events),
            'bangla_transcript_len': len(result.transcript_bangla),
            'lecture_notes_len': len(result.final_lecture_notes),
            'error': None,
        }
        
    except Exception as e:
        duration = time.time() - start_time
        console.print(f"[red]Error processing {video_path.name}: {e}[/red]")
        import traceback
        traceback.print_exc()
        
        return {
            'status': 'failed',
            'video': video_path.name,
            'output_dir': str(output_dir),
            'duration': duration,
            'video_duration': 0,
            'ttr_improvement': 0,
            'visual_keywords': 0,
            'gaze_events': 0,
            'error': str(e),
        }


def print_summary(results: list[dict], total_time: float):
    """Print a summary table of all processed videos."""
    console.print("\n")
    console.print(Panel.fit(
        "[bold green]BATCH PROCESSING COMPLETE[/bold green]",
        border_style="green"
    ))
    
    # Summary table
    table = Table(title="Batch Processing Summary", box=box.ROUNDED)
    table.add_column("Video", style="cyan")
    table.add_column("Status", style="white")
    table.add_column("Duration", style="white")
    table.add_column("TTR Δ", style="white")
    table.add_column("Keywords", style="white")
    
    success_count = 0
    failed_count = 0
    
    for r in results:
        if r['status'] == 'success':
            status = "[green]✓ Success[/green]"
            success_count += 1
            ttr = f"+{r['ttr_improvement']:.1f}%" if r['ttr_improvement'] > 0 else f"{r['ttr_improvement']:.1f}%"
        else:
            status = "[red]✗ Failed[/red]"
            failed_count += 1
            ttr = "N/A"
        
        table.add_row(
            r['video'][:30] + "..." if len(r['video']) > 30 else r['video'],
            status,
            f"{r['duration']:.1f}s",
            ttr,
            str(r['visual_keywords']),
        )
    
    console.print(table)
    
    # Overall stats
    console.print(f"\n[bold]Total Videos:[/bold] {len(results)}")
    console.print(f"[green]Successful:[/green] {success_count}")
    console.print(f"[red]Failed:[/red] {failed_count}")
    console.print(f"[bold]Total Time:[/bold] {total_time:.1f}s ({total_time/60:.1f} minutes)")
    
    # Average TTR improvement
    successful = [r for r in results if r['status'] == 'success']
    if successful:
        avg_ttr = sum(r['ttr_improvement'] for r in successful) / len(successful)
        console.print(f"[bold cyan]Average TTR Improvement:[/bold cyan] {avg_ttr:+.1f}%")


def main():
    """Main entry point for batch processing."""
    parser = argparse.ArgumentParser(
        description="Batch process all videos in data/raw/",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    parser.add_argument(
        "-i", "--input",
        type=str,
        default="data/raw",
        help="Input directory containing videos (default: data/raw)"
    )
    
    parser.add_argument(
        "-o", "--output",
        type=str,
        default="output",
        help="Output base directory (default: output)"
    )
    
    parser.add_argument(
        "--interval",
        type=int,
        default=45,
        help="Frame extraction interval in seconds (default: 45)"
    )
    
    parser.add_argument(
        "--mock",
        action="store_true",
        help="Use mock VLM data (faster testing)"
    )
    
    parser.add_argument(
        "--skip-gaze",
        action="store_true",
        help="Skip gaze tracking"
    )
    
    parser.add_argument(
        "--live",
        action="store_true",
        help="Enable live mode: uses 4-bit quantized LLM to fit all models in 24GB VRAM"
    )
    
    args = parser.parse_args()
    
    # Print banner
    console.print(Panel.fit(
        "[bold cyan]BATCH VIDEO PROCESSOR[/bold cyan]\n"
        "Multimodal Banglish Classroom Summarizer",
        border_style="cyan"
    ))
    
    # Find videos
    input_dir = Path(args.input)
    output_dir = Path(args.output)
    
    if not input_dir.exists():
        console.print(f"[red]Error: Input directory not found: {input_dir}[/red]")
        console.print(f"[yellow]Create it and add your videos:[/yellow]")
        console.print(f"  mkdir {input_dir}")
        return 1
    
    videos = find_videos(input_dir)
    
    if not videos:
        console.print(f"[yellow]No video files found in {input_dir}[/yellow]")
        console.print(f"[dim]Supported formats: {', '.join(VIDEO_EXTENSIONS)}[/dim]")
        return 1
    
    # Print configuration
    console.print(f"\n[bold]Configuration:[/bold]")
    console.print(f"  Input directory: {input_dir.absolute()}")
    console.print(f"  Output directory: {output_dir.absolute()}")
    console.print(f"  Frame interval: {args.interval}s")
    console.print(f"  Mock VLM: {args.mock}")
    console.print(f"  Skip gaze: {args.skip_gaze}")
    console.print(f"  Live mode (4-bit LLM): {args.live}")
    
    # List videos
    console.print(f"\n[bold]Found {len(videos)} video(s):[/bold]")
    for i, v in enumerate(videos, 1):
        console.print(f"  {i}. {v.name}")
    
    # Note: Models are loaded on-demand per pipeline stage
    # This is necessary because 24GB VRAM cannot hold all models (~50GB total)
    # The ModelRegistry caches models within each video's processing
    if REGISTRY_AVAILABLE and not args.mock:
        console.print(f"\n[bold cyan]🧠 GPU Model Strategy: Stage-based Loading[/bold cyan]")
        console.print(f"[dim]  24GB VRAM cannot hold all models (~50GB total)[/dim]")
        console.print(f"[dim]  Models will load/unload per pipeline stage[/dim]")
        console.print(f"[dim]  Registry caches models within each video[/dim]\n")
    
    # Confirm
    console.print(f"\n[bold yellow]Starting batch processing...[/bold yellow]")
    console.print(f"[dim]Press Ctrl+C to cancel[/dim]\n")
    time.sleep(2)  # Give user time to cancel
    
    # Process each video
    output_dir.mkdir(parents=True, exist_ok=True)
    results = []
    total_start = time.time()
    
    for i, video in enumerate(videos, 1):
        console.print(f"\n[bold magenta]{'='*60}[/bold magenta]")
        console.print(f"[bold magenta]VIDEO {i}/{len(videos)}[/bold magenta]")
        console.print(f"[bold magenta]{'='*60}[/bold magenta]")
        
        result = process_video(
            video_path=video,
            output_base=output_dir,
            interval=args.interval,
            mock=args.mock,
            skip_gaze=args.skip_gaze,
            live_mode=args.live,
        )
        results.append(result)
        
        # Save intermediate results
        _save_batch_log(results, output_dir)
    
    total_time = time.time() - total_start
    
    # Print final summary
    print_summary(results, total_time)
    
    # Save final log
    _save_batch_log(results, output_dir, final=True)
    
    # Cleanup: Unload all models from registry
    if REGISTRY_AVAILABLE:
        console.print(f"\n[dim]Cleaning up GPU models...[/dim]")
        try:
            registry = ModelRegistry.get_instance()
            registry.unload_all()
            console.print(f"[green]✓ GPU memory cleared[/green]")
        except Exception as e:
            console.print(f"[yellow]⚠ Cleanup warning: {e}[/yellow]")
    
    return 0 if all(r['status'] == 'success' for r in results) else 1


def _save_batch_log(results: list[dict], output_dir: Path, final: bool = False):
    """Save batch processing log to JSON."""
    import json
    
    log_file = output_dir / "batch_log.json"
    
    log_data = {
        'timestamp': datetime.now().isoformat(),
        'completed': final,
        'total_videos': len(results),
        'successful': sum(1 for r in results if r['status'] == 'success'),
        'failed': sum(1 for r in results if r['status'] == 'failed'),
        'results': results,
    }
    
    log_file.write_text(json.dumps(log_data, indent=2), encoding='utf-8')
    
    if final:
        console.print(f"\n[green]✓ Batch log saved to:[/green] {log_file}")


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        console.print("\n[yellow]Batch processing cancelled by user[/yellow]")
        sys.exit(1)
