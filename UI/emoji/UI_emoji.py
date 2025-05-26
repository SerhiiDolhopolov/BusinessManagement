from UI.language_resources import LanguageResources
from UI.base import get_text


__emoji = LanguageResources().emoji


def get_money() -> str:
    return get_text(__emoji, 'money')
