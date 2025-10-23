#!/bin/bash
# macOS-specific build script with proper pygame handling
# Fixes common macOS app bundle issues

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}"
echo "╔══════════════════════════════════════════╗"
echo "║  🍎 Dinosaur Island - macOS Builder 🍎  ║"
echo "╚══════════════════════════════════════════╝"
echo -e "${NC}"

# Verify we're on macOS
if [ "$(uname -s)" != "Darwin" ]; then
    echo -e "${RED}❌ This script is for macOS only!${NC}"
    echo "   For Linux, use: ./build.sh"
    exit 1
fi

echo -e "${GREEN}✅ Running on macOS${NC}"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 not found!${NC}"
    echo "   Install with: brew install python3"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d ' ' -f 2)
echo -e "${GREEN}✅ Python ${PYTHON_VERSION}${NC}"

# Check pygame installation
echo ""
echo -e "${BLUE}🎮 Checking pygame installation...${NC}"

if ! python3 -c "import pygame" 2>/dev/null; then
    echo -e "${YELLOW}⚠️  pygame not found, installing...${NC}"
    pip3 install pygame
fi

echo -e "${GREEN}✅ pygame installed${NC}"

# Check/Install PyInstaller
echo ""
echo -e "${BLUE}📦 Checking PyInstaller...${NC}"

if ! python3 -c "import PyInstaller" &> /dev/null 2>&1; then
    echo -e "${YELLOW}Installing PyInstaller...${NC}"
    pip3 install pyinstaller
    echo -e "${GREEN}✅ PyInstaller installed${NC}"
else
    PYINST_VERSION=$(python3 -c "import PyInstaller; print(PyInstaller.__version__)")
    echo -e "${GREEN}✅ PyInstaller ${PYINST_VERSION}${NC}"
fi

# Clean previous builds
echo ""
echo -e "${YELLOW}🧹 Cleaning previous builds...${NC}"
rm -rf build dist

# Build with macOS-specific spec file
echo ""
echo -e "${BLUE}🔨 Building macOS app bundle...${NC}"
echo "   This may take 2-3 minutes..."
echo ""

# Use macOS-specific spec file if it exists, otherwise fall back to Unix spec
if [ -f "DinosaurIsland-macOS.spec" ]; then
    SPEC_FILE="DinosaurIsland-macOS.spec"
    echo -e "${BLUE}Using macOS-optimized spec file${NC}"
else
    SPEC_FILE="DinosaurIsland-Unix.spec"
    echo -e "${YELLOW}Using generic Unix spec file${NC}"
fi

pyinstaller --clean "$SPEC_FILE" 2>&1 | grep -E '(INFO: Building|ERROR|WARNING|completed successfully)' || true

# Check if build succeeded
echo ""
if [ -d "dist/DinosaurIsland.app" ]; then
    SIZE=$(du -sh dist/DinosaurIsland.app | cut -f1)

    # Remove quarantine attribute immediately
    echo -e "${BLUE}🔓 Removing quarantine attribute...${NC}"
    xattr -cr dist/DinosaurIsland.app

    # Make sure executable is executable
    chmod +x dist/DinosaurIsland.app/Contents/MacOS/DinosaurIsland 2>/dev/null || true

    echo ""
    echo -e "${GREEN}"
    echo "╔══════════════════════════════════════════╗"
    echo "║        ✅ BUILD SUCCESSFUL! ✅           ║"
    echo "╚══════════════════════════════════════════╝"
    echo -e "${NC}"
    echo ""
    echo -e "${GREEN}🍎 App Bundle Created:${NC}"
    echo "   Location: dist/DinosaurIsland.app"
    echo "   Size: ${SIZE}"
    echo ""
    echo -e "${BLUE}🚀 How to use:${NC}"
    echo "   1. Test it:     open dist/DinosaurIsland.app"
    echo "   2. Move it:     mv dist/DinosaurIsland.app /Applications/"
    echo "   3. Share it:    ditto -c -k --keepParent dist/DinosaurIsland.app DinosaurIsland.zip"
    echo ""
    echo -e "${GREEN}💡 Tips:${NC}"
    echo "   • Quarantine attribute already removed"
    echo "   • If it doesn't open, run: ./diagnose_macos.sh"
    echo "   • Check Console.app for detailed error logs"
    echo ""

    # Try to open the app
    echo -e "${BLUE}🎮 Opening the app...${NC}"
    open dist/DinosaurIsland.app || {
        echo ""
        echo -e "${YELLOW}⚠️  Could not auto-open the app${NC}"
        echo "   Try opening manually: open dist/DinosaurIsland.app"
        echo "   Or run diagnostics: ./diagnose_macos.sh"
    }

else
    echo -e "${RED}"
    echo "╔══════════════════════════════════════════╗"
    echo "║          ❌ BUILD FAILED! ❌             ║"
    echo "╚══════════════════════════════════════════╝"
    echo -e "${NC}"
    echo ""
    echo -e "${RED}App bundle was not created!${NC}"
    echo ""
    echo -e "${YELLOW}Common fixes:${NC}"
    echo "1. Reinstall pygame: pip3 install --force-reinstall pygame"
    echo "2. Update PyInstaller: pip3 install --upgrade pyinstaller"
    echo "3. Check the error messages above"
    echo "4. Run diagnostics: ./diagnose_macos.sh"
    echo ""
    exit 1
fi
