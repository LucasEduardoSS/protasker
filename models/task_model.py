from peewee import Model, CharField, DateTimeField, ForeignKeyField, JOIN
from datetime import datetime

from database.db import database
from models.sector_model import Sector

class Task(Model):
    name = CharField()
    description = CharField(default="Sem descrição")
    sector = ForeignKeyField(Sector, backref='tasks', null=True)
    company = CharField(default="Sem empresa", null=True)
    priority = CharField()
    dependencies = CharField(default="Nenhuma", null=True)
    creation_date = DateTimeField(default=datetime.now)
    forecast_date = DateTimeField(default=None, null=True)
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
    def get_all():
        return Task.select()

    @staticmethod
    def get_all_dicts(order_by: bool = True):
        """
        Retorna uma lista de dicionários com os dados das pessoas.
        - order_by: se True, ordena por nome.
        """
        query = (Task
                 .select(Task, Sector.name.alias('sector_name'))
                 .join(Sector, on=(Task.sector == Sector.id), join_type=JOIN.LEFT_OUTER))

        if order_by:
            query = query.order_by(Task.name)
        return list(query.dicts())
