import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from database.users_db import UsersDB
from database.orders.statuses_db import StatusesDB

from handlers import commands, menu, users
from handlers.orders.phones import add_phone, change_phone, phones
from handlers.admin_menu import models_menu, colors_menu, defects_menu, memories_menu
from handlers.commands import get_backup

from bot import dp, bot, TIMEZONE


users_DB = UsersDB()
statuses_DB = StatusesDB()


async def send_backup_to_admins():
    admins = users_DB.get_admins()
    file, message = await get_backup()
    for telegram_id, _, _ in admins:
        await bot.send_document(telegram_id, document=file, caption=message, parse_mode='HTML')


scheduler = AsyncIOScheduler(timezone=TIMEZONE)
scheduler.add_job(send_backup_to_admins, 'cron', hour=23, minute=59)


async def main() -> None:
    dp.include_routers(
        commands.router,
        menu.router,
        users.router,
        add_phone.router,
        change_phone.router,
        phones.router,
        models_menu.router,
        colors_menu.router,
        defects_menu.router,
        memories_menu.router
    )
    scheduler.start()
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
    except Exception as e:
        print(e)
