"""OpenCV HUD overlay for GestureMouse Pro."""

from __future__ import annotations

import time
from typing import List, Optional, Tuple

import cv2
import mediapipe as mp
from mediapipe.framework.formats import landmark_pb2

import config


class Dashboard:
    """Renders the HUD overlay, border, and visual feedback."""

    def __init__(self) -> None:
        """Initialize dashboard state."""
        self._last_mode: Optional[str] = None
        self._mode_transition_start: Optional[float] = None
        self._mode_transition_text: str = ""
        self._flash_frames_remaining = 0
        self._mp_drawing = mp.solutions.drawing_utils
        self._mp_hands = mp.solutions.hands

    def trigger_click_flash(self) -> None:
        """Flash the border white for a few frames after a click."""
        self._flash_frames_remaining = 3

    def _get_border_color(self, mode: str) -> Tuple[int, int, int]:
        """Return the border color for the given mode."""
        if self._flash_frames_remaining > 0:
            return (255, 255, 255)
        if mode == "DRAG":
            return (0, 200, 255)
        if mode == "SCROLL":
            return (50, 150, 255)
        if mode == "PAUSED":
            return (0, 0, 220)
        return (0, 220, 80)

    def _mode_color(self, mode: str) -> Tuple[int, int, int]:
        """Return the text color for the current mode."""
        if mode == "SCROLL":
            return (50, 150, 255)
        if mode == "DRAG":
            return (0, 200, 255)
        if mode == "PAUSED":
            return (0, 0, 220)
        return (0, 220, 80)

    def _draw_landmarks(self, frame: "cv2.Mat", landmarks: List[Tuple[float, float]]) -> None:
        """Draw hand landmarks with MediaPipe drawing utils."""
        if not landmarks:
            return
        landmark_list = landmark_pb2.NormalizedLandmarkList(
            landmark=[landmark_pb2.NormalizedLandmark(x=x, y=y, z=0.0) for x, y in landmarks]
        )
        self._mp_drawing.draw_landmarks(
            frame,
            landmark_list,
            self._mp_hands.HAND_CONNECTIONS,
            landmark_drawing_spec=self._mp_drawing.DrawingSpec(color=(160, 160, 160), thickness=1, circle_radius=2),
            connection_drawing_spec=self._mp_drawing.DrawingSpec(color=(120, 120, 120), thickness=1),
        )

    def draw(
        self,
        frame: "cv2.Mat",
        mode: str,
        fps: float,
        gesture: str,
        hand_detected: bool,
        landmarks: Optional[List[Tuple[float, float]]] = None,
    ) -> None:
        """Draw HUD, borders, landmarks, and overlays on the frame."""
        now = time.perf_counter()
        if mode != self._last_mode:
            self._last_mode = mode
            self._mode_transition_start = now
            self._mode_transition_text = f"{mode} MODE" if mode != "PAUSED" else "PAUSED"

        border_color = self._get_border_color(mode)
        if self._flash_frames_remaining > 0:
            self._flash_frames_remaining -= 1

        thickness = config.BORDER_FLASH_THICKNESS if mode == "PAUSED" else config.BORDER_FLASH_THICKNESS
        cv2.rectangle(frame, (0, 0), (frame.shape[1] - 1, frame.shape[0] - 1), border_color, thickness)

        overlay = frame.copy()
        cv2.rectangle(overlay, (10, 10), (320, 130), (20, 20, 20), -1)
        cv2.addWeighted(overlay, 0.45, frame, 0.55, 0, frame)

        font = cv2.FONT_HERSHEY_SIMPLEX
        line_y = 35
        line_step = 22
        cv2.putText(
            frame,
            f"MODE: {mode}",
            (20, line_y),
            font,
            config.DASHBOARD_FONT_SCALE,
            self._mode_color(mode),
            config.DASHBOARD_THICKNESS,
            cv2.LINE_AA,
        )
        line_y += line_step
        cv2.putText(
            frame,
            f"FPS: {fps:.1f}",
            (20, line_y),
            font,
            config.DASHBOARD_FONT_SCALE,
            (230, 230, 230),
            config.DASHBOARD_THICKNESS,
            cv2.LINE_AA,
        )
        line_y += line_step
        cv2.putText(
            frame,
            f"GESTURE: {gesture}",
            (20, line_y),
            font,
            config.DASHBOARD_FONT_SCALE,
            (230, 230, 230),
            config.DASHBOARD_THICKNESS,
            cv2.LINE_AA,
        )
        line_y += line_step
        hand_text = "DETECTED" if hand_detected else "NOT FOUND"
        cv2.putText(
            frame,
            f"HAND: {hand_text}",
            (20, line_y),
            font,
            config.DASHBOARD_FONT_SCALE,
            (230, 230, 230),
            config.DASHBOARD_THICKNESS,
            cv2.LINE_AA,
        )

        cheat_text = "☝ MOVE  |  ✌ SCROLL  |  ✊ PAUSE  |  ✊(hold+move) DRAG  |  Q QUIT"
        text_size = cv2.getTextSize(cheat_text, font, 0.6, 2)[0]
        text_x = int((frame.shape[1] - text_size[0]) / 2)
        cv2.putText(
            frame,
            cheat_text,
            (text_x, frame.shape[0] - 20),
            font,
            0.6,
            (230, 230, 230),
            2,
            cv2.LINE_AA,
        )

        if mode == "PAUSED" and not hand_detected:
            warning_text = "HAND LOST — AUTO PAUSE"
            warning_size = cv2.getTextSize(warning_text, font, 0.9, 3)[0]
            warning_x = int((frame.shape[1] - warning_size[0]) / 2)
            warning_y = int(frame.shape[0] / 2)
            cv2.putText(
                frame,
                warning_text,
                (warning_x, warning_y),
                font,
                0.9,
                (0, 0, 220),
                3,
                cv2.LINE_AA,
            )

        if self._mode_transition_start is not None:
            elapsed = now - self._mode_transition_start
            if elapsed <= 0.8:
                alpha = max(0.0, 1.0 - (elapsed / 0.8))
                transition_overlay = frame.copy()
                transition_size = cv2.getTextSize(self._mode_transition_text, font, 1.5, 4)[0]
                transition_x = int((frame.shape[1] - transition_size[0]) / 2)
                transition_y = int(frame.shape[0] / 2)
                cv2.putText(
                    transition_overlay,
                    self._mode_transition_text,
                    (transition_x, transition_y),
                    font,
                    1.5,
                    self._mode_color(mode),
                    4,
                    cv2.LINE_AA,
                )
                cv2.addWeighted(transition_overlay, alpha, frame, 1 - alpha, 0, frame)
            else:
                self._mode_transition_start = None

        if landmarks is not None:
            self._draw_landmarks(frame, landmarks)
