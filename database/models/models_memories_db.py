from database.database import DB
from database.models.models_db import ModelsDB
from database.memories_db import MemoriesDB


class ModelsMemoriesDB(DB):
    TABLE_NAME = 'models_memories'

    MODEL_ID = 'model_id'
    MEMORY_ID = 'memory_id'

    def __init__(self):
        super().__init__()        

        self._create_table(self.TABLE_NAME, self.get_columns(), [
            f"FOREIGN KEY ({self.MODEL_ID}) REFERENCES {ModelsDB.TABLE_NAME} ({ModelsDB.ID})",
            f"FOREIGN KEY ({self.MEMORY_ID}) REFERENCES {MemoriesDB.TABLE_NAME} ({MemoriesDB.ID}) ON DELETE CASCADE"
        ])

    def get_columns(self):
        return {
            self.MODEL_ID: 'INTEGER',
            self.MEMORY_ID: 'INTEGER'
        }

    def is_related(self, model_id:int, memory_id:int) -> bool:
        answer = self._fetchone(f"SELECT COUNT(*) FROM {self.TABLE_NAME} WHERE {self.MODEL_ID} = {model_id} AND {self.MEMORY_ID} = {memory_id};")
        return None if not answer else bool(answer[0])

    def add_relation(self, model_id:int, memory_id:int):
        self._insert_data(self.TABLE_NAME, {
            self.MODEL_ID: model_id,
            self.MEMORY_ID: memory_id,
        })

    def delete_relation(self, model_id:int, memory_id:int):
        self._delete_data(self.TABLE_NAME, f"WHERE {self.MODEL_ID} = {model_id} AND {self.MEMORY_ID} = {memory_id}")

    def get_count_for_model(self, model_id:int) -> int:
        answer = self._fetchone(f"""SELECT COUNT(DISTINCT {self.MEMORY_ID})
                                FROM {self.TABLE_NAME}
                                WHERE {self.MODEL_ID} = {model_id};""")
        return None if not answer else int(answer[0])

    def get_memories_id(self, model_id:int) -> list[int]:
        answer = self._fetchall(f"SELECT DISTINCT {self.MEMORY_ID} FROM {self.TABLE_NAME} WHERE {self.MODEL_ID} = {model_id};")
        return [] if not answer else [memory_id[0] for memory_id in answer]

    def get_memories_with_flag(self, model_id:int, limit:int = 0, offset:int = 0) -> dict[int:(int, bool)]:
        """RETURNS { color_id: (memory, is_using_by_model) }"""
        answer = self._fetchall(f"""SELECT DISTINCT {MemoriesDB.ID}, {MemoriesDB.MEMORY}, CASE WHEN
                                {MemoriesDB.ID} IN 
                                (SELECT {self.MEMORY_ID} FROM {self.TABLE_NAME} WHERE {self.MODEL_ID} = {model_id})
                                THEN {True}
                                ELSE {False}
                                END AS Flag
                                FROM {MemoriesDB.TABLE_NAME}
                                ORDER BY {MemoriesDB.MEMORY} ASC
                                {f"LIMIT {limit} OFFSET {offset}" if limit else ''};""")
        return {} if not answer else {int(line[0]):(int(line[1]), bool(line[2])) for line in answer}