# -*- coding: utf-8 -*-

from Model import Model


class MediaType(Model):
    __TABLE_NAME = "media_types"

    id: int
    name: str
