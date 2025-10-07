from peewee import CharField, ForeignKeyField

from database.db import database
from models.base_model import BaseModel
from models.sector_model import Sector


class Person(BaseModel):
    """
    Classe modelo de Pessoa.
    Campos: Nome, Cargo, Setor, Empresa, Tarefas (FK)
    """

    name = CharField()
    role = CharField()
    sector = ForeignKeyField(Sector, backref='members', null=True)
    company = CharField(default="Sem empresa", null=True)

    class Meta:
        database = database
        table_name = 'person'

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Person: {self.name}>"
