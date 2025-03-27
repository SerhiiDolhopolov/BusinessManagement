from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from database.defects_db import DefectsDB

from UI.menu import UI_admin_page

from decorators import delete_callback_message, delete_message, is_user_role_admin
from handlers.admin_menu.admin_menu_keyboards import get_show_objects_keyboard
import re
from bot import bot


router = Router()
defects_DB = DefectsDB()
obj_count_on_page = 10


class AdmindefectsMenuState(StatesGroup):
    add_model_defect = State()


async def show_defects_page(message: Message, page: int):
    defects = defects_DB.get_defects(obj_count_on_page, page * obj_count_on_page)
    all_count = defects_DB.get_all_count()
    await message.answer(UI_admin_page.get_defects_info(), 
                         reply_markup=get_show_objects_keyboard('defects', page, defects, all_count, obj_count_on_page))

@router.callback_query(F.data.regexp(r'defects\|show\|page:(\d+)'))
@delete_callback_message
@is_user_role_admin
async def show_defects(callback: CallbackQuery):
    match = re.match(r'defects\|show\|page:(\d+)', callback.data)
    page = int(match.group(1))
    await show_defects_page(callback.message, page)

@router.callback_query(F.data == 'defects|add|')
@delete_callback_message
@is_user_role_admin
async def ask_add_model_defect(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AdmindefectsMenuState.add_model_defect)
    message = await callback.message.answer(UI_admin_page.get_ask_new_defect())
    await state.update_data({'message_id':message.message_id})

@router.message(AdmindefectsMenuState.add_model_defect, F.text)  
@delete_message
@is_user_role_admin
async def add_model_defect(message: Message, state: FSMContext):
    try:
        await bot.delete_message(message.from_user.id, (await state.get_data())['message_id'])
    except TelegramBadRequest:
        pass
    defect = message.text
    defects_DB.add_defect(defect)
    await state.clear()
    await show_defects_page(message, 0)

@router.callback_query(F.data.regexp(r'defects\|select\|id:(\d+)'))
@delete_callback_message
@is_user_role_admin
async def delete_defect(callback: CallbackQuery):
    match = re.match(r'defects\|select\|id:(\d+)', callback.data)
    defect_id = int(match.group(1))
    defects_DB.delete_defect(defect_id)
    await show_defects_page(callback.message, 0)