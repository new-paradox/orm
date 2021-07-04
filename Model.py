from typing import Any, Dict
import random

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


class Driver(DBConfigSettings):
    def __init__(self):
        super().__init__()
        self.connection = psycopg2.connect(
            f"dbname={self.db_name} user={self.user} password={self.password}")
        self.__cursor = self.connection.cursor()

    def __del__(self, instance):
        self.connection.close()


class Model(Driver):
    _table: str

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    def create(self, *args) -> Dict:
        data_array = []

        # keys = ', '.join([key for key in args])
        # values = ', '.join([val for val in self])
        a4 = ("Model.__dict__:", self.__dict__)
        values = 'bar'
        query = f"INSERT INTO {config.DB_NAME}.{self._table} {args} VALUES "
        # data_array.append(f"{values}")
        sql_query = query + ", ".join(data_array) + ';'
        # print(sql_query)
        return self.__cursor.execute(sql_query)

    # def read(self, **kvargs) -> Dict:
    #     key, value = kvargs
    #     data_array = []
    #     query = f"SELECT * FROM {config.DB_NAME}.{self.__table} WHERE {key} = {value};"
    #     return self.__cursor.execute(query)

    # def update(self):
    #     pass
    #
    # def delete(self):
    #     pass
    #
    # def create_table(self):
    #     pass
    #
    # def delete_table(self):
    #     pass
    #
    # def alter_table(self):
    #     pass
