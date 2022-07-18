from aiogram import Dispatcher, Bot
import os
from dotenv import load_dotenv


load_dotenv(".env")
TOKEN = os.getenv("TOKEN")

bot = Bot(TOKEN)
dp = Dispatcher(bot=bot)
