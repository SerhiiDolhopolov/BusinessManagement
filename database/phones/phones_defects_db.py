from database.database import DB
from database.phones.phones_db import PhonesDB


class PhonesDefectsDB(DB):
    TABLE_NAME = 'phones_defects'

    PHONE_ID = 'phone_id'
    defect = 'defect'

    def __init__(self):
        super().__init__()        

        self._create_table(self.TABLE_NAME, self.get_columns(), [
            f"FOREIGN KEY ({self.PHONE_ID}) REFERENCES {PhonesDB.TABLE_NAME} ({PhonesDB.ID})"
        ])

    def get_columns(self):
        return {
            self.PHONE_ID: 'INTEGER',
            self.defect: 'TEXT'
        }

    def add_defect(self, phone_id: int, defect: str):
        self._insert_data(self.TABLE_NAME, {self.PHONE_ID: phone_id,
                                            self.defect: defect})

    def add_defects(self, phone_id: int, defects: list[str]):
        for defect in defects:
            self.add_defect(phone_id, defect)

    def clear_defects(self, phone_id: int):
        self._delete_data(self.TABLE_NAME, f'WHERE {self.PHONE_ID} = {DB.sql(phone_id)}')

    def get_phone_defects(self, phone_id: int) -> list[str]:
        """RETURNS list(defect)"""
        answer = self._fetchall(f"""SELECT {self.defect} 
                                FROM {self.TABLE_NAME}
                                WHERE {self.PHONE_ID} = {DB.sql(phone_id)};""")
        return list() if not answer else [line[0] for line in answer]