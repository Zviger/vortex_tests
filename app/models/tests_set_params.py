from peewee import AutoField


from .base_model import BaseModel


class TestsSetParamsModel(BaseModel):

    id = AutoField()
