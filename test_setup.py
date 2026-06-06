#!/usr/bin/env python3
"""Quick test to verify all dependencies are installed"""

import sys

print("Testing dependencies...\n")

dependencies = {
    'PyQt6': 'PyQt6',
    'MediaPipe': 'mediapipe',
    'OpenCV': 'cv2',
    'NumPy': 'numpy',
    'Requests': 'requests',
}

missing = []
for name, module in dependencies.items():
    try:
        __import__(module)
        print(f"✅ {name} - OK")
    except ImportError as e:
        print(f"❌ {name} - MISSING")
        missing.append(name)

if missing:
    print(f"\n⚠️  Missing dependencies: {', '.join(missing)}")
    print("Please install them with: pip install " + " ".join(missing))
    sys.exit(1)
else:
    print("\n✅ All dependencies installed!")
    print("You can now run: python main.py")

