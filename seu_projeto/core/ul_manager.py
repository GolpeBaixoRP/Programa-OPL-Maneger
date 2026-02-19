import os
import math
import zlib

UL_CHUNK_SIZE = 1073741824  # 1GB


class ULManager:

    @staticmethod
    def calculate_crc32(filepath):
        crc = 0
        with open(filepath, "rb") as f:
            while True:
                chunk = f.read(1024 * 1024)
                if not chunk:
                    break
                crc = zlib.crc32(chunk, crc)
        return f"{crc & 0xFFFFFFFF:08X}"

    @staticmethod
    def extract_game_id(iso_path):
        prefixes = [b"SLUS_", b"SLES_", b"SCUS_", b"SCES_", b"SLPM_", b"SCPS_"]

        with open(iso_path, "rb") as f:
            data = f.read(5 * 1024 * 1024)

        for p in prefixes:
            idx = data.find(p)
            if idx != -1:
                return data[idx:idx+11].decode("ascii")

        return None

    @staticmethod
    def write_ul_cfg(root_path, game_name, game_id, total_parts, is_dvd):
        cfg_path = os.path.join(root_path, "ul.cfg")
        entry = bytearray(64)

        display_name = os.path.splitext(game_name)[0]
        name_bytes = display_name.encode("ascii", errors="ignore")[:32]
        entry[0:len(name_bytes)] = name_bytes

        base_string = f"ul.{game_id}"
        base_bytes = base_string.encode("ascii")[:16]
        entry[0x20:0x20+len(base_bytes)] = base_bytes

        entry[0x30:0x32] = total_parts.to_bytes(2, "little")
        disc_type = 0x0014 if is_dvd else 0x0012
        entry[0x32:0x34] = disc_type.to_bytes(2, "little")
        entry[0x34:0x38] = (0).to_bytes(4, "little")

        mode = "ab" if os.path.exists(cfg_path) else "wb"

        with open(cfg_path, mode) as f:
            f.write(entry)

    @staticmethod
    def split_to_ul(src_path, root_path, display_name, progress_callback=None):
        game_id = ULManager.extract_game_id(src_path)
        if not game_id:
            raise Exception("Game ID não encontrado")

        crc32 = ULManager.calculate_crc32(src_path)
        file_size = os.path.getsize(src_path)
        total_parts = math.ceil(file_size / UL_CHUNK_SIZE)
        is_dvd = file_size >= 700 * 1024 * 1024

        with open(src_path, "rb") as src:
            for part in range(total_parts):

                part_name = f"ul.{crc32}.{game_id}.{part:02d}"
                dest_path = os.path.join(root_path, part_name)

                with open(dest_path, "wb") as out:

                    remaining = min(
                        UL_CHUNK_SIZE,
                        file_size - (part * UL_CHUNK_SIZE)
                    )

                    written = 0

                    while written < remaining:
                        chunk = src.read(
                            min(1024 * 1024, remaining - written)
                        )
                        if not chunk:
                            break

                        out.write(chunk)
                        written += len(chunk)

                        if progress_callback:
                            progress_callback(written / remaining)

        ULManager.write_ul_cfg(
            root_path,
            display_name,
            game_id,
            total_parts,
            is_dvd
        )
