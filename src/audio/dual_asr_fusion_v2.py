"""
Smart Dual-ASR Fusion v2 - Fixed for Banglish Content

NOVELTY 2: Intelligently merges Whisper + BanglaASR outputs.

The key insight:
- Whisper outputs English/Romanized Banglish (readable)
- BanglaASR outputs Bengali Unicode (not directly usable)

Strategy:
1. Use Whisper as the BASE transcript (it's more readable)
2. Extract Bengali segments from BanglaASR
3. Use Bengali segments to ENHANCE coverage, not replace
4. Report language composition metrics
"""

import re
from dataclasses import dataclass, field
from typing import List, Dict, Any, Tuple, Optional
from enum import Enum


class LanguageType(Enum):
    """Types of language content."""
    ENGLISH = "english"
    BENGALI = "bengali"  
    BANGLISH = "banglish"  # Mixed romanized Bengali with English


@dataclass
class FusionResult:
    """Result of dual-ASR fusion."""
    fused_transcript: str
    whisper_base: str           # Original Whisper output
    bengali_supplement: str     # Bengali content from BanglaASR
    
    # Metrics
    whisper_word_count: int
    bangla_word_count: int
    bengali_char_ratio: float   # % Bengali Unicode in BanglaASR
    english_word_ratio: float   # % English words in Whisper
    banglish_detected: bool     # Whether Banglish pattern detected
    
    # Coverage
    total_coverage_chars: int
    fusion_benefit: str         # Description of what fusion added
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "fused_transcript": self.fused_transcript,
            "whisper_word_count": self.whisper_word_count,
            "bangla_word_count": self.bangla_word_count,
            "bengali_char_ratio": self.bengali_char_ratio,
            "english_word_ratio": self.english_word_ratio,
            "banglish_detected": self.banglish_detected,
            "total_coverage_chars": self.total_coverage_chars,
            "fusion_benefit": self.fusion_benefit,
        }


class DualASRFusionV2:
    """
    Improved Dual-ASR Fusion for Banglish Lecture Content.
    
    Key difference from v1: Doesn't try to merge incompatible scripts.
    Instead:
    1. Uses Whisper as base (readable romanized output)
    2. Extracts unique Bengali content from BanglaASR
    3. Appends Bengali supplement for LLM context
    """
    
    def __init__(self):
        # Bengali Unicode range
        self.bengali_pattern = re.compile(r'[\u0980-\u09FF]+')
        
        # English word pattern
        self.english_word_pattern = re.compile(r'\b[a-zA-Z]{2,}\b')
        
        # Technical terms (keep in English)
        self.technical_terms = {
            'class', 'object', 'method', 'function', 'variable', 'array',
            'string', 'integer', 'boolean', 'public', 'private', 'static',
            'void', 'return', 'import', 'java', 'python', 'code', 'programming',
            'inheritance', 'polymorphism', 'encapsulation', 'abstraction',
            'constructor', 'instance', 'blueprint', 'template', 'design',
            'tutorial', 'example', 'hello', 'world', 'data', 'type',
            'behavior', 'property', 'attribute', 'method', 'phone', 'car',
            'student', 'course', 'lecture', 'video', 'ram', 'processor',
        }
        
        # Romanized Bengali words (Banglish indicators)
        self.banglish_words = {
            'ami', 'tumi', 'apni', 'eta', 'ota', 'ki', 'keno', 'ar', 'ba',
            'kintu', 'tai', 'jodi', 'akhon', 'ekhane', 'ache', 'nei', 'hoy',
            'kora', 'bola', 'dekha', 'amader', 'tader', 'ekta', 'shob',
            'thakbe', 'lagbe', 'chai', 'bujhte', 'mone', 'korlam', 'korbo',
            'dekhbo', 'jani', 'shikhi', 'bhalo', 'boro', 'choto', 'abar',
            'dekho', 'bolo', 'koro', 'kemne', 'jehetu', 'jekono', 'prottek',
            # Common in lectures
            'bujhte', 'parchi', 'parbo', 'dekhun', 'bolchi', 'likhchi',
            'ashakori', 'basically', 'actually', 'bolechi', 'bolbo',
        }
    
    def _count_bengali_chars(self, text: str) -> int:
        """Count Bengali Unicode characters."""
        return len(self.bengali_pattern.findall(text))
    
    def _count_english_words(self, text: str) -> int:
        """Count English words."""
        words = self.english_word_pattern.findall(text.lower())
        return len([w for w in words if w in self.technical_terms or len(w) > 3])
    
    def _detect_banglish(self, text: str) -> bool:
        """Detect if text contains Banglish (romanized Bengali)."""
        words = text.lower().split()
        banglish_count = sum(1 for w in words if w in self.banglish_words)
        return banglish_count > 3  # At least 3 Banglish words
    
    def _extract_bengali_words(self, text: str) -> List[str]:
        """Extract Bengali words from text."""
        return self.bengali_pattern.findall(text)
    
    def _extract_unique_bengali_content(self, bangla_text: str) -> str:
        """
        Extract Bengali-heavy sentences that might add value.
        These are sentences with high Bengali Unicode content.
        """
        # Split into sentences
        sentences = re.split(r'[।.!?]', bangla_text)
        
        bengali_sentences = []
        for sent in sentences:
            sent = sent.strip()
            if not sent:
                continue
            
            # Calculate Bengali character ratio
            bengali_chars = len(self.bengali_pattern.findall(sent))
            total_chars = len(sent)
            
            if total_chars > 20 and bengali_chars / total_chars > 0.5:
                # This sentence is mostly Bengali
                bengali_sentences.append(sent)
        
        # Return top 5 most Bengali-heavy sentences
        return '। '.join(bengali_sentences[:5])
    
    def fuse(
        self,
        whisper_transcript: str,
        bangla_transcript: str,
    ) -> FusionResult:
        """
        Fuse Whisper and BanglaASR transcripts.
        
        Strategy (v2):
        1. Use Whisper as base (readable)
        2. Extract Bengali supplement from BanglaASR
        3. Combine for richer LLM context
        
        Args:
            whisper_transcript: Output from Whisper (English/Romanized)
            bangla_transcript: Output from BanglaASR (Bengali Unicode)
            
        Returns:
            FusionResult with fused transcript and metrics
        """
        # Calculate metrics
        whisper_words = whisper_transcript.split()
        bangla_words = bangla_transcript.split()
        
        whisper_word_count = len(whisper_words)
        bangla_word_count = len(bangla_words)
        
        # Bengali character ratio in BanglaASR output
        bengali_chars = self._count_bengali_chars(bangla_transcript)
        total_chars = len(bangla_transcript)
        bengali_char_ratio = bengali_chars / max(1, total_chars)
        
        # English word ratio in Whisper output
        english_words = self._count_english_words(whisper_transcript)
        english_word_ratio = english_words / max(1, whisper_word_count)
        
        # Detect Banglish in Whisper
        banglish_detected = self._detect_banglish(whisper_transcript)
        
        # Extract Bengali supplement
        bengali_supplement = self._extract_unique_bengali_content(bangla_transcript)
        
        # Build fused transcript
        # For Banglish content, Whisper is the best base
        # We add Bengali supplement at the end for LLM context
        if bengali_supplement and len(bengali_supplement) > 50:
            fused = f"{whisper_transcript}\n\n[Bengali Reference from BanglaASR]:\n{bengali_supplement}"
            fusion_benefit = f"Added {len(bengali_supplement)} chars of Bengali reference"
        else:
            fused = whisper_transcript
            fusion_benefit = "Whisper output sufficient (Banglish content)"
        
        return FusionResult(
            fused_transcript=fused,
            whisper_base=whisper_transcript,
            bengali_supplement=bengali_supplement,
            whisper_word_count=whisper_word_count,
            bangla_word_count=bangla_word_count,
            bengali_char_ratio=bengali_char_ratio,
            english_word_ratio=english_word_ratio,
            banglish_detected=banglish_detected,
            total_coverage_chars=len(fused),
            fusion_benefit=fusion_benefit,
        )


# ============================================================================
# SIMPLE TEST
# ============================================================================

if __name__ == "__main__":
    # Test with sample content
    whisper = """Hello everyone, I am Tohid. Today's tutorial will be Java 
    object-oriented programming. Object-oriented programming is actually key.
    Class object encapsulation inheritance polymorphism abstraction."""
    
    bangla = """হ্যালু ভিমান, আমি তওহিদ, আজকেট-টুটোনিল আমরা জাভার 
    অবজেক্টো-রেন্ডেড প্রোগ্রামিং নিয়ে কথা বলবো।"""
    
    fusion = DualASRFusionV2()
    result = fusion.fuse(whisper, bangla)
    
    print("=" * 60)
    print("DUAL-ASR FUSION v2 TEST")
    print("=" * 60)
    print(f"Whisper words: {result.whisper_word_count}")
    print(f"BanglaASR words: {result.bangla_word_count}")
    print(f"Bengali char ratio: {result.bengali_char_ratio:.1%}")
    print(f"English word ratio: {result.english_word_ratio:.1%}")
    print(f"Banglish detected: {result.banglish_detected}")
    print(f"Fusion benefit: {result.fusion_benefit}")
    print()
    print("FUSED OUTPUT:")
    print("-" * 60)
    print(result.fused_transcript[:500])
