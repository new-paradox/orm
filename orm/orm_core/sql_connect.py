# -*- coding: utf-8 -*-
import sqlite3
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
    db_driver: str
    host: str
    user: str
    password: str
    database: str


class PostgreSQLDB(BaseDBConfig):
    """
    Инициализирует соединение с PostgreSQL;
    """

    def __init__(self, *args):
        args = args[0]
        self.user = args['user']
        self.password = args['password']
        self.database = args['database']
        self.connection = psycopg2.connect(dbname=f"{self.database}",
                                           user=f"{self.user}",
                                           password=f"{self.password}")



class SQLite(BaseDBConfig):
    """
    Инициализирует соединение с sqlite3;
    """

    def __init__(self, *args):
        args = args[0]
        self.database = args['database']
        self.connection = sqlite3.connect(self.database)


class MysqlDB(BaseDBConfig):
    """
    Инициализирует соединение с MySQL;
    """

    def __init__(self, *args):
        args = args[0]
        self.user = args['user']
        self.host = args['host']
        self.password = args['password']
        self.database = args['database']
        self.connection = pymysql.connect(host=self.host,
                                          user=self.user,
                                          password=self.password,
                                          database=self.database
                                          )


class DBDrivers(Enum):
    mysql = MysqlDB
    psql = PostgreSQLDB
    sqlite = SQLite


def get_driver(driver_name: str):
    enum_elem = [{"name": name, "method": sql_driver} for name, sql_driver in vars(DBDrivers).items()
                 if name == driver_name]
    if enum_elem:
        return enum_elem[0]["method"]


class AutoDBConfigManager(BaseDBConfig):
    """
    Смотрит config.py -> выбирает из DBDrivers db для соединения;
    """

    def __init__(self):
        try:
            self.db_driver = config.DB_DRIVER
            self.host = config.HOST
            self.user = config.USER
            self.password = config.PASSWORD
            self.database = config.DATABASE
            data = {"host": self.host,
                    "user": self.user,
                    "password": self.password,
                    "database": self.database
                    }
            self._connection = get_driver(self.db_driver).value(data).connection
            # self._cursor = self._connection.cursor()
        except (pymysql.Error, psycopg2.Error, ValueError) as err:
            print(f'Error from db controller {err}')

    def __del__(self):
        self._connection.commit()
        self._connection.close()

    @property
    def connection(self):
        return self._connection

