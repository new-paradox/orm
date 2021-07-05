from models.Article import Article


# @route("POST", "/new_article")
def new_article():
    flow = {'id': 1, 'title': 'zopa', 'description': 'foo', 'content': 'FOO'}

    new_article_ = Article()

    new_article_._Property.id = flow['id']
    new_article_._Property.title = flow['title']
    new_article_._Property.description = flow['description']
    new_article_._Property.content = flow['content']
    new_article_.create()


if __name__ == '__main__':
    new_article()
