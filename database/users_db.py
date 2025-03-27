from database.database import DB
from enum import Enum

from UI import UI_roles


class Role(Enum):
    ADMIN = UI_roles.get_admin()
    MANAGER = UI_roles.get_manager()
    COURIER = UI_roles.get_courier()
    USER = UI_roles.get_user()

    def __str__(self):
        return self.value


class RoleManager:
    @staticmethod
    def get_emoji(role:Role) -> str:
        return '🅰️' if role == Role.ADMIN else \
                'Ⓜ️' if role == Role.MANAGER else \
                '📦' if role == Role.COURIER else \
                '👤' if role == Role.USER else \
                ''


class UsersDB(DB):
    TABLE_NAME = 'users'

    ID = 'user_id'
    USERNAME = 'username'
    ROLE = 'role'

    def __init__(self):
        super().__init__()
        self._create_table(self.TABLE_NAME, self.get_columns())

    def get_columns(self):
        return {
            self.ID: 'INTEGER PRIMARY KEY UNIQUE NOT NULL',
            self.USERNAME: 'TEXT',
            self.ROLE: 'TEXT NOT NULL',
        }

    def register_user(self, telegram_id:int, username:str):
        self._insert_data(self.TABLE_NAME, {
            self.ID: telegram_id,
            self.USERNAME: username,
            self.ROLE: Role.USER,
        })

    def __get_users_request(self, where:str = '', limit:int = 0, offset:int = 0) -> list[tuple[int, str, 'Role']]:
        """RETURNS list[(telegram_id, username, role)]"""
        users = self._fetchall(f"""SELECT {self.ID}, {self.USERNAME}, {self.ROLE} FROM {self.TABLE_NAME} 
                               {where} 
                               ORDER BY CASE {self.ROLE}
                                    WHEN '{Role.ADMIN}' THEN 1
                                    WHEN '{Role.MANAGER}' THEN 2
                                    WHEN '{Role.COURIER}' THEN 3
                                    WHEN '{Role.USER}' THEN 4
                                    ELSE 5
                               END
                               {f"LIMIT {limit} OFFSET {offset}" if limit else ''};""")
        return [] if not users else [(int(line[0]), line[1], Role(line[2])) for line in users]

    def get_users(self, limit:int=0, offset:int=0) -> list[(int, str, Role)]:
        """RETURNS list[(telegram_id, username, role)]"""
        return self.__get_users_request('', limit, offset)

    def get_users_by_role(self, role:Role, limit:int=0, offset:int=0) -> list[(int, str, Role)]:
        """RETURNS list[(telegram_id, username, role)]"""
        return self.__get_users_request(f"WHERE {self.ROLE} = \'{role}\'", limit, offset)

    def get_admins(self, except_telegram_id: int = None) -> list[(int, str, Role)]:
        """RETURNS list[(telegram_id, username, role)]"""
        return self.__get_users_request(f"""WHERE {self.ROLE} IN (\'{Role.ADMIN}\') 
                                        {f'AND {self.ID} != {except_telegram_id}' if except_telegram_id else ''}""")

    def get_managers_and_higher(self, except_telegram_id:int=None) -> list[(int, str, Role)]:
        """RETURNS list[(telegram_id, username, role)]"""
        return self.__get_users_request(f"""WHERE {self.ROLE} IN (\'{Role.ADMIN}\', \'{Role.MANAGER}\') 
                                        {f'AND {self.ID} != {except_telegram_id}' if except_telegram_id else ''}""")

    def __get_users_count_request(self, where:str = '') -> int:
        """RETURNS count"""
        count = self._fetchone(f"""SELECT COUNT(*) FROM {self.TABLE_NAME}
                              {where};""") 
        return 0 if not count else count[0]

    def get_users_count(self) -> int:
        """RETURNS count"""
        return self.__get_users_count_request('')

    def get_users_by_role_count(self, role:Role) -> int:
        """RETURNS count users by role"""
        return self.__get_users_count_request(f"WHERE {self.ROLE} = \'{role}\'")

    def is_user_exist(self, telegram_id:int) -> bool:
        return bool(self.get_user(telegram_id))

    def get_user(self, telegram_id:int) -> tuple[str, Role]:
        """RETURNS (username, Role)"""
        user = self._fetchone(f"SELECT {self.USERNAME}, {self.ROLE} FROM {self.TABLE_NAME} WHERE {self.ID} = {telegram_id}")
        return None if not user else (user[0], Role(user[1]))

    def get_username(self, telegram_id:int) -> str:
        user = self.get_user(telegram_id)
        return None if not user else user[0]

    def get_role(self, telegram_id:int) -> Role:
        user = self.get_user(telegram_id)
        return None if not user else user[1]

    def set_username(self, telegram_id:int, username:str):
        self._update_data(self.TABLE_NAME, self.USERNAME, username, f"WHERE {self.ID} = {telegram_id}")

    def set_role(self, telegram_id:int, role:Role):
        self._update_data(self.TABLE_NAME, self.ROLE, role, f"WHERE {self.ID} = {telegram_id}")
