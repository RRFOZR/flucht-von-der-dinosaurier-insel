# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for macOS and Linux
Optimized build configuration for Unix systems
"""

import os
import sys

block_cipher = None

# Collect all game assets
game_assets = []
for root, dirs, files in os.walk('konrad_insel'):
    for file in files:
        file_path = os.path.join(root, file)
        game_assets.append((file_path, root))

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=game_assets,
    hiddenimports=[
        'pygame',
        'pygame.mixer',
        'pygame.font',
        'pygame.image',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'matplotlib',
        'IPython',
        'PIL',
        'scipy',
        'pandas',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='DinosaurIsland',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # Compress executable
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window (GUI mode)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# macOS App bundle
if sys.platform == 'darwin':
    app = BUNDLE(
        exe,
        name='DinosaurIsland.app',
        icon=None,
        bundle_identifier='com.weberfamily.dinosaurisland',
        info_plist={
            'CFBundleName': 'Flucht von der Dinosaurier-Insel',
            'CFBundleDisplayName': 'Dinosaur Island',
            'CFBundleShortVersionString': '2.0.0',
            'CFBundleVersion': '2.0.0',
            'NSHighResolutionCapable': True,
            'LSMinimumSystemVersion': '10.13.0',
        },
    )
