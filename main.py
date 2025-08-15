import customtkinter as ctk

from database.db import database
from models.pessoa_model import Pessoa
from models.tarefa_model import Tarefa
from models.setor_model import Setor
from views.main_view import ProTaskerView

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

pro_tasker_view = ProTaskerView()

if __name__ == "__main__":
    database.connect()
    database.create_tables([Pessoa, Tarefa, Setor], safe=True)

    pro_tasker_view.mainloop()
    database.close()
