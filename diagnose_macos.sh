#!/bin/bash
# Diagnostic script for macOS .app issues
# Run this to find out why the app won't open

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🔍 Diagnosing macOS .app issue...${NC}"
echo ""

# Check if .app exists
if [ ! -d "dist/DinosaurIsland.app" ]; then
    echo -e "${RED}❌ dist/DinosaurIsland.app not found!${NC}"
    echo "   Run ./build.sh first"
    exit 1
fi

echo -e "${GREEN}✅ App bundle found${NC}"
echo ""

# Check the actual executable
EXEC_PATH="dist/DinosaurIsland.app/Contents/MacOS/DinosaurIsland"

if [ ! -f "$EXEC_PATH" ]; then
    echo -e "${RED}❌ Executable not found at: $EXEC_PATH${NC}"
    echo ""
    echo "Checking bundle structure:"
    ls -la dist/DinosaurIsland.app/Contents/
    exit 1
fi

echo -e "${GREEN}✅ Executable found${NC}"
echo ""

# Check permissions
if [ -x "$EXEC_PATH" ]; then
    echo -e "${GREEN}✅ Executable permissions OK${NC}"
else
    echo -e "${RED}❌ Executable not executable! Fixing...${NC}"
    chmod +x "$EXEC_PATH"
    echo -e "${GREEN}✅ Fixed permissions${NC}"
fi
echo ""

# Check file type
echo -e "${BLUE}📋 Executable info:${NC}"
file "$EXEC_PATH"
echo ""

# Try to run and capture error
echo -e "${BLUE}🚀 Attempting to run executable directly...${NC}"
echo ""

# Run the executable and capture output
"$EXEC_PATH" 2>&1 | head -20 || {
    ERROR_CODE=$?
    echo ""
    echo -e "${RED}❌ Executable failed with error code: $ERROR_CODE${NC}"
    echo ""
}

# Check Console.app for crash logs
echo ""
echo -e "${YELLOW}💡 To see detailed error logs:${NC}"
echo "   1. Open Console.app"
echo "   2. Search for 'DinosaurIsland'"
echo "   3. Look for crash reports"
echo ""

# Check Gatekeeper status
echo -e "${BLUE}🔒 Checking Gatekeeper status...${NC}"
spctl -a -vv "dist/DinosaurIsland.app" 2>&1 || {
    echo ""
    echo -e "${YELLOW}⚠️  App is not signed (expected for development)${NC}"
    echo ""
    echo -e "${BLUE}To bypass Gatekeeper:${NC}"
    echo "   1. Right-click the app"
    echo "   2. Choose 'Open'"
    echo "   3. Click 'Open' in the dialog"
    echo ""
    echo "   OR run this command:"
    echo "   xattr -cr dist/DinosaurIsland.app"
}

echo ""
echo -e "${BLUE}📦 Checking for common issues...${NC}"
echo ""

# Check if pygame is installed
if python3 -c "import pygame" 2>/dev/null; then
    echo -e "${GREEN}✅ pygame is installed${NC}"
else
    echo -e "${RED}❌ pygame not found!${NC}"
    echo "   Install with: pip3 install pygame"
fi

# Check SDL libraries
echo ""
echo -e "${BLUE}🔍 Checking for SDL libraries...${NC}"
if [ -d "/opt/homebrew/lib" ]; then
    SDLS=$(ls /opt/homebrew/lib/libSDL2* 2>/dev/null || echo "")
    if [ -n "$SDLS" ]; then
        echo -e "${GREEN}✅ SDL2 libraries found in /opt/homebrew/lib${NC}"
    fi
fi

if [ -d "/usr/local/lib" ]; then
    SDLS=$(ls /usr/local/lib/libSDL2* 2>/dev/null || echo "")
    if [ -n "$SDLS" ]; then
        echo -e "${GREEN}✅ SDL2 libraries found in /usr/local/lib${NC}"
    fi
fi

# Check Info.plist
echo ""
echo -e "${BLUE}📄 Checking Info.plist...${NC}"
if [ -f "dist/DinosaurIsland.app/Contents/Info.plist" ]; then
    echo -e "${GREEN}✅ Info.plist exists${NC}"
    echo ""
    echo "Bundle identifier:"
    /usr/libexec/PlistBuddy -c "Print :CFBundleIdentifier" "dist/DinosaurIsland.app/Contents/Info.plist" 2>/dev/null || echo "  (not set)"
else
    echo -e "${RED}❌ Info.plist missing${NC}"
fi

echo ""
echo -e "${BLUE}════════════════════════════════════════${NC}"
echo -e "${YELLOW}💡 COMMON FIXES:${NC}"
echo ""
echo "1. Remove quarantine attribute:"
echo "   xattr -cr dist/DinosaurIsland.app"
echo ""
echo "2. Try opening with right-click → Open"
echo ""
echo "3. Check Console.app for detailed errors"
echo ""
echo "4. Reinstall pygame without framework:"
echo "   pip3 uninstall pygame"
echo "   pip3 install pygame --no-binary pygame"
echo ""
echo "5. Run executable directly to see errors:"
echo "   dist/DinosaurIsland.app/Contents/MacOS/DinosaurIsland"
echo ""
echo -e "${BLUE}════════════════════════════════════════${NC}"
