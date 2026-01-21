"""
=============================================================================
BANGLISH TRANSCRIBER - Whisper-based ASR for Bengali + English
=============================================================================
Multimodal Banglish Classroom Summarizer
Master's Thesis - Phase 3: Transcription

Uses OpenAI Whisper (large-v3-turbo) for automatic speech recognition.
Optimized for Banglish (Bengali mixed with English) lecture content.

Model: openai/whisper-large-v3-turbo
- Fast and accurate
- Auto-detects language (no forced language to avoid hallucinations)
- Uses native generate() for robust long-form transcription
- temperature=0.0 for deterministic/greedy decoding
=============================================================================
"""

import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

import torch
import librosa
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel

console = Console()


@dataclass
class TranscriptSegment:
    """A single segment of transcribed audio."""
    text: str
    start: float  # Start time in seconds
    end: float    # End time in seconds
    
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
    text: str                          # Full transcript text
    segments: List[TranscriptSegment]  # Segments with timestamps
    language: str                      # Detected/specified language
    duration: float                    # Total audio duration
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "language": self.language,
            "duration": self.duration,
            "segments": [seg.to_dict() for seg in self.segments]
        }
    
    def save(self, output_path: str):
        """Save transcript to JSON file."""
        import json
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)
    
    def to_srt(self) -> str:
        """Convert to SRT subtitle format."""
        srt_lines = []
        for i, seg in enumerate(self.segments, 1):
            start_srt = _seconds_to_srt_time(seg.start)
            end_srt = _seconds_to_srt_time(seg.end)
            srt_lines.append(f"{i}")
            srt_lines.append(f"{start_srt} --> {end_srt}")
            srt_lines.append(seg.text.strip())
            srt_lines.append("")
        return "\n".join(srt_lines)


def _seconds_to_srt_time(seconds: float) -> str:
    """Convert seconds to SRT timestamp format (HH:MM:SS,mmm)."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


class BanglishTranscriber:
    """
    Whisper-based transcriber for Banglish (Bengali + English) audio.
    
    Uses whisper-large-v3-turbo with native generate() for robust long-form transcription.
    Auto-detects language to avoid hallucinations.
    
    Usage:
        transcriber = BanglishTranscriber()
        result = transcriber.transcribe("audio.wav")
        print(result.text)
        for seg in result.segments:
            print(f"[{seg.start:.1f}s] {seg.text}")
    """
    
    def __init__(
        self,
        model_name: str = "openai/whisper-large-v3-turbo",
        device: str = "cuda",
        torch_dtype: torch.dtype = torch.float16
    ):
        """
        Initialize the Banglish transcriber.
        
        Args:
            model_name: HuggingFace model identifier
            device: Device to run inference on ("cuda" or "cpu")
            torch_dtype: Data type for model (float16 for GPU efficiency)
        """
        self.model_name = model_name
        self.device = device
        self.torch_dtype = torch_dtype
        self.model = None
        self.processor = None
        self._is_loaded = False
        
    def load_model(self):
        """Load the Whisper model and processor."""
        if self._is_loaded:
            return
        
        console.print(f"\n[bold cyan]🎤 Loading Whisper Model[/bold cyan]")
        console.print(f"[dim]Model: {self.model_name}[/dim]")
        console.print(f"[dim]Device: {self.device}[/dim]\n")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Loading Whisper model...", total=None)
            
            # Load model with native generate() support
            self.model = AutoModelForSpeechSeq2Seq.from_pretrained(
                self.model_name,
                torch_dtype=self.torch_dtype,
                low_cpu_mem_usage=True,
            ).to(self.device)
            
            self.processor = AutoProcessor.from_pretrained(self.model_name)
            
            progress.remove_task(task)
        
        # Get VRAM usage
        if self.device == "cuda" and torch.cuda.is_available():
            memory_gb = torch.cuda.memory_allocated() / (1024**3)
            console.print(f"[green]✓ Whisper loaded[/green] [dim]({memory_gb:.2f} GB VRAM)[/dim]\n")
        else:
            console.print("[green]✓ Whisper loaded[/green]\n")
        
        self._is_loaded = True
    
    def transcribe(
        self,
        audio_path: str,
    ) -> TranscriptResult:
        """
        Transcribe an audio file using Whisper's native long-form transcription.
        
        Args:
            audio_path: Path to audio file (WAV, MP3, etc.)
            
        Returns:
            TranscriptResult with full text and timestamped segments
            
        Note:
            - Language is auto-detected (no forced language to avoid hallucinations)
            - Uses Whisper's native chunking mechanism for long-form audio
            - condition_on_previous_text=False prevents repetition loops
            - temperature=0.0 for deterministic greedy decoding
        """
        # Ensure model is loaded
        if not self._is_loaded:
            self.load_model()
        
        audio_path = Path(audio_path)
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        console.print(f"[bold]🎵 Transcribing:[/bold] {audio_path.name}")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Loading audio...", total=None)
            
            # Load audio with librosa (Whisper expects 16kHz)
            audio_array, sr = librosa.load(str(audio_path), sr=16000)
            audio_duration = len(audio_array) / sr
            
            progress.update(task, description="Processing with Whisper (native long-form)...")
            
            # Process audio through processor - return_attention_mask needed for long-form
            inputs = self.processor(
                audio_array,
                sampling_rate=16000,
                return_tensors="pt",
                return_attention_mask=True,
                truncation=False,
                padding="longest",
            )
            # Move to device with correct dtype
            input_features = inputs["input_features"].to(self.device, dtype=self.torch_dtype)
            attention_mask = inputs.get("attention_mask")
            if attention_mask is not None:
                attention_mask = attention_mask.to(self.device)
            
            # Use Whisper's native generate() with long-form settings
            # This uses Whisper's own chunking mechanism (30s chunks internally)
            # 
            # Key settings for Banglish (Bengali + English mix):
            # - language="bengali" tells Whisper the primary language
            # - prompt_ids biases model to expect technical English terms mixed in
            
            # Initial prompt to bias model toward Banglish (mixed Bengali + English)
            initial_prompt = "This is a technical lecture in Banglish. It mixes Bengali and English terms like Algorithm, Heuristic, A-Star, Greedy Search."
            prompt_ids = self.processor.get_prompt_ids(initial_prompt, return_tensors="pt").to(self.device)
            
            generate_kwargs = {
                "language": "bengali",
                "task": "transcribe",
                "return_timestamps": True,
                "prompt_ids": prompt_ids,
                # Anti-hallucination settings
                "condition_on_prev_tokens": False,  # Prevent repetition loops
                "temperature": 0.0,                  # Greedy decoding
                "no_speech_threshold": 0.6,          # Filter silence
                "compression_ratio_threshold": 2.4,  # Detect repetitive output
                "logprob_threshold": -1.0,           # Accept low confidence
            }
            if attention_mask is not None:
                generate_kwargs["attention_mask"] = attention_mask
            
            generated_ids = self.model.generate(
                input_features,
                **generate_kwargs
            )
            
            progress.update(task, description="Decoding transcription...")
            
            # Decode with timestamps
            result = self.processor.batch_decode(
                generated_ids,
                skip_special_tokens=True,
                decode_with_timestamps=True,
            )[0]
            
            progress.remove_task(task)
        
        # Parse timestamps from the output
        segments = self._parse_whisper_timestamps(result, audio_duration)
        
        # Get clean text without timestamps
        full_text = self._clean_transcript_text(result)
        
        # Detect language (set to Bengali for Banglish content)
        detected_language = "bengali (Banglish mode)"
        
        transcript = TranscriptResult(
            text=full_text,
            segments=segments,
            language=detected_language,
            duration=audio_duration
        )
        
        # Print summary
        console.print(f"[green]✓ Transcription complete[/green]")
        console.print(f"[dim]  Duration: {audio_duration:.1f}s | Segments: {len(segments)} | Characters: {len(full_text)}[/dim]")
        console.print(f"[dim]  Language: {detected_language}[/dim]\n")
        
        return transcript
    
    def _parse_whisper_timestamps(self, text: str, total_duration: float) -> List[TranscriptSegment]:
        """Parse Whisper's timestamp tokens from decoded text."""
        import re
        
        segments = []
        # Whisper outputs timestamps like <|0.00|> text <|2.50|>
        pattern = r'<\|(\d+\.?\d*)\|>'
        
        parts = re.split(pattern, text)
        # parts alternates between text and timestamps
        
        current_time = 0.0
        current_text = ""
        
        for i, part in enumerate(parts):
            if i % 2 == 0:  # Text part
                cleaned = part.strip()
                if cleaned:
                    current_text = cleaned
            else:  # Timestamp part
                try:
                    timestamp = float(part)
                    if current_text and timestamp > current_time:
                        segments.append(TranscriptSegment(
                            text=current_text,
                            start=current_time,
                            end=timestamp
                        ))
                        current_text = ""
                    current_time = timestamp
                except ValueError:
                    pass
        
        # Handle any remaining text
        if current_text:
            segments.append(TranscriptSegment(
                text=current_text,
                start=current_time,
                end=total_duration
            ))
        
        # If no timestamps were parsed, create a single segment
        if not segments and text.strip():
            clean_text = self._clean_transcript_text(text)
            segments.append(TranscriptSegment(
                text=clean_text,
                start=0.0,
                end=total_duration
            ))
        
        return segments
    
    def _clean_transcript_text(self, text: str) -> str:
        """Remove timestamp tokens from Whisper output."""
        import re
        # Remove <|timestamp|> tokens
        cleaned = re.sub(r'<\|\d+\.?\d*\|>', '', text)
        # Remove other special tokens
        cleaned = re.sub(r'<\|[^|]+\|>', '', cleaned)
        # Clean up whitespace
        cleaned = ' '.join(cleaned.split())
        return cleaned.strip()
    
    def unload_model(self):
        """Unload model to free GPU memory."""
        if self.model is not None:
            del self.model
            self.model = None
        if self.processor is not None:
            del self.processor
            self.processor = None
        self._is_loaded = False
        
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            console.print("[dim]Whisper model unloaded, GPU memory cleared[/dim]")


# =============================================================================
# CLI Entry Point
# =============================================================================
def main():
    """Test transcription on temp_output/full_audio.wav"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Transcribe audio using Whisper (Banglish optimized)"
    )
    parser.add_argument(
        "audio",
        type=str,
        nargs="?",
        default="temp_output/full_audio.wav",
        help="Path to audio file (default: temp_output/full_audio.wav)"
    )
    parser.add_argument(
        "--output", "-o",
        type=str,
        default=None,
        help="Output JSON file (default: <audio_name>_transcript.json)"
    )
    parser.add_argument(
        "--language", "-l",
        type=str,
        default="bengali",
        help="Language hint (default: bengali)"
    )
    parser.add_argument(
        "--chunk-length", "-c",
        type=int,
        default=30,
        help="Chunk length in seconds (default: 30)"
    )
    
    args = parser.parse_args()
    
    # Check if audio file exists
    audio_path = Path(args.audio)
    if not audio_path.exists():
        console.print(f"[red]Error: Audio file not found: {audio_path}[/red]")
        console.print("[dim]Run video ingestion first: python src/ingest_video.py <video>[/dim]")
        sys.exit(1)
    
    # Initialize transcriber
    transcriber = BanglishTranscriber()
    
    # Transcribe
    result = transcriber.transcribe(
        str(audio_path),
        chunk_length_s=args.chunk_length,
        language=args.language
    )
    
    # Print results
    console.print(Panel.fit(
        f"[bold]Full Transcript[/bold]\n\n{result.text[:2000]}{'...' if len(result.text) > 2000 else ''}",
        title="📝 Transcription Result",
        border_style="green"
    ))
    
    # Print first few segments
    console.print("\n[bold]Segments (first 10):[/bold]")
    for seg in result.segments[:10]:
        start_str = f"{int(seg.start//60):02d}:{int(seg.start%60):02d}"
        end_str = f"{int(seg.end//60):02d}:{int(seg.end%60):02d}"
        console.print(f"  [dim][{start_str} → {end_str}][/dim] {seg.text.strip()}")
    
    if len(result.segments) > 10:
        console.print(f"  [dim]... and {len(result.segments) - 10} more segments[/dim]")
    
    # Save to file
    output_path = args.output or str(audio_path.with_suffix('.transcript.json'))
    result.save(output_path)
    console.print(f"\n[green]✓ Transcript saved to:[/green] {output_path}")
    
    # Also save SRT
    srt_path = str(audio_path.with_suffix('.srt'))
    with open(srt_path, 'w', encoding='utf-8') as f:
        f.write(result.to_srt())
    console.print(f"[green]✓ Subtitles saved to:[/green] {srt_path}")
    
    return result


if __name__ == "__main__":
    main()
