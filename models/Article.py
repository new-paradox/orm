from Model import Model, BaseDBSettings, DBConfigSettings


class Article(Model):
    __TABLE_NAME = "Articles"

    id: int
    title: str
    description: str
    content: str
