import sqlite3
from abc import ABC, abstractmethod
from pathlib import Path
from datetime import datetime
from bot import DATE_TIME_FORMAT, TEMP_PATH, SETTINGS_PATH
import logging


class DB(ABC):
    __instances = {}
    DB_NAME = SETTINGS_PATH / 'database.db'

    def __new__(cls, *args, **kwargs):    
        if cls not in cls.__instances:
            instance = super().__new__(cls)
            cls.__instances[cls] = instance
        return cls.__instances[cls]

    def __init__(self):
        if not hasattr(self, "connection"):
            self.connection = sqlite3.connect(self.DB_NAME)

    def __del__(self):
        self.connection.close()

    @abstractmethod
    def get_columns(self) -> dict[str,str]:
        raise NotImplementedError('Implement get_columns() method with return dict[column_name, column_creation]')

    @staticmethod
    def sql(value: any) -> str:
        if value is None:
            return 'NULL'
        elif type(value) is bool:
            return str(int(value))
        elif type(value) is int:
            return str(value)
        elif type(value) is datetime:
            return f'\'{value.strftime(DATE_TIME_FORMAT)}\''
        return f'\'{value}\''

    def get_all_count(self) -> int:
        answer = self._fetchone(f"SELECT COUNT(*) FROM {self.TABLE_NAME}")
        return answer[0]

    def _execute(self, request: str) -> sqlite3.Cursor:
        logging.debug(request)
        cursor = self.connection.cursor()
        cursor.execute(request)
        self.connection.commit()
        return cursor

    def _fetchone(self, request: str) -> tuple[str]:
        return self._execute(request).fetchone()

    def _fetchall(self, request: str) -> list[any]:
        fetchall = self._execute(request).fetchall()
        return fetchall if fetchall else []

    def _create_table(self, table_name: str, columns: dict[str, any], additional_expressions:list[str] = None):
        if hasattr(self, "_table_created"):
            return
        self._table_created = True
        columns_definition = ',\n'.join([f"{name} {definition}" for name, definition in columns.items()])
        additional_expressions = list() if additional_expressions is None else additional_expressions
        additional = (',' + ',\n'.join(additional_expressions)) if additional_expressions else ''

        self._execute(f"""CREATE TABLE IF NOT EXISTS {table_name}(
{columns_definition}
{additional});""")

    def _insert_data(self, table_name: str, column_value: dict[str, any]) -> sqlite3.Cursor:
        return self._execute(f"""INSERT OR REPLACE INTO {table_name} ({', '.join(column_value.keys())}) VALUES 
                     ({', '.join(DB.sql(x) for x in list(column_value.values()))});""")

    def _update_data(self, table_name: str, column: str, value: str, where: str = '') -> sqlite3.Cursor:
        return self._execute(f"""UPDATE {table_name} SET {column} = {DB.sql(value)} {where};""")

    def _delete_data(self, table_name: str, where: str = '') -> sqlite3.Cursor:
        return self._execute(f"""DELETE FROM {table_name} {where}""")

    @staticmethod
    def get_backup() -> Path:
        """Make backup and send file location by Path"""
        source_connection = sqlite3.connect(DB.DB_NAME)
        back_up_name = TEMP_PATH / Path('database_backup.db')
        if back_up_name.exists():
            back_up_name.unlink()
        backup_connection = sqlite3.connect(back_up_name)
        with backup_connection:
            source_connection.backup(backup_connection)
        backup_connection.close()
        return back_up_name