from logging import INFO, ERROR, DEBUG


BOT_TOKEN = 'int:string'
# tg_bot app
YDISK_CLIENT_ID = ''
YDISK_CLIENT_SECRET = ''
YDISK_CLIENT_TOKEN = ''

OUTLINE_API_URL = 'https://ip:port/string'
OUTLINE_CERT = ''

TRAFFIC_LIMIT = 50*1024*1024*1024
PAY_OVER_LIMIT = 1000 #рублей за х1 лимита

DB_FOLDER = "tg_bot"
DB_NAME = "tg_bot.db"
DB_TABLE_STUDIOS = "studios"
DB_TABLE_GUESTS = "guests"
DB_STUDIO_KEYWORD = "Студия"
DB_STUDIO_KEYWORD_LIKE = "Студия%"
DB_OLD_STUDIO_PREFIX = "_old"
DB_OLD_STUDIOS_LIKE = "Студия%_old%"

LOG_FILENAME = 'tg_bot.log'
LOG_PATH = '.'
LOG_FORMAT = '%(asctime)s %(levelname)s: %(filename)s:%(funcName)s:%(lineno)d %(message)s'
LOG_LEVEL = DEBUG
LOG_SIZE = 5*1024*1024
LOG_FILECOUNT = 5
LOG_LINESNUM = 20