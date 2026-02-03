"""
Dual-ASR Fusion with LLM (Option 3)

NOVELTY: Uses LLM to intelligently merge Whisper and BanglaASR outputs.

Strategy:
1. Send both transcripts to LLM
2. LLM understands both scripts and merges intelligently
3. Preserves technical terms from Whisper
4. Captures Bengali nuances from BanglaASR
5. Outputs clean, merged transcript

Benefits:
- Semantic understanding (not just word matching)
- Handles script differences naturally
- Can correct errors from both sources
- Produces coherent output
"""

import re
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from pathlib import Path

import torch


@dataclass
class LLMFusionResult:
    """Result of LLM-based fusion."""
    fused_transcript: str
    whisper_input: str
    bangla_input: str
    
    # Metrics
    whisper_char_count: int
    bangla_char_count: int
    fused_char_count: int
    processing_time: float = 0.0
    
    # Quality indicators
    fusion_description: str = ""
    technical_terms_preserved: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "fused_transcript": self.fused_transcript,
            "whisper_char_count": self.whisper_char_count,
            "bangla_char_count": self.bangla_char_count,
            "fused_char_count": self.fused_char_count,
            "processing_time": self.processing_time,
            "fusion_description": self.fusion_description,
            "technical_terms_preserved": self.technical_terms_preserved,
        }


class DualASRFusionLLM:
    """
    LLM-based Dual-ASR Fusion for Banglish Lecture Content.
    
    Uses Qwen2.5-7B-Instruct to merge:
    - Whisper output (English/Romanized Banglish)
    - BanglaASR output (Bengali Unicode)
    
    The LLM understands both scripts and can:
    - Identify overlapping content
    - Choose better transcription per segment
    - Preserve technical terms
    - Output coherent romanized Banglish
    """
    
    def __init__(self, use_4bit: bool = False):
        self.use_4bit = use_4bit
        self.model = None
        self.tokenizer = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Technical terms to preserve
        self.technical_terms = {
            'class', 'object', 'method', 'function', 'variable', 'array',
            'string', 'integer', 'boolean', 'public', 'private', 'static',
            'void', 'return', 'import', 'java', 'python', 'programming',
            'inheritance', 'polymorphism', 'encapsulation', 'abstraction',
            'constructor', 'instance', 'blueprint', 'template', 'design',
            'tutorial', 'example', 'data', 'type', 'behavior', 'property',
            'attribute', 'code', 'compile', 'runtime', 'memory', 'stack',
        }
    
    def _load_model(self):
        """Load the LLM model (reuses from registry if available)."""
        if self.model is not None:
            return
        
        try:
            # Try to use model registry first
            from src.model_registry import get_registry
            registry = get_registry()
            
            if "llm" in registry.loaded_models or "llm_4bit" in registry.loaded_models:
                model_key = "llm_4bit" if self.use_4bit else "llm"
                if model_key in registry.loaded_models:
                    self.model = registry.loaded_models[model_key]["model"]
                    self.tokenizer = registry.loaded_models[model_key]["tokenizer"]
                    print(f"[LLM Fusion] Reusing model from registry")
                    return
        except ImportError:
            pass
        
        # Load directly
        from transformers import AutoModelForCausalLM, AutoTokenizer
        
        model_name = "Qwen/Qwen2.5-7B-Instruct"
        print(f"[LLM Fusion] Loading {model_name}...")
        
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        
        if self.use_4bit:
            from transformers import BitsAndBytesConfig
            quantization_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.float16,
            )
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                quantization_config=quantization_config,
                device_map="auto",
            )
        else:
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                torch_dtype=torch.float16,
                device_map="auto",
            )
        
        print(f"[LLM Fusion] Model loaded")
    
    def _build_fusion_prompt(
        self, 
        whisper_text: str, 
        bangla_text: str,
        max_length: int = 4000
    ) -> str:
        """Build the LLM prompt for fusion."""
        
        # Truncate if needed
        whisper_truncated = whisper_text[:max_length]
        bangla_truncated = bangla_text[:max_length]
        
        system_prompt = """You are an expert at merging transcripts from two different ASR systems.

You will receive:
1. WHISPER TRANSCRIPT - In English/Romanized Banglish (e.g., "ami class ta likhbo")
2. BANGLA ASR TRANSCRIPT - In Bengali Unicode (e.g., "আমি ক্লাস টা লিখবো")

Both transcripts are from the SAME audio lecture, but in different scripts.

Your task:
1. Merge them into a SINGLE coherent transcript in ROMANIZED BANGLISH
2. PRESERVE technical terms from Whisper exactly (class, object, method, function, etc.)
3. Use Bengali understanding from BanglaASR to fill gaps or correct errors
4. Output ONLY the merged transcript, no explanations

Important rules:
- Output must be in Latin script (readable in English)
- Keep all technical programming terms from Whisper
- The transcript is a lecture about Java programming
- Remove repetitions and clean up errors from both sources"""

        user_prompt = f"""Merge these two transcripts of the same lecture:

## WHISPER TRANSCRIPT (English/Romanized):
{whisper_truncated}

## BANGLA ASR TRANSCRIPT (Bengali Unicode):
{bangla_truncated}

## MERGED TRANSCRIPT (Romanized Banglish, technical terms preserved):"""

        return system_prompt, user_prompt
    
    def _extract_preserved_terms(self, text: str) -> List[str]:
        """Extract technical terms that were preserved."""
        words = set(text.lower().split())
        return sorted(words & self.technical_terms)
    
    def fuse(
        self,
        whisper_transcript: str,
        bangla_transcript: str,
    ) -> LLMFusionResult:
        """
        Fuse Whisper and BanglaASR using LLM.
        
        Args:
            whisper_transcript: Output from Whisper
            bangla_transcript: Output from BanglaASR
            
        Returns:
            LLMFusionResult with merged transcript
        """
        import time
        start_time = time.time()
        
        # Load model if needed
        self._load_model()
        
        # Build prompt
        system_prompt, user_prompt = self._build_fusion_prompt(
            whisper_transcript, 
            bangla_transcript
        )
        
        # Generate with LLM
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        
        inputs = self.tokenizer(text, return_tensors="pt").to(self.model.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=2048,
                do_sample=True,
                temperature=0.3,  # Low temperature for more deterministic output
                top_p=0.9,
                pad_token_id=self.tokenizer.eos_token_id,
            )
        
        # Decode
        generated = self.tokenizer.decode(
            outputs[0][inputs['input_ids'].shape[1]:], 
            skip_special_tokens=True
        )
        
        # Clean up the output
        fused_transcript = generated.strip()
        
        # Remove any markdown or explanatory text
        if fused_transcript.startswith("```"):
            fused_transcript = re.sub(r'^```.*?\n', '', fused_transcript)
            fused_transcript = re.sub(r'\n```$', '', fused_transcript)
        
        processing_time = time.time() - start_time
        
        # Extract preserved terms
        preserved = self._extract_preserved_terms(fused_transcript)
        
        return LLMFusionResult(
            fused_transcript=fused_transcript,
            whisper_input=whisper_transcript,
            bangla_input=bangla_transcript,
            whisper_char_count=len(whisper_transcript),
            bangla_char_count=len(bangla_transcript),
            fused_char_count=len(fused_transcript),
            processing_time=processing_time,
            fusion_description=f"LLM merged {len(whisper_transcript)} + {len(bangla_transcript)} chars in {processing_time:.1f}s",
            technical_terms_preserved=preserved,
        )


# ============================================================================
# LIGHTWEIGHT VERSION (No LLM, just smart fallback)
# ============================================================================

class DualASRFusionLLMLite:
    """
    Lightweight version that prepares content for existing LLM step.
    
    Instead of running a separate LLM call, this packages both
    transcripts for the summarization LLM to handle.
    """
    
    def __init__(self):
        self.technical_terms = {
            'class', 'object', 'method', 'function', 'variable', 'array',
            'string', 'integer', 'boolean', 'public', 'private', 'static',
            'void', 'return', 'import', 'java', 'python', 'programming',
        }
    
    def fuse(
        self,
        whisper_transcript: str,
        bangla_transcript: str,
    ) -> LLMFusionResult:
        """
        Create a structured fusion for the summarization LLM.
        
        Instead of merging here, we format both transcripts
        so the LLM summarizer can use both sources.
        """
        # Count Bengali characters
        bengali_chars = len(re.findall(r'[\u0980-\u09FF]', bangla_transcript))
        bengali_ratio = bengali_chars / max(1, len(bangla_transcript))
        
        # Build structured output
        if bengali_ratio > 0.3:
            # Significant Bengali content - include both
            fused = f"""[WHISPER - English/Romanized]:
{whisper_transcript}

[BANGLA ASR - Bengali Reference]:
{bangla_transcript[:2000]}{"..." if len(bangla_transcript) > 2000 else ""}"""
            description = f"Structured: Whisper primary + Bengali reference ({bengali_ratio:.0%} Bengali)"
        else:
            # Mostly English/transliterated - use Whisper
            fused = whisper_transcript
            description = "Whisper only (BanglaASR not useful)"
        
        return LLMFusionResult(
            fused_transcript=fused,
            whisper_input=whisper_transcript,
            bangla_input=bangla_transcript,
            whisper_char_count=len(whisper_transcript),
            bangla_char_count=len(bangla_transcript),
            fused_char_count=len(fused),
            fusion_description=description,
            technical_terms_preserved=[],
        )


# ============================================================================
# TEST
# ============================================================================

if __name__ == "__main__":
    # Quick test with lightweight version (no model loading)
    whisper = """Hello everyone, I am Tohid. Today's tutorial will be Java 
    object-oriented programming. Class is a blueprint or template.
    We use class to create objects. Object has properties and behaviors."""
    
    bangla = """হ্যালো সবাইকে, আমি তওহিদ। আজকের টিউটোরিয়াল হলো জাভা 
    অবজেক্ট ওরিয়েন্টেড প্রোগ্রামিং। ক্লাস হলো ব্লুপ্রিন্ট বা টেমপ্লেট।"""
    
    print("=" * 70)
    print("LLM FUSION TEST (Lite Version)")
    print("=" * 70)
    
    # Test lite version
    fusion_lite = DualASRFusionLLMLite()
    result = fusion_lite.fuse(whisper, bangla)
    
    print(f"\nWhisper chars: {result.whisper_char_count}")
    print(f"BanglaASR chars: {result.bangla_char_count}")
    print(f"Fused chars: {result.fused_char_count}")
    print(f"Description: {result.fusion_description}")
    print()
    print("FUSED OUTPUT:")
    print("-" * 70)
    print(result.fused_transcript[:600])
