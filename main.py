import customtkinter as ctk

from database.db import database
from models.person_model import Person
from models.task_model import Task
from models.sector_model import Sector
from views.main_view import ProTaskerView

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

pro_tasker_view = ProTaskerView()

if __name__ == "__main__":
    database.connect()
    database.drop_tables([Person, Task, Sector])
    database.create_tables([Person, Task, Sector], safe=True)

    pro_tasker_view.mainloop()
    database.close()
