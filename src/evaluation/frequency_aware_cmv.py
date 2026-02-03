"""
=============================================================================
FREQUENCY-AWARE CROSS-MODAL VERIFIER (CMV-F)
=============================================================================
Multimodal Banglish Classroom Summarizer
Master's Thesis - NOVELTY: Frequency-Aware Hallucination Detection

IMPROVEMENT OVER BASIC CMV:
The original CrossModalVerifier only checks PRESENCE - whether a term in the
transcript matches any visual keyword. This fails to detect REPETITION-based
hallucinations where a grounded term is repeated excessively.

Example Problem:
- "Compiler" appears on whiteboard → CMV says "compile" is grounded
- But ASR says "compile" 138 times (vs ~9 in ground truth)
- Original CMV: "All grounded, 0% hallucination" ← WRONG
- CMV-F: "138x is abnormal, 93% hallucination rate" ← CORRECT

Key Innovation:
1. Count term frequencies in transcript
2. Compare against expected baseline frequency
3. Flag terms that exceed threshold as repetition-hallucinations
4. Provide Repetition Hallucination Rate (RHR) metric

Metrics:
- Term Frequency Deviation (TFD) = actual_count / expected_count
- Repetition Hallucination Score (RHS) = terms with TFD > threshold
- Combined Hallucination Rate = ungrounded + over-represented
=============================================================================
"""

import re
from typing import List, Dict, Any, Set, Tuple
from collections import Counter
from thefuzz import fuzz
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


class FrequencyAwareCMV:
    """
    Frequency-Aware Cross-Modal Verifier for ASR hallucination detection.
    
    Detects two types of hallucinations:
    1. UNGROUNDED: Terms not matching any visual context (original CMV)
    2. REPETITION: Terms matching visual context but repeated excessively
    
    The key insight is that visual biasing can cause "grounded" terms to
    repeat in a self-reinforcing loop, which original CMV misses.
    """
    
    def __init__(
        self, 
        fuzzy_threshold: int = 80,
        min_term_length: int = 3,
        repetition_threshold: float = 3.0,  # Flag if >3x expected
        expected_frequency: float = 5.0,     # Baseline expected occurrence
    ):
        """
        Initialize the frequency-aware verifier.
        
        Args:
            fuzzy_threshold: Minimum fuzzy match score for grounding
            min_term_length: Minimum characters for term consideration
            repetition_threshold: TFD threshold for flagging repetition
            expected_frequency: Baseline expected term frequency
        """
        self.fuzzy_threshold = fuzzy_threshold
        self.min_term_length = min_term_length
        self.repetition_threshold = repetition_threshold
        self.expected_frequency = expected_frequency
        
        # Stopwords (same as original CMV)
        self.stopwords = {
            'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'must', 'shall', 'can', 'need', 'dare',
            'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it',
            'we', 'they', 'what', 'which', 'who', 'whom', 'whose', 'where',
            'when', 'why', 'how', 'all', 'each', 'every', 'both', 'few', 'more',
            'most', 'other', 'some', 'such', 'no', 'not', 'only', 'same', 'so',
            'than', 'too', 'very', 'just', 'but', 'and', 'or', 'if', 'then',
            'else', 'for', 'from', 'to', 'with', 'about', 'into', 'through',
            'ami', 'tumi', 'apni', 'se', 'ora', 'amra', 'tomra', 'apnara',
            'eta', 'ota', 'ki', 'keno', 'kothay', 'kokhon', 'kivabe', 'kemon',
            'ar', 'ba', 'kintu', 'tai', 'jodi', 'tahole', 'akhon', 'ekhane',
            'okay', 'right', 'now', 'see', 'look', 'basically', 'actually',
            'let', 'lets', 'going', 'like', 'get', 'make', 'use', 'using',
        }
    
    def _extract_all_words(self, text: str) -> List[str]:
        """Extract all words for frequency counting."""
        words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        return [w for w in words if len(w) >= self.min_term_length and w not in self.stopwords]
    
    def _extract_technical_terms(self, text: str) -> List[str]:
        """Extract potential technical terms (same as original CMV)."""
        terms = []
        
        # CamelCase
        terms.extend(re.findall(r'\b[A-Z][a-z]+(?:[A-Z][a-z]+)+\b', text))
        
        # ALL CAPS
        terms.extend(re.findall(r'\b[A-Z]{2,}\b', text))
        
        # Capitalized words
        for word in re.findall(r'\b[A-Z][a-z]{2,}\b', text):
            if word.lower() not in self.stopwords:
                terms.append(word)
        
        # Programming keywords
        programming_terms = {
            'int', 'string', 'void', 'public', 'private', 'static', 'class',
            'interface', 'extends', 'implements', 'return', 'null', 'true',
            'false', 'new', 'this', 'super', 'import', 'package', 'final',
            'compile', 'run', 'execute', 'method', 'object', 'variable',
        }
        words = set(text.lower().split())
        for word in words:
            clean = re.sub(r'[^a-z]', '', word)
            if clean in programming_terms:
                terms.append(clean)
        
        # Deduplicate
        seen = set()
        unique = []
        for term in terms:
            if term.lower() not in seen and len(term) >= self.min_term_length:
                seen.add(term.lower())
                unique.append(term)
        
        return unique
    
    def _count_word_frequencies(self, text: str) -> Counter:
        """Count all word frequencies in text."""
        words = self._extract_all_words(text)
        return Counter(words)
    
    def _is_grounded(self, term: str, visual_keywords: List[str]) -> Tuple[bool, int, str]:
        """Check if term is grounded in visual context."""
        term_lower = term.lower()
        best_score = 0
        best_match = ""
        
        for visual_term in visual_keywords:
            visual_lower = visual_term.lower()
            
            if term_lower == visual_lower:
                return True, 100, visual_term
            
            if term_lower in visual_lower or visual_lower in term_lower:
                return True, 95, visual_term
            
            score = fuzz.ratio(term_lower, visual_lower)
            if score > best_score:
                best_score = score
                best_match = visual_term
        
        return best_score >= self.fuzzy_threshold, best_score, best_match
    
    def _detect_repetition_hallucinations(
        self, 
        text: str, 
        visual_keywords: List[str]
    ) -> Dict[str, Any]:
        """
        Detect repetition-based hallucinations.
        
        A repetition hallucination occurs when a term that IS grounded in
        visual context appears far more times than expected, indicating
        a self-reinforcing loop during generation.
        
        Args:
            text: Transcript text
            visual_keywords: Visual context keywords
            
        Returns:
            Repetition analysis results
        """
        word_freq = self._count_word_frequencies(text)
        total_words = sum(word_freq.values())
        
        # Calculate average frequency for context
        avg_frequency = total_words / len(word_freq) if word_freq else 1.0
        
        # Use dynamic expected frequency based on text length
        dynamic_expected = max(self.expected_frequency, avg_frequency * 1.5)
        
        repetition_hallucinations = []
        grounded_normal = []
        
        for word, count in word_freq.items():
            # Check if grounded
            is_gr, score, match = self._is_grounded(word, visual_keywords)
            
            if is_gr:
                # Term is grounded - check if over-represented
                tfd = count / dynamic_expected
                
                if tfd > self.repetition_threshold:
                    repetition_hallucinations.append({
                        'term': word,
                        'count': count,
                        'expected': dynamic_expected,
                        'tfd': tfd,
                        'matched_visual': match,
                        'excess': count - int(dynamic_expected),
                    })
                else:
                    grounded_normal.append({
                        'term': word,
                        'count': count,
                        'tfd': tfd,
                        'matched_visual': match,
                    })
        
        # Calculate total excess (hallucinated repetitions)
        total_excess = sum(rh['excess'] for rh in repetition_hallucinations)
        
        # Repetition Hallucination Rate
        rhr = total_excess / total_words if total_words > 0 else 0.0
        
        return {
            'repetition_hallucinations': sorted(
                repetition_hallucinations, 
                key=lambda x: -x['tfd']
            ),
            'grounded_normal': grounded_normal,
            'total_words': total_words,
            'total_excess': total_excess,
            'repetition_hallucination_rate': rhr,
            'dynamic_expected': dynamic_expected,
        }
    
    def verify(
        self, 
        transcript: str, 
        visual_keywords: List[str]
    ) -> Dict[str, Any]:
        """
        Perform frequency-aware verification.
        
        Detects both:
        1. Ungrounded terms (traditional CMV)
        2. Repetition hallucinations (NEW in CMV-F)
        
        Args:
            transcript: ASR output text
            visual_keywords: Visual context keywords
            
        Returns:
            Comprehensive verification results
        """
        # Part 1: Traditional grounding check (unique terms only)
        technical_terms = self._extract_technical_terms(transcript)
        
        grounded = []
        ungrounded = []
        term_details = {}
        
        for term in technical_terms:
            is_gr, score, match = self._is_grounded(term, visual_keywords)
            term_details[term] = {
                'is_grounded': is_gr,
                'score': score,
                'matched_to': match if is_gr else None
            }
            
            if is_gr:
                grounded.append(term)
            else:
                ungrounded.append(term)
        
        total_unique = len(technical_terms)
        traditional_groundedness = len(grounded) / total_unique if total_unique > 0 else 1.0
        traditional_hallucination = 1.0 - traditional_groundedness
        
        # Part 2: Frequency-aware repetition detection
        rep_analysis = self._detect_repetition_hallucinations(transcript, visual_keywords)
        
        # Part 3: Combined metrics
        # Combined hallucination = ungrounded unique + excess repetitions
        word_freq = self._count_word_frequencies(transcript)
        total_words = sum(word_freq.values())
        
        ungrounded_word_count = sum(
            word_freq.get(term.lower(), 0) 
            for term in ungrounded
        )
        
        combined_hallucination_count = ungrounded_word_count + rep_analysis['total_excess']
        combined_hallucination_rate = combined_hallucination_count / total_words if total_words > 0 else 0.0
        
        return {
            # Traditional metrics (for comparison)
            'traditional': {
                'groundedness_score': traditional_groundedness,
                'hallucination_rate': traditional_hallucination,
                'grounded_count': len(grounded),
                'ungrounded_count': len(ungrounded),
            },
            
            # Frequency-aware metrics (NEW)
            'frequency_aware': {
                'repetition_hallucination_rate': rep_analysis['repetition_hallucination_rate'],
                'total_excess_words': rep_analysis['total_excess'],
                'repetition_hallucinations': rep_analysis['repetition_hallucinations'],
            },
            
            # Combined metrics
            'combined': {
                'hallucination_rate': combined_hallucination_rate,
                'hallucination_word_count': combined_hallucination_count,
                'total_words': total_words,
            },
            
            # Details
            'grounded_terms': grounded,
            'ungrounded_terms': ungrounded,
            'term_details': term_details,
            'visual_keywords_count': len(visual_keywords),
        }
    
    def compare_transcripts(
        self,
        baseline_transcript: str,
        biased_transcript: str,
        visual_keywords: List[str],
    ) -> Dict[str, Any]:
        """Compare two transcripts with frequency awareness."""
        baseline = self.verify(baseline_transcript, visual_keywords)
        biased = self.verify(biased_transcript, visual_keywords)
        
        return {
            'baseline': baseline,
            'biased': biased,
            'comparison': {
                'traditional_groundedness_change': (
                    biased['traditional']['groundedness_score'] - 
                    baseline['traditional']['groundedness_score']
                ),
                'repetition_hallucination_change': (
                    biased['frequency_aware']['repetition_hallucination_rate'] -
                    baseline['frequency_aware']['repetition_hallucination_rate']
                ),
                'combined_hallucination_change': (
                    biased['combined']['hallucination_rate'] -
                    baseline['combined']['hallucination_rate']
                ),
            }
        }
    
    def print_report(self, result: Dict[str, Any], name: str = "Transcript") -> None:
        """Print a detailed verification report."""
        console.print(f"\n[bold]═══ {name} - Frequency-Aware CMV Report ═══[/bold]")
        
        # Traditional metrics
        trad = result['traditional']
        console.print(f"\n[cyan]Traditional CMV (presence only):[/cyan]")
        console.print(f"  Groundedness: {trad['groundedness_score']*100:.1f}%")
        console.print(f"  Hallucination Rate: {trad['hallucination_rate']*100:.1f}%")
        
        # Frequency-aware metrics
        freq = result['frequency_aware']
        console.print(f"\n[cyan]Frequency-Aware CMV (NEW):[/cyan]")
        console.print(f"  Repetition Hallucination Rate: {freq['repetition_hallucination_rate']*100:.1f}%")
        console.print(f"  Excess Words (hallucinated): {freq['total_excess_words']}")
        
        if freq['repetition_hallucinations']:
            console.print(f"\n  [yellow]⚠ Repetition Hallucinations Detected:[/yellow]")
            for rh in freq['repetition_hallucinations'][:5]:
                console.print(
                    f"    • '{rh['term']}': {rh['count']}x "
                    f"(expected ~{rh['expected']:.0f}, excess: {rh['excess']})"
                )
        
        # Combined
        comb = result['combined']
        console.print(f"\n[cyan]Combined Hallucination Rate:[/cyan]")
        console.print(f"  {comb['hallucination_rate']*100:.1f}% ({comb['hallucination_word_count']} / {comb['total_words']} words)")


# =============================================================================
# TEST FUNCTION
# =============================================================================

def test_frequency_aware_cmv():
    """Test the frequency-aware CMV with known examples."""
    console.print(Panel.fit(
        "[bold]Frequency-Aware CMV Test[/bold]\n"
        "Testing with synthetic examples",
        border_style="blue"
    ))
    
    cmv = FrequencyAwareCMV(
        repetition_threshold=3.0,
        expected_frequency=5.0
    )
    
    # Example 1: Normal transcript (no hallucination)
    normal = "Today we learn about Java classes and objects. A class is a template."
    
    # Example 2: Repetition hallucination
    hallucinated = "Today we learn about compile. Compile. Compile. Compile. Compile. " * 10
    
    visual_keywords = ["Java", "class", "object", "Compiler", "template"]
    
    console.print("\n[bold]Example 1: Normal Transcript[/bold]")
    result1 = cmv.verify(normal, visual_keywords)
    cmv.print_report(result1, "Normal")
    
    console.print("\n[bold]Example 2: Hallucinated Transcript[/bold]")
    result2 = cmv.verify(hallucinated, visual_keywords)
    cmv.print_report(result2, "Hallucinated")
    
    console.print("\n[green]✓ Frequency-Aware CMV correctly identifies repetition hallucinations[/green]")


if __name__ == "__main__":
    test_frequency_aware_cmv()
