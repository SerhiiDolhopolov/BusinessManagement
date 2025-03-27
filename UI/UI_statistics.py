from UI.language_resources import LanguageResources


__statistics = LanguageResources().statistics


def get_summary_statistic() -> str:
    return __statistics.get('summary_statistic')

def get_profit() -> str:
    return __statistics.get('profit')

def get_income() -> str:
    return __statistics.get('income')

def get_spent() -> str:
    return __statistics.get('spent')

def get_price_purchase() -> str:
    return __statistics.get('price_purchase')

def get_charges() -> str:
    return __statistics.get('charges')

def get_total_models() -> str:
    return __statistics.get('total_models')

def get_total_defects() -> str:
    return __statistics.get('total_defects')

def get_without_defect() -> str:
    return __statistics.get('without_defect')

def get_chart_profit_phones() -> str:
    return __statistics.get('chart_profit_phones')

def get_chart_profit_models() -> str:
    return __statistics.get('chart_profit_models')

def get_chart_profit_solved_defects() -> str:
    return __statistics.get('chart_profit_solved_defects')

def get_chart_profit_users() -> str:
    return __statistics.get('chart_profit_users')

def get_all_statistic() -> str:
    return __statistics.get('all_statistic')

def get_statistic_by_months() -> str:
    return __statistics.get('statistic_by_months')

def get_statistic_by_years() -> str:
    return __statistics.get('statistic_by_years')

def get_statistic_from() -> str:
    return __statistics.get('statistic_from')

def get_statistic_to() -> str:
    return __statistics.get('statistic_to')

def get_by_days() -> str:
    return __statistics.get('by_days')

def get_by_months() -> str:
    return __statistics.get('by_months')

def get_by_years() -> str:
    return __statistics.get('by_years')

def get_for_preview_week() -> str:
    return __statistics.get('for_preview_week')

def get_for_preview_month() -> str:
    return __statistics.get('for_preview_month')

def get_for_current_week() -> str:
    return __statistics.get('for_current_week')

def get_for_current_month() -> str:
    return __statistics.get('for_current_month')

def get_for_7_days() -> str:
    return __statistics.get('for_7_days')

def get_for_30_days() -> str:
    return __statistics.get('for_30_days')

def get_for_31_days() -> str:
    return __statistics.get('for_31_days')

def get_apply_filter() -> str:
    return __statistics.get('apply_filter')