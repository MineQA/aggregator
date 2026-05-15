from __future__ import annotations

import customtkinter as ctk


class LogPanel(ctk.CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 4))
        header.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(header, text="运行日志", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, sticky="w")
        ctk.CTkButton(header, text="清空", width=72, command=self.clear).grid(row=0, column=1, sticky="e")

        self.text = ctk.CTkTextbox(self, wrap="word")
        self.text.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

    def append(self, message: str) -> None:
        self.text.insert("end", message)
        self.text.see("end")

    def clear(self) -> None:
        self.text.delete("1.0", "end")
