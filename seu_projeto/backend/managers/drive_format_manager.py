# backend/managers/drive_format_manager.py

import os
from backend.executors.drive_executor import DriveExecutor


class DriveFormatManager:

    def __init__(self):
        self.executor = DriveExecutor()

    def format_drive(
        self,
        disk_number: int,
        drive_letter: str,
        filesystem: str,
        mode: str,
        quick: bool,
        log_callback=None
    ) -> dict:

        if filesystem.upper() not in ["FAT32", "EXFAT"]:
            return {"success": False, "message": "Filesystem inválido", "exit_code": 1}

        # Sempre MBR
        clean_command = "clean all" if mode == "advanced" else "clean"

        diskpart_script = f"""
        select disk {disk_number}
        {clean_command}
        convert mbr
        create partition primary
        assign letter={drive_letter}
        exit
        """

        script_path = "diskpart_script.txt"
        with open(script_path, "w") as f:
            f.write(diskpart_script)

        if log_callback:
            log_callback("[Manager] Executando DiskPart...")

        code, out, err = self.executor.run_command(
            ["diskpart", "/s", script_path],
            timeout=None,
            log_callback=log_callback
        )

        os.remove(script_path)

        if code != 0:
            return {"success": False, "message": "Falha no DiskPart", "exit_code": code}

        # =============================
        # FORMATAÇÃO
        # =============================

        if filesystem.upper() == "FAT32":
            fat32_exe = os.path.abspath("assets/FAT32FORMAT.EXE")

            format_cmd = [
                fat32_exe,
                f"{drive_letter}:"
            ]

        else:
            format_cmd = [
                "format",
                f"{drive_letter}:",
                "/FS:exFAT",
                "/Q" if quick else ""
            ]

        if log_callback:
            log_callback("[Manager] Executando formatação...")

        code, out, err = self.executor.run_command(
            format_cmd,
            timeout=None,
            log_callback=log_callback
        )

        if code != 0:
            return {"success": False, "message": "Falha na formatação", "exit_code": code}

        return {"success": True, "message": "Formatação concluída", "exit_code": 0}