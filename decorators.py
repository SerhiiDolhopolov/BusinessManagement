from functools import wraps
from typing import Union

from aiogram.types import CallbackQuery, Message
from aiogram.exceptions import TelegramBadRequest

from database.users_db import UsersDB, Role
from bot import bot

usersDB = UsersDB()


def delete_callback_message(func):
    @wraps(func)
    async def wrapper(callback: CallbackQuery, *args, **kwargs):
        result = await func(callback, *args, **kwargs)
        try:
            await bot.delete_message(callback.from_user.id, callback.message.message_id)
        except TelegramBadRequest:
            pass
        return result
    return wrapper


def delete_message(func):
    @wraps(func)
    async def wrapper(message: Message, *args, **kwargs):
        result = await func(message, *args, **kwargs)
        try:
            await bot.delete_message(message.from_user.id, message.message_id)
        except TelegramBadRequest:
            pass
        return result
    return wrapper


def is_user_role_admin(func):
    """aigram_event IN (CallbackQuery, Message)"""
    @wraps(func)
    async def wrapper(aiogram_event: Union[CallbackQuery, Message], *args, **kwargs):
        if usersDB.get_role(aiogram_event.from_user.id) == Role.ADMIN:
            return await func(aiogram_event, *args, **kwargs)
    return wrapper


def is_user_role_manager_or_higher(func):
    @wraps(func)
    async def wrapper(aiogram_event: Union[CallbackQuery, Message], *args, **kwargs):
        if usersDB.get_role(aiogram_event.from_user.id) in (Role.ADMIN, Role.MANAGER):
            return await func(aiogram_event, *args, **kwargs)
    return wrapper


def is_user_role_courier_or_higher(func):
    @wraps(func)
    async def wrapper(aiogram_event: Union[CallbackQuery, Message], *args, **kwargs):
        if usersDB.get_role(aiogram_event.from_user.id) in (
            Role.ADMIN, Role.MANAGER, Role.COURIER
        ):
            return await func(aiogram_event, *args, **kwargs)
    return wrapper