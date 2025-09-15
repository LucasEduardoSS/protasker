from peewee import CharField

from database.db import database
from models.base_model import BaseModel


class Sector(BaseModel):
    """
    Classe modelo de setor.
    Campos: Nome
    """

    name = CharField()

    class Meta:
        database = database
        table_name = 'sector'

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Sector: {self.name}>"

    @staticmethod
    def get_by_name(name: str):
        return Sector.get_or_none(Sector.name == name)
