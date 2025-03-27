import json

from data_statistics.javascript_manager.base_functions import *
from data_statistics.javascript_manager.show_diagrams import *
from data_statistics.javascript_manager.show_income_diagrams import *
from data_statistics.javascript_manager.show_defects_diagrams import *
from data_statistics.javascript_manager.show_models_diagrams import *
from data_statistics.javascript_manager.show_users_diagram import *

from data_statistics.html_manager.html_header import get_html_header
from data_statistics.html_manager.html_body import get_html_body

from data_statistics.income_statistics import IncomeStatistics
from data_statistics.models_statistics import ModelsStatistics
from data_statistics.defects_statistics import DeffectsStaticts
from data_statistics.users_statistics import UsersStatistics


def get_html_template(currency: str) -> str:
    income_path_dir = IncomeStatistics.PATH_DIR
    income_diagram_figure_by_dates = ''
    income_diagram_figure_by_months = ''
    income_diagram_figure_by_years = ''
    with open(income_path_dir / 'figure_by_dates.json', 'r') as file:
        income_diagram_figure_by_dates = file.read()
    with open(income_path_dir / 'figure_by_months.json', 'r') as file:
        income_diagram_figure_by_months = file.read()
    with open(income_path_dir / 'figure_by_years.json', 'r') as file:
        income_diagram_figure_by_years = file.read()

    models_path_dir = ModelsStatistics.PATH_DIR
    models_diagram_layout = ''
    models_diagram_data = ''
    with open(models_path_dir / 'layout.json', 'r') as file:
        models_diagram_layout = file.read()
    with open(models_path_dir / 'data.json', 'r') as file:
        models_diagram_data = json.load(file)

    defects_path_dir = DeffectsStaticts.PATH_DIR
    defects_diagram_layout = ''
    defects_diagram_data = ''
    with open(defects_path_dir / 'layout.json', 'r') as file:
        defects_diagram_layout = file.read()
    with open(defects_path_dir / 'data.json', 'r') as file:
        defects_diagram_data = json.load(file)

    users_path_dir = UsersStatistics.PATH_DIR
    users_diagram_layout = ''
    users_diagram_data = ''
    with open(users_path_dir / 'layout.json', 'r') as file:
        users_diagram_layout = file.read()
    with open(users_path_dir / 'data.json', 'r') as file:
        users_diagram_data = json.load(file)

    return f"""<!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="viewport" content='width=1000' />

        <style>
            body{{
                font-family: Arial, sans-serif;
                padding: 0px;
                margin: 0px;
                min-width: 1000px;
            }}

            .navbar {{
                width: 100%;
                background-color: #333;
                color: white;
                transition: all 0.3s ease;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.5);
                justify-content: center;
                display: flex;

            }}

            .container {{
                display: flex;
                justify-content: space-between;
                align-items: center;
            }}

            .menu {{
                list-style: none;
                display: flex;
                justify-content: space-between;
                padding: 0px 0px 0px 0px;
            }}

            .filter-block{{
                display: flex;
                padding: 0.4em 1em;
                justify-content: center;
                border-right: 5px solid white;
                border-left: 5px solid white; 
            }}

            .filter-block:last-child {{
            border-left: none;
            }}

            .filter-block:first-child {{
            border-right: none;
            }}

            .menu li {{
                display: flex;
                justify-content: center;
                align-items: center;
            }}

            button {{
            background-color: #333333;
            border: 1px solid white;
            color: white;
            text-align: center;
            text-decoration: none;
            font-size: 14px;
            transition-duration: 0.4s;
            cursor: pointer;
            }}

            button:hover {{
                background-color: #3d3d3d;
            }}

            input{{
                background-color: #333333;
                border: 1px solid white;
                border-radius: 5px;
                color: white;
                padding: 2em 1em;
                text-align: center;
                font-size: 18px;
                margin: 1em 0.5em;
                opacity: 1;
                transition: 0.3s;
                display: inline-block;
                text-decoration: none;
            }}

            ::placeholder {{
            color: white;
            opacity: 0.6;
            }}

            table, th, td {{
            border: 1px solid black;
            border-collapse: collapse;
            text-align: center;
            padding: 15px;
            }}

            h1, h2{{
                text-align: center;
            }}

            @media (orientation: landscape) {{
                .navbar {{
                    height: 7em;
                }}

                .menu {{
                    flex-direction: row;
                    padding: 0px 0px 0px 0px;
                }}

                .filter-block {{
                    flex-direction: row;
                    gap: 2em;
                }}

                button {{
                    padding: 0.5em 1.5em;
                    margin: 0.3em 0.3em;
                }}

                input {{
                    padding: 1em 0.5em;
                }}

            }}

            @media (max-width: 1600px) {{
                button {{
                    font-size: 12px;
                }}
                input {{
                    font-size: 14px;
                }}
            }}

            @media (max-width: 1250px) {{
                button {{
                    font-size: 10px;
                }}
                input {{
                    font-size: 12px;
                }}
            }}

            @media (max-width: 1050px) {{
                .navbar {{
                    height: auto;
                }}
                .menu {{
                    flex-direction: column;
                    justify-content: center;
                    padding: 0px 0px 0px 0px;
                }}
                .filter-block {{
                    flex-direction: column;
                    gap: 1em;
                    padding: 0em 0em;
                }}
                .filter-block:last-child {{
                border-left: 5px solid white;
                }}

                .filter-block:first-child {{
                border-right: 5px solid white;
                }}
                button {{
                    font-size: 12px;
                    padding: 0.75em 1.5em;
                    margin: 0.2em 0.2em;
                }}
                input {{
                    font-size: 14px;
                    padding: 1em;
                }}
            }}

            @media (max-width: 480px) {{
                button {{
                    font-size: 10px;
                    padding: 0.5em 1em;
                }}
                input {{
                    font-size: 10px;
                    padding: 0.3em;
                }}
            }}
        </style>

        <script>
            {get_func_date_to_str()}
            {get_func_get_count_days_in_month()}
            {get_func_set_info_text()}

            {get_func_show_diagrams_by_dates_filter()}
            {get_func_show_diagrams_by_dates()}
            {get_func_show_diagrams_by_months()}
            {get_func_show_diagrams_by_years()}

            {get_func_show_diagrams_to_next_x_days()}
            {get_func_show_diagrams_by_x_days(7)}
            {get_func_show_diagrams_by_x_days(30)}
            {get_func_show_diagrams_by_x_days(31)}

            {get_func_show_diagrams_from_monday_to_next_week()}
            {get_func_show_diagrams_by_x_week('Current')}
            {get_func_show_diagrams_by_x_week('Previous', -1)}

            {get_func_show_diagrams_from_first_day_to_next_month()}
            {get_func_show_diagrams_by_x_month('Current')}
            {get_func_show_diagrams_by_x_month('Previous', -1)}

            {get_func_get_income_diagram_figure_by_dates(income_diagram_figure_by_dates)}
            {get_func_show_income_diagram_by_dates_filter()}
            {get_func_show_income_diagram_by_dates()}
            {get_func_show_income_diagram_by_months(income_diagram_figure_by_months)}
            {get_func_show_income_diagram_by_years(income_diagram_figure_by_years)}
            {get_func_show_income_diagram(currency)}

            {get_func_get_models_diagram_data(models_diagram_data)}
            {get_func_show_models_diagram_by_dates_filter()}
            {get_func_show_models_diagram_by_dates()}
            {get_func_show_models_diagram(models_diagram_layout, currency)} 

            {get_func_get_defects_diagram_data(defects_diagram_data)}
            {get_func_show_defects_diagram_by_dates_filter()}
            {get_func_show_defects_diagram_by_dates()}
            {get_func_show_defects_diagram(defects_diagram_layout, currency)}     

            {get_func_get_users_diagram_data(users_diagram_data)}
            {get_func_show_users_diagram_by_dates_filter()}
            {get_func_show_users_diagram_by_dates()}
            {get_func_show_users_diagram(users_diagram_layout, currency)}   

            window.onload = function() 
            {{
                showDiagramsByDates();
            }};
        </script>
    </head>
    <body>
        {get_html_header()}
        {get_html_body()}
    </body>
    </html>"""