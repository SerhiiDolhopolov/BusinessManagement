from database.database import DB
from datetime import datetime

from database.phones.phones_db import PhonesDB

from models.status import Status, StatusType
from models.order import Order
from models.phone import Phone


class OrdersDB(DB):
    TABLE_NAME = 'orders'

    ID = 'order_id'
    PHONE_ID = 'phone_id'
    PRICE_PURCHASE = 'price_purchase'
    PRICE_SELLING = 'price_selling'
    CHARGES = 'charges'

    def __init__(self):
        super().__init__()
        self._create_table(
            self.TABLE_NAME,
            self.get_columns(),
            [
                f"FOREIGN KEY ({self.PHONE_ID}) REFERENCES {PhonesDB.TABLE_NAME} ({PhonesDB.ID})"
            ]
        )

    def get_columns(self):
        return {
            self.ID: 'INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL',
            self.PHONE_ID: 'INTEGER',
            self.PRICE_PURCHASE: 'REAL',
            self.PRICE_SELLING: 'REAL',
            self.CHARGES: 'REAL',
        }

    def add_order(self, phone_id: int, price_purchase: float) -> int:
        """RETURNS order_id"""
        return self._insert_data(
            self.TABLE_NAME,
            {
                self.PHONE_ID: phone_id,
                self.PRICE_PURCHASE: price_purchase
            }
        ).lastrowid

    def get_order(self, order_id: int) -> Order:
        from database.orders.statuses_db import StatusesDB
        answer = self._fetchone(
            f"""SELECT {self.PRICE_PURCHASE}, {self.PRICE_SELLING}, {self.CHARGES},
            {StatusesDB.STATUS_TYPE}, {StatusesDB.COMMENT}, MAX({StatusesDB.DATE_TIME})
            FROM {self.TABLE_NAME}
            JOIN {StatusesDB.TABLE_NAME} USING ({self.ID})
            WHERE {self.ID} = {DB.sql(order_id)};"""
        )
        if not answer:
            return None
        status = Status(StatusType(answer[3]))
        status.comment = answer[4]
        status.date_time = answer[5]
        order = Order(status)
        order.price_purchase = answer[0]
        order.price_selling = answer[1]
        order.charges = answer[2]
        return order

    def get_phone_id(self, order_id: int) -> int:
        answer = self._fetchone(
            f"""SELECT {OrdersDB.PHONE_ID}
            FROM {OrdersDB.TABLE_NAME}
            WHERE {OrdersDB.ID} = {DB.sql(order_id)};"""
        )
        return None if not answer else int(answer[0])

    def get_order_id(self, phone_id: int) -> int:
        answer = self._fetchone(
            f"""SELECT {OrdersDB.ID}
            FROM {OrdersDB.TABLE_NAME}
            WHERE {OrdersDB.PHONE_ID} = {DB.sql(phone_id)};"""
        )
        return None if not answer else int(answer[0])

    def update_price_purchase(self, order_id: int, price: float):
        self._update_data(
            OrdersDB.TABLE_NAME,
            OrdersDB.PRICE_PURCHASE,
            price,
            f'WHERE {OrdersDB.ID} = {DB.sql(order_id)}'
        )

    def update_price_selling(self, order_id: int, price: float):
        self._update_data(
            OrdersDB.TABLE_NAME,
            OrdersDB.PRICE_SELLING,
            price,
            f'WHERE {OrdersDB.ID} = {DB.sql(order_id)}'
        )

    def update_charges(self, order_id: int, price: float):
        self._update_data(
            OrdersDB.TABLE_NAME,
            OrdersDB.CHARGES,
            price,
            f'WHERE {OrdersDB.ID} = {DB.sql(order_id)}'
        )

    def get_statistics(
        self, status_type: StatusType = None, min_date: datetime = None
    ) -> dict[str, any]:
        """RETURNS dict[name, value] with data:
        count of statuses
        min|avg|max|sum of price_purchase|price_selling|charges
        """
        from database.orders.statuses_db import StatusesDB
        if min_date:
            min_date = min_date.replace(microsecond=0)
        answer = self._fetchone(
            f"""SELECT COUNT({StatusesDB.STATUS_TYPE}),
            MIN(COALESCE({OrdersDB.PRICE_PURCHASE}, 0)),
            AVG(COALESCE({OrdersDB.PRICE_PURCHASE}, 0)),
            MAX(COALESCE({OrdersDB.PRICE_PURCHASE}, 0)),
            SUM(COALESCE({OrdersDB.PRICE_PURCHASE}, 0)),

            MIN(COALESCE({OrdersDB.PRICE_SELLING}, 0)),
            AVG(COALESCE({OrdersDB.PRICE_SELLING}, 0)),
            MAX(COALESCE({OrdersDB.PRICE_SELLING}, 0)),
            SUM(COALESCE({OrdersDB.PRICE_SELLING}, 0)),

            MIN(COALESCE({OrdersDB.CHARGES}, 0)),
            AVG(COALESCE({OrdersDB.CHARGES}, 0)),
            MAX(COALESCE({OrdersDB.CHARGES}, 0)),
            SUM(COALESCE({OrdersDB.CHARGES}, 0))

            FROM {OrdersDB.TABLE_NAME}
            JOIN (SELECT {StatusesDB.ID}, {StatusesDB.USER_ID}, {StatusesDB.ORDER_ID},
            {StatusesDB.STATUS_TYPE}, {StatusesDB.COMMENT}, MAX({StatusesDB.DATE_TIME}) as date
            FROM {StatusesDB.TABLE_NAME}
            GROUP BY {OrdersDB.ID}) USING ({OrdersDB.ID})
            {'WHERE' if status_type or min_date else ''}
            {f"{StatusesDB.DATE_TIME} > {DB.sql(min_date)}" if min_date else ''}
            {'AND' if status_type and min_date else ''}
            {f"{StatusesDB.STATUS_TYPE} = {DB.sql(status_type)}" if status_type else ''};"""
        )
        if not answer or int(answer[0] == 0):
            return dict()
        result = {
            'count': int(answer[0]),
            'min_price_purchase': float(answer[1]),
            'avg_price_purchase': float(answer[2]),
            'max_price_purchase': float(answer[3]),
            'sum_price_purchase': float(answer[4]),
            'min_price_selling': float(answer[5]),
            'avg_price_selling': float(answer[6]),
            'max_price_selling': float(answer[7]),
            'sum_price_selling': float(answer[8]),
            'min_charges': float(answer[9]),
            'avg_charges': float(answer[10]),
            'max_charges': float(answer[11]),
            'sum_charges': float(answer[12]),
        }
        return result

    def get_orders_phones(
        self, status_type: StatusType = None, limit: int = 0, offset: int = 0
    ) -> list[(int, Order), (int, Phone)]:
        """RETURNS [(order_id, Order), (phone_id, Phone)]"""
        from database.orders.statuses_db import StatusesDB
        answer = self._fetchall(
            f"""WITH LatestStatuses AS (
                SELECT {PhonesDB.ID}, {PhonesDB.MODEL}, {PhonesDB.COLOR},
                {PhonesDB.MEMORY}, {PhonesDB.BATTERY_STATUS},
                {StatusesDB.ID}, {StatusesDB.STATUS_TYPE}, {StatusesDB.COMMENT}, {StatusesDB.DATE_TIME},
                {OrdersDB.ID}, {OrdersDB.PRICE_PURCHASE}, {OrdersDB.PRICE_SELLING}, {OrdersDB.CHARGES},
                ROW_NUMBER() OVER (PARTITION BY {OrdersDB.ID} ORDER BY {StatusesDB.DATE_TIME} DESC) AS rn
                FROM {OrdersDB.TABLE_NAME}
                JOIN {PhonesDB.TABLE_NAME} USING ({PhonesDB.ID})
                JOIN {StatusesDB.TABLE_NAME} USING ({OrdersDB.ID})
            )
            SELECT *
            FROM LatestStatuses
            WHERE rn = 1
            {f'AND {StatusesDB.STATUS_TYPE} = {DB.sql(status_type)}' if status_type else ''}
            ORDER BY {StatusesDB.DATE_TIME} DESC
            {f"LIMIT {limit} OFFSET {offset}" if limit else ''};"""
        )
        result = []
        if not answer:
            return result
        for line in answer:
            phone = Phone(line[1])
            phone.color = line[2]
            phone.memory = line[3]
            phone.battery_status = line[4]

            status = Status(StatusType(line[6]))
            status.comment = line[7]
            status.date_time = line[8]

            order = Order(status)
            order.price_purchase = line[10]
            order.price_selling = line[11]
            order.charges = line[12]
            order.status = status
            result.append(((int(line[9]), order), (int(line[0]), phone)))
        return result

    def get_order_phone(self, order_id: int) -> tuple[(int, Order), (int, Phone)]:
        """RETURNS ((order_id, Order), (phone_id, Phone))"""
        from database.orders.statuses_db import StatusesDB
        answer = self._fetchone(
            f"""SELECT {PhonesDB.ID}, {PhonesDB.MODEL}, {PhonesDB.COLOR}, {PhonesDB.MEMORY}, {PhonesDB.BATTERY_STATUS},
            {StatusesDB.ID}, {StatusesDB.STATUS_TYPE}, {StatusesDB.COMMENT}, MAX({StatusesDB.DATE_TIME}) AS max_date,
            {OrdersDB.ID}, {OrdersDB.PRICE_PURCHASE}, {OrdersDB.PRICE_SELLING}, {OrdersDB.CHARGES}
            FROM {OrdersDB.TABLE_NAME}
            JOIN {PhonesDB.TABLE_NAME} USING ({OrdersDB.PHONE_ID})
            JOIN {StatusesDB.TABLE_NAME} USING ({OrdersDB.ID})
            WHERE {OrdersDB.ID} = {DB.sql(order_id)};
            """
        )
        if not answer[0]:
            return None
        phone = Phone(answer[1])
        phone.color = answer[2]
        phone.memory = answer[3]
        phone.battery_status = answer[4]

        status = Status(StatusType(answer[6]))
        status.comment = answer[7]
        status.date_time = answer[8]

        order = Order(status)
        order.price_purchase = answer[10]
        order.price_selling = answer[11]
        order.charges = answer[12]
        order.status = status
        return ((int(answer[9]), order), (int(answer[0]), phone))