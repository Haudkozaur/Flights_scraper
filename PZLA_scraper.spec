# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['main.py', 'fav.txt','Add_To_Favourites.py', 'Fav_athls.py', 'Find_event.py', 'GUI_run_class.py', 'incorrect_data_checker.py', 'input_encoding_func.py', 'PZLA_stats.py', 'request_func.py', 'Start_lists.py', 'sub_GUI_run_class.py', 'Table_class.py', 'Third_searching.py'],
    pathex=[],
    binaries=[],
    datas=[("fav.txt", ".")],
    hiddenimports=['requests','bs4','pysimplegui','readability-lxml', 'fav.txt'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    exclude_binaries=True,
    name='PZLA_scraper',
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
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='PZLA_scraper',
)
