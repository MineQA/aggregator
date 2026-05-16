from __future__ import annotations

import runpy
import sys
from pathlib import Path

import gui.pyinstaller_preload  # noqa: F401


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        if len(sys.argv) < 3:
            raise SystemExit("missing script path")
        script = sys.argv[2]
        if getattr(sys, "frozen", False):
            script = str((Path(getattr(sys, "_MEIPASS", Path(sys.executable).resolve().parent)) / script).resolve())
        script_path = Path(script).resolve()
        parent_dir = str(script_path.parent)
        if parent_dir not in sys.path:
            sys.path.insert(0, parent_dir)
        sys.argv = sys.argv[2:]
        runpy.run_path(str(script_path), run_name="__main__")
        return

    from gui.app import run

    run()


if __name__ == "__main__":
    main()
