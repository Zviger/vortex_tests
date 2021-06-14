from peewee import TimestampField, IntegerField, ForeignKeyField, AutoField

from .test_info import TestInfoModel
from .test_set import TestSetModel
from .base_model import BaseModel


class TestModel(BaseModel):

    id = AutoField()
    time_start = TimestampField()
    time_end = TimestampField()
    status = IntegerField()
    elapsed_time = IntegerField()
    test_info = ForeignKeyField(TestInfoModel)
    test_set = ForeignKeyField(TestSetModel, backref="tests")
