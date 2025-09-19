# -*- mode: python ; coding: utf-8 -*-

"""
PyInstaller spec file pour SyncMark Unifié
Génère un seul exécutable intégrant toutes les fonctionnalités
"""

a = Analysis(
    ['syncmark_unified.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('native_host_manifest.json', '.'),  # Inclure le manifest
        ('manifest.json', '.'),              # Inclure le manifest de l'extension si présent
    ],
    hiddenimports=[
        'tkinter',
        'tkinter.messagebox',
        'winreg',
        'threading',
        'argparse',
        'pathlib',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'scipy',
        'pandas',
        'PIL',
        'PyQt5',
        'PyQt6',
        'PySide2',
        'PySide6',
    ],
    noarchive=False,
    optimize=2,  # Optimisation maximale
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='SyncMark',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,  # Réduire la taille
    upx=True,    # Compression UPX
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Application Windows (pas de console)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Ajouter une icône si disponible
    version_file=None,  # Ajouter des informations de version si nécessaire
)