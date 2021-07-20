# -*- coding: utf-8 -*-
from typing import Dict

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


@dataclass
class MySQLDBConfig(BaseDBConfig):
    """
    Настраивается индивидаульно под mysql db;
    """
    password: str
    database: str


@dataclass
class PSQLDBConfig(BaseDBConfig):
    """
    Настраивается индивидаульно под psql db;
    """
    password: str
    database: str


class PostgreSQLDB(PSQLDBConfig):
    """
    Инициализирует соединение с PostgreSQL;
    """

    def __init__(self):
        self.connection = psycopg2.connect(dbname=f"{config.DATABASE}",
                                           user=f"{config.USER}",
                                           password=f"{config.PASSWORD}")

    def get_connection(self):
        return self.connection


class MysqlDB(MySQLDBConfig):
    """
    Инициализирует соединение с MySQL;
    """

    def __init__(self, *args):
        args = args[0]
        host = args['host']
        user = args['user']
        password = args['password']
        database = args['database']
        self.connection = pymysql.connect(host=host,
                                          user=user,
                                      password=password,
                                      database=database)

    def get_connection(self):
        return self.connection


class DBDrivers(Enum):
    mysql = MysqlDB
    psql = PostgreSQLDB


def get_driver(driver_name: str) -> Dict:
    enum_elem = [{"name": name, "method": sql_driver} for name, sql_driver in vars(DBDrivers).items()
                 if name == driver_name]
    if enum_elem:
        return enum_elem[0]


def prepare_driver(driver: str):
    driver = get_driver(driver)
    return driver["method"]


class AutoDBConfigManager(BaseDBConfig):
    """
    Смотрит config.py -> выбирает db для соединения;
    """

    def __init__(self):
        try:
            self.db_driver = config.DB_DRIVER
            self.host = config.HOST
            self.user = config.USER
            self.password = config.PASSWORD
            self.database = config.DATABASE
            data = {"host": self.host, "user": self.user, "password": self.password, "database": self.database}
            self._connection = prepare_driver(config.DB_DRIVER).value(data).get_connection()
        except (pymysql.Error, psycopg2.Error, ValueError) as err:
            print(f'Error from db controller {err}')

    def __del__(self):
        self._connection.commit()
        self._connection.close()

    @property
    def connection(self):
        return self._connection

