from peewee import Model

from app.database import db


class BaseModel(Model):

    class Meta:
        database = db
        legacy_table_names = False
