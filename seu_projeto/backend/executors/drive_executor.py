# backend/executors/drive_executor.py

import subprocess
import time
from typing import Tuple, Optional


class DriveExecutor:

    def __init__(self, max_retries: int = 3):
        self.max_retries = max_retries

    def run_command(
        self,
        command: list,
        timeout: Optional[int] = None,
        log_callback=None
    ) -> Tuple[int, str, str]:

        last_exception = None

        for attempt in range(1, self.max_retries + 1):
            try:
                if log_callback:
                    log_callback(f"[Executor] Tentativa {attempt}/{self.max_retries}")

                result = subprocess.run(
                    command,
                    capture_output=True,
                    text=True,
                    timeout=timeout
                )

                if log_callback:
                    log_callback(f"[Executor] Exit Code: {result.returncode}")

                if result.returncode == 0:
                    return result.returncode, result.stdout, result.stderr

                if log_callback:
                    log_callback("[Executor] Comando falhou, tentando novamente...")

            except subprocess.TimeoutExpired as e:
                last_exception = e
                if log_callback:
                    log_callback("[Executor] Timeout atingido, tentando novamente...")

            except Exception as e:
                last_exception = e
                if log_callback:
                    log_callback(f"[Executor] Erro inesperado: {e}")

            time.sleep(2)

        if last_exception:
            raise last_exception

        return 1, "", "Falha após múltiplas tentativas"