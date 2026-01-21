"""
Main Pipeline Execution Script
==============================
Run the complete multimodal summarization pipeline.
"""

import argparse
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils import load_config, setup_logging, get_device, ensure_dir


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Multimodal Banglish Classroom Summarizer"
    )
    parser.add_argument(
        "--input", "-i",
        type=str,
        required=True,
        help="Path to input video file"
    )
    parser.add_argument(
        "--output", "-o",
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
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    return parser.parse_args()


def main():
    """Main pipeline execution."""
    args = parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    # Setup logging
    logger = setup_logging(
        log_dir=config["paths"]["logs"],
        name="pipeline"
    )
    
    # Get device
    device = get_device()
    logger.info(f"Using device: {device}")
    
    # Verify input exists
    input_path = Path(args.input)
    if not input_path.exists():
        logger.error(f"Input file not found: {input_path}")
        return 1
    
    # Ensure output directory
    output_dir = ensure_dir(args.output)
    logger.info(f"Output directory: {output_dir}")
    
    # TODO: Implement pipeline steps
    # 1. Extract audio from video
    # 2. Transcribe audio (Whisper)
    # 3. Extract frames from video
    # 4. Detect whiteboard and run OCR
    # 5. Align audio and visual streams
    # 6. Generate notes with LLM
    
    logger.info("Pipeline not yet implemented - Phase 1 complete!")
    logger.info("Run verify_stack.py to confirm environment setup.")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
