from loader import dp
from aiogram import executor
from notify import startup, shutdown
from handlers.message import register_message_handlers
from handlers.commands import comm_reg

register_message_handlers()
comm_reg()


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, on_startup=startup, on_shutdown=shutdown)
