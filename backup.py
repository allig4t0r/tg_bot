import yadisk
import config
import asyncio
from datetime import date
import logging
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
        if await yclient.is_dir(f"/Приложения/{config.DB_FOLDER}"):
            logger.info(f"CLOUD: {config.DB_FOLDER} folder exists")
        else:
            logger.error(f"CLOUD: {config.DB_FOLDER} folder does NOT exist!")
            return
        # renaming the old db backup
        try:
            await yclient.rename(f"/Приложения/{config.DB_FOLDER}/{config.DB_NAME}", \
                                f"{config.DB_FOLDER}_{date.today().strftime('%d-%m-%Y')}.db")
            logger.info(f"RENAME CLOUD: {config.DB_NAME} was successfully renamed")
        except yadisk.exceptions.PathExistsError:
            logger.warning(f"RENAME CLOUD: today's {config.DB_NAME} backup already exists!")
            # return # not worth leaving
        except yadisk.exceptions.PathNotFoundError:
            logger.warning(f"RENAME CLOUD: {config.DB_NAME} was not found!")
            # return # not worth it to leave now since we can do the upload
        except:
            logger.exception("RENAME CLOUD: some weird error")
        # uploading the new db backup
        try:
            await yclient.upload(f"{config.DB_NAME}", f"/Приложения/{config.DB_FOLDER}/{config.DB_NAME}")
            logger.info(f"CLOUD: {config.DB_NAME} was successfully uploaded")
        except FileNotFoundError:
            logger.error(f"LOCAL: {config.DB_NAME} was NOT found!")
            return
        except yadisk.exceptions.ForbiddenError:
            logger.error("CLOUD: permission denied")
            return
        except:
            logger.exception("UPLOAD: some weird error")
            return


if __name__ == '__main__':
    logging.basicConfig(filename='backup.log', level=logging.DEBUG, format=config.LOG_FORMAT)
    logger = logging.getLogger(__name__)
    logger.info("Backup started")
    asyncio.run(main())
    logger.info("Backup finished")
    logger.info("==========================================================================")
