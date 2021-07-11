# -*- coding: utf-8 -*-

from models.Article import Article
from Conditions import EQ, AND, QFilter, OR, NE


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
    # row.condition = QFilter(AND(EQ('description', 'foo'), EQ('content', 'FOO')))
    row.condition = flow
    data = row.read()
    print(data)

if __name__ == '__main__':
    # flow = {'id': 45, 'content': 'FOO'}
    # get_article(QFilter(OR(EQ('description', 'foo'), NE('id', 1))))
    print(Article().read_by_one_id(model_id=45))