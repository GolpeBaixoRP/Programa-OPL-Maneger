import os
import sys

# Sobe um nível até a raiz do projeto
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

from backend.services.drive_format_service import DriveFormatService
from backend.services.device_service import DeviceService

def log_console(message):
    print(message)


def main():

    device_service = DeviceService()
    format_service = DriveFormatService()

    print("\n=== DISPOSITIVOS DISPONÍVEIS ===\n")

    devices = device_service.list_devices()

    if not devices:
        print("Nenhum dispositivo encontrado.")
        return

    for d in devices:
        print(
            f"Unidade: {d['letter']} | "
            f"FS: {d['filesystem']} | "
            f"Estilo: {d['partition_style']} | "
            f"Total: {round(d['total_bytes']/1024**3,2)} GB"
        )

    print("\n================================\n")

    drive_letter = input("Digite a letra da unidade (ex: E): ").upper()

    filesystem = input("Filesystem (FAT32 / exFAT): ").upper()

    mode = input("Modo (normal / advanced): ").lower()

    quick_input = input("Formatação rápida? (s/n): ").lower()
    quick = quick_input == "s"

    confirm = input("\n⚠ CONFIRMA FORMATAÇÃO? (DIGITE SIM): ")

    if confirm != "SIM":
        print("Operação cancelada.")
        return

    print("\nIniciando formatação...\n")

    result = format_service.format_drive(
        drive_letter=drive_letter,
        filesystem=filesystem,
        mode=mode,
        quick=quick,
        log_callback=log_console
    )

    print("\n=== RESULTADO ===")
    print(result)


if __name__ == "__main__":
    main()