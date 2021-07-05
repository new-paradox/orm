from typing import Any, Dict
import random

import config
import psycopg2


# TODO: BaseDBSettings & DBConfigSettings в датаклассы
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
    _Property: object
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    def __setitem__(self, key, value):
        pass

    def create(self):
        values = []
        args = [key for key in dir(self._Property)
                if not key.startswith('__')
                and not callable(getattr(self._Property, key))
                ]
        for i in args:
            values.append(getattr(self._Property, i))
        prepare_key = f"({', '.join(args)})"
        prepare_values = tuple(values)
        query = f"INSERT INTO {config.DB_NAME}.{self._table} {prepare_key} VALUES {prepare_values};"
        print(query)
        return self.__cursor.execute(query)

# INSERT INTO greetings(gname) VALUES('{hello}')
# cur.execute(sql, ("{{{}}}".format(line.rstrip()),))


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
