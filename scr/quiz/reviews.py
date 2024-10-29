import sqlite3
import os
from scr.config.logs import logger


class DataBase:
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(DataBase, cls).__new__(cls)
        return cls.instance

    def __init__(self, path: str = 'review'):
        self.cur = None
        self.__connect = sqlite3.connect(os.path.realpath('..//' + path + '.db'))

    @property
    def connect(self):
        return self.__connect

    def update_reviews(self, param: tuple):
        try:
            with self.connect:
                count_param = '?,' * len(param)
                print(*param)
                self.cur = self.connect.cursor()
                self.cur.execute(f"""INSERT INTO reviews (User_first_name,
                 User_last_name) VALUES({count_param[:-1]})""", param)
        except Exception as e:
            logger.exception(e)

