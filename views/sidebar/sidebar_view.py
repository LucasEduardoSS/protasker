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
        self.buttons_by_tab = {}
        self.active_tab_id = None

        # Cores para estados
        self.active_fg = "#3E4D66"
        self.active_hover = "#4C5E7F"
        self.inactive_fg = "transparent"
        self.inactive_hover = "#3E4D66"

        self._setup_buttons()

    def _setup_buttons(self):
        buttons_config = [
            (str(IMAGES_DIR / "clarify-filled-icon.png"), "detalhes", "Detalhes"),
            (str(IMAGES_DIR / "checklist-icon.png"), "controle", "Controle"),
            (str(IMAGES_DIR / "hand-raised-icon.png"), "primeiros-passos", "Primeiros Passos")
        ]

        for icon, tab_id, tooltip in buttons_config:
            btn = self._create_button(icon, tab_id)
            self.buttons.append(btn)
            self.buttons_by_tab[tab_id] = btn

        self._set_active_button("primeiros-passos")

    def _create_button(self, icon_path, tab_id):
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
            command=lambda: self._toggle_tab(tab_id)
        )
        button.pack(pady=(2, 0))
        return button

    def _toggle_tab(self, tab_id):
        """Ativa/Desativa a aba baseado no tab_id informado."""

        # Chama a função auxiliar no escopo do workspace
        workspace = self.master.main_meta["workspace"]
        workspace.toggle_sidebar_tabs(tab_id)

        # Atualiza o estado ativo
        self._set_active_button(tab_id)

    def _set_active_button(self, tab_id: str):
        """Atualiza visual dos botões baseado na tab ativa"""

        if tab_id == self.active_tab_id:
            self.buttons_by_tab[tab_id].configure(fg_color=self.inactive_fg, hover_color=self.inactive_hover)
            self.active_tab_id = None
            return

        # Atualiza o estado ativo
        self.active_tab_id = tab_id

        # Muda a cor dos botões
        for tid, button in self.buttons_by_tab.items():
            if tid == tab_id:
                button.configure(fg_color=self.active_fg, hover_color=self.active_hover)
            else:
                button.configure(fg_color=self.inactive_fg, hover_color=self.inactive_hover)
