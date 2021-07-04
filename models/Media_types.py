from Model import Model, BaseDBSettings, DBConfigSettings


class MediaType(Model):
    __TABLE_NAME = "media_types"

    id: int
    name: str
