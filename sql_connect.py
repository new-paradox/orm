# -*- coding: utf-8 -*-
import pymysql
import config
from dataclasses import dataclass
import psycopg2


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


class PostgreSQLDB:
    class_name = 'psql'

    def __init__(self, host, user, db_driver):
        self.host = host
        self.user = user
        self.db_driver = db_driver
        self.db_config = PSQLDBConfig(host=self.host,
                                      user=self.user,
                                      db_driver=self.db_driver,
                                      password=config.PASSWORD,
                                      database=config.DATABASE
                                      )

    def get_connection(self):
        _connection = psycopg2.connect(dbname=f"{self.db_config.database}",
                                       user=f"{self.db_config.user}",
                                       password=f"{self.db_config.password}")
        return _connection


class MysqlDB:
    class_name = 'mysql'

    def __init__(self, host, user, db_driver):
        self.host = host
        self.user = user
        self.db_driver = db_driver
        self.db_config = MySQLDBConfig(host=self.host,
                                       user=self.user,
                                       db_driver=self.db_driver,
                                       password=config.PASSWORD,
                                       database=config.DATABASE
                                       )

    def get_connection(self):
        _connection = pymysql.connect(host=self.db_config.host,
                                      user=self.db_config.user,
                                      password=self.db_config.password,
                                      database=self.db_config.database)
        return _connection


class AutoDBConfigManager(BaseDBConfig):
    """
    Класс-контроллер:
    Смотрит config, на основе данных выбирает драйвер;
    """

    def __init__(self):
        self.db_driver = config.DB_DRIVER
        self.host = config.HOST
        self.user = config.USER
        try:
            if self.db_driver.lower() == PostgreSQLDB.class_name:
                self._connection = PostgreSQLDB(host=self.host,
                                                user=self.user,
                                                db_driver=self.db_driver).get_connection()
                self._cursor = self._connection.cursor()
        except psycopg2.Error as err:
            print(f'Error from psql controller {err}')
        try:
            if self.db_driver.lower() == MysqlDB.class_name:
                self._connection = MysqlDB(host=self.host,
                                           user=self.user,
                                           db_driver=self.db_driver).get_connection()
                self._cursor = self._connection.cursor()

        except pymysql.Error as err:
            print(f'Error from psql controller {err}')
