# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['App.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['torch', 'bokeh','matplotlib','mkl-fft','mkl-random' ,'mkl-service','llvmlite','scipy','qtpy','QtPy',
                'babel','pyOpenSSL','pyarrow','pyqt',
                'Sphinx','sphinx','docutils','scikit-learn','scipy','PyQt5',
                'PyQt5-sip','PyQtWebEngine','pygments','docutils','cryptography'],
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
    name='App',
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
