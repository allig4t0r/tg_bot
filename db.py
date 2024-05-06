import config
import logging

from sqlite3 import connect, Error
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

def datetime_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()

class BotDB(object):
    def __init__(self, db_name: str = config.DB_NAME):
        self.db_name = db_name
        self.conn = None
    def __enter__(self):
        try:
            logger.info(f"DB: initializing {self.db_name}...")
            self.conn = connect(self.db_name)
            logger.debug(f"DB: {self.db_name} was successfully opened")
            self.cur = self.conn.cursor()
            self.cur.execute("CREATE TABLE IF NOT EXISTS studios"
                             "(tg_id INTEGER, key_id INTEGER PRIMARY KEY, name TEXT NOT NULL UNIQUE, "
                             "access_url TEXT, date_created TEXT)")
            self.conn.commit()
            logger.debug(f"DB: table {config.DB_TABLE_STUDIOS} was initialized")
            self.cur.execute("CREATE TABLE IF NOT EXISTS guests"
                             "(tg_id INTEGER, key_id INTEGER PRIMARY KEY, name TEXT NOT NULL UNIQUE, "
                             "access_url TEXT, date_created TEXT)")
            self.conn.commit()
            logger.debug(f"DB: table {config.DB_TABLE_GUESTS} was initialized")
            logger.info(f"DB: {self.db_name} was initialized")
            return self
        except Error as e:
            logger.exception(f"DB {self.db_name} was NOT initialized: {e}")
            return None
    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            self.conn.close()
            logger.debug(f"DB: database {self.db_name} was closed")
        else:
            logger.debug(f"DB: database {self.db_name} was NOT closed")

    def get_studios(self) -> list|None:
        try:
            studios = self.cur.execute("SELECT * FROM studios WHERE name LIKE ?", (config.DB_STUDIO_KEYWORD_LIKE,)).fetchall()
            if studios and len(studios) > 0:
                return studios
            else:
                return False
        except Error as e:
            logger.exception(f"DB: failed to get studios, {e}")

    def get_studio(self, data: int | str) -> list|None:
        if type(data) == int:
            try:
                studios = self.cur.execute("SELECT * FROM studios WHERE tg_id LIKE ?", (data,)).fetchall()
                if studios and len(studios) > 0:
                    return studios
                else:
                    return False
            except Error as e:
                logger.exception(f"DB: failed to get studio with tg_id {data}, {e}")
        elif type(data) == str:
            try:
                studios = self.cur.execute("SELECT * FROM studios WHERE name LIKE ?", (data,)).fetchone()
                if studios and len(studios) > 0:
                    return studios
                else:
                    return False
            except Error as e:
                logger.exception(f"DB: failed to get studio with name {data}, {e}")

    def create_studio(self, tg_id: int, key_id: int, name: str, access_url: str) -> bool:
        try:
            query = self.cur.execute("SELECT * FROM studios WHERE name LIKE ?", (name,)).fetchone()
            if query and len(query) > 0:
                logger.warning(f"DB: studio {name} already exists!")
                return False
            else:
                try:
                    self.cur.execute("INSERT INTO studios VALUES "
                                     "(?, ?, ?, ?, ?)", (tg_id, key_id, name, access_url, datetime_now()))
                    self.conn.commit()
                    logger.info(f"DB: studio {name} was created successfully")
                    return True
                except Error as e:
                    logger.exception(f"DB: failed to create new studio {name}, {e}")
                    return False
        except Error as e:
            logger.exception(f"DB: failed to check if studio {name} exists, {e}")
            return False
        
    def delete_studio(self, data: int| str) -> bool:
        if type(data) == int:
            try:
                self.cur.execute("DELETE FROM studios WHERE key_id LIKE ?", (data,)).fetchone()
                self.conn.commit()
                logger.info(f"DB: studio with key_id {data} was successfully deleted")
                return True
            except Error as e:
                logger.exception(f"DB: failed to delete studio with key_id {data}, {e}")
                return False
        elif type(data) == str:
            try:
                self.cur.execute("DELETE FROM studios WHERE name LIKE ?", (data,)).fetchone()
                self.conn.commit()
                logger.info(f"DB: studio with name {data} was successfully deleted")
                return True
            except Error as e:
                logger.exception(f"DB: failed to delete studio with name {data}, {e}")
                return False
        
    def get_key(self, tg_id: int):
        try:
            studios = self.cur.execute("SELECT tg_id, name, access_url FROM studios WHERE tg_id LIKE ?", (tg_id,)).fetchall()
            if studios and len(studios) > 0:
                return studios
            else:
                return False
        except Error as e:
            logger.exception(f"DB: failed to get key/keys for tg_id {tg_id}, {e}")
