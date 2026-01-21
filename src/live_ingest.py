"""
=============================================================================
LIVE INGEST - Real-Time Audio & Video Capture
=============================================================================
Multimodal Banglish Classroom Summarizer
Master's Thesis

This script captures LIVE feeds from:
1. Microphone → 10-second audio chunks → latest_audio_chunk.wav
2. Webcam → frame every 30 seconds → latest_board_frame.jpg

Both streams run in parallel using threading.
AI models can read the temp files instantly for real-time processing.

Hardware: Windows 11 | RTX 3090
=============================================================================
"""

import os
import sys
import time
import wave
import threading
from pathlib import Path
from datetime import datetime
from typing import Optional, Callable
from dataclasses import dataclass

import cv2
import numpy as np

try:
    import pyaudio
except ImportError:
    print("ERROR: pyaudio not installed. Run: pip install pyaudio")
    print("On Windows, you may need: pip install pipwin && pipwin install pyaudio")
    sys.exit(1)

from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.panel import Panel

console = Console()


# =============================================================================
# Configuration
# =============================================================================
@dataclass
class IngestConfig:
    """Configuration for live ingestion."""
    # Audio settings
    audio_chunk_duration: float = 10.0  # seconds per audio chunk
    audio_sample_rate: int = 16000      # 16kHz for Whisper
    audio_channels: int = 1              # Mono
    audio_format: int = pyaudio.paInt16  # 16-bit
    
    # Video settings
    frame_capture_interval: float = 30.0  # seconds between frame captures
    camera_index: int = 0                  # Default webcam
    frame_width: int = 1280               # Capture resolution
    frame_height: int = 720
    
    # Output paths
    output_dir: str = "data/live"
    audio_output: str = "latest_audio_chunk.wav"
    frame_output: str = "latest_board_frame.jpg"
    
    # Control
    max_runtime: Optional[float] = None  # None = run forever


# =============================================================================
# Audio Capture Thread
# =============================================================================
class AudioCapture:
    """
    Captures audio from microphone in fixed-duration chunks.
    Saves each chunk to a WAV file for immediate processing.
    """
    
    def __init__(self, config: IngestConfig, output_dir: Path):
        self.config = config
        self.output_dir = output_dir
        self.output_path = output_dir / config.audio_output
        
        self.pyaudio = pyaudio.PyAudio()
        self.stream: Optional[pyaudio.Stream] = None
        self.is_running = False
        self.thread: Optional[threading.Thread] = None
        
        # Stats
        self.chunks_captured = 0
        self.last_capture_time: Optional[datetime] = None
        self.error: Optional[str] = None
        
    def _get_device_info(self) -> dict:
        """Get default input device info."""
        try:
            return self.pyaudio.get_default_input_device_info()
        except Exception:
            return {"name": "Unknown", "index": 0}
    
    def start(self):
        """Start audio capture in background thread."""
        if self.is_running:
            return
            
        self.is_running = True
        self.thread = threading.Thread(target=self._capture_loop, daemon=True)
        self.thread.start()
        
    def stop(self):
        """Stop audio capture."""
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=2.0)
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.pyaudio.terminate()
        
    def _capture_loop(self):
        """Main capture loop - runs in background thread."""
        try:
            # Calculate buffer sizes
            chunk_size = 1024
            chunks_per_buffer = int(
                self.config.audio_sample_rate * self.config.audio_chunk_duration / chunk_size
            )
            
            # Open audio stream
            self.stream = self.pyaudio.open(
                format=self.config.audio_format,
                channels=self.config.audio_channels,
                rate=self.config.audio_sample_rate,
                input=True,
                frames_per_buffer=chunk_size
            )
            
            while self.is_running:
                frames = []
                
                # Record for chunk_duration seconds
                for _ in range(chunks_per_buffer):
                    if not self.is_running:
                        break
                    try:
                        data = self.stream.read(chunk_size, exception_on_overflow=False)
                        frames.append(data)
                    except Exception as e:
                        self.error = f"Read error: {e}"
                        break
                
                if frames and self.is_running:
                    # Save to WAV file
                    self._save_wav(frames)
                    self.chunks_captured += 1
                    self.last_capture_time = datetime.now()
                    
        except Exception as e:
            self.error = str(e)
        finally:
            if self.stream:
                self.stream.stop_stream()
                self.stream.close()
    
    def _save_wav(self, frames: list):
        """Save audio frames to WAV file."""
        # Write to temp file first, then rename (atomic operation)
        temp_path = self.output_path.with_suffix('.tmp')
        
        with wave.open(str(temp_path), 'wb') as wf:
            wf.setnchannels(self.config.audio_channels)
            wf.setsampwidth(self.pyaudio.get_sample_size(self.config.audio_format))
            wf.setframerate(self.config.audio_sample_rate)
            wf.writeframes(b''.join(frames))
        
        # Atomic rename
        temp_path.replace(self.output_path)


# =============================================================================
# Video Capture Thread
# =============================================================================
class VideoCapture:
    """
    Captures frames from webcam at fixed intervals.
    Saves each frame as a JPEG for immediate processing.
    """
    
    def __init__(self, config: IngestConfig, output_dir: Path):
        self.config = config
        self.output_dir = output_dir
        self.output_path = output_dir / config.frame_output
        
        self.cap: Optional[cv2.VideoCapture] = None
        self.is_running = False
        self.thread: Optional[threading.Thread] = None
        
        # Stats
        self.frames_captured = 0
        self.last_capture_time: Optional[datetime] = None
        self.error: Optional[str] = None
        self.camera_name: str = "Unknown"
        
    def start(self):
        """Start video capture in background thread."""
        if self.is_running:
            return
            
        self.is_running = True
        self.thread = threading.Thread(target=self._capture_loop, daemon=True)
        self.thread.start()
        
    def stop(self):
        """Stop video capture."""
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=2.0)
        if self.cap:
            self.cap.release()
            
    def _capture_loop(self):
        """Main capture loop - runs in background thread."""
        try:
            # Open camera
            self.cap = cv2.VideoCapture(self.config.camera_index)
            
            if not self.cap.isOpened():
                self.error = f"Cannot open camera {self.config.camera_index}"
                return
            
            # Set resolution
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.config.frame_width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.config.frame_height)
            
            # Get actual camera info
            actual_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            actual_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self.camera_name = f"Camera {self.config.camera_index} ({actual_width}x{actual_height})"
            
            last_capture = 0
            
            while self.is_running:
                current_time = time.time()
                
                # Always read frames to keep buffer fresh (prevent lag)
                ret, frame = self.cap.read()
                
                if not ret:
                    self.error = "Failed to read frame"
                    time.sleep(0.1)
                    continue
                
                # Only save at specified interval
                if current_time - last_capture >= self.config.frame_capture_interval:
                    self._save_frame(frame)
                    self.frames_captured += 1
                    self.last_capture_time = datetime.now()
                    last_capture = current_time
                
                # Small sleep to prevent CPU spinning
                time.sleep(0.03)  # ~30fps read rate
                
        except Exception as e:
            self.error = str(e)
        finally:
            if self.cap:
                self.cap.release()
    
    def _save_frame(self, frame: np.ndarray):
        """Save frame to JPEG file."""
        # Write to temp file first, then rename (atomic operation)
        temp_path = self.output_path.with_suffix('.tmp')
        
        cv2.imwrite(str(temp_path), frame, [cv2.IMWRITE_JPEG_QUALITY, 95])
        
        # Atomic rename
        temp_path.replace(self.output_path)


# =============================================================================
# Live Ingest Controller
# =============================================================================
class LiveIngestController:
    """
    Main controller for live audio/video ingestion.
    Manages both capture threads and provides status monitoring.
    """
    
    def __init__(self, config: Optional[IngestConfig] = None):
        self.config = config or IngestConfig()
        self.output_dir = Path(self.config.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.audio_capture = AudioCapture(self.config, self.output_dir)
        self.video_capture = VideoCapture(self.config, self.output_dir)
        
        self.start_time: Optional[datetime] = None
        self.is_running = False
        
    def start(self):
        """Start both audio and video capture."""
        console.print(Panel.fit(
            "[bold cyan]🎬 Live Ingest Starting[/bold cyan]\n"
            f"[dim]Audio: {self.config.audio_chunk_duration}s chunks @ {self.config.audio_sample_rate}Hz[/dim]\n"
            f"[dim]Video: Frame every {self.config.frame_capture_interval}s[/dim]",
            border_style="cyan"
        ))
        
        self.start_time = datetime.now()
        self.is_running = True
        
        # Start capture threads
        self.audio_capture.start()
        self.video_capture.start()
        
        console.print("\n[green]✓ Audio capture started[/green]")
        console.print("[green]✓ Video capture started[/green]")
        console.print(f"\n[dim]Output directory: {self.output_dir.absolute()}[/dim]")
        console.print(f"[dim]Audio file: {self.config.audio_output}[/dim]")
        console.print(f"[dim]Frame file: {self.config.frame_output}[/dim]\n")
        
    def stop(self):
        """Stop all capture."""
        self.is_running = False
        self.audio_capture.stop()
        self.video_capture.stop()
        console.print("\n[yellow]⏹ Live ingest stopped[/yellow]")
        
    def get_status_table(self) -> Table:
        """Generate status table for live display."""
        table = Table(title="Live Ingest Status", show_header=True)
        table.add_column("Stream", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Captured", justify="right")
        table.add_column("Last Update", style="dim")
        
        # Audio status
        audio_status = "🔴 Recording" if self.audio_capture.is_running else "⏹ Stopped"
        if self.audio_capture.error:
            audio_status = f"❌ {self.audio_capture.error}"
        audio_last = (
            self.audio_capture.last_capture_time.strftime("%H:%M:%S")
            if self.audio_capture.last_capture_time else "—"
        )
        table.add_row(
            "🎤 Audio",
            audio_status,
            f"{self.audio_capture.chunks_captured} chunks",
            audio_last
        )
        
        # Video status
        video_status = "📹 Active" if self.video_capture.is_running else "⏹ Stopped"
        if self.video_capture.error:
            video_status = f"❌ {self.video_capture.error}"
        video_last = (
            self.video_capture.last_capture_time.strftime("%H:%M:%S")
            if self.video_capture.last_capture_time else "—"
        )
        table.add_row(
            "📷 Video",
            video_status,
            f"{self.video_capture.frames_captured} frames",
            video_last
        )
        
        # Runtime
        if self.start_time:
            runtime = datetime.now() - self.start_time
            hours, remainder = divmod(int(runtime.total_seconds()), 3600)
            minutes, seconds = divmod(remainder, 60)
            table.add_row(
                "⏱ Runtime",
                f"{hours:02d}:{minutes:02d}:{seconds:02d}",
                "",
                ""
            )
        
        return table
    
    def run_with_live_display(self):
        """Run with live status display in terminal."""
        self.start()
        
        console.print("[dim]Press Ctrl+C to stop[/dim]\n")
        
        try:
            with Live(self.get_status_table(), refresh_per_second=1, console=console) as live:
                while self.is_running:
                    live.update(self.get_status_table())
                    time.sleep(0.5)
                    
                    # Check max runtime
                    if self.config.max_runtime:
                        runtime = (datetime.now() - self.start_time).total_seconds()
                        if runtime >= self.config.max_runtime:
                            console.print(f"\n[yellow]Max runtime ({self.config.max_runtime}s) reached[/yellow]")
                            break
                            
        except KeyboardInterrupt:
            console.print("\n[yellow]Interrupted by user[/yellow]")
        finally:
            self.stop()


# =============================================================================
# Callback-based API for integration
# =============================================================================
class LiveIngestWithCallbacks(LiveIngestController):
    """
    Extended controller with callbacks for AI model integration.
    
    Usage:
        def on_audio(path):
            # Process new audio chunk
            transcript = whisper_model.transcribe(path)
            
        def on_frame(path):
            # Process new frame
            analysis = vlm_model.analyze(path)
            
        ingest = LiveIngestWithCallbacks(
            on_audio_ready=on_audio,
            on_frame_ready=on_frame
        )
        ingest.run_with_live_display()
    """
    
    def __init__(
        self,
        config: Optional[IngestConfig] = None,
        on_audio_ready: Optional[Callable[[Path], None]] = None,
        on_frame_ready: Optional[Callable[[Path], None]] = None
    ):
        super().__init__(config)
        self.on_audio_ready = on_audio_ready
        self.on_frame_ready = on_frame_ready
        
        # Override captures with callback versions
        self.audio_capture = AudioCaptureWithCallback(
            self.config, self.output_dir, on_audio_ready
        )
        self.video_capture = VideoCaptureWithCallback(
            self.config, self.output_dir, on_frame_ready
        )


class AudioCaptureWithCallback(AudioCapture):
    """Audio capture with callback on each chunk."""
    
    def __init__(self, config, output_dir, callback):
        super().__init__(config, output_dir)
        self.callback = callback
        
    def _save_wav(self, frames):
        super()._save_wav(frames)
        if self.callback:
            try:
                self.callback(self.output_path)
            except Exception as e:
                self.error = f"Callback error: {e}"


class VideoCaptureWithCallback(VideoCapture):
    """Video capture with callback on each frame."""
    
    def __init__(self, config, output_dir, callback):
        super().__init__(config, output_dir)
        self.callback = callback
        
    def _save_frame(self, frame):
        super()._save_frame(frame)
        if self.callback:
            try:
                self.callback(self.output_path)
            except Exception as e:
                self.error = f"Callback error: {e}"


# =============================================================================
# CLI Entry Point
# =============================================================================
def main():
    """Main entry point for live ingest."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Live Audio/Video Ingest for Classroom Summarizer"
    )
    parser.add_argument(
        "--audio-duration", "-a",
        type=float,
        default=10.0,
        help="Audio chunk duration in seconds (default: 10)"
    )
    parser.add_argument(
        "--frame-interval", "-f",
        type=float,
        default=30.0,
        help="Frame capture interval in seconds (default: 30)"
    )
    parser.add_argument(
        "--camera", "-c",
        type=int,
        default=0,
        help="Camera index (default: 0)"
    )
    parser.add_argument(
        "--output-dir", "-o",
        type=str,
        default="data/live",
        help="Output directory (default: data/live)"
    )
    parser.add_argument(
        "--max-runtime", "-t",
        type=float,
        default=None,
        help="Maximum runtime in seconds (default: unlimited)"
    )
    
    args = parser.parse_args()
    
    config = IngestConfig(
        audio_chunk_duration=args.audio_duration,
        frame_capture_interval=args.frame_interval,
        camera_index=args.camera,
        output_dir=args.output_dir,
        max_runtime=args.max_runtime
    )
    
    controller = LiveIngestController(config)
    controller.run_with_live_display()


if __name__ == "__main__":
    main()
