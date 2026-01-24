"""
=============================================================================
GAZE TRACKER - Spatio-Temporal Hand Pointing Detection
=============================================================================
Multimodal Banglish Classroom Summarizer
Master's Thesis - Research Component 2: Spatio-Temporal Gaze Tracking

Detects when a lecturer's hand points to specific terms on the whiteboard
using YOLOv8-Pose for real-time pose estimation.

Model: YOLOv8n-Pose (lightweight, fast inference)
Keypoints: Uses wrist position to estimate pointing location
=============================================================================
"""

import numpy as np
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass

import cv2
from ultralytics import YOLO

from rich.console import Console

console = Console()


# YOLOv8 COCO Pose Keypoint Indices
KEYPOINT_NOSE = 0
KEYPOINT_LEFT_EYE = 1
KEYPOINT_RIGHT_EYE = 2
KEYPOINT_LEFT_EAR = 3
KEYPOINT_RIGHT_EAR = 4
KEYPOINT_LEFT_SHOULDER = 5
KEYPOINT_RIGHT_SHOULDER = 6
KEYPOINT_LEFT_ELBOW = 7
KEYPOINT_RIGHT_ELBOW = 8
KEYPOINT_LEFT_WRIST = 9
KEYPOINT_RIGHT_WRIST = 10
KEYPOINT_LEFT_HIP = 11
KEYPOINT_RIGHT_HIP = 12
KEYPOINT_LEFT_KNEE = 13
KEYPOINT_RIGHT_KNEE = 14
KEYPOINT_LEFT_ANKLE = 15
KEYPOINT_RIGHT_ANKLE = 16


@dataclass
class TextBoundingBox:
    """Bounding box for text on whiteboard."""
    x1: int
    y1: int
    x2: int
    y2: int
    text: str
    
    def contains_point(self, x: float, y: float) -> bool:
        """Check if a point (x, y) is inside this bounding box."""
        return self.x1 <= x <= self.x2 and self.y1 <= y <= self.y2
    
    def to_list(self) -> List[int]:
        """Return as [x1, y1, x2, y2]."""
        return [self.x1, self.y1, self.x2, self.y2]


@dataclass
class PointingResult:
    """Result of pointing detection."""
    is_pointing: bool
    focused_term: Optional[str]
    hand_position: Optional[Tuple[int, int]]  # (x, y) of wrist/hand
    extended_position: Optional[Tuple[int, int]]  # Estimated fingertip
    confidence: float
    keypoints: Optional[np.ndarray]  # All detected keypoints


class GazeTracker:
    """
    Tracks hand pointing gestures to detect focus on whiteboard terms.
    
    Uses YOLOv8-Pose for skeleton detection and estimates pointing
    direction from elbow-wrist vector to find focused text regions.
    """
    
    def __init__(
        self, 
        model_name: str = "yolov8n-pose.pt",
        confidence_threshold: float = 0.5,
        extension_factor: float = 0.5,  # How far to extend past wrist
    ):
        """
        Initialize the GazeTracker.
        
        Args:
            model_name: YOLOv8 pose model to use (default: yolov8n-pose.pt)
            confidence_threshold: Minimum keypoint confidence
            extension_factor: Factor to extend from wrist toward estimated fingertip
                             (as fraction of elbow-wrist distance)
        """
        self.model_name = model_name
        self.confidence_threshold = confidence_threshold
        self.extension_factor = extension_factor
        self.model: Optional[YOLO] = None
        self._is_loaded = False
        
    def load_model(self) -> None:
        """Load the YOLOv8 pose model."""
        if self._is_loaded:
            return
            
        console.print(f"[bold]🦴 Loading YOLOv8-Pose:[/bold] {self.model_name}")
        
        # YOLOv8 auto-downloads the model if not present
        self.model = YOLO(self.model_name)
        self._is_loaded = True
        
        console.print(f"[green]✓ YOLOv8-Pose loaded[/green]\n")
    
    def _get_keypoint(
        self, 
        keypoints: np.ndarray, 
        index: int
    ) -> Optional[Tuple[float, float, float]]:
        """
        Extract a specific keypoint from the keypoints array.
        
        Args:
            keypoints: Array of shape (17, 3) with (x, y, confidence)
            index: Keypoint index (0-16)
            
        Returns:
            Tuple of (x, y, confidence) or None if not detected
        """
        if keypoints is None or len(keypoints) <= index:
            return None
            
        kp = keypoints[index]
        x, y, conf = float(kp[0]), float(kp[1]), float(kp[2])
        
        if conf < self.confidence_threshold:
            return None
            
        return (x, y, conf)
    
    def _estimate_pointing_position(
        self, 
        keypoints: np.ndarray,
        use_right: bool = True,
    ) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """
        Estimate pointing position by extending elbow-wrist vector.
        
        Since COCO pose doesn't have finger keypoints, we estimate
        the pointing direction by extending the elbow→wrist vector.
        
        Args:
            keypoints: Detected keypoints array
            use_right: Use right arm (True) or left arm (False)
            
        Returns:
            Tuple of ((wrist_x, wrist_y), (extended_x, extended_y)) or None
        """
        if use_right:
            elbow_idx, wrist_idx = KEYPOINT_RIGHT_ELBOW, KEYPOINT_RIGHT_WRIST
        else:
            elbow_idx, wrist_idx = KEYPOINT_LEFT_ELBOW, KEYPOINT_LEFT_WRIST
        
        elbow = self._get_keypoint(keypoints, elbow_idx)
        wrist = self._get_keypoint(keypoints, wrist_idx)
        
        if elbow is None or wrist is None:
            return None
        
        elbow_x, elbow_y, _ = elbow
        wrist_x, wrist_y, _ = wrist
        
        # Calculate direction vector from elbow to wrist
        dx = wrist_x - elbow_x
        dy = wrist_y - elbow_y
        
        # Extend past wrist to estimate fingertip
        extended_x = int(wrist_x + dx * self.extension_factor)
        extended_y = int(wrist_y + dy * self.extension_factor)
        
        return ((int(wrist_x), int(wrist_y)), (extended_x, extended_y))
    
    def detect_focus(
        self, 
        frame: np.ndarray, 
        text_bounding_boxes: List[Dict[str, Any]],
    ) -> Optional[str]:
        """
        Detect which term (if any) the hand is pointing at.
        
        Args:
            frame: BGR image frame (numpy array)
            text_bounding_boxes: List of dicts with keys:
                - 'bbox': [x1, y1, x2, y2]
                - 'text': str (the term)
                
        Returns:
            The text of the focused term, or None if not pointing at anything
        """
        result = self.detect_focus_detailed(frame, text_bounding_boxes)
        return result.focused_term
    
    def detect_focus_detailed(
        self, 
        frame: np.ndarray, 
        text_bounding_boxes: List[Dict[str, Any]],
    ) -> PointingResult:
        """
        Detect pointing with full details.
        
        Args:
            frame: BGR image frame
            text_bounding_boxes: List of {'bbox': [x1,y1,x2,y2], 'text': str}
            
        Returns:
            PointingResult with all detection details
        """
        if not self._is_loaded:
            self.load_model()
        
        # Run pose estimation
        results = self.model(frame, verbose=False)
        
        if not results or len(results) == 0:
            return PointingResult(
                is_pointing=False,
                focused_term=None,
                hand_position=None,
                extended_position=None,
                confidence=0.0,
                keypoints=None,
            )
        
        # Get keypoints from first detected person
        result = results[0]
        if result.keypoints is None or len(result.keypoints.data) == 0:
            return PointingResult(
                is_pointing=False,
                focused_term=None,
                hand_position=None,
                extended_position=None,
                confidence=0.0,
                keypoints=None,
            )
        
        keypoints = result.keypoints.data[0].cpu().numpy()  # Shape: (17, 3)
        
        # Try right hand first, then left
        pointing = self._estimate_pointing_position(keypoints, use_right=True)
        if pointing is None:
            pointing = self._estimate_pointing_position(keypoints, use_right=False)
        
        if pointing is None:
            return PointingResult(
                is_pointing=False,
                focused_term=None,
                hand_position=None,
                extended_position=None,
                confidence=0.0,
                keypoints=keypoints,
            )
        
        wrist_pos, extended_pos = pointing
        
        # Check if extended position is inside any text bounding box
        focused_term = None
        for box_info in text_bounding_boxes:
            bbox = box_info.get('bbox', box_info.get('bounding_box', []))
            text = box_info.get('text', '')
            
            if len(bbox) >= 4:
                x1, y1, x2, y2 = bbox[:4]
                # Check extended position (estimated fingertip)
                if x1 <= extended_pos[0] <= x2 and y1 <= extended_pos[1] <= y2:
                    focused_term = text
                    break
                # Also check wrist position as fallback
                if x1 <= wrist_pos[0] <= x2 and y1 <= wrist_pos[1] <= y2:
                    focused_term = text
                    break
        
        # Get confidence from wrist keypoint
        wrist_kp = self._get_keypoint(keypoints, KEYPOINT_RIGHT_WRIST)
        if wrist_kp is None:
            wrist_kp = self._get_keypoint(keypoints, KEYPOINT_LEFT_WRIST)
        confidence = wrist_kp[2] if wrist_kp else 0.0
        
        return PointingResult(
            is_pointing=True,
            focused_term=focused_term,
            hand_position=wrist_pos,
            extended_position=extended_pos,
            confidence=confidence,
            keypoints=keypoints,
        )
    
    def visualize(
        self, 
        frame: np.ndarray, 
        result: PointingResult,
        text_bounding_boxes: List[Dict[str, Any]],
        show_skeleton: bool = True,
    ) -> np.ndarray:
        """
        Draw visualization on the frame.
        
        Args:
            frame: BGR image to draw on (will be modified)
            result: PointingResult from detect_focus_detailed
            text_bounding_boxes: List of text bounding boxes
            show_skeleton: Whether to draw the full skeleton
            
        Returns:
            Frame with visualizations drawn
        """
        frame = frame.copy()
        
        # Draw all text bounding boxes
        for box_info in text_bounding_boxes:
            bbox = box_info.get('bbox', box_info.get('bounding_box', []))
            text = box_info.get('text', '')
            
            if len(bbox) >= 4:
                x1, y1, x2, y2 = map(int, bbox[:4])
                
                # Highlight if this is the focused term
                if result.focused_term and text == result.focused_term:
                    # Green highlight for focused term
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
                    cv2.putText(
                        frame, f"FOCUS: {text}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2
                    )
                else:
                    # Blue for other terms
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 1)
                    cv2.putText(
                        frame, text, (x1, y1 - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1
                    )
        
        # Draw hand position and pointing direction
        if result.hand_position:
            # Wrist: Yellow circle
            cv2.circle(frame, result.hand_position, 10, (0, 255, 255), -1)
            cv2.circle(frame, result.hand_position, 12, (0, 0, 0), 2)
            
        if result.extended_position:
            # Extended position: Red circle (estimated fingertip)
            cv2.circle(frame, result.extended_position, 8, (0, 0, 255), -1)
            cv2.circle(frame, result.extended_position, 10, (0, 0, 0), 2)
            
            # Draw line from wrist to extended position
            if result.hand_position:
                cv2.line(
                    frame, result.hand_position, result.extended_position,
                    (0, 255, 255), 2
                )
        
        # Draw skeleton if requested
        if show_skeleton and result.keypoints is not None:
            self._draw_skeleton(frame, result.keypoints)
        
        # Status text
        status = f"Focused: {result.focused_term}" if result.focused_term else "No focus detected"
        cv2.putText(
            frame, status, (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2
        )
        
        return frame
    
    def _draw_skeleton(self, frame: np.ndarray, keypoints: np.ndarray) -> None:
        """Draw skeleton connections on frame."""
        # COCO skeleton connections
        connections = [
            (KEYPOINT_NOSE, KEYPOINT_LEFT_EYE),
            (KEYPOINT_NOSE, KEYPOINT_RIGHT_EYE),
            (KEYPOINT_LEFT_EYE, KEYPOINT_LEFT_EAR),
            (KEYPOINT_RIGHT_EYE, KEYPOINT_RIGHT_EAR),
            (KEYPOINT_NOSE, KEYPOINT_LEFT_SHOULDER),
            (KEYPOINT_NOSE, KEYPOINT_RIGHT_SHOULDER),
            (KEYPOINT_LEFT_SHOULDER, KEYPOINT_RIGHT_SHOULDER),
            (KEYPOINT_LEFT_SHOULDER, KEYPOINT_LEFT_ELBOW),
            (KEYPOINT_RIGHT_SHOULDER, KEYPOINT_RIGHT_ELBOW),
            (KEYPOINT_LEFT_ELBOW, KEYPOINT_LEFT_WRIST),
            (KEYPOINT_RIGHT_ELBOW, KEYPOINT_RIGHT_WRIST),
            (KEYPOINT_LEFT_SHOULDER, KEYPOINT_LEFT_HIP),
            (KEYPOINT_RIGHT_SHOULDER, KEYPOINT_RIGHT_HIP),
            (KEYPOINT_LEFT_HIP, KEYPOINT_RIGHT_HIP),
        ]
        
        for (idx1, idx2) in connections:
            kp1 = self._get_keypoint(keypoints, idx1)
            kp2 = self._get_keypoint(keypoints, idx2)
            
            if kp1 is not None and kp2 is not None:
                pt1 = (int(kp1[0]), int(kp1[1]))
                pt2 = (int(kp2[0]), int(kp2[1]))
                cv2.line(frame, pt1, pt2, (0, 255, 0), 2)
        
        # Draw keypoints
        for i in range(17):
            kp = self._get_keypoint(keypoints, i)
            if kp is not None:
                pt = (int(kp[0]), int(kp[1]))
                cv2.circle(frame, pt, 4, (0, 0, 255), -1)


def demo_gaze_tracking(image_path: str, output_path: str = None) -> None:
    """
    Demo function to test gaze tracking on a single image.
    
    Args:
        image_path: Path to input image
        output_path: Optional path to save visualization
    """
    console.print(f"[bold]🎯 GazeTracker Demo[/bold]")
    console.print(f"Input: {image_path}\n")
    
    # Load image
    frame = cv2.imread(image_path)
    if frame is None:
        console.print(f"[red]Error: Could not load image[/red]")
        return
    
    # Example text bounding boxes (normally from VLM/OCR)
    # These would be replaced with actual detected text regions
    h, w = frame.shape[:2]
    text_boxes = [
        {'bbox': [int(w*0.1), int(h*0.1), int(w*0.3), int(h*0.15)], 'text': 'A* Algorithm'},
        {'bbox': [int(w*0.4), int(h*0.2), int(w*0.6), int(h*0.25)], 'text': 'Heuristic'},
        {'bbox': [int(w*0.1), int(h*0.3), int(w*0.25), int(h*0.35)], 'text': 'BFS'},
        {'bbox': [int(w*0.3), int(h*0.4), int(w*0.5), int(h*0.45)], 'text': 'f(n) = g(n) + h(n)'},
    ]
    
    # Initialize tracker
    tracker = GazeTracker()
    
    # Detect focus
    result = tracker.detect_focus_detailed(frame, text_boxes)
    
    # Print results
    console.print(f"[cyan]Pointing detected:[/cyan] {result.is_pointing}")
    console.print(f"[cyan]Hand position:[/cyan] {result.hand_position}")
    console.print(f"[cyan]Extended position:[/cyan] {result.extended_position}")
    console.print(f"[cyan]Focused term:[/cyan] {result.focused_term or 'None'}")
    console.print(f"[cyan]Confidence:[/cyan] {result.confidence:.2f}")
    
    # Visualize
    vis_frame = tracker.visualize(frame, result, text_boxes)
    
    # Save or display
    if output_path:
        cv2.imwrite(output_path, vis_frame)
        console.print(f"\n[green]✓ Saved visualization to {output_path}[/green]")
    else:
        # Display in window
        cv2.imshow("GazeTracker Demo", vis_frame)
        console.print("\n[dim]Press any key to close...[/dim]")
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == "__main__":
    import sys
    
    console.print("""
╭──────────────────────────────────────────────────────────────╮
│  GazeTracker - Spatio-Temporal Hand Pointing Detection       │
│  Uses YOLOv8-Pose to detect hand gestures toward whiteboard  │
╰──────────────────────────────────────────────────────────────╯
    """)
    
    if len(sys.argv) > 1:
        # Run demo with provided image
        image_path = sys.argv[1]
        output_path = sys.argv[2] if len(sys.argv) > 2 else None
        demo_gaze_tracking(image_path, output_path)
    else:
        # Quick test without image - just verify model loads
        console.print("[bold]Quick Test Mode[/bold] (no image provided)\n")
        
        tracker = GazeTracker()
        tracker.load_model()
        
        # Create a dummy frame to test
        dummy_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        dummy_boxes = [
            {'bbox': [100, 100, 200, 150], 'text': 'TestTerm'},
        ]
        
        result = tracker.detect_focus_detailed(dummy_frame, dummy_boxes)
        console.print(f"[green]✓ Model loaded and inference working[/green]")
        console.print(f"[dim]  (No person detected in blank frame, as expected)[/dim]")
        
        console.print("\n[bold]Usage:[/bold]")
        console.print("  python src/research/gaze_tracker.py <image_path> [output_path]")
