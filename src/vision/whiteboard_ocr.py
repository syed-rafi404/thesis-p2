"""
=============================================================================
WHITEBOARD OCR - Vision Language Model for Whiteboard Understanding
=============================================================================
Multimodal Banglish Classroom Summarizer
Master's Thesis - Phase 4: Vision Module

Uses Qwen2.5-VL-7B-Instruct to extract text, formulas, and diagrams
from whiteboard images. VLM approach replaces traditional OCR for
better understanding of handwritten and mixed-language content.

Model: Qwen/Qwen2.5-VL-7B-Instruct (FP16, ~15GB VRAM)
=============================================================================
"""

import sys
import json
from pathlib import Path
from typing import List, Dict, Any
from dataclasses import dataclass, asdict

import torch
from PIL import Image
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.panel import Panel

console = Console()


@dataclass
class FrameAnalysis:
    """Analysis result for a single frame."""
    frame_path: str
    frame_number: int
    timestamp_sec: float  # Estimated from frame number and interval
    content: str          # Extracted whiteboard content
    has_content: bool     # Whether meaningful content was found
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass 
class VisionContext:
    """Complete vision analysis for all frames."""
    frames: List[FrameAnalysis]
    total_frames: int
    frames_with_content: int
    model: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "model": self.model,
            "total_frames": self.total_frames,
            "frames_with_content": self.frames_with_content,
            "frames": [f.to_dict() for f in self.frames]
        }
    
    def save(self, output_path: str):
        """Save to JSON file."""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)
    
    def get_combined_content(self) -> str:
        """Get all unique content combined."""
        contents = [f.content for f in self.frames if f.has_content]
        return "\n\n---\n\n".join(contents)


class WhiteboardVLM:
    """
    Vision Language Model for whiteboard content extraction.
    
    Uses Qwen2.5-VL-7B-Instruct to understand and transcribe
    whiteboard content including text, formulas, and diagrams.
    """
    
    def __init__(
        self,
        model_name: str = "Qwen/Qwen2.5-VL-7B-Instruct",
        torch_dtype: torch.dtype = torch.float16,
        device_map: str = "auto"
    ):
        self.model_name = model_name
        self.torch_dtype = torch_dtype
        self.device_map = device_map
        self.model = None
        self.processor = None
        self._is_loaded = False
    
    def load_model(self):
        """Load the Qwen2.5-VL model."""
        if self._is_loaded:
            return
        
        console.print(f"\n[bold cyan]🖼️  Loading Vision Language Model[/bold cyan]")
        console.print(f"[dim]Model: {self.model_name}[/dim]")
        console.print(f"[dim]Precision: FP16 | Device Map: {self.device_map}[/dim]\n")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Loading Qwen2.5-VL model...", total=None)
            
            from transformers import Qwen2_5_VLForConditionalGeneration, AutoProcessor
            
            # Load model with FP16
            self.model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
                self.model_name,
                torch_dtype=self.torch_dtype,
                device_map=self.device_map,
            )
            
            # Load processor
            self.processor = AutoProcessor.from_pretrained(self.model_name)
            
            progress.remove_task(task)
        
        # Get VRAM usage
        if torch.cuda.is_available():
            memory_gb = torch.cuda.memory_allocated() / (1024**3)
            console.print(f"[green]✓ Qwen2.5-VL loaded[/green] [dim]({memory_gb:.2f} GB VRAM)[/dim]\n")
        else:
            console.print("[green]✓ Qwen2.5-VL loaded[/green]\n")
        
        self._is_loaded = True
    
    def analyze_frame(self, image_path: str) -> str:
        """
        Analyze a single whiteboard frame.
        
        Args:
            image_path: Path to the frame image
            
        Returns:
            Extracted content from the whiteboard
        """
        if not self._is_loaded:
            self.load_model()
        
        # Load image
        image = Image.open(image_path).convert("RGB")
        
        # Whiteboard extraction prompt
        prompt = "Transcribe all text, formulas, and diagrams written on this whiteboard. Ignore people."
        
        # Build conversation format for Qwen2.5-VL
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "image", "image": image},
                    {"type": "text", "text": prompt}
                ]
            }
        ]
        
        # Process with the model
        text = self.processor.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        
        inputs = self.processor(
            text=[text],
            images=[image],
            padding=True,
            return_tensors="pt"
        )
        inputs = inputs.to(self.model.device)
        
        # Generate response
        with torch.no_grad():
            generated_ids = self.model.generate(
                **inputs,
                max_new_tokens=512,
                do_sample=False,
                temperature=None,
                top_p=None,
            )
        
        # Decode - only get the new tokens (skip input)
        generated_ids_trimmed = [
            out_ids[len(in_ids):] 
            for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
        ]
        
        response = self.processor.batch_decode(
            generated_ids_trimmed,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=False
        )[0]
        
        return response.strip()
    
    def extract_board_content(
        self,
        frames_dir: str,
        frame_interval: int = 30  # seconds between frames
    ) -> VisionContext:
        """
        Extract content from all whiteboard frames.
        
        Args:
            frames_dir: Directory containing frame images
            frame_interval: Time interval between frames (for timestamp estimation)
            
        Returns:
            VisionContext with all frame analyses
        """
        self.load_model()
        
        frames_dir = Path(frames_dir)
        if not frames_dir.exists():
            raise FileNotFoundError(f"Frames directory not found: {frames_dir}")
        
        # Find all frame images
        frame_files = sorted(frames_dir.glob("frame_*.jpg"))
        if not frame_files:
            frame_files = sorted(frames_dir.glob("frame_*.png"))
        if not frame_files:
            frame_files = sorted(frames_dir.glob("*.jpg")) + sorted(frames_dir.glob("*.png"))
        
        if not frame_files:
            raise FileNotFoundError(f"No frame images found in {frames_dir}")
        
        console.print(f"[bold]📸 Analyzing {len(frame_files)} frames...[/bold]\n")
        
        analyses = []
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console,
        ) as progress:
            task = progress.add_task("Processing frames...", total=len(frame_files))
            
            for i, frame_path in enumerate(frame_files):
                progress.update(task, description=f"Analyzing {frame_path.name}...")
                
                try:
                    # Extract frame number from filename
                    frame_num = i + 1
                    try:
                        # Try to parse frame number from filename like "frame_0001.jpg"
                        frame_num = int(frame_path.stem.split('_')[-1])
                    except (ValueError, IndexError):
                        pass
                    
                    # Analyze the frame
                    content = self.analyze_frame(str(frame_path))
                    
                    # Check if meaningful content was found
                    has_content = bool(content) and len(content) > 10
                    
                    # Estimate timestamp
                    timestamp = (frame_num - 1) * frame_interval
                    
                    analysis = FrameAnalysis(
                        frame_path=str(frame_path),
                        frame_number=frame_num,
                        timestamp_sec=timestamp,
                        content=content,
                        has_content=has_content
                    )
                    analyses.append(analysis)
                    
                except Exception as e:
                    console.print(f"[yellow]⚠ Error processing {frame_path.name}: {e}[/yellow]")
                    analyses.append(FrameAnalysis(
                        frame_path=str(frame_path),
                        frame_number=i + 1,
                        timestamp_sec=(i) * frame_interval,
                        content=f"Error: {str(e)}",
                        has_content=False
                    ))
                
                progress.advance(task)
        
        # Build context
        frames_with_content = sum(1 for a in analyses if a.has_content)
        
        context = VisionContext(
            frames=analyses,
            total_frames=len(analyses),
            frames_with_content=frames_with_content,
            model=self.model_name
        )
        
        console.print(f"\n[green]✓ Vision analysis complete[/green]")
        console.print(f"[dim]  Total frames: {len(analyses)} | With content: {frames_with_content}[/dim]\n")
        
        return context
    
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
            console.print("[dim]Qwen2.5-VL model unloaded, GPU memory cleared[/dim]")


# =============================================================================
# CLI
# =============================================================================
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Whiteboard OCR using Qwen2.5-VL")
    parser.add_argument("frames_dir", help="Directory containing frame images")
    parser.add_argument("--output", "-o", default="temp_output/vision_context.json",
                        help="Output JSON path")
    parser.add_argument("--interval", "-i", type=int, default=30,
                        help="Time interval between frames in seconds")
    
    args = parser.parse_args()
    
    # Run extraction
    vlm = WhiteboardVLM()
    context = vlm.extract_board_content(args.frames_dir, args.interval)
    
    # Save output
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    context.save(str(output_path))
    
    console.print(f"[bold green]✓ Saved to:[/bold green] {output_path}\n")
    
    # Print results
    print("=" * 70)
    print("WHITEBOARD CONTENT EXTRACTION RESULTS")
    print("=" * 70)
    
    for frame in context.frames:
        print(f"\n📸 Frame {frame.frame_number} (t={frame.timestamp_sec}s)")
        print("-" * 50)
        if frame.has_content:
            print(frame.content[:500] + "..." if len(frame.content) > 500 else frame.content)
        else:
            print("[No meaningful content detected]")
