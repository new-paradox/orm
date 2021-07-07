from Model import Model


class Article(Model):
    _table_name = "Articles"
    id: int
    title: str
    description: str
    content: str
