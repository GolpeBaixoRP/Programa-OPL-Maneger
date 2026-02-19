from database.db_manager import DatabaseManager


class UnitService:
    def __init__(self, db: DatabaseManager):
        self.db = db

    def add_or_update_unit(self, letra, tipo, sistema_arquivos, capacidade):
        self.db.add_or_update_unit(letra, tipo, sistema_arquivos, capacidade)

    def get_units(self):
        return self.db.get_units()

    def clear_units(self):
        self.db.clear_units()
