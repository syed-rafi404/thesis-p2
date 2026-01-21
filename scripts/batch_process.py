"""
Batch Processing Script
=======================
Process multiple lecture videos in batch.
"""

import argparse
import sys
from pathlib import Path
from typing import List

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils import load_config, setup_logging, ensure_dir


def find_videos(input_dir: str, extensions: List[str] = None) -> List[Path]:
    """
    Find all video files in a directory.
    
    Args:
        input_dir: Directory to search
        extensions: List of valid extensions
        
    Returns:
        List of video file paths
    """
    if extensions is None:
        extensions = [".mp4", ".mkv", ".avi", ".mov", ".webm"]
    
    input_path = Path(input_dir)
    videos = []
    
    for ext in extensions:
        videos.extend(input_path.glob(f"*{ext}"))
        videos.extend(input_path.glob(f"*{ext.upper()}"))
    
    return sorted(videos)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Batch process lecture videos"
    )
    parser.add_argument(
        "--input-dir", "-i",
        type=str,
        default="data/raw",
        help="Directory containing input videos"
    )
    parser.add_argument(
        "--output-dir", "-o",
        type=str,
        default="data/outputs",
        help="Output directory for generated notes"
    )
    parser.add_argument(
        "--config", "-c",
        type=str,
        default="config/config.yaml",
        help="Path to configuration file"
    )
    parser.add_argument(
        "--max-videos", "-n",
        type=int,
        default=None,
        help="Maximum number of videos to process"
    )
    return parser.parse_args()


def main():
    """Main batch processing."""
    args = parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    # Setup logging
    logger = setup_logging(
        log_dir=config["paths"]["logs"],
        name="batch_process"
    )
    
    # Find videos
    videos = find_videos(args.input_dir)
    
    if args.max_videos:
        videos = videos[:args.max_videos]
    
    logger.info(f"Found {len(videos)} videos to process")
    
    if not videos:
        logger.warning("No videos found in input directory")
        return 0
    
    # Ensure output directory
    output_dir = ensure_dir(args.output_dir)
    
    # Process each video
    for i, video_path in enumerate(videos, 1):
        logger.info(f"[{i}/{len(videos)}] Processing: {video_path.name}")
        
        # TODO: Call run_pipeline for each video
        logger.info(f"  → Skipped (pipeline not implemented)")
    
    logger.info("Batch processing complete!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
