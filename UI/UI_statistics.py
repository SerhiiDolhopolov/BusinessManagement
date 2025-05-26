from UI.language_resources import LanguageResources
from UI.base import get_text


__statistics = LanguageResources().statistics


def get_summary_statistic() -> str:
    return get_text(__statistics, 'summary_statistic')


def get_profit() -> str:
    return get_text(__statistics, 'profit')


def get_income() -> str:
    return get_text(__statistics, 'income')


def get_spent() -> str:
    return get_text(__statistics, 'spent')


def get_price_purchase() -> str:
    return get_text(__statistics, 'price_purchase')


def get_charges() -> str:
    return get_text(__statistics, 'charges')


def get_total_models() -> str:
    return get_text(__statistics, 'total_models')


def get_total_defects() -> str:
    return get_text(__statistics, 'total_defects')


def get_without_defect() -> str:
    return get_text(__statistics, 'without_defect')


def get_chart_profit_phones() -> str:
    return get_text(__statistics, 'chart_profit_phones')


def get_chart_profit_models() -> str:
    return get_text(__statistics, 'chart_profit_models')


def get_chart_profit_solved_defects() -> str:
    return get_text(__statistics, 'chart_profit_solved_defects')


def get_chart_profit_users() -> str:
    return get_text(__statistics, 'chart_profit_users')


def get_all_statistic() -> str:
    return get_text(__statistics, 'all_statistic')


def get_statistic_by_months() -> str:
    return get_text(__statistics, 'statistic_by_months')


def get_statistic_by_years() -> str:
    return get_text(__statistics, 'statistic_by_years')


def get_statistic_from() -> str:
    return get_text(__statistics, 'statistic_from')


def get_statistic_to() -> str:
    return get_text(__statistics, 'statistic_to')


def get_by_days() -> str:
    return get_text(__statistics, 'by_days')


def get_by_months() -> str:
    return get_text(__statistics, 'by_months')


def get_by_years() -> str:
    return get_text(__statistics, 'by_years')


def get_for_preview_week() -> str:
    return get_text(__statistics, 'for_preview_week')


def get_for_preview_month() -> str:
    return get_text(__statistics, 'for_preview_month')


def get_for_current_week() -> str:
    return get_text(__statistics, 'for_current_week')


def get_for_current_month() -> str:
    return get_text(__statistics, 'for_current_month')


def get_for_7_days() -> str:
    return get_text(__statistics, 'for_7_days')


def get_for_30_days() -> str:
    return get_text(__statistics, 'for_30_days')


def get_for_31_days() -> str:
    return get_text(__statistics, 'for_31_days')


def get_apply_filter() -> str:
    return get_text(__statistics, 'apply_filter')