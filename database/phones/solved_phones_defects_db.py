from database.database import DB
from database.phones.phones_db import PhonesDB


class SolvedPhonesDefectsDB(DB):
    TABLE_NAME = 'solved_phones_defects'

    PHONE_ID = 'phone_id'
    defect = 'defect'

    def __init__(self):
        super().__init__()        

        self._create_table(self.TABLE_NAME, self.get_columns(), [
            f"FOREIGN KEY ({self.PHONE_ID}) REFERENCES {PhonesDB.TABLE_NAME} ({PhonesDB.ID})",
        ])

    def get_columns(self):
        return {
            self.PHONE_ID: 'INTEGER NOT NULL',
            self.defect: 'TEXT NOT NULL',
        }

    def add_defect(self, phone_id: int, defect: str):
        self._insert_data(self.TABLE_NAME, {self.PHONE_ID: phone_id,
                                            self.defect: defect})

    def add_defects(self, phone_id: int, defects: list[str]):
        for defect in defects:
            self.add_defect(phone_id, defect)