from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.builtin import Text

async def handle_other_text(message: types.Message):
    await message.answer(f"Нет такой команды!\nИли бот нужно перезапустить: /start")


def register_message_handler(dp: Dispatcher):
    dp.register_message_handler(handle_other_text, state="*")