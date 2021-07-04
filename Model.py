from typing import Any, Dict

import config
import psycopg2


class BaseDBSettings:
    host: str
    user: str
    password: str
    db_name: str


class DBConfigSettings(BaseDBSettings):
    def __init__(self):
        self.host = config.HOST
        self.user = config.USER
        self.password = config.PASSWORD
        self.db_name = config.DB_NAME


class Driver:
    def __init__(self, db_setting: DBConfigSettings):
        self.setting = db_setting
        self.connection = psycopg2.connect(
            f"dbname={self.setting.db_name} user={self.setting.user} password={self.setting.password}")
        self.__cursor = self.connection.cursor()

    def __del__(self, instance):
        self.connection.close()


class Model:

    def __init__(self, db_driver: Driver):
        self.__cursor = db_driver.connection.cursor()

    id: int
    __TABLE_NAME = str

    def create(self, **args) -> Dict:
        data_array = []
        print(args)
        keys = ', '.join([key for key in args.keys()])
        values = ', '.join([str(val) for val in args.values()])
        query = f"INSERT INTO {config.DB_NAME}.{self.__TABLE_NAME} {keys} VALUES "
        data_array.append(f"{values}")
        sql_query = query + ", ".join(data_array) + ';'
        return self.__cursor.execute(sql_query)

    def read(self, **kvargs) -> Dict:
        key, value = kvargs
        data_array = []
        query = f"SELECT * FROM {config.DB_NAME}.{self.__TABLE_NAME} WHERE {key} = {value};"
        return self.__cursor.execute(query)

    def update(self):
        pass

    def delete(self):
        pass

    def create_table(self):
        pass

    def delete_table(self):
        pass

    def alter_table(self):
        pass
