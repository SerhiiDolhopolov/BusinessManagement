import html

from bot import CURRENCY, MEMORY_DIMENSION, format_money

from UI.language_resources import LanguageResources
from UI.base import get_text, get_html_text
from database.users_db import Role, RoleManager
from models.phone import Phone
from models.order import Order


__menu = LanguageResources().menu
__add_page = __menu['add_page']


def get_select_model() -> str:
    return get_text(__add_page, 'select_model')


def get_select_color() -> str:
    return get_text(__add_page, 'select_color')


def get_select_memory() -> str:
    return get_text(__add_page, 'select_memory')


def get_ask_battery_status() -> str:
    return get_text(__add_page, 'ask_battery_status')


def get_select_defects(phone: Phone) -> str:
    model = f"<code>{phone.model}</code>"
    return get_html_text(__add_page, 'select_defect', model=model)


def get_continue_button() -> str:
    return get_text(__add_page, 'continue_button')


def get_ask_price_purchase() -> str:
    return get_text(__add_page, 'ask_price_purchase')


def get_ask_comment() -> str:
    return get_text(__add_page, 'ask_comment')


def get_confirm_button() -> str:
    return get_text(__add_page, 'confirm_button')


def get_confirm_message(order: Order, order_id: int, phone: Phone) -> str:
    order_id = f"<code>{order_id}</code>"
    title = (
        f"<code>{html.escape(f'{phone.model} {phone.memory}{MEMORY_DIMENSION} | {phone.color}')}</code>"
    )
    battery_status = f"<code>{phone.battery_status}%</code>"
    defects = (
        "-"
        if not phone.get_defects()
        else f"<pre>{html.escape(chr(10).join(f'- {defect}' for defect in phone.get_defects()))}</pre>"
    )
    price_purchase = f"<code>{format_money(order.price_purchase)} {CURRENCY}</code>"
    comment = (
        "-"
        if not order.status.comment
        else f"<pre>{html.escape(str(order.status.comment))}</pre>"
    )
    date_time = f"<code>{order.status.get_str_date_time()}</code>"
    return get_html_text(
        __add_page, 'confirm_message',
        order_id=order_id,
        title=title,
        battery_status=battery_status,
        defects=defects,
        price_purchase=price_purchase,
        comment=comment,
        date_time=date_time,
    )


def get_confirm_message_to_other_admin(
    user_username: str, user_role: Role, text: str
) -> str:
    emoji_user = RoleManager.get_emoji(user_role)
    return get_html_text(
        __add_page, 'confirm_message_to_other_admin',
        emoji_user=emoji_user, username=user_username, text=text
    )


def get_order_button(order_id: int) -> str:
    return get_text(__add_page, 'order_button', order_id=order_id)