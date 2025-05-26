from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, FSInputFile

from UI.menu import UI_admin_page
from UI.menu import UI_phones_page

from data_statistics.defects_statistics import DeffectsStaticts
from data_statistics.income_statistics import IncomeStatistics
from data_statistics.users_statistics import UsersStatistics
from data_statistics.models_statistics import ModelsStatistics
from data_statistics.html_manager.html_template import get_html_template

from decorators import delete_callback_message, is_user_role_admin, is_user_role_manager_or_higher
from handlers.commands import command_menu
from models.status import StatusType
import handlers.keyboards as keyboards
from bot import bot, TEMP_PATH, CURRENCY


router = Router()


@router.callback_query(F.data == 'skip')
@delete_callback_message
async def skip(callback: CallbackQuery):
    pass


@router.callback_query(F.data == 'menu|show|')
@delete_callback_message
async def show_menu(callback: CallbackQuery):
    await command_menu(callback.from_user.id)


@router.callback_query(F.data == 'admin_menu|show|')
@delete_callback_message
@is_user_role_admin
async def show_admin_menu(callback: CallbackQuery):
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.row(
        InlineKeyboardButton(
            text=UI_admin_page.get_models_button(),
            callback_data='models|show|page:0'
        ),
        InlineKeyboardButton(
            text=UI_admin_page.get_colors_button(),
            callback_data='colors|show|page:0'
        )
    )
    keyboard_builder.row(
        InlineKeyboardButton(
            text=UI_admin_page.get_defects_button(),
            callback_data='defects|show|page:0'
        ),
        InlineKeyboardButton(
            text=UI_admin_page.get_memory_button(),
            callback_data='memories|show|page:0'
        )
    )
    keyboard_builder.row(keyboards.get_back_button('menu|show|'))
    await callback.message.answer(
        UI_admin_page.get_info(),
        reply_markup=keyboard_builder.as_markup()
    )


@router.callback_query(F.data == 'phone_status_menu|show|')
@delete_callback_message
@is_user_role_manager_or_higher
async def show_phones_status_menu(callback: CallbackQuery):
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.row(
        InlineKeyboardButton(
            text=UI_phones_page.get_status_button(),
            callback_data='or_ph_all|show|page:0'
        )
    )
    i = 0
    for status in StatusType:
        strategy = keyboard_builder.add
        if i % 2 == 0:
            strategy = keyboard_builder.row
        i += 1
        strategy(
            InlineKeyboardButton(
                text=UI_phones_page.get_status_button(status),
                callback_data=f'or_ph_{status.name}|statuses|page:0'
            )
        )
    keyboard_builder.row(keyboards.get_back_button('menu|show|'))
    await callback.message.answer(
        UI_phones_page.get_select_status(),
        reply_markup=keyboard_builder.as_markup()
    )


@router.callback_query(F.data == 'statistics|show|')
@delete_callback_message
@is_user_role_admin
async def show_statistics(callback: CallbackQuery):
    DeffectsStaticts()
    IncomeStatistics()
    UsersStatistics()
    ModelsStatistics()
    with open(TEMP_PATH / "diagram.html", "w", encoding="utf-8") as file:
        file.write(get_html_template(CURRENCY))
    file = FSInputFile(TEMP_PATH / "diagram.html", filename="diagram.html")
    await bot.send_document(callback.from_user.id, document=file)