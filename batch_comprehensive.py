"""
=============================================================================
COMPREHENSIVE BATCH PROCESSOR - All Videos × All Intervals × Gaze Variants
=============================================================================
P2 Evaluation Data Generation

This script runs ALL combinations needed for thesis evaluation:
- 16 videos (7 screen recorded + 9 live classroom)
- 6 frame intervals (5, 10, 15, 20, 25, 30 seconds)
- Gaze variants (with/without for live classroom)

Output Structure:
    output/comprehensive/
        ├── screen_recorded/
        │   ├── interval_05s/
        │   │   ├── L1/
        │   │   ├── L2/
        │   │   └── ...
        │   ├── interval_10s/
        │   └── ...
        └── live_classroom/
            ├── no_gaze/
            │   ├── interval_05s/
            │   │   ├── BanglaASR1/
            │   │   └── ...
            │   └── ...
            └── with_gaze/
                ├── interval_05s/
                └── ...

Total runs: 150 (estimated 15-30 hours depending on video lengths)
=============================================================================
"""

import sys
import time
import json
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Tuple

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich import box

console = Console()

# Configuration
INTERVALS = [5, 10, 15, 20, 25, 30]  # Frame intervals in seconds
VIDEO_EXTENSIONS = {'.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.MOV'}

# Paths
SCREEN_RECORDED_DIR = Path("data/raw/screen_recorded")
LIVE_CLASSROOM_DIR = Path("data/raw/live_classroom")
OUTPUT_BASE = Path("output/comprehensive")


def find_videos(directory: Path) -> List[Path]:
    """Find all video files in directory."""
    videos = []
    for ext in VIDEO_EXTENSIONS:
        videos.extend(directory.glob(f"*{ext}"))
    return sorted(set(videos))


def get_video_name(video_path: Path) -> str:
    """Get clean video name for folder."""
    name = video_path.stem
    # Truncate long names
    if len(name) > 50:
        name = name[:50]
    # Clean special characters
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
        console.print(f"  [cyan]→ {run_id}[/cyan]")
        console.print(f"    Video: {video_path.name[:40]}...")
        console.print(f"    Interval: {interval}s, Gaze: {'OFF' if skip_gaze else 'ON'}")
        console.print(f"    Output: {output_dir}")
        
        pipeline = ThesisPipeline(
            video_path=str(video_path),
            output_dir=str(output_dir),
            frame_interval=interval,
            use_mock_vlm=False,  # Always use real VLM
            skip_gaze=skip_gaze,
            live_mode=True,  # Use 4-bit quantization for 12GB GPU
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
            'video_duration': result.video_duration,
            'ttr_improvement': result.ttr_improvement,
            'visual_keywords': len(result.visual_keywords),
            'gaze_events': len(result.gaze_events),
            'transcript_len': len(result.transcript_fused),
            'notes_len': len(result.final_lecture_notes),
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


def estimate_total_time(screen_videos: List[Path], live_videos: List[Path]) -> str:
    """Estimate total processing time."""
    # Rough estimates based on previous runs:
    # - VLM: ~2 min per frame
    # - Whisper: ~1 min per minute of audio
    # - Average video: ~10 min
    
    n_screen = len(screen_videos)
    n_live = len(live_videos)
    n_intervals = len(INTERVALS)
    
    # Screen: n_videos × n_intervals runs
    # Live: n_videos × n_intervals × 2 (with and without gaze)
    total_runs = (n_screen * n_intervals) + (n_live * n_intervals * 2)
    
    # Assume 15 min average per run
    total_minutes = total_runs * 15
    
    hours = total_minutes // 60
    minutes = total_minutes % 60
    
    return f"{hours}h {minutes}m (estimated)"


def save_progress(results: List[dict], output_dir: Path, completed: bool = False):
    """Save progress log."""
    log_file = output_dir / "comprehensive_batch_log.json"
    
    log_data = {
        'timestamp': datetime.now().isoformat(),
        'completed': completed,
        'total_runs': len(results),
        'successful': sum(1 for r in results if r.get('status') == 'success'),
        'failed': sum(1 for r in results if r.get('status') == 'failed'),
        'results': results,
    }
    
    log_file.write_text(json.dumps(log_data, indent=2), encoding='utf-8')
    return log_file


def main():
    parser = argparse.ArgumentParser(description="Comprehensive batch processing for P2 evaluation")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without running")
    parser.add_argument("--resume", action="store_true", help="Skip already completed runs")
    parser.add_argument("--screen-only", action="store_true", help="Only process screen recordings")
    parser.add_argument("--live-only", action="store_true", help="Only process live classroom")
    parser.add_argument("--interval", type=int, help="Run only specific interval (5,10,15,20,25,30)")
    args = parser.parse_args()
    
    # Banner
    console.print(Panel.fit(
        "[bold cyan]COMPREHENSIVE BATCH PROCESSOR[/bold cyan]\n"
        "[bold]P2 Thesis Evaluation Data Generation[/bold]\n\n"
        "• All 16 videos\n"
        "• 6 frame intervals (5-30s)\n"
        "• Gaze variants for live classroom",
        border_style="cyan"
    ))
    
    # Find videos
    screen_videos = find_videos(SCREEN_RECORDED_DIR) if not args.live_only else []
    live_videos = find_videos(LIVE_CLASSROOM_DIR) if not args.screen_only else []
    
    console.print(f"\n[bold]Videos Found:[/bold]")
    console.print(f"  Screen Recorded: {len(screen_videos)}")
    for v in screen_videos:
        console.print(f"    - {v.name}")
    console.print(f"  Live Classroom: {len(live_videos)}")
    for v in live_videos:
        console.print(f"    - {v.name}")
    
    # Intervals to run
    intervals = [args.interval] if args.interval else INTERVALS
    console.print(f"\n[bold]Frame Intervals:[/bold] {intervals}")
    
    # Calculate runs
    runs = []
    
    # Screen recordings (gaze usually doesn't work, but we'll try without)
    for video in screen_videos:
        video_name = get_video_name(video)
        for interval in intervals:
            output_dir = OUTPUT_BASE / "screen_recorded" / f"interval_{interval:02d}s" / video_name
            runs.append({
                'video': video,
                'output_dir': output_dir,
                'interval': interval,
                'skip_gaze': True,  # Skip gaze for screen recordings (no person visible)
                'category': 'screen_recorded',
            })
    
    # Live classroom - WITHOUT gaze
    for video in live_videos:
        video_name = get_video_name(video)
        for interval in intervals:
            output_dir = OUTPUT_BASE / "live_classroom" / "no_gaze" / f"interval_{interval:02d}s" / video_name
            runs.append({
                'video': video,
                'output_dir': output_dir,
                'interval': interval,
                'skip_gaze': True,
                'category': 'live_no_gaze',
            })
    
    # Live classroom - WITH gaze
    for video in live_videos:
        video_name = get_video_name(video)
        for interval in intervals:
            output_dir = OUTPUT_BASE / "live_classroom" / "with_gaze" / f"interval_{interval:02d}s" / video_name
            runs.append({
                'video': video,
                'output_dir': output_dir,
                'interval': interval,
                'skip_gaze': False,  # ENABLE gaze tracking
                'category': 'live_with_gaze',
            })
    
    console.print(f"\n[bold]Total Runs Planned:[/bold] {len(runs)}")
    console.print(f"  - Screen Recorded: {len(screen_videos) * len(intervals)}")
    console.print(f"  - Live (no gaze): {len(live_videos) * len(intervals)}")
    console.print(f"  - Live (with gaze): {len(live_videos) * len(intervals)}")
    
    # Estimate time
    est_time = estimate_total_time(screen_videos, live_videos)
    console.print(f"\n[bold yellow]Estimated Time:[/bold yellow] {est_time}")
    
    if args.dry_run:
        console.print("\n[yellow]DRY RUN - No processing will occur[/yellow]")
        
        table = Table(title="Planned Runs", box=box.SIMPLE)
        table.add_column("#", style="dim")
        table.add_column("Category")
        table.add_column("Video")
        table.add_column("Interval")
        table.add_column("Gaze")
        table.add_column("Output")
        
        for i, run in enumerate(runs[:20], 1):  # Show first 20
            table.add_row(
                str(i),
                run['category'],
                run['video'].name[:25] + "...",
                f"{run['interval']}s",
                "OFF" if run['skip_gaze'] else "ON",
                str(run['output_dir'])[-40:],
            )
        
        if len(runs) > 20:
            table.add_row("...", "...", "...", "...", "...", "...")
        
        console.print(table)
        return 0
    
    # Resume check
    if args.resume:
        completed_dirs = set()
        log_file = OUTPUT_BASE / "comprehensive_batch_log.json"
        if log_file.exists():
            with open(log_file) as f:
                prev_log = json.load(f)
                for r in prev_log.get('results', []):
                    if r.get('status') == 'success':
                        completed_dirs.add(r.get('output_dir'))
        
        original_count = len(runs)
        runs = [r for r in runs if str(r['output_dir']) not in completed_dirs]
        console.print(f"\n[yellow]Resuming: Skipping {original_count - len(runs)} completed runs[/yellow]")
    
    # Confirm
    console.print(f"\n[bold red]Starting in 5 seconds... Press Ctrl+C to cancel[/bold red]")
    time.sleep(5)
    
    # Create output directory
    OUTPUT_BASE.mkdir(parents=True, exist_ok=True)
    
    # Process all runs
    results = []
    total_start = time.time()
    
    for i, run in enumerate(runs, 1):
        console.print(f"\n[bold magenta]{'='*70}[/bold magenta]")
        console.print(f"[bold magenta]RUN {i}/{len(runs)} ({i/len(runs)*100:.0f}%)[/bold magenta]")
        console.print(f"[bold magenta]{'='*70}[/bold magenta]")
        
        run_id = f"{run['category']}_int{run['interval']:02d}_{get_video_name(run['video'])}"
        
        result = run_single_video(
            video_path=run['video'],
            output_dir=run['output_dir'],
            interval=run['interval'],
            skip_gaze=run['skip_gaze'],
            run_id=run_id,
        )
        
        results.append(result)
        
        # Save progress after each run
        save_progress(results, OUTPUT_BASE, completed=False)
        
        # ETA
        elapsed = time.time() - total_start
        avg_per_run = elapsed / i
        remaining = (len(runs) - i) * avg_per_run
        eta = datetime.now() + timedelta(seconds=remaining)
        console.print(f"\n[dim]Elapsed: {elapsed/60:.0f}m | ETA: {eta.strftime('%H:%M')} ({remaining/60:.0f}m remaining)[/dim]")
    
    # Final summary
    total_time = time.time() - total_start
    
    console.print(f"\n\n[bold green]{'='*70}[/bold green]")
    console.print(f"[bold green]COMPREHENSIVE BATCH COMPLETE[/bold green]")
    console.print(f"[bold green]{'='*70}[/bold green]")
    
    successful = sum(1 for r in results if r.get('status') == 'success')
    failed = sum(1 for r in results if r.get('status') == 'failed')
    
    console.print(f"\n[bold]Summary:[/bold]")
    console.print(f"  Total runs: {len(results)}")
    console.print(f"  [green]Successful: {successful}[/green]")
    console.print(f"  [red]Failed: {failed}[/red]")
    console.print(f"  Total time: {total_time/3600:.1f} hours")
    
    # Save final log
    log_file = save_progress(results, OUTPUT_BASE, completed=True)
    console.print(f"\n[green]✓ Log saved to:[/green] {log_file}")
    
    # Cleanup GPU
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
        console.print("\n[yellow]Batch processing cancelled by user[/yellow]")
        sys.exit(1)
