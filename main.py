from __future__ import annotations

import runpy
import sys
from pathlib import Path


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        if len(sys.argv) < 3:
            raise SystemExit("missing script path")
        script = str((Path(getattr(sys, "_MEIPASS", Path(sys.executable).resolve().parent)) / sys.argv[2]).resolve()) if getattr(sys, "frozen", False) else sys.argv[2]
        sys.argv = sys.argv[2:]
        runpy.run_path(script, run_name="__main__")
        return

    from gui.app import run

    run()


if __name__ == "__main__":
    main()
