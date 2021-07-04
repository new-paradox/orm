from models.Article import Article
from models.Media_types import MediaType


# @route("POST", "/new_article")
def new_article():
    flow = {'id': 1, 'title': 'zopa', 'description': 'foo', 'content': 'FOO'}
    new_article_ = Article()
    new_article_.id = flow['id']
    new_article_.title = flow['title']
    new_article_.description = flow['description']
    new_article_.content = flow['content']

    keys = f"({', '.join([key for key in flow.keys()])})"
    new_article_.create(keys)


def new_media_type(flow):
    new_media_type = MediaType()
    new_media_type.title = flow['title']
    new_media_type.description = flow['description']
    new_media_type.content = flow['content']
    new_media_type.create()


if __name__ == '__main__':
    
    new_article()
