import re

from aiogram import Router, F
from aiogram.types import CallbackQuery

from database.users_db import UsersDB, Role

from UI.menu import UI_users_page
from UI.commands import UI_commands

import handlers.keyboards as keyboards
from decorators import delete_callback_message, is_user_role_admin
from bot import bot


router = Router()
users_DB = UsersDB()
users_count_on_page = 20


@router.callback_query(F.data.regexp(r'users\|show\|page:(\d+)'))
@delete_callback_message
@is_user_role_admin
async def show_users(callback: CallbackQuery):
    match = re.match(r'users\|show\|page:(\d+)', callback.data)
    page = int(match.group(1))
    users = users_DB.get_users(users_count_on_page, page * users_count_on_page)
    all_users_count = users_DB.get_users_count()

    await bot.send_message(callback.from_user.id, UI_users_page.get_users_text(users), parse_mode='HTML', 
                           reply_markup=keyboards.get_pagination_keyboard(page, 'users|show|', 
                           users_count_on_page, all_users_count))

@router.callback_query(F.data.regexp(r'users\|show_couriers\|page:(\d+)'))
@delete_callback_message
@is_user_role_admin
async def show_courier_users(callback: CallbackQuery):
    match = re.match(r'users\|show_couriers\|page:(\d+)', callback.data)
    page = int(match.group(1))
    users = users_DB.get_users_by_role(Role.COURIER, users_count_on_page, page * users_count_on_page)
    all_couriers_users_count = users_DB.get_users_by_role_count(Role.COURIER)
    await bot.send_message(callback.from_user.id, UI_users_page.get_couriers_text(users), parse_mode='HTML',
                           reply_markup=keyboards.get_pagination_keyboard(page, 'users|show_couriers|', 
                           users_count_on_page, all_couriers_users_count))

@router.callback_query(F.data.regexp(r'users\|show_managers\|page:(\d+)'))
@delete_callback_message
@is_user_role_admin
async def show_manager_users(callback: CallbackQuery):
    match = re.match(r'users\|show_managers\|page:(\d+)', callback.data)
    page = int(match.group(1))
    users = users_DB.get_users_by_role(Role.MANAGER, users_count_on_page, page * users_count_on_page)
    all_managers_users_count = users_DB.get_users_by_role_count(Role.MANAGER)
    await bot.send_message(callback.from_user.id, UI_users_page.get_managers_text(users), parse_mode='HTML',
                           reply_markup=keyboards.get_pagination_keyboard(page, 'users|show_managers|', 
                           users_count_on_page, all_managers_users_count))

@router.callback_query(F.data.regexp(r'user\|set_role\|id:(\d+)&role:(.+)'))
@delete_callback_message
@is_user_role_admin
async def user_set_role(callback:CallbackQuery):
    match = re.match(r'user\|set_role\|id:(\d+)&role:(.+)', callback.data)
    user_id = int(match.group(1))
    role = Role(match.group(2))
    username, old_role = users_DB.get_user(user_id)
    users_DB.set_role(user_id, role)

    admin_username = users_DB.get_username(callback.from_user.id)
    for admin_id, _, _ in users_DB.get_admins():
        if callback.from_user.id == admin_id:
            await callback.message.answer(UI_commands.get_change_role_message_for_admin(username, old_role, role), 
                                          reply_markup=keyboards.get_change_role_keyboard(user_id))
        else:
            await bot.send_message(admin_id, UI_commands.get_change_role_message_for_other_admins(admin_username, username, old_role, role))
    await bot.send_message(user_id, UI_commands.get_change_role_message_for_user(role))