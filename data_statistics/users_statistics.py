from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from bot import TEMP_PATH

from data_statistics.statistics import Statistics
from database.orders.statuses_db import StatusesDB, StatusType
from database.orders.orders_db import OrdersDB
from database.users_db import UsersDB


class UsersStatistics(Statistics):
    PATH_DIR = TEMP_PATH / Path('users_diagram')

    def __init__(self):
        df = self._read_sql(parse_dates=[StatusesDB.DATE_TIME])
        self._clear_dataframe(df)
        self._add_dates_from_date_time(df, 'date_time')
        data = self._get_grouped_data(df, ['date', 'username'])

        self.PATH_DIR.mkdir(exist_ok=True)
        fig = self._get_diagram(data)
        self._save_design(self.PATH_DIR / 'design.html', fig)
        self._save_layout(self.PATH_DIR / 'layout.json', fig)
        self._save_data(self.PATH_DIR / 'data.json', data)

    def _get_request(self) -> str:
        return f"""WITH LatestStatusess AS (
    SELECT {StatusesDB.ORDER_ID}, {StatusesDB.STATUS_TYPE},
    ROW_NUMBER() OVER (PARTITION BY {StatusesDB.ORDER_ID} ORDER BY {StatusesDB.DATE_TIME} DESC) AS latest_index 
    FROM {StatusesDB.TABLE_NAME}
    ),

    first_statuses_by_latest AS (
        SELECT {StatusesDB.ID}, s.{StatusesDB.STATUS_TYPE}, {StatusesDB.DATE_TIME},
        {OrdersDB.ID}, {OrdersDB.PRICE_PURCHASE}, {OrdersDB.PRICE_SELLING}, {OrdersDB.CHARGES},
        {UsersDB.ID}, {UsersDB.USERNAME},
        ROW_NUMBER() OVER (PARTITION BY {StatusesDB.ORDER_ID} ORDER BY {StatusesDB.DATE_TIME} ASC) AS first_index 
        FROM {StatusesDB.TABLE_NAME} s
        JOIN LatestStatusess ls USING ({StatusesDB.ORDER_ID})
        JOIN {OrdersDB.TABLE_NAME} USING ({OrdersDB.ID})
        JOIN {UsersDB.TABLE_NAME} USING ({UsersDB.ID})
        WHERE ls.latest_index = 1 AND ls.{StatusesDB.STATUS_TYPE} = '{StatusType.FINISHED}'
    )
    SELECT {OrdersDB.ID}, {OrdersDB.PRICE_PURCHASE}, {OrdersDB.PRICE_SELLING}, {OrdersDB.CHARGES}, 
    {StatusesDB.STATUS_TYPE}, {StatusesDB.DATE_TIME},
    {UsersDB.USERNAME}
    FROM first_statuses_by_latest
    WHERE first_index = 1 AND {StatusesDB.STATUS_TYPE} = '{StatusType.ON_THE_WAY}';
    """

    def _clear_dataframe(self, df: pd.DataFrame):
        self._drop_na(df, subset=['price_selling'])
        self._fill_na_0(df, 'price_purchase')
        self._fill_na_0(df, 'charges')

    def _get_grouped_data(
        self, df: pd.DataFrame, group_by: str, query: str = None
    ) -> pd.DataFrame:
        data = df.query(query) if query else df
        data = (
            data.groupby(group_by, as_index=False)
            .aggregate(
                price_selling_sum=('price_selling', 'sum'),
                price_purchase_sum=('price_purchase', 'sum'),
                charges_sum=('charges', 'sum'),
                orders_count=('order_id', 'nunique'),
            )
            .sort_values(group_by)
        )
        data['income_sum'] = (
            data.price_selling_sum - (data.price_purchase_sum + data.charges_sum)
        )
        return data

    def _get_figure(self):
        fig = make_subplots(
            rows=1,
            cols=2,
            specs=[[{'type': 'xy'}, {'type': 'domain'}]]
        )

        fig.update_layout(
            hovermode='x unified',
            plot_bgcolor='white',
            xaxis=dict(showspikes=False)
        )
        fig.update_xaxes(
            tickfont=dict(
                size=14,
            ),
            showline=True,
            linecolor='black'
        )
        return fig

    def _get_diagram(self, grouped_data: pd.DataFrame) -> go.Figure:
        return self._get_figure()