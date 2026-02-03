"""
=============================================================================
LIVE CLASSROOM BATCH PROCESSOR - 9 Videos × 3 Intervals × Gaze Variants
=============================================================================
Focused processing for P2 deadline:
- 9 live classroom videos (BanglaASR1-9)
- 3 frame intervals (10, 20, 30 seconds)
- With and without gaze tracking

Total runs: 54 (estimated 22-28 hours)
=============================================================================
"""

import sys
import time
import json
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from typing import List

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

console = Console()

# Configuration - FOCUSED FOR DEADLINE
INTERVALS = [10, 20, 30]  # Skip 5s (too slow), skip 15s, 25s (redundant)
VIDEO_EXTENSIONS = {'.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.MOV'}

# Paths
LIVE_CLASSROOM_DIR = Path("data/raw/live_classroom")
OUTPUT_BASE = Path("output/live_focused")


def find_videos(directory: Path) -> List[Path]:
    """Find all video files in directory."""
    videos = []
    for ext in VIDEO_EXTENSIONS:
        videos.extend(directory.glob(f"*{ext}"))
    return sorted(set(videos))


def get_video_name(video_path: Path) -> str:
    """Get clean video name for folder."""
    name = video_path.stem
    if len(name) > 50:
        name = name[:50]
    name = name.replace(" ", "_").replace("-", "_")
    return name


def run_single_video(
    video_path: Path,
    output_dir: Path,
    interval: int,
    skip_gaze: bool,
    run_id: str,
) -> dict:
    """Process a single video with given parameters."""
    from run_thesis import ThesisPipeline
    
    start_time = time.time()
    
    try:
        console.print(f"\n  [cyan]→ {run_id}[/cyan]")
        console.print(f"    Video: {video_path.name}")
        console.print(f"    Interval: {interval}s, Gaze: {'ON 👁️' if not skip_gaze else 'OFF'}")
        console.print(f"    Output: {output_dir}")
        
        pipeline = ThesisPipeline(
            video_path=str(video_path),
            output_dir=str(output_dir),
            frame_interval=interval,
            use_mock_vlm=False,
            skip_gaze=skip_gaze,
            live_mode=False,  # Use FP16 for quality
        )
        
        result = pipeline.run()
        
        duration = time.time() - start_time
        
        return {
            'status': 'success',
            'run_id': run_id,
            'video': video_path.name,
            'interval': interval,
            'gaze': not skip_gaze,
            'output_dir': str(output_dir),
            'duration_sec': duration,
            'duration_min': round(duration / 60, 1),
            'video_duration': result.video_duration,
            'ttr_improvement': result.ttr_improvement,
            'visual_keywords': len(result.visual_keywords),
            'gaze_events': len(result.gaze_events),
            'transcript_len': len(result.transcript_fused),
            'notes_len': len(result.final_lecture_notes),
            'quality_score': getattr(result, 'quality_score', 0),
            'error': None,
        }
        
    except Exception as e:
        duration = time.time() - start_time
        console.print(f"    [red]ERROR: {e}[/red]")
        import traceback
        traceback.print_exc()
        
        return {
            'status': 'failed',
            'run_id': run_id,
            'video': video_path.name,
            'interval': interval,
            'gaze': not skip_gaze,
            'output_dir': str(output_dir),
            'duration_sec': duration,
            'error': str(e),
        }


def save_progress(results: List[dict], output_dir: Path, completed: bool = False):
    """Save progress log."""
    log_file = output_dir / "live_batch_log.json"
    
    log_data = {
        'timestamp': datetime.now().isoformat(),
        'completed': completed,
        'total_runs': len(results),
        'successful': sum(1 for r in results if r.get('status') == 'success'),
        'failed': sum(1 for r in results if r.get('status') == 'failed'),
        'results': results,
    }
    
    output_dir.mkdir(parents=True, exist_ok=True)
    with open(log_file, 'w') as f:
        json.dump(log_data, f, indent=2, default=str)
    
    return log_file


def main():
    parser = argparse.ArgumentParser(description="Live Classroom Focused Batch Processor")
    parser.add_argument("--dry-run", action="store_true", help="Show plan without processing")
    parser.add_argument("--resume", action="store_true", help="Resume from previous run")
    parser.add_argument("--no-gaze-only", action="store_true", help="Only run no-gaze variants (skip gaze runs)")
    args = parser.parse_args()
    
    console.print(Panel(
        "[bold cyan]LIVE CLASSROOM FOCUSED BATCH[/bold cyan]\n\n"
        "• 9 live classroom videos\n"
        "• 3 intervals (10s, 20s, 30s)\n"
        + ("• NO GAZE ONLY (P2 mode)\n" if args.no_gaze_only else "• With AND without gaze tracking\n")
        + f"• Total: {27 if args.no_gaze_only else 54} runs",
        border_style="green"
    ))
    
    # Find videos
    live_videos = find_videos(LIVE_CLASSROOM_DIR)
    
    console.print(f"\n[bold]Live Classroom Videos Found: {len(live_videos)}[/bold]")
    for v in live_videos:
        console.print(f"    - {v.name}")
    
    console.print(f"\n[bold]Frame Intervals:[/bold] {INTERVALS}")
    
    # Build run list
    runs = []
    
    # WITHOUT gaze first (faster, good baseline)
    for video in live_videos:
        video_name = get_video_name(video)
        for interval in INTERVALS:
            output_dir = OUTPUT_BASE / "no_gaze" / f"interval_{interval:02d}s" / video_name
            runs.append({
                'video': video,
                'output_dir': output_dir,
                'interval': interval,
                'skip_gaze': True,
                'category': 'no_gaze',
            })
    
    # WITH gaze (slower but shows novelty) - skip if --no-gaze-only
    if not args.no_gaze_only:
        for video in live_videos:
            video_name = get_video_name(video)
            for interval in INTERVALS:
                output_dir = OUTPUT_BASE / "with_gaze" / f"interval_{interval:02d}s" / video_name
                runs.append({
                    'video': video,
                    'output_dir': output_dir,
                    'interval': interval,
                    'skip_gaze': False,
                    'category': 'with_gaze',
                })
    
    console.print(f"\n[bold]Total Runs Planned:[/bold] {len(runs)}")
    console.print(f"  - Without gaze: {len(live_videos) * len(INTERVALS)}")
    if not args.no_gaze_only:
        console.print(f"  - With gaze: {len(live_videos) * len(INTERVALS)}")
    else:
        console.print(f"  - With gaze: [dim]SKIPPED (--no-gaze-only)[/dim]")
    console.print(f"\n[bold yellow]Estimated Time:[/bold yellow] {'5-8' if args.no_gaze_only else '22-28'} hours")
    
    if args.dry_run:
        console.print("\n[yellow]DRY RUN - Showing planned runs:[/yellow]\n")
        
        table = Table(title="Planned Runs", box=box.SIMPLE)
        table.add_column("#", style="dim")
        table.add_column("Gaze")
        table.add_column("Video")
        table.add_column("Interval")
        
        for i, run in enumerate(runs, 1):
            table.add_row(
                str(i),
                "👁️ ON" if not run['skip_gaze'] else "OFF",
                run['video'].stem[:40],
                f"{run['interval']}s"
            )
        
        console.print(table)
        return 0
    
    # Resume support - check for existing output directories with final_lecture_notes.md
    if args.resume:
        original = len(runs)
        completed_runs = []
        
        for run in runs:
            output_dir = run['output_dir']
            # Check if output directory exists AND has final_lecture_notes.md (means completed successfully)
            notes_file = output_dir / "final_lecture_notes.md"
            if notes_file.exists():
                completed_runs.append(run)
        
        runs = [r for r in runs if r not in completed_runs]
        console.print(f"\n[yellow]Resuming: Skipping {len(completed_runs)} completed runs (found final_lecture_notes.md)[/yellow]")
        
        if completed_runs:
            console.print(f"[dim]Completed directories:[/dim]")
            for r in completed_runs[:5]:  # Show first 5
                console.print(f"  [dim]✓ {r['output_dir']}[/dim]")
            if len(completed_runs) > 5:
                console.print(f"  [dim]... and {len(completed_runs) - 5} more[/dim]")
    
    console.print(f"\n[bold red]Starting in 5 seconds... Press Ctrl+C to cancel[/bold red]")
    time.sleep(5)
    
    OUTPUT_BASE.mkdir(parents=True, exist_ok=True)
    
    results = []
    total_start = time.time()
    
    for i, run in enumerate(runs, 1):
        console.print(f"\n[bold magenta]{'='*70}[/bold magenta]")
        console.print(f"[bold magenta]RUN {i}/{len(runs)} ({i/len(runs)*100:.0f}%)[/bold magenta]")
        console.print(f"[bold magenta]{'='*70}[/bold magenta]")
        
        gaze_str = "gaze" if not run['skip_gaze'] else "nogaze"
        run_id = f"{gaze_str}_int{run['interval']:02d}_{get_video_name(run['video'])}"
        
        result = run_single_video(
            video_path=run['video'],
            output_dir=run['output_dir'],
            interval=run['interval'],
            skip_gaze=run['skip_gaze'],
            run_id=run_id,
        )
        
        results.append(result)
        save_progress(results, OUTPUT_BASE, completed=False)
        
        # Progress stats
        elapsed = time.time() - total_start
        avg_per_run = elapsed / i
        remaining = (len(runs) - i) * avg_per_run
        eta = datetime.now() + timedelta(seconds=remaining)
        
        console.print(f"\n[dim]Run time: {result.get('duration_min', 0):.1f}m | "
                     f"Elapsed: {elapsed/60:.0f}m | "
                     f"ETA: {eta.strftime('%b %d %H:%M')} ({remaining/3600:.1f}h remaining)[/dim]")
    
    # Final summary
    total_time = time.time() - total_start
    
    console.print(f"\n\n[bold green]{'='*70}[/bold green]")
    console.print(f"[bold green]LIVE CLASSROOM BATCH COMPLETE! 🎉[/bold green]")
    console.print(f"[bold green]{'='*70}[/bold green]")
    
    successful = sum(1 for r in results if r.get('status') == 'success')
    failed = sum(1 for r in results if r.get('status') == 'failed')
    
    console.print(f"\n[bold]Summary:[/bold]")
    console.print(f"  Total runs: {len(results)}")
    console.print(f"  [green]Successful: {successful}[/green]")
    console.print(f"  [red]Failed: {failed}[/red]")
    console.print(f"  Total time: {total_time/3600:.1f} hours")
    
    # Gaze comparison summary
    gaze_results = [r for r in results if r.get('gaze') and r.get('status') == 'success']
    no_gaze_results = [r for r in results if not r.get('gaze') and r.get('status') == 'success']
    
    if gaze_results and no_gaze_results:
        avg_gaze_events = sum(r.get('gaze_events', 0) for r in gaze_results) / len(gaze_results)
        console.print(f"\n[bold]Gaze Analysis:[/bold]")
        console.print(f"  Avg gaze events detected: {avg_gaze_events:.1f}")
    
    log_file = save_progress(results, OUTPUT_BASE, completed=True)
    console.print(f"\n[green]✓ Log saved to:[/green] {log_file}")
    
    # Cleanup
    try:
        from src.model_registry import ModelRegistry
        registry = ModelRegistry.get_instance()
        registry.unload_all()
        console.print("[green]✓ GPU memory cleared[/green]")
    except:
        pass
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        console.print("\n[yellow]Batch cancelled by user[/yellow]")
        sys.exit(1)
