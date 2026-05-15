from __future__ import annotations

from tkinter import filedialog, messagebox

import customtkinter as ctk

from gui.config_panel import ConfigPanel
from gui.log_panel import LogPanel
from gui.runner import ProcessRunner


class AggregatorApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        self.title("Aggregator - 代理池构建工具")
        self.geometry("1080x760")
        self.minsize(980, 680)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._build_header()
        body = ctk.CTkFrame(self)
        body.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 12))
        body.grid_columnconfigure(0, weight=1)
        body.grid_columnconfigure(1, weight=1)
        body.grid_rowconfigure(0, weight=1)

        self.config_panel = ConfigPanel(body)
        self.config_panel.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=10)
        self.log_panel = LogPanel(body)
        self.log_panel.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=10)

        self.runner = ProcessRunner(self._append_log, self._on_exit)
        self._build_footer()

    def _build_header(self) -> None:
        header = ctk.CTkFrame(self)
        header.grid(row=0, column=0, sticky="ew", padx=12, pady=12)
        header.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(header, text="Aggregator - 代理池构建工具", font=ctk.CTkFont(size=22, weight="bold")).grid(row=0, column=0, sticky="w", padx=12, pady=10)
        self.theme_switch = ctk.CTkSwitch(header, text="暗色", command=self._toggle_theme)
        self.theme_switch.grid(row=0, column=1, sticky="e", padx=12)

    def _build_footer(self) -> None:
        footer = ctk.CTkFrame(self)
        footer.grid(row=2, column=0, sticky="ew", padx=12, pady=(0, 12))
        footer.grid_columnconfigure(4, weight=1)
        self.run_btn = ctk.CTkButton(footer, text="▶ 运行", command=self.run_task)
        self.run_btn.grid(row=0, column=0, padx=8, pady=8)
        self.stop_btn = ctk.CTkButton(footer, text="■ 停止", fg_color="#b23b3b", hover_color="#922f2f", command=self.stop_task)
        self.stop_btn.grid(row=0, column=1, padx=8, pady=8)
        ctk.CTkButton(footer, text="💾 保存配置", command=self.save_config).grid(row=0, column=2, padx=8, pady=8)
        ctk.CTkButton(footer, text="📂 加载配置", command=self.load_config).grid(row=0, column=3, padx=8, pady=8)
        self.status = ctk.CTkLabel(footer, text="状态：空闲")
        self.status.grid(row=0, column=4, sticky="e", padx=12)

    def _toggle_theme(self) -> None:
        ctk.set_appearance_mode("Dark" if self.theme_switch.get() else "Light")

    def _append_log(self, message: str) -> None:
        self.after(0, lambda: self.log_panel.append(message))

    def _on_exit(self, code: int) -> None:
        self.after(0, lambda: self.status.configure(text=f"状态：已结束（退出码 {code}）"))
        self.after(0, lambda: self.run_btn.configure(state="normal"))

    def run_task(self) -> None:
        try:
            args, env = self.config_panel.build_command()
            self.runner.start(args=args, env=env)
            self.status.configure(text="状态：运行中")
            self.run_btn.configure(state="disabled")
        except Exception as exc:
            messagebox.showerror("启动失败", str(exc))

    def stop_task(self) -> None:
        self.runner.stop()

    def save_config(self) -> None:
        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json")], initialfile="config_gui.json")
        if path:
            self.config_panel.save_config(path)
            self.status.configure(text="状态：配置已保存")

    def load_config(self) -> None:
        path = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
        if path:
            self.config_panel.load_config(path)
            self.status.configure(text="状态：配置已加载")


def run() -> None:
    app = AggregatorApp()
    app.mainloop()
