from Model import Driver, DBConfigSettings
from models.Article import Article


# @route("POST", "/new_article")
def new_article(flow):
    new_article = Article(Driver(DBConfigSettings()))

    new_article.title = flow['title']
    new_article.description = flow['description']
    new_article.content = flow['content']

    new_article.create()


if __name__ == '__main__':
    flow = {'title': 'zopa', 'description': 'foo', 'content': 'FOO'}
    new_article(flow)
