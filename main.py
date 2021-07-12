# -*- coding: utf-8 -*-

from models.Article import Article
from Conditions import QFilter


# @route("POST", "/new_article")
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
    data = row.read()
    print(data)


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
    row.read_by_one_id(model_id=model_id)


if __name__ == '__main__':
    # flow = {'id': 45, 'content': 'FOO'}
    # get_article(QFilter().add_k('description').eq().add_v('foo').q_or().add_k('id').ne().add_v(1).condition)
    # print(Article().read_by_one_id(model_id=1))
    # update_article(set_update=QFilter().add_k('title').eq().add_v('AARRRGH').condition,
    #                condition=QFilter().add_k('id').eq().add_v(45).condition)
    delete_article(condition=QFilter().add_k('id').eq().add_v(1).condition)
