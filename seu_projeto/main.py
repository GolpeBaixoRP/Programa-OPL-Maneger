import customtkinter as ctk

from core.bootstrap import build_services

from tabs.ps2.ps2_write_tab import PS2WriteTab
from tabs.ps2.ps2_list_tab import PS2ListTab
from tabs.ps1.ps1_list_tab import PS1ListTab
from tabs.ps1.ps1_write_tab import PS1WriteTab
from tabs.prepare_drive_tab import PrepareDriveTab


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("PSX Manager")
        self.geometry("1000x650")

        self.services = build_services()

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True)

        tab_ps2_write = self.tabview.add("PS2 Gravação")
        tab_ps2_list = self.tabview.add("PS2 Lista")
        tab_ps1_write = self.tabview.add("PS1 Gravação")
        tab_ps1_list = self.tabview.add("PS1 Lista")
        tab_prepare = self.tabview.add("Preparar Unidade")

        PS2WriteTab(tab_ps2_write, self.services)
        PS2ListTab(tab_ps2_list, self.services)
        PS1WriteTab(tab_ps1_write, self.services)
        PS1ListTab(tab_ps1_list, self.services)
        PrepareDriveTab(tab_prepare, self.services)

    def on_close(self):
        if hasattr(self, "services"):
            self.services.close()
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
