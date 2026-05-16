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

a = Analysis(
    ["main.py"],
    pathex=[str(root), str(root / "subscribe")],
    binaries=[],
    datas=datas,
    hiddenimports=[
        "customtkinter", "yaml", "geoip2", "Cryptodome", "fofa_hack",
        "crawl", "airport", "clash", "subconverter", "push", "workflow",
        "executable", "logger", "origin", "mailtm", "urlvalidator",
        "renewal", "location", "utils", "collect", "process",
        "scripts.commons", "scripts.fofa", "scripts.dynamic",
        "scripts.gitforks", "scripts.scaner", "scripts.tempairport",
        "scripts.v2rayfree", "scripts.v2rayse",
    ],
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
