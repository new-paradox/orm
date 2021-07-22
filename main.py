# -*- coding: utf-8 -*-

# @route("POST", "/new_article")
from models.Article import Article
from orm_core.Conditions import QFilter


def add_article(flow):
    row = Article()
    row['id'] = flow['id']
    row['title'] = flow['title']
    row['description'] = flow['description']
    row['content'] = flow['content']
    row.create()


def get_article(condition):
    """

    :param condition: (QFilter().add_k('description').eq().add_v('foo').q_or().add_k('id').ne().add_v(1).condition)
    """

    row = Article()
    row.condition = condition
    return row.read()


def update_article(set_update, condition):
    """

    :param set_update: QFilter().add_k('title').eq().add_v('AARRRGH').condition
    :param condition: condition=QFilter().add_k('id').eq().add_v(45).condition
    """

    row = Article()
    row.set_update = set_update
    row.condition = condition
    row.update()


def delete_article(condition):
    """

    :param condition: QFilter().add_k('id').eq().add_v(1).condition
    """

    row = Article()
    row.condition = condition
    row.delete()


def read_by_one_id(model_id):
    """

    :param model_id: any row id
    """

    row = Article()
    return row.read_by_one_id(model_id=model_id)


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
    print(read_by_one_id(45))
