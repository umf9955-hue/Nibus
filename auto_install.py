#!/usr/bin/env python3
"""Auto-install dependencies and run"""

import subprocess
import sys
import os

packages = ['PyQt6', 'mediapipe', 'requests', 'SpeechRecognition', 'pyttsx3']

print("Installing dependencies...")
print("="*60)

for package in packages:
    print(f"\nInstalling {package}...")
    subprocess.run([sys.executable, '-m', 'pip', 'install', package])

print("\n" + "="*60)
print("Installation complete! Starting application...")
print("="*60)
print("\nPress Ctrl+C to stop\n")

os.system(f'{sys.executable} main.py')


