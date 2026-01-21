"""
=============================================================================
SPECIALIZED BANGLA TRANSCRIBER - BanglaASR Model
=============================================================================
Tests the bangla-speech-processing/BanglaASR model for Bengali speech.

This model is specifically trained for Bangla/Bengali speech recognition
and may capture Bengali words better than multilingual Whisper.
=============================================================================
"""

import sys
import json
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Any

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import torch
from transformers import pipeline
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


@dataclass
class TranscriptSegment:
    """A single segment of transcribed audio."""
    text: str
    start: float
    end: float
    
    @property
    def duration(self) -> float:
        return self.end - self.start
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "start": self.start,
            "end": self.end,
            "duration": self.duration
        }


@dataclass
class TranscriptResult:
    """Complete transcription result."""
    text: str
    segments: List[TranscriptSegment]
    language: str
    duration: float
    model: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "language": self.language,
            "duration": self.duration,
            "model": self.model,
            "segments": [seg.to_dict() for seg in self.segments]
        }
    
    def save(self, output_path: str):
        """Save transcript to JSON file."""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)


class BanglaASRTranscriber:
    """
    Specialized Bangla ASR transcriber using bangla-speech-processing/BanglaASR.
    
    This model is specifically trained for Bengali speech recognition.
    """
    
    def __init__(
        self,
        model_name: str = "bangla-speech-processing/BanglaASR",
        device: str = "cuda"
    ):
        self.model_name = model_name
        self.device = device
        self.pipe = None
        self._is_loaded = False
    
    def load_model(self):
        """Load the BanglaASR model pipeline."""
        if self._is_loaded:
            return
        
        console.print(f"\n[bold cyan]🎤 Loading Specialized Bangla ASR Model[/bold cyan]")
        console.print(f"[dim]Model: {self.model_name}[/dim]")
        console.print(f"[dim]Device: {self.device}[/dim]\n")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Loading BanglaASR pipeline...", total=None)
            
            try:
                self.pipe = pipeline(
                    "automatic-speech-recognition",
                    model=self.model_name,
                    device=self.device,
                )
                progress.remove_task(task)
                
                # Get VRAM usage
                if self.device == "cuda" and torch.cuda.is_available():
                    memory_gb = torch.cuda.memory_allocated() / (1024**3)
                    console.print(f"[green]✓ BanglaASR loaded[/green] [dim]({memory_gb:.2f} GB VRAM)[/dim]\n")
                else:
                    console.print("[green]✓ BanglaASR loaded[/green]\n")
                
                self._is_loaded = True
                
            except Exception as e:
                progress.remove_task(task)
                console.print(f"[red]✗ Failed to load model: {e}[/red]")
                raise
    
    def transcribe(self, audio_path: str) -> TranscriptResult:
        """
        Transcribe an audio file using BanglaASR.
        
        Args:
            audio_path: Path to audio file (WAV, MP3, etc.)
            
        Returns:
            TranscriptResult with transcription
        """
        if not self._is_loaded:
            self.load_model()
        
        audio_path = Path(audio_path)
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        console.print(f"[bold]🎵 Transcribing with BanglaASR:[/bold] {audio_path.name}")
        
        # Get audio duration
        import librosa
        audio_array, sr = librosa.load(str(audio_path), sr=16000)
        audio_duration = len(audio_array) / sr
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Processing audio with BanglaASR...", total=None)
            
            try:
                # Run the pipeline
                result = self.pipe(
                    str(audio_path),
                    return_timestamps=True,
                    chunk_length_s=30,
                )
                
                progress.remove_task(task)
                
            except Exception as e:
                progress.remove_task(task)
                console.print(f"[yellow]⚠ Timestamps not supported, trying without...[/yellow]")
                
                # Try without timestamps
                result = self.pipe(str(audio_path))
        
        # Parse results
        if isinstance(result, dict):
            full_text = result.get("text", "")
            chunks = result.get("chunks", [])
        else:
            full_text = str(result)
            chunks = []
        
        # Convert chunks to segments
        segments = []
        if chunks:
            for chunk in chunks:
                timestamp = chunk.get("timestamp", (0, 0))
                start = timestamp[0] if timestamp[0] is not None else 0
                end = timestamp[1] if timestamp[1] is not None else start
                
                segment = TranscriptSegment(
                    text=chunk.get("text", ""),
                    start=start,
                    end=end
                )
                segments.append(segment)
        else:
            # Single segment for entire audio
            segments.append(TranscriptSegment(
                text=full_text,
                start=0.0,
                end=audio_duration
            ))
        
        transcript = TranscriptResult(
            text=full_text,
            segments=segments,
            language="bengali",
            duration=audio_duration,
            model=self.model_name
        )
        
        # Print summary
        console.print(f"[green]✓ Transcription complete[/green]")
        console.print(f"[dim]  Duration: {audio_duration:.1f}s | Segments: {len(segments)} | Characters: {len(full_text)}[/dim]\n")
        
        return transcript
    
    def unload_model(self):
        """Unload model to free GPU memory."""
        if self.pipe is not None:
            del self.pipe
            self.pipe = None
        self._is_loaded = False
        
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            console.print("[dim]BanglaASR model unloaded, GPU memory cleared[/dim]")


# =============================================================================
# CLI
# =============================================================================
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Specialized Bangla ASR transcription")
    parser.add_argument("audio_path", help="Path to audio file")
    parser.add_argument("--output", "-o", default="temp_output/transcript_specialized.json",
                        help="Output JSON path")
    
    args = parser.parse_args()
    
    # Run transcription
    transcriber = BanglaASRTranscriber()
    result = transcriber.transcribe(args.audio_path)
    
    # Save output
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    result.save(str(output_path))
    
    console.print(f"[bold green]✓ Saved to:[/bold green] {output_path}\n")
    
    # Print transcript
    print("=" * 60)
    print("BANGLA ASR TRANSCRIPT:")
    print("=" * 60)
    print(result.text)
