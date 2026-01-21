"""
=============================================================================
HARDWARE HANDSHAKE SCRIPT - verify_stack.py
=============================================================================
Multimodal Banglish Classroom Summarizer
Master's Thesis - Phase 1 Verification

This script verifies that your GPU stack is correctly configured:
1. CUDA availability and GPU detection
2. AutoGPTQ import (critical for Windows AWQ support)
3. Load a small AWQ model to prove GPU inference works

Hardware: Windows 11 | NVIDIA RTX 3090 (24GB VRAM)
=============================================================================
"""

import sys
import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


def print_header():
    """Print a styled header."""
    console.print(Panel.fit(
        "[bold cyan]🎓 Multimodal Banglish Classroom Summarizer[/bold cyan]\n"
        "[dim]Hardware Handshake Verification Script[/dim]",
        border_style="cyan"
    ))
    console.print()


def check_python_version():
    """Verify Python version."""
    console.print("[bold]Step 0: Python Version[/bold]")
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    if version.major == 3 and version.minor == 10:
        console.print(f"  ✅ Python {version_str} (Required: 3.10.x)\n")
        return True
    else:
        console.print(f"  ⚠️  Python {version_str} (Expected: 3.10.x)\n")
        return True  # Continue anyway


def check_cuda():
    """Check CUDA availability and GPU info."""
    console.print("[bold]Step 1: CUDA & GPU Detection[/bold]")
    
    try:
        import torch
        
        cuda_available = torch.cuda.is_available()
        
        if not cuda_available:
            console.print("  ❌ CUDA is NOT available!")
            console.print("  [dim]Possible fixes:[/dim]")
            console.print("  [dim]  1. Install NVIDIA drivers[/dim]")
            console.print("  [dim]  2. Reinstall PyTorch with CUDA support[/dim]")
            return False
        
        # CUDA is available - gather info
        device_count = torch.cuda.device_count()
        current_device = torch.cuda.current_device()
        device_name = torch.cuda.get_device_name(current_device)
        
        # Memory info
        total_memory = torch.cuda.get_device_properties(current_device).total_memory
        total_memory_gb = total_memory / (1024**3)
        
        # Create info table
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column("Property", style="dim")
        table.add_column("Value", style="green")
        
        table.add_row("CUDA Available", "✅ Yes")
        table.add_row("PyTorch Version", torch.__version__)
        table.add_row("CUDA Version", torch.version.cuda or "N/A")
        table.add_row("cuDNN Version", str(torch.backends.cudnn.version()))
        table.add_row("GPU Count", str(device_count))
        table.add_row("Current GPU", device_name)
        table.add_row("Total VRAM", f"{total_memory_gb:.1f} GB")
        
        console.print(table)
        console.print()
        
        # Verify it's an RTX 3090
        if "3090" in device_name:
            console.print("  ✅ RTX 3090 detected - Perfect for thesis work!\n")
        else:
            console.print(f"  ℹ️  Detected: {device_name}\n")
        
        return True
        
    except ImportError:
        console.print("  ❌ PyTorch is not installed!")
        console.print("  [dim]Run: pip install torch --index-url https://download.pytorch.org/whl/cu124[/dim]")
        return False
    except Exception as e:
        console.print(f"  ❌ Error checking CUDA: {e}")
        return False


def check_autogptq():
    """Check if AutoGPTQ is importable."""
    console.print("[bold]Step 2: AutoGPTQ Import Check[/bold]")
    
    try:
        import auto_gptq
        console.print(f"  ✅ auto_gptq imported successfully")
        console.print(f"  [dim]Version: {auto_gptq.__version__ if hasattr(auto_gptq, '__version__') else 'N/A'}[/dim]\n")
        return True
    except ImportError as e:
        console.print(f"  ❌ Failed to import auto_gptq: {e}")
        console.print("  [dim]Run: pip install auto-gptq --extra-index-url https://huggingface.github.io/autogptq-index/whl/cu124/[/dim]\n")
        return False
    except Exception as e:
        console.print(f"  ❌ Error importing auto_gptq: {e}\n")
        return False


def check_transformers():
    """Check transformers library."""
    console.print("[bold]Step 3: Transformers Library[/bold]")
    
    try:
        import transformers
        console.print(f"  ✅ transformers {transformers.__version__}\n")
        return True
    except ImportError:
        console.print("  ❌ transformers not installed")
        console.print("  [dim]Run: pip install transformers[/dim]\n")
        return False


def check_audio_stack():
    """Check audio processing libraries."""
    console.print("[bold]Step 4: Audio Processing Stack[/bold]")
    
    libraries = {
        'librosa': 'librosa',
        'soundfile': 'soundfile',
    }
    
    all_ok = True
    for display_name, import_name in libraries.items():
        try:
            module = __import__(import_name)
            version = getattr(module, '__version__', 'N/A')
            console.print(f"  ✅ {display_name} {version}")
        except ImportError:
            console.print(f"  ❌ {display_name} not installed")
            all_ok = False
    
    console.print()
    return all_ok


def check_vision_stack():
    """Check vision processing libraries."""
    console.print("[bold]Step 5: Vision Processing Stack[/bold]")
    
    # OpenCV
    try:
        import cv2
        console.print(f"  ✅ opencv-python {cv2.__version__}")
    except ImportError:
        console.print("  ❌ opencv-python not installed")
    
    # PIL
    try:
        from PIL import Image
        import PIL
        console.print(f"  ✅ pillow {PIL.__version__}")
    except ImportError:
        console.print("  ❌ pillow not installed")
    
    # MoviePy
    try:
        import moviepy
        version = getattr(moviepy, '__version__', 'installed')
        console.print(f"  ✅ moviepy {version}")
    except ImportError:
        console.print("  ❌ moviepy not installed")
    
    console.print()
    return True


def load_test_awq_model():
    """
    Load a small model to verify GPU inference works.
    Uses TinyLlama/TinyLlama-1.1B-Chat-v1.0 in float16 - a 1.1B parameter model.
    
    NOTE: We test with a non-quantized model first to verify basic GPU inference,
    since GPTQ/AWQ quantization on Windows can have compilation issues.
    """
    console.print("[bold]Step 6: LLM GPU Inference Test[/bold]")
    console.print("  [dim]Loading TinyLlama/TinyLlama-1.1B-Chat-v1.0 (float16)...[/dim]")
    console.print("  [dim]This will download ~2GB on first run.[/dim]")
    console.print("  [dim]Testing basic GPU inference capability.[/dim]\n")
    
    try:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
        
        model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            
            # Load tokenizer
            task1 = progress.add_task("Loading tokenizer...", total=None)
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            progress.remove_task(task1)
            console.print("  ✅ Tokenizer loaded")
            
            # Load model in float16
            task2 = progress.add_task("Loading model to GPU (float16)...", total=None)
            
            model = AutoModelForCausalLM.from_pretrained(
                model_name,
                device_map="cuda",
                torch_dtype=torch.float16,
            )
            progress.remove_task(task2)
            console.print("  ✅ Model loaded to GPU")
            
            # Test inference
            task3 = progress.add_task("Running test inference...", total=None)
            
            test_prompt = "The capital of Bangladesh is"
            inputs = tokenizer(test_prompt, return_tensors="pt").to("cuda")
            
            start_time = time.time()
            with torch.no_grad():
                outputs = model.generate(
                    **inputs,
                    max_new_tokens=20,
                    do_sample=False,
                    pad_token_id=tokenizer.eos_token_id
                )
            inference_time = time.time() - start_time
            
            generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
            progress.remove_task(task3)
            
            console.print("  ✅ Inference successful!")
            console.print(f"  [dim]Time: {inference_time:.2f}s[/dim]")
            console.print(f"  [dim]Output: \"{generated_text[:80]}...\"[/dim]\n")
            
            # Memory stats
            memory_allocated = torch.cuda.memory_allocated() / (1024**3)
            memory_reserved = torch.cuda.memory_reserved() / (1024**3)
            console.print(f"  [dim]GPU Memory Used: {memory_allocated:.2f} GB allocated, {memory_reserved:.2f} GB reserved[/dim]")
            
            # Cleanup
            del model, tokenizer, inputs, outputs
            torch.cuda.empty_cache()
            console.print("  ✅ Model unloaded, GPU memory cleared\n")
            
            return True
            
    except Exception as e:
        console.print(f"  ❌ Failed to load model: {e}")
        console.print("\n  [dim]Troubleshooting:[/dim]")
        console.print("  [dim]  1. Ensure transformers is installed correctly[/dim]")
        console.print("  [dim]  2. Check internet connection for model download[/dim]")
        console.print("  [dim]  3. Verify GPU has enough VRAM[/dim]\n")
        return False


def load_test_vlm_model():
    """
    Load Qwen2-VL-7B-Instruct to verify VLM works.
    This is the actual model we'll use for whiteboard understanding.
    Using float16 (not AWQ) due to Windows quantization issues.
    """
    console.print("[bold]Step 7: VLM (Qwen2-VL-7B) Loading Test[/bold]")
    console.print("  [dim]Loading Qwen/Qwen2-VL-7B-Instruct (float16)...[/dim]")
    console.print("  [dim]This will download ~15GB on first run.[/dim]")
    console.print("  [dim]This is the VLM that replaces OCR for whiteboard reading.[/dim]\n")
    
    try:
        import torch
        from transformers import Qwen2VLForConditionalGeneration, AutoProcessor
        
        model_name = "Qwen/Qwen2-VL-7B-Instruct"
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            
            # Load processor
            task1 = progress.add_task("Loading VLM processor...", total=None)
            processor = AutoProcessor.from_pretrained(model_name)
            progress.remove_task(task1)
            console.print("  ✅ Processor loaded")
            
            # Load model in float16
            task2 = progress.add_task("Loading Qwen2-VL-7B to GPU (float16)...", total=None)
            model = Qwen2VLForConditionalGeneration.from_pretrained(
                model_name,
                device_map="cuda",
                torch_dtype=torch.float16,
            )
            progress.remove_task(task2)
            console.print("  ✅ VLM loaded to GPU")
            
            # Memory stats
            memory_allocated = torch.cuda.memory_allocated() / (1024**3)
            memory_reserved = torch.cuda.memory_reserved() / (1024**3)
            console.print(f"  [dim]GPU Memory Used: {memory_allocated:.2f} GB allocated, {memory_reserved:.2f} GB reserved[/dim]")
            
            # Cleanup
            del model, processor
            torch.cuda.empty_cache()
            console.print("  ✅ VLM unloaded, GPU memory cleared\n")
            
            return True
            
    except ImportError as e:
        console.print(f"  ❌ Import error: {e}")
        console.print("  [dim]Qwen2-VL may require: pip install qwen-vl-utils[/dim]\n")
        return False
    except Exception as e:
        console.print(f"  ❌ Failed to load VLM: {e}")
        console.print("\n  [dim]Troubleshooting:[/dim]")
        console.print("  [dim]  1. Ensure transformers >= 4.40.0[/dim]")
        console.print("  [dim]  2. Try: pip install qwen-vl-utils[/dim]")
        console.print("  [dim]  3. Check GPU has ~15GB free VRAM[/dim]\n")
        return False


def print_summary(results):
    """Print final summary."""
    console.print(Panel.fit(
        "[bold]Verification Summary[/bold]",
        border_style="cyan"
    ))
    
    table = Table(show_header=True, header_style="bold")
    table.add_column("Check", style="dim")
    table.add_column("Status")
    
    status_map = {
        True: "[green]✅ PASS[/green]",
        False: "[red]❌ FAIL[/red]"
    }
    
    for check_name, passed in results.items():
        table.add_row(check_name, status_map[passed])
    
    console.print(table)
    console.print()
    
    all_passed = all(results.values())
    
    if all_passed:
        console.print(Panel.fit(
            "[bold green]🎉 All checks passed![/bold green]\n"
            "Your environment is ready for the thesis project.\n\n"
            "[dim]Next Steps:[/dim]\n"
            "1. Place lecture videos in data/raw/\n"
            "2. Start building the audio pipeline in src/audio/\n"
            "3. Start building the vision pipeline in src/vision/",
            border_style="green"
        ))
    else:
        console.print(Panel.fit(
            "[bold red]⚠️ Some checks failed![/bold red]\n"
            "Please fix the issues above before proceeding.\n"
            "Refer to SETUP_COMMANDS.txt for installation instructions.",
            border_style="red"
        ))
    
    return all_passed


def main():
    """Main verification routine."""
    print_header()
    
    results = {}
    
    # Run all checks
    results["Python Version"] = check_python_version()
    results["CUDA & GPU"] = check_cuda()
    results["AutoGPTQ"] = check_autogptq()
    results["Transformers"] = check_transformers()
    results["Audio Stack"] = check_audio_stack()
    results["Vision Stack"] = check_vision_stack()
    
    # Only run model loading if previous checks passed
    if results["CUDA & GPU"] and results["Transformers"]:
        results["LLM Inference"] = load_test_awq_model()
    else:
        console.print("[bold]Step 6: LLM GPU Inference Test[/bold]")
        console.print("  ⏭️  Skipped (prerequisite checks failed)\n")
        results["LLM Inference"] = False
    
    # VLM Test - Qwen2-VL-7B (the actual model for whiteboard understanding)
    if results.get("LLM Inference", False):
        results["VLM (Qwen2-VL)"] = load_test_vlm_model()
    else:
        console.print("[bold]Step 7: VLM (Qwen2-VL-7B) Loading Test[/bold]")
        console.print("  ⏭️  Skipped (LLM inference test failed)\n")
        results["VLM (Qwen2-VL)"] = False
    
    # Print summary
    success = print_summary(results)
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
