"""GestureMouse Pro application entry point."""

__version__ = "1.0.0"

import sys
import time
from collections import deque
from typing import Deque, Optional

import cv2

import config
import dashboard
import gesture_engine
import mouse_controller


class GestureMouseApp:
    """Orchestrates camera capture, gesture detection, and mouse control."""

    def __init__(self) -> None:
        """Initialize dependencies and camera resources."""
        self._print_startup_banner()
        self.gesture_engine = gesture_engine.GestureEngine()
        self.mouse_controller = mouse_controller.MouseController()
        self.dashboard = dashboard.Dashboard()
        self.camera = cv2.VideoCapture(config.CAMERA_INDEX)
        if not self.camera.isOpened():
            print(
                "Error: Could not open camera. "
                "Check CAMERA_INDEX in config.py and ensure the webcam is available."
            )
            self.camera.release()
            self.gesture_engine.close()
            sys.exit(1)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, config.FRAME_WIDTH)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, config.FRAME_HEIGHT)
        self.current_mode = "PAUSED"
        self.hand_loss_timer: Optional[float] = None
        self._frame_times: Deque[float] = deque(maxlen=15)
        self._last_frame_time = time.perf_counter()
        self.fist_start_time: Optional[float] = None
        self.fist_start_palm_x: Optional[float] = None
        self.fist_start_palm_y: Optional[float] = None
        self.DRAG_MOVE_THRESHOLD = 15
        self.DRAG_FIST_HOLD_TIME = 0.4

    def _print_startup_banner(self) -> None:
        """Print a startup banner to the terminal."""
        print(
            "╔══════════════════════════════════╗\n"
            "║     GestureMouse Pro v1.0.0      ║\n"
            "║  Show your hand to the camera.   ║\n"
            "║  Press Q to quit safely.         ║\n"
            "╚══════════════════════════════════╝"
        )

    def _update_fps(self) -> float:
        """Compute rolling average FPS over the last 15 frames."""
        now = time.perf_counter()
        frame_time = now - self._last_frame_time
        self._last_frame_time = now
        self._frame_times.append(frame_time)
        total_time = sum(self._frame_times)
        if total_time <= 0:
            return 0.0
        return len(self._frame_times) / total_time

    def run(self) -> None:
        """Run the main application loop."""
        try:
            while True:
                ok, frame = self.camera.read()
                if not ok:
                    continue

                frame = cv2.flip(frame, 1)

                landmarks, gesture, pinch_data, palm_center = self.gesture_engine.process_frame(frame)
                fps = self._update_fps()

                if not landmarks:
                    if self.hand_loss_timer is None:
                        self.hand_loss_timer = time.perf_counter()
                    elif time.perf_counter() - self.hand_loss_timer > config.HAND_LOSS_PAUSE_DELAY:
                        self.current_mode = "PAUSED"
                else:
                    self.hand_loss_timer = None

                if fps < config.FPS_AUTO_PAUSE_THRESHOLD:
                    self.current_mode = "PAUSED"

                if landmarks:
                    if gesture == "FIST":
                        if self.fist_start_time is None:
                            self.fist_start_time = time.perf_counter()
                            self.fist_start_palm_x = palm_center[0]
                            self.fist_start_palm_y = palm_center[1]

                        fist_held_duration = time.perf_counter() - self.fist_start_time

                        if palm_center[0] is not None and self.fist_start_palm_x is not None:
                            dx = (palm_center[0] - self.fist_start_palm_x) * config.FRAME_WIDTH
                            dy = (palm_center[1] - self.fist_start_palm_y) * config.FRAME_HEIGHT
                            palm_moved = (dx**2 + dy**2) ** 0.5
                        else:
                            palm_moved = 0.0

                        if self.current_mode != "DRAG":
                            if (
                                fist_held_duration >= self.DRAG_FIST_HOLD_TIME
                                and palm_moved >= self.DRAG_MOVE_THRESHOLD
                            ):
                                self.current_mode = "DRAG"
                                self.mouse_controller.start_drag()
                            elif (
                                fist_held_duration >= self.DRAG_FIST_HOLD_TIME
                                and palm_moved < self.DRAG_MOVE_THRESHOLD
                            ):
                                self.current_mode = "PAUSED"
                                self.fist_start_time = None
                    else:
                        if self.current_mode == "DRAG":
                            self.mouse_controller.stop_drag()
                            self.current_mode = "MOVE"
                        self.fist_start_time = None
                        self.fist_start_palm_x = None
                        self.fist_start_palm_y = None

                    if self.current_mode == "PAUSED":
                        if gesture == "MOVE":
                            self.current_mode = "MOVE"
                    elif gesture == "SCROLL":
                        self.current_mode = "SCROLL"
                    elif self.current_mode == "SCROLL" and gesture != "SCROLL":
                        self.current_mode = "MOVE"
                        self.mouse_controller.reset_scroll_anchor()

                    if self.current_mode == "MOVE":
                        if gesture == "LEFT_CLICK":
                            is_left_pinching = pinch_data["left_pinch_dist"] < config.CLICK_DISTANCE_THRESHOLD
                            if self.mouse_controller.handle_left_click(is_left_pinching):
                                self.dashboard.trigger_click_flash()
                        elif gesture == "RIGHT_CLICK":
                            is_right_pinching = pinch_data["right_pinch_dist"] < config.CLICK_DISTANCE_THRESHOLD
                            if self.mouse_controller.handle_right_click(is_right_pinching):
                                self.dashboard.trigger_click_flash()
                        elif gesture == "MOVE":
                            if palm_center[0] is not None:
                                self.mouse_controller.move_cursor(palm_center[0], palm_center[1])
                            self.mouse_controller.handle_left_click(False)
                            self.mouse_controller.handle_right_click(False)

                    if self.current_mode == "DRAG":
                        if palm_center[0] is not None:
                            self.mouse_controller.move_cursor(palm_center[0], palm_center[1])

                    if self.current_mode == "SCROLL":
                        if palm_center[1] is not None:
                            self.mouse_controller.handle_scroll(palm_center[1])

                self.dashboard.draw(
                    frame,
                    self.current_mode,
                    fps,
                    gesture,
                    hand_detected=bool(landmarks),
                    landmarks=landmarks,
                )

                cv2.imshow("GestureMouse Pro — Press Q to quit", frame)
                if cv2.waitKey(1) & 0xFF == config.KILL_KEY:
                    break
        finally:
            self.cleanup()

    def cleanup(self) -> None:
        """Release all resources and close windows."""
        self.gesture_engine.close()
        self.camera.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    GestureMouseApp().run()
