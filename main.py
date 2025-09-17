import customtkinter as ctk
import queue, threading

from database.db import database
from models.distribution_model import Distribution
from models.person_model import Person
from models.task_model import Task
from models.sector_model import Sector
from models.assignment_model import Assignment
from views.main_view import ProTaskerView
from utils.db_utils import gen_sample_data

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Conecta ao banco de dados
if database.is_closed():
  database.connect()

# Cria as tabelas
database.drop_tables([Assignment, Person, Task, Distribution, Sector], safe=True)
database.create_tables([Sector, Person, Task, Distribution, Assignment], safe=True)

# Gera dados de exemplo
gen_sample_data()

pro_tasker_view = ProTaskerView()

if __name__ == "__main__":

    # Loop principal
    pro_tasker_view.mainloop()

    # Fecha a conexão com a BD
    database.close()
