from peewee import CharField, AutoField

from .base_model import BaseModel


class FilePathModel(BaseModel):

    id = AutoField()
    path = CharField(max_length=300)
