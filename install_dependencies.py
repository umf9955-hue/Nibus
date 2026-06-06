#!/usr/bin/env python3
"""Install all required dependencies"""

import subprocess
import sys

dependencies = [
    'PyQt6',
    'mediapipe',
    'requests',
    'numpy',
    'opencv-python',
    'pillow',
    'SpeechRecognition',
    'pyttsx3',
]

print("Installing dependencies...\n")

for dep in dependencies:
    print(f"Installing {dep}...")
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'install', dep],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"✅ {dep} installed successfully")
        else:
            print(f"❌ {dep} installation failed:")
            print(result.stderr)
    except Exception as e:
        print(f"❌ Error installing {dep}: {e}")

print("\n" + "="*50)
print("Installation complete!")
print("Run 'python test_setup.py' to verify installation")


