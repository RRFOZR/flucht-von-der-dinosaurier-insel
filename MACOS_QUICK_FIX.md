# 🍎 macOS .app Won't Open? - Quick Fix Guide

## 🚀 Try These (in order)

### Fix 1: Remove Quarantine (Most Common Fix!)

```bash
xattr -cr dist/DinosaurIsland.app
open dist/DinosaurIsland.app
```

**This fixes 80% of cases!**

---

### Fix 2: Right-Click to Open

1. Right-click on `DinosaurIsland.app` in Finder
2. Click "Open"
3. Click "Open" again in the dialog

---

### Fix 3: See the Actual Error

```bash
dist/DinosaurIsland.app/Contents/MacOS/DinosaurIsland
```

This will show you what's actually wrong!

---

### Fix 4: Rebuild with macOS-Specific Script

```bash
./build_macos.sh
```

This uses the macOS-optimized spec file.

---

### Fix 5: Run Diagnostics

```bash
./diagnose_macos.sh
```

This will tell you exactly what's wrong!

---

## 🔍 Common Errors & Fixes

### "App is damaged"
```bash
xattr -cr dist/DinosaurIsland.app
```

### "pygame not found"
```bash
pip3 install --force-reinstall pygame
./build_macos.sh
```

### "SDL2 framework not found"
```bash
brew install sdl2 sdl2_mixer sdl2_ttf
./build_macos.sh
```

### Blank window or immediate crash
```bash
# Check Console.app for errors
open -a Console

# Or run diagnostics
./diagnose_macos.sh
```

---

## 📋 Complete Rebuild (if all else fails)

```bash
# Clean everything
rm -rf build dist

# Reinstall dependencies
pip3 install --force-reinstall pygame pyinstaller

# Rebuild
./build_macos.sh

# Remove quarantine
xattr -cr dist/DinosaurIsland.app

# Open
open dist/DinosaurIsland.app
```

---

## 💻 Alternative: Run Without .app

If the .app still doesn't work, just run the Python version:

```bash
pip3 install pygame
python3 main.py
```

This always works! The .app is just for convenience.

---

## 📚 Need More Help?

See **MACOS_TROUBLESHOOTING.md** for detailed solutions to all issues!

---

## 🎯 Most Likely Solution

**99% of the time, this is all you need:**

```bash
xattr -cr dist/DinosaurIsland.app
open dist/DinosaurIsland.app
```

Done! 🎉
