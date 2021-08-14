# -*- coding: utf-8 -*-

from models.Article import Article
from orm_core.Conditions import QFilter


def add_article(flow):
    article = Article()
    article['id'] = flow['id']
    article['title'] = flow['title']
    article['description'] = flow['description']
    article['content'] = flow['content']
    article.create()


def get_article(condition):
    """

    :param condition: (QFilter().add_k('description').eq().add_v('foo').q_or().add_k('id').ne().add_v(1).condition)
    """

    article = Article()
    article.condition = condition
    return article.read()


def update_article(set_update, condition):
    """

    :param set_update: QFilter().add_k('title').eq().add_v('AARRRGH').condition
    :param condition: condition=QFilter().add_k('id').eq().add_v(45).condition
    """

    article = Article()
    article.set_update = set_update
    article.condition = condition
    article.update()


def delete_article(condition):
    """

    :param condition: QFilter().add_k('id').eq().add_v(1).condition
    """

    article = Article()
    article.condition = condition
    article.delete()


def read_by_one_id(model_id):
    """

    :param model_id: any article id
    """

    article = Article()
    return article.read_by_one_id(model_id=model_id)


def get_user(condition):
    """

    :param condition: (QFilter().add_k('description').eq().add_v('foo').q_or().add_k('id').ne().add_v(1).condition)
    """

    article = Users()
    article.condition = condition
    return article.read()


if __name__ == '__main__':
    """
    Обязательный import:
    Структура таблицы:
    from models.Article import Article
    
    Конструктор условий:
    from Conditions import QFilter
    ----------------------------
    
    Пример создания строки в таблице:
    
    flow = {'id': 45, 'content': 'FOO'}
    add_article(flow)
    ----------------------------
    Пример SELECT запроса в таблицу с условием:
    
    get_article(QFilter().add_k('description').eq().add_v('foo').q_or().add_k('id').ne().add_v(1).condition)
    ----------------------------
    Пример UPDATE запроса в таблицу:
    
    update_article(set_update=QFilter().add_k('title').eq().add_v('AARRRGH').condition,
                   condition=QFilter().add_k('id').eq().add_v(45).condition)
    ----------------------------   
    Пример DELETE запроса в таблицу:
    
    delete_article(condition=QFilter().add_k('id').eq().add_v(1).condition)
    ----------------------------
    Пример SELECT запроса с прокидыванием id строки:
        
    read_by_one_id(45)
    ----------------------------
    Пример создания запроса из терминала:
    
    $ python make_query.py -Q 'SELECT * FROM avail.articles;'
    
    """
