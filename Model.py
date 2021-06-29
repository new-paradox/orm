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


class Model:

    def __init__(self, db_settings: BaseDBSettings):
        self._settings = db_settings
        self._connection = psycopg2.connect(dbname=f"{self._settings.db_name}",
                                            user=f"{self._settings.user}",
                                            password=f"{self._settings.password}")
        self.__cursor = self._connection.cursor()

    def close_connection(self):
        self._connection.close()

    id: int
    __TABLE_NAME = str

    def create(self, **kvargs) -> Dict:
        data_array = []
        query = f"INSERT INTO {config.DB_NAME}.{self.__TABLE_NAME} SET "
        for key, value in kvargs:
            data_array.append(f"{key} = '{value}'")
        sql_query = query + ", ".join(data_array)
        """Почитай про подготовленные выражения в Postgres"""
        return self.__cursor.execute(sql_query)

    def read(self):
        query = f"SELECT * FROM {config.DB_NAME}.{self.__TABLE_NAME} BY id = '{self.id}' "

    def update(self):
        pass

    def delete(self):
        pass

    def create_table(self):
        pass
