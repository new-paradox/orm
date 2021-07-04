from Model import Model


class Article(Model):
    _table = "Articles"

    id: int
    title: str
    description: str
    content: str
