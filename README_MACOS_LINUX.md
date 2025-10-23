# 🦕 Flucht von der Dinosaurier-Insel
## macOS & Linux Distribution Guide

Build and distribute the game for macOS and Linux systems.

---

## 🚀 Quick Build (One Command!)

### Just run:
```bash
./build.sh
```

That's it! ✨

---

## 📦 What You Get

### macOS
- **Output:** `dist/DinosaurIsland.app`
- **Size:** ~8-10 MB
- **Format:** macOS Application Bundle (.app)
- **Compatible:** macOS 10.13+ (High Sierra and newer)

### Linux
- **Output:** `dist/DinosaurIsland`
- **Size:** ~7 MB (awesome!)
- **Format:** ELF 64-bit executable
- **Compatible:** Most modern Linux distros (Ubuntu, Fedora, Arch, etc.)

---

## 🛠️ Prerequisites

### macOS
```bash
# Install Python 3 (if not already installed)
brew install python3

# Install dependencies
pip3 install pygame pyinstaller
```

### Linux
```bash
# Ubuntu/Debian
sudo apt install python3 python3-pip
pip3 install pygame pyinstaller

# Fedora
sudo dnf install python3 python3-pip
pip3 install pygame pyinstaller

# Arch
sudo pacman -S python python-pip
pip install pygame pyinstaller
```

---

## 🔨 Building

### Method 1: Simple Build Script (Recommended)
```bash
./build.sh
```

The script will:
- ✅ Check Python installation
- ✅ Install PyInstaller if needed
- ✅ Build the executable
- ✅ Show you where it is
- ✅ Give you usage instructions

### Method 2: Manual PyInstaller
```bash
# Clean previous builds
rm -rf build dist

# Build
pyinstaller DinosaurIsland-Unix.spec

# macOS: dist/DinosaurIsland.app
# Linux: dist/DinosaurIsland
```

---

## 🎮 Running

### macOS
```bash
# From terminal
open dist/DinosaurIsland.app

# Or double-click in Finder
# First time: Right-click → Open (to bypass Gatekeeper)
```

### Linux
```bash
# From terminal
./dist/DinosaurIsland

# Make it accessible system-wide
sudo cp dist/DinosaurIsland /usr/local/bin/
dinosaurisland  # run from anywhere!
```

---

## 📤 Distributing

### macOS - Create .dmg (Professional)

```bash
# Simple zip (easiest)
cd dist
zip -r DinosaurIsland-macOS.zip DinosaurIsland.app

# Or create DMG (more professional)
hdiutil create -volname "Dinosaur Island" \
  -srcfolder dist/DinosaurIsland.app \
  -ov -format UDZO \
  DinosaurIsland.dmg
```

**Share:** Send the .zip or .dmg to friends!

### Linux - Create tarball

```bash
# Compress
tar -czf DinosaurIsland-Linux-x86_64.tar.gz -C dist DinosaurIsland

# Or create AppImage (portable, runs on any Linux)
# See: https://appimage.org/
```

**Share:** Upload to GitHub releases, itch.io, or send directly!

---

## 🌐 Publishing Platforms

### itch.io (Best for Indie Games!)
1. Go to https://itch.io
2. Create account (free)
3. Create new game project
4. Upload:
   - macOS: DinosaurIsland.app (zipped)
   - Linux: DinosaurIsland executable (tarball)
5. Set to free or paid
6. Publish!

**Benefits:**
- Free hosting
- Download analytics
- Community features
- Professional presentation

### GitHub Releases
```bash
# Tag release
git tag v2.0.0
git push origin v2.0.0

# Create release on GitHub
# Upload DinosaurIsland-macOS.zip
# Upload DinosaurIsland-Linux-x86_64.tar.gz
```

### Flathub (Linux)
Create Flatpak for distribution through Flathub:
- https://flatpak.org/
- Reaches millions of Linux users

---

## 🔧 Troubleshooting

### macOS: "App is damaged and can't be opened"

This is Gatekeeper blocking unsigned apps.

**Solution:**
```bash
# Remove quarantine flag
xattr -cr dist/DinosaurIsland.app

# Or right-click → Open (first time only)
```

### macOS: "Command not found: python3"

**Solution:**
```bash
# Install Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python3
```

### Linux: "pygame.error: No available video device"

You're trying to run it in a headless environment (no display).

**Solution:**
```bash
# Make sure you're in a graphical session
# Or use xvfb for headless testing
xvfb-run ./dist/DinosaurIsland
```

### Linux: Missing libraries

**Error:** `error while loading shared libraries: libSDL2-2.0.so.0`

**Solution:**
```bash
# Ubuntu/Debian
sudo apt install libsdl2-2.0-0 libsdl2-mixer-2.0-0 libsdl2-ttf-2.0-0

# Fedora
sudo dnf install SDL2 SDL2_mixer SDL2_ttf

# Arch
sudo pacman -S sdl2 sdl2_mixer sdl2_ttf
```

### Build fails with import errors

**Solution:**
```bash
# Reinstall dependencies
pip3 install --force-reinstall pygame

# Clean and rebuild
rm -rf build dist
./build.sh
```

---

## 📊 File Sizes

| Platform | Uncompressed | Compressed (zip/tar.gz) |
|----------|-------------|-------------------------|
| macOS    | ~10 MB      | ~6 MB                  |
| Linux    | ~7 MB       | ~4 MB                  |

Why so small? The game is lightweight and PyInstaller only includes what's needed!

---

## 🎨 Advanced: Custom Icon

### Create icon for macOS

```bash
# Create .icns from PNG
mkdir DinosaurIcon.iconset
sips -z 16 16     icon.png --out DinosaurIcon.iconset/icon_16x16.png
sips -z 32 32     icon.png --out DinosaurIcon.iconset/icon_16x16@2x.png
sips -z 32 32     icon.png --out DinosaurIcon.iconset/icon_32x32.png
sips -z 64 64     icon.png --out DinosaurIcon.iconset/icon_32x32@2x.png
sips -z 128 128   icon.png --out DinosaurIcon.iconset/icon_128x128.png
sips -z 256 256   icon.png --out DinosaurIcon.iconset/icon_128x128@2x.png
sips -z 256 256   icon.png --out DinosaurIcon.iconset/icon_256x256.png
sips -z 512 512   icon.png --out DinosaurIcon.iconset/icon_256x256@2x.png
sips -z 512 512   icon.png --out DinosaurIcon.iconset/icon_512x512.png
sips -z 1024 1024 icon.png --out DinosaurIcon.iconset/icon_512x512@2x.png

# Create .icns
iconutil -c icns DinosaurIcon.iconset

# Use in spec file
# icon='DinosaurIcon.icns'
```

### Create icon for Linux

```bash
# Use .png directly
# Place as: konrad_insel/icon.png
# PyInstaller will include it
```

---

## 🚢 Code Signing (Optional, for professional distribution)

### macOS

Requires Apple Developer account ($99/year)

```bash
# Sign app
codesign --deep --force --verify --verbose \
  --sign "Developer ID Application: Your Name (TEAM_ID)" \
  dist/DinosaurIsland.app

# Verify signature
codesign -dv --verbose=4 dist/DinosaurIsland.app

# Notarize for Catalina+
# (Prevents Gatekeeper warnings)
xcrun notarytool submit DinosaurIsland.zip \
  --apple-id "your@email.com" \
  --team-id "TEAM_ID" \
  --password "app-specific-password"
```

### Linux

No code signing needed! Linux users are used to running unsigned binaries.

---

## 📚 Additional Resources

- **PyInstaller Docs:** https://pyinstaller.org/
- **itch.io Publishing:** https://itch.io/developers
- **AppImage Tutorial:** https://docs.appimage.org/
- **Flatpak Tutorial:** https://docs.flatpak.org/
- **Homebrew Cask:** https://docs.brew.sh/Cask-Cookbook

---

## 🎯 Summary

### For Distribution:

**Quick & Easy:**
```bash
./build.sh
cd dist
zip -r DinosaurIsland.zip DinosaurIsland.app  # macOS
tar -czf DinosaurIsland.tar.gz DinosaurIsland # Linux
```

**Professional:**
1. Build for both platforms
2. Upload to itch.io
3. Share the link!

### For Development:

```bash
# Just run the game directly
pip3 install -r requirements.txt
python3 main.py
```

---

## 💬 Support

Questions? Issues?
1. Check the troubleshooting section above
2. See full docs in `PACKAGING.md`
3. Create an issue on GitHub

---

## 🦕 Have Fun!

You've got a fully packaged dinosaur survival game ready to share with the world!

**Built with ❤️ by Konrad Weber (age 11) and family**

---

Made with 🐍 Python + 🎮 Pygame + 📦 PyInstaller
