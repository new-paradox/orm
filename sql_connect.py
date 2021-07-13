# -*- coding: utf-8 -*-
import pymysql
import config
from dataclasses import dataclass
import psycopg2
from enum import Enum


@dataclass
class BaseDBConfig:
    """
    Стандартные настройки для соединения с db;
    """
    host: str
    user: str
    db_driver: str
    password: str
    database: str


@dataclass
class MySQLDBConfig(BaseDBConfig):
    """
    Настраивается индивидаульно под db;
    """
    password: str
    database: str


@dataclass
class PSQLDBConfig(BaseDBConfig):
    """
    Настраивается индивидаульно под db;
    """
    password: str
    database: str


class PostgreSQLDB(PSQLDBConfig):
    """
    Инициализирует соединение с PostgreSQL;
    """
    def __init__(self, database, user, password):
        self.database = database
        self.password = password
        self.user = user
        self._connection = psycopg2.connect(dbname=f"{self.database}",
                                            user=f"{self.user}",
                                            password=f"{self.password}")

    def get_connection(self):
        return self._connection


class MysqlDB(MySQLDBConfig):
    """
    Инициализирует соединение с MySQL;
    """
    def __init__(self, host, user, password, database):
        self.database = database
        self.password = password
        self.user = user
        self.host = host
        self._connection = pymysql.connect(host=self.host,
                                           user=self.user,
                                           password=self.password,
                                           database=self.database)

    def get_connection(self):
        return self._connection


class DBDrivers(Enum):
    """
    Хранит имена объектов, инициализирующих соединение с db;
    """
    PostgreSQLDB = 'psql'
    MysqlDB = 'mysql'


class AutoDBConfigManager(BaseDBConfig):
    """
    Смотрит config.py -> выбирает db для соединения;
    """
    def __init__(self):
        try:
            self.db_driver = DBDrivers(config.DB_DRIVER).name
            self.host = config.HOST
            self.user = config.USER
            self.password = config.PASSWORD
            self.database = config.DATABASE
            if self.db_driver == PostgreSQLDB.__name__:
                self._connection = PostgreSQLDB(database=self.database,
                                                user=self.user,
                                                password=self.password).get_connection()

            if self.db_driver == MysqlDB.__name__:
                self._connection = MysqlDB(host=self.host,
                                           user=self.user,
                                           password=self.password,
                                           database=self.database).get_connection()
            self._cursor = self._connection.cursor()
        except (pymysql.Error, psycopg2.Error, ValueError) as err:
            print(f'Error from db controller {err}')

    def __del__(self):
        self._connection.commit()
        self._connection.close()
