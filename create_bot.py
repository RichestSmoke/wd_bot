from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from dotenv import load_dotenv, find_dotenv
import os


class MenuStates(StatesGroup):
    MAIN_MENU = State()
    MENU_BUY = State()
    MENU_BUY_HOUSE = State()
    MENU_RENT = State()
    GET_CONTACT_RENT_HOUSE = State()
    GET_CONTACT_RENT_COMMERS = State()
    GET_CONTACT_RENT_LAND = State()
    GET_CONTACT_BUY_COMMERS = State()
    GET_CONTACT_BUY_LAND = State()
    GET_CONTACT_BUY_HOUSE_NEW = State()
    GET_CONTACT_BUY_HOUSE_OLD = State()
    GET_CONTACT_INTERNATIONAL = State()


load_dotenv(find_dotenv())
bot = Bot(os.getenv("TELEGRAM_TOKEN"), parse_mode='HTML')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())


