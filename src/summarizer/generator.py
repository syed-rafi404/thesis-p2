"""
=============================================================================
LECTURE NOTE GENERATOR - Final Summarization Module
=============================================================================
Multimodal Banglish Classroom Summarizer
Master's Thesis - Phase 5: Final Summarization

Merges noisy audio transcripts with clean visual context from VLM
to generate accurate, structured lecture notes.

Model: Qwen/Qwen2.5-7B-Instruct (FP16)
Strategy: Use visual text to correct technical terms from audio
=============================================================================
"""

import sys
import json
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel

# ModelRegistry for GPU model caching (optimized batch/live processing)
try:
    from src.model_registry import ModelRegistry
    REGISTRY_AVAILABLE = True
except ImportError:
    REGISTRY_AVAILABLE = False

console = Console()


@dataclass
class MultimodalContext:
    """Combined context from all modalities."""
    english_transcript: str
    bengali_transcript: str
    visual_content: str
    frames_summary: str
    
    def to_prompt_context(self) -> str:
        """Format context for LLM prompt."""
        return f"""## AUDIO TRANSCRIPT (English Pass)
{self.english_transcript}

## AUDIO TRANSCRIPT (Bengali Pass)  
{self.bengali_transcript}

## VISUAL CONTENT (From Whiteboard)
{self.visual_content}

## FRAME-BY-FRAME VISUAL SUMMARY
{self.frames_summary}"""


class LectureNoteGenerator:
    """
    Generates structured lecture notes by merging multimodal inputs.
    
    Uses Qwen2.5-7B-Instruct to intelligently combine:
    - Noisy audio transcripts (English + Bengali passes)
    - Clean visual text from whiteboard (VLM extracted)
    
    The visual text helps correct technical terms that may be
    misheard in the audio (e.g., "A-Store" -> "A*").
    """
    
    def __init__(
        self,
        model_name: str = "Qwen/Qwen2.5-14B-Instruct",
        torch_dtype: torch.dtype = torch.float16,
        device_map: str = "auto",
        use_4bit: bool = False  # Enable 4-bit quantization for live mode
    ):
        self.model_name = model_name
        self.torch_dtype = torch_dtype
        self.device_map = device_map
        self.use_4bit = use_4bit
        self.model = None
        self.tokenizer = None
        self._is_loaded = False
    
    def load_model(self, use_registry: bool = True):
        """Load the Qwen2.5 model.
        
        Args:
            use_registry: If True, use ModelRegistry singleton (recommended for batch/live)
        """
        if self._is_loaded:
            return
        
        precision_str = "4-bit quantized" if self.use_4bit else "FP16"
        
        # Use ModelRegistry for shared model access (faster batch processing)
        if use_registry and REGISTRY_AVAILABLE:
            console.print(f"\n[bold cyan]🧠 Loading Language Model (via Registry)[/bold cyan]")
            console.print(f"[dim]Model: {self.model_name}[/dim]")
            console.print(f"[dim]Precision: {precision_str} | Device Map: {self.device_map}[/dim]\n")
            
            registry = ModelRegistry.get_instance()
            self.model, self.tokenizer = registry.get_llm(
                model_name=self.model_name,
                torch_dtype=self.torch_dtype,
                device_map=self.device_map,
                use_4bit=self.use_4bit
            )
            self._is_loaded = True
            self._using_registry = True
            return
        
        # Direct loading (legacy behavior)
        self._using_registry = False
        console.print(f"\n[bold cyan]🧠 Loading Language Model[/bold cyan]")
        console.print(f"[dim]Model: {self.model_name}[/dim]")
        console.print(f"[dim]Precision: {precision_str} | Device Map: {self.device_map}[/dim]\n")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Loading Qwen2.5 model...", total=None)
            
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=self.torch_dtype,
                device_map=self.device_map,
            )
            
            progress.remove_task(task)
        
        # Get VRAM usage
        if torch.cuda.is_available():
            memory_gb = torch.cuda.memory_allocated() / (1024**3)
            console.print(f"[green]✓ Qwen2.5 loaded[/green] [dim]({memory_gb:.2f} GB VRAM)[/dim]\n")
        else:
            console.print("[green]✓ Qwen2.5 loaded[/green]\n")
        
        self._is_loaded = True
    
    def load_context_files(
        self,
        english_path: str = "temp_output/transcript_en.json",
        bengali_path: str = "temp_output/transcript_bn.json",
        vision_path: str = "temp_output/vision_context.json"
    ) -> MultimodalContext:
        """Load and parse all context files."""
        
        console.print("[bold]📂 Loading context files...[/bold]")
        
        # Load English transcript
        english_text = ""
        if Path(english_path).exists():
            with open(english_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                english_text = data.get("text", "")
            console.print(f"[dim]  ✓ English transcript: {len(english_text)} chars[/dim]")
        else:
            console.print(f"[yellow]  ⚠ English transcript not found: {english_path}[/yellow]")
        
        # Load Bengali transcript
        bengali_text = ""
        if Path(bengali_path).exists():
            with open(bengali_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                bengali_text = data.get("text", "")
            console.print(f"[dim]  ✓ Bengali transcript: {len(bengali_text)} chars[/dim]")
        else:
            console.print(f"[yellow]  ⚠ Bengali transcript not found: {bengali_path}[/yellow]")
        
        # Load vision context
        visual_content = ""
        frames_summary = ""
        if Path(vision_path).exists():
            with open(vision_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # Build visual content from frames
                frames = data.get("frames", [])
                visual_parts = []
                frame_summaries = []
                
                for frame in frames:
                    content = frame.get("content", "")
                    timestamp = frame.get("timestamp_sec", 0)
                    
                    if content and "no text" not in content.lower():
                        visual_parts.append(content)
                        frame_summaries.append(f"[{timestamp}s] {content[:100]}...")
                
                visual_content = "\n\n".join(visual_parts)
                frames_summary = "\n".join(frame_summaries)
                
            console.print(f"[dim]  ✓ Vision context: {len(frames)} frames, {len(visual_content)} chars[/dim]")
        else:
            console.print(f"[yellow]  ⚠ Vision context not found: {vision_path}[/yellow]")
        
        console.print()
        
        return MultimodalContext(
            english_transcript=english_text,
            bengali_transcript=bengali_text,
            visual_content=visual_content,
            frames_summary=frames_summary
        )
    
    def generate_notes(
        self,
        context: MultimodalContext,
        max_new_tokens: int = 2048,
        notes_language: str = "legacy",
        transcript: str = "",
        board_content: str = "",
        figures=None,
        topic_hint: str = "",
    ) -> str:
        """
        Generate structured lecture notes from multimodal context.

        Args:
            context: MultimodalContext with all input sources
            max_new_tokens: Maximum tokens to generate
            notes_language: "legacy" reproduces the original prompt exactly and is
                the default, because the board-recall baseline was produced with it.
                "english", "banglish" and "mixed" use the grounded prompts in
                src/summarizer/prompts.py.
            transcript, board_content, figures, topic_hint: inputs for the grounded
                prompts; ignored in legacy mode.

        Returns:
            Markdown formatted lecture notes
        """
        from src.summarizer.prompts import build_messages

        self.load_model()

        console.print(f"[bold]📝 Generating lecture notes ({notes_language})...[/bold]\n")

        messages = build_messages(
            notes_language,
            prompt_context=context.to_prompt_context(),
            transcript=transcript,
            board_content=board_content,
            figures=figures,
            topic_hint=topic_hint,
        )
        
        # Apply chat template
        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        
        inputs = self.tokenizer(text, return_tensors="pt").to(self.model.device)
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Generating notes with LLM...", total=None)
            
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=max_new_tokens,
                    do_sample=True,
                    temperature=0.7,
                    top_p=0.9,
                    pad_token_id=self.tokenizer.eos_token_id,
                )
            
            progress.remove_task(task)
        
        # Decode only the new tokens
        generated_ids = outputs[0][inputs.input_ids.shape[1]:]
        response = self.tokenizer.decode(generated_ids, skip_special_tokens=True)
        
        console.print("[green]✓ Lecture notes generated[/green]\n")
        
        return response.strip()
    
    def save_notes(self, notes: str, output_path: str = "final_lecture_notes.md"):
        """Save generated notes to file."""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(notes)
        
        console.print(f"[bold green]✓ Saved to:[/bold green] {output_path}\n")
        return output_path
    
    def unload_model(self):
        """Unload model to free GPU memory.
        
        Note: If using ModelRegistry, this is a no-op (registry manages lifecycle).
        """
        if getattr(self, '_using_registry', False):
            console.print("[dim]LLM model managed by registry (not unloading)[/dim]")
            return
            
        if self.model is not None:
            del self.model
            self.model = None
        if self.tokenizer is not None:
            del self.tokenizer
            self.tokenizer = None
        self._is_loaded = False
        
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            console.print("[dim]Model unloaded, GPU memory cleared[/dim]")


def generate_lecture_notes(
    english_path: str = "temp_output/transcript_en.json",
    bengali_path: str = "temp_output/transcript_bn.json",
    vision_path: str = "temp_output/vision_context.json",
    output_path: str = "final_lecture_notes.md"
) -> str:
    """
    Main function to generate lecture notes from all sources.
    
    Args:
        english_path: Path to English transcript JSON
        bengali_path: Path to Bengali transcript JSON  
        vision_path: Path to vision context JSON
        output_path: Output path for Markdown notes
        
    Returns:
        Generated lecture notes as string
    """
    console.print(Panel.fit(
        "[bold white]Phase 5: Final Summarization[/bold white]\n"
        "Merging Audio + Vision into Lecture Notes",
        border_style="cyan"
    ))
    
    generator = LectureNoteGenerator()
    
    # Load all context
    context = generator.load_context_files(english_path, bengali_path, vision_path)
    
    # Generate notes
    notes = generator.generate_notes(context)
    
    # Save output
    generator.save_notes(notes, output_path)
    
    return notes


# =============================================================================
# CLI
# =============================================================================
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate lecture notes from multimodal sources")
    parser.add_argument("--english", "-e", default="temp_output/transcript_en.json",
                        help="Path to English transcript JSON")
    parser.add_argument("--bengali", "-b", default="temp_output/transcript_bn.json",
                        help="Path to Bengali transcript JSON")
    parser.add_argument("--vision", "-v", default="temp_output/vision_context.json",
                        help="Path to vision context JSON")
    parser.add_argument("--output", "-o", default="final_lecture_notes.md",
                        help="Output Markdown file path")
    
    args = parser.parse_args()
    
    notes = generate_lecture_notes(
        english_path=args.english,
        bengali_path=args.bengali,
        vision_path=args.vision,
        output_path=args.output
    )
    
    # Print result
    print("\n" + "=" * 70)
    print("GENERATED LECTURE NOTES")
    print("=" * 70)
    print(notes)
