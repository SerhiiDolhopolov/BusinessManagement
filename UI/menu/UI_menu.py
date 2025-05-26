from UI.language_resources import LanguageResources
from UI_base import get_text


__menu = LanguageResources().menu


def get_welcome() -> str:
    return get_text(__menu, 'welcome')


def get_user_registration_select_role(username: str) -> str:
    return get_text(__menu, 'user_registration_select_role', username=username)


def get_chat_with_admin_button(username: str) -> str:
    return f"{get_text(__menu, 'chat_with_admin_button')} {username}"