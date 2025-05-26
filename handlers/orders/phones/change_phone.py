import re
from datetime import datetime

from aiogram import Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, InlineKeyboardButton, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from database.phones.phones_db import PhonesDB
from database.phones.phones_defects_db import PhonesDefectsDB
from database.orders.orders_db import OrdersDB
from database.models.models_db import ModelsDB
from database.memories_db import MemoriesDB
from database.models.models_memories_db import ModelsMemoriesDB
from database.orders.statuses_db import StatusesDB
from database.users_db import UsersDB
from database.defects_db import DefectsDB
from database.phones.solved_phones_defects_db import SolvedPhonesDefectsDB

from UI.menu import UI_phone_page
from decorators import delete_callback_message, delete_message, is_user_role_manager_or_higher
from models.status import Status, StatusManager, StatusType
import handlers.keyboards as keyboards
from bot import bot, TIMEZONE, MEMORY_DIMENSION
import handlers.orders.phones.phones_manager as phones_manager
from handlers.orders.phones.phones_manager import clear_state


router = Router()
obj_count_on_page = 10

phones_DB = PhonesDB()
phones_defects_DB = PhonesDefectsDB()
orders_DB = OrdersDB()
statuses_DB = StatusesDB()
models_DB = ModelsDB()
memories_DB = MemoriesDB()
defects_DB = DefectsDB()
solved_phones_defects_DB = SolvedPhonesDefectsDB()
models_memories_DB = ModelsMemoriesDB()
users_DB = UsersDB()


class PhonesState(StatesGroup):
    edit_comment = State()
    edit_battery_status = State()
    edit_price_purchase = State()
    edit_price_selling = State()
    edit_charges = State()


async def send_message_to_other_admins(user_id: int, order_id: int, message: str):
    username, role = users_DB.get_user(user_id)
    for admin_id, _, _ in users_DB.get_admins(user_id):
        try:
            keyboard_builder = InlineKeyboardBuilder()
            text = UI_phone_page.get_order_button(order_id)
            keyboard_builder.row(
                InlineKeyboardButton(
                    text=text,
                    callback_data=f'or_ph|find|or_id:{order_id}'
                )
            )
            await bot.send_message(
                admin_id,
                UI_phone_page.get_confirm_message_to_other_admin(
                    username, role, order_id, message
                ),
                parse_mode='HTML',
                reply_markup=keyboard_builder.as_markup()
            )
        except TelegramBadRequest:
            pass


@router.callback_query(F.data.regexp(r'change_phone\|status\|id:(\d+)'))
@delete_callback_message
@is_user_role_manager_or_higher
async def change_status(callback: CallbackQuery):
    match = re.match(r'change_phone\|status\|id:(\d+)', callback.data)
    order_id = int(match.group(1))
    (order_id, order), (phone_id, phone) = orders_DB.get_order_phone(order_id)

    keyboard_builder = InlineKeyboardBuilder()
    current_status_type = statuses_DB.get_current_status_type(order_id)
    for select_status_type in StatusType:
        text = f'{StatusManager.get_emoji(select_status_type)}{select_status_type}'
        if select_status_type == current_status_type:
            text = f'< {StatusManager.get_emoji(select_status_type)}{select_status_type} >'
        keyboard_builder.row(
            InlineKeyboardButton(
                text=text,
                callback_data=(
                    f'change_phone|set_status|id:{order_id}&type:{select_status_type.name}'
                )
            )
        )
    keyboard_builder.adjust(2)
    keyboard_builder.row(keyboards.get_back_button(f'or_ph|select|or_id:{order_id}&page:0'))
    text = UI_phone_page.get_ask_change_status(current_status_type)
    await callback.message.answer(
        text, reply_markup=keyboard_builder.as_markup(), parse_mode='HTML'
    )


@router.callback_query(F.data.regexp(r'change_phone\|set_status\|id:(\d+)&type:(\w+)'))
@delete_callback_message
@is_user_role_manager_or_higher
async def ask_comment(callback: CallbackQuery, state: FSMContext):
    match = re.match(r'change_phone\|set_status\|id:(\d+)&type:(\w+)', callback.data)
    order_id = int(match.group(1))
    new_status_type = StatusType[match.group(2)]
    (order_id, order), (phone_id, phone) = orders_DB.get_order_phone(order_id)
    await state.set_state(PhonesState.edit_comment)
    await state.update_data({'status_type': new_status_type.name, 'order_id': order_id})

    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.row(
        InlineKeyboardButton(
            text=UI_phone_page.get_status_confirm_button(),
            callback_data='change_phone|edit_comment|'
        )
    )
    keyboard_builder.row(keyboards.get_back_button(f'change_phone|status|id:{order_id}'))
    text = UI_phone_page.get_ask_sure_change_status(order.status.status_type, new_status_type)
    message = await callback.message.answer(
        text, reply_markup=keyboard_builder.as_markup(), parse_mode='HTML'
    )
    await phones_manager.save_need_to_delete_message(state, message.message_id)


@router.callback_query(F.data.regexp(r'change_phone\|edit_comment\|'))
@delete_callback_message
@is_user_role_manager_or_higher
async def edit_comment_confirm_callback(callback: CallbackQuery, state: FSMContext):
    order_id = int((await state.get_data())['order_id'])
    status_type = StatusType[(await state.get_data())['status_type']]
    await edit_comment_message(callback.from_user.id, state, order_id, None, status_type)


@router.message(PhonesState.edit_comment, F.text)
@delete_message
@is_user_role_manager_or_higher
async def edit_comment_confirm(message: Message, state: FSMContext):
    await phones_manager.delete_ask_messages(message.from_user.id, state)
    status_type = StatusType[(await state.get_data())['status_type']]
    order_id = int((await state.get_data())['order_id'])
    await edit_comment_message(message.from_user.id, state, order_id, message.text, status_type)


async def edit_comment_message(
    chat_id: int, state: FSMContext, order_id: int, comment: str, new_status_type: StatusType
):
    (order_id, order), (phone_id, phone) = orders_DB.get_order_phone(order_id)
    status = Status(new_status_type)
    status.comment = comment
    status.date_time = datetime.now(TIMEZONE)
    order.status = status
    statuses_DB.add_status(chat_id, order_id, status)
    await clear_state(state)
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.row(keyboards.get_back_button(f'or_ph|select|or_id:{order_id}'))
    text = UI_phone_page.get_confirm_change_status(order, order_id, phone, status)
    await bot.send_message(
        chat_id, text, parse_mode='HTML', reply_markup=keyboard_builder.as_markup()
    )
    await send_message_to_other_admins(chat_id, order_id, text)


async def ask_battery_status_message(chat_id: int, state: FSMContext, order_id: int):
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.row(keyboards.get_back_button(f'or_ph|select|or_id:{order_id}'))
    phone_id = orders_DB.get_phone_id(order_id)
    phone = phones_DB.get_phone(phone_id)
    text = UI_phone_page.get_ask_change_battery_status(phone.battery_status)
    message = await bot.send_message(
        chat_id, text, reply_markup=keyboard_builder.as_markup()
    )
    await phones_manager.save_need_to_delete_message(state, message.message_id)


@router.callback_query(F.data.regexp(r'change_phone\|edit_battery_status\|or_id:(\d+)'))
@delete_callback_message
@is_user_role_manager_or_higher
async def ask_battery_status_callback(callback: CallbackQuery, state: FSMContext):
    match = re.match(r'change_phone\|edit_battery_status\|or_id:(\d+)', callback.data)
    order_id = int(match.group(1))
    (order_id, order), (phone_id, phone) = orders_DB.get_order_phone(order_id)
    await phones_manager.save_phone(state, phone)
    await state.update_data({'order_id': order_id})
    await phones_manager.save_need_to_delete_message(state, callback.message.message_id)
    await state.set_state(PhonesState.edit_battery_status)
    await ask_battery_status_message(callback.from_user.id, state, order_id)


@router.message(PhonesState.edit_battery_status, F.text)
@delete_message
@is_user_role_manager_or_higher
async def filling_battery_status(message: Message, state: FSMContext):
    order_id = int((await state.get_data())['order_id'])
    (order_id, order), (phone_id, phone) = orders_DB.get_order_phone(order_id)
    await phones_manager.delete_ask_messages(message.from_user.id, state)
    try:
        old_battery_status = phone.battery_status
        phone.battery_status = message.text
        await clear_state(state)
        phones_DB.update_battery_status(order_id, phone.battery_status)
        keyboard_builder = InlineKeyboardBuilder()
        keyboard_builder.row(keyboards.get_back_button(f'or_ph|select|or_id:{order_id}'))
        text = UI_phone_page.get_confirm_change_battery_status(
            old_battery_status, phone.battery_status
        )
        await message.answer(text=text, reply_markup=keyboard_builder.as_markup())
        await send_message_to_other_admins(message.from_user.id, order_id, text)
    except Exception as e:
        error_message = await bot.send_message(message.from_user.id, str(e))
        await phones_manager.save_need_to_delete_message(state, error_message.message_id)
        await state.set_state(PhonesState.edit_battery_status)
        await ask_battery_status_message(message.from_user.id, state, order_id)


async def ask_memory_message(chat_id: int, order_id: int, page: int):
    (order_id, order), (phone_id, phone) = orders_DB.get_order_phone(order_id)
    model_id = models_DB.get_model_id(phone.model)
    memories = memories_DB.get_memories_by_id(
        models_memories_DB.get_memories_id(model_id),
        obj_count_on_page,
        obj_count_on_page * page
    )
    all_count = models_memories_DB.get_count_for_model(model_id)
    keyboard_builder = InlineKeyboardBuilder()
    for memory_id, memory in memories.items():
        keyboard_builder.add(
            InlineKeyboardButton(
                text=f"{memory}{MEMORY_DIMENSION}",
                callback_data=f'change_phone|select_memory|or_id:{order_id}&id:{memory_id}'
            )
        )
    keyboard_builder = keyboard_builder.adjust(2)
    keyboard_builder.row(
        *keyboards.get_pagination_row(
            page,
            f'change_phone|edit_memory|or_id:{order_id}&page',
            obj_count_on_page,
            all_count
        )
    )
    keyboard_builder.row(keyboards.get_back_button(f'or_ph|select|or_id:{order_id}'))
    text = UI_phone_page.get_ask_change_memory(phone.memory)
    await bot.send_message(
        chat_id, text, reply_markup=keyboard_builder.as_markup()
    )


@router.callback_query(F.data.regexp(r'change_phone\|edit_memory\|or_id:(\d+)&page:(\d+)'))
@delete_callback_message
@is_user_role_manager_or_higher
async def ask_memory(callback: CallbackQuery, state: FSMContext):
    match = re.match(r'change_phone\|edit_memory\|or_id:(\d+)&page:(\d+)', callback.data)
    order_id = int(match.group(1))
    page = int(match.group(2))
    await ask_memory_message(callback.from_user.id, order_id, page)


@router.callback_query(F.data.regexp(r'change_phone\|select_memory\|or_id:(\d+)&id:(\d+)'))
@delete_callback_message
@is_user_role_manager_or_higher
async def select_memory(callback: CallbackQuery, state: FSMContext):
    match = re.match(r'change_phone\|select_memory\|or_id:(\d+)&id:(\d+)', callback.data)
    order_id = int(match.group(1))
    (order_id, order), (phone_id, phone) = orders_DB.get_order_phone(order_id)
    memory_id = int(match.group(2))
    memory = memories_DB.get_memory(memory_id)
    old_memory = phone.memory
    phone.memory = memory
    phones_DB.update_memory(phone_id, phone.memory)
    await clear_state(state)
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.row(keyboards.get_back_button(f'or_ph|select|or_id:{order_id}'))
    text = UI_phone_page.get_confirm_change_memory(old_memory, phone.memory)
    await callback.message.answer(text=text, reply_markup=keyboard_builder.as_markup())
    await send_message_to_other_admins(callback.from_user.id, order_id, text)


async def save_phone_for_defects_page(state: FSMContext, order_id: int):
    phone_id = orders_DB.get_phone_id(order_id)
    phone = phones_DB.get_phone(phone_id)
    phone.add_defects(phones_defects_DB.get_phone_defects(phone_id))
    await state.update_data({'phone_id': phone_id})
    await phones_manager.save_phone(state, phone)


@router.callback_query(F.data.regexp(r'change_phone\|edit_defect\|or_id:(\d+)&page:(\d+)'))
@delete_callback_message
@is_user_role_manager_or_higher
async def show_edit_defects_page(callback: CallbackQuery, state: FSMContext):
    match = re.match(r'change_phone\|edit_defect\|or_id:(\d+)&page:(\d+)', callback.data)
    order_id = int(match.group(1))
    page = int(match.group(2))
    await save_phone_for_defects_page(state, order_id)
    await ask_edit_defect(callback.from_user.id, state, order_id, page)


async def ask_edit_defect(chat_id: int, state: FSMContext, order_id: int, page: int):
    phone = await phones_manager.load_phone(state)
    all_count = defects_DB.get_all_count()
    keyboard_builder = InlineKeyboardBuilder()
    for defect_id, defect in defects_DB.get_defects(
        obj_count_on_page, obj_count_on_page * page
    ).items():
        keyboard_builder.add(
            InlineKeyboardButton(
                text=f"{'✅' if defect in phone.get_defects() else '❌'}{defect}",
                callback_data=f'change_phone|select_edit_defect|id:{defect_id}&page:{page}'
            )
        )
    keyboard_builder.adjust(2)
    keyboard_builder.row(
        *keyboards.get_pagination_row(
            page,
            f'change_phone|edit_defect|or_id:{order_id}&page',
            obj_count_on_page,
            all_count
        )
    )
    keyboard_builder.row(
        InlineKeyboardButton(
            text=UI_phone_page.get_defect_continue_button(),
            callback_data=f'change_phone|confirm_defects|or_id:{order_id}'
        )
    )
    keyboard_builder.row(keyboards.get_back_button(f'or_ph|select|or_id:{order_id}'))
    text = UI_phone_page.get_ask_change_defects(phone)
    await bot.send_message(
        chat_id, text, reply_markup=keyboard_builder.as_markup()
    )


@router.callback_query(F.data.regexp(r'change_phone\|select_edit_defect\|id:(\d+)&page:(\d+)'))
@delete_callback_message
@is_user_role_manager_or_higher
async def edit_defect(callback: CallbackQuery, state: FSMContext):
    match = re.match(r'change_phone\|select_edit_defect\|id:(\d+)&page:(\d+)', callback.data)
    defect_id = int(match.group(1))
    defect = defects_DB.get_defect(defect_id)
    page = int(match.group(2))
    phone_id = int((await state.get_data())['phone_id'])
    phone = await phones_manager.load_phone(state)
    order_id = orders_DB.get_order_id(phone_id)
    if defect in phone.get_defects():
        phone.remove_defect(defect)
    else:
        phone.add_defect(defect)
    await phones_manager.save_phone(state, phone)
    await ask_edit_defect(callback.from_user.id, state, order_id, page)


@router.callback_query(F.data.regexp(r'change_phone\|confirm_defects\|or_id:(\d+)'))
@delete_callback_message
@is_user_role_manager_or_higher
async def edit_defects_confirm(callback: CallbackQuery, state: FSMContext):
    match = re.match(r'change_phone\|confirm_defects\|or_id:(\d+)', callback.data)
    order_id = int(match.group(1))
    phone_id = int((await state.get_data())['phone_id'])
    phone = await phones_manager.load_phone(state)
    previous_defects = phones_defects_DB.get_phone_defects(phone_id)
    phones_defects_DB.clear_defects(phone_id)
    phones_defects_DB.add_defects(phone_id, phone.get_defects())
    await clear_state(state)
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.row(keyboards.get_back_button(f'or_ph|select|or_id:{order_id}'))
    text = UI_phone_page.get_confirm_change_defects(previous_defects, phone.get_defects())
    await callback.message.answer(
        text=text, reply_markup=keyboard_builder.as_markup(), parse_mode='HTML'
    )
    await send_message_to_other_admins(callback.from_user.id, order_id, text)


@router.callback_query(F.data.regexp(r'change_phone\|solve_defect\|or_id:(\d+)&page:(\d+)'))
@delete_callback_message
@is_user_role_manager_or_higher
async def show_solve_defects_page(callback: CallbackQuery, state: FSMContext):
    match = re.match(r'change_phone\|solve_defect\|or_id:(\d+)&page:(\d+)', callback.data)
    order_id = int(match.group(1))
    page = int(match.group(2))
    await save_phone_for_defects_page(state, order_id)
    await ask_solve_defect(callback.from_user.id, state, order_id, page)


async def ask_solve_defect(chat_id: int, state: FSMContext, order_id: int, page: int):
    phone = await phones_manager.load_phone(state)
    defects = phone.get_defects()
    keyboard_builder = InlineKeyboardBuilder()
    for defect_id, defect in defects_DB.get_defects(
        obj_count_on_page, obj_count_on_page * page
    ).items():
        if defect in defects:
            keyboard_builder.add(
                InlineKeyboardButton(
                    text=f"✅{defect}",
                    callback_data=f'change_phone|select_solve_defect|id:{defect_id}&page:{page}'
                )
            )
    keyboard_builder.adjust(2)
    keyboard_builder.row(
        *keyboards.get_pagination_row(
            page,
            f'change_phone|solve_defect|or_id:{order_id}&page',
            obj_count_on_page,
            len(defects)
        )
    )
    keyboard_builder.row(keyboards.get_back_button(f'or_ph|select|or_id:{order_id}'))
    text = UI_phone_page.get_ask_solve_defect(phone)
    await bot.send_message(
        chat_id, text, reply_markup=keyboard_builder.as_markup()
    )


@router.callback_query(F.data.regexp(r'change_phone\|select_solve_defect\|id:(\d+)&page:(\d+)'))
@delete_callback_message
@is_user_role_manager_or_higher
async def solve_defect(callback: CallbackQuery, state: FSMContext):
    match = re.match(r'change_phone\|select_solve_defect\|id:(\d+)&page:(\d+)', callback.data)
    defect_id = int(match.group(1))
    defect = defects_DB.get_defect(defect_id)
    page = int(match.group(2))
    phone_id = int((await state.get_data())['phone_id'])
    phone = await phones_manager.load_phone(state)
    order_id = orders_DB.get_order_id(phone_id)
    phone.remove_defect(defect)

    await clear_state(state)
    phones_defects_DB.clear_defects(phone_id)
    phones_defects_DB.add_defects(phone_id, phone.get_defects())
    solved_phones_defects_DB.add_defect(phone_id, defect)

    keyboard_builder = InlineKeyboardBuilder()
    if phone.get_defects():
        keyboard_builder.add(
            InlineKeyboardButton(
                text=UI_phone_page.get_solve_defect_button(),
                callback_data=f'change_phone|solve_defect|or_id:{order_id}&page:{page}'
            )
        )
    keyboard_builder.row(keyboards.get_back_button(f'or_ph|select|or_id:{order_id}'))
    text = UI_phone_page.get_confirm_solve_defect(phone, defect)
    await callback.message.answer(
        text=text, reply_markup=keyboard_builder.as_markup(), parse_mode='HTML'
    )
    await send_message_to_other_admins(callback.from_user.id, order_id, text)


async def ask_order_parametr_message(text: str, chat_id: int, state: FSMContext, order_id: int):
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.row(keyboards.get_back_button(f'or_ph|select|or_id:{order_id}'))
    message = await bot.send_message(
        chat_id, text, reply_markup=keyboard_builder.as_markup()
    )
    await phones_manager.save_need_to_delete_message(state, message.message_id)


@router.callback_query(F.data.regexp(r'change_phone\|edit_(price_purchase|price_selling|charges)\|or_id:(\d+)'))
@delete_callback_message
@is_user_role_manager_or_higher
async def ask_order_parametr_callback(callback: CallbackQuery, state: FSMContext):
    match = re.match(
        r'change_phone\|edit_(price_purchase|price_selling|charges)\|or_id:(\d+)', callback.data
    )
    parametr = match.group(1)
    order_id = int(match.group(2))
    order = orders_DB.get_order(order_id)
    await state.update_data({'order_id': order_id})
    await phones_manager.save_need_to_delete_message(state, callback.message.message_id)
    if parametr == 'price_purchase':
        await state.set_state(PhonesState.edit_price_purchase)
        text = UI_phone_page.get_ask_change_price_purchase(order.price_purchase)
        await ask_order_parametr_message(text, callback.from_user.id, state, order_id)
    elif parametr == 'price_selling':
        await state.set_state(PhonesState.edit_price_selling)
        text = UI_phone_page.get_ask_change_price_selling(order.price_selling)
        await ask_order_parametr_message(text, callback.from_user.id, state, order_id)
    elif parametr == 'charges':
        await state.set_state(PhonesState.edit_charges)
        text = UI_phone_page.get_ask_change_charges(order.charges)
        await ask_order_parametr_message(text, callback.from_user.id, state, order_id)


@delete_message
@is_user_role_manager_or_higher
async def filling_order_parametr(message: Message, state: FSMContext, parametr: str):
    order_id = int((await state.get_data())['order_id'])
    order = orders_DB.get_order(order_id)
    await phones_manager.delete_ask_messages(message.from_user.id, state)
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.row(keyboards.get_back_button(f'or_ph|select|or_id:{order_id}'))
    try:
        if parametr == 'price_purchase':
            old_price_purchase = order.price_purchase
            order.price_purchase = message.text
            orders_DB.update_price_purchase(order_id, order.price_purchase)
            text = UI_phone_page.get_confirm_change_price_purchase(
                old_price_purchase, order.price_purchase
            )
        elif parametr == 'price_selling':
            old_price_selling = order.price_selling
            order.price_selling = message.text
            orders_DB.update_price_selling(order_id, order.price_selling)
            text = UI_phone_page.get_confirm_change_price_selling(
                old_price_selling, order.price_selling
            )
        elif parametr == 'charges':
            old_charges = order.charges
            order.charges = message.text
            orders_DB.update_charges(order_id, order.charges)
            text = UI_phone_page.get_confirm_change_charges(old_charges, order.charges)
        await message.answer(text=text, reply_markup=keyboard_builder.as_markup())
        await send_message_to_other_admins(message.from_user.id, order_id, text)
        await clear_state(state)
    except Exception as e:
        error_message = await bot.send_message(message.from_user.id, str(e))
        await phones_manager.save_need_to_delete_message(state, error_message.message_id)
        if parametr == 'price_purchase':
            await state.set_state(PhonesState.edit_price_purchase)
            text = UI_phone_page.get_ask_change_price_purchase(order.price_purchase)
            await ask_order_parametr_message(text, message.from_user.id, state, order_id)
        elif parametr == 'price_selling':
            await state.set_state(PhonesState.edit_price_selling)
            text = UI_phone_page.get_ask_change_price_selling(order.price_selling)
            await ask_order_parametr_message(text, message.from_user.id, state, order_id)
        elif parametr == 'charges':
            await state.set_state(PhonesState.edit_charges)
            text = UI_phone_page.get_ask_change_charges(order.charges)
            await ask_order_parametr_message(text, message.from_user.id, state, order_id)


@router.message(PhonesState.edit_price_purchase, F.text)
@is_user_role_manager_or_higher
async def filling_price_purchase(message: Message, state: FSMContext):
    await filling_order_parametr(message, state, 'price_purchase')


@router.message(PhonesState.edit_price_selling, F.text)
@is_user_role_manager_or_higher
async def filling_price_selling(message: Message, state: FSMContext):
    await filling_order_parametr(message, state, 'price_selling')


@router.message(PhonesState.edit_charges, F.text)
@is_user_role_manager_or_higher
async def filling_price_charges(message: Message, state: FSMContext):
    await filling_order_parametr(message, state, 'charges')
