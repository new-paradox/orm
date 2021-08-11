from orm_core.Model import Model


class AuthKey(Model):
    """
    Описывается структура траблицы;
    Обязательное наследование от Model
    """
    _table_name = "auth_key"
    id: int
    cookie: str
    username: str
