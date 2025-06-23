import re
import random
import string
from datetime import datetime, timedelta

from aiogram import Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.users_db import UsersDB
from database.phones.phones_db import PhonesDB
from database.phones.phones_defects_db import PhonesDefectsDB
from database.phones.solved_phones_defects_db import SolvedPhonesDefectsDB
from database.colors_db import ColorsDB
from database.defects_db import DefectsDB
from database.models.models_db import ModelsDB
from database.memories_db import MemoriesDB
from database.models.models_colors_db import ModelsColorsDB
from database.models.models_memories_db import ModelsMemoriesDB
from database.orders.orders_db import OrdersDB
from database.orders.statuses_db import StatusesDB

from models.phone import Phone
from models.order import Order
from models.status import Status, StatusType

from UI.menu import UI_add_page
from bot import bot, TIMEZONE, MEMORY_DIMENSION
from decorators import delete_callback_message, delete_message, is_user_role_courier_or_higher
import handlers.keyboards as keyboards
import handlers.orders.phones.phones_manager as phones_manager


router = Router()
obj_count_on_page = 10

users_DB = UsersDB()
phones_DB = PhonesDB()
defects_DB = DefectsDB()
colors_DB = ColorsDB()
models_DB = ModelsDB()
memories_DB = MemoriesDB()
phones_defects_DB = PhonesDefectsDB()
solved_phones_defects_DB = SolvedPhonesDefectsDB()
models_colors_DB = ModelsColorsDB()
models_memories_DB = ModelsMemoriesDB()
orders_DB = OrdersDB()
statuses_DB = StatusesDB()


class AddPhoneState(StatesGroup):
    battery_status = State()
    order_purchase_price = State()
    comment = State()
    confirm = State()


@router.callback_query(F.data.regexp(r'add_phone\|ask_model\|page:(\d+)'))
@delete_callback_message
@is_user_role_courier_or_higher
async def ask_model(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    match = re.match(r'add_phone\|ask_model\|page:(\d+)', callback.data)
    page = int(match.group(1))
    await ask_model_message(callback.from_user.id, page)


async def ask_model_message(chat_id: int, page: int):
    models = models_DB.get_models(obj_count_on_page, obj_count_on_page * page)
    all_count = models_DB.get_all_count()
    keyboard_builder = InlineKeyboardBuilder()
    for model_id, model in models.items():
        keyboard_builder.add(
            InlineKeyboardButton(
                text=model,
                callback_data=f'add_phone|select_model|id:{model_id}'
            )
        )
    keyboard_builder = keyboard_builder.adjust(2)
    keyboard_builder.row(
        *keyboards.get_pagination_row(
            page, 'add_phone|ask_model|page', obj_count_on_page, all_count
        )
    )
    keyboard_builder.row(keyboards.get_back_button('menu|show|'))
    await bot.send_message(
        chat_id,
        UI_add_page.get_select_model(),
        reply_markup=keyboard_builder.as_markup()
    )


@router.callback_query(F.data.regexp(r'add_phone\|select_model\|id:(\d+)'))
@delete_callback_message
@is_user_role_courier_or_higher
async def select_model(callback: CallbackQuery, state: FSMContext):
    model_id = re.match(r'add_phone\|select_model\|id:(\d+)', callback.data).group(1)
    model = models_DB.get_model(model_id)
    phone = Phone(model)
    await phones_manager.save_phone(state, phone)
    await ask_color_message(callback.from_user.id, phone, 0)


@router.callback_query(F.data.regexp(r'add_phone\|ask_color\|page:(\d+)'))
@delete_callback_message
@is_user_role_courier_or_higher
async def ask_color(callback: CallbackQuery, state: FSMContext):
    match = re.match(r'add_phone\|ask_color\|page:(\d+)', callback.data)
    page = int(match.group(1))
    phone = await phones_manager.load_phone(state)
    await ask_color_message(callback.from_user.id, phone, page)


async def ask_color_message(chat_id: int, phone: Phone, page: int):
    model_id = models_DB.get_model_id(phone.model)
    colors = colors_DB.get_colors_by_id(
        models_colors_DB.get_colors_id(model_id),
        obj_count_on_page,
        obj_count_on_page * page
    )
    all_count = models_colors_DB.get_count_for_model(model_id)
    keyboard_builder = InlineKeyboardBuilder()
    for color_id, color in colors.items():
        keyboard_builder.add(
            InlineKeyboardButton(
                text=color,
                callback_data=f'add_phone|select_color|id:{color_id}'
            )
        )
    keyboard_builder = keyboard_builder.adjust(2)
    keyboard_builder.row(
        *keyboards.get_pagination_row(
            page, 'add_phone|ask_color|page', obj_count_on_page, all_count
        )
    )
    keyboard_builder.row(keyboards.get_back_button('add_phone|ask_model|page:0'))
    await bot.send_message(
        chat_id,
        UI_add_page.get_select_color(),
        reply_markup=keyboard_builder.as_markup()
    )


@router.callback_query(F.data.regexp(r'add_phone\|select_color\|id:(\d+)'))
@delete_callback_message
@is_user_role_courier_or_higher
async def select_color(callback: CallbackQuery, state: FSMContext):
    phone = await phones_manager.load_phone(state)
    color_id = int(re.match(r'add_phone\|select_color\|id:(\d+)', callback.data).group(1))
    color = colors_DB.get_color(color_id)
    phone.color = color
    await phones_manager.save_phone(state, phone)
    await ask_memory_message(callback.from_user.id, phone, 0)


async def ask_memory_message(chat_id: int, phone: Phone, page: int):
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
                callback_data=f'add_phone|select_memory|id:{memory_id}'
            )
        )
    keyboard_builder = keyboard_builder.adjust(2)
    keyboard_builder.row(
        *keyboards.get_pagination_row(
            page, 'add_phone|ask_memory|page', obj_count_on_page, all_count
        )
    )
    keyboard_builder.row(keyboards.get_back_button('add_phone|ask_color|page:0'))
    await bot.send_message(
        chat_id,
        UI_add_page.get_select_memory(),
        reply_markup=keyboard_builder.as_markup()
    )


@router.callback_query(F.data.regexp(r'add_phone\|ask_memory\|page:(\d+)'))
@delete_callback_message
@is_user_role_courier_or_higher
async def ask_memory(callback: CallbackQuery, state: FSMContext):
    match = re.match(r'add_phone\|ask_memory\|page:(\d+)', callback.data)
    page = int(match.group(1))
    phone = await phones_manager.load_phone(state)
    await ask_memory_message(callback.from_user.id, phone, page)


@router.callback_query(F.data.regexp(r'add_phone\|select_memory\|id:(\d+)'))
@delete_callback_message
@is_user_role_courier_or_higher
async def select_memory(callback: CallbackQuery, state: FSMContext):
    phone = await phones_manager.load_phone(state)
    memory_id = re.match(r'add_phone\|select_memory\|id:(\d+)', callback.data).group(1)
    memory = memories_DB.get_memory(memory_id)
    phone.memory = memory
    await phones_manager.save_phone(state, phone)
    await state.set_state(AddPhoneState.battery_status)
    await ask_battery_status_message(callback.from_user.id, state, phone)


@router.callback_query(F.data.regexp(r'add_phone\|filling_battery_status\|'))
@delete_callback_message
@is_user_role_courier_or_higher
async def ask_battery_status_callback(callback: CallbackQuery, state: FSMContext):
    phone = await phones_manager.load_phone(state)
    await phones_manager.save_need_to_delete_message(state, callback.message.message_id)
    await state.set_state(AddPhoneState.battery_status)
    await ask_battery_status_message(callback.from_user.id, state, phone)


async def ask_battery_status_message(chat_id: int, state: FSMContext, phone: Phone):
    color_id = colors_DB.get_color_id(phone.color)
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.row(keyboards.get_back_button(f'add_phone|select_color|id:{color_id}'))
    message = await bot.send_message(
        chat_id,
        UI_add_page.get_ask_battery_status(),
        reply_markup=keyboard_builder.as_markup()
    )
    await phones_manager.save_need_to_delete_message(state, message.message_id)


@router.message(AddPhoneState.battery_status, F.text)
@delete_message
@is_user_role_courier_or_higher
async def filling_battery_status(message: Message, state: FSMContext):
    phone = await phones_manager.load_phone(state)
    await phones_manager.delete_ask_messages(message.from_user.id, state)
    try:
        phone.battery_status = message.text
        await state.clear()
        await phones_manager.save_phone(state, phone)
        await ask_defect(message.from_user.id, state, phone, 0)
    except Exception as e:
        error_message = await bot.send_message(message.from_user.id, str(e))
        await phones_manager.save_need_to_delete_message(state, error_message.message_id)
        await state.set_state(AddPhoneState.battery_status)
        await ask_battery_status_message(message.from_user.id, state, phone)


@router.callback_query(F.data.regexp(r'add_phone\|select_defect\|page:(\d+)'))
@delete_callback_message
@is_user_role_courier_or_higher
async def show_defects_page(callback: CallbackQuery, state: FSMContext):
    match = re.match(r'add_phone\|select_defect\|page:(\d+)', callback.data)
    page = int(match.group(1))
    phone = await phones_manager.load_phone(state)
    await ask_defect(callback.from_user.id, state, phone, page)


async def ask_defect(chat_id: int, state: FSMContext, phone: Phone, page: int):
    all_count = defects_DB.get_all_count()
    keyboard_builder = InlineKeyboardBuilder()
    for defect_id, defect in defects_DB.get_defects(
        obj_count_on_page, obj_count_on_page * page
    ).items():
        keyboard_builder.add(
            InlineKeyboardButton(
                text=f"{'✅' if defect in phone.get_defects() else '❌'}{defect}",
                callback_data=f'add_phone|select_defect|id:{defect_id}&page:{page}'
            )
        )
    keyboard_builder.adjust(2)
    keyboard_builder.row(
        *keyboards.get_pagination_row(
            page, 'add_phone|select_defect|page', obj_count_on_page, all_count
        )
    )
    keyboard_builder.row(
        InlineKeyboardButton(
            text=UI_add_page.get_continue_button(),
            callback_data='add_phone|filling_purchase_price|'
        )
    )
    keyboard_builder.row(keyboards.get_back_button('add_phone|filling_battery_status|'))
    message = await bot.send_message(
        chat_id,
        UI_add_page.get_select_defects(phone),
        reply_markup=keyboard_builder.as_markup()
    )
    await phones_manager.save_need_to_delete_message(state, message.message_id)


@router.callback_query(F.data.regexp(r'add_phone\|select_defect\|id:(\d+)&page:(\d+)'))
@delete_callback_message
@is_user_role_courier_or_higher
async def add_defect(callback: CallbackQuery, state: FSMContext):
    match = re.match(r'add_phone\|select_defect\|id:(\d+)&page:(\d+)', callback.data)
    defect_id = int(match.group(1))
    page = int(match.group(2))
    defect = defects_DB.get_defect(defect_id)
    phone = await phones_manager.load_phone(state)
    if defect in phone.get_defects():
        phone.remove_defect(defect)
    else:
        phone.add_defect(defect)
    await phones_manager.save_phone(state, phone)
    await ask_defect(callback.from_user.id, state, phone, page)


async def ask_order_purchase_price_message(chat_id: int, state: FSMContext):
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.row(keyboards.get_back_button('add_phone|select_defect|page:0'))
    message = await bot.send_message(
        chat_id,
        UI_add_page.get_ask_price_purchase(),
        reply_markup=keyboard_builder.as_markup()
    )
    await phones_manager.save_need_to_delete_message(state, message.message_id)
    await state.set_state(AddPhoneState.order_purchase_price)


@router.callback_query(F.data.regexp(r'add_phone\|filling_purchase_price\|'))
@delete_callback_message
@is_user_role_courier_or_higher
async def ask_order_purchase_price_callback(callback: CallbackQuery, state: FSMContext):
    await phones_manager.save_need_to_delete_message(state, callback.message.message_id)
    await state.set_state(AddPhoneState.order_purchase_price)
    await ask_order_purchase_price_message(callback.from_user.id, state)


@router.message(AddPhoneState.order_purchase_price, F.text)
@delete_message
@is_user_role_courier_or_higher
async def filling_order_purchase_price(message: Message, state: FSMContext):
    await phones_manager.delete_ask_messages(message.from_user.id, state)
    try:
        order = Order(Status(StatusType.ON_THE_WAY))
        order.price_purchase = message.text
        await phones_manager.save_order(state, order)
        await state.set_state(AddPhoneState.comment)
        await ask_order_comment(message, state)
    except Exception as e:
        error_message = await bot.send_message(message.from_user.id, str(e))
        await phones_manager.save_need_to_delete_message(state, error_message.message_id)
        await ask_order_purchase_price_message(message.from_user.id, state)


@router.message(AddPhoneState.comment, F.text)
@delete_message
@is_user_role_courier_or_higher
async def ask_order_comment(message: Message, state: FSMContext):
    await phones_manager.delete_ask_messages(message.from_user.id, state)
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.row(
        InlineKeyboardButton(
            text=UI_add_page.get_confirm_button(),
            callback_data='add_phone|confirm|'
        )
    )
    keyboard_builder.row(keyboards.get_back_button('add_phone|filling_purchase_price|'))
    await state.set_state(AddPhoneState.confirm)
    message = await message.answer(
        UI_add_page.get_ask_comment(),
        reply_markup=keyboard_builder.as_markup()
    )
    await phones_manager.save_need_to_delete_message(state, message.message_id)


@router.callback_query(F.data.regexp(r'add_phone\|confirm\|'))
@delete_callback_message
@is_user_role_courier_or_higher
async def confirm(callback: CallbackQuery, state: FSMContext):
    await confirm_message(callback.from_user.id, state, None)


@router.message(AddPhoneState.confirm, F.text)
@delete_message
@is_user_role_courier_or_higher
async def comment_confirm(message: Message, state: FSMContext):
    await phones_manager.delete_ask_messages(message.from_user.id, state)
    await confirm_message(message.from_user.id, state, message.text)


async def confirm_message(chat_id: int, state: FSMContext, comment: str):
    order = await phones_manager.load_order(state)
    order.status.comment = comment
    order.status.date_time = datetime.now(TIMEZONE)
    phone = await phones_manager.load_phone(state)
    await state.clear()

    phone_id = phones_DB.add_phone(phone)
    order_id = orders_DB.add_order(phone_id, order.price_purchase)
    statuses_DB.add_status(chat_id, order_id, order.status)
    phones_defects_DB.add_defects(phone_id, phone.get_defects())
    text = UI_add_page.get_confirm_message(order, order_id, phone)
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.row(
        InlineKeyboardButton(
            text=UI_add_page.get_order_button(order_id),
            callback_data=f'or_ph|find|or_id:{order_id}'
        )
    )
    keyboard_builder.row(keyboards.get_back_button('menu|show|'))
    await bot.send_message(
        chat_id,
        text,
        parse_mode='HTML',
        reply_markup=keyboard_builder.as_markup()
    )
    user_username, user_role = users_DB.get_user(chat_id)
    for admin_id, _, _ in users_DB.get_admins(chat_id):
        await bot.send_message(
            admin_id,
            UI_add_page.get_confirm_message_to_other_admin(user_username, user_role, text),
            parse_mode='HTML',
            reply_markup=keyboard_builder.as_markup()
        )


async def add_random_phones_to_database(count: int):
    models = list(models_DB.get_models().items())
    all_defects = list(defects_DB.get_defects().values())

    users_ids = [user_id for user_id, _, _ in users_DB.get_users()]

    add_seconds = 0
    for i in range(count):
        add_seconds += 60 * 10

        model_id, model = random.choice(models)
        memories = list(
            memories_DB.get_memories_by_id(
                models_memories_DB.get_memories_id(model_id)
            ).values()
        )
        colors = list(
            colors_DB.get_colors_by_id(
                models_colors_DB.get_colors_id(model_id)
            ).values()
        )
        defects = random.sample(all_defects, random.randint(0, len(all_defects)))
        solved_defects = random.sample(all_defects, random.randint(0, len(all_defects)))
        memory = random.choice(memories)
        color = random.choice(colors)

        phone = Phone(model)
        phone.add_defects(defects)
        phone.battery_status = random.randint(0, 100)
        phone.color = color
        phone.memory = memory
        phone_id = phones_DB.add_phone(phone)
        phones_defects_DB.add_defects(phone_id, phone.get_defects())
        solved_phones_defects_DB.add_defects(phone_id, solved_defects)

        status = Status(StatusType.ON_THE_WAY)
        status.comment = None
        status.date_time = datetime.now(TIMEZONE) - timedelta(days=30) + timedelta(seconds=add_seconds)
        user_id = random.choice(users_ids)

        order_id = orders_DB.add_order(phone_id, random.uniform(0, 1000))
        statuses_DB.add_status(user_id, order_id, status)

        price_selling = random.uniform(0, 1200)
        charges = random.uniform(0, 100)
        if i % 50 == 0:
            price_selling = None
        if i % 30 == 0:
            charges = None
        orders_DB.update_price_selling(order_id, price_selling)
        orders_DB.update_charges(order_id, charges)

        for status_type in random.choices(
            population=[
                [StatusType.AVAILABLE, StatusType.FINISHED],
                [StatusType.AVAILABLE],
                [StatusType.AVAILABLE, StatusType.CANCELED]
            ],
            weights=[0.75, 0.15, 0.1],
            k=1
        )[0]:
            status = Status(status_type)
            status.comment = random.choice([None, random.choice(string.ascii_letters)])
            status.date_time = (
                datetime.now(TIMEZONE)
                - timedelta(
                    days=30
                )
                + (
                    timedelta(seconds=add_seconds, minutes=5)
                    if status_type == StatusType.AVAILABLE
                    else timedelta(seconds=add_seconds, minutes=20)
                )
            )
            user_id = random.choice(users_ids)
            statuses_DB.add_status(user_id, order_id, status)
