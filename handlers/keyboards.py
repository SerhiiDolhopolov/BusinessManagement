from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from UI.emoji import UI_navigation
from database.users_db import UsersDB, Role


users_DB = UsersDB()


def get_back_button(callback: str) -> InlineKeyboardButton:
    return InlineKeyboardButton(text=UI_navigation.get_back_button(), callback_data=callback)


def get_pagination_keyboard(
    page: int, callback_info: str, obj_count_on_page: int, obj_count: int
) -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.row(
        *get_pagination_row(page, callback_info, obj_count_on_page, obj_count)
    )
    keyboard_builder.row(get_back_button('menu|show|'))
    return keyboard_builder.as_markup()


def get_pagination_row(
    page: int, callback_info: str, obj_count_on_page: int, obj_count: int
) -> list[InlineKeyboardButton]:
    buttons = []
    if obj_count_on_page >= obj_count:
        return buttons
    if page > 0:
        buttons.append(
            InlineKeyboardButton(
                text=UI_navigation.get_preview_page_button(),
                callback_data=f'{callback_info}:{page - 1}'
            )
        )
    buttons.append(
        InlineKeyboardButton(
            text=UI_navigation.get_current_page_button(page + 1),
            callback_data='None'
        )
    )
    if obj_count > (page + 1) * obj_count_on_page:
        buttons.append(
            InlineKeyboardButton(
                text=UI_navigation.get_next_page_button(),
                callback_data=f'{callback_info}:{page + 1}'
            )
        )
    return buttons


def get_change_role_keyboard(user_id: int) -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    current_role = users_DB.get_role(user_id)
    for role in Role:
        if role != current_role and role != Role.ADMIN:
            keyboard_builder.add(
                InlineKeyboardButton(
                    text=role,
                    callback_data=f'user|set_role|id:{user_id}&role:{role}'
                )
            )
    return keyboard_builder.as_markup()