from peewee import Model, ForeignKeyField

from database.db import database
from models.person_model import Person
from models.task_model import Task


class Assignment(Model):
    person = ForeignKeyField(Person, backref="assignments")
    task = ForeignKeyField(Task, backref="assignments")

    class Meta:
        database = database
        # Evita duplicidade
        indexes = ((( "person", "task"), True),)
