# GestureMouse Pro 🖐️🖱️

A real-time AI-powered virtual mouse controller built with Python, OpenCV, and MediaPipe that lets users control their computer cursor using hand gestures through a webcam.

GestureMouse Pro transforms hand movements into smooth mouse interactions including cursor movement, left click, right click, scrolling, pause mode, and drag-and-drop — all without touching a physical mouse.

---

## ✨ Features

- 🎯 Real-time hand tracking using MediaPipe
- 🖱️ Smooth cursor movement with motion smoothing
- 👆 Left-click gesture detection
- 👉 Right-click gesture detection
- ✌️ Scroll mode with gesture control
- ✊ Pause mode for safety
- 🟡 Drag-and-drop gesture support
- 📊 Live OpenCV dashboard HUD
- ⚡ FPS monitoring with auto-pause protection
- 🧠 Palm-center based tracking for stable movement
- 🔒 Cooldown protection against accidental clicks
- 🌍 Cross-platform support (Windows / Linux / macOS)

---

# 📸 Demo

> Add screenshots or GIFs here after uploading your project demo.

Example:
- Cursor movement
- Drag mode
- Scroll mode
- Dashboard overlay

---

# 🚀 Quick Start

## 1️⃣ Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/GestureMouse-Pro.git
cd GestureMouse-Pro
```

---

## 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 3️⃣ Run the Application

```bash
python main.py
```

---

# 🧠 Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| OpenCV | Webcam capture & rendering |
| MediaPipe | Hand landmark tracking |
| PyAutoGUI | Mouse automation |
| NumPy | Mathematical operations |
| ScreenInfo | Dynamic monitor resolution |

---

# 🎮 Gesture Controls

| Gesture | Action |
|---|---|
| ☝ Index finger up | Move Cursor |
| 🤏 Thumb + Index pinch | Left Click |
| 🤏 Thumb + Middle pinch | Right Click |
| ✌️ Two fingers up | Scroll Mode |
| ✊ Closed fist (hold still) | Pause Mode |
| ✊ Move fist while holding | Drag & Drop |

---

# 🖥️ Dashboard HUD

GestureMouse Pro includes a real-time visual dashboard displaying:

- Current mode
- FPS counter
- Active gesture
- Hand detection status
- Visual border feedback
- Mode transition animations

---

# ⚙️ Configuration

All tunable settings are available inside:

```bash
config.py
```

You can customize:

- Cursor sensitivity
- Smoothing factor
- Scroll speed
- Gesture cooldowns
- Camera resolution
- FPS thresholds
- Click sensitivity
- HUD appearance

---

# 📂 Project Structure

```bash
gesture_mouse_pro/
│
├── main.py
├── config.py
├── gesture_engine.py
├── mouse_controller.py
├── dashboard.py
├── requirements.txt
├── setup.bat
├── setup.sh
└── README.md
```

---

# 🔥 Advanced Features

## Palm-Center Cursor Tracking
Instead of tracking fingertip movement, the cursor follows the palm center for improved click stability and smoother motion.

## Smart Drag Detection
The system intelligently differentiates between:

- Pause Intent
- Drag Intent

using movement thresholds and hold timers.

## FPS Auto Protection
If FPS drops below a safe threshold, the system automatically pauses to prevent accidental cursor behavior.

---

# 🛠️ Installation Scripts

### Windows

```bash
setup.bat
```

### Linux / macOS

```bash
chmod +x setup.sh
./setup.sh
```

---

# 🧩 Requirements

- Python 3.11 or 3.12
- Webcam
- Good lighting conditions

---

# ⚠️ Troubleshooting

## Camera Not Opening

- Check webcam permissions
- Verify `CAMERA_INDEX` in `config.py`
- Close other apps using the camera

---

## Cursor Feels Laggy

Increase:

```python
SMOOTHING_FACTOR
MOVE_SENSITIVITY
```

inside `config.py`

---

## Clicks Not Registering

- Improve lighting
- Move hand closer to camera
- Reduce pinch distance threshold

---

## Cursor Shaking

- Keep hand steady
- Ensure background is not cluttered
- Lower movement sensitivity slightly

---

# 📈 Future Improvements

- Multi-monitor support
- Custom gesture mapping
- AI gesture training
- Voice command integration
- Gesture macros
- Wireless mobile camera support

---

# 🤝 Contributing

Pull requests are welcome.

For major changes, please open an issue first to discuss what you'd like to improve.

---

# 📜 License

MIT License

---

# ⭐ Support

If you like this project, consider giving it a ⭐ on GitHub.

It helps a lot and motivates future development 🚀

---

# 👨‍💻 Author

Developed by **ABHAY SINGH CHOUHAN**
Built using Computer Vision + Human Gesture Interaction concepts.
