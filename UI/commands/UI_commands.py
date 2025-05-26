from datetime import datetime

from UI.language_resources import LanguageResources
from UI.base import get_text
from models.status import StatusType
from database.users_db import Role
from bot import TIMEZONE, DATE_FORMAT_VISIBLE, CURRENCY, format_money


__commands = LanguageResources().commands
__role = __commands['role']
__role_exception = __role['exception']
__order = __commands['order']
__order_exception = __order['exception']
__backup = __commands['backup']


def get_ask_role() -> str:
    return get_text(__role, 'ask')


def get_select_role(username: str) -> str:
    return get_text(__role, 'select', username=username)


def get_change_role_message_for_admin(username: str, old_role: Role, role: Role) -> str:
    return get_text(__role, 'change_role_message_for_admin', username=username, old_role=old_role, role=role)


def get_change_role_message_for_other_admins(
    admin_username: str, username: str, old_role: Role, role: Role
) -> str:
    return get_text(__role, 'change_role_message_for_other_admins',
                    admin_username=admin_username,
                    username=username,
                    old_role=old_role,
                    role=role
                    )


def get_change_role_message_for_user(role: Role) -> str:
    return get_text(__role, 'change_role_message_for_user', role=role)


def get_role_exception_user_not_exist() -> str:
    return get_text(__role_exception, 'user_not_exist')


def get_role_exception_not_correct_id() -> str:
    return get_text(__role_exception, 'not_correct_id')


def get_ask_order() -> str:
    return get_text(__order, 'ask')


def get_order_exception_order_not_exist() -> str:
    return get_text(__order_exception, 'order_not_exist')


def get_order_exception_not_correct_id() -> str:
    return get_text(__order_exception, 'not_correct_id')


def get_backup_info(
    statuses_count: dict[StatusType, int],
    price_selling_sum: float,
    profit_money_sum: float,
    price_purchase_sum: float,
    charges_sum: float
) -> str:
    date = datetime.now(TIMEZONE).strftime(DATE_FORMAT_VISIBLE)
    statuses = (
        "<pre>"
        + "\n".join(
            [f'{status_type}: {count}' for status_type, count in statuses_count.items()]
        )
        + "</pre>"
    )
    profit = f"<code>{format_money(profit_money_sum)} {CURRENCY}</code>"
    earned = f"<code>{format_money(price_selling_sum)} {CURRENCY}</code>"
    spent_on_purchasing = f"<code>{format_money(price_purchase_sum)} {CURRENCY}</code>"
    spent_on_charges = f"<code>{format_money(charges_sum)} {CURRENCY}</code>"
    spent = f"<code>{format_money(price_purchase_sum + charges_sum)} {CURRENCY}</code>"

    return get_text(
        __backup, 'info',
        date=date,
        statuses=statuses,
        profit=profit,
        earned=earned,
        spent=spent,
        spent_on_purchasing=spent_on_purchasing,
        spent_on_charges=spent_on_charges
    )