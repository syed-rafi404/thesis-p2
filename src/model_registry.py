"""
=============================================================================
MODEL REGISTRY - Singleton Pattern for GPU Model Management
=============================================================================
Multimodal Banglish Classroom Summarizer
Master's Thesis

Keeps models loaded in GPU memory to avoid repeated loading overhead.
Essential for:
1. Batch processing (process multiple videos without reloading)
2. Live inference (real-time processing with zero loading latency)

Usage:
    from src.model_registry import ModelRegistry
    
    registry = ModelRegistry.get_instance()
    whisper = registry.get_whisper()  # First call loads, subsequent calls return cached
    vlm = registry.get_vlm()
    
Memory Management:
    registry.unload("whisper")  # Free specific model
    registry.unload_all()       # Free all models
    registry.get_memory_usage() # Check VRAM usage
=============================================================================
"""

import gc
import torch
from typing import Dict, Any, Optional
from dataclasses import dataclass
from rich.console import Console
from rich.panel import Panel

console = Console()


@dataclass
class ModelInfo:
    """Information about a loaded model."""
    name: str
    model: Any
    processor: Any = None
    vram_gb: float = 0.0
    device: str = "cuda"


class ModelRegistry:
    """
    Singleton registry for managing GPU models.
    
    Keeps models loaded in memory for fast inference.
    Handles VRAM management and model lifecycle.
    """
    
    _instance: Optional['ModelRegistry'] = None
    
    def __init__(self):
        if ModelRegistry._instance is not None:
            raise RuntimeError("Use ModelRegistry.get_instance() instead")
        
        self._models: Dict[str, ModelInfo] = {}
        self._device = "cuda" if torch.cuda.is_available() else "cpu"
        
    @classmethod
    def get_instance(cls) -> 'ModelRegistry':
        """Get the singleton instance."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    @classmethod
    def reset_instance(cls):
        """Reset the singleton (for testing)."""
        if cls._instance is not None:
            cls._instance.unload_all()
            cls._instance = None
    
    # =========================================================================
    # Model Accessors (lazy loading)
    # =========================================================================
    
    def get_whisper(
        self, 
        model_name: str = "openai/whisper-large-v3-turbo",
        device: str = None,
        torch_dtype: torch.dtype = None,
        model_id: str = None  # Alias for model_name
    ) -> tuple:
        """Get Whisper model and processor (loads if not cached).
        
        Args:
            model_name: HuggingFace model identifier
            device: Target device (defaults to registry's device)
            torch_dtype: Data type for model (defaults to float16)
            model_id: Alias for model_name (for backward compatibility)
        """
        # Handle both model_name and model_id for compatibility
        model_id = model_name if model_id is None else model_id
        key = f"whisper:{model_id}"
        
        if key not in self._models:
            console.print(f"[cyan]📦 Loading Whisper (caching for reuse)...[/cyan]")
            model, processor = self._load_whisper(model_id)
            vram = self._get_model_vram(model)
            self._models[key] = ModelInfo(
                name="Whisper",
                model=model,
                processor=processor,
                vram_gb=vram,
                device=device or self._device
            )
            console.print(f"[green]✓ Whisper cached ({vram:.2f} GB VRAM)[/green]")
        
        info = self._models[key]
        return info.model, info.processor
    
    def get_bangla_asr(
        self, 
        model_name: str = "bangla-speech-processing/BanglaASR",
        device: str = None,
        torch_dtype: torch.dtype = None,
        model_id: str = None  # Alias for model_name
    ) -> Any:
        """Get BanglaASR pipeline (loads if not cached).
        
        Args:
            model_name: HuggingFace model identifier
            device: Target device (defaults to registry's device)
            torch_dtype: Data type for model
            model_id: Alias for model_name (for backward compatibility)
        """
        model_id = model_name if model_id is None else model_id
        key = f"bangla_asr:{model_id}"
        
        if key not in self._models:
            console.print(f"[cyan]📦 Loading BanglaASR (caching for reuse)...[/cyan]")
            pipe = self._load_bangla_asr(model_id)
            # BanglaASR is a fine-tuned Whisper-small (~242M params, ~0.5GB VRAM)
            vram = self._get_pipeline_vram(pipe)
            self._models[key] = ModelInfo(
                name="BanglaASR",
                model=pipe,
                vram_gb=vram,
                device=device or self._device
            )
            console.print(f"[green]✓ BanglaASR cached ({vram:.2f} GB VRAM)[/green]")
        
        return self._models[key].model
    
    def get_vlm(
        self, 
        model_name: str = "Qwen/Qwen2.5-VL-7B-Instruct",
        torch_dtype: torch.dtype = None,
        device_map: str = "auto",
        use_4bit: bool = False,
        use_8bit: bool = False,
        model_id: str = None  # Alias for model_name
    ) -> tuple:
        """Get VLM model and processor (loads if not cached).
        
        Args:
            model_name: HuggingFace model identifier
            torch_dtype: Data type for model (defaults to float16)
            device_map: Device mapping strategy
            use_4bit: If True, load model with 4-bit quantization (~4.5GB for 7B)
            use_8bit: If True, load model with 8-bit quantization (~8GB for 7B, better quality)
            model_id: Alias for model_name (for backward compatibility)
        """
        model_id = model_name if model_id is None else model_id
        quant_suffix = "_8bit" if use_8bit else ("_4bit" if use_4bit else "")
        key = f"vlm:{model_id}{quant_suffix}"
        
        if key not in self._models:
            if use_8bit:
                console.print(f"[cyan]📦 Loading VLM 8-bit quantized (~8GB, better quality)...[/cyan]")
                model, processor = self._load_vlm_8bit(model_id)
                vram = 8.0  # Approximate for 7B 8-bit VLM
            elif use_4bit:
                console.print(f"[cyan]📦 Loading VLM 4-bit quantized (saves ~11GB VRAM)...[/cyan]")
                model, processor = self._load_vlm_4bit(model_id)
                vram = 4.5  # Approximate for 7B 4-bit VLM
            else:
                console.print(f"[cyan]📦 Loading VLM FP16 (caching for reuse)...[/cyan]")
                model, processor = self._load_vlm(model_id)
                vram = self._get_model_vram(model)
            
            self._models[key] = ModelInfo(
                name=f"VLM{quant_suffix}",
                model=model,
                processor=processor,
                vram_gb=vram,
                device=self._device
            )
            console.print(f"[green]✓ VLM cached ({vram:.2f} GB VRAM)[/green]")
        
        info = self._models[key]
        return info.model, info.processor
    
    def get_llm(
        self, 
        model_name: str = "Qwen/Qwen2.5-14B-Instruct",
        torch_dtype: torch.dtype = None,
        device_map: str = "auto",
        use_4bit: bool = False,
        model_id: str = None  # Alias for model_name
    ) -> tuple:
        """Get LLM model and tokenizer (loads if not cached).
        
        Args:
            model_name: HuggingFace model identifier
            torch_dtype: Data type for model (defaults to float16)
            device_map: Device mapping strategy
            use_4bit: If True, load model with 4-bit quantization (saves ~11GB VRAM)
            model_id: Alias for model_name (for backward compatibility)
        """
        model_id = model_name if model_id is None else model_id
        quant_suffix = "_4bit" if use_4bit else ""
        key = f"llm:{model_id}{quant_suffix}"
        
        if key not in self._models:
            if use_4bit:
                console.print(f"[cyan]📦 Loading LLM 4-bit quantized (saves ~11GB VRAM)...[/cyan]")
                model, tokenizer = self._load_llm_4bit(model_id)
                vram = 9.0  # Approximate for 14B 4-bit
            else:
                console.print(f"[cyan]📦 Loading LLM FP16 (caching for reuse)...[/cyan]")
                model, tokenizer = self._load_llm(model_id)
                vram = self._get_model_vram(model)
            
            self._models[key] = ModelInfo(
                name=f"LLM{quant_suffix}",
                model=model,
                processor=tokenizer,
                vram_gb=vram,
                device=self._device
            )
            console.print(f"[green]✓ LLM cached ({vram:.2f} GB VRAM)[/green]")
        
        info = self._models[key]
        return info.model, info.processor
    
    def get_yolo_pose(self, model_path: str = "yolov8n-pose.pt") -> Any:
        """Get YOLOv8-Pose model (loads if not cached)."""
        key = f"yolo:{model_path}"
        
        if key not in self._models:
            console.print(f"[cyan]📦 Loading YOLOv8-Pose (caching for reuse)...[/cyan]")
            from ultralytics import YOLO
            model = YOLO(model_path)
            self._models[key] = ModelInfo(
                name="YOLOv8-Pose",
                model=model,
                vram_gb=0.5,  # Very small
                device=self._device
            )
            console.print(f"[green]✓ YOLOv8-Pose cached[/green]")
        
        return self._models[key].model
    
    # =========================================================================
    # Model Loaders (private)
    # =========================================================================
    
    def _load_whisper(self, model_id: str) -> tuple:
        """Load Whisper model and processor."""
        from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor
        
        model = AutoModelForSpeechSeq2Seq.from_pretrained(
            model_id,
            torch_dtype=torch.float16,
            low_cpu_mem_usage=True,
            use_safetensors=True
        ).to(self._device)
        
        processor = AutoProcessor.from_pretrained(model_id)
        return model, processor
    
    def _load_bangla_asr(self, model_id: str) -> Any:
        """Load BanglaASR pipeline."""
        from transformers import pipeline
        
        pipe = pipeline(
            "automatic-speech-recognition",
            model=model_id,
            torch_dtype=torch.float16,
            device=self._device
        )
        return pipe
    
    def _load_vlm(self, model_id: str) -> tuple:
        """Load Vision-Language Model (Qwen2.5-VL FP16)."""
        from transformers import Qwen2_5_VLForConditionalGeneration, AutoProcessor
        
        model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
            model_id,
            torch_dtype=torch.float16,
            device_map="auto",
            low_cpu_mem_usage=True
        )
        
        processor = AutoProcessor.from_pretrained(model_id)
        return model, processor
    
    def _load_vlm_4bit(self, model_id: str) -> tuple:
        """Load Vision-Language Model with 4-bit quantization (saves ~11GB VRAM).
        
        Uses bitsandbytes NF4 quantization for efficient inference.
        Recommended for GPUs with <16GB VRAM (e.g., RTX 3060 12GB).
        """
        from transformers import Qwen2_5_VLForConditionalGeneration, AutoProcessor, BitsAndBytesConfig
        
        # Configure 4-bit quantization
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_quant_type="nf4",  # Normalized float 4-bit
            bnb_4bit_use_double_quant=True,  # Double quantization for more savings
        )
        
        console.print(f"[dim]  VLM Quantization: NF4 with double quant[/dim]")
        
        model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
            model_id,
            quantization_config=quantization_config,
            device_map="auto",
            low_cpu_mem_usage=True
        )
        
        processor = AutoProcessor.from_pretrained(model_id)
        return model, processor
    
    def _load_vlm_8bit(self, model_id: str) -> tuple:
        """Load Vision-Language Model with 8-bit quantization (~8GB VRAM).
        
        Uses bitsandbytes LLM.int8() quantization for better quality than 4-bit.
        Recommended for GPUs with 12GB VRAM when models are loaded sequentially.
        """
        from transformers import Qwen2_5_VLForConditionalGeneration, AutoProcessor, BitsAndBytesConfig
        
        # Configure 8-bit quantization
        quantization_config = BitsAndBytesConfig(
            load_in_8bit=True,
        )
        
        console.print(f"[dim]  VLM Quantization: INT8 (higher quality than NF4)[/dim]")
        
        model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
            model_id,
            quantization_config=quantization_config,
            device_map="auto",
            low_cpu_mem_usage=True
        )
        
        processor = AutoProcessor.from_pretrained(model_id)
        return model, processor
    
    def _load_llm(self, model_id: str) -> tuple:
        """Load Language Model for summarization (FP16)."""
        from transformers import AutoModelForCausalLM, AutoTokenizer
        
        model = AutoModelForCausalLM.from_pretrained(
            model_id,
            torch_dtype=torch.float16,
            device_map="auto",
            low_cpu_mem_usage=True
        )
        
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        return model, tokenizer
    
    def _load_llm_4bit(self, model_id: str) -> tuple:
        """Load Language Model with 4-bit quantization (saves ~11GB VRAM).
        
        Uses bitsandbytes NF4 quantization for efficient inference.
        Quality loss is minimal for text generation tasks.
        """
        from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
        
        # Configure 4-bit quantization
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_quant_type="nf4",  # Normalized float 4-bit
            bnb_4bit_use_double_quant=True,  # Double quantization for more savings
        )
        
        console.print(f"[dim]  Quantization: NF4 with double quant[/dim]")
        
        model = AutoModelForCausalLM.from_pretrained(
            model_id,
            quantization_config=quantization_config,
            device_map="auto",
            low_cpu_mem_usage=True
        )
        
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        return model, tokenizer
    
    # =========================================================================
    # Memory Management
    # =========================================================================
    
    def _get_model_vram(self, model) -> float:
        """Estimate model VRAM usage in GB."""
        try:
            param_bytes = sum(p.numel() * p.element_size() for p in model.parameters())
            return param_bytes / (1024 ** 3)
        except:
            return 0.0
    
    def _get_pipeline_vram(self, pipe) -> float:
        """Estimate pipeline model VRAM usage in GB."""
        try:
            # Pipelines wrap models - access the underlying model
            if hasattr(pipe, 'model'):
                return self._get_model_vram(pipe.model)
            return 0.5  # Default fallback
        except:
            return 0.5
    
    def get_memory_usage(self) -> Dict[str, float]:
        """Get VRAM usage for all cached models."""
        usage = {}
        for key, info in self._models.items():
            usage[info.name] = info.vram_gb
        usage["total"] = sum(usage.values())
        
        # Add actual GPU memory
        if torch.cuda.is_available():
            usage["gpu_allocated"] = torch.cuda.memory_allocated() / (1024 ** 3)
            usage["gpu_reserved"] = torch.cuda.memory_reserved() / (1024 ** 3)
        
        return usage
    
    def unload(self, model_type: str):
        """Unload a specific model type to free GPU memory."""
        keys_to_remove = [k for k in self._models if k.startswith(model_type)]
        
        for key in keys_to_remove:
            info = self._models.pop(key)
            del info.model
            if info.processor:
                del info.processor
            console.print(f"[yellow]🗑️ Unloaded {info.name}[/yellow]")
        
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
    
    def unload_all(self):
        """Unload all models to free GPU memory."""
        for key in list(self._models.keys()):
            info = self._models.pop(key)
            del info.model
            if info.processor:
                del info.processor
        
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        
        console.print("[yellow]🗑️ All models unloaded[/yellow]")
    
    def is_loaded(self, model_type: str) -> bool:
        """Check if a model type is currently loaded."""
        return any(k.startswith(model_type) for k in self._models)
    
    def list_loaded(self) -> list:
        """List all currently loaded models."""
        return [info.name for info in self._models.values()]
    
    def ensure_only(self, *model_types: str):
        """
        Ensure only the specified model types are loaded.
        Unloads all other models to free VRAM.
        
        Usage for 24GB GPU stage-based loading:
            registry.ensure_only("vlm")      # Vision stage
            registry.ensure_only("whisper", "bangla_asr")  # Audio stage
            registry.ensure_only("llm")      # Summarization stage
        
        Args:
            *model_types: Model type prefixes to keep (e.g., "vlm", "whisper", "llm")
        """
        keep_set = set(model_types)
        keys_to_remove = []
        
        for key in self._models:
            # Check if this key should be kept
            should_keep = any(key.startswith(mt) for mt in keep_set)
            if not should_keep:
                keys_to_remove.append(key)
        
        if keys_to_remove:
            for key in keys_to_remove:
                info = self._models.pop(key)
                del info.model
                if info.processor:
                    del info.processor
                console.print(f"[dim]🔄 Swapped out {info.name} to free VRAM[/dim]")
            
            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
    
    def get_available_vram(self) -> float:
        """Get available GPU VRAM in GB."""
        if torch.cuda.is_available():
            total = torch.cuda.get_device_properties(0).total_memory / (1024 ** 3)
            allocated = torch.cuda.memory_allocated() / (1024 ** 3)
            return total - allocated
        return 0.0
    
    def __repr__(self) -> str:
        models = ", ".join(self.list_loaded()) or "none"
        return f"ModelRegistry(loaded=[{models}])"


# =============================================================================
# Convenience Functions
# =============================================================================

def get_registry() -> ModelRegistry:
    """Get the global model registry instance."""
    return ModelRegistry.get_instance()


def preload_models(models: list = None):
    """
    Preload models before processing for zero-latency inference.
    
    Args:
        models: List of model types to preload. 
                Options: ["whisper", "bangla_asr", "vlm", "llm", "yolo"]
                Default: All models
    """
    registry = get_registry()
    
    if models is None:
        models = ["whisper", "vlm", "llm"]  # Most commonly used
    
    console.print(Panel(
        f"[bold cyan]Preloading {len(models)} models for fast inference...[/bold cyan]",
        title="Model Preloader"
    ))
    
    for model_type in models:
        if model_type == "whisper":
            registry.get_whisper()
        elif model_type == "bangla_asr":
            registry.get_bangla_asr()
        elif model_type == "vlm":
            registry.get_vlm()
        elif model_type == "llm":
            registry.get_llm()
        elif model_type == "yolo":
            registry.get_yolo_pose()
    
    usage = registry.get_memory_usage()
    console.print(f"[green]✓ Preloading complete. Total VRAM: {usage['total']:.2f} GB[/green]")


# =============================================================================
# Testing
# =============================================================================

if __name__ == "__main__":
    console.print("[bold]Testing Model Registry...[/bold]\n")
    
    registry = get_registry()
    console.print(f"Registry: {registry}")
    
    # Test lazy loading
    console.print("\n[cyan]First call - should load model:[/cyan]")
    model, proc = registry.get_whisper()
    console.print(f"Got Whisper: {type(model).__name__}")
    
    console.print("\n[cyan]Second call - should use cache:[/cyan]")
    model2, proc2 = registry.get_whisper()
    console.print(f"Same instance: {model is model2}")
    
    # Memory usage
    console.print(f"\n[cyan]Memory usage:[/cyan]")
    for k, v in registry.get_memory_usage().items():
        console.print(f"  {k}: {v:.2f} GB")
    
    # Cleanup
    console.print("\n[cyan]Unloading all...[/cyan]")
    registry.unload_all()
