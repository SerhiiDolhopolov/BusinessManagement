from database.database import DB
from database.models.models_db import ModelsDB
from database.colors_db import ColorsDB


class ModelsColorsDB(DB):
    TABLE_NAME = 'models_colors'

    MODEL_ID = 'model_id'
    COLOR_ID = 'color_id'

    def __init__(self):
        super().__init__()

        self._create_table(
            self.TABLE_NAME,
            self.get_columns(),
            [
                f"FOREIGN KEY ({self.MODEL_ID}) REFERENCES {ModelsDB.TABLE_NAME} ({ModelsDB.ID})",
                f"FOREIGN KEY ({self.COLOR_ID}) REFERENCES {ColorsDB.TABLE_NAME} ({ColorsDB.ID}) ON DELETE CASCADE"
            ]
        )

    def get_columns(self):
        return {
            self.MODEL_ID: 'INTEGER',
            self.COLOR_ID: 'INTEGER'
        }

    def is_related(self, model_id: int, color_id: int) -> bool:
        answer = self._fetchone(
            f"SELECT COUNT(*) FROM {self.TABLE_NAME} WHERE {self.MODEL_ID} = {model_id} "
            f"AND {self.COLOR_ID} = {color_id};"
        )
        return None if not answer else bool(answer[0])

    def add_relation(self, model_id: int, color_id: int):
        self._insert_data(
            self.TABLE_NAME,
            {
                self.MODEL_ID: model_id,
                self.COLOR_ID: color_id,
            }
        )

    def delete_relation(self, model_id: int, color_id: int):
        self._delete_data(
            self.TABLE_NAME,
            f"WHERE {self.MODEL_ID} = {model_id} AND {self.COLOR_ID} = {color_id}"
        )

    def get_count_for_model(self, model_id: int) -> int:
        answer = self._fetchone(
            f"""SELECT COUNT(DISTINCT {self.COLOR_ID})
            FROM {self.TABLE_NAME}
            WHERE {self.MODEL_ID} = {model_id};"""
        )
        return None if not answer else int(answer[0])

    def get_colors_id(self, model_id: int) -> list[int]:
        answer = self._fetchall(
            f"SELECT DISTINCT {self.COLOR_ID} FROM {self.TABLE_NAME} WHERE {self.MODEL_ID} = {model_id};"
        )
        return [] if not answer else [color_id[0] for color_id in answer]

    def get_colors_with_flag(
        self, model_id: int, limit: int = 0, offset: int = 0
    ) -> dict[int, (str, bool)]:
        """RETURNS { color_id: (color, is_using_by_model) }"""
        answer = self._fetchall(
            f"""SELECT DISTINCT {ColorsDB.ID}, {ColorsDB.COLOR}, CASE WHEN
            {ColorsDB.ID} IN 
            (SELECT {self.COLOR_ID} FROM {self.TABLE_NAME} WHERE {self.MODEL_ID} = {model_id})
            THEN {True}
            ELSE {False}
            END AS Flag
            FROM {ColorsDB.TABLE_NAME}
            ORDER BY {ColorsDB.PRIORITY} DESC
            {f"LIMIT {limit} OFFSET {offset}" if limit else ''};"""
        )
        return {} if not answer else {int(line[0]): (line[1], bool(line[2])) for line in answer}