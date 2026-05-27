"""Hand tracking and gesture detection logic for GestureMouse Pro."""

from __future__ import annotations

import math
from typing import Dict, List, Tuple

import cv2
import mediapipe as mp

import config


class GestureEngine:
    """Detects hand landmarks and classifies gestures."""

    def __init__(self) -> None:
        """Initialize the MediaPipe Hands solution."""
        self._mp_hands = mp.solutions.hands
        self._hands = self._mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.75,
            min_tracking_confidence=0.75,
        )

    def _finger_is_raised(self, landmarks: List[Tuple[float, float]], tip: int, pip: int) -> bool:
        """Return True if the finger is raised based on tip/pip Y positions."""
        return landmarks[tip][1] < landmarks[pip][1]

    def _finger_is_curled(self, landmarks: List[Tuple[float, float]], tip: int, pip: int) -> bool:
        """Return True if the finger is curled based on tip/pip Y positions."""
        return landmarks[tip][1] > landmarks[pip][1]

    def _pixel_distance(
        self,
        landmarks: List[Tuple[float, float]],
        a: int,
        b: int,
        frame_width: int,
        frame_height: int,
    ) -> float:
        """Compute Euclidean distance between two landmarks in pixel space."""
        ax = landmarks[a][0] * frame_width
        ay = landmarks[a][1] * frame_height
        bx = landmarks[b][0] * frame_width
        by = landmarks[b][1] * frame_height
        return math.hypot(ax - bx, ay - by)

    def process_frame(
        self, bgr_frame: "cv2.Mat"
    ) -> Tuple[List[Tuple[float, float]], str, Dict[str, float], Tuple[float | None, float | None]]:
        """Process a frame and return landmarks, gesture name, pinch data, and palm center."""
        frame_height, frame_width = bgr_frame.shape[:2]
        rgb_frame = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2RGB)
        results = self._hands.process(rgb_frame)

        if not results.multi_hand_landmarks:
            return [], "NONE", {"left_pinch_dist": float("inf"), "right_pinch_dist": float("inf")}, (None, None)

        hand_landmarks = results.multi_hand_landmarks[0]
        landmarks = [(lm.x, lm.y) for lm in hand_landmarks.landmark]

        left_pinch_dist = self._pixel_distance(landmarks, 4, 8, frame_width, frame_height)
        right_pinch_dist = self._pixel_distance(landmarks, 4, 12, frame_width, frame_height)

        pinch_data = {
            "left_pinch_dist": left_pinch_dist,
            "right_pinch_dist": right_pinch_dist,
        }

        palm_indices = [0, 5, 9, 13, 17]
        palm_x = sum(landmarks[i][0] for i in palm_indices) / len(palm_indices)
        palm_y = sum(landmarks[i][1] for i in palm_indices) / len(palm_indices)
        palm_center = (palm_x, palm_y)

        thumb_to_palm_dist = math.hypot(
            landmarks[4][0] - landmarks[0][0],
            landmarks[4][1] - landmarks[0][1],
        )

        fist_detected = (
            self._finger_is_curled(landmarks, 8, 5)
            and self._finger_is_curled(landmarks, 12, 9)
            and self._finger_is_curled(landmarks, 16, 13)
            and self._finger_is_curled(landmarks, 20, 17)
            and thumb_to_palm_dist < 0.1
        )

        if fist_detected:
            return landmarks, "FIST", pinch_data, palm_center

        scroll_detected = (
            self._finger_is_raised(landmarks, 8, 6)
            and self._finger_is_raised(landmarks, 12, 10)
            and self._finger_is_curled(landmarks, 16, 14)
            and self._finger_is_curled(landmarks, 20, 18)
        )

        if scroll_detected:
            return landmarks, "SCROLL", pinch_data, palm_center

        left_click_detected = (
            left_pinch_dist < config.CLICK_DISTANCE_THRESHOLD
            and self._finger_is_curled(landmarks, 12, 10)
            and self._finger_is_curled(landmarks, 16, 14)
            and self._finger_is_curled(landmarks, 20, 18)
        )

        if left_click_detected:
            return landmarks, "LEFT_CLICK", pinch_data, palm_center

        right_click_detected = (
            right_pinch_dist < config.CLICK_DISTANCE_THRESHOLD
            and self._finger_is_curled(landmarks, 8, 6)
            and self._finger_is_curled(landmarks, 16, 14)
            and self._finger_is_curled(landmarks, 20, 18)
        )

        if right_click_detected:
            return landmarks, "RIGHT_CLICK", pinch_data, palm_center

        move_detected = (
            self._finger_is_raised(landmarks, 8, 6)
            and self._finger_is_curled(landmarks, 12, 10)
            and self._finger_is_curled(landmarks, 16, 14)
            and self._finger_is_curled(landmarks, 20, 18)
        )

        if move_detected:
            return landmarks, "MOVE", pinch_data, palm_center

        return landmarks, "NONE", pinch_data, palm_center

    def close(self) -> None:
        """Release MediaPipe resources."""
        self._hands.close()
