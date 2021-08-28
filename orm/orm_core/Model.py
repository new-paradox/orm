# -*- coding: utf-8 -*-
from orm.orm_core.sql_connect import AutoDBConfigManager

DRIVER = AutoDBConfigManager()


class Model:
    """
    Model имеет CRUD методы взаимодействия с MySQL, SQLite и PostgreSQL;
    От этого объекта наследуются модели таблиц, в которых уже описываются их поля;
    :param keys: -> List Используется для create операций, получает имена столбцов таблицы;
    :param Values: -> List Используется для create операций, получает значения столбцов таблицы;
    :param condition: Используется для read/update/delete операций;
    :param set_update: Используется для update операции хранит условие для ихменения типа колонок таблицы;

    :method read_by_one_id: SELECT запрос с прокидыванием id искомой строки;
    :method make_query: создание запроса из терминала;
    """
    _table_name = str
    _row = {}

    condition = None
    set_update = None
    _cursor = DRIVER.connection.cursor()

    def __setitem__(self, key, value):
        self._row[key] = value

    def create(self):
        keys = []
        values = []
        for key, value in self._row.items():
            keys.append(key)
            values.append(value)
        prepare_key = f"({', '.join(keys)})"
        prepare_values = str(tuple(values))
        query = f"INSERT INTO {self._table_name.lower()} {prepare_key} VALUES {prepare_values};"
        print(query)
        return self._cursor.execute(query)

    def read(self):
        query = f"SELECT * FROM {self._table_name.lower()}"
        if self.condition:
            query += f" WHERE {self.condition}"
        self._cursor.execute(query + ";")
        print(query)
        return self._cursor.fetchall()

    def read_by_one_id(self, model_id):
        query = f"SELECT * FROM {self._table_name.lower()}" \
                f" WHERE {self._table_name.lower()}.id = {model_id};"
        self._cursor.execute(query)
        print(query)
        return self._cursor.fetchone()

    def update(self):
        query = f" UPDATE {self._table_name.lower()}" \
                f" SET {self.set_update}" \
                f" WHERE {self.condition};"
        print(query)
        return self._cursor.execute(query)

    def delete(self):
        query = f" DELETE FROM {self._table_name.lower()}" \
                f" WHERE {self.condition};"
        print(query)
        return self._cursor.execute(query)

    def make_query(self, query):
        print(query)
        self._cursor.execute(query)
        return self._cursor.fetchall()
