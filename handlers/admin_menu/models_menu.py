from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from database.models.models_db import ModelsDB
from database.models.models_colors_db import ModelsColorsDB
from database.models.models_memories_db import ModelsMemoriesDB
from database.colors_db import ColorsDB
from database.memories_db import MemoriesDB

from UI.menu import UI_admin_page

from decorators import delete_callback_message, delete_message, is_user_role_admin
import handlers.keyboards as keyboards
from handlers.admin_menu.admin_menu_keyboards import get_show_objects_keyboard, get_model_show_objects_keyboard
import re
from bot import bot


router = Router()
obj_count_on_page = 10

models_DB = ModelsDB()
models_colors_DB = ModelsColorsDB()
models_memories_DB = ModelsMemoriesDB()
memories_DB = MemoriesDB()
colors_DB = ColorsDB()


class AdminModelsMenuState(StatesGroup):
    add_model = State()


async def show_models_page(message: Message, page: int):
    models = models_DB.get_models(obj_count_on_page, page * obj_count_on_page)
    all_count = models_DB.get_all_count()
    await message.answer(UI_admin_page.get_models_info(), 
                         reply_markup=get_show_objects_keyboard('models', page, models, all_count, obj_count_on_page))

@router.callback_query(F.data.regexp(r'models\|show\|page:(\d+)'))
@delete_callback_message
@is_user_role_admin
async def show_models(callback: CallbackQuery):
    match = re.match(r'models\|show\|page:(\d+)', callback.data)
    page = int(match.group(1))
    await show_models_page(callback.message, page)

@router.callback_query(F.data.regexp(r'models\|select\|id:(\d+)'))
@delete_callback_message
@is_user_role_admin
async def select_model(callback: CallbackQuery):
    match = re.match(r'models\|select\|id:(\d+)', callback.data)
    model_id = int(match.group(1))
    await show_model_option_page(callback.message, model_id)

async def show_model_option_page(message: Message, model_id: int):
    model = models_DB.get_model(model_id)
    page = 0
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.row(InlineKeyboardButton(text=UI_admin_page.get_models_color_button(), 
                                              callback_data=f'model_colors|show|m_id:{model_id}&page:{page}'), 
                         InlineKeyboardButton(text=UI_admin_page.get_models_memory_button(), 
                                              callback_data=f'model_memories|show|m_id:{model_id}&page:{page}'))
    keyboard_builder.row(InlineKeyboardButton(text=UI_admin_page.get_models_delete_button(), 
                                              callback_data=f'models|delete|id:{model_id}'))
    keyboard_builder.row(keyboards.get_back_button(f'models|show|page:{page}'))
    await message.answer(UI_admin_page.get_model_info(model), reply_markup=keyboard_builder.as_markup())

@router.callback_query(F.data == 'models|add|')
@delete_callback_message
@is_user_role_admin
async def ask_add_model(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AdminModelsMenuState.add_model)
    message = await callback.message.answer(UI_admin_page.get_ask_new_model())
    await state.update_data({'message_id':message.message_id})

@router.message(AdminModelsMenuState.add_model, F.text)  
@delete_message
@is_user_role_admin
async def add_model(message: Message, state: FSMContext):
    try:
        await bot.delete_message(message.from_user.id, (await state.get_data())['message_id'])
    except TelegramBadRequest:
        pass
    model = message.text
    model_id = models_DB.add_model(model)
    await state.clear()
    await show_model_option_page(message, model_id)

@router.callback_query(F.data.regexp(r'models\|delete\|id:(\d+)'))
@delete_callback_message
@is_user_role_admin
async def delete_model(callback: CallbackQuery):
    match = re.match(r'models\|delete\|id:(\d+)', callback.data)
    model_id = int(match.group(1))
    models_DB.delete_model(model_id)
    await show_models_page(callback.message, 0)



async def show_model_colors_page(message: Message, model_id: int, page: int):
    model = models_DB.get_model(model_id)
    colors = models_colors_DB.get_colors_with_flag(model_id, obj_count_on_page, page * obj_count_on_page)
    all_count = colors_DB.get_all_count()
    await message.answer(UI_admin_page.get_ask_select_colors(model), 
                         reply_markup=get_model_show_objects_keyboard(model_id, 'colors', page, colors, 
                         all_count, obj_count_on_page))

@router.callback_query(F.data.regexp(r'model_colors\|show\|m_id:(\d+)&page:(\d+)'))
@delete_callback_message
@is_user_role_admin
async def ask_select_color(callback: CallbackQuery):
    match = re.match(r'model_colors\|show\|m_id:(\d+)&page:(\d+)', callback.data)
    model_id = int(match.group(1))
    page = int(match.group(2))
    await show_model_colors_page(callback.message, model_id, page)

@router.callback_query(F.data.regexp(r'model_colors\|select\|m_id:(\d+)&id:(\d+)&page:(\d+)'))
@delete_callback_message
@is_user_role_admin
async def select_color(callback: CallbackQuery):
    match = re.match(r'model_colors\|select\|m_id:(\d+)&id:(\d+)&page:(\d+)', callback.data)
    model_id = int(match.group(1))
    color_id = int(match.group(2))
    page = int(match.group(3))
    if models_colors_DB.is_related(model_id, color_id):
        models_colors_DB.delete_relation(model_id, color_id)
    else:
        models_colors_DB.add_relation(model_id, color_id)
    await show_model_colors_page(callback.message, model_id, page)



async def show_model_memories_page(message: Message, model_id: int, page: int):
    model = models_DB.get_model(model_id)
    memories = models_memories_DB.get_memories_with_flag(model_id, obj_count_on_page, page * obj_count_on_page)
    all_count = memories_DB.get_all_count()
    await message.answer(UI_admin_page.get_ask_select_memories(model), 
                         reply_markup=get_model_show_objects_keyboard(model_id, 'memories', page, memories, 
                         all_count, obj_count_on_page))

@router.callback_query(F.data.regexp(r'model_memories\|show\|m_id:(\d+)&page:(\d+)'))
@delete_callback_message
@is_user_role_admin
async def ask_select_memory(callback: CallbackQuery):
    match = re.match(r'model_memories\|show\|m_id:(\d+)&page:(\d+)', callback.data)
    model_id = int(match.group(1))
    page = int(match.group(2))
    await show_model_memories_page(callback.message, model_id, page)

@router.callback_query(F.data.regexp(r'model_memories\|select\|m_id:(\d+)&id:(\d+)&page:(\d+)'))
@delete_callback_message
@is_user_role_admin
async def select_defect(callback: CallbackQuery):
    match = re.match(r'model_memories\|select\|m_id:(\d+)&id:(\d+)&page:(\d+)', callback.data)
    model_id = int(match.group(1))
    memory_id = int(match.group(2))
    page = int(match.group(3))
    if models_memories_DB.is_related(model_id, memory_id):
        models_memories_DB.delete_relation(model_id, memory_id)
    else:
        models_memories_DB.add_relation(model_id, memory_id)
    await show_model_memories_page(callback.message, model_id, page)