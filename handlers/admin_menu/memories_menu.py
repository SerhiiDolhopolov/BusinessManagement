import re

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from database.memories_db import MemoriesDB

from UI.menu import UI_admin_page
from decorators import delete_callback_message, delete_message, is_user_role_admin
from handlers.admin_menu.admin_menu_keyboards import get_show_objects_keyboard
from bot import bot, MEMORY_DIMENSION


router = Router()
memories_DB = MemoriesDB()
obj_count_on_page = 10


class AdminMemoriesMenuState(StatesGroup):
    add_memory = State()


async def show_memories_page(message: Message, page: int):
    memories = memories_DB.get_memories(obj_count_on_page, page * obj_count_on_page)
    all_count = memories_DB.get_all_count()
    memories = {memory[0]: f'{memory[1]} {MEMORY_DIMENSION}' for memory in memories.items()}
    await message.answer(
        UI_admin_page.get_memory_info(),
        reply_markup=get_show_objects_keyboard(
            'memories', page, memories, all_count, obj_count_on_page
        )
    )


@router.callback_query(F.data.regexp(r'memories\|show\|page:(\d+)'))
@delete_callback_message
@is_user_role_admin
async def show_memories(callback: CallbackQuery):
    match = re.match(r'memories\|show\|page:(\d+)', callback.data)
    page = int(match.group(1))
    await show_memories_page(callback.message, page)


@router.callback_query(F.data == 'memories|add|')
@delete_callback_message
@is_user_role_admin
async def ask_add_memory(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AdminMemoriesMenuState.add_memory)
    message = await callback.message.answer(UI_admin_page.get_ask_new_memory())
    await state.update_data({'message_id': message.message_id})


@router.message(AdminMemoriesMenuState.add_memory, F.text)
@delete_message
@is_user_role_admin
async def add_memory(message: Message, state: FSMContext):
    try:
        message_id = (await state.get_data())['message_id']
        await bot.delete_message(message.from_user.id, message_id)
    except TelegramBadRequest:
        pass
    memory = message.text
    try:
        memories_DB.add_memory(memory)
    except Exception as e:
        await message.answer(str(e))
    await state.clear()
    await show_memories_page(message, 0)


@router.callback_query(F.data.regexp(r'memories\|select\|id:(\d+)'))
@delete_callback_message
@is_user_role_admin
async def delete_memory(callback: CallbackQuery):
    match = re.match(r'memories\|select\|id:(\d+)', callback.data)
    memory_id = int(match.group(1))
    memories_DB.delete_memory(memory_id)
    await show_memories_page(callback.message, 0)
