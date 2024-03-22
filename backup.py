import yadisk
import config
import asyncio
from datetime import date
import logging

LOG_FORMAT = '%(asctime)s %(levelname)s %(message)s'

async def main():

    yclient = yadisk.AsyncClient(id=config.YDISK_CLIENT_ID, \
                                 secret=config.YDISK_CLIENT_SECRET, \
                                 token=config.YDISK_CLIENT_TOKEN, \
                                 session="aiohttp")

    async with yclient:
        if await yclient.check_token():
            logger.info("YDISK_CLIENT_TOKEN is good")
        else:
            logger.error("YDISK_CLIENT_TOKEN is not found or valid")
            return
        if await yclient.is_dir("/Приложения/tg_bot"):
            logger.info("CLOUD: tg_bot folder exists")
        else:
            logger.error("CLOUD: tg_bot folder does NOT exist!")
            return
        # renaming the old db backup
        try:
            await yclient.rename("/Приложения/tg_bot/tg_bot.db", \
                                f"tg_bot_{date.today().strftime('%d-%m-%Y')}.db")
            logger.info("RENAME CLOUD: tg_bot.db was successfully renamed")
        except yadisk.exceptions.PathExistsError:
            logger.warning("RENAME CLOUD: today's tg_bot.db backup already exists!")
            # return # not worth leaving
        except yadisk.exceptions.PathNotFoundError:
            logger.warning("RENAME CLOUD: tg_bot.db was not found!")
            # return # not worth it to leave now since we can do the upload
        except:
            logger.exception("RENAME CLOUD: some weird error")
        # uploading the new db backup
        try:
            await yclient.upload("tg_bot.db", "/Приложения/tg_bot/tg_bot.db")
            logger.info("CLOUD: tg_bot.db was successfully uploaded")
        except FileNotFoundError:
            logger.error("LOCAL: tg_bot.db was NOT found!")
            return
        except yadisk.exceptions.ForbiddenError:
            logger.error("CLOUD: permission denied")
            return
        except:
            logger.exception("UPLOAD: some weird error")
            return


if __name__ == '__main__':
    logging.basicConfig(filename='backup.log', level=logging.DEBUG, format=LOG_FORMAT)
    logger = logging.getLogger(__name__)
    logger.info("Backup started")
    asyncio.run(main())
    logger.info("Backup finished")
    logger.info("==========================================================================")
