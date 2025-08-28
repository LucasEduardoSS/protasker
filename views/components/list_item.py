from customtkinter import CTkFrame, CTkLabel
from views.components.edit_button import EditButton
from models.sector_model import Sector


class ListItemView(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="#3E4D66", border_color="#777", height=30)

        # Botão de editar registro
        edit_button = EditButton(self, text="Editar")
        edit_button.pack(side="right", padx=(0, 5))

    def load_fields(self, fields: dict):
        for field in fields.items():
            # Ignora campos vazios
            if field[1] is None:
                continue

            # Nome do campo
            name_lb = CTkLabel(
                self,
                text=field[0]+":",
                fg_color="transparent",
                font=("Tahoma", 11, "bold"),
                height=20,
            )
            name_lb.pack(side="left", ipadx=10)

            # Valor do campo
            value_label = CTkLabel(self, text=field[1], fg_color="transparent", font=("Tahoma", 11))
            value_label.pack(side="left", padx=(0, 10))

    def edit_record(self):
        pass

    def toggle_filter_tab(self):
        pass

class ListItemPessoa(ListItemView):
    def __init__(self, master, person_info: dict, **kwargs):
        super().__init__(master, **kwargs)

        self._person_meta = {
            "Nome": person_info["name"],
            "Cargo": person_info["role"],
            "Setor": Sector.get_by_id(person_info["sector"]).name if person_info["sector"] is not None else None,
            "Empresa": person_info["company"]
        }

        self.load_fields(self._person_meta)


class ListItemTarefa(ListItemView):
    def __init__(self, master, task_info: dict, **kwargs):
        super().__init__(master, **kwargs)

        # Atributos da tarefa
        self._task_meta = {
            "Tarefa": task_info["name"],
            "Descrição": task_info["description"],
            "Setor": Sector.get_by_id(task_info["sector"]).name if task_info["sector"] is not None else None,
            "Prioridade": task_info["priority"],
            "Status": "Pendente",
            "Prazo": task_info["deadline"]
        }

        self.load_fields(self._task_meta)


class ListItemSetor(ListItemView):
    def __init__(self, master, sector_info: dict, **kwargs):
        super().__init__(master, **kwargs)

        self._sector_meta = {
            "Setor": sector_info["name"]
        }

        self.load_fields(self._sector_meta)
