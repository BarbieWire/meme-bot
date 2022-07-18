from aiogram.types import Message
from loader import dp


async def _help(message: Message):
    greetings = f"Hi {message.from_user.username}!\n" \
                f"I was developed by *t.me/barbiewire*\n" \
                f"If you want to variegate your telegram channel or just have fun I'm your best option\n" \

    options = f"For one user at the same time only one thread (channel) available\n" \
              f"To start work with me:\n" \
              f"1. Add me to your channel and promote role to admin\n" \
              f"2. To start: form a query starts with 'start' and with params _channel_ / _time in seconds_, " \
              f"example: start -123123 1500\n" \
              f"3.To end polling start with 'stop' word and param *channel*, example: stop -123123"

    await message.answer(text=greetings, parse_mode="Markdown")
    await message.answer(text=options, parse_mode="Markdown")


def comm_reg():
    dp.register_message_handler(_help, commands=["help"])
