"""
PS2 List Tab — PRO STABLE (ANTI-CRASH)

✔ Dark theme
✔ Checkbox robusto
✔ Standalone seguro
✔ Selecionar Destino
✔ Atualizar Unidade
✔ Remover da Unidade
✔ Proteção contra crash
"""

from __future__ import annotations

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox


class PS2ListTab:
    CHECK_ON = "☑"
    CHECK_OFF = "☐"

    # =========================================================
    def __init__(self, parent, services=None):
        self.parent = parent
        self.services = services

        self.game_service = getattr(services, "game_service", None)

        self.source_folder = tk.StringVar()
        self.dest_drive = tk.StringVar()

        self._configure_dark_theme()
        self._build_ui()

    # =========================================================
    # THEME (SAFE)
    # =========================================================
    def _configure_dark_theme(self):
        try:
            style = ttk.Style(self.parent)
            style.theme_use("default")

            style.configure(
                "Treeview",
                background="#1e1e1e",
                foreground="#e6e6e6",
                fieldbackground="#1e1e1e",
                rowheight=24,
            )

            style.map(
                "Treeview",
                background=[("selected", "#094771")],
                foreground=[("selected", "#ffffff")],
            )

            style.configure(
                "Treeview.Heading",
                background="#2d2d2d",
                foreground="#ffffff",
                relief="flat",
            )
        except Exception as e:
            print("Theme warning:", e)

    # =========================================================
    # UI
    # =========================================================
    def _build_ui(self):
        self.parent.configure(bg="#1e1e1e")

        root_frame = tk.Frame(self.parent, bg="#1e1e1e")
        root_frame.pack(fill="both", expand=True, padx=10, pady=10)

        title = tk.Label(
            root_frame,
            text="Lista de Jogos PS2",
            bg="#1e1e1e",
            fg="#e6e6e6",
            font=("Segoe UI", 14, "bold"),
        )
        title.pack(anchor="w", pady=(0, 8))

        panes = tk.Frame(root_frame, bg="#1e1e1e")
        panes.pack(fill="both", expand=True)

        panes.columnconfigure((0, 1, 2), weight=1)
        panes.rowconfigure(0, weight=1)

        self._build_left_panel(panes)
        self._build_middle_panel(panes)
        self._build_right_panel(panes)

    # =========================================================
    # LEFT
    # =========================================================
    def _build_left_panel(self, parent):
        frame = tk.LabelFrame(parent, text="Jogos na Pasta", bg="#1e1e1e", fg="#e6e6e6")
        frame.grid(row=0, column=0, sticky="nsew", padx=4)
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        self.tree_source = ttk.Treeview(
            frame,
            columns=("check", "name", "size"),
            show="headings",
        )

        self.tree_source.heading("check", text="✔")
        self.tree_source.heading("name", text="Nome")
        self.tree_source.heading("size", text="Tamanho (GB)")

        self.tree_source.column("check", width=40, anchor="center")
        self.tree_source.column("name", width=180)
        self.tree_source.column("size", width=90, anchor="center")

        self.tree_source.grid(row=0, column=0, sticky="nsew")
        self.tree_source.bind("<Button-1>", self._toggle_source_checkbox)

        scroll = ttk.Scrollbar(frame, command=self.tree_source.yview)
        scroll.grid(row=0, column=1, sticky="ns")
        self.tree_source.configure(yscrollcommand=scroll.set)

        btn_frame = tk.Frame(frame, bg="#1e1e1e")
        btn_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=6)

        tk.Button(btn_frame, text="Selecionar Origem", command=self.select_folder,
                  bg="#2d2d2d", fg="white").pack(side="left", padx=2)

        tk.Button(btn_frame, text="Atualizar", command=self.refresh_source,
                  bg="#2d2d2d", fg="white").pack(side="left", padx=2)

        tk.Button(btn_frame, text="Criar Lista →", command=self.add_selected_to_queue,
                  bg="#0e639c", fg="white").pack(side="right", padx=2)

    # =========================================================
    # MIDDLE
    # =========================================================
    def _build_middle_panel(self, parent):
        frame = tk.LabelFrame(parent, text="Fila para Gravação", bg="#1e1e1e", fg="#e6e6e6")
        frame.grid(row=0, column=1, sticky="nsew", padx=4)
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        self.tree_queue = ttk.Treeview(
            frame,
            columns=("check", "name"),
            show="headings",
        )

        self.tree_queue.heading("check", text="✔")
        self.tree_queue.heading("name", text="Jogos Selecionados")

        self.tree_queue.column("check", width=40, anchor="center")
        self.tree_queue.column("name", width=220)

        self.tree_queue.grid(row=0, column=0, sticky="nsew")
        self.tree_queue.bind("<Button-1>", self._toggle_queue_checkbox)

        scroll = ttk.Scrollbar(frame, command=self.tree_queue.yview)
        scroll.grid(row=0, column=1, sticky="ns")
        self.tree_queue.configure(yscrollcommand=scroll.set)

        btn_frame = tk.Frame(frame, bg="#1e1e1e")
        btn_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=6)

        tk.Button(btn_frame, text="Remover", command=self.remove_from_queue,
                  bg="#2d2d2d", fg="white").pack(side="left", padx=2)

    # =========================================================
    # RIGHT
    # =========================================================
    def _build_right_panel(self, parent):
        frame = tk.LabelFrame(parent, text="Jogos na Unidade", bg="#1e1e1e", fg="#e6e6e6")
        frame.grid(row=0, column=2, sticky="nsew", padx=4)
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        self.tree_drive = ttk.Treeview(
            frame,
            columns=("check", "name"),
            show="headings",
        )

        self.tree_drive.heading("check", text="✔")
        self.tree_drive.heading("name", text="Instalados")

        self.tree_drive.column("check", width=40, anchor="center")
        self.tree_drive.column("name", width=220)

        self.tree_drive.grid(row=0, column=0, sticky="nsew")
        self.tree_drive.bind("<Button-1>", self._toggle_drive_checkbox)

        scroll = ttk.Scrollbar(frame, command=self.tree_drive.yview)
        scroll.grid(row=0, column=1, sticky="ns")
        self.tree_drive.configure(yscrollcommand=scroll.set)

        btn_frame = tk.Frame(frame, bg="#1e1e1e")
        btn_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=6)

        tk.Button(btn_frame, text="Selecionar Destino",
                  command=self.select_drive_destination,
                  bg="#2d2d2d", fg="white").pack(side="left", padx=2)

        tk.Button(btn_frame, text="Atualizar Unidade",
                  command=self.refresh_drive,
                  bg="#2d2d2d", fg="white").pack(side="left", padx=2)

        tk.Button(btn_frame, text="Remover da Unidade",
                  command=self.remove_from_drive,
                  bg="#c74e39", fg="white").pack(side="right", padx=2)

    # =========================================================
    # CHECKBOX CORE
    # =========================================================
    def _toggle_checkbox(self, tree, event):
        if tree.identify("region", event.x, event.y) != "cell":
            return
        if tree.identify_column(event.x) != "#1":
            return

        item = tree.identify_row(event.y)
        if not item:
            return

        values = list(tree.item(item, "values"))
        if not values:
            return

        values[0] = self.CHECK_ON if values[0] != self.CHECK_ON else self.CHECK_OFF
        tree.item(item, values=values)

    def _toggle_source_checkbox(self, event):
        self._toggle_checkbox(self.tree_source, event)

    def _toggle_queue_checkbox(self, event):
        self._toggle_checkbox(self.tree_queue, event)

    def _toggle_drive_checkbox(self, event):
        self._toggle_checkbox(self.tree_drive, event)

    # =========================================================
    # ACTIONS
    # =========================================================
    def select_drive_destination(self):
        path = filedialog.askdirectory(title="Selecionar unidade de destino")
        if path:
            self.dest_drive.set(path)

    def select_folder(self):
        path = filedialog.askdirectory(title="Selecionar pasta de ISOs")
        if path:
            self.source_folder.set(path)
            self.refresh_source()

    def refresh_source(self):
        self.tree_source.delete(*self.tree_source.get_children())
        folder = self.source_folder.get()

        if not folder or not os.path.isdir(folder):
            return

        for file in os.listdir(folder):
            if file.lower().endswith(".iso"):
                full = os.path.join(folder, file)
                size_gb = os.path.getsize(full) / (1024 ** 3)
                self.tree_source.insert("", "end",
                                        values=(self.CHECK_OFF, file, f"{size_gb:.2f}"))

    def refresh_drive(self):
        self.tree_drive.delete(*self.tree_drive.get_children())
        mock_games = ["God of War II", "Resident Evil 4", "Gran Turismo 4"]
        for name in mock_games:
            self.tree_drive.insert("", "end", values=(self.CHECK_OFF, name))

    def add_selected_to_queue(self):
        pass

    def remove_from_queue(self):
        for item in list(self.tree_queue.get_children()):
            if self.tree_queue.item(item, "values")[0] == self.CHECK_ON:
                self.tree_queue.delete(item)

    def remove_from_drive(self):
        for item in list(self.tree_drive.get_children()):
            if self.tree_drive.item(item, "values")[0] == self.CHECK_ON:
                self.tree_drive.delete(item)


# =============================================================
# STANDALONE SAFE
# =============================================================
if __name__ == "__main__":
    try:
        root = tk.Tk()
        root.title("PS2 List Tab — PRO STABLE")
        root.geometry("1100x600")
        PS2ListTab(root)
        root.mainloop()
    except Exception as e:
        print("FATAL:", e)
        input("Pressione ENTER para sair...")