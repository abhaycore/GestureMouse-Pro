"""Configuration constants for GestureMouse Pro."""

CAMERA_INDEX = 0  # Webcam device index (0 = default)
FRAME_WIDTH = 640  # Capture frame width in pixels
FRAME_HEIGHT = 480  # Capture frame height in pixels

SMOOTHING_FACTOR = 0.45  # Lower = smoother but slower (0.1-0.5)
MOVE_SENSITIVITY = 2.2  # Multiplier to amplify cursor movement range
DEAD_ZONE_PIXELS = 10  # Dead zone radius to ignore micro-movements

CLICK_DISTANCE_THRESHOLD = 40  # Pixels: max pinch distance to register click
CLICK_HOLD_DURATION = 0.25  # Seconds pinch must be held before click fires
GESTURE_COOLDOWN = 0.6  # Seconds before same gesture can fire again

SCROLL_SPEED = 80  # Scroll units per tick (higher = faster)
SCROLL_SENSITIVITY = 0.12  # Hand Y-movement multiplier for scrolling

FPS_AUTO_PAUSE_THRESHOLD = 8  # FPS below this triggers auto-pause
HAND_LOSS_PAUSE_DELAY = 1.5  # Seconds after hand disappears before auto-pause

DASHBOARD_FONT_SCALE = 0.65  # HUD text size
DASHBOARD_THICKNESS = 2  # HUD text stroke weight
BORDER_FLASH_THICKNESS = 8  # Colored border thickness around frame

KILL_KEY = ord('q')  # Keyboard key to quit (lowercase q)
