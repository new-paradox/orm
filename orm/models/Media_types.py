# -*- coding: utf-8 -*-

from orm_core.Model import Model


class MediaType(Model):
    __TABLE_NAME = "media_types"

    id: int
    name: str
