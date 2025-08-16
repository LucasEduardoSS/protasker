from peewee import Model, CharField, DateField, ForeignKeyField

from models.sector_model import Sector
from database.db import database

class Task(Model):
    title = CharField()
    description = CharField()
    sector = ForeignKeyField(Sector, backref='tasks', null=True)
    priority = CharField()
    creation_date = DateField()
    forecast_date = DateField()
    closure_date = DateField()
    status = DateField()

    class Meta:
        database = database
        table_name = 'tasks'
