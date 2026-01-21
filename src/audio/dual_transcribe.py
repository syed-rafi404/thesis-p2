"""
=============================================================================
DUAL-STREAM TRANSCRIPTION - English + Bengali Passes
=============================================================================
Runs Whisper twice with different language settings to capture both
English and Bengali content in Banglish lectures.

Stream 1: English mode - captures English portions accurately
Stream 2: Bengali mode - captures Bengali portions with Bengali prompt
=============================================================================
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import torch
import librosa
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor
from rich.console import Console
from rich.panel import Panel

from src.audio.transcriber import TranscriptResult, TranscriptSegment

console = Console()


class DualStreamTranscriber:
    """
    Dual-stream transcriber for Banglish content.
    
    Runs Whisper twice:
    - English pass: Captures English content accurately
    - Bengali pass: Captures Bengali content with Bengali prompt
    """
    
    def __init__(
        self,
        model_name: str = "openai/whisper-large-v3-turbo",
        device: str = "cuda",
        torch_dtype: torch.dtype = torch.float16
    ):
        self.model_name = model_name
        self.device = device
        self.torch_dtype = torch_dtype
        self.model = None
        self.processor = None
        self._is_loaded = False
    
    def load_model(self):
        """Load Whisper model once for both passes."""
        if self._is_loaded:
            return
        
        console.print(f"\n[bold cyan]🎤 Loading Whisper Model[/bold cyan]")
        console.print(f"[dim]Model: {self.model_name}[/dim]")
        console.print(f"[dim]Device: {self.device}[/dim]\n")
        
        self.model = AutoModelForSpeechSeq2Seq.from_pretrained(
            self.model_name,
            torch_dtype=self.torch_dtype,
            low_cpu_mem_usage=True,
        ).to(self.device)
        
        self.processor = AutoProcessor.from_pretrained(self.model_name)
        
        if self.device == "cuda" and torch.cuda.is_available():
            memory_gb = torch.cuda.memory_allocated() / (1024**3)
            console.print(f"[green]✓ Whisper loaded[/green] [dim]({memory_gb:.2f} GB VRAM)[/dim]\n")
        
        self._is_loaded = True
    
    def _transcribe_single(
        self,
        audio_array,
        audio_duration: float,
        language: str,
        initial_prompt: str = None
    ) -> TranscriptResult:
        """Run a single transcription pass."""
        
        # Process audio
        inputs = self.processor(
            audio_array,
            sampling_rate=16000,
            return_tensors="pt",
            return_attention_mask=True,
            truncation=False,
            padding="longest",
        )
        input_features = inputs["input_features"].to(self.device, dtype=self.torch_dtype)
        attention_mask = inputs.get("attention_mask")
        if attention_mask is not None:
            attention_mask = attention_mask.to(self.device)
        
        # Build generate kwargs
        generate_kwargs = {
            "language": language,
            "task": "transcribe",
            "return_timestamps": True,
            "condition_on_prev_tokens": False,
            "temperature": 0.0,
            "no_speech_threshold": 0.6,
            "compression_ratio_threshold": 2.4,
            "logprob_threshold": -1.0,
        }
        
        # Add prompt if provided
        if initial_prompt:
            prompt_ids = self.processor.get_prompt_ids(initial_prompt, return_tensors="pt").to(self.device)
            generate_kwargs["prompt_ids"] = prompt_ids
        
        if attention_mask is not None:
            generate_kwargs["attention_mask"] = attention_mask
        
        # Generate
        generated_ids = self.model.generate(input_features, **generate_kwargs)
        
        # Decode
        result = self.processor.batch_decode(
            generated_ids,
            skip_special_tokens=True,
            decode_with_timestamps=True,
        )[0]
        
        # Parse
        segments = self._parse_timestamps(result, audio_duration)
        full_text = self._clean_text(result)
        
        return TranscriptResult(
            text=full_text,
            segments=segments,
            language=language,
            duration=audio_duration
        )
    
    def _parse_timestamps(self, text: str, total_duration: float):
        """Parse Whisper timestamp tokens."""
        import re
        segments = []
        pattern = r'<\|(\d+\.?\d*)\|>'
        parts = re.split(pattern, text)
        
        current_time = 0.0
        current_text = ""
        
        for i, part in enumerate(parts):
            if i % 2 == 0:
                cleaned = part.strip()
                if cleaned:
                    current_text = cleaned
            else:
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
        
        if current_text:
            segments.append(TranscriptSegment(
                text=current_text,
                start=current_time,
                end=total_duration
            ))
        
        if not segments and text.strip():
            clean_text = self._clean_text(text)
            segments.append(TranscriptSegment(
                text=clean_text,
                start=0.0,
                end=total_duration
            ))
        
        return segments
    
    def _clean_text(self, text: str) -> str:
        """Remove timestamp tokens."""
        import re
        cleaned = re.sub(r'<\|\d+\.?\d*\|>', '', text)
        cleaned = re.sub(r'<\|[^|]+\|>', '', cleaned)
        cleaned = ' '.join(cleaned.split())
        return cleaned.strip()
    
    def transcribe_dual(
        self,
        audio_path: str,
        output_dir: str = "temp_output"
    ) -> tuple:
        """
        Run dual-stream transcription.
        
        Returns:
            Tuple of (english_result, bengali_result)
        """
        self.load_model()
        
        audio_path = Path(audio_path)
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Load audio once
        console.print(f"[bold]🎵 Loading audio:[/bold] {audio_path.name}")
        audio_array, sr = librosa.load(str(audio_path), sr=16000)
        audio_duration = len(audio_array) / sr
        console.print(f"[dim]  Duration: {audio_duration:.1f}s[/dim]\n")
        
        # ===== STREAM 1: ENGLISH =====
        console.print(Panel.fit(
            "[bold white]STREAM 1: ENGLISH[/bold white]",
            border_style="blue"
        ))
        
        english_prompt = "This is a technical lecture mixing English and Bengali. Terms like Algorithm, Heuristic, A-Star, Greedy Search are used."
        
        result_en = self._transcribe_single(
            audio_array,
            audio_duration,
            language="english",
            initial_prompt=english_prompt
        )
        
        en_path = output_dir / "transcript_en.json"
        result_en.save(str(en_path))
        console.print(f"[green]✓ English transcript saved:[/green] {en_path}")
        console.print(f"[dim]  Characters: {len(result_en.text)} | Segments: {len(result_en.segments)}[/dim]\n")
        
        # ===== STREAM 2: BENGALI =====
        console.print(Panel.fit(
            "[bold white]STREAM 2: BENGALI[/bold white]",
            border_style="green"
        ))
        
        # Bengali script prompt
        bengali_prompt = "এটি একটি টেকনিক্যাল লেকচার। এখানে Greedy Search, A-Star এর মতো ইংরেজি শব্দ ব্যবহার করা হয়েছে।"
        
        result_bn = self._transcribe_single(
            audio_array,
            audio_duration,
            language="bengali",
            initial_prompt=bengali_prompt
        )
        
        bn_path = output_dir / "transcript_bn.json"
        result_bn.save(str(bn_path))
        console.print(f"[green]✓ Bengali transcript saved:[/green] {bn_path}")
        console.print(f"[dim]  Characters: {len(result_bn.text)} | Segments: {len(result_bn.segments)}[/dim]\n")
        
        # Summary
        console.print(Panel.fit(
            f"[bold green]✓ Dual-Stream Transcription Complete[/bold green]\n\n"
            f"[white]English:[/white] {en_path}\n"
            f"[white]Bengali:[/white] {bn_path}",
            title="Summary",
            border_style="cyan"
        ))
        
        return result_en, result_bn
    
    def unload_model(self):
        """Free GPU memory."""
        if self.model is not None:
            del self.model
            self.model = None
        if self.processor is not None:
            del self.processor
            self.processor = None
        self._is_loaded = False
        
        if torch.cuda.is_available():
            torch.cuda.empty_cache()


# =============================================================================
# CLI
# =============================================================================
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Dual-stream Banglish transcription")
    parser.add_argument("audio_path", help="Path to audio file")
    parser.add_argument("--output-dir", default="temp_output", help="Output directory")
    
    args = parser.parse_args()
    
    transcriber = DualStreamTranscriber()
    result_en, result_bn = transcriber.transcribe_dual(args.audio_path, args.output_dir)
    
    print("\n" + "="*60)
    print("ENGLISH TRANSCRIPT:")
    print("="*60)
    print(result_en.text[:1000] + "..." if len(result_en.text) > 1000 else result_en.text)
    
    print("\n" + "="*60)
    print("BENGALI TRANSCRIPT:")
    print("="*60)
    print(result_bn.text[:1000] + "..." if len(result_bn.text) > 1000 else result_bn.text)
