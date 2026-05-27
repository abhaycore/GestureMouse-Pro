# GestureMouse Pro

GestureMouse Pro is a software-only hand-gesture mouse controller that uses your webcam, MediaPipe hand tracking, and PyAutoGUI to move the cursor, click, and scroll.

## Quick Start (3 steps)
1. Install dependencies: `pip install -r requirements.txt`
2. Run the app: `python main.py`
3. Hold your hand in view and use the gesture cheat sheet on the HUD.

## Requirements
- Python 3.9+
- A webcam
- Windows 10/11, Ubuntu 22.04+, or macOS 13+

## Installation
- Windows: double-click `setup.bat` or run `pip install -r requirements.txt`
- Linux/macOS: run `./setup.sh` or `pip3 install -r requirements.txt`

## Gesture Reference Table
```
+------------+----------------------------------------------+-------------------------------+
| GESTURE    | HAND SHAPE                                   | ACTION                        |
+------------+----------------------------------------------+-------------------------------+
| MOVE       | Index finger up, others curled                | Move cursor                   |
| LEFT_CLICK | Thumb + index pinch, other fingers curled     | Left click (hold to fire)     |
| RIGHT_CLICK| Thumb + middle pinch, others curled           | Right click (hold to fire)    |
| SCROLL     | Index + middle up, ring + pinky curled        | Scroll                        |
| FIST       | All fingers curled, thumb near palm           | Pause mode                    |
| NONE       | No recognized gesture                         | No action                     |
+------------+----------------------------------------------+-------------------------------+
```

## Configuration Guide
All tunable settings live in `config.py`:
- CAMERA_INDEX: Selects the webcam device index (0 is default).
- FRAME_WIDTH / FRAME_HEIGHT: Camera capture resolution.
- SMOOTHING_FACTOR: Time-based smoothing strength (lower = smoother).
- MOVE_SENSITIVITY: Expands the movement range to cover the screen.
- DEAD_ZONE_PIXELS: Ignores tiny movements to prevent cursor jitter.
- CLICK_DISTANCE_THRESHOLD: Maximum pinch distance in pixels to register a click.
- CLICK_HOLD_DURATION: How long the pinch must be held before clicking.
- GESTURE_COOLDOWN: Delay between repeated clicks.
- SCROLL_SPEED: Scroll units per tick.
- SCROLL_SENSITIVITY: Hand Y-movement multiplier for scrolling.
- FPS_AUTO_PAUSE_THRESHOLD: Auto-pause if FPS drops below this value.
- HAND_LOSS_PAUSE_DELAY: Auto-pause if the hand disappears for this long.
- DASHBOARD_FONT_SCALE: HUD font size.
- DASHBOARD_THICKNESS: HUD font stroke thickness.
- BORDER_FLASH_THICKNESS: Border thickness around the frame.
- KILL_KEY: Keyboard key to quit the app.

## Troubleshooting
- Camera not found: Verify your webcam is connected and adjust CAMERA_INDEX in config.py.
- Low FPS: Reduce FRAME_WIDTH/FRAME_HEIGHT or close other camera apps.
- Cursor jumping: Lower MOVE_SENSITIVITY or increase SMOOTHING_FACTOR.
- Click not firing: Increase CLICK_DISTANCE_THRESHOLD or CLICK_HOLD_DURATION.

## How It Works
GestureMouse Pro uses MediaPipe to track 21 hand landmarks per frame. These landmarks drive a gesture classifier with a priority order (fist, scroll, clicks, move). The mouse controller maps normalized landmark positions to screen coordinates, applies time-based smoothing, and handles click cooldowns. The HUD provides visual feedback, FPS, and mode transitions for safe and predictable control.
