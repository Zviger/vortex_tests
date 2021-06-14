from peewee import TimestampField, ForeignKeyField, AutoField

from .base_model import BaseModel
from .tests_set_info import TestsSetInfoModel


class TestSetModel(BaseModel):

    id = AutoField()
    time_start = TimestampField()
    time_end = TimestampField()
    tests_set_info = ForeignKeyField(TestsSetInfoModel)
