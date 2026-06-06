#!/usr/bin/env python3
"""Install dependencies and run the application"""

import subprocess
import sys
import os

def install_package(package):
    """Install a package and show output"""
    print(f"\n{'='*60}")
    print(f"Installing {package}...")
    print('='*60)
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'install', package],
            capture_output=False,
            text=True
        )
        if result.returncode == 0:
            print(f"✅ {package} installed successfully!")
            return True
        else:
            print(f"❌ {package} installation failed!")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def check_package(package_name, import_name):
    """Check if a package is installed"""
    try:
        __import__(import_name)
        return True
    except ImportError:
        return False

def main():
    print("Smart Mirror - Dependency Installer & Launcher")
    print("="*60)
    
    # Check what's already installed
    packages_to_install = []
    
    if not check_package('PyQt6', 'PyQt6.QtWidgets'):
        packages_to_install.append('PyQt6')
    else:
        print("✅ PyQt6 already installed")
    
    if not check_package('MediaPipe', 'mediapipe'):
        packages_to_install.append('mediapipe')
    else:
        print("✅ MediaPipe already installed")
    
    if not check_package('Requests', 'requests'):
        packages_to_install.append('requests')
    else:
        print("✅ Requests already installed")
    
    if not check_package('SpeechRecognition', 'speech_recognition'):
        packages_to_install.append('SpeechRecognition')
    else:
        print("✅ SpeechRecognition already installed")
    
    if not check_package('pyttsx3', 'pyttsx3'):
        packages_to_install.append('pyttsx3')
    else:
        print("✅ pyttsx3 already installed")
    
    # Install missing packages
    if packages_to_install:
        print(f"\nNeed to install: {', '.join(packages_to_install)}")
        response = input("\nInstall now? (y/n): ").lower().strip()
        
        if response == 'y':
            for package in packages_to_install:
                if not install_package(package):
                    print(f"\n⚠️  Installation of {package} failed!")
                    print("Please install manually: pip install " + package)
                    return
        
        print("\n✅ All packages installed!")
    else:
        print("\n✅ All dependencies are already installed!")
    
    # Try to run the application
    print("\n" + "="*60)
    print("Starting Smart Mirror...")
    print("="*60)
    print("\nPress Ctrl+C to stop\n")
    
    try:
        # Import and run
        os.system(f'{sys.executable} main.py')
    except KeyboardInterrupt:
        print("\n\nApplication stopped by user.")
    except Exception as e:
        print(f"\n❌ Error running application: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()


