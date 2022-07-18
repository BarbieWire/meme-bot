import threading
from loader import bot, dp
from aiogram.types import Message
from reddit import CacheData, RedditInit, GetMemes
from dotenv import load_dotenv
import os
import asyncio

load_dotenv(".env")
SECRET, ID, ADMINS = os.getenv("SECRET"), os.getenv("ID"), os.getenv("ADMIN")
_cache = CacheData()


def thread_form(chat_id, loop):
    asyncio.run_coroutine_threadsafe(
        loop=loop,
        coro=meme_posting(chat_id)
    )


async def meme_posting(chat_id: int):
    cfg = await _cache.get_user(chat_id=chat_id)

    while True:
        if cfg["active"] is False:
            break
        conn = await RedditInit(user_id=ID, secret=SECRET).connect()
        meme = await GetMemes(conn).load()
        storage = await _cache.get_storage()

        if len(storage[chat_id]) == 0 or meme[0][0] not in storage[chat_id][0]:
            if meme[0][0].endswith(".jpg") or meme[0][0].endswith(".png"):
                try:
                    channel = cfg["channel"]
                    await bot.send_message(text=F"{meme[0][1]}\n{meme[0][0]}", chat_id=channel)
                    await _cache.add_meme(meme, chat_id)

                except Exception as ex:
                    alert = F"Bot ended working with ERROR {ex}"
                    await bot.send_message(text=alert, chat_id=chat_id)
                    print(ex)

        await asyncio.sleep(cfg["between_posts"])


async def send_msg(message: Message):
    data = message.text.split()
    if len(data) < 3:
        await message.answer(text="something went wrong,\ncheck your query")
        return None

    if data[0].lower() == "start" and 1500 <= int(data[2]) <= 18001:
        try:
            await _cache.add_user(chat_id=message.from_user.id, channel=int(data[1]), active=True, time=int(data[2]))
            threading.Thread(
                target=thread_form, args=(message.from_user.id, asyncio.get_event_loop())
            ).start()
            await message.answer(text="everything went good, first post may take a several seconds")
        except Exception as _ex:
            await message.answer(text="something went wrong,\ncheck your query")
    else:
        await message.answer(text="Wrong params")


async def stop_sending(message: Message):
    data = message.text.split()
    if data[0].lower() == "stop":
        try:
            await _cache.change_status(chat_id=message.from_user.id, channel=int(data[1]))
            await message.answer(text="You successfully turned off the bot")
        except KeyError as _ex:
            await message.answer(text="something went wrong,\ncheck your query")


def register_message_handlers():
    dp.register_message_handler(send_msg, lambda x: x.text and (
            x.text.split()[0].lower() == "start"
    ))
    dp.register_message_handler(
        stop_sending, lambda x: x.text and x.text.split()[0].lower() == "stop"
    )
