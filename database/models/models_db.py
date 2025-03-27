from database.database import DB


class ModelsDB(DB):
    TABLE_NAME = 'models'

    ID = 'model_id'
    MODEL = 'model'
    PRIORITY = 'priority'

    def __init__(self):
        super().__init__()
        self._create_table(self.TABLE_NAME, self.get_columns())

    def get_columns(self):
        return {
            self.ID: 'INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL',
            self.MODEL: 'TEXT UNIQUE NOT NULL',
            self.PRIORITY: 'INTEGER NOT NULL',
        }

    def add_model(self, model:str) -> int:
        """RETURNS id"""
        return self._insert_data(self.TABLE_NAME, {
            self.MODEL: model,
            self.PRIORITY: 0
        }).lastrowid

    def get_models(self, limit:int = 0, offset:int = 0) -> dict[int, str]:
        answer = self._fetchall(f"""SELECT {self.ID}, {self.MODEL} 
                                FROM {self.TABLE_NAME} 
                                ORDER BY {self.PRIORITY} DESC
                                {f"LIMIT {limit} OFFSET {offset}" if limit else ''};""")
        return {line[0]: line[1] for line in answer}

    def get_model(self, model_id:int) -> str:
        answer = self._fetchone(f"SELECT {self.MODEL} FROM {self.TABLE_NAME} WHERE {self.ID} = {model_id};")
        return answer[0] 

    def get_model_id(self, model:str) -> int:
        answer = self._fetchone(f"SELECT {self.ID} FROM {self.TABLE_NAME} WHERE {self.MODEL} = {DB.sql(model)};")
        return None if not answer[0] else int(answer[0]) 

    def delete_model(self, model_id:int):
        self._delete_data(self.TABLE_NAME, f"WHERE {self.ID} = {model_id}")
