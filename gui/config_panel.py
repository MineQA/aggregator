from __future__ import annotations

import json
from pathlib import Path
from tkinter import filedialog, messagebox

import customtkinter as ctk


TARGETS = ["clash", "v2ray", "singbox", "mixed", "clashr", "quan", "quanx", "loon", "ss", "sssub", "ssd", "ssr", "surfboard", "surge"]
STORAGE_ENGINES = ["gist", "local", "pastegg", "imperial", "pastefy", "qbin"]


class ConfigPanel(ctk.CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master)
        self.mode = ctk.StringVar(value="collect")
        self.target_vars = {name: ctk.BooleanVar(value=name in {"clash", "v2ray", "singbox"}) for name in TARGETS}
        self.collect_vars: dict[str, ctk.Variable] = {}
        self.process_vars: dict[str, ctk.Variable] = {}
        self.common_vars: dict[str, ctk.Variable] = {}
        self._build()

    def _build(self) -> None:
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        mode_bar = ctk.CTkFrame(self)
        mode_bar.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        mode_bar.grid_columnconfigure((0, 1), weight=1)
        ctk.CTkSegmentedButton(mode_bar, values=["collect", "process"], variable=self.mode, command=lambda _: self._refresh_mode()).grid(row=0, column=0, sticky="w", padx=8, pady=8)
        self.storage_engine = ctk.StringVar(value="gist")
        ctk.CTkLabel(mode_bar, text="Process 存储引擎").grid(row=0, column=1, sticky="e", padx=(8, 4))
        ctk.CTkOptionMenu(mode_bar, variable=self.storage_engine, values=STORAGE_ENGINES, width=120).grid(row=0, column=2, sticky="e", padx=8)

        self.scroll = ctk.CTkScrollableFrame(self)
        self.scroll.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.scroll.grid_columnconfigure(1, weight=1)

        self._build_common(0)
        self.collect_start = 9
        self._build_collect(self.collect_start)
        self.process_start = 27
        self._build_process(self.process_start)
        self._refresh_mode()

    def _entry(self, row: int, label: str, var: ctk.StringVar, show: str | None = None, browse: str | None = None) -> None:
        ctk.CTkLabel(self.scroll, text=label).grid(row=row, column=0, sticky="w", padx=8, pady=5)
        entry = ctk.CTkEntry(self.scroll, textvariable=var, show=show or "")
        entry.grid(row=row, column=1, sticky="ew", padx=8, pady=5)
        if browse:
            ctk.CTkButton(self.scroll, text="浏览", width=64, command=lambda: self._browse(var, browse)).grid(row=row, column=2, sticky="e", padx=8, pady=5)

    def _check(self, row: int, text: str, var: ctk.BooleanVar, column: int = 0) -> None:
        ctk.CTkCheckBox(self.scroll, text=text, variable=var).grid(row=row, column=column, sticky="w", padx=8, pady=5)

    def _build_common(self, row: int) -> None:
        ctk.CTkLabel(self.scroll, text="通用配置", font=ctk.CTkFont(size=15, weight="bold")).grid(row=row, column=0, columnspan=3, sticky="w", padx=8, pady=(8, 4))
        self.common_vars["threads"] = ctk.StringVar(value="64")
        self.common_vars["timeout"] = ctk.StringVar(value="5000")
        self.common_vars["test_url"] = ctk.StringVar(value="https://www.google.com/generate_204")
        self._entry(row + 1, "线程数", self.common_vars["threads"])
        self._entry(row + 2, "超时(ms)", self.common_vars["timeout"])
        self._entry(row + 3, "测试 URL", self.common_vars["test_url"])
        ctk.CTkLabel(self.scroll, text="输出类型").grid(row=row + 4, column=0, sticky="nw", padx=8, pady=5)
        box = ctk.CTkFrame(self.scroll, fg_color="transparent")
        box.grid(row=row + 4, column=1, columnspan=2, sticky="ew", padx=8, pady=5)
        for idx, target in enumerate(TARGETS):
            ctk.CTkCheckBox(box, text=target, variable=self.target_vars[target], width=90).grid(row=idx // 4, column=idx % 4, sticky="w", padx=4, pady=3)

    def _build_collect(self, row: int) -> None:
        self.collect_widgets: list[ctk.CTkBaseClass] = []
        title = ctk.CTkLabel(self.scroll, text="Collect 模式", font=ctk.CTkFont(size=15, weight="bold"))
        title.grid(row=row, column=0, columnspan=3, sticky="w", padx=8, pady=(16, 4)); self.collect_widgets.append(title)
        defaults = {
            "gist_pat": "", "gist_link": "", "local_path": "", "pages": "0", "flow": "0", "life": "0", "delay": "5000", "customize": "",
        }
        for k, v in defaults.items():
            self.collect_vars[k] = ctk.StringVar(value=v)
        for k, v in {"skip": True, "overwrite": True, "easygoing": False, "chuck": False, "all": True, "vitiate": False, "local": False}.items():
            self.collect_vars[k] = ctk.BooleanVar(value=v)
        entries = [("gist_pat", "GitHub Token", "*", None), ("gist_link", "Gist ID(username/gist_id)", None, None), ("local_path", "本地输出路径", None, "dir"), ("pages", "爬取页数(0=不限)", None, None), ("flow", "最小剩余流量GB", None, None), ("life", "最小剩余时间小时", None, None), ("delay", "最大延迟ms", None, None), ("customize", "自定义机场列表URL/文件", None, None)]
        for idx, (key, label, show, browse) in enumerate(entries, start=row + 1):
            self._entry(idx, label, self.collect_vars[key], show=show, browse=browse)
        checks = [("local", "输出到本地"), ("skip", "跳过可用性检查"), ("overwrite", "覆盖域名列表"), ("easygoing", "宽松注册"), ("chuck", "丢弃需人机验证站点"), ("all", "生成完整 Clash 配置"), ("vitiate", "忽略默认过滤规则")]
        for i, (key, text) in enumerate(checks):
            self._check(row + 10 + i // 2, text, self.collect_vars[key], i % 2)

    def _build_process(self, row: int) -> None:
        self.process_widgets: list[ctk.CTkBaseClass] = []
        title = ctk.CTkLabel(self.scroll, text="Process 模式", font=ctk.CTkFont(size=15, weight="bold"))
        title.grid(row=row, column=0, columnspan=3, sticky="w", padx=8, pady=(16, 4)); self.process_widgets.append(title)
        defaults = {"server": "", "push_token": "", "retry": "3", "environment": ".env", "workflow_mode": "0"}
        for k, v in defaults.items():
            self.process_vars[k] = ctk.StringVar(value=v)
        for k, v in {"check": False, "flexible": False, "overwrite": False, "invisible": False, "skip_alive": False, "skip_remark": False, "special_protocols": True, "trace": False, "reachable": True}.items():
            self.process_vars[k] = ctk.BooleanVar(value=v)
        entries = [("server", "配置文件路径/URL", None, "file"), ("push_token", "Push Token", "*", None), ("retry", "重试次数", None, None), ("environment", "环境文件", None, "file"), ("workflow_mode", "工作流模式(0/1/2)", None, None)]
        for idx, (key, label, show, browse) in enumerate(entries, start=row + 1):
            self._entry(idx, label, self.process_vars[key], show=show, browse=browse)
        checks = [("check", "仅检查模式"), ("flexible", "灵活注册"), ("overwrite", "覆写"), ("invisible", "隐藏进度条"), ("skip_alive", "跳过活性检查"), ("skip_remark", "跳过备注"), ("special_protocols", "启用特殊协议"), ("trace", "追踪日志"), ("reachable", "要求网络可达")]
        for i, (key, text) in enumerate(checks):
            self._check(row + 7 + i // 2, text, self.process_vars[key], i % 2)

    def _refresh_mode(self) -> None:
        mode = self.mode.get()
        for widget in getattr(self, "collect_widgets", []):
            pass
        for child in self.scroll.winfo_children():
            info = child.grid_info()
            row = int(info.get("row", -1))
            if self.collect_start <= row < self.process_start:
                child.grid() if mode == "collect" else child.grid_remove()
            elif row >= self.process_start:
                child.grid() if mode == "process" else child.grid_remove()

    def _browse(self, var: ctk.StringVar, kind: str) -> None:
        path = filedialog.askdirectory() if kind == "dir" else filedialog.askopenfilename()
        if path:
            var.set(path)

    def selected_targets(self) -> list[str]:
        return [name for name, var in self.target_vars.items() if var.get()]

    def build_command(self) -> tuple[list[str], dict[str, str]]:
        targets = self.selected_targets()
        if not targets:
            raise ValueError("请至少选择一种输出类型")
        threads = self.common_vars["threads"].get().strip() or "64"
        timeout = self.common_vars["timeout"].get().strip() or "5000"
        test_url = self.common_vars["test_url"].get().strip()
        if self.mode.get() == "collect":
            env = {
                "GIST_PAT": self.collect_vars["gist_pat"].get(),
                "GIST_LINK": self.collect_vars["gist_link"].get(),
                "CUSTOMIZE_LINK": self.collect_vars["customize"].get(),
                "LOCAL_BASEDIR": self.collect_vars["local_path"].get(),
            }
            args = ["subscribe/collect.py", "-n", threads, "-d", self.collect_vars["delay"].get() or timeout, "-t", *targets]
            gist = self.collect_vars["gist_link"].get().strip()
            token = self.collect_vars["gist_pat"].get().strip()
            if gist:
                args += ["-g", gist]
            if token:
                args += ["-k", token]
            pages = self.collect_vars["pages"].get().strip()
            if pages and pages != "0": args += ["-p", pages]
            for opt, flag in [("flow", "-f"), ("life", "-l"), ("customize", "-y")]:
                val = self.collect_vars[opt].get().strip()
                if val and val != "0": args += [flag, val]
            if test_url: args += ["-u", test_url]
            for opt, flag in [("skip", "--skip"), ("overwrite", "--overwrite"), ("easygoing", "--easygoing"), ("chuck", "--chuck"), ("all", "--all"), ("vitiate", "--vitiate")]:
                if self.collect_vars[opt].get(): args.append(flag)
            return args, env

        env = {
            "PUSH_TOKEN": self.process_vars["push_token"].get(),
            "WORKFLOW_MODE": self.process_vars["workflow_mode"].get(),
            "SKIP_ALIVE_CHECK": str(self.process_vars["skip_alive"].get()).lower(),
            "SKIP_REMARK": str(self.process_vars["skip_remark"].get()).lower(),
            "ENABLE_SPECIAL_PROTOCOLS": str(self.process_vars["special_protocols"].get()).lower(),
            "TRACE_ENABLE": str(self.process_vars["trace"].get()).lower(),
            "REACHABLE": str(self.process_vars["reachable"].get()).lower(),
            "LOCAL_BASEDIR": self.collect_vars["local_path"].get(),
        }
        server = self.process_vars["server"].get().strip()
        if server:
            env["SUBSCRIBE_CONF"] = server
        args = ["subscribe/process.py", "-n", threads, "-t", timeout, "-r", self.process_vars["retry"].get() or "3", "-e", self.process_vars["environment"].get() or ".env"]
        if server: args += ["-s", server]
        if test_url: args += ["-u", test_url]
        for opt, flag in [("check", "--check"), ("flexible", "--flexible"), ("overwrite", "--overwrite"), ("invisible", "--invisible")]:
            if self.process_vars[opt].get(): args.append(flag)
        return args, env

    def save_config(self, path: str) -> None:
        data = {
            "mode": self.mode.get(),
            "storage_engine": self.storage_engine.get(),
            "targets": {k: v.get() for k, v in self.target_vars.items()},
            "common": {k: v.get() for k, v in self.common_vars.items()},
            "collect": {k: v.get() for k, v in self.collect_vars.items()},
            "process": {k: v.get() for k, v in self.process_vars.items()},
        }
        Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def load_config(self, path: str) -> None:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        self.mode.set(data.get("mode", "collect"))
        self.storage_engine.set(data.get("storage_engine", "gist"))
        for group, mapping in [(self.target_vars, data.get("targets", {})), (self.common_vars, data.get("common", {})), (self.collect_vars, data.get("collect", {})), (self.process_vars, data.get("process", {}))]:
            for key, value in mapping.items():
                if key in group:
                    group[key].set(value)
        self._refresh_mode()
