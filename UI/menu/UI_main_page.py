from UI.language_resources import LanguageResources

from database.users_db import Role
from models.status import StatusManager, StatusType


__menu = LanguageResources().menu
__main_page = __menu['main_page']
__buttons = __main_page['buttons']


def get_info(role: Role) -> str:
    commands = []
    if role in (Role.ADMIN, Role.MANAGER):
        commands.append(__main_page['command_order'])
    if role is Role.ADMIN:
        commands.append(__main_page['command_role'])
    if role in (Role.ADMIN, Role.MANAGER):
        commands.append(__main_page['command_backup'])

    return (
        '\n'.join(commands)
        + '\n\n'
        + __main_page.get('additional_info')
    )


def get_my_phones_button() -> str:
    return __buttons.get('my_phones')


def get_add_button() -> str:
    return __buttons.get('add')


def get_available_button() -> str:
    return __buttons.get('available').format(
        emoji=StatusManager.get_emoji(StatusType.AVAILABLE)
    )


def get_phones_button() -> str:
    return __buttons.get('phones')


def get_need_spares_button() -> str:
    return __buttons.get('need_spares').format(
        emoji=StatusManager.get_emoji(StatusType.WAITING_FOR_SPARES)
    )


def get_need_repairs_button() -> str:
    return __buttons.get('need_repairs').format(
        emoji=StatusManager.get_emoji(StatusType.WAITING_FOR_REPAIRS)
    )


def get_users_button() -> str:
    return __buttons.get('users')


def get_couriers_button() -> str:
    return __buttons.get('couriers')


def get_managers_button() -> str:
    return __buttons.get('managers')


def get_admin_panel_button() -> str:
    return __buttons.get('admin_panel')


def get_statistics_button() -> str:
    return __buttons.get('statistics')