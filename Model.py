from psql_connect import DBConnectSettings


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Model(DBConnectSettings, metaclass=Singleton):
    __table_name = "Articles"
    keys = []
    Values = []

    def __setitem__(self, key, value):
        self.keys.append(key)
        self.Values.append(value)

    def create(self):
        prepare_key = f"({', '.join(self.keys)})"
        prepare_values = str(tuple(self.Values))
        query = f"INSERT INTO {self.__table_name.lower()} {prepare_key} VALUES {prepare_values};"
        # self._cursor.execute(query)
        return self._cursor.execute(query)
