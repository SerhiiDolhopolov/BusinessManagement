import sqlite3
from abc import ABC, abstractmethod
from bot import CURRENCY

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio

from database.database import DB

from UI import UI_statistics


class Statistics(ABC):
    CURRENCY = CURRENCY

    @abstractmethod
    def __init__(self):
        """
            ___init___ with an instruction how to create and save a diagram.  
        """ 
        raise NotImplementedError('Implement __init__() method with an instruction how to create and save a diagram.')  

    def _save_figure(self, path: str, fig: go.Figure):
        figure_json = pio.to_json(fig)
        with open(path, 'w') as file:
            file.write(figure_json)

    def _save_design(self, path: str, fig: go.Figure):
        design = pio.to_html(fig, full_html=False)    
        with open(path, 'w') as file:
            file.write(design)

    def _save_data(self, path: str, data: pd.DataFrame):
        data.to_json(path, orient='records')

    def _save_layout(self, path: str, fig: go.Figure):
        layout = pio.to_json(fig.layout)
        with open(path, 'w') as file:
            file.write(layout)

    @abstractmethod
    def _get_request(self) -> str:
        """
        Returns:
            str: sql_request
        """
        raise NotImplementedError('Implement _get_request() method with return str')

    def _read_sql(self, parse_dates: list[str]) -> pd.DataFrame:
        print(self._get_request())
        with sqlite3.connect(DB.DB_NAME) as connection:
            return pd.read_sql(self._get_request(), connection, parse_dates=parse_dates)

    @abstractmethod
    def _clear_dataframe(self, df: pd.DataFrame):
        """
            Clear dataframe
        """
        raise NotImplementedError('Implement _clear_datafrane(df) method with return None')

    def _drop_duplicates(self, df: pd.DataFrame, subset: list[str]):
        df.drop_duplicates(subset=subset, inplace=True)

    def _drop_na(self, df: pd.DataFrame, subset: list[str]):
        df.dropna(subset=subset, inplace=True)

    def _fill_na_0(self, df: pd.DataFrame, column: str):
        df[column] = df[column].fillna(0)

    def _fill_na_defect(self, df: pd.DataFrame):
        df['defect'] = df.defect.fillna(UI_statistics.get_without_defect())

    def _add_dates_from_date_time(self, df: pd.DataFrame, date_time_column: str):
        """
            Create 'date', 'year', 'month' columns from date_time column
        """
        df['date'] = pd.to_datetime(df[date_time_column].dt.date)
        df['year'] = df[date_time_column].dt.year
        df['month'] = df[date_time_column].dt.month

    @abstractmethod
    def _get_grouped_data(self, df: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError('Implement _get_groped_data(df) method with return pandas.DataFrame')

    @abstractmethod
    def _get_figure(self) -> go.Figure:
        raise NotImplementedError('Implement _get_figure() method with return go.Figure')

    @abstractmethod
    def _get_diagram(self, groped_data: pd.DataFrame) -> go.Figure:
        raise NotImplementedError('Implement _get_diagram(grouped_data) method with return go.Figure')

    def _add_trace_color(self, groped_data: pd.DataFrame, column: str):
        trace_colors = {key: color for key, color in zip(groped_data[column].unique(), px.colors.qualitative.Plotly)}
        groped_data['trace_color'] = groped_data[column].map(trace_colors)