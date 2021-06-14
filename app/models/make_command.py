from peewee import CharField, AutoField

from .base_model import BaseModel


class MakeCommandModel(BaseModel):

    id = AutoField()
    command = CharField(max_length=300)
