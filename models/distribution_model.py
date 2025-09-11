from peewee import Model, IntegerField, CharField
from database.db import database


class Distribution(Model):
    title = CharField()
    total_tasks = IntegerField()
    finished_tasks = IntegerField()

    class Meta:
        database = database
        table_name = 'distribution'
