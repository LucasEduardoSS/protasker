import customtkinter as ctk
from PIL import Image

# Project Config
GENERAL_FONT = ("Tahoma", 11)
IMAGES_PATH = "C:/Users/luedu/Documents/Projetos/Pycharm/ProTasker/images/"


class CardView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(
            fg_color="#3E4D66",
            border_color="#777",
            border_width=1,
            corner_radius=0,
            height=250,
            width=200
        )

        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=0, minsize=30)

        # Impede que os widgets redimensionem o card
        self.grid_propagate(False)

        edit_icon = ctk.CTkImage(
            light_image=Image.open(IMAGES_PATH + "edit-icon.png"),
            dark_image=Image.open(IMAGES_PATH + "edit-icon.png"),
            size=(20, 20)
        )

        edit_button = ctk.CTkButton(
            self,
            width=30,
            height=20,
            text="",
            font=("Tahoma", 11),
            image=edit_icon,
            fg_color="transparent",
            hover_color=self.cget("fg_color"),
            command=self.edit_card
        )
        edit_button.grid(row=0, column=1, padx=5, pady=5, sticky="n")

    def load_fields(self, fields: dict):
        card_info_frame = ctk.CTkFrame(self)
        card_info_frame.grid(row=0, column=0, padx=2, pady=2, ipadx=2, ipady=2, sticky="nsew")
        card_info_frame.configure(fg_color="transparent")

        for field in fields.items():
            # Ignora campos vazios
            if field[1] is None:
                continue

            # Nome do campo
            lb = ctk.CTkLabel(card_info_frame, text=field[0], fg_color="transparent", font=("Tahoma", 11, "italic"),
                              height=20, anchor="w", justify="left")
            lb.pack(side="top", anchor="w", padx=5, pady=(5, 0), fill="x", expand=True)

            # Valor do campo
            lb = ctk.CTkLabel(card_info_frame, text=field[1], fg_color="transparent", font=("Tahoma", 12),
                              height=20, anchor="w", justify="left")
            lb.pack(side="top", anchor="w", padx=5, pady=2, fill="x", expand=True)

    def edit_card(self):
        pass


class CardPessoa(CardView):
    def __init__(self, master, person_info: dict, **kwargs):
        super().__init__(master, **kwargs)

        # Atributos da pessoa
        self._card_meta = {
            "nome": person_info["name"],
            "cargo": person_info["role"],
            "setor": person_info["sector"],
            "empresa": person_info["company"]
        }

        self.load_fields(self._card_meta)


class CardTarefa(CardView):
    def __init__(self, master, task_info: dict, **kwargs):
        super().__init__(master, **kwargs)

        # Atributos da tarefa
        self._card_meta = {
            "nome": task_info["name"],
            "descricao": task_info["description"],
            "prioridade": task_info["priority"],
            "status": task_info["status"]
        }

        self.load_fields(self._card_meta)


class CardSetor(CardView):
    def __init__(self, master, sector_info: dict, **kwargs):
        super().__init__(master, **kwargs)

        # Atributos do setor
        self._card_meta = {
            "nome": sector_info["name"]
            #"descricao": sector_info["description"]
        }

        self.load_fields(self._card_meta)
