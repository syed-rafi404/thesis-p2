"""
Vision Processing Module
========================
Handles frame extraction, whiteboard detection, and VLM-based understanding.

NOTE: We use Vision Language Models (VLM) instead of traditional OCR.
      EasyOCR was tested in a previous version and failed on Banglish handwriting.
"""

from .frame_extractor import FrameExtractor
from .vlm_analyzer import WhiteboardVLM
from .preprocessor import VisionPreprocessor

__all__ = ["FrameExtractor", "WhiteboardVLM", "VisionPreprocessor"]
