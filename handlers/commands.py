import logging

from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InlineKeyboardButton, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from database.users_db import UsersDB, Role
from database.database import DB
from database.orders.statuses_db import StatusesDB

from UI.menu import UI_menu, UI_main_page
from UI.commands import UI_commands

from bot import bot, get_backup_name
import handlers.keyboards as keyboards
from handlers.orders.phones.phones import select_phone
from handlers.orders.phones.add_phone import add_random_phones_to_database
from decorators import is_user_role_admin, is_user_role_manager_or_higher, delete_message
from models.status import StatusType


router = Router()
users_DB = UsersDB()
statuses_DB = StatusesDB()


class CommandsState(StatesGroup):
    set_role = State()
    find_order = State()


@router.message(Command('add_phones'))
@delete_message
@is_user_role_admin
async def command_add_phones(message: Message):
    await send_backup(message.from_user.id)
    if logging.getLogger().isEnabledFor(logging.DEBUG):
        await add_random_phones_to_database(20000)


@router.message(CommandStart())
@delete_message
async def command_start(message: Message) -> None:
    if not users_DB.is_user_exist(message.from_user.id):
        users_DB.register_user(message.from_user.id, message.from_user.username)
        await message.answer(UI_menu.get_welcome())

        keyboard_builder = InlineKeyboardBuilder()
        current_role = users_DB.get_role(message.from_user.id)
        for role in Role:
            if role != current_role and role != Role.ADMIN:
                keyboard_builder.add(
                    InlineKeyboardButton(
                        text=role,
                        callback_data=f'user|set_role|id:{message.from_user.id}&role:{role}'
                    )
                )

        for admin_id, _, _ in users_DB.get_admins(message.from_user.id):
            await bot.send_message(
                admin_id,
                UI_menu.get_user_registration_select_role(message.from_user.username),
                reply_markup=keyboard_builder.as_markup()
            )
    else:
        users_DB.set_username(message.from_user.id, message.from_user.username)
    await command_menu(message.from_user.id)


async def command_menu(chat_id: int):
    role = users_DB.get_role(chat_id)
    keyboard_builder = InlineKeyboardBuilder()

    if role is Role.USER:
        for _, admin_username, _ in users_DB.get_admins():
            keyboard_builder.row(
                InlineKeyboardButton(
                    text=UI_menu.get_chat_with_admin_button(admin_username),
                    url=f'https://t.me/{admin_username}'
                )
            )

    if role in (Role.ADMIN, Role.MANAGER, Role.COURIER):
        keyboard_builder.row(
            InlineKeyboardButton(
                text=UI_main_page.get_my_phones_button(),
                callback_data='or_ph_my|show|page:0'
            ),
            InlineKeyboardButton(
                text=UI_main_page.get_add_button(),
                callback_data='add_phone|ask_model|page:0'
            )
        )

    keyboard_builder.row(
        InlineKeyboardButton(
            text=UI_main_page.get_available_button(),
            callback_data=f'or_ph_{StatusType.AVAILABLE.name}|show|page:0'
        )
    )

    if role in (Role.ADMIN, Role.MANAGER):
        keyboard_builder.row(
            InlineKeyboardButton(
                text=UI_main_page.get_phones_button(),
                callback_data='phone_status_menu|show|'
            )
        )
        keyboard_builder.row(
            InlineKeyboardButton(
                text=UI_main_page.get_need_spares_button(),
                callback_data='or_ph_spares_defects|show_categories|page:0'
            )
        )
        keyboard_builder.row(
            InlineKeyboardButton(
                text=UI_main_page.get_need_repairs_button(),
                callback_data='or_ph_repairs_defects|show_categories|page:0'
            )
        )

    if role == Role.ADMIN:
        keyboard_builder.row(
            InlineKeyboardButton(
                text=UI_main_page.get_users_button(),
                callback_data='users|show|page:0'
            )
        )
        keyboard_builder.row(
            InlineKeyboardButton(
                text=UI_main_page.get_couriers_button(),
                callback_data='users|show_couriers|page:0'
            ),
            InlineKeyboardButton(
                text=UI_main_page.get_managers_button(),
                callback_data='users|show_managers|page:0'
            )
        )
        keyboard_builder.row(
            InlineKeyboardButton(
                text=UI_main_page.get_admin_panel_button(),
                callback_data='admin_menu|show|'
            )
        )
        keyboard_builder.row(
            InlineKeyboardButton(
                text=UI_main_page.get_statistics_button(),
                callback_data='statistics|show|'
            )
        )

    await bot.send_message(
        chat_id,
        UI_main_page.get_info(role),
        reply_markup=keyboard_builder.as_markup()
    )


@router.message(Command('role'))
@delete_message
@is_user_role_admin
async def command_role(message: Message, state: FSMContext):
    await state.set_state(CommandsState.set_role)
    message = await message.answer(UI_commands.get_ask_role())
    await state.update_data({'message_for_delete': message.message_id})


@router.message(CommandsState.set_role)
@delete_message
@is_user_role_admin
async def command_ask_role(message: Message, state: FSMContext):
    try:
        await bot.delete_message(
            message.from_user.id, int((await state.get_data())['message_for_delete'])
        )
    except TelegramBadRequest:
        pass
    try:
        user_id = int(message.text)
        if users_DB.is_user_exist(user_id):
            username = users_DB.get_username(user_id)
            await message.answer(
                UI_commands.get_select_role(username),
                reply_markup=keyboards.get_change_role_keyboard(user_id)
            )
        else:
            await message.answer(UI_commands.get_role_exception_user_not_exist())
        await state.clear()
    except ValueError:
        await message.answer(UI_commands.get_role_exception_not_correct_id())


@router.message(Command('order'))
@delete_message
@is_user_role_manager_or_higher
async def command_order(message: Message, state: FSMContext):
    await state.set_state(CommandsState.find_order)
    message = await message.answer(UI_commands.get_ask_order())
    await state.update_data({'message_for_delete': message.message_id})


@router.message(CommandsState.find_order, F.text)
@delete_message
@is_user_role_manager_or_higher
async def find_order(message: Message, state: FSMContext):
    try:
        await bot.delete_message(
            message.from_user.id, int((await state.get_data())['message_for_delete'])
        )
    except TelegramBadRequest:
        pass
    try:
        order_id = int(message.text)
        await select_phone(message.from_user.id, order_id, 'skip')
        await state.clear()
    except ValueError:
        await message.answer(UI_commands.get_order_exception_not_correct_id())


@router.message(Command('backup'))
@delete_message
@is_user_role_manager_or_higher
async def command_backup(message: Message):
    await send_backup(message.from_user.id)


async def send_backup(user_id: int):
    file, message = await get_backup()
    await bot.send_document(user_id, document=file, caption=message, parse_mode='HTML')


async def get_backup() -> tuple[FSInputFile, str]:
    """RETURNS (File, message)"""
    statuses_count = statuses_DB.get_count_statuses_by_today()
    price_selling_sum, profit_money_sum = statuses_DB.get_earned_money_by_today()
    price_purchase_sum, charges_sum = statuses_DB.get_spent_money_by_today()
    message = UI_commands.get_backup_info(
        statuses_count, price_selling_sum, profit_money_sum, price_purchase_sum, charges_sum
    )
    backup_path = DB.get_backup()
    file = FSInputFile(backup_path, filename=str(get_backup_name()))
    return file, message