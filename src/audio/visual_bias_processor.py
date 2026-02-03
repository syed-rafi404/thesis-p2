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

import re
import torch
from typing import List, Set, Union, Optional, Tuple, Dict, Any
from dataclasses import dataclass
from transformers import LogitsProcessor, LogitsProcessorList, WhisperTokenizer


# =============================================================================
# ANTI-HALLUCINATION POST-PROCESSOR (Aggressive)
# =============================================================================

def detect_repetition_ratio(text: str, ngram_size: int = 3) -> float:
    """
    Calculate what percentage of n-grams are repeated.
    High ratio indicates hallucination.
    
    Args:
        text: Input text
        ngram_size: Size of n-grams to check
        
    Returns:
        Ratio of repeated n-grams (0.0 = no repeats, 1.0 = all repeats)
    """
    words = text.lower().split()
    if len(words) < ngram_size * 2:
        return 0.0
    
    ngrams = []
    for i in range(len(words) - ngram_size + 1):
        ngrams.append(tuple(words[i:i + ngram_size]))
    
    if not ngrams:
        return 0.0
    
    unique_ngrams = set(ngrams)
    repetition_ratio = 1.0 - (len(unique_ngrams) / len(ngrams))
    return repetition_ratio


def remove_repetitions(text: str, max_repeats: int = 3) -> str:
    """
    Remove excessive word/phrase repetitions from transcript.
    
    This is a post-processing step to clean up Whisper hallucinations
    where phrases like "Student Student Student..." repeat many times.
    
    Args:
        text: The raw transcript text
        max_repeats: Maximum allowed consecutive repetitions (default: 3)
        
    Returns:
        Cleaned text with repetitions reduced to max_repeats
        
    Example:
        >>> remove_repetitions("Hello. Student. Student. Student. Student. Student. Bye.")
        'Hello. Student. Student. Student. Bye.'
    """
    if not text or max_repeats < 1:
        return text
    
    words = text.split()
    if len(words) < 2:
        return text
    
    cleaned = []
    repeat_count = 1
    
    for i, word in enumerate(words):
        if i == 0:
            cleaned.append(word)
            continue
            
        # Check if current word matches previous (case-insensitive)
        if word.lower().strip('.,!?;:') == words[i-1].lower().strip('.,!?;:'):
            repeat_count += 1
            if repeat_count <= max_repeats:
                cleaned.append(word)
            # Skip if exceeds max_repeats
        else:
            repeat_count = 1
            cleaned.append(word)
    
    return ' '.join(cleaned)


def remove_phrase_repetitions(text: str, min_phrase_len: int = 2, max_phrase_len: int = 15, max_repeats: int = 2) -> str:
    """
    Remove repeated phrases (multiple consecutive words) from transcript.
    Uses a safe word-based algorithm instead of regex to avoid catastrophic backtracking.
    
    Handles patterns like:
    - "This is the design. This is the design. This is the design."
    - "The course of the course of the course of the course"
    
    Args:
        text: The raw transcript text
        min_phrase_len: Minimum phrase length in words to detect
        max_phrase_len: Maximum phrase length in words
        max_repeats: Maximum allowed consecutive phrase repetitions
        
    Returns:
        Cleaned text with phrase repetitions removed
    """
    if not text or len(text.split()) < min_phrase_len * 2:
        return text
    
    words = text.split()
    result = []
    i = 0
    
    while i < len(words):
        found_repeat = False
        
        # Try phrase lengths from max to min (longer phrases first)
        for phrase_len in range(min(max_phrase_len, (len(words) - i) // 2), min_phrase_len - 1, -1):
            if i + phrase_len * 2 > len(words):
                continue
                
            # Extract potential phrase
            phrase = words[i:i + phrase_len]
            phrase_lower = [w.lower().strip('.,!?;:') for w in phrase]
            
            # Count consecutive repetitions
            repeat_count = 1
            j = i + phrase_len
            
            while j + phrase_len <= len(words):
                next_phrase = [w.lower().strip('.,!?;:') for w in words[j:j + phrase_len]]
                if next_phrase == phrase_lower:
                    repeat_count += 1
                    j += phrase_len
                else:
                    break
            
            # If we found 3+ repetitions, keep only max_repeats
            if repeat_count >= 3:
                for _ in range(max_repeats):
                    result.extend(phrase)
                i = j  # Skip past all repetitions
                found_repeat = True
                break
        
        if not found_repeat:
            result.append(words[i])
            i += 1
    
    return ' '.join(result)


def remove_hyphenated_repetitions(text: str, max_repeats: int = 2) -> str:
    """
    Remove hyphenated word repetitions like "class-class-class-class".
    
    Args:
        text: Input text
        max_repeats: Max repetitions to keep
        
    Returns:
        Cleaned text
    """
    import re
    
    def replace_hyphen_repeats(match):
        full = match.group(0)
        parts = full.split('-')
        if len(parts) <= max_repeats:
            return full
        # Check if all parts are the same word
        unique = set(p.lower() for p in parts if p)
        if len(unique) == 1:
            return '-'.join(parts[:max_repeats])
        return full
    
    # Match word-word-word-... patterns
    pattern = r'\b(\w+(?:-\w+){2,})\b'
    return re.sub(pattern, replace_hyphen_repeats, text)


def remove_ngram_loops(text: str, ngram_sizes: list = [3, 4, 5, 6], max_repeats: int = 2) -> str:
    """
    Detect and remove n-gram based loops like "of the course of the course of the course".
    
    This catches overlapping repetition patterns that phrase-based detection misses.
    
    Args:
        text: Input text
        ngram_sizes: List of n-gram sizes to check
        max_repeats: Maximum repetitions to keep
        
    Returns:
        Cleaned text
    """
    words = text.split()
    if len(words) < 10:
        return text
    
    for ngram_size in sorted(ngram_sizes, reverse=True):  # Start with larger n-grams
        i = 0
        result = []
        
        while i < len(words):
            if i + ngram_size > len(words):
                result.extend(words[i:])
                break
            
            # Get current n-gram
            ngram = tuple(w.lower().strip('.,!?;:') for w in words[i:i + ngram_size])
            
            # Count how many times this n-gram repeats starting from position i
            repeat_count = 0
            j = i
            while j + ngram_size <= len(words):
                test_ngram = tuple(w.lower().strip('.,!?;:') for w in words[j:j + ngram_size])
                if test_ngram == ngram:
                    repeat_count += 1
                    j += ngram_size
                else:
                    break
            
            if repeat_count >= 3:
                # Keep only max_repeats worth
                for _ in range(min(max_repeats, repeat_count)):
                    result.extend(words[i:i + ngram_size])
                i = j
            else:
                result.append(words[i])
                i += 1
        
        words = result
    
    return ' '.join(words)


def clean_transcript(text: str, max_word_repeats: int = 2, max_phrase_repeats: int = 1) -> str:
    """
    Full transcript cleaning pipeline for Whisper hallucination removal.
    
    AGGRESSIVE cleaning to handle severe hallucinations like:
    - "the course of the course of the course of the course" (100+ times)
    - "design design design design design"
    - "class-class-class-class-class"
    
    Applies multiple passes:
    1. Hyphenated repetition removal
    2. N-gram loop detection
    3. Phrase-level repetition removal
    4. Word-level repetition removal
    5. Final n-gram cleanup
    
    Args:
        text: Raw transcript from Whisper
        max_word_repeats: Max consecutive identical words (default: 2)
        max_phrase_repeats: Max consecutive identical phrases (default: 1)
        
    Returns:
        Cleaned transcript
    """
    if not text or len(text) < 20:
        return text
    
    # Check if this text is heavily hallucinated
    initial_ratio = detect_repetition_ratio(text, ngram_size=3)
    
    # Step 0: Remove hyphenated repetitions (e.g., "class-class-class")
    text = remove_hyphenated_repetitions(text, max_repeats=max_word_repeats)
    
    # Step 1: Remove n-gram loops (catches "of the course of the course" patterns)
    text = remove_ngram_loops(text, ngram_sizes=[3, 4, 5, 6, 7, 8], max_repeats=max_phrase_repeats)
    
    # Step 2: Remove phrase repetitions
    text = remove_phrase_repetitions(text, min_phrase_len=2, max_phrase_len=15, max_repeats=max_phrase_repeats)
    
    # Step 3: Remove word repetitions
    text = remove_repetitions(text, max_repeats=max_word_repeats)
    
    # Step 4: Second pass of n-gram removal (catches any remaining loops)
    text = remove_ngram_loops(text, ngram_sizes=[2, 3, 4], max_repeats=max_phrase_repeats)
    
    # Step 5: Final word-level cleanup
    text = remove_repetitions(text, max_repeats=max_word_repeats)
    
    return text.strip()


# =============================================================================
# KEYWORD CONFIDENCE FILTERING (NOVELTY IMPROVEMENT)
# =============================================================================

@dataclass
class FilteredKeyword:
    """A keyword with confidence score for filtering."""
    keyword: str
    confidence: float
    occurrences: int = 1  # How many frames this keyword appeared in
    char_length: int = 0
    is_technical: bool = False
    

def filter_keywords_for_bias(
    keywords: List[str],
    min_length: int = 3,
    min_occurrences: int = 1,
    exclude_single_chars: bool = True,
    technical_terms_boost: bool = True,
) -> Tuple[List[str], Dict[str, Any]]:
    """
    Filter and score visual keywords before applying ASR bias.
    
    NOVELTY IMPROVEMENT: Addresses inconsistent visual bias results by:
    1. Removing very short keywords (< 3 chars) that cause false positives
    2. Boosting keywords that appear across multiple frames (more reliable)
    3. Prioritizing known technical terms
    4. Filtering out common noise words
    
    Problem Solved:
    - Visual bias was hurting 3/5 videos because it over-inserted keywords
    - Short keywords like "i", "a", "is" were biasing wrong tokens
    - Keywords from one frame were applied to entire audio inappropriately
    
    Args:
        keywords: Raw list of keywords from VLM extraction
        min_length: Minimum character length (default: 3)
        min_occurrences: Minimum frame occurrences for inclusion (default: 1)
        exclude_single_chars: Remove single character keywords (default: True)
        technical_terms_boost: Give higher confidence to known technical terms (default: True)
        
    Returns:
        Tuple of (filtered_keywords, filter_stats)
        
    Example:
        >>> raw = ["Class", "Object", "i", "a", "OOP", "polymorphism", "is"]
        >>> filtered, stats = filter_keywords_for_bias(raw)
        >>> print(filtered)  # ['Class', 'Object', 'OOP', 'polymorphism']
        >>> print(stats)     # {'removed': 3, 'kept': 4, 'reason': {...}}
    """
    # Known technical terms (high confidence)
    TECHNICAL_TERMS = {
        'class', 'object', 'method', 'function', 'variable', 'array',
        'string', 'integer', 'boolean', 'public', 'private', 'static',
        'void', 'return', 'import', 'java', 'python', 'code', 'compile',
        'inheritance', 'polymorphism', 'encapsulation', 'abstraction',
        'constructor', 'instance', 'blueprint', 'template', 'design',
        'interface', 'abstract', 'override', 'implements', 'extends',
        'algorithm', 'heuristic', 'dijkstra', 'loop', 'recursion',
        'attribute', 'property', 'behavior', 'parameter', 'argument',
        'oop', 'api', 'sdk', 'ide', 'jvm', 'jdk', 'jre',
    }
    
    # Noise words to always exclude
    NOISE_WORDS = {
        'a', 'an', 'the', 'is', 'are', 'was', 'were', 'be', 'been',
        'to', 'of', 'and', 'or', 'in', 'on', 'at', 'for', 'with',
        'this', 'that', 'it', 'we', 'you', 'i', 'so', 'if', 'but',
        'can', 'will', 'just', 'now', 'then', 'here', 'there',
        'what', 'when', 'where', 'how', 'why', 'who', 'which',
        'ok', 'okay', 'yes', 'no', 'um', 'uh', 'ah', 'oh',
        # File system / UI noise
        'users', 'desktop', 'documents', 'downloads', 'file', 'folder',
        'left', 'right', 'side', 'screen', 'computer', 'taw', 'tawhid',
        # OCR noise
        'notes', 'whiteboard', 'diagram', 'text', 'additional', 'handwritten',
        'console', 'output', 'editor', 'compilation', 'snippets',
        'initially', 'however', 'welcome', 'working', 'error',
        # Location noise  
        'dhaka', 'ctg', 'ctg2', 'ctgz', 'cse',
    }
    
    # Count occurrences across the keyword list
    from collections import Counter
    keyword_counts = Counter(kw.lower().strip() for kw in keywords if kw.strip())
    
    filtered = []
    removed = {'too_short': [], 'single_char': [], 'noise': [], 'low_occurrence': [], 'malformed': []}
    kept_with_scores = []
    
    # Process unique keywords
    seen = set()
    for kw in keywords:
        kw_clean = kw.strip()
        kw_lower = kw_clean.lower()
        
        # Skip duplicates
        if kw_lower in seen:
            continue
        seen.add(kw_lower)
        
        # Skip empty
        if not kw_clean:
            continue
        
        # Filter: Contains newlines or tabs (malformed VLM output)
        if '\n' in kw_clean or '\t' in kw_clean or '\r' in kw_clean:
            removed['malformed'].append(kw_clean[:30] + '...' if len(kw_clean) > 30 else kw_clean)
            continue
        
        # Filter: Too many words (probably a phrase/sentence, not a keyword)
        if len(kw_clean.split()) > 5:
            removed['malformed'].append(kw_clean[:30] + '...')
            continue
        
        # Filter: Single characters
        if exclude_single_chars and len(kw_clean) == 1:
            removed['single_char'].append(kw_clean)
            continue
        
        # Filter: Too short
        if len(kw_clean) < min_length:
            removed['too_short'].append(kw_clean)
            continue
        
        # Filter: Noise words (check each word in multi-word keywords)
        words_in_kw = kw_lower.split()
        if len(words_in_kw) == 1 and kw_lower in NOISE_WORDS:
            removed['noise'].append(kw_clean)
            continue
        
        # Get occurrence count
        occurrences = keyword_counts.get(kw_lower, 1)
        
        # Filter: Low occurrence (if threshold > 1)
        if occurrences < min_occurrences:
            removed['low_occurrence'].append(kw_clean)
            continue
        
        # Calculate confidence score
        confidence = 0.5  # Base confidence
        
        # Boost for technical terms
        if technical_terms_boost and kw_lower in TECHNICAL_TERMS:
            confidence += 0.3
        
        # Boost for longer keywords (more specific)
        if len(kw_clean) >= 6:
            confidence += 0.1
        if len(kw_clean) >= 10:
            confidence += 0.1
        
        # Boost for multi-frame occurrence
        if occurrences >= 2:
            confidence += 0.1 * min(occurrences - 1, 3)  # Max +0.3 for 4+ occurrences
        
        confidence = min(confidence, 1.0)  # Cap at 1.0
        
        filtered.append(kw_clean)
        kept_with_scores.append({
            'keyword': kw_clean,
            'confidence': confidence,
            'occurrences': occurrences,
            'is_technical': kw_lower in TECHNICAL_TERMS,
        })
    
    # Sort by confidence (highest first)
    kept_with_scores.sort(key=lambda x: x['confidence'], reverse=True)
    filtered = [k['keyword'] for k in kept_with_scores]
    
    # Build stats
    stats = {
        'original_count': len(keywords),
        'filtered_count': len(filtered),
        'removed_count': sum(len(v) for v in removed.values()),
        'removed': removed,
        'keyword_scores': kept_with_scores[:20],  # Top 20 for logging
        'top_keywords': filtered[:10],  # Quick view of top 10
    }
    
    return filtered, stats


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
# TEMPORAL VISUAL BIAS PROCESSOR (NOVELTY)
# =============================================================================

class TemporalVisualBiasProcessor(LogitsProcessor):
    """
    NOVELTY: Temporally-Aligned Visual Bias Processor.
    
    This processor applies DIFFERENT visual biases at DIFFERENT timestamps
    during Whisper's generation. Instead of biasing the entire audio with
    all keywords, each audio segment gets only the keywords that are
    temporally relevant (visible on screen at that time).
    
    Key Innovation:
    - Frame at 0:30 has keywords ["Object", "Class"]
    - Frame at 1:00 has keywords ["Method", "Function"]  
    - Audio segment 0:00-1:00 gets bias for ["Object", "Class"]
    - Audio segment 1:00-2:00 gets bias for ["Method", "Function"]
    
    This prevents false biasing where a keyword from minute 10 affects
    transcription at minute 1.
    
    Args:
        tokenizer: Whisper tokenizer
        temporal_context: TemporalVisualContext with timestamp-to-keywords mapping
        bias_value: Base bias strength
        audio_duration: Total audio duration in seconds
        
    Note:
        Since Whisper generates tokens autoregressively, we estimate the
        current timestamp based on the number of tokens generated so far.
    """
    
    def __init__(
        self,
        tokenizer,
        temporal_context,
        bias_value: float = 1.5,
        audio_duration: float = 600.0,  # 10 min default
    ):
        from src.fusion.temporal_context import TemporalVisualContext
        
        self.tokenizer = tokenizer
        self.temporal_context = temporal_context
        self.bias_value = bias_value
        self.audio_duration = audio_duration
        
        # Pre-compute token IDs for each frame's keywords
        self._frame_token_cache = {}
        for fk in temporal_context.frame_keywords:
            token_ids = get_tokens_for_words(tokenizer, fk.keywords)
            self._frame_token_cache[fk.timestamp_sec] = set(token_ids)
        
        # Track generation progress
        self._prev_input_len = 0
        self._current_timestamp = 0.0
        
        # Whisper generates ~2 tokens per second on average
        self.tokens_per_second = 2.0
        
        # Cache for current bias tensor
        self._current_bias_tensor = None
        self._current_keywords = None
    
    def _estimate_timestamp(self, input_ids_len: int) -> float:
        """Estimate current audio timestamp from token count."""
        # Simple linear estimation: ~2 tokens per second of audio
        # More sophisticated: could use Whisper's timestamp tokens
        estimated_time = input_ids_len / self.tokens_per_second
        return min(estimated_time, self.audio_duration)
    
    def _get_keywords_for_timestamp(self, timestamp: float) -> List[str]:
        """Get relevant keywords for current timestamp."""
        return self.temporal_context.get_keywords_for_timestamp(timestamp)
    
    def _get_token_ids_for_timestamp(self, timestamp: float) -> set:
        """Get token IDs to bias for current timestamp."""
        token_ids = set()
        
        for fk in self.temporal_context.frame_keywords:
            window_start = fk.timestamp_sec - self.temporal_context.window_before_sec
            window_end = fk.timestamp_sec + self.temporal_context.window_after_sec
            
            if window_start <= timestamp <= window_end:
                if fk.timestamp_sec in self._frame_token_cache:
                    token_ids.update(self._frame_token_cache[fk.timestamp_sec])
        
        return token_ids
    
    def __call__(
        self,
        input_ids: torch.LongTensor,
        scores: torch.FloatTensor
    ) -> torch.FloatTensor:
        """Apply temporal visual bias to scores."""
        
        # Estimate current timestamp
        current_len = input_ids.shape[-1]
        current_timestamp = self._estimate_timestamp(current_len)
        
        # Only recompute bias if we've moved to a new time window (every ~5 seconds)
        # This is an optimization to avoid recomputing every step
        time_changed = abs(current_timestamp - self._current_timestamp) > 5.0
        
        if time_changed or self._current_bias_tensor is None:
            self._current_timestamp = current_timestamp
            
            # Get token IDs for current timestamp
            token_ids = self._get_token_ids_for_timestamp(current_timestamp)
            
            # Create bias tensor
            vocab_size = scores.shape[-1]
            self._current_bias_tensor = torch.zeros(vocab_size, device=scores.device)
            
            for token_id in token_ids:
                if 0 <= token_id < vocab_size:
                    self._current_bias_tensor[token_id] = self.bias_value
        
        # Ensure tensor is on correct device
        if self._current_bias_tensor.device != scores.device:
            self._current_bias_tensor = self._current_bias_tensor.to(scores.device)
        
        # Apply bias
        scores = scores + self._current_bias_tensor
        
        return scores
    
    def __repr__(self) -> str:
        return (
            f"TemporalVisualBiasProcessor("
            f"frames={len(self.temporal_context)}, "
            f"window=±{self.temporal_context.window_before_sec}s, "
            f"bias={self.bias_value})"
        )


def create_temporal_visual_bias_processor(
    tokenizer,
    temporal_context,
    bias_value: float = 1.5,
    audio_duration: float = 600.0,
) -> TemporalVisualBiasProcessor:
    """
    Factory function to create a TemporalVisualBiasProcessor.
    
    NOVELTY: This creates a processor that applies time-aligned visual bias.
    
    Args:
        tokenizer: Whisper tokenizer
        temporal_context: TemporalVisualContext with timestamp-to-keywords mapping
        bias_value: Bias strength (default 1.5, lower than global bias)
        audio_duration: Total audio duration in seconds
        
    Returns:
        Configured TemporalVisualBiasProcessor
        
    Example:
        >>> from src.fusion.temporal_context import TemporalVisualContext
        >>> ctx = TemporalVisualContext()
        >>> ctx.add_frame_keywords("frame_001.jpg", 30.0, ["Object", "Class"])
        >>> ctx.add_frame_keywords("frame_002.jpg", 60.0, ["Method", "Function"])
        >>> 
        >>> processor = create_temporal_visual_bias_processor(
        ...     tokenizer=tokenizer,
        ...     temporal_context=ctx,
        ...     audio_duration=120.0
        ... )
    """
    return TemporalVisualBiasProcessor(
        tokenizer=tokenizer,
        temporal_context=temporal_context,
        bias_value=bias_value,
        audio_duration=audio_duration,
    )


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
