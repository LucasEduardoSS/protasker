import customtkinter as ctk
from PIL import Image

# Project Config
GENERAL_FONT = ("Tahoma", 11)
IMAGES_PATH = "C:/Users/luedu/Documents/Projetos/Pycharm/ProTasker/images/"


class CardView(ctk.CTkFrame):
    def __init__(self, master, name, **kwargs):
        super().__init__(master, **kwargs)

        self._card_meta = {
            "name": name
        }

        self.configure(
            fg_color="#3E4D66",
            border_color="#777",
            border_width=1,
            corner_radius=0,
            height=250,
            width=150
        )

        # Impede que os widgets redimensionem o card
        self.pack_propagate(False)

        self.card_name_label = ctk.CTkLabel(
            self,
            text=self._card_meta["name"],
            fg_color="transparent",
            font=("Tahoma", 11)
        )
        self.card_name_label.pack(
            anchor="nw",
            side="left",
            padx=10,
            pady=10
        )

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
        edit_button.pack(
            anchor="n",
            side="right",
            padx=10,
            pady=10
        )

    def edit_card(self):
        pass


class CardPessoa(CardView):
    def __init__(self, master, name, **kwargs):
        super().__init__(master, name, **kwargs)

        # Atributos da pessoa
        self._card_meta.update({
            "name": "Nova Pessoas",
            "role": "Faxineiro",
            "sector": None,
            "company": None
        })

        role_label = ctk.CTkLabel(
            self,
            text=self._card_meta["role"],
            fg_color="transparent",
            font=("Tahoma", 11)
        )
        role_label.pack(
            after=self.card_name_label,
            anchor="nw",
            side="left",
            padx=10,
            pady=10
        )
