from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from bot import TEMP_PATH

from UI import UI_statistics

from data_statistics.statistics import Statistics
from database.phones.phones_db import PhonesDB
from database.orders.statuses_db import StatusesDB, StatusType
from database.orders.orders_db import OrdersDB


class IncomeStatistics(Statistics):
    PATH_DIR = TEMP_PATH / Path('income_diagram')

    def __init__(self):
        df = self._read_sql(parse_dates=[StatusesDB.DATE_TIME])
        self._clear_dataframe(df)
        self._add_dates_from_date_time(df, 'date_time')

        self.PATH_DIR.mkdir(exist_ok=True)

        data_by_dates = self._get_grouped_data(df, ['date'])
        fig = self._get_diagram(data_by_dates)
        self._save_design(self.PATH_DIR / 'design.html', fig)
        self._save_figure(self.PATH_DIR / 'figure_by_dates.json', fig)

        data_by_months = self._get_grouped_data(df, ['year', 'month'])
        data_by_months = data_by_months.reset_index()
        data_by_months['year_month'] = data_by_months['year'].astype(str) + " " + pd.to_datetime(data_by_months['month'], format='%m').dt.strftime('%b')
        data_by_months.set_index('year_month', inplace=True)
        fig = self._get_diagram(data_by_months)
        self._save_figure(self.PATH_DIR / 'figure_by_months.json', fig)

        data_by_years = self._get_grouped_data(df, ['year'])
        fig = self._get_diagram(data_by_years)
        self._save_figure(self.PATH_DIR / 'figure_by_years.json', fig)


    def _get_request(self) -> str:
        return f"""WITH LatestStatusess AS (
    SELECT {PhonesDB.ID}, {PhonesDB.MODEL},
    {OrdersDB.ID}, {OrdersDB.PRICE_PURCHASE}, {OrdersDB.PRICE_SELLING}, {OrdersDB.CHARGES},
    {StatusesDB.STATUS_TYPE}, {StatusesDB.DATE_TIME}, 
    ROW_NUMBER() OVER (PARTITION BY {StatusesDB.ORDER_ID} ORDER BY {StatusesDB.DATE_TIME} DESC) AS rn FROM {StatusesDB.TABLE_NAME}
    JOIN {OrdersDB.TABLE_NAME} USING ({OrdersDB.ID})
    JOIN {PhonesDB.TABLE_NAME} USING ({PhonesDB.ID})
    )

    SELECT {OrdersDB.ID}, {OrdersDB.PRICE_PURCHASE}, {OrdersDB.PRICE_SELLING}, {OrdersDB.CHARGES}, 
    {PhonesDB.MODEL},
    {StatusesDB.STATUS_TYPE}, {StatusesDB.DATE_TIME}
    FROM LatestStatusess
    WHERE rn = 1 and {StatusesDB.STATUS_TYPE} = '{StatusType.FINISHED}';
    """

    def _clear_dataframe(self, df: pd.DataFrame):
        self._drop_na(df, subset=['price_selling'])
        self._fill_na_0(df, 'price_purchase')
        self._fill_na_0(df, 'charges')

    def _get_grouped_data(self, df: pd.DataFrame, group_by: str, query: str = None) -> pd.DataFrame:
        data = df.query(query) if query else df
        data = data \
            .groupby(group_by, as_index=True) \
            .aggregate(price_selling_sum=('price_selling', 'sum'), 
                price_purchase_sum=('price_purchase', 'sum'),
                charges_sum=('charges', 'sum')
                       ) \
            .sort_values(group_by)
        data['income_sum'] = data.price_selling_sum - (data.price_purchase_sum + data.charges_sum)
        return data

    def _get_figure(self):
        fig = go.Figure()
        fig.update_layout(hovermode='x unified', plot_bgcolor='white')
        fig.update_xaxes(
            tickfont=dict(
                size=14,
            ),
            showline=True,
            linecolor='black',
            gridcolor='lightgrey'
        )
        fig.update_yaxes(
            showline=True,
            linecolor='black',
            gridcolor='lightgrey'
        )
        return fig

    def _fill_diagram(self, fig: go.Figure, grouped_data: pd.DataFrame) -> go.Figure:
        currency = self.CURRENCY
        x = grouped_data.index
        price_selling_sum = grouped_data.price_selling_sum
        price_purchase_sum = grouped_data.price_purchase_sum
        charges_sum = grouped_data.charges_sum
        income_sum = grouped_data.income_sum

        fig.add_trace(go.Scatter(
            x=x, 
            y=price_selling_sum, 
            name=UI_statistics.get_income(), 
            line=dict(color='blue'),
            mode='lines+markers',
            hovertemplate=f'<span style="color:green;">%{{y:,.2f}} {currency}</span><br><br>',
            visible='legendonly'
        ))

        fig.add_trace(go.Scatter(
            x=x, 
            y=(price_purchase_sum + charges_sum), 
            name=UI_statistics.get_spent(), 
            line=dict(color='red'),
            mode='lines+markers',
            hovertemplate=f'<span style="color:red;">%{{y:,.2f}} {currency} (%{{customdata[0]:.2f}}%)</span>' + 
            f'<br>{UI_statistics.get_price_purchase()}: <span style="color:red;">%{{customdata[1]:,.2f}} {currency} (%{{customdata[2]:.2f}}%)</span>' + 
            f'<br>{UI_statistics.get_charges()}: <span style="color:red;">%{{customdata[3]:,.2f}} {currency} (%{{customdata[4]:.2f}}%)</span>',
            customdata=[( 
                        (price_purchase + charge) / price_selling * 100, 
                        price_purchase, price_purchase / price_selling * 100, 
                        charge, charge / price_selling * 100
                        ) 
                        for price_selling, price_purchase, charge
                        in zip(price_selling_sum, price_purchase_sum, charges_sum)],
            visible='legendonly'
        ))

        fig.add_trace(go.Scatter(
            x=x,
            y=income_sum,
            name=UI_statistics.get_profit(),
            line=dict(color='green'),
            mode='lines+markers',
            hovertemplate=f'<span style="color:%{{customdata[1]}};">%{{customdata[2]}}%{{y:,.2f}} {currency} (%{{customdata[0]:.2f}}%)</span>',
            customdata=[(income / price_selling * 100, 
                        'green' if income >= 0 else 'red', 
                        '+' if income >= 0 else '') 
                        for price_selling, income 
                        in zip(price_selling_sum, income_sum)]
        ))

    def _get_diagram(self, grouped_data: pd.DataFrame) -> go.Figure:
        fig = self._get_figure()
        self._fill_diagram(fig, grouped_data)
        return fig