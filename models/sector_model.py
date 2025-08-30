from peewee import Model, CharField
from database.db import database


class Sector(Model):
    name = CharField()

    class Meta:
        database = database
        table_name = 'sector'

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Sector: {self.name}>"

    @staticmethod
    def get_all():
        return Sector.select()

    @staticmethod
    def get_all_dicts(order_by: bool = True):
        """
        Retorna uma lista de dicionários com os dados das pessoas.
        - order_by: se True, ordena por nome.
        """
        query = Sector.select()

        if order_by:
            query = query.order_by(Sector.name)
        return list(query.dicts())
