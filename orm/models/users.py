from orm_core.Model import Model


class Users(Model):
    """
    Описывается структура траблицы;
    Обязательное наследование от Model
    """
    _table_name = "users"
    id: int
    name: str
    age: str
    city: int