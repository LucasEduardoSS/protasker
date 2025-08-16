from peewee import Model, CharField
from database.db import database


class Sector(Model):
    name = CharField()

    class Meta:
        database = database
        table_name = 'sector'
