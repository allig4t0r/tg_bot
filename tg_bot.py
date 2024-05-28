# -*- coding: utf-8 -*-
import asyncio
from pprint import pformat
from sys import version_info
from pathlib import Path

from aiogram import Dispatcher
from aiogram.utils.chat_action import ChatActionMiddleware
from aiogram_sqlite_storage.sqlitestore import SQLStorage

import config
from bot.handlers import bot, router
from bot.log import log_init

async def main() -> None:
    botinfo = await bot.get_me()
    logger.info(f"Bot ID: {botinfo.id}, Full Name: {botinfo.full_name}, Username: {botinfo.username}")
    fsm_storage = SQLStorage(Path(config.BOT_FOLDER)/config.DB_FILENAME, serializing_method='json')
    logger.info(f"Storage for FSM was initialized: {fsm_storage.db_path}")
    dp = Dispatcher(storage=fsm_storage)
    dp.include_router(router)
    dp.message.middleware(ChatActionMiddleware())
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == '__main__':
    logger = log_init()
    logger.info(f"Python version is: {version_info}")
    # logger.debug(f'Configuration: {pformat(config.__dict__)}')
    logger.info("tg_bot has started")
    asyncio.run(main())
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