from peewee import CharField, DateTimeField, ForeignKeyField, IntegerField
from datetime import datetime

from database.db import database
from models.base_model import BaseModel
from models.sector_model import Sector


class Task(BaseModel):
    """
    Classe modelo de tarefa.
    Campos: Nome, Descrição, Setor, Empresa, Peso, Prioridade, Dependências, Data de Criação, Prazo, Data de Conclusão e Condição.
    """

    name = CharField()
    description = CharField(default="Sem descrição")
    sector = ForeignKeyField(Sector, backref='tasks', null=True)
    company = CharField(default="Sem empresa", null=True)
    weight = IntegerField(default=0)
    priority = CharField()
    dependencies = CharField(default="Nenhuma", null=True)
    creation_date = DateTimeField(default=datetime.now)
    deadline = DateTimeField(default=None, null=True)
    closure_date = DateTimeField(default=None, null=True)
    status = CharField(default="Pendente")

    class Meta:
        database = database
        table_name = 'tasks'

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Task: {self.name}>"

    @staticmethod
    def get_by_name(name: str):
        return Task.get_or_none(Task.name == name)
