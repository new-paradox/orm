from models.Article import Article


# @route("POST", "/new_article")
def get_article(flow):
    new_row = Article()
    new_row['id'] = flow['id']
    new_row['title'] = flow['title']
    new_row['description'] = flow['description']
    new_row['content'] = flow['content']
    new_row.create()


if __name__ == '__main__':
    flow = {'id': 1, 'title': 'bar', 'description': 'foo', 'content': 'FOO'}
    query = get_article(flow)
