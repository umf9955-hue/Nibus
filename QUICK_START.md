# Quick Start Guide

## Installation (Choose One Method)

### Method 1: Batch Script (Easiest)
Double-click `quick_install.bat` and wait for installation to complete.

### Method 2: Manual Command
Open PowerShell in this folder and run:
```powershell
python -m pip install PyQt6 mediapipe requests SpeechRecognition pyttsx3
```

### Method 3: One at a Time (If having issues)
```powershell
python -m pip install PyQt6
python -m pip install mediapipe  
python -m pip install requests
python -m pip install SpeechRecognition
python -m pip install pyttsx3
```

## After Installation

1. **Test if dependencies are installed:**
   ```powershell
   python test_setup.py
   ```

2. **Run the application:**
   ```powershell
   python main.py
   ```

## Troubleshooting

- **If PyQt6 fails**: Try `python -m pip install --upgrade pip` first
- **If MediaPipe fails**: It might take a few minutes to download
- **Python 3.13**: Some packages might need Python 3.11 or 3.12

## What You'll See

When the app runs:
- Black fullscreen window (or windowed if fullscreen disabled)
- Widgets: Clock, Weather, Calendar, News, Notes
- Virtual cursor (white circle) that follows your index finger
- Pinch to drag widgets around

## Controls

- **Index Finger**: Move cursor
- **Pinch (Thumb + Index)**: Drag widgets
- **Release Pinch**: Drop widget
- **F11**: Toggle fullscreen
- **ESC**: Exit


