from database.database import DB


class DefectsDB(DB):
    TABLE_NAME = 'defects'

    ID = 'defect_id'
    defect = 'defect'
    PRIORITY = 'priority'

    def __init__(self):
        super().__init__()
        self._create_table(self.TABLE_NAME, self.get_columns())

    def get_columns(self):
        return {
            self.ID: 'INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL',
            self.defect: 'TEXT UNIQUE NOT NULL',
            self.PRIORITY: 'INTEGER NOT NULL',
        }

    def add_defect(self, defect: str):
        self._insert_data(
            self.TABLE_NAME,
            {
                self.defect: defect,
                self.PRIORITY: 0
            }
        )

    def get_defects(self, limit: int = 0, offset: int = 0) -> dict[int, str]:
        """RETURNS {defect_id:defect}"""
        answer = self._fetchall(
            f"""SELECT {self.ID}, {self.defect} 
            FROM {self.TABLE_NAME} 
            ORDER BY {self.PRIORITY} DESC
            {f"LIMIT {limit} OFFSET {offset}" if limit else ''};"""
        )
        return {line[0]: line[1] for line in answer}

    def get_defect(self, id: int) -> str:
        answer = self._fetchone(
            f"""SELECT {self.defect} FROM {self.TABLE_NAME} WHERE {self.ID} = {id};"""
        )
        return answer[0]

    def delete_defect(self, id: int):
        self._delete_data(self.TABLE_NAME, f"WHERE {self.ID} = {id}")