#!/bin/bash
# Check what's actually bundled in the .app

echo "🔍 Checking DinosaurIsland.app bundle contents..."
echo ""

if [ ! -d "dist/DinosaurIsland.app" ]; then
    echo "❌ dist/DinosaurIsland.app not found!"
    exit 1
fi

echo "📦 App bundle structure:"
echo ""
echo "Contents directory:"
ls -la dist/DinosaurIsland.app/Contents/

echo ""
echo "MacOS directory:"
ls -la dist/DinosaurIsland.app/Contents/MacOS/ | head -20

echo ""
echo "Frameworks directory (if exists):"
if [ -d "dist/DinosaurIsland.app/Contents/Frameworks" ]; then
    ls -la dist/DinosaurIsland.app/Contents/Frameworks/ | head -20
else
    echo "  (Frameworks directory doesn't exist)"
fi

echo ""
echo "Resources directory (if exists):"
if [ -d "dist/DinosaurIsland.app/Contents/Resources" ]; then
    ls -la dist/DinosaurIsland.app/Contents/Resources/ | head -20
else
    echo "  (Resources directory doesn't exist)"
fi

echo ""
echo "🔍 Looking for konrad_insel directory..."
find dist/DinosaurIsland.app -name "konrad_insel" -type d

echo ""
echo "🔍 Looking for sound files..."
find dist/DinosaurIsland.app -name "*.mp3" | head -10

echo ""
echo "💡 Checking sys._MEIPASS location..."
echo "   (Where PyInstaller actually extracts files)"
echo ""
echo "   When app runs, check this path for assets"
