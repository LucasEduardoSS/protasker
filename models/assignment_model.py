from peewee import ForeignKeyField

from database.db import database
from models.base_model import BaseModel
from models.person_model import Person
from models.task_model import Task
from models.distribution_model import Distribution


class Assignment(BaseModel):
    """
    Classe modelo de distribuição de tarefas.
    Campos: Distribuição, Pessoa e Tarefa.
    """

    distro = ForeignKeyField(Distribution, backref="assignments")
    person = ForeignKeyField(Person, backref="assignments")
    task = ForeignKeyField(Task, backref="assignments")

    class Meta:
        database = database
        # Evita duplicidade
        indexes = ((( "person", "task"), True),)
