from app.database import db
from app.models import (
    CommitHashModel, CoreInfoModel, FilePathModel, TestModel,
    TestInfoModel, TestSetModel, TestsSetInfoModel, TestsSetParamsModel, MakeCommandModel)


def create_tables():
    with db.atomic():
        db.create_tables([CommitHashModel, CoreInfoModel, FilePathModel, TestModel, TestInfoModel,
                          TestSetModel, TestsSetInfoModel, TestsSetParamsModel, MakeCommandModel])
