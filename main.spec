# -*- mode: python ; coding: utf-8 -*-

import os

# Change the path to look for PNG files directly in the src directory
image_source_dir = os.path.abspath("src")  # Get absolute path to src directory
image_files = [(os.path.join(image_source_dir, f), "src") for f in os.listdir(image_source_dir) if f.endswith(".png")]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=image_files,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)