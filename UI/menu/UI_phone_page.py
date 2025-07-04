import html

from database.users_db import Role, RoleManager

from models.status import StatusManager, StatusType, Status
from models.order import Order
from models.phone import Phone

from UI.language_resources import LanguageResources
from UI.base import get_text, get_html_text
from bot import MEMORY_DIMENSION, CURRENCY, format_money


__menu = LanguageResources().menu
__phone_page = __menu['phone_page']
__buttons = __phone_page['buttons']
__change_price_purchase = __phone_page['change_price_purchase']
__change_charges = __phone_page['change_charges']
__change_price_selling = __phone_page['change_price_selling']
__change_memory = __phone_page['change_memory']
__change_battery_status = __phone_page['change_battery_status']
__change_defects = __phone_page['change_defects']
__change_status = __phone_page['change_status']
__solve_defect = __phone_page['solve_defect']


def get_info(order: Order, order_id: int, phone: Phone, role: Role) -> str:
    status_emoji = StatusManager.get_emoji(order.status.status_type)
    title = (
        f"<code>{html.escape(phone.model)} {phone.memory}{MEMORY_DIMENSION} | "
        f"{html.escape(phone.color)}</code>"
    )
    title = get_html_text(__phone_page, 'title', status_emoji=status_emoji, title=title)

    battery_status = f"<code>{phone.battery_status}%</code>"
    battery_status = get_html_text(__phone_page, 'battery_status', battery_status=battery_status)

    price_purchase = f"<code>{format_money(order.price_purchase)} {CURRENCY}</code>"
    price_purchase = get_html_text(__phone_page, 'price_purchase', price_purchase=price_purchase)

    charges = f"<code>{format_money(order.charges)} {CURRENCY}</code>"
    charges = get_html_text(__phone_page, 'charges', charges=charges)

    price_selling = f"<code>{format_money(order.price_selling)} {CURRENCY}</code>"
    price_selling = get_html_text(__phone_page, 'price_selling', price_selling=price_selling)

    ps = float(order.price_selling if order.price_selling else 0)
    pp = float(order.price_purchase if order.price_purchase else 0)
    ch = float(order.charges if order.charges else 0)
    profit_count = ps - pp - ch

    profit = f"<code>{format_money(profit_count)} {CURRENCY}</code>"
    profit = get_html_text(__phone_page, 'profit', profit=profit)

    defects = (
        "-"
        if not phone.get_defects()
        else f"<pre>{html.escape(chr(10).join(f'- {defect}' for defect in phone.get_defects()))}</pre>"
    )
    defects = get_html_text(__phone_page, 'defects', defects=defects)

    comment = (
        "-"
        if not order.status.comment
        else f"<pre>{html.escape(str(order.status.comment))}</pre>"
    )
    comment = get_html_text(__phone_page, 'comment', comment=comment)

    date_time = f"<code>{html.escape(str(order.status.get_str_date_time()))}</code>"
    date_time = get_html_text(__phone_page, 'date_time', date_time=date_time)

    order = f"<code>{html.escape(str(order_id))}</code>"
    order = get_html_text(__phone_page, 'order', order=order)

    return (
        title + '\n\n'
        + battery_status + '\n'
        + (price_purchase + '\n' + charges + '\n' if role in (Role.ADMIN, Role.MANAGER) else '')
        + price_selling + '\n'
        + (profit + '\n\n' if role in (Role.ADMIN, Role.MANAGER) else '')
        + defects + '\n\n'
        + comment + '\n\n'
        + date_time + '\n'
        + order
    )

def get_confirm_message_to_other_admin(user_username: str, user_role: Role, order_id: int, text: str) -> str:
    emoji_user = RoleManager.get_emoji(user_role)
    order_id = f"<code>{order_id}</code>"
    return get_html_text(__phone_page, 'confirm_message_to_other_admin', emoji_user=emoji_user, username=user_username,
                                                                     order_id=order_id, text=text)

def get_order_button(order_id: int) -> str:
    return get_html_text(__phone_page, 'order_button', order_id=order_id)

def get_change_price_purchase_button() -> str:
    return get_html_text(__buttons, 'change_price_purchase')

def get_change_charges_button() -> str:
    return get_html_text(__buttons, 'change_charges')

def get_change_price_selling_button() -> str:
    return get_html_text(__buttons, 'change_price_selling')

def get_change_memory_button() -> str:
    return get_html_text(__buttons, 'change_memory')

def get_change_battery_button() -> str:
    return get_html_text(__buttons, 'change_battery')

def get_change_defects_button() -> str:
    return get_html_text(__buttons, 'change_defects')

def get_change_status_button() -> str:
    return get_html_text(__buttons, 'change_status')

def get_solve_defect_button() -> str:
    return get_html_text(__buttons, 'solve_defect')

def get_history_button() -> str:
    return get_html_text(__buttons, 'history')

def get_ask_change_price_purchase(current_price_purchase: float) -> str:
    value = f"<code>{format_money(current_price_purchase)} {CURRENCY}</code>"
    return get_text(__change_price_purchase, 'ask', value=value)

def get_confirm_change_price_purchase(price_purchase_from: float, price_purchase_to: float) -> str:
    value_from = f"<code>{format_money(price_purchase_from)} {CURRENCY}</code>"
    value_to = f"<code>{format_money(price_purchase_to)} {CURRENCY}</code>"
    return get_text(__change_price_purchase, 'confirm', value_from=value_from, value_to=value_to)

def get_ask_change_charges(current_charges: float) -> str:
    value = f"<code>{format_money(current_charges)} {CURRENCY}</code>"
    return get_text(__change_charges, 'ask', value=value)

def get_confirm_change_charges(charges_from: float, charges_to: float) -> str:
    value_from = f"<code>{format_money(charges_from)} {CURRENCY}</code>"
    value_to = f"<code>{format_money(charges_to)} {CURRENCY}</code>"
    return get_text(__change_charges, 'confirm', value_from=value_from, value_to=value_to)

def get_ask_change_price_selling(current_price_selling: float) -> str:
    value = f"<code>{format_money(current_price_selling)} {CURRENCY}</code>"
    return get_text(__change_price_selling, 'ask', value=value)

def get_confirm_change_price_selling(price_selling_from: float, price_selling_to: float) -> str:
    value_from = f"<code>{format_money(price_selling_from)} {CURRENCY}</code>"
    value_to = f"<code>{format_money(price_selling_to)} {CURRENCY}</code>"
    return get_text(__change_price_selling, 'confirm', value_from=value_from, value_to=value_to)

def get_ask_change_memory(current_memory: float) -> str:
    value = f"<code>{current_memory}{MEMORY_DIMENSION}</code>"
    return get_text(__change_memory, 'ask', value=value)

def get_confirm_change_memory(memory_from: float, memory_to: float) -> str:
    value_from = f"<code>{memory_from}{MEMORY_DIMENSION}</code>"
    value_to = f"<code>{memory_to}{MEMORY_DIMENSION}</code>"
    return get_text(__change_memory, 'confirm', value_from=value_from, value_to=value_to)

def get_ask_change_battery_status(current_battery_status: float) -> str:
    value = f"<code>{current_battery_status}%</code>"
    return get_text(__change_battery_status, 'ask', value=value)

def get_confirm_change_battery_status(battery_status_from: float, battery_status_to: float) -> str:
    value_from = f"<code>{battery_status_from}%</code>"
    value_to = f"<code>{battery_status_to}%</code>"
    return get_text(__change_battery_status, 'confirm', value_from=value_from, value_to=value_to)

def get_ask_change_defects(phone: Phone) -> str:
    model = f"<code>{phone.model}</code>"
    return __change_defects.get('ask').format(model=model)

def get_confirm_change_defects(defects_from: list[str], defects_to: list[str]) -> str:
    defects_from = '-' if not defects_from else f"<pre>{html.escape('\n'.join(f'- {defect}' for defect in defects_from))}</pre>"
    defects_to = '-' if not defects_to else f"<pre>{html.escape('\n'.join(f'- {defect}' for defect in defects_to))}</pre>"
    return __change_defects.get('confirm').format(defects_from=defects_from, defects_to=defects_to)

def get_defect_continue_button() -> str:
    return get_html_text(__change_defects, 'continue_button')

def get_ask_change_status(current_status_type: StatusType) -> str:
    emoji = StatusManager.get_emoji(current_status_type)
    return get_text(__change_status, 'ask', emoji=emoji, status=current_status_type)

def get_ask_sure_change_status(status_type_from: StatusType, status_type_to: StatusType) -> str:
    emoji_from = StatusManager.get_emoji(status_type_from)
    emoji_to = StatusManager.get_emoji(status_type_to)
    return get_text(__change_status, 'ask_sure', emoji_from=emoji_from, status_from=status_type_from,
                                                  emoji_to=emoji_to, status_to=status_type_to)

def get_confirm_change_status(order: Order, order_id: int, phone: Phone, status_new: Status) -> str:
    order_id = f"<code>{order_id}</code>"
    title = f"<code>{html.escape(phone.model)} {phone.memory}{MEMORY_DIMENSION} | {html.escape(phone.color)}</code>"
    status_from = order.status.status_type
    emoji_from = StatusManager.get_emoji(status_from)
    status_to = status_new.status_type
    emoji_to = StatusManager.get_emoji(status_to)
    comment = '-' if not status_new.comment else f"<pre>{html.escape(str(order.status.comment))}</pre>"
    date_time = f"<code>{status_new.get_str_date_time()}</code>"
    return __change_status.get('confirm').format(order_id=order_id, date_time=date_time, title=title,
                                                 emoji_from=emoji_from, status_from=status_from,
                                                 emoji_to=emoji_to, status_to=status_to,
                                                 comment=comment)

def get_status_confirm_button() -> str:
    return get_html_text(__change_status, 'confirm_button')

def get_ask_solve_defect(phone: Phone) -> str:
    model = f"<code>{phone.model}</code>"
    return get_text(__solve_defect, 'ask', model=model)

def get_confirm_solve_defect(phone: Phone, solved_defect: str) -> str:
    defect = f"<code>{solved_defect}</code>"
    defects = '-' if not phone.get_defects() else f"<pre>{html.escape('\n'.join(f'- {defect}' for defect in phone.get_defects()))}</pre>"
    return get_html_text(__solve_defect, 'confirm', defect = defect, defects = defects)