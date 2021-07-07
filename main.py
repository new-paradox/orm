# -*- coding: utf-8 -*-

from models.Article import Article
from Conditions import QFilter, EQ


# @route("POST", "/new_article")
def add_article(flow):
    row = Article()
    row['id'] = flow['id']
    row['title'] = flow['title']
    row['description'] = flow['description']
    row['content'] = flow['content']
    row.create()


def get_article():
    row = Article()
    # row.condition = QFilter(EQ('id', 45), EQ('title', 'bar'))
    condition = str(QFilter(EQ('id', 45)))
    data = row.read()
    print(data)


if __name__ == '__main__':
    flow = {'id': 45, 'content': 'FOO'}
    get_article()
