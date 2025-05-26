import re
import html
from itertools import islice
from bot import bot

from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext

from database.orders.orders_db import OrdersDB
from database.orders.statuses_db import StatusesDB
from database.memories_db import MemoriesDB
from database.users_db import UsersDB, Role
from database.phones.phones_defects_db import PhonesDefectsDB

from UI.menu import UI_phones_page, UI_phone_page
from UI.commands import UI_commands

from decorators import delete_callback_message, is_user_role_manager_or_higher
from models.status import StatusManager, StatusType
import handlers.keyboards as keyboards
import handlers.orders.phones.phones_manager as phones_manager


router = Router()
obj_count_on_page = 10

orders_DB = OrdersDB()
statuses_DB = StatusesDB()
users_DB = UsersDB()
memories_DB = MemoriesDB()
phones_defect_DB = PhonesDefectsDB()


@router.callback_query(F.data.regexp(r'or_ph_(.+)\|(show|statuses)\|page:(\d+)'))
@delete_callback_message
async def get_phones(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    match = re.match(r'or_ph_(.+)\|(\w+)\|page:(\d+)', callback.data)
    page_status_type = match.group(1)
    status_type = (
        None if page_status_type in ('all', 'my')
        or re.match(r'(.+)defect_(\w+)', page_status_type)
        else StatusType[page_status_type]
    )
    back_button = 'menu|show|' if match.group(2) == 'show' else 'phone_status_menu|show|'
    page = int(match.group(3))
    text = UI_phones_page.get_info()

    if page_status_type == 'my':
        orders_phones = statuses_DB.get_orders_by_user(
            callback.from_user.id, obj_count_on_page, page * obj_count_on_page
        )
        all_count = statuses_DB.get_count_orders_by_user(callback.from_user.id)
        text = UI_phones_page.get_my_phones_info()
    elif re.match(r'spares_defect_(.+)', page_status_type) or re.match(r'repairs_defect_(.+)', page_status_type):
        page = 0
        if re.match(r'spares_defect_(.+)', page_status_type):
            defect = re.match(r'spares_defect_(.+)', page_status_type).group(1)
            status_type = StatusType.WAITING_FOR_SPARES
            back_button = f'or_ph_spares_defects|show_categories|page:{page}'
        elif re.match(r'repairs_defect_(.+)', page_status_type):
            defect = re.match(r'repairs_defect_(.+)', page_status_type).group(1)
            status_type = StatusType.WAITING_FOR_REPAIRS
            back_button = f'or_ph_repairs_defects|show_categories|page:{page}'
        orders_phones = statuses_DB.get_orders_by_defect(
            status_type, defect, obj_count_on_page, page * obj_count_on_page
        )
        all_count = statuses_DB.get_count_orders_by_defect(status_type, defect)
        text = UI_phones_page.get_defect_info(status_type, defect)
    else:
        orders_phones = orders_DB.get_orders_phones(
            status_type, obj_count_on_page, page * obj_count_on_page
        )
        all_count = statuses_DB.get_count_orders_with_current_status(status_type)
        text = UI_phones_page.get_info(status_type)

    await phones_manager.save_current_phone_menu_status_type(state, page_status_type)
    await phones_manager.save_page(state, page)

    keyboard_builder = InlineKeyboardBuilder()
    for (order_id, order), (phone_id, phone) in orders_phones:
        keyboard_builder.row(
            InlineKeyboardButton(
                text=UI_phones_page.get_phone_button(order, phone),
                callback_data=f"or_ph|select|or_id:{order_id}"
            )
        )
    keyboard_builder.row(
        *keyboards.get_pagination_row(
            page, f'or_ph_{page_status_type}|show|page', obj_count_on_page, all_count
        )
    )
    keyboard_builder.row(keyboards.get_back_button(back_button))
    await callback.message.answer(text, reply_markup=keyboard_builder.as_markup())


@router.callback_query(F.data.regexp(r'or_ph\|find\|or_id:(\d+)'))
@delete_callback_message
async def find_phone_callback(callback: CallbackQuery):
    match = re.match(r'or_ph\|find\|or_id:(\d+)', callback.data)
    order_id = int(match.group(1))
    await select_phone(callback.from_user.id, order_id, 'menu|show|')


@router.callback_query(F.data.regexp(r'or_ph\|select\|or_id:(\d+)'))
@delete_callback_message
async def select_phone_callback(callback: CallbackQuery, state: FSMContext):
    match = re.match(r'or_ph\|select\|or_id:(\d+)', callback.data)
    page_status_type = await phones_manager.load_current_phone_menu_status_type(state)
    order_id = int(match.group(1))
    page = await phones_manager.load_page(state)
    await select_phone(
        callback.from_user.id, order_id, f'or_ph_{page_status_type}|show|page:{page}'
    )


async def select_phone(chat_id: int, order_id: int, callback_back_button: str = None):
    role = users_DB.get_role(chat_id)
    order_phone = orders_DB.get_order_phone(order_id)
    if not order_phone:
        await bot.send_message(chat_id, UI_commands.get_order_exception_order_not_exist())
        return

    (order_id, order), (phone_id, phone) = order_phone
    phone.add_defects(phones_defect_DB.get_phone_defects(phone_id))
    phone_information = UI_phone_page.get_info(order, order_id, phone, role)

    keyboard_builder = InlineKeyboardBuilder()
    if role in (Role.ADMIN, Role.MANAGER):
        keyboard_builder.row(
            InlineKeyboardButton(
                text=UI_phone_page.get_change_price_purchase_button(),
                callback_data=f'change_phone|edit_price_purchase|or_id:{order_id}'
            ),
            InlineKeyboardButton(
                text=UI_phone_page.get_change_charges_button(),
                callback_data=f'change_phone|edit_charges|or_id:{order_id}'
            ),
            InlineKeyboardButton(
                text=UI_phone_page.get_change_price_selling_button(),
                callback_data=f'change_phone|edit_price_selling|or_id:{order_id}'
            )
        )
        keyboard_builder.row(
            InlineKeyboardButton(
                text=UI_phone_page.get_change_memory_button(),
                callback_data=f'change_phone|edit_memory|or_id:{order_id}&page:0'
            ),
            InlineKeyboardButton(
                text=UI_phone_page.get_change_battery_button(),
                callback_data=f'change_phone|edit_battery_status|or_id:{order_id}'
            ),
            InlineKeyboardButton(
                text=UI_phone_page.get_change_defects_button(),
                callback_data=f'change_phone|edit_defect|or_id:{order_id}&page:0'
            )
        )
        keyboard_builder.row(
            InlineKeyboardButton(
                text=UI_phone_page.get_change_status_button(),
                callback_data=f'change_phone|status|id:{order_id}'
            )
        )
        keyboard_builder.row(
            InlineKeyboardButton(
                text=UI_phone_page.get_solve_defect_button(),
                callback_data=f'change_phone|solve_defect|or_id:{order_id}&page:0'
            )
        )
        keyboard_builder.row(
            InlineKeyboardButton(
                text=UI_phone_page.get_history_button(),
                callback_data=f'or_ph|history|or_id:{order_id}'
            )
        )
    if callback_back_button:
        keyboard_builder.row(keyboards.get_back_button(callback_back_button))
    await bot.send_message(
        chat_id, phone_information, parse_mode='HTML', reply_markup=keyboard_builder.as_markup()
    )


@router.callback_query(F.data.regexp(r'or_ph\|history\|or_id:(\d+)'))
@delete_callback_message
@is_user_role_manager_or_higher
async def show_order_history(callback: CallbackQuery):
    match = re.match(r'or_ph\|history\|or_id:(\d+)', callback.data)
    order_id = int(match.group(1))
    statuses = statuses_DB.get_statuses_ascending(order_id)
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.row(keyboards.get_back_button(f'or_ph|select|or_id:{order_id}'))

    while statuses:
        await callback.message.answer(
            f'\n<b>{ " " * 30}↓</b>\n'.join([
                (
                    f"{StatusManager.get_emoji(status.status_type)} {status.status_type}"
                    f"\n@{users_DB.get_username(user_id)}"
                    + (f"\n<pre>{html.escape(str(status.comment))}</pre>" if status.comment else '')
                    + f"\n<code>{html.escape(str(status.get_str_date_time()))}</code>"
                )
                for status_id, (user_id, status) in dict(islice(statuses.items(), 10)).items()
            ]),
            parse_mode='HTML',
            reply_markup=keyboard_builder.as_markup()
        )
        statuses = dict(islice(statuses.items(), 10, None))


@router.callback_query(F.data.regexp(r'or_ph_(\w+)_defects\|show_categories\|page:(\d+)'))
@delete_callback_message
@is_user_role_manager_or_higher
async def show_select_defect(callback: CallbackQuery):
    match = re.match(r'or_ph_(\w+)_defects\|show_categories\|page:(\d+)', callback.data)
    what_status_type = match.group(1)
    page = int(match.group(2))

    status_type = (
        StatusType.WAITING_FOR_SPARES
        if what_status_type == 'spares'
        else StatusType.WAITING_FOR_REPAIRS
    )

    defects_group = statuses_DB.get_defect_groups_orders(
        status_type, obj_count_on_page, page * obj_count_on_page
    )
    all_count = statuses_DB.get_count_defect_groups_orders(status_type)
    message = UI_phones_page.get_defect_ask_category(status_type)

    keyboard_builder = InlineKeyboardBuilder()
    for defect, count in defects_group.items():
        keyboard_builder.add(
            InlineKeyboardButton(
                text=f"{defect}:{count}",
                callback_data=f"or_ph_{what_status_type}_defect_{defect}|show|page:0"
            )
        )
    keyboard_builder.adjust(2)
    keyboard_builder.row(
        *keyboards.get_pagination_row(
            page,
            f"or_ph_{what_status_type}_defects|show_categories|page",
            obj_count_on_page,
            all_count
        )
    )
    keyboard_builder.row(keyboards.get_back_button('menu|show|'))
    await callback.message.answer(message, reply_markup=keyboard_builder.as_markup())
