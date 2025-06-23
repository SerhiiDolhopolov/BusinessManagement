from UI.language_resources import LanguageResources
from UI.base import get_text, get_html_text

from database.users_db import Role
from models.status import StatusManager, StatusType


__menu = LanguageResources().menu
__main_page = __menu['main_page']
__buttons = __main_page['buttons']


def get_info(role: Role) -> str:
    commands = []
    if role in (Role.ADMIN, Role.MANAGER):
        commands.append(get_text(__main_page, 'command_order'))
    if role is Role.ADMIN:
        commands.append(get_text(__main_page, 'command_role'))
    if role in (Role.ADMIN, Role.MANAGER):
        commands.append(get_text(__main_page, 'command_backup'))

    return (
        '\n'.join(commands)
        + '\n\n'
        + get_text(__main_page, 'additional_info')
    )


def get_my_phones_button() -> str:
    return get_html_text(__buttons, 'my_phones')


def get_add_button() -> str:
    return get_html_text(__buttons, 'add')


def get_available_button() -> str:
    return get_html_text(__buttons, 'available', emoji=StatusManager.get_emoji(StatusType.AVAILABLE))


def get_phones_button() -> str:
    return get_html_text(__buttons, 'phones')


def get_need_spares_button() -> str:
    return get_html_text(__buttons, 'need_spares', emoji=StatusManager.get_emoji(StatusType.WAITING_FOR_SPARES))


def get_need_repairs_button() -> str:
    return get_html_text(__buttons, 'need_repairs', emoji=StatusManager.get_emoji(StatusType.WAITING_FOR_REPAIRS))


def get_users_button() -> str:
    return get_html_text(__buttons, 'users')


def get_couriers_button() -> str:
    return get_html_text(__buttons, 'couriers')


def get_managers_button() -> str:
    return get_html_text(__buttons, 'managers')


def get_admin_panel_button() -> str:
    return get_html_text(__buttons, 'admin_panel')


def get_statistics_button() -> str:
    return get_html_text(__buttons, 'statistics')