"""
Hyperparameter Validation for Transliteration Fusion

Tests different similarity thresholds to find the optimal value
for matching Whisper and BanglaASR segments.

Usage:
    python scripts/validate_fusion_threshold.py [video_path]
"""

import sys
import json
import time
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.audio.dual_asr_fusion_transliterate import DualASRFusionTransliterate


@dataclass
class ThresholdResult:
    """Result for a specific threshold."""
    threshold: float
    merged_segments: int
    average_similarity: float
    fused_word_count: int
    unique_from_bangla: int
    processing_time: float
    
    def score(self) -> float:
        """
        Calculate a composite score for this threshold.
        
        Higher is better:
        - More merged segments = better alignment
        - Higher average similarity = better quality matches
        - More unique words from Bangla = better coverage
        """
        # Normalize merged segments (assume max ~100)
        merged_norm = min(self.merged_segments / 50.0, 1.0)
        
        # Average similarity already 0-1
        sim_norm = self.average_similarity
        
        # Unique words bonus (assume max ~500)
        unique_norm = min(self.unique_from_bangla / 300.0, 1.0)
        
        # Weighted combination
        return (0.35 * merged_norm) + (0.40 * sim_norm) + (0.25 * unique_norm)


def validate_thresholds(
    whisper_transcript: str,
    bangla_transcript: str,
    thresholds: List[float] = None
) -> Dict[float, ThresholdResult]:
    """
    Test multiple thresholds and return results.
    
    Args:
        whisper_transcript: Whisper output text
        bangla_transcript: BanglaASR output text (Bengali Unicode)
        thresholds: List of thresholds to test
        
    Returns:
        Dictionary mapping threshold to ThresholdResult
    """
    if thresholds is None:
        thresholds = [0.01, 0.02, 0.03, 0.05, 0.07, 0.10, 0.15, 0.20, 0.25, 0.30]
    
    results = {}
    
    print("\n" + "=" * 70)
    print("HYPERPARAMETER VALIDATION: Similarity Threshold")
    print("=" * 70)
    print(f"\nTesting {len(thresholds)} threshold values...")
    print(f"Whisper length: {len(whisper_transcript):,} chars")
    print(f"BanglaASR length: {len(bangla_transcript):,} chars")
    print("-" * 70)
    
    for threshold in thresholds:
        start_time = time.time()
        
        # Create fusion with specific threshold
        fusion = DualASRFusionTransliterate(similarity_threshold=threshold)
        result = fusion.fuse(whisper_transcript, bangla_transcript)
        
        processing_time = time.time() - start_time
        
        threshold_result = ThresholdResult(
            threshold=threshold,
            merged_segments=result.merged_segments,
            average_similarity=result.average_similarity,
            fused_word_count=result.fused_word_count,
            unique_from_bangla=result.unique_words_from_bangla,
            processing_time=processing_time,
        )
        
        results[threshold] = threshold_result
        
        print(f"  Threshold {threshold:.2f}: "
              f"merged={result.merged_segments:3d}, "
              f"avg_sim={result.average_similarity:.3f}, "
              f"unique={result.unique_words_from_bangla:3d}, "
              f"score={threshold_result.score():.3f}")
    
    return results


def find_optimal_threshold(results: Dict[float, ThresholdResult]) -> float:
    """Find the threshold with the best composite score."""
    best_threshold = min(results.keys())
    best_score = -1.0
    
    for threshold, result in results.items():
        score = result.score()
        if score > best_score:
            best_score = score
            best_threshold = threshold
    
    return best_threshold


def run_validation_on_file(output_dir: Path) -> Dict[str, Any]:
    """
    Run validation using existing transcripts from an output directory.
    
    Args:
        output_dir: Path to output directory containing transcripts
        
    Returns:
        Validation results dictionary
    """
    # Load transcripts
    whisper_path = output_dir / "transcript_whisper_baseline.txt"
    bangla_path = output_dir / "transcript_bangla.txt"
    
    if not whisper_path.exists() or not bangla_path.exists():
        raise FileNotFoundError(f"Missing transcripts in {output_dir}")
    
    whisper_text = whisper_path.read_text(encoding='utf-8')
    bangla_text = bangla_path.read_text(encoding='utf-8')
    
    # Run validation
    results = validate_thresholds(whisper_text, bangla_text)
    
    # Find optimal
    optimal = find_optimal_threshold(results)
    
    print("\n" + "=" * 70)
    print(f"OPTIMAL THRESHOLD: {optimal:.2f}")
    print(f"Score: {results[optimal].score():.3f}")
    print(f"Merged segments: {results[optimal].merged_segments}")
    print(f"Average similarity: {results[optimal].average_similarity:.3f}")
    print(f"Unique from BanglaASR: {results[optimal].unique_from_bangla}")
    print("=" * 70)
    
    # Build report
    report = {
        "source_dir": str(output_dir),
        "whisper_chars": len(whisper_text),
        "bangla_chars": len(bangla_text),
        "optimal_threshold": optimal,
        "optimal_score": results[optimal].score(),
        "results": {
            str(t): {
                "merged_segments": r.merged_segments,
                "average_similarity": r.average_similarity,
                "fused_word_count": r.fused_word_count,
                "unique_from_bangla": r.unique_from_bangla,
                "score": r.score(),
                "processing_time": r.processing_time,
            }
            for t, r in results.items()
        }
    }
    
    return report


def main():
    """Main entry point."""
    # Default to test_transliteration output
    if len(sys.argv) > 1:
        output_dir = Path(sys.argv[1])
    else:
        output_dir = Path("output/test_transliteration")
    
    if not output_dir.exists():
        print(f"Error: Output directory not found: {output_dir}")
        print("Usage: python scripts/validate_fusion_threshold.py [output_dir]")
        sys.exit(1)
    
    print(f"\nValidating fusion thresholds using: {output_dir}")
    
    report = run_validation_on_file(output_dir)
    
    # Save report
    report_path = output_dir / "threshold_validation.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    
    print(f"\nReport saved to: {report_path}")
    
    # Return optimal for CI/automation
    print(f"\n[RESULT] Optimal threshold: {report['optimal_threshold']}")
    return report['optimal_threshold']


if __name__ == "__main__":
    main()
