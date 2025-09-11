from peewee import Model, CharField, ForeignKeyField, JOIN
from database.db import database
from models.sector_model import Sector
from models.task_model import Task


class Person(Model):
    name = CharField()
    role = CharField()
    sector = ForeignKeyField(Sector, backref='members', null=True)
    company = CharField(default="Sem empresa", null=True)
    tasks = ForeignKeyField(Task, backref='responsible', null=True)

    class Meta:
        database = database
        table_name = 'person'

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Person: {self.name}>"

    @staticmethod
    def get_all():
        """ Retorna uma lista com dicionários dos dados das pessoas."""
        return Person.select()

    @staticmethod
    def get_by_name(name: str):
        """ Retorna a instância de Person com o nome informado. """
        return Person.get_or_none(Person.name == name)

    @staticmethod
    def get_all_dicts(order_by: bool = True):
        """
        Retorna uma lista de dicionários com os dados das pessoas.
        - order_by: se True, ordena por nome.
        """
        query = (Person
                 .select(Person, Sector.name.alias('sector_name'))
                 .join(Sector, on=(Person.sector == Sector.id), join_type=JOIN.LEFT_OUTER))

        if order_by:
            query = query.order_by(Person.name)
        return list(query.dicts())

