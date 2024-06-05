# -*- coding: utf-8 -*-
import asyncio
from pprint import pformat
from sys import version_info
from pathlib import Path
from aiohttp import web

from aiogram import Dispatcher, Bot
from aiogram.utils.chat_action import ChatActionMiddleware
from aiogram_sqlite_storage.sqlitestore import SQLStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

import config
from bot.handlers import bot, router
from bot.log import log_init

async def on_startup(bot: Bot) -> None:
    botinfo = await bot.get_me()
    logger.info(f"Bot ID: {botinfo.id}, Full Name: {botinfo.full_name}, Username: {botinfo.username}")
    await bot.set_webhook(f"{config.WEBHOOK_URL}{config.WEBHOOK_PATH}",
                          secret_token=config.WEBHOOK_SECRET,
                          drop_pending_updates=True,
                          max_connections=20)
    webhook_info = await bot.get_webhook_info()
    logger.info(f"WEBHOOK: {webhook_info}")

def main() -> None:
    fsm_storage = SQLStorage(Path(config.BOT_FOLDER)/config.DB_FILENAME, serializing_method='json')
    logger.info(f"Storage for FSM was initialized: {fsm_storage.db_path}")
    dp = Dispatcher(storage=fsm_storage)
    dp.include_router(router)
    dp.message.middleware(ChatActionMiddleware())
    # await bot.delete_webhook(drop_pending_updates=True)
    # await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    dp.startup.register(on_startup)
    app = web.Application()
    webhook_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=config.WEBHOOK_SECRET
    )
    webhook_handler.register(app, path=config.WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)
    web.run_app(app, host=config.WEBHOOK_SERVER_HOST, port=config.WEBHOOK_SERVER_PORT)

if __name__ == '__main__':
    logger = log_init()
    logger.info(f"Python version is: {version_info}")
    # logger.debug(f'Configuration: {pformat(config.__dict__)}')
    logger.info("tg_bot has started")
    main()
    logger.info("tg_bot has stopped")
    logger.info("==========================================================================")

# на случай отмирания бота внутри мейна
# while True:
#     try:
#         if __name__ == '__main__':
#             asyncio.run(main())
#     except Exception as e:
#         time.sleep(3)
#         logger.exception(e)
#         time.sleep(3)