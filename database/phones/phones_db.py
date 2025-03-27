from database.database import DB
from models.phone import Phone


class PhonesDB(DB):
    TABLE_NAME = 'phones'

    ID = 'phone_id'
    MODEL = 'model'
    COLOR = 'color'
    MEMORY = 'memory'
    BATTERY_STATUS = 'battery_status'

    def __init__(self):
        super().__init__()
        self._create_table(self.TABLE_NAME, self.get_columns())

    def get_columns(self):
        return {
            self.ID: 'INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL',
            self.MODEL: 'TEXT NOT NULL',
            self.COLOR: 'TEXT',
            self.MEMORY: 'INTEGER NOT NULL',
            self.BATTERY_STATUS: 'INTEGER NOT NULL',
        }

    def add_phone(self, phone:'Phone') -> int:
        f"""Returns {self.ID}"""
        return self._insert_data(self.TABLE_NAME, {
            self.MODEL: phone.model,
            self.COLOR: phone.color,
            self.MEMORY: phone.memory,
            self.BATTERY_STATUS: phone.battery_status
        }).lastrowid

    def get_phone(self, phone_id:int) -> 'Phone':
        """Returns Phone without defects"""
        answer = self._fetchone(f"""SELECT {self.MODEL}, {self.COLOR}, {self.MEMORY}, {self.BATTERY_STATUS} 
                              FROM {self.TABLE_NAME} WHERE {self.ID} = {DB.sql(phone_id)};""")
        if not answer:
            return None
        phone = Phone(answer[0])
        phone.color = answer[1]
        phone.memory = answer[2]
        phone.battery_status = answer[3]
        return phone

    def update_memory(self, id: int, memory: int):
        self._update_data(self.TABLE_NAME, self.MEMORY, memory, f'WHERE {self.ID} = {DB.sql(id)}')

    def update_battery_status(self, id: int, battery_status: int):
        self._update_data(self.TABLE_NAME, self.BATTERY_STATUS, battery_status, f'WHERE {self.ID} = {DB.sql(id)}')

    def get_phones(self, limit:int = 0, offset:int = 0) -> list[(int, 'Phone')]:
        """Returns list[(id, phone)]"""
        answer = self._fetchall(f"""SELECT {self.ID}, {self.MODEL}, {self.COLOR}, {self.MEMORY}, {self.BATTERY_STATUS} 
                              FROM {self.TABLE_NAME}
                              {f"LIMIT {limit} OFFSET {offset}" if limit else ''};""")
        phones = list()
        if not answer:
            return phones

        for phone_id, model, color, memory, battery_status in answer:
            phone = Phone(model)
            phone.color = color
            phone.memory = memory
            phone.battery_status = battery_status
            phones.append((int(phone_id), phone))
        return phones