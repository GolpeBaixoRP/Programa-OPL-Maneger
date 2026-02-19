import sqlite3
import os
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path="data/app.db"):
        os.makedirs("data", exist_ok=True)
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.create_tables()

    # ================= TABELAS =================

    def create_tables(self):
        cursor = self.conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS jogos_ps2 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            game_id TEXT,
            tamanho REAL,
            unidade TEXT,
            data_gravacao TEXT
        )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS jogos_ps1 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            game_id TEXT,
            formato TEXT,
            tamanho REAL,
            unidade TEXT,
            data_gravacao TEXT
        )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS unidades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            letra TEXT UNIQUE,
            tipo TEXT,
            sistema_arquivos TEXT,
            capacidade TEXT,
            ultima_verificacao TEXT
        )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nivel TEXT,
            mensagem TEXT,
            origem TEXT,
            data TEXT
        )''')

        self.conn.commit()

    # ================= PS2 =================

    def add_ps2_game(self, nome, game_id=None, tamanho=None, unidade=None):
        self.conn.execute(
            "INSERT INTO jogos_ps2 (nome, game_id, tamanho, unidade, data_gravacao) VALUES (?, ?, ?, ?, ?)",
            (nome, game_id, tamanho, unidade, self._now())
        )
        self.conn.commit()

    def get_all_ps2_games(self):
        return self.conn.execute("SELECT * FROM jogos_ps2").fetchall()

    # ================= PS1 =================

    def add_ps1_game(self, nome, game_id=None, formato=None, tamanho=None, unidade=None):
        self.conn.execute(
            "INSERT INTO jogos_ps1 (nome, game_id, formato, tamanho, unidade, data_gravacao) VALUES (?, ?, ?, ?, ?, ?)",
            (nome, game_id, formato, tamanho, unidade, self._now())
        )
        self.conn.commit()

    def get_all_ps1_games(self):
        return self.conn.execute("SELECT * FROM jogos_ps1").fetchall()

    # ================= UNIDADES (NOVO) =================

    def add_or_update_unit(self, letra, tipo, sistema_arquivos, capacidade):
        self.conn.execute("""
            INSERT INTO unidades (letra, tipo, sistema_arquivos, capacidade, ultima_verificacao)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(letra) DO UPDATE SET
                tipo=excluded.tipo,
                sistema_arquivos=excluded.sistema_arquivos,
                capacidade=excluded.capacidade,
                ultima_verificacao=excluded.ultima_verificacao
        """, (letra, tipo, sistema_arquivos, capacidade, self._now()))
        self.conn.commit()

    def get_units(self):
        return self.conn.execute("SELECT * FROM unidades").fetchall()

    def clear_units(self):
        self.conn.execute("DELETE FROM unidades")
        self.conn.commit()

    # ================= LOG =================

    def log(self, nivel, mensagem, origem="system"):
        self.conn.execute(
            "INSERT INTO logs (nivel, mensagem, origem, data) VALUES (?, ?, ?, ?)",
            (nivel, mensagem, origem, self._now())
        )
        self.conn.commit()

    # ================= UTILS =================

    def _now(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def close(self):
        self.conn.close()
