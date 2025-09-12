from peewee import Model, IntegerField, CharField
from database.db import database


class Distribution(Model):
    title = CharField()
    total_tasks = IntegerField()
    finished_tasks = IntegerField()

    class Meta:
        database = database
        table_name = 'distribution'

    @staticmethod
    def get_all_dicts(order_by: bool = True):
        """Retorna uma lista de dicionários com os dados das pessoas."""

        query = Distribution.select()
        if order_by:
            query = query.order_by(Distribution.title)
        return list(query.dicts())
