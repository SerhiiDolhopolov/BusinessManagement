from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from models.phone import Phone
from models.order import Order

from bot import bot

async def clear_state(state: FSMContext):
    data = await state.get_data()
    data.pop('phone', None)
    data.pop('order', None)
    data.pop('order_id', None)
    data.pop('phone_id', None)
    await state.set_data(data)

async def save_current_phone_menu_status_type(state: FSMContext, status_type: str = None):
    await state.update_data({'current_phone_menu_status_type': status_type})
    data = await state.get_data()
    if status_type:
        await state.update_data({'current_phone_menu_status_type': status_type})
    else:
        data.pop('current_phone_menu_status_type', None)
        await state.set_data(data)

async def load_current_phone_menu_status_type(state: FSMContext) -> str:
    """RETURNS all or status type name"""
    data = await state.get_data()
    value = data.get('current_phone_menu_status_type', 'all')
    return value


async def save_page(state: FSMContext, page: int):
    await state.update_data({'page': page})

async def load_page(state: FSMContext):
    data = await state.get_data()
    if 'page' not in data:
        return 0
    return int(data['page'])

async def save_phone(state: FSMContext, phone: Phone):
    await state.update_data({'phone': phone})

async def load_phone(state: FSMContext) -> Phone:
    data = await state.get_data()
    if 'phone' not in data:
        return
    return data['phone']

async def save_order(state: FSMContext, order: Order):
    await state.update_data({'order': order})

async def load_order(state: FSMContext) -> Order:
    data = await state.get_data()
    if 'order' not in data:
        return
    return data['order']

async def save_need_to_delete_message(state: FSMContext, message_id: int):
    data = await state.get_data()
    messages_need_to_delete = []
    if 'messages_need_to_delete' in data:
        if data['messages_need_to_delete']:
            messages_need_to_delete = data['messages_need_to_delete']
    messages_need_to_delete.append(message_id)
    await state.update_data({'messages_need_to_delete': messages_need_to_delete})

async def delete_ask_messages(chat_id: int, state: FSMContext):
    data = await state.get_data()
    messages_need_to_delete = []
    if 'messages_need_to_delete' in data:
        if data['messages_need_to_delete']:
            messages_need_to_delete = data['messages_need_to_delete']
    for message_id in messages_need_to_delete:
        try:
            await bot.delete_message(chat_id, message_id)
        except TelegramBadRequest:
            pass
    await state.update_data({'messages_need_to_delete': None})