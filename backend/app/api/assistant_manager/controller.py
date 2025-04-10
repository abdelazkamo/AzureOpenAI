from app.database.db_operation import DB_Operations


class Controller:
    def __init__(self, db: DB_Operations) -> None:
        self.db = db
