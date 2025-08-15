import customtkinter as ctk
from PIL import Image

# Project Config
GENERAL_FONT = ("Tahoma", 11)
IMAGES_PATH = "C:/Users/luedu/Documents/Projetos/Pycharm/ProTasker/images/"


class RecordView(ctk.CTkFrame):
    def __init__(self, master, name, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(
            fg_color="#3E4D66",
            border_color="#777",
            height=30
        )
        self.pack(
            anchor="nw",
            side="top",
            padx=10,
            pady=5,
            fill="x"
        )

        title = ctk.CTkLabel(
            self,
            text=name,
            font=("Tahoma", 11)
        )
        title.pack(
            anchor="w",
            side="left",
            padx=(10, 0)
        )
