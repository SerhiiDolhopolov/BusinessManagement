from UI.language_resources import LanguageResources
from UI.base import get_text


__roles = LanguageResources().roles


def get_user() -> str:
    return get_text(__roles, 'user')


def get_courier() -> str:
    return get_text(__roles, 'courier')


def get_manager() -> str:
    return get_text(__roles, 'manager')


def get_admin() -> str:
    return get_text(__roles, 'admin')