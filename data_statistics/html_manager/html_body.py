from data_statistics.income_statistics import IncomeStatistics
from data_statistics.models_statistics import ModelsStatistics
from data_statistics.defects_statistics import DeffectsStaticts
from data_statistics.users_statistics import UsersStatistics

from UI import UI_statistics


def get_html_body() -> str:
    income_path_dir = IncomeStatistics.PATH_DIR
    income_diagram_design = ''
    with open(income_path_dir / 'design.html', 'r') as file:
        income_diagram_design = file.read()

    models_path_dir = ModelsStatistics.PATH_DIR
    models_diagram_design = ''
    with open(models_path_dir / 'design.html', 'r') as file:
        models_diagram_design = file.read()

    defects_path_dir = DeffectsStaticts.PATH_DIR
    defects_diagram_design = ''
    with open(defects_path_dir / 'design.html', 'r') as file:
        defects_diagram_design = file.read()

    users_path_dir = UsersStatistics.PATH_DIR
    users_diagram_design = ''
    with open(users_path_dir / 'design.html', 'r') as file:
        users_diagram_design = file.read()

    return f"""
    <h2>{UI_statistics.get_summary_statistic()}</h1>
    <div style="display: flex; flex-direction: column; align-items: center;">
        <table style="width:80%">
          <tr>
            <th style="width:5%"></th>
            <th>{UI_statistics.get_profit()}</th>
            <th>{UI_statistics.get_income()}</th>
            <th>{UI_statistics.get_spent()}</th> 
          </tr>
          <tr>
            <td>MIN</td>
            <td id="income-min">0</td>
            <td id="purchase-min">0</td>
            <td id="was-spent-min">0</td>
          </tr>
          <tr>
            <td>AVG</td>
            <td id="income-avg">0</td>
            <td id="purchase-avg">0</td>
            <td id="was-spent-avg">0</td>
          </tr>
          <tr>
            <td>MAX</td>
            <td id="income-max">0</td>
            <td id="purchase-max">0</td>
            <td id="was-spent-max">0</td>
          </tr>
          <tr>
            <td>SUM</td>
            <td id="income-sum">0</td>
            <td id="purchase-sum">0</td>
            <td id="was-spent-sum">0</td>
          </tr>
        </table>
    </div>
    <h2 id="diagram-info">{UI_statistics.get_chart_profit_phones()}</h1>
    <div id="income-diagram" style="display: block;">{income_diagram_design}</div>
    <h2 id="diagram-info">{UI_statistics.get_chart_profit_models()}</h1>
    <div id="models-diagram" style="display: block;>{models_diagram_design}</div>
    <h2 id="diagram-info">{UI_statistics.get_chart_profit_solved_defects()}</h1>
    <div id="defects-diagram" style="display: block;>{defects_diagram_design}</div>
    <h2 id="diagram-info">{UI_statistics.get_chart_profit_users()}</h1>
    <div id="users-diagram" style="display: block;">{users_diagram_design}</div>
"""