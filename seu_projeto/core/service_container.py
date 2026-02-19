from database.db_manager import DatabaseManager
from core.game_service import GameService
from core.unit_service import UnitService
from core.integrity_checker import check_drive_integrity
from core.ul_manager import ULManager


class ServiceContainer:
    """
    Fonte única de serviços da aplicação.
    """

    def __init__(self):
        self.db = DatabaseManager()
        self.games = GameService(self.db)
        self.units = UnitService(self.db)
        self.integrity_checker = check_drive_integrity
        self.ul_manager = ULManager()

    def close(self):
        if self.db:
            self.db.close()
