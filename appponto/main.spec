# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

# Coletar dados e binários do tkinter
tkinter_data = collect_all('tkinter')

# Configurar dados
datas = [
    ('appponto', 'appponto'),
] + tkinter_data[0]

# Configurar binários
binaries = tkinter_data[1]

# Configurar imports ocultos
hiddenimports = [
    'tkinter.messagebox',
    'tkinter.ttk',
    'tkinter.simpledialog',
] + tkinter_data[2]

# Análise
a = Analysis(
    ['main.py'],
    pathex=['.', './appponto'],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
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
    a.zipfiles,
    a.datas,
    [],
    name='AppPonto',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
)