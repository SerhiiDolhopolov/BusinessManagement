from UI.language_resources import LanguageResources


__emoji = LanguageResources().emoji


def get_money() -> str:
    return __emoji.get('money')