from aiogram import  types, Dispatcher, Bot
from create_bot import dp, bot
from data_base import sqlite_db

import logging
import os
from fastapi import FastAPI
from handlers import client, admin, other
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

client.register_message_handler(dp)
admin.register_message_handler(dp)
other.register_message_handler(dp)

load_dotenv()
TG_API_TOKEN = os.getenv('TELEGRAM_TOKEN')
WEBHOOK_PATH = f"/{TG_API_TOKEN}"
NGINX_HOST = os.getenv('NGINX_HOST')
WEBHOOK_URL = f"{NGINX_HOST}{WEBHOOK_PATH}"
print(NGINX_HOST)
print(WEBHOOK_URL)

app = FastAPI()

@app.on_event('startup')
async def on_startup():
    sqlite_db.sql_start()
    await bot.delete_webhook(drop_pending_updates=True)
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(WEBHOOK_URL)


@app.post(WEBHOOK_PATH)
async def bot_webhook(update: dict):
    telegram_update = types.Update(**update)
    Dispatcher.set_current(dp)
    Bot.set_current(bot)
    await dp.process_update(telegram_update)


@app.on_event('shutdown')
async def on_shutdown():
    await bot.session.close()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8443)

 

# REAL_ESTATE/
#   |- main.py
#   |- create_bot.py
#   |- config.py
#   |- .env
#   |- .gitignore
#   |- requirements.txt
#   |- od_eastate.jpeg
#   |- data_base/
#   |   |- __init__.py
#   |   |- sqlite_db.py
#   |- handlers/
#   |   |- __init__.py
#   |   |- admin.py
#   |   |- client.py
#   |   |- other.py
#   |- keyboards/
#   |   |- __init__.py
#   |   |- admin_kb.py
#   |   |- client_kb.py
