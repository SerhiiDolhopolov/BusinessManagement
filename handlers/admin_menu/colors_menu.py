import re
from bot import bot

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from database.colors_db import ColorsDB

from UI.menu import UI_admin_page
from decorators import delete_callback_message, delete_message, is_user_role_admin
from handlers.admin_menu.admin_menu_keyboards import get_show_objects_keyboard


router = Router()
colors_DB = ColorsDB()
obj_count_on_page = 10


class AdminColorsMenuState(StatesGroup):
    add_color = State()


async def show_colors_page(message: Message, page: int):
    colors = colors_DB.get_colors(obj_count_on_page, page * obj_count_on_page)
    all_count = colors_DB.get_all_count()
    await message.answer(
        UI_admin_page.get_colors_info(),
        reply_markup=get_show_objects_keyboard(
            'colors', page, colors, all_count, obj_count_on_page
        )
    )


@router.callback_query(F.data.regexp(r'colors\|show\|page:(\d+)'))
@delete_callback_message
@is_user_role_admin
async def show_colors(callback: CallbackQuery):
    match = re.match(r'colors\|show\|page:(\d+)', callback.data)
    page = int(match.group(1))
    await show_colors_page(callback.message, page)


@router.callback_query(F.data == 'colors|add|')
@delete_callback_message
@is_user_role_admin
async def ask_add_color(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AdminColorsMenuState.add_color)
    message = await callback.message.answer(UI_admin_page.get_ask_new_color())
    await state.update_data({'message_id': message.message_id})


@router.message(AdminColorsMenuState.add_color, F.text)
@delete_message
@is_user_role_admin
async def add_color(message: Message, state: FSMContext):
    try:
        await bot.delete_message(
            message.from_user.id, (await state.get_data())['message_id']
        )
    except TelegramBadRequest:
        pass
    color = message.text
    colors_DB.add_color(color)
    await state.clear()
    await show_colors_page(message, 0)


@router.callback_query(F.data.regexp(r'colors\|select\|id:(\d+)'))
@delete_callback_message
@is_user_role_admin
async def delete_color(callback: CallbackQuery):
    match = re.match(r'colors\|select\|id:(\d+)', callback.data)
    color_id = int(match.group(1))
    colors_DB.delete_color(color_id)
    await show_colors_page(callback.message, 0)