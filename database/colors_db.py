from database.database import DB


class ColorsDB(DB):
    TABLE_NAME = 'colors'

    ID = 'color_id'
    COLOR = 'color'
    PRIORITY = 'priority'

    def __init__(self):
        super().__init__()
        self._create_table(self.TABLE_NAME, self.get_columns())

    def get_columns(self):
        return {
            self.ID: 'INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL',
            self.COLOR: 'TEXT UNIQUE NOT NULL',
            self.PRIORITY: 'INTEGER NOT NULL',
        }

    def add_color(self, color: str):
        self._insert_data(self.TABLE_NAME, {
            self.COLOR: color,
            self.PRIORITY: 0
        })

    def get_color(self, color_id: int) -> str:
        answer = self._fetchone(f"SELECT DISTINCT {self.COLOR} FROM {self.TABLE_NAME} WHERE {self.ID} = {color_id};")
        return answer[0] 

    def get_color_id(self, color: str) -> int:
        answer = self._fetchone(f"SELECT DISTINCT {self.ID} FROM {self.TABLE_NAME} WHERE {self.COLOR} = {DB.sql(color)};")
        return answer[0] 

    def delete_color(self, color_id: int):
        self._delete_data(self.TABLE_NAME, f"WHERE {self.ID} = {color_id}")

    def get_colors(self, limit: int = 0, offset: int = 0) -> dict[int, str]:
        """RETURNS {color_id:color}"""
        answer = self._fetchall(f"""SELECT DISTINCT {self.ID}, {self.COLOR} 
                                FROM {self.TABLE_NAME} 
                                ORDER BY {self.PRIORITY} DESC
                                {f"LIMIT {limit} OFFSET {offset}" if limit else ''};""")
        return {line[0]: line[1] for line in answer} if answer else dict()

    def get_colors_by_id(self, color_id_list: list[int] = None, limit: int = 0, offset: int = 0) -> dict[int, str]:
        """RETURNS {color_id:color}"""
        if not color_id_list:
            return dict()
        answer = self._fetchall(f"""SELECT DISTINCT {self.ID}, {self.COLOR} FROM {self.TABLE_NAME} 
                                WHERE {' OR '.join([f"{self.ID} = {color_id}" for color_id in color_id_list])} 
                                ORDER BY {self.PRIORITY} DESC
                                {f"LIMIT {limit} OFFSET {offset}" if limit else ''};""")
        return {line[0]: line[1] for line in answer} if answer else dict()
