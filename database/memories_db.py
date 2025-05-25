from database.database import DB


class MemoriesDB(DB):
    TABLE_NAME = 'memories'

    ID = 'memory_id'
    MEMORY = 'memory'

    def __init__(self):
        super().__init__()
        self._create_table(self.TABLE_NAME, self.get_columns())

    def get_columns(self):
        return {
            self.ID: 'INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL',
            self.MEMORY: 'INTEGER UNIQUE NOT NULL',
        }

    def add_memory(self, memory: int):
        try:
            memory = int(memory)
        except TypeError:
            raise TypeError("Введите целую цифру!")
        self._insert_data(
            self.TABLE_NAME,
            {self.MEMORY: memory}
        )

    def get_memory(self, memory_id: int) -> int:
        answer = self._fetchone(
            f"SELECT DISTINCT {self.MEMORY} FROM {self.TABLE_NAME} WHERE {self.ID} = {memory_id};"
        )
        return answer[0]

    def delete_memory(self, memory_id: int):
        self._delete_data(self.TABLE_NAME, f"WHERE {self.ID} = {memory_id}")

    def get_memories(self, limit: int = 0, offset: int = 0) -> dict[int, int]:
        """RETURNS {memory_id:memory}"""
        answer = self._fetchall(
            f"""SELECT DISTINCT {self.ID}, {self.MEMORY} 
            FROM {self.TABLE_NAME} 
            ORDER BY {self.MEMORY} ASC
            {f"LIMIT {limit} OFFSET {offset}" if limit else ''};"""
        )
        return {line[0]: line[1] for line in answer}

    def get_memories_by_id(
        self, memory_id_list: list[int] = None, limit: int = 0, offset: int = 0
    ) -> dict[int, int]:
        """RETURNS {memory_id:memory}"""
        if not memory_id_list:
            return dict()
        answer = self._fetchall(
            f"""SELECT DISTINCT {self.ID}, {self.MEMORY} FROM {self.TABLE_NAME} 
            WHERE {' OR '.join([f"{self.ID} = {memory_id}" for memory_id in memory_id_list])} 
            ORDER BY {self.MEMORY} ASC
            {f"LIMIT {limit} OFFSET {offset}" if limit else ''};"""
        )
        return {line[0]: line[1] for line in answer}
