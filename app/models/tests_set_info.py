from peewee import AutoField, ForeignKeyField

from .base_model import BaseModel
from .commit_hash import CommitHashModel
from .tests_set_params import TestsSetParamsModel


class TestsSetInfoModel(BaseModel):

    id = AutoField()
    commit_hash = ForeignKeyField(CommitHashModel)
    vortex_commit_hash = ForeignKeyField(CommitHashModel)
    toolchain_commit_hash = ForeignKeyField(CommitHashModel)
    tests_set_params = ForeignKeyField(TestsSetParamsModel)
