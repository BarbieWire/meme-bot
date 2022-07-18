from aiogram import Dispatcher
from dotenv import load_dotenv
import os
from loader import bot

load_dotenv(".env")
ADMINS = [os.getenv("ADMIN")]


async def startup(dp: Dispatcher):
    for admin in ADMINS:
        await bot.send_message(text="Bot just started!", chat_id=admin)


async def shutdown(dp: Dispatcher):
    for admin in ADMINS:
        await bot.send_message(text="Bot finished work", chat_id=admin)
