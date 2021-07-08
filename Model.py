# -*- coding: utf-8 -*-

from typing import Optional

from psql_connect import DBConnectSettings


class Singleton(type):
    _instances = {}
    _table_name = str

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Model(DBConnectSettings, metaclass=Singleton):
    keys = []
    Values = []
    condition = None

    def __setitem__(self, key, value):
        self.keys.append(key)
        self.Values.append(value)

    def create(self):
        prepare_key = f"({', '.join(self.keys)})"
        prepare_values = str(tuple(self.Values))
        query = f"INSERT INTO {self._table_name.lower()} {prepare_key} VALUES {prepare_values};"
        return self._cursor.execute(query)

    def read(self):
        query = f"SELECT * FROM {self._table_name.lower()}"
        if self.condition:
            query += f" WHERE {self.condition}"
        self._cursor.execute(query + ";")
        return self._cursor.fetchall()

    def update(self):
        pass

    def delete(self):
        pass
