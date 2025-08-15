from peewee import Model, CharField
from database.db import database


class Setor(Model):
    nome = CharField()

    class Meta:
        database = database
        table_name = 'setor'
