"""
=============================================================================
VIDEO INGESTOR - Batch Processing for Lecture Videos
=============================================================================
Multimodal Banglish Classroom Summarizer
Master's Thesis - Phase 1

This module extracts audio and frames from a lecture video file
for processing by Whisper (ASR) and Qwen2-VL (whiteboard understanding).

Input: Video file (mp4, mkv, avi, mov, webm)
Output:
  - temp/full_audio.wav (16kHz mono)
  - temp/frames/frame_000000.jpg, frame_000030.jpg, ...
  - Metadata JSON with timestamps
=============================================================================
"""

import os
import json
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import timedelta

import cv2
import numpy as np

try:
    from moviepy.editor import VideoFileClip
    MOVIEPY_AVAILABLE = True
except ImportError:
    MOVIEPY_AVAILABLE = False

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

console = Console()


@dataclass
class FrameMetadata:
    """Metadata for a single extracted frame."""
    time: float          # Timestamp in seconds
    time_str: str        # Human-readable timestamp (HH:MM:SS)
    frame_path: str      # Path to extracted frame
    frame_index: int     # Frame number (0, 1, 2, ...)


@dataclass 
class IngestResult:
    """Result of video ingestion."""
    video_path: str
    duration: float
    audio_path: str
    frames_dir: str
    frames: List[FrameMetadata]
    total_frames: int
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "video_path": self.video_path,
            "duration": self.duration,
            "duration_str": str(timedelta(seconds=int(self.duration))),
            "audio_path": self.audio_path,
            "frames_dir": self.frames_dir,
            "total_frames": self.total_frames,
            "frames": [
                {
                    "time": f.time,
                    "time_str": f.time_str,
                    "frame": f.frame_path,
                    "index": f.frame_index
                }
                for f in self.frames
            ]
        }
    
    def save_metadata(self, output_path: str):
        """Save metadata to JSON file."""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)


class VideoIngestor:
    """
    Extracts audio and frames from lecture videos for AI processing.
    
    Usage:
        ingestor = VideoIngestor(output_dir="temp")
        result = ingestor.process("lecture.mp4", frame_interval=30)
        
        # Audio is at: result.audio_path
        # Frames are at: result.frames[i].frame_path
        # Save metadata: result.save_metadata("metadata.json")
    """
    
    def __init__(
        self,
        output_dir: str = "temp",
        audio_sample_rate: int = 16000,
        audio_channels: int = 1,
        frame_quality: int = 95
    ):
        """
        Initialize VideoIngestor.
        
        Args:
            output_dir: Directory for extracted audio and frames
            audio_sample_rate: Sample rate for audio (16kHz for Whisper)
            audio_channels: Number of audio channels (1 = mono)
            frame_quality: JPEG quality for frames (1-100)
        """
        self.output_dir = Path(output_dir)
        self.audio_sample_rate = audio_sample_rate
        self.audio_channels = audio_channels
        self.frame_quality = frame_quality
        
        # Create output directories
        self.audio_dir = self.output_dir
        self.frames_dir = self.output_dir / "frames"
        
    def process(
        self,
        video_path: str,
        frame_interval: float = 30.0
    ) -> IngestResult:
        """
        Process a video file - extract audio and frames.
        
        Args:
            video_path: Path to input video file
            frame_interval: Seconds between frame extractions (default: 30)
            
        Returns:
            IngestResult with paths and metadata
        """
        video_path = Path(video_path)
        
        if not video_path.exists():
            raise FileNotFoundError(f"Video not found: {video_path}")
        
        console.print(f"\n[bold cyan]📹 Processing Video:[/bold cyan] {video_path.name}")
        
        # Get video info
        duration = self._get_video_duration(video_path)
        console.print(f"[dim]Duration: {timedelta(seconds=int(duration))}[/dim]")
        
        # Create output directories
        self.audio_dir.mkdir(parents=True, exist_ok=True)
        self.frames_dir.mkdir(parents=True, exist_ok=True)
        
        # Extract audio
        audio_path = self.extract_audio(video_path)
        
        # Extract frames
        frames = self.extract_frames(video_path, frame_interval)
        
        # Create result
        result = IngestResult(
            video_path=str(video_path.absolute()),
            duration=duration,
            audio_path=str(audio_path.absolute()),
            frames_dir=str(self.frames_dir.absolute()),
            frames=frames,
            total_frames=len(frames)
        )
        
        # Save metadata
        metadata_path = self.output_dir / "ingest_metadata.json"
        result.save_metadata(str(metadata_path))
        
        console.print(f"\n[green]✅ Ingestion complete![/green]")
        console.print(f"[dim]Audio: {audio_path}[/dim]")
        console.print(f"[dim]Frames: {len(frames)} extracted to {self.frames_dir}[/dim]")
        console.print(f"[dim]Metadata: {metadata_path}[/dim]")
        
        return result
    
    def extract_audio(self, video_path: Path) -> Path:
        """
        Extract full audio from video to WAV file.
        
        Args:
            video_path: Path to input video
            
        Returns:
            Path to extracted audio file (16kHz mono WAV)
        """
        output_path = self.audio_dir / "full_audio.wav"
        
        console.print("\n[bold]🎵 Extracting Audio...[/bold]")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Extracting audio track...", total=None)
            
            # Try FFmpeg first (faster and more reliable)
            if self._ffmpeg_available():
                self._extract_audio_ffmpeg(video_path, output_path)
            elif MOVIEPY_AVAILABLE:
                self._extract_audio_moviepy(video_path, output_path)
            else:
                raise RuntimeError(
                    "Neither FFmpeg nor MoviePy available. "
                    "Install FFmpeg or run: pip install moviepy"
                )
            
            progress.remove_task(task)
        
        # Verify output
        if not output_path.exists():
            raise RuntimeError(f"Audio extraction failed: {output_path}")
        
        file_size = output_path.stat().st_size / (1024 * 1024)
        console.print(f"  [green]✓[/green] Audio extracted: {output_path.name} ({file_size:.1f} MB)")
        
        return output_path
    
    def extract_frames(
        self,
        video_path: Path,
        interval: float = 30.0
    ) -> List[FrameMetadata]:
        """
        Extract frames from video at specified interval.
        
        Args:
            video_path: Path to input video
            interval: Seconds between frame extractions
            
        Returns:
            List of FrameMetadata objects
        """
        console.print(f"\n[bold]🖼️  Extracting Frames (every {interval}s)...[/bold]")
        
        # Open video
        cap = cv2.VideoCapture(str(video_path))
        
        if not cap.isOpened():
            raise RuntimeError(f"Cannot open video: {video_path}")
        
        # Get video properties
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps if fps > 0 else 0
        
        # Calculate frame positions
        frame_times = []
        t = 0.0
        while t < duration:
            frame_times.append(t)
            t += interval
        
        frames_metadata = []
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console,
        ) as progress:
            task = progress.add_task("Extracting frames...", total=len(frame_times))
            
            for idx, timestamp in enumerate(frame_times):
                # Seek to timestamp
                frame_number = int(timestamp * fps)
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
                
                ret, frame = cap.read()
                
                if not ret:
                    console.print(f"  [yellow]⚠ Could not read frame at {timestamp:.1f}s[/yellow]")
                    progress.advance(task)
                    continue
                
                # Generate filename with timestamp
                time_str = self._format_timestamp(timestamp)
                frame_filename = f"frame_{idx:06d}_{int(timestamp):06d}s.jpg"
                frame_path = self.frames_dir / frame_filename
                
                # Save frame
                cv2.imwrite(
                    str(frame_path),
                    frame,
                    [cv2.IMWRITE_JPEG_QUALITY, self.frame_quality]
                )
                
                # Create metadata
                metadata = FrameMetadata(
                    time=timestamp,
                    time_str=time_str,
                    frame_path=str(frame_path.absolute()),
                    frame_index=idx
                )
                frames_metadata.append(metadata)
                
                progress.advance(task)
        
        cap.release()
        
        console.print(f"  [green]✓[/green] Extracted {len(frames_metadata)} frames")
        
        return frames_metadata
    
    def _get_video_duration(self, video_path: Path) -> float:
        """Get video duration in seconds."""
        cap = cv2.VideoCapture(str(video_path))
        
        if not cap.isOpened():
            raise RuntimeError(f"Cannot open video: {video_path}")
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps if fps > 0 else 0
        
        cap.release()
        return duration
    
    def _ffmpeg_available(self) -> bool:
        """Check if FFmpeg is available."""
        try:
            result = subprocess.run(
                ["ffmpeg", "-version"],
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except FileNotFoundError:
            return False
    
    def _extract_audio_ffmpeg(self, video_path: Path, output_path: Path):
        """Extract audio using FFmpeg."""
        cmd = [
            "ffmpeg",
            "-i", str(video_path),
            "-vn",                          # No video
            "-acodec", "pcm_s16le",         # 16-bit PCM
            "-ar", str(self.audio_sample_rate),  # Sample rate
            "-ac", str(self.audio_channels),     # Channels
            "-y",                           # Overwrite output
            str(output_path)
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            raise RuntimeError(f"FFmpeg error: {result.stderr}")
    
    def _extract_audio_moviepy(self, video_path: Path, output_path: Path):
        """Extract audio using MoviePy (fallback)."""
        video = VideoFileClip(str(video_path))
        audio = video.audio
        
        if audio is None:
            raise RuntimeError("Video has no audio track")
        
        audio.write_audiofile(
            str(output_path),
            fps=self.audio_sample_rate,
            nbytes=2,  # 16-bit
            codec='pcm_s16le',
            ffmpeg_params=["-ac", str(self.audio_channels)],
            verbose=False,
            logger=None
        )
        
        video.close()
    
    def _format_timestamp(self, seconds: float) -> str:
        """Format seconds to HH:MM:SS."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        return f"{minutes:02d}:{secs:02d}"


# =============================================================================
# CLI Entry Point
# =============================================================================
def main():
    """Command-line interface for video ingestion."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Extract audio and frames from lecture videos"
    )
    parser.add_argument(
        "video",
        type=str,
        help="Path to input video file"
    )
    parser.add_argument(
        "--output-dir", "-o",
        type=str,
        default="temp",
        help="Output directory (default: temp)"
    )
    parser.add_argument(
        "--interval", "-i",
        type=float,
        default=30.0,
        help="Frame extraction interval in seconds (default: 30)"
    )
    parser.add_argument(
        "--sample-rate", "-r",
        type=int,
        default=16000,
        help="Audio sample rate in Hz (default: 16000)"
    )
    
    args = parser.parse_args()
    
    ingestor = VideoIngestor(
        output_dir=args.output_dir,
        audio_sample_rate=args.sample_rate
    )
    
    result = ingestor.process(
        video_path=args.video,
        frame_interval=args.interval
    )
    
    # Print summary
    console.print("\n[bold]📋 Extraction Summary:[/bold]")
    console.print(f"  Video: {result.video_path}")
    console.print(f"  Duration: {timedelta(seconds=int(result.duration))}")
    console.print(f"  Audio: {result.audio_path}")
    console.print(f"  Frames: {result.total_frames} files in {result.frames_dir}")
    
    return result


if __name__ == "__main__":
    main()
