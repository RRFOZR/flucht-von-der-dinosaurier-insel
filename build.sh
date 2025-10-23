#!/bin/bash
# 🦕 Build script for macOS and Linux
# Creates standalone executable for Dinosaur Island game

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔══════════════════════════════════════════╗"
echo "║  🦕 Dinosaur Island Builder 🦕          ║"
echo "║  Building for macOS and Linux           ║"
echo "╚══════════════════════════════════════════╝"
echo -e "${NC}"

# Detect OS
OS="$(uname -s)"
case "${OS}" in
    Linux*)     PLATFORM="Linux";;
    Darwin*)    PLATFORM="macOS";;
    *)          echo -e "${RED}❌ Unsupported OS: ${OS}${NC}"; exit 1;;
esac

echo -e "${BLUE}🖥️  Platform: ${PLATFORM}${NC}"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 not found!${NC}"
    echo "   Install Python 3 from your package manager"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d ' ' -f 2)
echo -e "${GREEN}✅ Python ${PYTHON_VERSION}${NC}"

# Check/Install PyInstaller
if ! python3 -c "import PyInstaller" &> /dev/null 2>&1; then
    echo -e "${YELLOW}📦 Installing PyInstaller...${NC}"
    pip3 install pyinstaller --quiet
    echo -e "${GREEN}✅ PyInstaller installed${NC}"
else
    PYINST_VERSION=$(python3 -c "import PyInstaller; print(PyInstaller.__version__)")
    echo -e "${GREEN}✅ PyInstaller ${PYINST_VERSION}${NC}"
fi

# Clean previous builds
echo ""
echo -e "${YELLOW}🧹 Cleaning previous builds...${NC}"
rm -rf build dist

# Build executable
echo ""
echo -e "${BLUE}🔨 Building executable...${NC}"
echo "   This may take 1-2 minutes..."
echo ""

pyinstaller --clean DinosaurIsland-Unix.spec 2>&1 | grep -E '(INFO: Building|ERROR|WARNING|completed successfully)' || true

# Check result
echo ""
if [[ "${PLATFORM}" == "macOS" ]]; then
    if [ -d "dist/DinosaurIsland.app" ]; then
        SIZE=$(du -sh dist/DinosaurIsland.app | cut -f1)
        echo -e "${GREEN}"
        echo "╔══════════════════════════════════════════╗"
        echo "║        ✅ BUILD SUCCESSFUL! ✅           ║"
        echo "╚══════════════════════════════════════════╝"
        echo -e "${NC}"
        echo ""
        echo -e "${GREEN}📦 App Bundle Created:${NC}"
        echo "   Location: dist/DinosaurIsland.app"
        echo "   Size: ${SIZE}"
        echo ""
        echo -e "${BLUE}🚀 How to use:${NC}"
        echo "   1. Test it:     open dist/DinosaurIsland.app"
        echo "   2. Move it:     mv dist/DinosaurIsland.app /Applications/"
        echo "   3. Share it:    zip -r DinosaurIsland.zip dist/DinosaurIsland.app"
        echo ""
        echo -e "${YELLOW}💡 Tip: First run requires right-click → Open to bypass Gatekeeper${NC}"
    else
        echo -e "${RED}❌ Build failed! Check errors above.${NC}"
        exit 1
    fi
elif [[ "${PLATFORM}" == "Linux" ]]; then
    if [ -f "dist/DinosaurIsland" ]; then
        chmod +x dist/DinosaurIsland
        SIZE=$(du -sh dist/DinosaurIsland | cut -f1)
        echo -e "${GREEN}"
        echo "╔══════════════════════════════════════════╗"
        echo "║        ✅ BUILD SUCCESSFUL! ✅           ║"
        echo "╚══════════════════════════════════════════╝"
        echo -e "${NC}"
        echo ""
        echo -e "${GREEN}🐧 Executable Created:${NC}"
        echo "   Location: dist/DinosaurIsland"
        echo "   Size: ${SIZE}"
        echo ""
        echo -e "${BLUE}🚀 How to use:${NC}"
        echo "   1. Test it:     ./dist/DinosaurIsland"
        echo "   2. Install it:  sudo cp dist/DinosaurIsland /usr/local/bin/"
        echo "   3. Share it:    tar -czf DinosaurIsland-Linux.tar.gz dist/DinosaurIsland"
        echo ""
        echo -e "${YELLOW}💡 Tip: Create AppImage for maximum portability (see docs)${NC}"
    else
        echo -e "${RED}❌ Build failed! Check errors above.${NC}"
        exit 1
    fi
fi

echo ""
echo -e "${GREEN}🎮 Ready to play!${NC}"
echo ""
