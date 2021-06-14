from peewee import CharField, AutoField

from .base_model import BaseModel


class CommitHashModel(BaseModel):

    id = AutoField()
    hash = CharField(max_length=40, unique=True)
