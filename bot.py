import logging
import sys
from pathlib import Path
from os import getenv
from dotenv import load_dotenv
import pytz
from datetime import datetime

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode


load_dotenv()
TOKEN = getenv("BOT_TOKEN")
DATE_TIME_FORMAT = getenv('DATE_TIME_FORMAT')
DATE_FORMAT_VISIBLE = getenv('DATE_FORMAT_VISIBLE')
DATE_TIME_FORMAT_VISIBLE = getenv('DATE_TIME_FORMAT_VISIBLE')
TIMEZONE = pytz.timezone(getenv('TIMEZONE'))
TEMP_PATH = Path('temp')
TEMP_PATH.mkdir(exist_ok=True)
CURRENCY = getenv('CURRENCY')
MEMORY_DIMENSION = getenv('MEMORY_DIMENSION')
SETTINGS_PATH = Path('settings')

if not SETTINGS_PATH.exists():
    SETTINGS_PATH.mkdir()

logging_level = getattr(
    logging, getenv('LOGGING_LEVEL').upper(), logging.INFO
)
logging.basicConfig(level=logging_level, stream=sys.stdout)

dp = Dispatcher()
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


def get_backup_name() -> str:
    return (
        TEMP_PATH
        / f"backup_{datetime.now(TIMEZONE).replace(microsecond=0).strftime(DATE_TIME_FORMAT)}.db"
    )


def format_money(money: float) -> str:
    return '-' if not money else f"{money:.2f}"