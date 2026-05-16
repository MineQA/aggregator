"""Imports used only for PyInstaller dependency discovery.

Business modules under subscribe/ are executed from bundled data files via
runpy.run_path, so PyInstaller cannot statically see their stdlib/third-party
dependencies.  Importing external dependencies here keeps the executable
self-contained without asking PyInstaller to analyze local bare modules such as
workflow, which conflicts with _pyinstaller_hooks_contrib's hook-workflow.py.
"""

# stdlib modules commonly used by dynamically loaded subscribe/*.py scripts
import base64  # noqa: F401
import gzip  # noqa: F401
import http.client  # noqa: F401
import ipaddress  # noqa: F401
import multiprocessing  # noqa: F401
import multiprocessing.pool  # noqa: F401
import queue  # noqa: F401
import socket  # noqa: F401
import ssl  # noqa: F401
import uuid  # noqa: F401
import xml.etree.ElementTree  # noqa: F401

# third-party modules used by dynamically loaded subscribe/*.py scripts.
# They are also listed in aggregator.spec hiddenimports. Keep these imports
# best-effort so the GUI can still show an actionable error from the real
# worker script instead of failing during GUI bootstrap.
try:
    import geoip2.database  # noqa: F401
except Exception:
    pass

try:
    import yaml  # noqa: F401
except Exception:
    pass

try:
    import tqdm  # noqa: F401
except Exception:
    pass

try:
    from Cryptodome.Cipher import AES  # noqa: F401
except Exception:
    pass

try:
    import fofa_hack  # noqa: F401
except Exception:
    pass
