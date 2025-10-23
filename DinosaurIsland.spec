# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Flucht von der Dinosaurier-Insel
Advanced configuration for building standalone executables

Usage:
    pyinstaller DinosaurIsland.spec
"""

import os
import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# Collect all game assets
game_assets = []
for root, dirs, files in os.walk('konrad_insel'):
    for file in files:
        file_path = os.path.join(root, file)
        game_assets.append((file_path, root))

# Collect all hidden imports
hidden_imports = [
    'pygame',
    'pygame.mixer',
    'pygame.font',
    'pygame.image',
    'pygame.surfarray',
    'numpy',
]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=game_assets,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',      # Remove unused modules
        'matplotlib',
        'IPython',
        'PIL',
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
    icon='konrad_insel/icon.png' if os.path.exists('konrad_insel/icon.png') else None,
)

# macOS App bundle (only on macOS)
if sys.platform == 'darwin':
    app = BUNDLE(
        exe,
        name='DinosaurIsland.app',
        icon='konrad_insel/icon.png' if os.path.exists('konrad_insel/icon.png') else None,
        bundle_identifier='com.weberfamily.dinosaurisland',
        info_plist={
            'CFBundleShortVersionString': '2.0.0',
            'CFBundleVersion': '2.0.0',
            'NSHighResolutionCapable': True,
        },
    )
