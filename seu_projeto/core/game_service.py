from database.db_manager import DatabaseManager



class GameService:
    def __init__(self, db: DatabaseManager):
        self.db = db

    def add_ps2_game(self, nome, game_id=None, tamanho=None, unidade=None):
        self.db.add_ps2_game(nome, game_id, tamanho, unidade)

    def add_ps1_game(self, nome, game_id=None, formato=None, tamanho=None, unidade=None):
        self.db.add_ps1_game(nome, game_id, formato, tamanho, unidade)

    def get_all_ps2_games(self):
        return self.db.get_all_ps2_games()

    def get_all_ps1_games(self):
        return self.db.get_all_ps1_games()

    def log(self, nivel, mensagem):
        self.db.log(nivel, mensagem)
