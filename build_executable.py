#!/usr/bin/env python3
"""
PyInstaller build script for Flucht von der Dinosaurier-Insel
Creates standalone executables for Windows, Mac, and Linux

Usage:
    python build_executable.py
"""

import PyInstaller.__main__
import os
import sys
import platform

def build_executable():
    """Build standalone executable with PyInstaller."""

    # Detect platform
    system = platform.system()

    # Common PyInstaller arguments
    args = [
        'main.py',                          # Entry point
        '--name=DinosaurIsland',            # Executable name
        '--onefile',                        # Single executable file
        '--windowed',                       # No console window (GUI only)
        '--icon=konrad_insel/icon.png' if os.path.exists('konrad_insel/icon.png') else '',

        # Include all game assets
        '--add-data=konrad_insel:konrad_insel',

        # Include all Python modules
        '--hidden-import=pygame',
        '--hidden-import=numpy',
        '--collect-all=pygame',

        # Optimization
        '--optimize=2',

        # Clean build
        '--clean',

        # Logging
        '--log-level=INFO',
    ]

    # Platform-specific settings
    if system == 'Windows':
        print("🪟 Building for Windows...")
        # Add version info for Windows
        args.extend([
            '--version-file=version_info.txt' if os.path.exists('version_info.txt') else '',
        ])
    elif system == 'Darwin':  # macOS
        print("🍎 Building for macOS...")
        args.extend([
            '--osx-bundle-identifier=com.weberfamily.dinosaurisland',
        ])
    elif system == 'Linux':
        print("🐧 Building for Linux...")

    # Remove empty arguments
    args = [arg for arg in args if arg]

    print(f"\n📦 Building executable with PyInstaller...")
    print(f"   Platform: {system}")
    print(f"   Python: {sys.version.split()[0]}")
    print(f"   Arguments: {' '.join(args)}\n")

    # Run PyInstaller
    PyInstaller.__main__.run(args)

    print("\n✅ Build complete!")
    print(f"   Executable: dist/DinosaurIsland{'.exe' if system == 'Windows' else ''}")
    print(f"   Size: ~{get_dir_size('dist')} MB\n")

def get_dir_size(path):
    """Get directory size in MB."""
    total = 0
    try:
        for entry in os.scandir(path):
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_dir_size(entry.path)
    except FileNotFoundError:
        return 0
    return round(total / (1024 * 1024), 1)

if __name__ == '__main__':
    # Check if PyInstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("❌ PyInstaller not found!")
        print("   Install with: pip install pyinstaller")
        sys.exit(1)

    # Check if main.py exists
    if not os.path.exists('main.py'):
        print("❌ main.py not found!")
        print("   Run this script from the game directory")
        sys.exit(1)

    build_executable()
