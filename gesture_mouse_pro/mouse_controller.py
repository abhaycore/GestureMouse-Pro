"""Mouse movement, click, and scroll control for GestureMouse Pro."""

from __future__ import annotations

import math
import time
from typing import Optional

import pyautogui

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0

from screeninfo import get_monitors

import config


class MouseController:
    """Controls the system mouse with smoothing and gesture cooldowns."""

    def __init__(self) -> None:
        """Initialize screen geometry and motion state."""
        monitor = next((m for m in get_monitors() if m.is_primary), None)
        if monitor is None:
            monitor = get_monitors()[0]
        self.screen_width = int(monitor.width)
        self.screen_height = int(monitor.height)
        self.smoothed_x = self.screen_width / 2.0
        self.smoothed_y = self.screen_height / 2.0
        self.left_click_timer: Optional[float] = None
        self.right_click_timer: Optional[float] = None
        self.last_left_click_time = 0.0
        self.last_right_click_time = 0.0
        self.scroll_anchor_y: Optional[float] = None
        self.current_mode = "MOVE"
        self._last_move_time: Optional[float] = None
        self.is_dragging = False

    def _time_based_alpha(self, now: float) -> float:
        """Compute time-based smoothing factor using elapsed time."""
        if self._last_move_time is None:
            self._last_move_time = now
            return 1.0
        dt = max(0.0, now - self._last_move_time)
        self._last_move_time = now
        alpha = 1.0 - math.exp(-config.SMOOTHING_FACTOR * dt * 60.0)
        return max(0.0, min(1.0, alpha))

    def move_cursor(self, norm_x: float, norm_y: float) -> None:
        """Move the cursor based on normalized hand coordinates."""
        scaled_x = (norm_x - 0.5) * config.MOVE_SENSITIVITY + 0.5
        scaled_y = (norm_y - 0.5) * config.MOVE_SENSITIVITY + 0.5

        scaled_x = max(0.0, min(1.0, scaled_x))
        scaled_y = max(0.0, min(1.0, scaled_y))

        target_x = scaled_x * self.screen_width
        target_y = scaled_y * self.screen_height

        alpha = self._time_based_alpha(time.perf_counter())
        dx = target_x - self.smoothed_x
        dy = target_y - self.smoothed_y
        if math.hypot(dx, dy) < config.DEAD_ZONE_PIXELS:
            return
        self.smoothed_x = self.smoothed_x * (1.0 - alpha) + target_x * alpha
        self.smoothed_y = self.smoothed_y * (1.0 - alpha) + target_y * alpha

        self.smoothed_x = max(0.0, min(self.screen_width - 1, self.smoothed_x))
        self.smoothed_y = max(0.0, min(self.screen_height - 1, self.smoothed_y))

        pyautogui.moveTo(self.smoothed_x, self.smoothed_y)

    def handle_left_click(self, is_pinching: bool) -> bool:
        """Handle left click with hold duration and cooldown."""
        now = time.perf_counter()
        if is_pinching:
            if self.left_click_timer is None:
                self.left_click_timer = now
            held_time = now - self.left_click_timer
            if held_time >= config.CLICK_HOLD_DURATION and now - self.last_left_click_time > config.GESTURE_COOLDOWN:
                pyautogui.click()
                self.last_left_click_time = now
                self.left_click_timer = None
                return True
        else:
            self.left_click_timer = None
        return False

    def handle_right_click(self, is_pinching: bool) -> bool:
        """Handle right click with hold duration and cooldown."""
        now = time.perf_counter()
        if is_pinching:
            if self.right_click_timer is None:
                self.right_click_timer = now
            held_time = now - self.right_click_timer
            if held_time >= config.CLICK_HOLD_DURATION and now - self.last_right_click_time > config.GESTURE_COOLDOWN:
                pyautogui.rightClick()
                self.last_right_click_time = now
                self.right_click_timer = None
                return True
        else:
            self.right_click_timer = None
        return False

    def handle_scroll(self, current_norm_y: float) -> None:
        """Scroll based on changes in normalized hand Y position."""
        if self.scroll_anchor_y is None:
            self.scroll_anchor_y = current_norm_y
            return
        delta_y = current_norm_y - self.scroll_anchor_y
        scroll_amount = int(delta_y * config.SCROLL_SENSITIVITY * self.screen_height)
        if scroll_amount != 0:
            pyautogui.scroll(-scroll_amount)
        self.scroll_anchor_y = current_norm_y

    def reset_scroll_anchor(self) -> None:
        """Reset the scroll anchor when leaving scroll mode."""
        self.scroll_anchor_y = None

    def start_drag(self) -> None:
        """Start a left-button drag operation."""
        pyautogui.mouseDown(button="left")
        self.is_dragging = True

    def stop_drag(self) -> None:
        """Stop a left-button drag operation."""
        pyautogui.mouseUp(button="left")
        self.is_dragging = False
