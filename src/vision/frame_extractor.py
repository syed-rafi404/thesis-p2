"""
Frame Extractor - Extract frames from lecture videos
====================================================
"""

import cv2
import numpy as np
from typing import List, Tuple, Generator, Optional
from pathlib import Path


class FrameExtractor:
    """
    Extract frames from lecture videos.
    
    Features:
    - Configurable frame rate
    - Keyframe detection (scene changes)
    - Frame deduplication
    """
    
    def __init__(
        self,
        target_fps: float = 1.0,
        resize_width: Optional[int] = 1280,
        detect_keyframes: bool = True
    ):
        """
        Initialize frame extractor.
        
        Args:
            target_fps: Target frames per second to extract
            resize_width: Width to resize frames (maintains aspect ratio)
            detect_keyframes: Whether to detect scene changes
        """
        self.target_fps = target_fps
        self.resize_width = resize_width
        self.detect_keyframes = detect_keyframes
        
    def extract_frames(
        self,
        video_path: str,
        output_dir: Optional[str] = None
    ) -> List[Tuple[float, np.ndarray]]:
        """
        Extract frames from video at specified FPS.
        
        Args:
            video_path: Path to video file
            output_dir: Optional directory to save frames
            
        Returns:
            List of (timestamp, frame) tuples
        """
        # TODO: Implement frame extraction
        raise NotImplementedError("FrameExtractor.extract_frames() - Implement in Phase 2")
    
    def extract_frames_generator(
        self,
        video_path: str
    ) -> Generator[Tuple[float, np.ndarray], None, None]:
        """
        Generator version for memory-efficient processing.
        
        Args:
            video_path: Path to video file
            
        Yields:
            (timestamp, frame) tuples
        """
        # TODO: Implement generator version
        raise NotImplementedError("FrameExtractor.extract_frames_generator() - Implement in Phase 2")
    
    def detect_scene_changes(
        self,
        video_path: str,
        threshold: float = 30.0
    ) -> List[float]:
        """
        Detect scene changes/keyframes in video.
        
        Args:
            video_path: Path to video file
            threshold: Sensitivity threshold for detection
            
        Returns:
            List of timestamps where scenes change
        """
        # TODO: Implement scene change detection
        raise NotImplementedError("FrameExtractor.detect_scene_changes() - Implement in Phase 2")
    
    def get_video_info(self, video_path: str) -> dict:
        """
        Get video metadata.
        
        Args:
            video_path: Path to video file
            
        Returns:
            Dictionary with fps, duration, resolution, etc.
        """
        # TODO: Implement video info extraction
        raise NotImplementedError("FrameExtractor.get_video_info() - Implement in Phase 2")
