# -*- mode: python ; coding: utf-8 -*-

import os

added_files = []
for folder in ['res', 'levels']:
    if os.path.exists(folder):
        for root, dirs, files in os.walk(folder):
            if '.vscode' in root:
                continue
            for file in files:
                if not file.endswith('.ase') and not file.endswith('.pyc'):
                    full_path = os.path.join(root, file)
                    
                    # Force forward slashes for PyInstaller's internal directory mapping
                    dest_dir = root.replace('\\', '/') 
                    
                    # (actual_file_on_disk, folder_path_inside_exe)
                    added_files.append((full_path, dest_dir))


a = Analysis(
    ['launcher.py'],
    pathex=[],
    binaries=[],
    datas=added_files,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='launcher',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
