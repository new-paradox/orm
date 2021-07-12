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


def get_article(flow):
    row = Article()
    # row.condition = QFilter().add_k('description').eq().add_v('foo').q_or().add_k('id').ne().add_v(1).condition
    row.condition = flow
    data = row.read()
    print(data)

if __name__ == '__main__':
    # flow = {'id': 45, 'content': 'FOO'}
    get_article(QFilter().add_k('description').eq().add_v('foo').q_or().add_k('id').ne().add_v(1).condition)
    # print(Article().read_by_one_id(model_id=45))