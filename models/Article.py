from Model import Model


class Article(Model):
    __table_name = "Articles"
    id: int
    title: str
    description: str
    content: str
