from UI.language_resources import LanguageResources
from UI.emoji import UI_emoji
from UI.base import get_text, get_html_text

from models.status import StatusManager, StatusType
from models.order import Order
from models.phone import Phone

from bot import MEMORY_DIMENSION, CURRENCY, format_money


__menu = LanguageResources().menu
__phones_page = __menu['phones_page']
__defect_need_spares = __phones_page['defect_need_spares']
__defect_need_repairs = __phones_page['defect_need_repairs']


def get_my_phones_info() -> str:
    return get_text(__phones_page, 'my_phones_info')


def get_info(status_type: StatusType = None) -> str:
    """If status_type == None return all phones info"""
    emoji = StatusManager.get_emoji(status_type)
    if status_type:
        return get_text(__phones_page, 'info', emoji=emoji, status=status_type)
    return get_text(__phones_page, 'all_phones_info')


def get_status_button(status_type: StatusType = None) -> str:
    """If status_type == None return all phones info"""
    emoji = StatusManager.get_emoji(status_type)
    if status_type:
        return get_html_text(__phones_page, 'status_button', emoji=emoji, status=status_type)
    return get_html_text(__phones_page, 'all_phones_status_button')


def get_select_status() -> str:
    return get_text(__phones_page, 'select_status')


def get_phone_button(order: Order, phone: Phone) -> str:
    status_emoji = (
        StatusManager.get_emoji(order.status.status_type)
        if order.status.status_type else ''
    )
    title = f"{phone.model} {phone.memory}{MEMORY_DIMENSION}|{phone.color}"

    price_selling, money_emoji = '', ''
    if order.price_selling:
        price_selling = f"{format_money(order.price_selling)}{CURRENCY}"
        money_emoji = UI_emoji.get_money()

    return get_html_text(
        __phones_page, 'phone_button',
        status_emoji=status_emoji,
        title=title,
        price_selling=price_selling,
        money_emoji=money_emoji
    )


def get_defect_ask_category(status_type: StatusType) -> str:
    """status_type in (StatusType.WAITING_FOR_SPARES, StatusType.WAITING_FOR_REPAIRS)"""
    if status_type == StatusType.WAITING_FOR_SPARES:
        return get_text(__defect_need_spares, 'ask_category')
    elif status_type == StatusType.WAITING_FOR_REPAIRS:
        return get_text(__defect_need_repairs, 'ask_category')
    else:
        return None


def get_defect_info(status_type: StatusType, defect: str) -> str:
    """status_type in (StatusType.WAITING_FOR_SPARES, StatusType.WAITING_FOR_REPAIRS)"""
    if status_type == StatusType.WAITING_FOR_SPARES:
        return get_text(__defect_need_spares, 'info', defect=defect)
    elif status_type == StatusType.WAITING_FOR_REPAIRS:
        return get_text(__defect_need_repairs, 'info', defect=defect)
    else:
        return None