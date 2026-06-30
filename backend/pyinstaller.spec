# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec for MathTools Offline backend.

Build:
    pyinstaller backend/pyinstaller.spec

This produces a single executable at dist/backend/backend (or .exe).
Copy it to src-tauri/binaries/ with the correct target-triple suffix.
"""

import sys
from pathlib import Path

BLOCK_CIPHER_LIST = None

a = Analysis(
    ['backend/main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('backend/core', 'backend/core'),
        ('backend/models', 'backend/models'),
        ('backend/routers', 'backend/routers'),
        ('backend/schemas', 'backend/schemas'),
    ],
    hiddenimports=[
        'uvicorn',
        'uvicorn.logging',
        'uvicorn.loops.auto',
        'uvicorn.protocols.http.auto',
        'uvicorn.protocols.websockets.auto',
        'sympy',
        'sqlalchemy',
        'sqlalchemy.sql.default_comparator',
        'pydantic',
        'multipart',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'matplotlib',
        'numpy',
        'scipy',
        'PIL',
        'pandas',
    ],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='backend',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    contents_directory='.',
)
