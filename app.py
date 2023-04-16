from aiogram import executor
from aiogram.utils.executor import start_webhook, set_webhook
import logging
from aiogram.contrib.middlewares.logging import LoggingMiddleware
import db
from loader import dp
from db import engine, Base
import routes

# from utils.notify_admins import on_startup_notify

from utils.misc.set_bot_commands import set_default_commands

dp.middleware.setup(LoggingMiddleware())


async def init_tables():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def on_startup(dp):
    # await bot_tg.bot.set_webhook('https://9f3c-82-215-97-98.eu.ngrok.io')
    await set_default_commands(dp)
    print('bot online')
    await routes.handlers_uz_kir()
    await routes.handlers_uz()
    await routes.handlers_ru()
    routes.lang_change_handler()
    routes.handlers_settings_changes()

    await init_tables()

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
# if __name__ == '__main__':
#
#     start_webhook(
#         dispatcher=dp,
#         webhook_path='/',
#         on_startup=on_startup,
#
#         # on_shutdown=on_shutdown,
#         skip_updates=True,
#         host='127.0.0.1',
#         port=9000,
#     )