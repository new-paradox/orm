# -*- coding: utf-8 -*-

import config
import psycopg2


class BaseDBSettings:
    host: str
    user: str
    password: str
    db_name: str


class DBConnectSettings(BaseDBSettings):
    def __init__(self):
        self.host = config.HOST
        self.user = config.USER
        self.password = config.PASSWORD
        self.db_name = config.DB_NAME
        self._connection = psycopg2.connect(dbname=f"{self.db_name}",
                                            user=f"{self.user}",
                                            password=f"{self.password}")
        self._cursor = self._connection.cursor()

    def __del__(self):
        self._connection.commit()
        self._connection.close()
