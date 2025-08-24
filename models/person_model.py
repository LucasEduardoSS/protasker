from peewee import Model, CharField, ForeignKeyField
from database.db import database
from models.sector_model import Sector


class Person(Model):
    name = CharField()
    role = CharField()
    sector = ForeignKeyField(Sector, backref='members', null=True)
    company = CharField(default="Sem empresa", null=True)

    class Meta:
        database = database
        table_name = 'person'
