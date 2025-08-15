from peewee import Model, CharField, DateField

from database.db import database

class Tarefa(Model):
    titulo = CharField()
    descricao = CharField()
    setor = CharField()
    prioridade = CharField()
    data_criacao = DateField()
    data_previsao = DateField()
    data_conclusao = DateField()
    status = DateField()

    class Meta:
        database = database
        table_name = 'tarefa'
