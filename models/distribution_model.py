from peewee import IntegerField, CharField

from database.db import database
from models.base_model import BaseModel


class Distribution(BaseModel):
    """
    Classe modelo de distribuição de tarefas.
    Possui os campos: Título, total de tarefas e número de tarefas concluídas.
    """

    name = CharField()
    total_tasks = IntegerField()
    finished_tasks = IntegerField()

    class Meta:
        database = database
        table_name = 'distribution'
