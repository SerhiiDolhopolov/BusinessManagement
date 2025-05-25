import html

from UI.language_resources import LanguageResources
from database.users_db import Role, RoleManager

__menu = LanguageResources().menu
__users_page = __menu['users_page']


def get_users_text(users: list[int, str, Role, bool]) -> str:
    return __users_page.get('users').format(users=__get_users_format_text(users))


def get_couriers_text(users: list[int, str, Role, bool]) -> str:
    return __users_page.get('couriers').format(users=__get_users_format_text(users))


def get_managers_text(users: list[int, str, Role, bool]) -> str:
    return __users_page.get('managers').format(users=__get_users_format_text(users))


def __get_users_format_text(users: list[int, str, Role, bool]) -> str:
    return '\n'.join(
        [
            f"{RoleManager.get_emoji(role)}<code>{html.escape(str(user_id))}</code>: @{user_username}"
            for (user_id, user_username, role) in users
        ]
    )