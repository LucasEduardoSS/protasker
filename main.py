import customtkinter as ctk
import queue, threading

from database.db import database
from models.person_model import Person
from models.task_model import Task
from models.sector_model import Sector
from views.main_view import ProTaskerView
from utils.gen_sample_db import gen_sample_data

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

pro_tasker_view = ProTaskerView()

if __name__ == "__main__":
    # Cria as tabelas
    if database.is_closed():
      database.connect()
    database.drop_tables([Person, Task, Sector])
    database.create_tables([Person, Task, Sector], safe=True)
    gen_sample_data()

    pro_tasker_view.mainloop()
    database.close()
