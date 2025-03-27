from datetime import datetime
from bot import TIMEZONE

from database.database import DB
from database.orders.orders_db import OrdersDB
from database.phones.phones_db import PhonesDB
from database.phones.phones_defects_db import PhonesDefectsDB
from database.users_db import UsersDB


from models.status import Status, StatusType
from models.phone import Phone
from models.order import Order


class StatusesDB(DB):
    TABLE_NAME = 'statuses'

    ID = 'status_id'
    ORDER_ID = 'order_id'
    USER_ID = 'user_id'
    STATUS_TYPE = 'status_type'
    COMMENT = 'comment'
    DATE_TIME = 'date_time'

    def __init__(self):
        super().__init__()
        self._create_table(self.TABLE_NAME, self.get_columns(),
                    [f"FOREIGN KEY ({self.ORDER_ID}) REFERENCES {OrdersDB.TABLE_NAME} ({OrdersDB.ID})",
                    f"FOREIGN KEY ({self.USER_ID}) REFERENCES {UsersDB.TABLE_NAME} ({UsersDB.ID})"])

    def get_columns(self):
        return {
            self.ID: 'INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL',
            self.USER_ID: 'INTEGER NOT NULL',
            self.ORDER_ID: 'INTEGER NOT NULL',
            self.STATUS_TYPE: 'TEXT NOT NULL',
            self.COMMENT: 'TEXT',
            self.DATE_TIME: 'TEXT',
        }    

    def add_status(self, user_id: int, order_id: int, status: Status) -> int:
        return self._insert_data(self.TABLE_NAME, {
            self.USER_ID: user_id,
            self.ORDER_ID: order_id,
            self.STATUS_TYPE: status.status_type,
            self.COMMENT: status.comment,
            self.DATE_TIME: status.date_time,
        }).lastrowid

    def get_current_status_type(self, order_id: int) -> StatusType:
        answer = self._fetchone(f"""SELECT {self.STATUS_TYPE}, MAX({self.DATE_TIME})
                                FROM {self.TABLE_NAME}
                                WHERE {self.ORDER_ID} = {DB.sql(order_id)};""")
        return StatusType(answer[0]) if answer else None

    def get_count_orders_by_user(self, user_id: int) -> int:
        answer = self._fetchone(f"""SELECT COUNT(DISTINCT({StatusesDB.ORDER_ID}))
                                FROM {StatusesDB.TABLE_NAME}
                                WHERE {StatusesDB.USER_ID} = {DB.sql(user_id)};""")
        return answer[0] if answer[0] else 0

    def get_orders_by_user(self, user_id: int, limit: int = 0, offset: int = 0) -> list[(int, Order), (int, Phone)]:
        """RETURNS [(order_id, Order), (phone_id, Phone)], all orders, where was status for user"""
        answer = self._fetchall(f"""SELECT {PhonesDB.ID}, {PhonesDB.MODEL}, {PhonesDB.COLOR}, 
                       {PhonesDB.MEMORY}, {PhonesDB.BATTERY_STATUS}, 
                       {StatusesDB.ID}, {StatusesDB.STATUS_TYPE}, {StatusesDB.COMMENT}, MAX({StatusesDB.DATE_TIME}),
                       {OrdersDB.ID}, {OrdersDB.PRICE_PURCHASE}, {OrdersDB.PRICE_SELLING}, {OrdersDB.CHARGES}
                       FROM (
                           SELECT {StatusesDB.ORDER_ID}
                           FROM {StatusesDB.TABLE_NAME}
                           WHERE {StatusesDB.USER_ID} = {DB.sql(user_id)}
                           )
                        JOIN {StatusesDB.TABLE_NAME} USING ({StatusesDB.ORDER_ID})
                        JOIN {OrdersDB.TABLE_NAME} USING ({OrdersDB.ID})
                        JOIN {PhonesDB.TABLE_NAME} USING ({PhonesDB.ID})
                        GROUP BY {OrdersDB.ID}
                        ORDER BY {StatusesDB.DATE_TIME} DESC
                        {f"LIMIT {limit} OFFSET {offset}" if limit else ''};
                        """)
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
            result.append( ((int(line[9]), order), (int(line[0]), phone)))
        return result

    def get_count_orders_by_defect(self, status_type: StatusType, defect: str) -> int:
        """RETURNS COUNT of orders with current defect with selected status type"""
        answer = self._fetchone(f"""WITH LatestStatuses AS (
                                SELECT  {StatusesDB.ORDER_ID}, {StatusesDB.STATUS_TYPE},
                                ROW_NUMBER() OVER (PARTITION BY {StatusesDB.ORDER_ID} ORDER BY {StatusesDB.DATE_TIME} DESC) 
                                AS rn FROM {StatusesDB.TABLE_NAME}
                                )
                                SELECT COUNT({StatusesDB.ORDER_ID})
                                FROM LatestStatuses
                                JOIN {OrdersDB.TABLE_NAME} USING ({OrdersDB.ID})
                                JOIN {PhonesDefectsDB.TABLE_NAME} USING ({PhonesDefectsDB.PHONE_ID})
                                WHERE rn = 1 
                                AND {PhonesDefectsDB.defect} = {DB.sql(defect)} 
                                AND {StatusesDB.STATUS_TYPE} = {DB.sql(status_type)};
                                """)
        return answer[0] if answer[0] else 0

    def get_orders_by_defect(self, status_type: StatusType, defect: str, limit: int = 0, offset: int = 0) -> list[(int, Order), (int, Phone)]:
        """RETURNS [(order_id, Order), (phone_id, Phone)], all orders, where was current defect and status"""
        answer = self._fetchall(f"""WITH LatestStatuses AS (
                            SELECT {PhonesDB.ID}, {PhonesDB.MODEL}, {PhonesDB.COLOR},
                            {PhonesDB.MEMORY}, {PhonesDB.BATTERY_STATUS},
                            {StatusesDB.ID}, {StatusesDB.STATUS_TYPE}, {StatusesDB.COMMENT}, {StatusesDB.DATE_TIME},
                            {OrdersDB.ID}, {OrdersDB.PRICE_PURCHASE}, {OrdersDB.PRICE_SELLING}, {OrdersDB.CHARGES},
                            ROW_NUMBER() OVER (PARTITION BY {OrdersDB.ID} ORDER BY {StatusesDB.DATE_TIME} DESC) 
                            AS rn, {PhonesDefectsDB.defect}
                            FROM {OrdersDB.TABLE_NAME}
                            JOIN {PhonesDB.TABLE_NAME} USING ({PhonesDB.ID})
                            JOIN {PhonesDefectsDB.TABLE_NAME} USING ({PhonesDefectsDB.PHONE_ID})
                            JOIN {StatusesDB.TABLE_NAME} USING ({StatusesDB.ORDER_ID})
                            WHERE {PhonesDefectsDB.defect} = {DB.sql(defect)} 
                            )
                            SELECT *
                            FROM LatestStatuses
                            WHERE rn = 1
                            AND {StatusesDB.STATUS_TYPE} = {DB.sql(status_type)}
                            ORDER BY {StatusesDB.DATE_TIME} DESC
                            {f"LIMIT {limit} OFFSET {offset}" if limit else ''};
                            """)
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
            result.append( ((int(line[9]), order), (int(line[0]), phone)))
        return result

    def get_count_orders_with_current_status(self, status_type: StatusType = None) -> int:
        answer = self._fetchone(f"""WITH LatestStatusesS AS (
                            SELECT {self.STATUS_TYPE}, 
                            ROW_NUMBER() OVER (PARTITION BY {self.ORDER_ID} ORDER BY {self.DATE_TIME} DESC) as rn 
                            FROM {self.TABLE_NAME}
                            )

                            SELECT COUNT() 
                            FROM LatestStatusesS 
                            WHERE rn = 1 
                            {f'AND {self.STATUS_TYPE} = {DB.sql(status_type)}' if status_type else ''};""")
        return answer[0] if answer[0] else 0

    def get_count_defect_groups_orders(self, status_type: StatusType) -> int:
        """RETURNS COUNT of defect groups with selected status type"""
        answer = self._fetchone(f"""SELECT COUNT(DISTINCT {PhonesDefectsDB.defect}) FROM {OrdersDB.TABLE_NAME}
                            JOIN {PhonesDefectsDB.TABLE_NAME} USING ({PhonesDefectsDB.PHONE_ID})
                            JOIN (SELECT {StatusesDB.ORDER_ID}, {StatusesDB.STATUS_TYPE} 
                            FROM {StatusesDB.TABLE_NAME} GROUP BY {StatusesDB.ORDER_ID}) USING ({StatusesDB.ORDER_ID})
                            WHERE {StatusesDB.STATUS_TYPE} = {DB.sql(status_type)};
                            """)
        return answer[0] if answer[0] else 0

    def get_defect_groups_orders(self, status_type: StatusType, limit: int = 0, offset: int = 0) -> dict[str, int]:
        """RETURNS {defect, count} with selected status type"""
        answer = self._fetchall(f"""SELECT {PhonesDefectsDB.defect}, COUNT({OrdersDB.ID})
                            FROM {OrdersDB.TABLE_NAME}
                            JOIN {PhonesDefectsDB.TABLE_NAME} USING ({PhonesDefectsDB.PHONE_ID})
                            JOIN (SELECT {StatusesDB.ORDER_ID}, {StatusesDB.STATUS_TYPE}, MAX({StatusesDB.DATE_TIME}) as date 
                            FROM {StatusesDB.TABLE_NAME} GROUP BY {StatusesDB.ORDER_ID}) USING ({StatusesDB.ORDER_ID})
                            WHERE {StatusesDB.STATUS_TYPE} = {DB.sql(status_type)}
                            GROUP BY {PhonesDefectsDB.defect}
                            {f"LIMIT {limit} OFFSET {offset}" if limit else ''};""")
        result = dict()
        if not answer:
            return result
        return {line[0]: int(line[1]) for line in answer}

    def get_statuses_ascending(self, order_id: int) -> dict[int,(int, Status)]:
        """RETURNS {status_id:(user_id, Status)}"""
        answer = self._fetchall(f"""SELECT {self.ID}, {self.USER_ID}, {self.STATUS_TYPE}, {self.COMMENT}, {self.DATE_TIME}
                                FROM {self.TABLE_NAME}
                                WHERE {self.ORDER_ID} = {DB.sql(order_id)}
                                ORDER BY {self.DATE_TIME} ASC;""")
        statuses = {}
        for line in answer:
            status = Status(StatusType(line[2]))
            status.comment = line[3]
            status.date_time = line[4]
            statuses[int(line[0])] = (int(line[1]), status)
        return statuses

    def get_count_statuses_by_today(self) -> dict[str: int]:
        """RETURNS {status_type: count}"""
        date_time_now = self.get_date_time_now()
        answer = self._fetchall(f"""WITH LatestStatusess AS (
                            SELECT {OrdersDB.ID}, 
                            {StatusesDB.STATUS_TYPE}, {StatusesDB.DATE_TIME}, 
                            ROW_NUMBER() OVER (PARTITION BY {StatusesDB.ORDER_ID} ORDER BY {StatusesDB.DATE_TIME} DESC)
                            AS rn FROM {StatusesDB.TABLE_NAME}
                            JOIN {OrdersDB.TABLE_NAME} USING ({OrdersDB.ID})
                        )

                        SELECT {StatusesDB.STATUS_TYPE}, COUNT({StatusesDB.ORDER_ID})
                        FROM LatestStatusess 
                        WHERE rn = 1 
                        AND {StatusesDB.DATE_TIME} BETWEEN '{date_time_now} 00:00:00' AND '{date_time_now} 23:59:59'    
                        GROUP BY {StatusesDB.STATUS_TYPE};
                        """)
        return {line[0]: line[1] for line in answer} if answer else dict()

    def get_earned_money_by_today(self) -> tuple[float, float]:
        """RETURNS (price_selling_sum, profit_money_sum_for_statuses)"""
        date_time_now = self.get_date_time_now()
        answer = self._fetchone(f"""WITH LatestStatusess AS (
                    SELECT {OrdersDB.ID}, {OrdersDB.PRICE_PURCHASE}, {OrdersDB.PRICE_SELLING}, {OrdersDB.CHARGES},
                    {StatusesDB.STATUS_TYPE}, {StatusesDB.DATE_TIME}, 
                    ROW_NUMBER() OVER (PARTITION BY {StatusesDB.ORDER_ID} ORDER BY {StatusesDB.DATE_TIME} DESC)
                    AS rn FROM {StatusesDB.TABLE_NAME}
                    JOIN {OrdersDB.TABLE_NAME} USING ({OrdersDB.ID})
                    )

                    SELECT price_selling_sum, price_selling_sum - (price_purchase_sum + charges_sum) FROM (
                        SELECT SUM({OrdersDB.PRICE_SELLING}) as price_selling_sum, 
                            SUM({OrdersDB.PRICE_PURCHASE}) as price_purchase_sum, 
                            SUM({OrdersDB.CHARGES}) as charges_sum
                        FROM LatestStatusess 
                        WHERE rn = 1 
                        AND {StatusesDB.DATE_TIME} BETWEEN '{date_time_now} 00:00:00' AND '{date_time_now} 23:59:59' 
                        AND {StatusesDB.STATUS_TYPE} = {DB.sql(StatusType.FINISHED)}
                    );
                """)  
        return (answer[0], answer[1]) if answer[0] and answer[1] else [0, 0]

    def get_spent_money_by_today(self) -> tuple[float, float]:
        """RETURNS (price_purchase_sum, charges_sum)"""
        date_time_now = self.get_date_time_now()
        answer = self._fetchone(f"""WITH first_statuses AS (
                SELECT 
                {OrdersDB.PRICE_PURCHASE}, {OrdersDB.CHARGES},
                {StatusesDB.STATUS_TYPE}, {StatusesDB.DATE_TIME}, 
                ROW_NUMBER() OVER (PARTITION BY {StatusesDB.ORDER_ID} ORDER BY {StatusesDB.DATE_TIME} ASC) 
                AS rn FROM {StatusesDB.TABLE_NAME}
                JOIN {OrdersDB.TABLE_NAME} USING ({OrdersDB.ID})
            )

            SELECT SUM({OrdersDB.PRICE_PURCHASE}), SUM({OrdersDB.CHARGES})
            FROM first_statuses 
            WHERE rn = 1 
            AND {StatusesDB.DATE_TIME} BETWEEN '{date_time_now} 00:00:00' AND '{date_time_now} 23:59:59';    
        """)
        return (answer[0], answer[1]) if answer[0] and answer[1] else [0, 0]

    def get_date_time_now(self) -> datetime:
        date_time_now = datetime.now(TIMEZONE)
        return f'{"{:04d}".format(date_time_now.year)}-{"{:02d}".format(date_time_now.month)}-{"{:02d}".format(date_time_now.day)}'