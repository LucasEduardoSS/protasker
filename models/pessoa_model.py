from peewee import Model, CharField
from database.db import database


class Pessoa(Model):
    nome = CharField()
    cargo = CharField()
    setor = CharField()
    empresa = CharField()

    class Meta:
        database = database
        table_name = 'pessoa'
