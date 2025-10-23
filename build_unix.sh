#!/bin/bash
# Build script for Linux and macOS
# Creates standalone executable

set -e  # Exit on error

echo "===================================="
echo "Building Dinosaur Island"
echo "Platform: $(uname -s)"
echo "===================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 not found!"
    echo "Install Python 3 from your package manager"
    exit 1
fi

echo "Python version: $(python3 --version)"

# Check if PyInstaller is installed
if ! python3 -c "import PyInstaller" &> /dev/null; then
    echo "Installing PyInstaller..."
    pip3 install pyinstaller
fi

# Clean previous builds
rm -rf build dist

# Build executable
echo ""
echo "Building executable..."
pyinstaller DinosaurIsland.spec

# Check if build succeeded
if [[ "$(uname -s)" == "Darwin" ]]; then
    # macOS
    if [ -d "dist/DinosaurIsland.app" ]; then
        echo ""
        echo "===================================="
        echo "SUCCESS! App bundle created:"
        echo "dist/DinosaurIsland.app"
        echo "===================================="
        echo ""
        echo "You can now:"
        echo "1. Open: open dist/DinosaurIsland.app"
        echo "2. Move to Applications folder"
        echo "3. Distribute the .app bundle"
    else
        echo "ERROR: Build failed!"
        exit 1
    fi
else
    # Linux
    if [ -f "dist/DinosaurIsland" ]; then
        chmod +x dist/DinosaurIsland
        echo ""
        echo "===================================="
        echo "SUCCESS! Executable created:"
        echo "dist/DinosaurIsland"
        echo "===================================="
        echo ""
        echo "You can now:"
        echo "1. Run: ./dist/DinosaurIsland"
        echo "2. Distribute the executable"
        echo "3. Create AppImage (see PACKAGING.md)"
    else
        echo "ERROR: Build failed!"
        exit 1
    fi
fi
