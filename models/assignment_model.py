from peewee import ForeignKeyField

from database.db import database
from models.base_model import BaseModel
from models.person_model import Person
from models.task_model import Task


class Assignment(BaseModel):
    """
    Classe modelo de distribuição de tarefas.
    Campos: Pessoa (FK) e Tarefa (FK).
    """

    person = ForeignKeyField(Person, backref="assignments")
    task = ForeignKeyField(Task, backref="assignments")

    class Meta:
        database = database
        # Evita duplicidade
        indexes = ((( "person", "task"), True),)
