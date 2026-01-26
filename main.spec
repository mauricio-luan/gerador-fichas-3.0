# -*- mode: python ; coding: utf-8 -*-
import os

a = Analysis(
    [os.path.join("src", "main.py")],
    pathex=[],
    binaries=[],
    datas=[
        (os.path.join("src", "assets", "payer.png"), "assets"),
        (os.path.join("src", "assets", "payer.ico"), "assets"),
    ],
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
    name="GeradorFichasPayer",
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
    icon=os.path.join("src", "assets", "payer.ico"),
)
