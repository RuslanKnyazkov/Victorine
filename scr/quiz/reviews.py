import sqlite3
import os

class DataBase:
    instance = None

    setting = {
        "name": ['user', 'review', 'result_quiz'],
        'column': [['user_id Integer', 'user_first_name Text', 'user_last_name Text'],
                   ['user_id Integer', 'user_first_name Text', 'user_last_name Text', 'review_text'],
                   ['user_id Integer', 'user_first_name Text', 'user_last_name Text', 'result_quiz']]
    }

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(DataBase, cls).__new__(cls)
        return cls.instance

    def __init__(self, path: str = 'APP_database'):

        self.__connect = sqlite3.connect(os.path.realpath('..//' + path + '.db'))
        self.__cur = self.connect.cursor()

        for i in range(len(self.setting['name'])):
            with self.connect:
                sql_request = self.connect.cursor()
                fields = ','.join([field for field in self.setting['column'][i]])
                sql_request.execute(f"""CREATE TABLE IF NOT EXISTS {self.setting['name'][i]}({fields})""")

    @property
    def connect(self):
        return self.__connect

    @property
    def cursor(self):
        return self.__cur


if __name__ == '__main__':
    test = DataBase()
