from peewee import AutoField, IntegerField, ForeignKeyField

from .test import TestModel
from .base_model import BaseModel


class CoreInfoModel(BaseModel):

    id = AutoField()
    core = IntegerField()
    cycles = IntegerField()
    instructions = IntegerField()
    test = ForeignKeyField(TestModel, backref="core_infos")
