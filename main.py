from Model import BaseDBSettings
from models.Article import Article


# @route("POST", "/new_article")
def new_article(flow):
    new_article = Article(BaseDBSettings())

    new_article.title = flow.title
    new_article.description = flow.description
    new_article.content = flow.content

    new_article.create()
