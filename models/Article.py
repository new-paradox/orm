# -*- coding: utf-8 -*-

from Model import Model


class Article(Model):
    """
    Описывается структура траблицы;
    Обязательное наследование от Model
    """
    _table_name = "Articles"
    id: int
    title: str
    description: str
    content: str
