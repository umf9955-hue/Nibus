# MediaPipe Installation Issue - Solution

## Problem
MediaPipe doesn't support Python 3.13 yet. It only supports Python 3.8-3.11.

## Solution Options

### Option 1: Use Python 3.11 or 3.12 (Recommended)

1. **Download Python 3.11 or 3.12:**
   - Go to: https://www.python.org/downloads/
   - Download Python 3.11.9 or 3.12.x
   - Install it (check "Add Python to PATH" during installation)

2. **Verify installation:**
   ```powershell
   python3.11 --version
   ```
   or
   ```powershell
   python3.12 --version
   ```

3. **Install dependencies with Python 3.11/3.12:**
   ```powershell
   python3.11 -m pip install PyQt6 mediapipe requests SpeechRecognition pyttsx3
   ```
   or
   ```powershell
   python3.12 -m pip install PyQt6 mediapipe requests SpeechRecognition pyttsx3
   ```

4. **Run the application:**
   ```powershell
   python3.11 main.py
   ```
   or
   ```powershell
   python3.12 main.py
   ```

### Option 2: Create Virtual Environment with Python 3.11

If you have Python 3.11 installed:

```powershell
# Create virtual environment with Python 3.11
py -3.11 -m venv venv

# Activate it
.\venv\Scripts\Activate.ps1

# Install packages
pip install PyQt6 mediapipe requests SpeechRecognition pyttsx3

# Run
python main.py
```

### Option 3: Use Alternative Hand Tracking (No MediaPipe)

I can create a version that uses OpenCV for basic hand tracking instead of MediaPipe. This will work with Python 3.13 but with less accurate gesture recognition.


