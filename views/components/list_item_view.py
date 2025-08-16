import customtkinter as ctk
from PIL import Image

# Project Config
GENERAL_FONT = ("Tahoma", 11)
IMAGES_PATH = "C:/Users/luedu/Documents/Projetos/Pycharm/ProTasker/images/"


class ListItemView(ctk.CTkFrame):
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

        title = ctk.CTkLabel(self, text=name, font=("Tahoma", 11))
        title.pack(anchor="w", side="left", padx=(10, 0))

        edit_icon = ctk.CTkImage(
            light_image=Image.open(IMAGES_PATH + "edit-icon.png"),
            dark_image=Image.open(IMAGES_PATH + "edit-icon.png"),
            size=(20, 20)
        )

        edit_button = ctk.CTkButton(
            self,
            width=30,
            height=20,
            text="Editar",
            font=("Tahoma", 11),
            image=edit_icon,
            fg_color="transparent",
            hover_color=self.cget("fg_color"),
            command = self.edit_record
        )
        edit_button.pack(
            side="right",
            padx=(0, 5)
        )

    def edit_record(self):
        pass

    def toggle_filter_tab(self):
        pass

