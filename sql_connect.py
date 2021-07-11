# -*- coding: utf-8 -*-

import config
from dataclasses import dataclass
import psycopg2
from mysql import connector


@dataclass
class BaseDBConfig:
    host: str
    user: str
    db_driver: str


@dataclass
class MySQLDBConfig(BaseDBConfig):
    """
    Настраивается индивидаульно под необходимые поля для db;
    """
    password: str
    database: str


@dataclass
class PSQLDBConfig(BaseDBConfig):
    """
    Настраивается индивидаульно под необходимые поля для db;
    """
    password: str
    database: str


class AutoDBConfigManager(BaseDBConfig):
    """
    Класс-контроллер:
    Смотрит config, на основе данных выбирает драйвер;
    """

    def __init__(self):
        self.db_driver = config.DB_DRIVER
        self.host = config.HOST
        self.user = config.USER
        # TODO: вынести драйвера в отдельные классы;
        if self.db_driver.lower() == 'psql':
            self.db_config = PSQLDBConfig(host=self.host,
                                          user=self.user,
                                          db_driver=self.db_driver,
                                          password=config.PASSWORD,
                                          database=config.DATABASE
                                          )

            self._connection = psycopg2.connect(dbname=f"{self.db_config.database}",
                                                user=f"{self.db_config.user}",
                                                password=f"{self.db_config.password}")
            self._cursor = self._connection.cursor()
        if self.db_driver.lower() == 'mysql':
            self.db_config = MySQLDBConfig(host=self.host,
                                           user=self.user,
                                           db_driver=self.db_driver,
                                           password=config.PASSWORD,
                                           database=config.DATABASE
                                           )
            # TODO: узнать, как коннектиться к мускулу
            self._connection = connector.connect(db=f"{self.db_config.database}",
                                                 user=f"{self.db_config.user}",
                                                 password=f"{self.db_config.password}")
            self._cursor = self._connection.cursor()
