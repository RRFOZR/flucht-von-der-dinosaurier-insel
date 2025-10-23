# 🍎 macOS Troubleshooting Guide

Having trouble with the DinosaurIsland.app? This guide will help you fix it!

---

## 🚨 Common Issues

### Issue 1: App Won't Open (Bounces and Quits)

**Symptoms:**
- App icon bounces in dock
- Immediately quits
- No error message

**Fixes:**

#### Fix A: Remove Quarantine Attribute
macOS blocks unsigned apps downloaded from the internet.

```bash
xattr -cr dist/DinosaurIsland.app
```

Then try opening again.

#### Fix B: Right-Click to Open
1. Right-click (or Control+Click) on DinosaurIsland.app
2. Select "Open"
3. Click "Open" in the security dialog

This tells Gatekeeper to allow the app.

#### Fix C: Check Actual Error
Run the executable directly to see the real error:

```bash
dist/DinosaurIsland.app/Contents/MacOS/DinosaurIsland
```

This will show you the actual error message!

---

### Issue 2: "Damaged" or "Can't be Opened" Message

**Error:** *"DinosaurIsland.app is damaged and can't be opened"*

**Fix:**
```bash
# Remove all extended attributes
xattr -cr dist/DinosaurIsland.app

# If that doesn't work, disable Gatekeeper temporarily (not recommended!)
sudo spctl --master-disable
# Open the app
# Re-enable Gatekeeper
sudo spctl --master-enable
```

---

### Issue 3: pygame Import Error

**Error when running executable:** `ModuleNotFoundError: No module named 'pygame'`

**Fix: Reinstall pygame and rebuild**
```bash
# Uninstall pygame
pip3 uninstall pygame

# Reinstall
pip3 install pygame

# Clean and rebuild
rm -rf build dist
./build_macos.sh
```

---

### Issue 4: SDL2 Library Errors

**Error:** `Library not loaded: @rpath/SDL2.framework/Versions/A/SDL2`

**Fix A: Install SDL2 via Homebrew**
```bash
brew install sdl2 sdl2_mixer sdl2_ttf sdl2_image
```

**Fix B: Use macOS-specific spec file**
```bash
# Make sure you're using the macOS spec file
./build_macos.sh
# (This uses DinosaurIsland-macOS.spec which bundles SDL2)
```

---

### Issue 5: Blank Window or Crash on Startup

**Symptoms:**
- Window opens but is blank
- App crashes immediately after window appears

**Diagnostic:**

Run with diagnostics:
```bash
./diagnose_macos.sh
```

Check Console.app:
1. Open Console.app (Applications → Utilities → Console)
2. Search for "DinosaurIsland"
3. Look for crash reports or error messages

**Common Fixes:**

```bash
# 1. Rebuild with verbose logging
pyinstaller --clean --debug all DinosaurIsland-macOS.spec

# 2. Test pygame installation
python3 -c "import pygame; pygame.init(); print('pygame works!')"

# 3. Update PyInstaller
pip3 install --upgrade pyinstaller

# 4. Rebuild
./build_macos.sh
```

---

### Issue 6: Python Framework Issues

**Error:** `Python is not installed as a framework`

This happens if pygame was built expecting a framework Python.

**Fix:**
```bash
# Method 1: Use homebrew Python (recommended)
brew install python3

# Make sure you're using homebrew Python
which python3
# Should show: /opt/homebrew/bin/python3 or /usr/local/bin/python3

# Reinstall pygame
pip3 install --force-reinstall pygame

# Rebuild
./build_macos.sh
```

**Method 2: Install pygame without framework**
```bash
pip3 uninstall pygame
pip3 install pygame --no-binary pygame
```

---

## 🔧 Diagnostic Commands

### Check if App is Signed
```bash
codesign -dv --verbose=4 dist/DinosaurIsland.app
```

### Check Gatekeeper Status
```bash
spctl -a -vv dist/DinosaurIsland.app
```

### List Extended Attributes
```bash
xattr -l dist/DinosaurIsland.app
```

### View App Bundle Structure
```bash
tree dist/DinosaurIsland.app
# or
find dist/DinosaurIsland.app -print
```

### Check Dependencies
```bash
otool -L dist/DinosaurIsland.app/Contents/MacOS/DinosaurIsland
```

### Run Diagnostic Script
```bash
chmod +x diagnose_macos.sh
./diagnose_macos.sh
```

---

## 🏗️ Rebuilding from Scratch

If nothing else works, try a complete clean rebuild:

```bash
# 1. Clean everything
rm -rf build dist __pycache__
rm -rf *.pyc *.pyo

# 2. Uninstall and reinstall dependencies
pip3 uninstall pygame pyinstaller -y
pip3 install pygame pyinstaller

# 3. Rebuild
./build_macos.sh

# 4. Remove quarantine
xattr -cr dist/DinosaurIsland.app

# 5. Test
open dist/DinosaurIsland.app
```

---

## 📊 Checking Logs

### System Logs (Console.app)

1. Open **Console.app**
2. Select your Mac under "Devices"
3. Click **Start** streaming
4. Try to open DinosaurIsland.app
5. Search for "DinosaurIsland" or "Python" in the logs

### Crash Reports

```bash
# View crash reports
open ~/Library/Logs/DiagnosticReports/

# Look for files named:
# DinosaurIsland_*.crash
```

### PyInstaller Debug Log

Build with debug mode:
```bash
pyinstaller --clean --debug all DinosaurIsland-macOS.spec
```

Then run and check:
```bash
open dist/DinosaurIsland.app
# Check for DinosaurIsland.log in the app bundle
cat dist/DinosaurIsland.app/Contents/MacOS/DinosaurIsland.log
```

---

## 🎯 macOS Version-Specific Issues

### macOS Sonoma (14.x)
- Gatekeeper is stricter
- Need to remove quarantine: `xattr -cr dist/DinosaurIsland.app`
- May need to allow in System Settings → Privacy & Security

### macOS Ventura (13.x)
- Similar to Sonoma
- Right-click → Open usually works

### macOS Monterey (12.x) and earlier
- Less strict
- Usually just need right-click → Open

---

## 🔐 Code Signing (Advanced)

If you want to properly sign the app (requires Apple Developer account - $99/year):

```bash
# Sign the app
codesign --deep --force --verify --verbose \
  --sign "Developer ID Application: Your Name (TEAM_ID)" \
  dist/DinosaurIsland.app

# Verify
codesign -dv --verbose=4 dist/DinosaurIsland.app

# Notarize (for macOS Catalina+)
# 1. Create zip
ditto -c -k --keepParent dist/DinosaurIsland.app DinosaurIsland.zip

# 2. Submit for notarization
xcrun notarytool submit DinosaurIsland.zip \
  --apple-id "your@email.com" \
  --team-id "TEAM_ID" \
  --password "app-specific-password" \
  --wait

# 3. Staple the ticket
xcrun stapler staple dist/DinosaurIsland.app

# 4. Verify
spctl -a -vv dist/DinosaurIsland.app
```

---

## 🆘 Still Not Working?

### Last Resort Fixes

1. **Run Python version directly (no .app)**
   ```bash
   python3 main.py
   ```
   If this works, the issue is with the .app bundle, not the game.

2. **Try older PyInstaller version**
   ```bash
   pip3 install pyinstaller==5.13.2
   ./build_macos.sh
   ```

3. **Build without UPX compression**
   Edit `DinosaurIsland-macOS.spec`:
   ```python
   upx=False,  # Change from True to False
   ```
   Then rebuild.

4. **Use --onefile mode (slower but simpler)**
   ```bash
   pyinstaller --onefile --windowed main.py
   # Creates single executable (no .app bundle)
   ```

---

## 📝 Getting Help

If you're still stuck, gather this info:

```bash
# System info
sw_vers

# Python version
python3 --version

# pygame version
python3 -c "import pygame; print(pygame.__version__)"

# PyInstaller version
pyinstaller --version

# Run diagnostics
./diagnose_macos.sh > diagnostics.txt 2>&1

# Try to run and capture error
dist/DinosaurIsland.app/Contents/MacOS/DinosaurIsland 2>&1 | head -50
```

Then create an issue with this information!

---

## ✅ Quick Checklist

- [ ] Removed quarantine: `xattr -cr dist/DinosaurIsland.app`
- [ ] Tried right-click → Open
- [ ] Ran executable directly to see error
- [ ] Checked Console.app for logs
- [ ] pygame installed: `python3 -c "import pygame"`
- [ ] PyInstaller updated: `pip3 install --upgrade pyinstaller`
- [ ] Used macOS-specific build: `./build_macos.sh`
- [ ] Ran diagnostics: `./diagnose_macos.sh`
- [ ] Checked crash reports in ~/Library/Logs/DiagnosticReports/

---

## 💡 Prevention

To avoid issues in the future:

1. **Always use the macOS build script:** `./build_macos.sh`
2. **Keep dependencies updated:** `pip3 install --upgrade pygame pyinstaller`
3. **Test immediately after building:** `open dist/DinosaurIsland.app`
4. **Remove quarantine before distributing:** `xattr -cr dist/DinosaurIsland.app`

---

**Most common fix:** Just run `xattr -cr dist/DinosaurIsland.app` and try again! 🍎
