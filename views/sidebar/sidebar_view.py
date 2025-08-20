import customtkinter as ctk
from pathlib import Path
from PIL import Image

# Obtém o caminho base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Define o caminho para a pasta de imagens
IMAGES_DIR = BASE_DIR / "images"


class SidebarView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(fg_color="#2E333C", corner_radius=0)
        self.pack(side="left", anchor="nw", fill="y", padx=0, pady=0)

        self.buttons = []
        self.setup_buttons()

    def setup_buttons(self):
        buttons_config = [
            (str(IMAGES_DIR / "clarify-filled-icon.png"), "detalhes", "Detalhes"),
            (str(IMAGES_DIR / "checklist-icon.png"), "controle", "Controle")
        ]

        for icon, tab_id, tooltip in buttons_config:
            btn = self.create_button(icon, tab_id, tooltip)
            self.buttons.append(btn)

    def create_button(self, icon_path, tab_id, tooltip):
        icon_image = ctk.CTkImage(
            light_image=Image.open(icon_path),
            dark_image=Image.open(icon_path),
            size=(20, 20)
        )

        button = ctk.CTkButton(
            self,
            text='',
            image=icon_image,
            width=30,
            height=30,
            fg_color="transparent",
            hover_color="#3E4D66",
            corner_radius=0,
            font=("Tahoma", 11),
            command=lambda: self.toggle_tab(tab_id)
        )
        button.pack(pady=(2, 0))
        return button

    def toggle_tab(self, tab_id):
        splitview = self.master.split_content
        splitview.toggle_sidebar_tabs(tab_id)
