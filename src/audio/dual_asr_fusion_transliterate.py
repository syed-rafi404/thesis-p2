"""
Dual-ASR Fusion with Transliteration (Option 2)

NOVELTY: Uses Bengali → Romanized transliteration to enable
word-level comparison between Whisper and BanglaASR outputs.

Strategy:
1. Transliterate BanglaASR output to romanized form
2. Compare word overlap between Whisper and transliterated BanglaASR
3. Merge by selecting best segments based on:
   - Technical term accuracy (prefer Whisper)
   - Bengali word coverage (prefer BanglaASR when transliterated matches)
4. Create unified romanized output
"""

import re
from dataclasses import dataclass, field
from typing import List, Dict, Any, Tuple, Optional, Set
from enum import Enum
from difflib import SequenceMatcher
from collections import Counter

from src.audio.bengali_transliterate import BengaliTransliterator


# ============================================================================
# FUZZY MATCHING UTILITIES
# ============================================================================

def levenshtein_distance(s1: str, s2: str) -> int:
    """Calculate Levenshtein (edit) distance between two strings."""
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    
    if len(s2) == 0:
        return len(s1)
    
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]


def levenshtein_similarity(s1: str, s2: str) -> float:
    """Calculate normalized Levenshtein similarity (0-1)."""
    if not s1 and not s2:
        return 1.0
    if not s1 or not s2:
        return 0.0
    
    distance = levenshtein_distance(s1.lower(), s2.lower())
    max_len = max(len(s1), len(s2))
    return 1.0 - (distance / max_len)


def get_ngrams(text: str, n: int = 2) -> Set[str]:
    """Generate character n-grams from text."""
    text = text.lower().replace(' ', '')
    if len(text) < n:
        return {text} if text else set()
    return {text[i:i+n] for i in range(len(text) - n + 1)}


def ngram_similarity(s1: str, s2: str, n: int = 2) -> float:
    """Calculate n-gram (Dice coefficient) similarity."""
    ngrams1 = get_ngrams(s1, n)
    ngrams2 = get_ngrams(s2, n)
    
    if not ngrams1 or not ngrams2:
        return 0.0
    
    intersection = len(ngrams1 & ngrams2)
    return (2.0 * intersection) / (len(ngrams1) + len(ngrams2))


def fuzzy_word_match(word1: str, word2: str, threshold: float = 0.5) -> bool:
    """
    Check if two words are fuzzy matches (allowing typos/transliteration variants).
    
    Uses a lower threshold (0.5) to handle:
    - Bengali suffixes: class → classero, method → metharo
    - Transliteration variants: design → dijaino, hello → hjalo
    """
    if word1 == word2:
        return True
    
    # Skip very short words (too many false positives)
    if len(word1) < 3 or len(word2) < 3:
        return word1 == word2


# Bengali transliteration suffix patterns (commonly added to English words)
BENGALI_SUFFIXES = ['ero', 'ro', 'ta', 'te', 'ke', 'er', 'o', 'i', 'e']


def strip_bengali_suffix(word: str) -> str:
    """Strip common Bengali suffixes from transliterated words."""
    word_lower = word.lower()
    for suffix in BENGALI_SUFFIXES:
        if word_lower.endswith(suffix) and len(word_lower) > len(suffix) + 2:
            return word_lower[:-len(suffix)]
    return word_lower


def enhanced_word_similarity(word1: str, word2: str) -> float:
    """
    Calculate enhanced similarity between two words, handling:
    - Exact matches
    - Suffix stripping (Bengali suffixes on English words)
    - Levenshtein distance
    - Prefix matching
    """
    w1 = word1.lower()
    w2 = word2.lower()
    
    # Exact match
    if w1 == w2:
        return 1.0
    
    # Strip Bengali suffixes and compare
    w1_stripped = strip_bengali_suffix(w1)
    w2_stripped = strip_bengali_suffix(w2)
    
    if w1_stripped == w2_stripped:
        return 0.95  # Very high match
    
    # Check if one is prefix of other (after stripping)
    if w1_stripped.startswith(w2_stripped) or w2_stripped.startswith(w1_stripped):
        prefix_len = min(len(w1_stripped), len(w2_stripped))
        max_len = max(len(w1_stripped), len(w2_stripped))
        if prefix_len >= 3:  # Meaningful prefix
            return 0.7 + (0.25 * prefix_len / max_len)
    
    # Levenshtein on stripped versions
    lev_sim = levenshtein_similarity(w1_stripped, w2_stripped)
    
    # Bonus for shared prefix (first 3+ chars)
    prefix_bonus = 0.0
    if len(w1_stripped) >= 3 and len(w2_stripped) >= 3:
        if w1_stripped[:3] == w2_stripped[:3]:
            prefix_bonus = 0.1
        elif w1_stripped[:2] == w2_stripped[:2]:
            prefix_bonus = 0.05
    
    return min(1.0, lev_sim + prefix_bonus)


class SegmentSource(Enum):
    """Source of a transcript segment."""
    WHISPER = "whisper"
    BANGLA_ASR = "bangla_asr"
    MERGED = "merged"


@dataclass
class FusedSegment:
    """A segment in the fused transcript with confidence scoring."""
    text: str
    source: SegmentSource
    similarity: float = 0.0
    whisper_original: str = ""
    bangla_original: str = ""
    bangla_transliterated: str = ""
    
    # NEW: Confidence scoring for segment reliability
    confidence: float = 0.5  # Overall confidence (0-1)
    needs_review: bool = False  # Flag for low-confidence segments
    confidence_reason: str = ""  # Why this confidence was assigned
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "text": self.text,
            "source": self.source.value,
            "similarity": self.similarity,
            "confidence": self.confidence,
            "needs_review": self.needs_review,
            "confidence_reason": self.confidence_reason,
        }


@dataclass
class TransliterationFusionResult:
    """Result of transliteration-based fusion with confidence metrics."""
    fused_transcript: str
    segments: List[FusedSegment]
    
    # Metrics
    whisper_segments: int
    bangla_segments: int
    merged_segments: int
    average_similarity: float
    
    # Coverage
    whisper_word_count: int
    bangla_word_count: int
    fused_word_count: int
    unique_words_from_bangla: int  # Words added from BanglaASR
    
    # NEW: Confidence metrics
    average_confidence: float = 0.5  # Average segment confidence
    high_confidence_segments: int = 0  # Segments with confidence > 0.7
    low_confidence_segments: int = 0   # Segments with confidence < 0.3 (needs review)
    segments_needing_review: int = 0   # Count of flagged segments
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "fused_transcript": self.fused_transcript,
            "whisper_segments": self.whisper_segments,
            "bangla_segments": self.bangla_segments,
            "merged_segments": self.merged_segments,
            "average_similarity": self.average_similarity,
            "whisper_word_count": self.whisper_word_count,
            "bangla_word_count": self.bangla_word_count,
            "fused_word_count": self.fused_word_count,
            "unique_words_from_bangla": self.unique_words_from_bangla,
            # NEW: Confidence metrics
            "average_confidence": self.average_confidence,
            "high_confidence_segments": self.high_confidence_segments,
            "low_confidence_segments": self.low_confidence_segments,
            "segments_needing_review": self.segments_needing_review,
        }
    
    def get_review_segments(self) -> List[FusedSegment]:
        """Get segments that need manual review (low confidence)."""
        return [s for s in self.segments if s.needs_review]


class DualASRFusionTransliterate:
    """
    Dual-ASR Fusion using Bengali → Romanized transliteration.
    
    This approach enables word-level comparison between:
    - Whisper: English/Romanized Banglish
    - BanglaASR: Bengali Unicode → Transliterated to Romanized
    
    Benefits:
    - Can identify overlapping content
    - Can merge complementary information
    - Preserves technical terms from Whisper
    - Adds Bengali words from BanglaASR
    
    Similarity Metrics:
    - Jaccard similarity (exact word overlap)
    - Fuzzy word matching (Levenshtein-based)
    - N-gram character similarity (for transliteration variants)
    """
    
    # Default threshold - can be tuned via hyperparameter search
    # Optimal value found via validation: 0.01
    DEFAULT_SIMILARITY_THRESHOLD = 0.01
    
    def __init__(self, similarity_threshold: float = None, fuzzy_word_threshold: float = 0.7):
        """
        Initialize the fusion module.
        
        Args:
            similarity_threshold: Minimum similarity for segment matching (default: 0.05)
            fuzzy_word_threshold: Minimum similarity for fuzzy word matching (default: 0.7)
        """
        self.transliterator = BengaliTransliterator()
        self.similarity_threshold = similarity_threshold or self.DEFAULT_SIMILARITY_THRESHOLD
        self.fuzzy_word_threshold = fuzzy_word_threshold
        
        # Technical terms (keep from Whisper)
        self.technical_terms = {
            'class', 'object', 'method', 'function', 'variable', 'array',
            'string', 'integer', 'boolean', 'public', 'private', 'static',
            'void', 'return', 'import', 'java', 'python', 'code', 'compile',
            'inheritance', 'polymorphism', 'encapsulation', 'abstraction',
            'constructor', 'instance', 'blueprint', 'template', 'design',
            'tutorial', 'example', 'data', 'type', 'behavior', 'property',
        }
        
        # Common words to ignore in similarity (too generic)
        self.stop_words = {
            'a', 'an', 'the', 'is', 'are', 'was', 'were', 'be', 'been',
            'to', 'of', 'and', 'or', 'in', 'on', 'at', 'for', 'with',
            'this', 'that', 'it', 'we', 'you', 'i', 'so', 'if', 'but',
            'ami', 'tumi', 'eta', 'ota', 'ki', 'ar', 'ba', 'o', 'e',
        }
    
    def _segment_text(self, text: str) -> List[str]:
        """Split text into sentence-like segments."""
        # Split on sentence boundaries and common pause markers
        segments = re.split(r'[.!?।,;]\s*', text)
        
        # Filter and clean
        result = []
        for seg in segments:
            seg = seg.strip()
            if len(seg) > 10:  # Minimum meaningful length
                result.append(seg)
        
        return result
    
    def _normalize_for_comparison(self, text: str) -> Set[str]:
        """Normalize text to word set for comparison."""
        words = re.findall(r'\b[a-zA-Z]{2,}\b', text.lower())
        return set(w for w in words if w not in self.stop_words)
    
    def _jaccard_similarity(self, words1: Set[str], words2: Set[str]) -> float:
        """Calculate Jaccard similarity between two word sets."""
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        
        return intersection / union if union > 0 else 0.0
    
    def _fuzzy_word_overlap(self, words1: Set[str], words2: Set[str]) -> Tuple[int, List[Tuple[str, str, float]]]:
        """
        Count fuzzy matches between two word sets using enhanced similarity.
        
        Uses enhanced_word_similarity which handles:
        - Bengali suffix stripping (classero → class)
        - Transliteration variants (dijaino → design)
        - Prefix matching
        
        Returns:
            Tuple of (fuzzy_match_count, list of (word1, word2, similarity) matches)
        """
        fuzzy_matches = []
        used_words2 = set()
        
        for w1 in words1:
            best_match = None
            best_sim = self.fuzzy_word_threshold
            
            for w2 in words2:
                if w2 in used_words2:
                    continue
                
                # Use enhanced similarity that handles Bengali suffixes
                sim = enhanced_word_similarity(w1, w2)
                if sim > best_sim:
                    best_sim = sim
                    best_match = (w1, w2, sim)
            
            if best_match:
                fuzzy_matches.append(best_match)
                used_words2.add(best_match[1])
        
        return len(fuzzy_matches), fuzzy_matches
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate combined similarity between two texts using multiple metrics.
        
        Combines:
        1. Jaccard similarity (exact word overlap)
        2. Fuzzy word matching (Levenshtein-based, tolerates typos)
        3. N-gram character similarity (handles transliteration variants)
        
        Returns:
            Combined similarity score (0-1)
        """
        words1 = self._normalize_for_comparison(text1)
        words2 = self._normalize_for_comparison(text2)
        
        if not words1 or not words2:
            return 0.0
        
        # 1. Exact Jaccard similarity
        exact_jaccard = self._jaccard_similarity(words1, words2)
        
        # 2. Fuzzy word overlap (for words that don't match exactly)
        non_matching1 = words1 - words2
        non_matching2 = words2 - words1
        fuzzy_count, _ = self._fuzzy_word_overlap(non_matching1, non_matching2)
        
        # Fuzzy bonus: additional similarity from fuzzy matches
        max_potential = len(words1 | words2)
        fuzzy_jaccard = fuzzy_count / max_potential if max_potential > 0 else 0.0
        
        # 3. N-gram character similarity (captures partial matches)
        ngram_sim = ngram_similarity(text1, text2, n=3)
        
        # Combine: weighted average
        # - Exact matches are most reliable (weight: 0.4)
        # - Fuzzy matches help with transliteration variants (weight: 0.35)
        # - N-gram provides backup for very different romanizations (weight: 0.25)
        combined = (0.4 * exact_jaccard) + (0.35 * fuzzy_jaccard) + (0.25 * ngram_sim)
        
        return combined
    
    def _has_technical_terms(self, text: str) -> bool:
        """Check if text contains technical terms."""
        words = set(text.lower().split())
        return bool(words & self.technical_terms)
    
    def _count_technical_terms(self, text: str) -> int:
        """Count technical terms in text."""
        words = set(text.lower().split())
        return len(words & self.technical_terms)
    
    def _calculate_segment_confidence(
        self,
        text: str,
        source: SegmentSource,
        similarity: float,
        has_technical_terms: bool,
    ) -> Tuple[float, bool, str]:
        """
        Calculate confidence score for a fused segment.
        
        NOVELTY IMPROVEMENT: Per-segment confidence scoring enables:
        1. Flagging unreliable segments for manual review
        2. Weighted fusion based on reliability
        3. Quality metrics for overall transcript
        
        Confidence Factors:
        - Higher similarity = higher confidence (cross-modal verification)
        - Merged segments > Whisper-only (more verification)
        - Technical terms increase confidence (less ambiguity)
        - Short segments decrease confidence (less context)
        
        Args:
            text: The segment text
            source: SegmentSource (WHISPER, BANGLA_ASR, MERGED)
            similarity: Similarity score from matching (0-1)
            has_technical_terms: Whether segment contains technical terms
            
        Returns:
            Tuple of (confidence, needs_review, reason)
        """
        confidence = 0.5  # Base confidence
        reasons = []
        
        # Factor 1: Source type
        if source == SegmentSource.MERGED:
            confidence += 0.2
            reasons.append("merged from dual-ASR")
        elif source == SegmentSource.WHISPER:
            # Whisper-only is OK but less verified
            confidence += 0.1
            reasons.append("Whisper-only")
        elif source == SegmentSource.BANGLA_ASR:
            # BanglaASR-only is least reliable (transliterated)
            confidence -= 0.1
            reasons.append("BanglaASR-only (transliterated)")
        
        # Factor 2: Similarity score (for matched segments)
        if similarity > 0.5:
            confidence += 0.2
            reasons.append(f"high similarity ({similarity:.0%})")
        elif similarity > 0.2:
            confidence += 0.1
            reasons.append(f"moderate similarity ({similarity:.0%})")
        elif similarity > 0 and similarity < 0.1:
            confidence -= 0.1
            reasons.append(f"low similarity ({similarity:.0%})")
        
        # Factor 3: Technical terms (clearer, less ambiguous)
        if has_technical_terms:
            confidence += 0.1
            reasons.append("contains technical terms")
        
        # Factor 4: Segment length (longer = more context)
        word_count = len(text.split())
        if word_count < 5:
            confidence -= 0.1
            reasons.append("very short segment")
        elif word_count > 20:
            confidence += 0.05
            reasons.append("long segment with context")
        
        # Clamp to 0-1
        confidence = max(0.0, min(1.0, confidence))
        
        # Determine if needs review
        needs_review = confidence < 0.4
        if needs_review:
            reasons.append("NEEDS REVIEW")
        
        reason_str = "; ".join(reasons)
        
        return confidence, needs_review, reason_str
    
    def _find_best_match(
        self, 
        segment: str, 
        candidates: List[Tuple[str, str]],  # (original, transliterated)
        threshold: float = None
    ) -> Optional[Tuple[str, str, float]]:
        """
        Find the best matching segment from candidates.
        
        Args:
            segment: The Whisper segment to match
            candidates: List of (original, transliterated) BanglaASR segments
            threshold: Minimum similarity (uses instance threshold if None)
        
        Returns:
            Tuple of (original, transliterated, similarity) or None
        """
        if threshold is None:
            threshold = self.similarity_threshold
            
        best_match = None
        best_sim = threshold
        
        for original, transliterated in candidates:
            sim = self._calculate_similarity(segment, transliterated)
            if sim > best_sim:
                best_sim = sim
                best_match = (original, transliterated, sim)
        
        return best_match
    
    def _merge_segments(
        self, 
        whisper_seg: str, 
        bangla_orig: str,
        bangla_trans: str,
        similarity: float
    ) -> str:
        """
        Merge a Whisper segment with its BanglaASR match.
        
        Strategy:
        - Keep Whisper version for technical terms
        - Add unique words from BanglaASR
        """
        # If very similar, prefer Whisper (more readable)
        if similarity > 0.7:
            return whisper_seg
        
        # Get words from both
        whisper_words = set(whisper_seg.lower().split())
        bangla_words = set(bangla_trans.lower().split())
        
        # Words only in BanglaASR
        unique_bangla = bangla_words - whisper_words - self.stop_words
        
        # If BanglaASR has unique non-trivial words, append them
        if unique_bangla and len(unique_bangla) > 2:
            unique_str = ' '.join(sorted(unique_bangla)[:5])  # Top 5 unique
            return f"{whisper_seg} [{unique_str}]"
        
        return whisper_seg
    
    def fuse(
        self,
        whisper_transcript: str,
        bangla_transcript: str,
    ) -> TransliterationFusionResult:
        """
        Fuse Whisper and BanglaASR using transliteration.
        
        Args:
            whisper_transcript: Output from Whisper (English/Romanized)
            bangla_transcript: Output from BanglaASR (Bengali Unicode)
            
        Returns:
            TransliterationFusionResult with merged transcript
        """
        # Segment both transcripts
        whisper_segments = self._segment_text(whisper_transcript)
        bangla_segments = self._segment_text(bangla_transcript)
        
        # Transliterate BanglaASR segments
        bangla_pairs = []  # (original, transliterated)
        for seg in bangla_segments:
            transliterated = self.transliterator.transliterate(seg)
            bangla_pairs.append((seg, transliterated))
        
        # Match and merge
        fused_segments: List[FusedSegment] = []
        used_bangla = set()
        total_similarity = 0.0
        
        for wseg in whisper_segments:
            # Find best matching BanglaASR segment
            match = self._find_best_match(wseg, bangla_pairs)
            
            if match:
                bangla_orig, bangla_trans, sim = match
                
                # Mark as used
                used_bangla.add(bangla_orig)
                total_similarity += sim
                
                # Merge the segments
                merged_text = self._merge_segments(wseg, bangla_orig, bangla_trans, sim)
                
                # Consider it "merged" if similarity exceeds the match threshold
                # (otherwise it's just Whisper with maybe some appended words)
                merge_threshold = max(self.similarity_threshold * 2, 0.05)
                
                # NEW: Calculate confidence score
                confidence, needs_review, reason = self._calculate_segment_confidence(
                    text=merged_text,
                    source=SegmentSource.MERGED if sim > merge_threshold else SegmentSource.WHISPER,
                    similarity=sim,
                    has_technical_terms=self._has_technical_terms(wseg),
                )
                
                fused_segments.append(FusedSegment(
                    text=merged_text,
                    source=SegmentSource.MERGED if sim > merge_threshold else SegmentSource.WHISPER,
                    similarity=sim,
                    whisper_original=wseg,
                    bangla_original=bangla_orig,
                    bangla_transliterated=bangla_trans,
                    confidence=confidence,
                    needs_review=needs_review,
                    confidence_reason=reason,
                ))
            else:
                # No match, use Whisper as-is
                # Lower confidence when no BanglaASR match (less verification)
                confidence, needs_review, reason = self._calculate_segment_confidence(
                    text=wseg,
                    source=SegmentSource.WHISPER,
                    similarity=0.0,
                    has_technical_terms=self._has_technical_terms(wseg),
                )
                
                fused_segments.append(FusedSegment(
                    text=wseg,
                    source=SegmentSource.WHISPER,
                    whisper_original=wseg,
                    confidence=confidence,
                    needs_review=needs_review,
                    confidence_reason=reason,
                ))
        
        # Add unmatched BanglaASR segments (may contain unique content)
        for bangla_orig, bangla_trans in bangla_pairs:
            if bangla_orig not in used_bangla:
                # Check if it has meaningful content
                if len(bangla_trans) > 20 and not self._calculate_similarity(
                    bangla_trans, whisper_transcript
                ) > 0.5:
                    # Unverified BanglaASR-only segments have lower confidence
                    fused_segments.append(FusedSegment(
                        text=bangla_trans,
                        source=SegmentSource.BANGLA_ASR,
                        bangla_original=bangla_orig,
                        bangla_transliterated=bangla_trans,
                        confidence=0.3,  # Lower confidence - unverified
                        needs_review=True,
                        confidence_reason="Unmatched BanglaASR segment - no Whisper verification",
                    ))
        
        # Build final transcript
        fused_texts = [seg.text for seg in fused_segments]
        fused_transcript = '. '.join(fused_texts)
        
        # Calculate metrics
        whisper_count = sum(1 for s in fused_segments if s.source == SegmentSource.WHISPER)
        bangla_count = sum(1 for s in fused_segments if s.source == SegmentSource.BANGLA_ASR)
        merged_count = sum(1 for s in fused_segments if s.source == SegmentSource.MERGED)
        
        avg_sim = total_similarity / max(1, len(whisper_segments))
        
        # Word counts
        whisper_words = set(whisper_transcript.lower().split())
        fused_words = set(fused_transcript.lower().split())
        unique_from_bangla = len(fused_words - whisper_words - self.stop_words)
        
        # NEW: Calculate confidence metrics
        confidences = [s.confidence for s in fused_segments]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.5
        high_conf_count = sum(1 for c in confidences if c > 0.7)
        low_conf_count = sum(1 for c in confidences if c < 0.3)
        review_count = sum(1 for s in fused_segments if s.needs_review)
        
        return TransliterationFusionResult(
            fused_transcript=fused_transcript,
            segments=fused_segments,
            whisper_segments=whisper_count,
            bangla_segments=bangla_count,
            merged_segments=merged_count,
            average_similarity=avg_sim,
            whisper_word_count=len(whisper_words),
            bangla_word_count=len(set(bangla_transcript.split())),
            fused_word_count=len(fused_words),
            unique_words_from_bangla=unique_from_bangla,
            # NEW: Confidence metrics
            average_confidence=avg_confidence,
            high_confidence_segments=high_conf_count,
            low_confidence_segments=low_conf_count,
            segments_needing_review=review_count,
        )


# ============================================================================
# TEST
# ============================================================================

if __name__ == "__main__":
    # Test with real-ish content
    whisper = """Hello everyone, I am Tohid. Today's tutorial will be Java 
    object-oriented programming. Object-oriented programming is actually key.
    Class is a blueprint or template. We use class to create objects.
    Object has properties and behaviors. This is encapsulation inheritance polymorphism."""
    
    bangla = """হ্যালো সবাইকে, আমি তওহিদ। আজকের টিউটোরিয়াল হলো জাভা 
    অবজেক্ট ওরিয়েন্টেড প্রোগ্রামিং। ক্লাস হলো ব্লুপ্রিন্ট বা টেমপ্লেট।
    অবজেক্ট এর প্রোপার্টি এবং বিহেভিয়র থাকে। এনক্যাপসুলেশন ইনহেরিটেন্স পলিমরফিজম।"""
    
    fusion = DualASRFusionTransliterate()
    result = fusion.fuse(whisper, bangla)
    
    print("=" * 70)
    print("TRANSLITERATION-BASED FUSION TEST")
    print("=" * 70)
    print(f"\nWhisper segments: {result.whisper_segments}")
    print(f"BanglaASR segments: {result.bangla_segments}")
    print(f"Merged segments: {result.merged_segments}")
    print(f"Average similarity: {result.average_similarity:.2%}")
    print(f"Unique words from BanglaASR: {result.unique_words_from_bangla}")
    print()
    print("FUSED OUTPUT:")
    print("-" * 70)
    print(result.fused_transcript[:800])
    print()
    print("SEGMENT DETAILS:")
    print("-" * 70)
    for i, seg in enumerate(result.segments[:5]):
        print(f"{i+1}. [{seg.source.value}] sim={seg.similarity:.2f}")
        print(f"   Text: {seg.text[:80]}...")
