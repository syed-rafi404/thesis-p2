"""
=============================================================================
TEMPORAL VISUAL CONTEXT - Time-Aligned Visual Bias for ASR
=============================================================================
Multimodal Banglish Classroom Summarizer
Master's Thesis - Novelty #2: Temporal Visual Bias

This module implements temporal alignment between visual keywords and audio segments.
Instead of biasing the ENTIRE audio with ALL keywords, we bias each audio segment
with keywords that are temporally relevant (visible at that time).

Key Innovation:
- Keywords from frame at 0:30 → bias audio segment 0:00-1:00
- Keywords from frame at 1:00 → bias audio segment 0:30-1:30
- This "sliding window" approach provides contextually appropriate visual grounding

Why It Matters:
- Reduces false biasing (e.g., "Object" from minute 5 shouldn't bias minute 1)
- More precise keyword injection at relevant timestamps
- Could be publishable: "Temporally-Grounded Visual Context for Speech Recognition"
=============================================================================
"""

from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple, Optional
from pathlib import Path
import json


@dataclass
class FrameKeywords:
    """Keywords extracted from a single frame with timestamp."""
    frame_path: str
    timestamp_sec: float
    keywords: List[str]
    
    def to_dict(self) -> Dict:
        return {
            "frame_path": self.frame_path,
            "timestamp_sec": self.timestamp_sec,
            "keywords": self.keywords
        }


@dataclass
class TemporalVisualContext:
    """
    Time-aligned visual context for ASR biasing.
    
    Maps timestamps to relevant keywords for segment-level visual bias.
    Implements a sliding window approach where each audio segment gets
    keywords from surrounding frames.
    
    Attributes:
        frame_keywords: List of FrameKeywords (timestamp → keywords)
        window_before_sec: How many seconds before a frame's timestamp to apply its keywords
        window_after_sec: How many seconds after a frame's timestamp to apply its keywords
        all_keywords: Flattened unique list of all keywords (for backward compatibility)
    """
    frame_keywords: List[FrameKeywords] = field(default_factory=list)
    window_before_sec: float = 30.0  # Apply keywords 30s before frame
    window_after_sec: float = 30.0   # Apply keywords 30s after frame
    
    @property
    def all_keywords(self) -> List[str]:
        """Get all unique keywords (backward compatible with flat list)."""
        all_kw = []
        for fk in self.frame_keywords:
            all_kw.extend(fk.keywords)
        # Deduplicate while preserving order
        seen = set()
        unique = []
        for kw in all_kw:
            if kw.lower() not in seen:
                seen.add(kw.lower())
                unique.append(kw)
        return unique
    
    def get_keywords_for_timestamp(self, timestamp_sec: float) -> List[str]:
        """
        Get keywords relevant for a specific audio timestamp.
        
        Uses sliding window: returns keywords from frames where
        frame_timestamp - window_before <= timestamp <= frame_timestamp + window_after
        
        Args:
            timestamp_sec: Audio timestamp in seconds
            
        Returns:
            List of unique keywords relevant at this timestamp
        """
        relevant_keywords = []
        
        for fk in self.frame_keywords:
            window_start = fk.timestamp_sec - self.window_before_sec
            window_end = fk.timestamp_sec + self.window_after_sec
            
            if window_start <= timestamp_sec <= window_end:
                relevant_keywords.extend(fk.keywords)
        
        # Deduplicate while preserving order
        seen = set()
        unique = []
        for kw in relevant_keywords:
            if kw.lower() not in seen:
                seen.add(kw.lower())
                unique.append(kw)
        
        return unique
    
    def get_keywords_for_segment(self, start_sec: float, end_sec: float) -> List[str]:
        """
        Get keywords for an audio segment (start to end).
        
        Args:
            start_sec: Segment start time in seconds
            end_sec: Segment end time in seconds
            
        Returns:
            List of unique keywords relevant for this segment
        """
        # Check keywords at segment start, middle, and end
        mid_sec = (start_sec + end_sec) / 2
        
        keywords = []
        keywords.extend(self.get_keywords_for_timestamp(start_sec))
        keywords.extend(self.get_keywords_for_timestamp(mid_sec))
        keywords.extend(self.get_keywords_for_timestamp(end_sec))
        
        # Deduplicate while preserving order
        seen = set()
        unique = []
        for kw in keywords:
            if kw.lower() not in seen:
                seen.add(kw.lower())
                unique.append(kw)
        
        return unique
    
    def get_segment_map(self, segment_duration_sec: float = 30.0) -> Dict[Tuple[float, float], List[str]]:
        """
        Pre-compute keyword map for fixed-size segments.
        
        Args:
            segment_duration_sec: Duration of each segment (default 30s = Whisper chunk)
            
        Returns:
            Dict mapping (start, end) tuples to keyword lists
        """
        if not self.frame_keywords:
            return {}
        
        # Find total duration
        max_timestamp = max(fk.timestamp_sec for fk in self.frame_keywords)
        total_duration = max_timestamp + segment_duration_sec
        
        segment_map = {}
        current_start = 0.0
        
        while current_start < total_duration:
            current_end = current_start + segment_duration_sec
            keywords = self.get_keywords_for_segment(current_start, current_end)
            segment_map[(current_start, current_end)] = keywords
            current_start = current_end
        
        return segment_map
    
    def add_frame_keywords(self, frame_path: str, timestamp_sec: float, keywords: List[str]):
        """Add keywords from a single frame."""
        self.frame_keywords.append(FrameKeywords(
            frame_path=frame_path,
            timestamp_sec=timestamp_sec,
            keywords=keywords
        ))
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "frame_keywords": [fk.to_dict() for fk in self.frame_keywords],
            "window_before_sec": self.window_before_sec,
            "window_after_sec": self.window_after_sec,
            "total_unique_keywords": len(self.all_keywords),
            "temporal_mode": True  # Flag to indicate this uses temporal alignment
        }
    
    def save(self, output_path: str):
        """Save to JSON file."""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'TemporalVisualContext':
        """Load from dictionary."""
        ctx = cls(
            window_before_sec=data.get('window_before_sec', 30.0),
            window_after_sec=data.get('window_after_sec', 30.0)
        )
        for fk_data in data.get('frame_keywords', []):
            ctx.frame_keywords.append(FrameKeywords(
                frame_path=fk_data['frame_path'],
                timestamp_sec=fk_data['timestamp_sec'],
                keywords=fk_data['keywords']
            ))
        return ctx
    
    @classmethod
    def load(cls, path: str) -> 'TemporalVisualContext':
        """Load from JSON file."""
        with open(path, 'r', encoding='utf-8') as f:
            return cls.from_dict(json.load(f))
    
    def __len__(self) -> int:
        """Number of frames with keywords."""
        return len(self.frame_keywords)
    
    def get_stats(self) -> Dict:
        """Get statistics about the temporal context."""
        if not self.frame_keywords:
            return {
                "total_frames": 0,
                "total_unique_keywords": 0,
                "avg_keywords_per_frame": 0,
                "temporal_coverage_sec": 0
            }
        
        all_kw = self.all_keywords
        timestamps = [fk.timestamp_sec for fk in self.frame_keywords]
        
        return {
            "total_frames": len(self.frame_keywords),
            "total_unique_keywords": len(all_kw),
            "avg_keywords_per_frame": sum(len(fk.keywords) for fk in self.frame_keywords) / len(self.frame_keywords),
            "temporal_coverage_sec": max(timestamps) - min(timestamps) if timestamps else 0,
            "window_size_sec": self.window_before_sec + self.window_after_sec
        }


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def create_temporal_context_from_flat_list(
    keywords: List[str],
    frame_paths: List[str],
    frame_interval_sec: float = 30.0
) -> TemporalVisualContext:
    """
    Create a TemporalVisualContext from a flat keyword list (backward compatibility).
    
    This distributes all keywords to all frames - essentially the old behavior.
    Use for comparison against true temporal alignment.
    
    Args:
        keywords: Flat list of all keywords
        frame_paths: List of frame file paths
        frame_interval_sec: Time between frames
        
    Returns:
        TemporalVisualContext with all keywords at all timestamps
    """
    ctx = TemporalVisualContext(
        window_before_sec=frame_interval_sec,
        window_after_sec=frame_interval_sec
    )
    
    for i, frame_path in enumerate(frame_paths):
        timestamp = i * frame_interval_sec
        ctx.add_frame_keywords(frame_path, timestamp, keywords)
    
    return ctx
