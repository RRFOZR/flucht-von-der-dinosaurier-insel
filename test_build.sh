#!/bin/bash
# Quick test script to verify the built executable works

set -e

BLUE='\033[0;34m'
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}🧪 Testing DinosaurIsland executable...${NC}"
echo ""

# Check if executable exists
if [ -f "dist/DinosaurIsland" ]; then
    echo -e "${GREEN}✅ Executable found: dist/DinosaurIsland${NC}"
elif [ -d "dist/DinosaurIsland.app" ]; then
    echo -e "${GREEN}✅ App bundle found: dist/DinosaurIsland.app${NC}"
else
    echo -e "${RED}❌ No executable found! Run ./build.sh first${NC}"
    exit 1
fi

# Check permissions
if [ -f "dist/DinosaurIsland" ]; then
    if [ -x "dist/DinosaurIsland" ]; then
        echo -e "${GREEN}✅ Executable permissions set${NC}"
    else
        echo -e "${RED}❌ Not executable! Setting permissions...${NC}"
        chmod +x dist/DinosaurIsland
        echo -e "${GREEN}✅ Permissions fixed${NC}"
    fi
fi

# Check file type
echo ""
echo -e "${BLUE}📋 File info:${NC}"
if [ -f "dist/DinosaurIsland" ]; then
    file dist/DinosaurIsland
    echo ""
    echo -e "${BLUE}📦 Size:${NC}"
    du -sh dist/DinosaurIsland
elif [ -d "dist/DinosaurIsland.app" ]; then
    echo "macOS Application Bundle"
    echo ""
    echo -e "${BLUE}📦 Size:${NC}"
    du -sh dist/DinosaurIsland.app
fi

echo ""
echo -e "${GREEN}✅ Build test passed!${NC}"
echo ""
echo -e "${BLUE}🎮 To run the game:${NC}"
if [ -f "dist/DinosaurIsland" ]; then
    echo "   ./dist/DinosaurIsland"
elif [ -d "dist/DinosaurIsland.app" ]; then
    echo "   open dist/DinosaurIsland.app"
fi
echo ""
