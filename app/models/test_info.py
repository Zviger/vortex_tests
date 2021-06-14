from peewee import ForeignKeyField, AutoField

from .base_model import BaseModel
from .file_path import FilePathModel
from .make_command import MakeCommandModel


class TestInfoModel(BaseModel):

    id = AutoField()
    file_path = ForeignKeyField(FilePathModel)
    make_command = ForeignKeyField(MakeCommandModel)
