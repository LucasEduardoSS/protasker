import customtkinter as ctk

from views.components.edit_button import EditButton
from models.sector_model import Sector


class CardView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(
            fg_color="#3E4D66",
            border_color="#777",
            border_width=1,
            corner_radius=0,
            height=250,
            width=175
        )

        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=0, minsize=30)

        # Impede que os widgets redimensionem o card
        self.grid_propagate(False)

        # Botão de editar registro
        edit_button = EditButton(self, text="")
        edit_button.grid(row=0, column=1, padx=5, pady=5, sticky="n")

    def load_fields(self, fields: dict):
        card_info_frame = ctk.CTkFrame(self)
        card_info_frame.grid(row=0, column=0, padx=5, pady=5, ipadx=2, ipady=2, sticky="nsew")
        card_info_frame.configure(fg_color="transparent")

        for field in fields.items():
            # Ignora campos vazios
            if field[1] is None:
                continue

            # Nome do campo
            lb = ctk.CTkLabel(card_info_frame, text=field[0]+":", fg_color="transparent", font=("Tahoma", 11, "bold"),
                              height=10, anchor="w", justify="left")
            lb.pack(side="top", anchor="w", padx=5, pady=(5, 0), fill="x", expand=True)

            # Valor do campo
            lb = ctk.CTkLabel(card_info_frame, text=field[1], fg_color="transparent", font=("Tahoma", 11),
                              height=10, anchor="w", justify="left")
            lb.pack(side="top", anchor="w", padx=5, pady=4, fill="x", expand=True)

    def edit_card(self):
        pass


class CardPessoa(CardView):
    def __init__(self, master, person_info: dict, **kwargs):
        super().__init__(master, **kwargs)

        # Atributos da pessoa
        self._card_meta = {
            "Nome": person_info["name"],
            "Cargo": person_info["role"],
            "Setor": Sector.get_by_id(person_info["sector"]).name if person_info["sector"] is not None else None,
            "Empresa": person_info["company"]
        }
        self.load_fields(self._card_meta)


class CardTarefa(CardView):
    def __init__(self, master, task_info: dict, **kwargs):
        super().__init__(master, **kwargs)

        # Atributos da tarefa
        self._card_meta = {
            "Tarefa": task_info["name"],
            "Descrição": task_info["description"],
            "Setor": Sector.get_by_id(task_info["sector"]).name if task_info["sector"] is not None else None,
            "Empresa": task_info["company"],
            "Prioridade": task_info["priority"],
            "Status": "Pendente"
        }
        self.load_fields(self._card_meta)


class CardSetor(CardView):
    def __init__(self, master, sector_info: dict, **kwargs):
        super().__init__(master, **kwargs)

        # Atributos do setor
        self._card_meta = {
            "Setor": sector_info["name"]
        }
        self.load_fields(self._card_meta)
