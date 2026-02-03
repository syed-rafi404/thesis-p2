"""
=============================================================================
SMART DUAL-ASR FUSION - Intelligent Whisper + BanglaASR Merging
=============================================================================
Multimodal Banglish Classroom Summarizer
Master's Thesis - NOVELTY 2: Smart Dual-ASR Fusion

PROBLEM:
Banglish lectures contain both English and Bengali. Standard Whisper
struggles with Bengali, while BanglaASR may miss English technical terms.

SOLUTION:
Intelligently merge outputs from both ASR systems:
1. SEGMENT - Split audio into language-homogeneous chunks
2. DETECT - Identify which language dominates each chunk
3. SELECT - Use Whisper for English-heavy, BanglaASR for Bengali-heavy
4. MERGE - Combine best segments into unified transcript

METRICS:
- Language Coverage Score: % of content captured from both languages
- Fusion Quality: Comparison of fused vs individual transcripts
=============================================================================
"""

import re
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


class LanguageType(Enum):
    """Language classification."""
    ENGLISH = "english"
    BENGALI = "bengali"
    MIXED = "mixed"


@dataclass
class TranscriptSegment:
    """A segment of transcript with language info."""
    text: str
    start_char: int
    end_char: int
    language: LanguageType
    confidence: float
    source: str  # "whisper" or "bangla_asr"


@dataclass
class FusionResult:
    """Result of dual-ASR fusion."""
    fused_transcript: str
    segments: List[TranscriptSegment]
    whisper_coverage: float  # % of output from Whisper
    bangla_coverage: float   # % of output from BanglaASR
    english_ratio: float     # % of detected English
    bengali_ratio: float     # % of detected Bengali
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "fused_transcript": self.fused_transcript,
            "whisper_coverage": self.whisper_coverage,
            "bangla_coverage": self.bangla_coverage,
            "english_ratio": self.english_ratio,
            "bengali_ratio": self.bengali_ratio,
            "segment_count": len(self.segments),
        }


class DualASRFusion:
    """
    Intelligently fuses Whisper and BanglaASR outputs.
    
    Strategy:
    1. Detect language patterns in both transcripts
    2. For English-heavy sections, prefer Whisper
    3. For Bengali-heavy sections, prefer BanglaASR
    4. Merge with overlap handling
    """
    
    def __init__(self):
        # Bengali Unicode range
        self.bengali_pattern = re.compile(r'[\u0980-\u09FF]')
        
        # English pattern (ASCII letters)
        self.english_pattern = re.compile(r'[a-zA-Z]')
        
        # Romanized Bengali common words
        self.romanized_bengali = {
            'ami', 'tumi', 'apni', 'se', 'ora', 'amra', 'tomra', 'apnara',
            'eta', 'ota', 'ki', 'keno', 'kothay', 'kokhon', 'kivabe', 'kemon',
            'ar', 'ba', 'kintu', 'tai', 'jodi', 'tahole', 'akhon', 'ekhane',
            'okhane', 'ache', 'nei', 'hoy', 'hobe', 'kora', 'bola', 'dekha',
            'jete', 'ashe', 'jay', 'dekhun', 'bolchi', 'korchi', 'likhchi',
            'amader', 'tader', 'ekta', 'duta', 'tinta', 'charta', 'pachta',
            'shob', 'kichu', 'keu', 'keuno', 'prottek', 'shudhu', 'matro',
            'thakbe', 'thake', 'chilam', 'chilo', 'hoye', 'gelo', 'eshe',
            'jkhon', 'tokhon', 'shomoy', 'dhorte', 'pari', 'parbo', 'parbe',
            'lagbe', 'dorkar', 'chai', 'chao', 'chan', 'debo', 'diben',
            'bujhte', 'bujhi', 'bujhecho', 'mone', 'kore', 'korlam', 'korbo',
            'likhte', 'likhi', 'likhbo', 'podte', 'podi', 'porbo', 'shunbo',
            'shuni', 'shunecho', 'dekhbo', 'dekhi', 'dekhecho', 'jani',
            'janbo', 'janen', 'shikhi', 'shikhbo', 'shikhecho', 'bojha',
            'bojhi', 'bojhecho', 'khub', 'onek', 'ektu', 'beshi', 'kom',
            'bhalo', 'kharap', 'boro', 'choto', 'notun', 'purano', 'prothom',
            'shesh', 'abar', 'ebar', 'ebaar', 'sebaar', 'porer', 'ager',
            'upore', 'niche', 'shamne', 'pechone', 'dane', 'bame', 'majhe',
            'bahire', 'bhitore', 'kache', 'dure', 'shathe', 'biruddhe',
            # Common lecture words in Romanized Bengali
            'dekho', 'bolo', 'koro', 'jao', 'eso', 'dao', 'nio', 'rakho',
            'prottek', 'shokol', 'sobai', 'karo', 'kauke', 'kothai', 'jehetu',
            'sheta', 'eita', 'oita', 'jeta', 'konta', 'koto', 'kotobar',
        }
        
        # English technical terms (prioritize in Whisper)
        self.technical_english = {
            'class', 'object', 'method', 'function', 'variable', 'array',
            'string', 'integer', 'boolean', 'public', 'private', 'static',
            'void', 'return', 'import', 'extends', 'implements', 'interface',
            'abstract', 'final', 'new', 'this', 'super', 'null', 'true', 'false',
            'if', 'else', 'for', 'while', 'do', 'switch', 'case', 'break',
            'continue', 'try', 'catch', 'throw', 'throws', 'finally',
            'inheritance', 'polymorphism', 'encapsulation', 'abstraction',
            'constructor', 'destructor', 'getter', 'setter', 'instance',
            'reference', 'pointer', 'memory', 'heap', 'stack', 'allocation',
            'algorithm', 'data', 'structure', 'programming', 'code', 'compile',
        }
    
    def _detect_language(self, text: str) -> Tuple[LanguageType, float]:
        """
        Detect the dominant language in text.
        
        Returns:
            Tuple of (language_type, confidence)
        """
        if not text:
            return LanguageType.MIXED, 0.0
        
        text_lower = text.lower()
        words = text_lower.split()
        
        # Count Bengali Unicode characters
        bengali_chars = len(self.bengali_pattern.findall(text))
        english_chars = len(self.english_pattern.findall(text))
        total_chars = bengali_chars + english_chars
        
        if total_chars == 0:
            return LanguageType.MIXED, 0.0
        
        # Count romanized Bengali words
        romanized_count = sum(1 for w in words if w in self.romanized_bengali)
        
        # Count technical English words
        technical_count = sum(1 for w in words if w in self.technical_english)
        
        # Calculate ratios
        bengali_ratio = bengali_chars / total_chars
        romanized_ratio = romanized_count / max(1, len(words))
        technical_ratio = technical_count / max(1, len(words))
        
        # If significant Bengali Unicode, it's Bengali
        if bengali_ratio > 0.3:
            return LanguageType.BENGALI, bengali_ratio
        
        # If high romanized Bengali, still Bengali-ish
        if romanized_ratio > 0.3 and technical_ratio < 0.1:
            return LanguageType.BENGALI, romanized_ratio
        
        # If technical terms present, prefer English
        if technical_ratio > 0.1:
            return LanguageType.ENGLISH, 1 - romanized_ratio
        
        # Default based on character ratio
        english_ratio = english_chars / total_chars
        if english_ratio > 0.7:
            return LanguageType.ENGLISH, english_ratio
        elif bengali_ratio > 0.3 or romanized_ratio > 0.2:
            return LanguageType.BENGALI, bengali_ratio + romanized_ratio
        else:
            return LanguageType.MIXED, 0.5
    
    def _segment_by_sentence(self, text: str) -> List[str]:
        """Split text into sentence-like segments."""
        # Split on sentence boundaries
        segments = re.split(r'(?<=[.!?।])\s+', text)
        
        # Merge very short segments
        merged = []
        current = ""
        for seg in segments:
            if len(current) + len(seg) < 200:
                current += " " + seg if current else seg
            else:
                if current:
                    merged.append(current.strip())
                current = seg
        if current:
            merged.append(current.strip())
        
        return merged
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate word-level similarity between two texts."""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        
        return intersection / union if union > 0 else 0.0
    
    def fuse(
        self,
        whisper_transcript: str,
        bangla_transcript: str,
    ) -> FusionResult:
        """
        Fuse Whisper and BanglaASR transcripts.
        
        Strategy:
        1. Segment both transcripts
        2. Detect language in each segment
        3. Select best source per segment
        4. Merge into unified output
        
        Args:
            whisper_transcript: Output from Whisper
            bangla_transcript: Output from BanglaASR
            
        Returns:
            FusionResult with merged transcript and metrics
        """
        # Segment transcripts
        whisper_segments = self._segment_by_sentence(whisper_transcript)
        bangla_segments = self._segment_by_sentence(bangla_transcript)
        
        # Analyze Whisper segments
        fused_parts = []
        segments = []
        whisper_chars = 0
        bangla_chars = 0
        english_chars = 0
        bengali_chars = 0
        
        for i, wseg in enumerate(whisper_segments):
            lang, conf = self._detect_language(wseg)
            
            # Count language characters
            eng = len(self.english_pattern.findall(wseg))
            ben = len(self.bengali_pattern.findall(wseg))
            english_chars += eng
            bengali_chars += ben
            
            # For English/Technical content, use Whisper
            if lang == LanguageType.ENGLISH or any(
                term in wseg.lower() for term in list(self.technical_english)[:20]
            ):
                fused_parts.append(wseg)
                whisper_chars += len(wseg)
                segments.append(TranscriptSegment(
                    text=wseg,
                    start_char=sum(len(p) for p in fused_parts[:-1]),
                    end_char=sum(len(p) for p in fused_parts),
                    language=lang,
                    confidence=conf,
                    source="whisper"
                ))
            else:
                # For Bengali content, check if BanglaASR has better coverage
                # Try to find matching segment in BanglaASR
                best_match = None
                best_sim = 0.0
                
                for bseg in bangla_segments:
                    sim = self._calculate_similarity(wseg, bseg)
                    if sim > best_sim and sim > 0.1:
                        best_sim = sim
                        best_match = bseg
                
                # Use BanglaASR if it has Bengali Unicode (real Bengali)
                if best_match and len(self.bengali_pattern.findall(best_match)) > 10:
                    fused_parts.append(best_match)
                    bangla_chars += len(best_match)
                    segments.append(TranscriptSegment(
                        text=best_match,
                        start_char=sum(len(p) for p in fused_parts[:-1]),
                        end_char=sum(len(p) for p in fused_parts),
                        language=LanguageType.BENGALI,
                        confidence=best_sim,
                        source="bangla_asr"
                    ))
                else:
                    # Fall back to Whisper
                    fused_parts.append(wseg)
                    whisper_chars += len(wseg)
                    segments.append(TranscriptSegment(
                        text=wseg,
                        start_char=sum(len(p) for p in fused_parts[:-1]),
                        end_char=sum(len(p) for p in fused_parts),
                        language=lang,
                        confidence=conf,
                        source="whisper"
                    ))
        
        fused_transcript = " ".join(fused_parts)
        total_chars = whisper_chars + bangla_chars
        
        return FusionResult(
            fused_transcript=fused_transcript,
            segments=segments,
            whisper_coverage=whisper_chars / max(1, total_chars),
            bangla_coverage=bangla_chars / max(1, total_chars),
            english_ratio=english_chars / max(1, english_chars + bengali_chars),
            bengali_ratio=bengali_chars / max(1, english_chars + bengali_chars),
        )
    
    def print_fusion_summary(self, result: FusionResult) -> None:
        """Pretty print fusion results."""
        console.print(Panel.fit(
            f"[bold]Dual-ASR Fusion Results[/bold]\n"
            f"Total segments: {len(result.segments)}\n"
            f"Transcript length: {len(result.fused_transcript)} chars",
            border_style="green"
        ))
        
        table = Table(title="Fusion Metrics", show_header=True)
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Whisper Coverage", f"{result.whisper_coverage*100:.1f}%")
        table.add_row("BanglaASR Coverage", f"{result.bangla_coverage*100:.1f}%")
        table.add_row("English Content", f"{result.english_ratio*100:.1f}%")
        table.add_row("Bengali Content", f"{result.bengali_ratio*100:.1f}%")
        table.add_row("Segments", str(len(result.segments)))
        
        console.print(table)
        
        # Show segment breakdown
        whisper_segs = sum(1 for s in result.segments if s.source == "whisper")
        bangla_segs = sum(1 for s in result.segments if s.source == "bangla_asr")
        console.print(f"\n[dim]Whisper segments: {whisper_segs}, BanglaASR segments: {bangla_segs}[/dim]")


if __name__ == "__main__":
    # Test the fusion
    console.print(Panel.fit(
        "[bold]Dual-ASR Fusion Test[/bold]",
        border_style="blue"
    ))
    
    # Sample transcripts
    whisper_sample = """
    Hello everyone, I am Tauhid. Today we will learn about Java OOP.
    Object-Oriented Programming has four pillars.
    Ami ekhane class and object niye kotha bolbo.
    So inheritance means one class extends another class.
    Polymorphism mane holo multiple forms.
    """
    
    bangla_sample = """
    হ্যালো সবাই, আমি তাওহিদ। আজকে আমরা জাভা ওওপি নিয়ে শিখব।
    অবজেক্ট-ওরিয়েন্টেড প্রোগ্রামিং এর চারটি পিলার আছে।
    আমি এখানে ক্লাস এবং অবজেক্ট নিয়ে কথা বলব।
    তাহলে ইনহেরিটেন্স মানে এক ক্লাস আরেক ক্লাস কে এক্সটেন্ড করে।
    পলিমরফিজম মানে হলো মাল্টিপল ফর্মস।
    """
    
    fusion = DualASRFusion()
    result = fusion.fuse(whisper_sample, bangla_sample)
    fusion.print_fusion_summary(result)
    
    console.print("\n[bold]Fused Transcript Sample:[/bold]")
    console.print(result.fused_transcript[:300] + "...")
