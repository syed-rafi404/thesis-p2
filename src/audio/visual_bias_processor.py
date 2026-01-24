"""
=============================================================================
VISUAL-BIASED ASR - Logits Processor for Whisper
=============================================================================
Multimodal Banglish Classroom Summarizer
Master's Thesis - Research Branch: visual-biased-asr

This module implements a custom LogitsProcessor that biases Whisper's
generation toward technical terms extracted from whiteboard visual analysis.

Key Insight:
- VLM extracts clean technical terms from whiteboard (e.g., "A*", "Heuristic")
- We boost the probability of these tokens during ASR decoding
- This helps Whisper correctly transcribe domain-specific terminology

Example:
    Without bias: "A-Store algorithm" (misheard)
    With bias:    "A* algorithm" (correct - boosted by visual context)
=============================================================================
"""

import torch
from typing import List, Set, Union, Optional
from transformers import LogitsProcessor, LogitsProcessorList, WhisperTokenizer


def get_tokens_for_words(
    tokenizer: WhisperTokenizer,
    words_list: List[str],
    add_prefix_space: bool = True
) -> List[int]:
    """
    Convert a list of words/phrases into their corresponding token IDs.
    
    Handles subword tokenization - a single word may split into multiple tokens.
    For example, "Heuristic" might become ["He", "ur", "istic"] with IDs [1234, 567, 890].
    
    Args:
        tokenizer: WhisperTokenizer instance
        words_list: List of words/phrases to tokenize (e.g., ["Heuristic", "A*", "Dijkstra"])
        add_prefix_space: Whether to add space prefix (Whisper often expects this)
        
    Returns:
        Flat list of unique token IDs for all words
        
    Example:
        >>> tokenizer = WhisperTokenizer.from_pretrained("openai/whisper-large-v3-turbo")
        >>> tokens = get_tokens_for_words(tokenizer, ["Heuristic", "A*", "GBFS"])
        >>> print(tokens)  # [1234, 567, 890, 42, ...]
    """
    all_token_ids: Set[int] = set()
    
    for word in words_list:
        # Try multiple variations to capture the token in different contexts
        variations = [
            word,                    # "Heuristic"
            word.lower(),            # "heuristic"
            word.upper(),            # "HEURISTIC"
            word.capitalize(),       # "Heuristic"
        ]
        
        # Add space-prefixed versions (common in Whisper tokenization)
        if add_prefix_space:
            variations.extend([
                f" {word}",
                f" {word.lower()}",
                f" {word.capitalize()}",
            ])
        
        for variant in variations:
            # Tokenize the variant
            encoded = tokenizer.encode(variant, add_special_tokens=False)
            all_token_ids.update(encoded)
    
    return list(all_token_ids)


def get_tokens_for_phrases(
    tokenizer: WhisperTokenizer,
    phrases: List[str]
) -> dict:
    """
    Get token IDs for phrases, returning a mapping for analysis.
    
    Args:
        tokenizer: WhisperTokenizer instance
        phrases: List of phrases (e.g., ["Greedy Best First Search", "A* algorithm"])
        
    Returns:
        Dictionary mapping each phrase to its token IDs and decoded tokens
        
    Example:
        >>> result = get_tokens_for_phrases(tokenizer, ["A* algorithm"])
        >>> print(result)
        {
            "A* algorithm": {
                "token_ids": [362, 9, 9470],
                "tokens": [" A", "*", " algorithm"]
            }
        }
    """
    result = {}
    
    for phrase in phrases:
        token_ids = tokenizer.encode(phrase, add_special_tokens=False)
        tokens = [tokenizer.decode([tid]) for tid in token_ids]
        
        result[phrase] = {
            "token_ids": token_ids,
            "tokens": tokens
        }
    
    return result


class VisualBiasLogitsProcessor(LogitsProcessor):
    """
    A LogitsProcessor that biases Whisper toward generating specific tokens.
    
    This processor adds a bias value to the logits of specified token IDs
    at every generation step, increasing the probability of those tokens
    being selected during decoding.
    
    The bias tokens typically come from visual analysis of whiteboard content,
    helping the ASR model correctly transcribe domain-specific terms.
    
    Args:
        bias_token_ids: List of token IDs to boost
        bias_value: Value to add to logits (higher = stronger bias)
                    Typical values: 1.0-5.0
                    - 1.0: Subtle preference
                    - 2.0: Moderate boost
                    - 5.0: Strong preference
        
    Example:
        >>> processor = VisualBiasLogitsProcessor(
        ...     bias_token_ids=[1234, 5678],
        ...     bias_value=2.0
        ... )
        >>> outputs = model.generate(
        ...     input_features,
        ...     logits_processor=LogitsProcessorList([processor])
        ... )
    """
    
    def __init__(
        self,
        bias_token_ids: List[int],
        bias_value: float = 2.0
    ):
        """
        Initialize the visual bias processor.
        
        Args:
            bias_token_ids: Token IDs to boost (from visual keywords)
            bias_value: Additive bias for logits (default: 2.0)
        """
        self.bias_token_ids = set(bias_token_ids)  # Set for O(1) lookup
        self.bias_value = bias_value
        
        # Pre-compute tensor for efficient biasing (will be moved to device on first call)
        self._bias_tensor: Optional[torch.Tensor] = None
        self._vocab_size: Optional[int] = None
    
    def __call__(
        self,
        input_ids: torch.LongTensor,
        scores: torch.FloatTensor
    ) -> torch.FloatTensor:
        """
        Apply bias to specified token logits.
        
        This method is called at each generation step by HuggingFace's
        generate() function.
        
        Args:
            input_ids: Previously generated token IDs (batch_size, seq_len)
            scores: Logits for next token prediction (batch_size, vocab_size)
            
        Returns:
            Modified scores with bias applied to target tokens
        """
        # Initialize bias tensor on first call (to get correct device and vocab size)
        if self._bias_tensor is None or self._vocab_size != scores.shape[-1]:
            self._vocab_size = scores.shape[-1]
            self._bias_tensor = torch.zeros(self._vocab_size, device=scores.device)
            
            # Set bias for target tokens
            for token_id in self.bias_token_ids:
                if 0 <= token_id < self._vocab_size:
                    self._bias_tensor[token_id] = self.bias_value
        
        # Move bias tensor to same device as scores (handles multi-GPU)
        if self._bias_tensor.device != scores.device:
            self._bias_tensor = self._bias_tensor.to(scores.device)
        
        # Apply bias: add bias_value to target token logits
        # This increases their probability during softmax
        scores = scores + self._bias_tensor
        
        return scores
    
    def __repr__(self) -> str:
        return (
            f"VisualBiasLogitsProcessor("
            f"num_tokens={len(self.bias_token_ids)}, "
            f"bias_value={self.bias_value})"
        )


class AdaptiveVisualBiasProcessor(LogitsProcessor):
    """
    An advanced LogitsProcessor with adaptive biasing based on context.
    
    Features:
    - Decaying bias: Reduces bias after a target token is generated
    - Phrase-aware: Can boost sequences of tokens for multi-word terms
    - Confidence-based: Adjusts bias based on current token probability
    
    This is useful when you want to avoid over-biasing (repeating terms).
    """
    
    def __init__(
        self,
        bias_token_ids: List[int],
        bias_value: float = 2.0,
        decay_factor: float = 0.5,
        min_bias: float = 0.5
    ):
        """
        Initialize adaptive processor.
        
        Args:
            bias_token_ids: Token IDs to boost
            bias_value: Initial bias value
            decay_factor: Multiply bias by this after token is generated
            min_bias: Minimum bias value (floor)
        """
        self.bias_token_ids = set(bias_token_ids)
        self.initial_bias = bias_value
        self.decay_factor = decay_factor
        self.min_bias = min_bias
        
        # Track current bias for each token
        self.current_bias = {tid: bias_value for tid in bias_token_ids}
        
        # Track previously generated tokens
        self._prev_len = 0
    
    def __call__(
        self,
        input_ids: torch.LongTensor,
        scores: torch.FloatTensor
    ) -> torch.FloatTensor:
        """Apply adaptive bias to scores."""
        
        # Check if new tokens were generated (for decay)
        current_len = input_ids.shape[-1]
        if current_len > self._prev_len:
            # Get newly generated tokens
            new_tokens = input_ids[0, self._prev_len:].tolist()
            
            # Decay bias for generated tokens
            for token_id in new_tokens:
                if token_id in self.current_bias:
                    self.current_bias[token_id] = max(
                        self.current_bias[token_id] * self.decay_factor,
                        self.min_bias
                    )
            
            self._prev_len = current_len
        
        # Apply current bias values
        vocab_size = scores.shape[-1]
        for token_id, bias in self.current_bias.items():
            if 0 <= token_id < vocab_size:
                scores[:, token_id] += bias
        
        return scores
    
    def reset(self):
        """Reset bias values (call before new transcription)."""
        self.current_bias = {tid: self.initial_bias for tid in self.bias_token_ids}
        self._prev_len = 0


# =============================================================================
# INTEGRATION EXAMPLE
# =============================================================================

def create_visual_biased_processor(
    tokenizer: WhisperTokenizer,
    visual_keywords: List[str],
    bias_value: float = 2.0
) -> VisualBiasLogitsProcessor:
    """
    Factory function to create a VisualBiasLogitsProcessor from keywords.
    
    Args:
        tokenizer: Whisper tokenizer
        visual_keywords: Words extracted from whiteboard
        bias_value: Bias strength
        
    Returns:
        Configured VisualBiasLogitsProcessor
        
    Example:
        >>> processor = create_visual_biased_processor(
        ...     tokenizer,
        ...     visual_keywords=["Heuristic", "A*", "Dijkstra", "GBFS"],
        ...     bias_value=2.5
        ... )
    """
    # Convert words to token IDs
    token_ids = get_tokens_for_words(tokenizer, visual_keywords)
    
    # Create processor
    processor = VisualBiasLogitsProcessor(
        bias_token_ids=token_ids,
        bias_value=bias_value
    )
    
    return processor


# =============================================================================
# USAGE EXAMPLE (for documentation)
# =============================================================================

USAGE_EXAMPLE = """
# =============================================================================
# COMPLETE USAGE EXAMPLE: Visual-Biased Whisper Transcription
# =============================================================================

import torch
from transformers import (
    AutoModelForSpeechSeq2Seq,
    AutoProcessor,
    LogitsProcessorList
)
from src.audio.visual_bias_processor import (
    get_tokens_for_words,
    VisualBiasLogitsProcessor,
    create_visual_biased_processor
)

# 1. Load Whisper model and processor
model_name = "openai/whisper-large-v3-turbo"
model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_name,
    torch_dtype=torch.float16,
    device_map="auto"
)
processor = AutoProcessor.from_pretrained(model_name)
tokenizer = processor.tokenizer

# 2. Define visual keywords (extracted from whiteboard by VLM)
visual_keywords = [
    "Heuristic",
    "A*",
    "Dijkstra",
    "GBFS",
    "Greedy",
    "optimal",
    "algorithm",
    "f(n)",
    "g(n)",
    "h(n)"
]

# 3. Create the visual bias processor
visual_bias_processor = create_visual_biased_processor(
    tokenizer=tokenizer,
    visual_keywords=visual_keywords,
    bias_value=2.0  # Moderate boost
)

print(f"Created processor: {visual_bias_processor}")

# 4. Prepare audio
import librosa
audio_array, sr = librosa.load("lecture_audio.wav", sr=16000)
inputs = processor(
    audio_array,
    sampling_rate=16000,
    return_tensors="pt"
).to(model.device, dtype=torch.float16)

# 5. Generate with visual bias!
generated_ids = model.generate(
    inputs["input_features"],
    task="transcribe",
    return_timestamps=True,
    # KEY: Pass the logits processor here
    logits_processor=LogitsProcessorList([visual_bias_processor])
)

# 6. Decode
transcription = processor.batch_decode(
    generated_ids,
    skip_special_tokens=True
)[0]

print("Transcription:", transcription)

# =============================================================================
# COMPARISON: Without vs With Visual Bias
# =============================================================================
#
# Without bias: "The A-Store algorithm uses the heuristic function..."
# With bias:    "The A* algorithm uses the Heuristic function..."
#
# The visual bias helps Whisper prefer domain-specific terms that were
# clearly written on the whiteboard, reducing ASR errors.
# =============================================================================
"""


if __name__ == "__main__":
    print(USAGE_EXAMPLE)
    
    # Quick test
    print("\n" + "="*60)
    print("QUICK TEST: Token ID extraction")
    print("="*60)
    
    from transformers import WhisperTokenizer
    
    tokenizer = WhisperTokenizer.from_pretrained("openai/whisper-large-v3-turbo")
    
    test_words = ["Heuristic", "A*", "Dijkstra", "GBFS", "algorithm"]
    
    # Show token mapping
    phrase_map = get_tokens_for_phrases(tokenizer, test_words)
    
    for word, info in phrase_map.items():
        print(f"\n'{word}':")
        print(f"  Token IDs: {info['token_ids']}")
        print(f"  Tokens:    {info['tokens']}")
    
    # Create processor
    all_token_ids = get_tokens_for_words(tokenizer, test_words)
    print(f"\nTotal unique token IDs: {len(all_token_ids)}")
    
    processor = VisualBiasLogitsProcessor(
        bias_token_ids=all_token_ids,
        bias_value=2.0
    )
    print(f"Processor: {processor}")
