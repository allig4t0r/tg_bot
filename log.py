import config
from logging import basicConfig, getLogger, Formatter, Logger
from logging.handlers import RotatingFileHandler
from pathlib import Path

def log_init() -> Logger:
    formatter = Formatter(fmt=config.LOG_FORMAT)
    file_handler = RotatingFileHandler(filename=Path(config.LOG_PATH)/config.LOG_FILENAME, 
                                       maxBytes=config.LOG_SIZE,
                                        backupCount=config.LOG_FILECOUNT)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(config.LOG_LEVEL)
    basicConfig(level=config.LOG_LEVEL, 
                format=config.LOG_FORMAT,
                handlers=[
                    file_handler
                ]
    )
    logger = getLogger(__name__)
    return logger