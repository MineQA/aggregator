from __future__ import annotations

import os
import queue
import subprocess
import sys
import threading
from pathlib import Path
from typing import Callable


LogCallback = Callable[[str], None]
ExitCallback = Callable[[int], None]


def app_root() -> Path:
    if getattr(sys, "frozen", False):
        return Path(getattr(sys, "_MEIPASS", Path(sys.executable).resolve().parent)).resolve()
    return Path(__file__).resolve().parent.parent


def python_executable() -> str:
    if getattr(sys, "frozen", False):
        return sys.executable
    return sys.executable


class ProcessRunner:
    def __init__(self, on_log: LogCallback, on_exit: ExitCallback | None = None) -> None:
        self.on_log = on_log
        self.on_exit = on_exit
        self.process: subprocess.Popen[str] | None = None
        self._thread: threading.Thread | None = None
        self._queue: queue.Queue[str] = queue.Queue()

    def running(self) -> bool:
        return self.process is not None and self.process.poll() is None

    def start(self, args: list[str], env: dict[str, str] | None = None) -> None:
        if self.running():
            raise RuntimeError("已有任务正在运行")

        root = app_root()
        final_env = os.environ.copy()
        if env:
            final_env.update({k: str(v) for k, v in env.items() if v is not None})

        if getattr(sys, "frozen", False):
            command = [sys.executable, "--cli", *args]
        else:
            command = [python_executable(), "-u", *args]

        self.on_log(f"$ {' '.join(command)}\n")
        self.process = subprocess.Popen(
            command,
            cwd=str(root),
            env=final_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
        )
        self._thread = threading.Thread(target=self._reader, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        if not self.running() or not self.process:
            return

        self.on_log("\n[GUI] 正在停止任务...\n")
        self.process.terminate()
        try:
            self.process.wait(timeout=8)
        except subprocess.TimeoutExpired:
            self.process.kill()

    def _reader(self) -> None:
        assert self.process is not None
        if self.process.stdout:
            for line in self.process.stdout:
                self.on_log(line)

        code = self.process.wait()
        self.on_log(f"\n[GUI] 任务结束，退出码：{code}\n")
        if self.on_exit:
            self.on_exit(code)
