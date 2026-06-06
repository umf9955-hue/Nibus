# How to Run the Smart Mirror

## Quick Start (Easiest Method)

**Just run this command:**
```powershell
python install_and_run.py
```

This script will:
1. Check what's installed
2. Install missing packages automatically
3. Launch the application

## Manual Installation

If the script doesn't work, install manually:

```powershell
python -m pip install PyQt6
python -m pip install mediapipe
python -m pip install requests
python -m pip install SpeechRecognition
python -m pip install pyttsx3
```

Then run:
```powershell
python main.py
```

## Troubleshooting

### If PyQt6 won't install:
- Try: `python -m pip install --upgrade pip` first
- Then: `python -m pip install PyQt6 --user`

### If you get "ModuleNotFoundError":
- Make sure you're using the same Python that has the packages
- Check: `python -m pip list` to see installed packages

### Python 3.13 Issues:
Some packages might not have wheels for Python 3.13 yet. If installation fails, consider using Python 3.11 or 3.12.

## What to Expect

When the app runs:
- A black window will open (fullscreen by default)
- You'll see widgets: Clock, Weather, Calendar, News, Notes
- Point your index finger at the camera - a white cursor should appear
- Pinch (thumb + index) to drag widgets
- Release to drop

## Controls

- **F11**: Toggle fullscreen
- **ESC**: Exit application


