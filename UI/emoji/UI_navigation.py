from UI.language_resources import LanguageResources
from UI.base import get_text


__emoji = LanguageResources().emoji
__navigation = __emoji['navigation']


def get_back_button() -> str:
    return __navigation.get('back')


def get_preview_page_button() -> str:
    return __navigation.get('preview_page')


def get_current_page_button(page: int) -> str:
    return __navigation.get('current_page').format(page=page)


def get_next_page_button() -> str:
    return __navigation.get('next_page')