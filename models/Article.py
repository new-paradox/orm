from Model import Model


class Article(Model):
    _table = "Articles"

    class _Property:
        id: int
        title: str
        description: str
        content: str
