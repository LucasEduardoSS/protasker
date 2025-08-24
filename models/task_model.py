from peewee import Model, CharField, DateTimeField, ForeignKeyField
from datetime import datetime

from database.db import database
from models.sector_model import Sector

class Task(Model):
    name = CharField()
    description = CharField(default="Sem descrição")
    sector = ForeignKeyField(Sector, backref='tasks', null=True)
    priority = CharField()
    dependencies = CharField()
    creation_date = DateTimeField(default=datetime.now)
    forecast_date = DateTimeField(default=None, null=True)
    closure_date = DateTimeField(default=None, null=True)
    status = CharField(default="Pendente")

    class Meta:
        database = database
        table_name = 'tasks'
