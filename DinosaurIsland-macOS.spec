# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file specifically for macOS
Handles pygame and SDL library bundling correctly
"""

import os
import sys
from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs

block_cipher = None

# Collect all game assets
game_assets = []
for root, dirs, files in os.walk('konrad_insel'):
    for file in files:
        file_path = os.path.join(root, file)
        game_assets.append((file_path, root))

# Collect pygame data and libraries
pygame_datas = collect_data_files('pygame')
pygame_binaries = collect_dynamic_libs('pygame')

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=pygame_binaries,
    datas=game_assets + pygame_datas,
    hiddenimports=[
        'pygame',
        'pygame.mixer',
        'pygame.font',
        'pygame.image',
        'pygame.transform',
        'pygame.display',
        'pygame.draw',
        'pygame.event',
        'pygame.key',
        'pygame.time',
        'pygame.surface',
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
        'numpy',  # pygame doesn't need numpy for this game
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
    [],
    exclude_binaries=True,  # Important for .app bundle
    name='DinosaurIsland',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # No console - GUI only
    disable_windowed_traceback=False,
    argv_emulation=False,  # Important for macOS
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='DinosaurIsland',
)

app = BUNDLE(
    coll,
    name='DinosaurIsland.app',
    icon=None,
    bundle_identifier='com.weberfamily.dinosaurisland',
    version='2.0.0',
    info_plist={
        'CFBundleName': 'Dinosaur Island',
        'CFBundleDisplayName': 'Flucht von der Dinosaurier-Insel',
        'CFBundleGetInfoString': "Escape from Dinosaur Island",
        'CFBundleIdentifier': 'com.weberfamily.dinosaurisland',
        'CFBundleVersion': '2.0.0',
        'CFBundleShortVersionString': '2.0.0',
        'NSHumanReadableCopyright': 'Copyright © 2024 Weber Family',
        'NSHighResolutionCapable': 'True',
        'LSMinimumSystemVersion': '10.13.0',
        'NSRequiresAquaSystemAppearance': 'False',
        'LSApplicationCategoryType': 'public.app-category.games',
        'NSSupportsAutomaticGraphicsSwitching': 'True',
    },
)
