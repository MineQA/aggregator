# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path

from PyInstaller.utils.hooks import collect_data_files

block_cipher = None
root = Path.cwd()


def collect_tree(path: str, excludes: set[str] | None = None):
    excludes = excludes or set()
    base = root / path
    items = []
    if not base.exists():
        return items

    for item in base.rglob("*"):
        if item.is_dir():
            continue
        rel = item.relative_to(root)
        if any(part in excludes for part in rel.parts):
            continue
        items.append((str(item), str(rel.parent)))
    return items


datas = []
datas += collect_tree("subscribe", excludes={"__pycache__"})
datas += collect_tree("clash", excludes={"__pycache__"})
datas += collect_tree("subconverter", excludes={"__pycache__"})
datas += collect_data_files("customtkinter")

# subscribe/*.py is loaded dynamically by main.py via runpy.run_path and kept as data files.
# Do not add local bare modules such as "workflow" to hiddenimports, otherwise PyInstaller
# may run third-party hooks (for example hook-workflow.py) against our local module name.
hiddenimports = [
    "customtkinter",
    "yaml",
    "tqdm",
    "geoip2",
    "Cryptodome",
    "fofa_hack",
    "uuid",
    "base64",
    "gzip",
    "ipaddress",
    "multiprocessing",
    "multiprocessing.pool",
    "xml.etree.ElementTree",
]

a = Analysis(
    ["main.py"],
    pathex=[str(root)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
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
    name="aggregator",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
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
    name="aggregator",
)
