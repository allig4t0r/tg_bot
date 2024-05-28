import logging
from datetime import date
from pathlib import Path

import yadisk
import asyncio

import config


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
        if await yclient.is_dir(f"/Приложения/{config.BACKUP_FOLDER}"):
            logger.info(f"CLOUD: {config.BACKUP_FOLDER} folder exists")
        else:
            logger.error(f"CLOUD: {config.BACKUP_FOLDER} folder does NOT exist!")
            return
        # renaming the old db backup
        try:
            await yclient.rename(f"/Приложения/{config.BACKUP_FOLDER}/{config.DB_FILENAME}", \
                                f"{config.BACKUP_FOLDER}_{date.today().strftime('%d-%m-%Y')}.db")
            logger.info(f"RENAME CLOUD: {config.DB_FILENAME} was successfully renamed")
        except yadisk.exceptions.PathExistsError:
            logger.warning(f"RENAME CLOUD: today's {config.DB_FILENAME} backup already exists!")
            # return # not worth leaving
        except yadisk.exceptions.PathNotFoundError:
            logger.warning(f"RENAME CLOUD: {config.DB_FILENAME} was not found!")
            # return # not worth it to leave now since we can do the upload
        except Exception as e:
            logger.exception(f"RENAME CLOUD: some weird error, {e}")
        # uploading the new db backup
        try:
            await yclient.upload(f"{Path(config.BOT_FOLDER)/config.DB_FILENAME}",
                                 f"/Приложения/{config.BACKUP_FOLDER}/{config.DB_FILENAME}")
            logger.info(f"CLOUD: {config.DB_FILENAME} was successfully uploaded")
        except FileNotFoundError:
            logger.error(f"LOCAL: {config.DB_FILENAME} was NOT found!")
            return
        except yadisk.exceptions.ForbiddenError:
            logger.error("CLOUD: permission denied")
            return
        except Exception as e:
            logger.exception(f"UPLOAD: some weird error, {e}")
            return


if __name__ == '__main__':
    logging.basicConfig(filename=Path(config.BOT_FOLDER)/config.BACKUP_FILENAME,
                        level=logging.DEBUG,
                        format=config.LOG_FORMAT)
    logger = logging.getLogger(__name__)
    logger.info("Backup started")
    asyncio.run(main())
    logger.info("Backup finished")
    logger.info("==========================================================================")
