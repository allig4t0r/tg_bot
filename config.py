from os import environ
from logging import INFO, ERROR, DEBUG

if environ.get('BOT_MODE') == 'PROD':
    BOT_TOKEN = environ.get('BOT_TOKEN_PROD')
    BOT_FOLDER = "/opt/tg_bot" # no trailing slash
elif environ.get('SHELL') == '/bin/zsh':
    BOT_TOKEN = environ.get('BOT_TOKEN')
    BOT_FOLDER = "/Users/ag/repos/tg_bot"
else:
    BOT_TOKEN = environ.get('BOT_TOKEN')
    BOT_FOLDER = "/opt/tg_bot"

# tg_bot app
YDISK_CLIENT_ID = environ.get('YDISK_CLIENT_ID')
YDISK_CLIENT_SECRET = environ.get('YDISK_CLIENT_SECRET')
YDISK_CLIENT_TOKEN = environ.get('YDISK_CLIENT_TOKEN')

OUTLINE_API_URL = environ.get('OUTLINE_API_URL')
OUTLINE_CERT = environ.get('OUTLINE_CERT')

TRAFFIC_LIMIT = 50*1024*1024*1024
PAY_OVER_LIMIT = 100 #рублей за х1 лимита

BACKUP_FOLDER = "tg_bot"
BACKUP_FILENAME = "backup.log"

DB_FILENAME = "tg_bot.db"
DB_TABLE_STUDIOS = "studios"
DB_TABLE_GUESTS = "guests"
DB_STUDIO_KEYWORD = "Студия"
DB_STUDIO_KEYWORD_LIKE = "Студия%"
DB_OLD_STUDIO_PREFIX = "_old"
DB_OLD_STUDIOS_LIKE = "Студия%_old%"

LOG_FILENAME = 'tg_bot.log'
LOG_FORMAT = '%(asctime)s %(levelname)s: %(filename)s:%(funcName)s:%(lineno)d %(message)s'
LOG_LEVEL = DEBUG
LOG_SIZE = 5*1024*1024
LOG_FILECOUNT = 5
LOG_LINESNUM = 20