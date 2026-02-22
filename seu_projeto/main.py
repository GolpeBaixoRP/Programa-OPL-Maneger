import customtkinter as ctk

from tabs.ps2.ps2_write_tab import PS2WriteTab
from tabs.ps2.ps2_list_tab import PS2ListTab
from tabs.ps1.ps1_write_tab import PS1WriteTab
from tabs.ps1.ps1_list_tab import PS1ListTab
from tabs.formatar.prepare_drive_tab import PrepareDriveTab


def main():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("OPL Manager")
    root.geometry("1200x700")

    tabview = ctk.CTkTabview(root)
    tabview.pack(fill="both", expand=True)

    # PS2
    ps2_write_tab = tabview.add("PS2 Gravar")
    PS2WriteTab(ps2_write_tab).pack(fill="both", expand=True)

    ps2_list_tab = tabview.add("PS2 Lista")
    PS2ListTab(ps2_list_tab).pack(fill="both", expand=True)

    # PS1
    ps1_write_tab = tabview.add("PS1 Gravar")
    PS1WriteTab(ps1_write_tab).pack(fill="both", expand=True)

    ps1_list_tab = tabview.add("PS1 Lista")
    PS1ListTab(ps1_list_tab).pack(fill="both", expand=True)

    # FORMATAR
    format_tab = tabview.add("Formatar")
    PrepareDriveTab(format_tab).pack(fill="both", expand=True)

    root.mainloop()


if __name__ == "__main__":
    main()