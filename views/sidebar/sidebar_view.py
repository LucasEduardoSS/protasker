import customtkinter as ctk

from utils.image_utils import get_image_as_tkimage
from views.components.tooltip import Tooltip


class SidebarView(ctk.CTkFrame):
    """ Define a barra lateral do workspace. """

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(fg_color="#2E333C", corner_radius=0)
        self.pack(side="left", anchor="nw", fill="y", padx=0, pady=0)

        self.tab_buttons = {}
        self.active_tab_id = None

        # Cores para estados
        self.active_fg = "#3E4D66"
        self.active_hover = "#4C5E7F"
        self.inactive_fg = "transparent"
        self.inactive_hover = "#3E4D66"

        # Define os botões
        buttons_config = [
            ("list-icon.png", "detalhes", "Detalhes"),
            ("checklist-icon.png", "controle", "Controle"),
            ("hand-raised-icon.png", "primeiros-passos", "Primeiros Passos")
        ]

        # Carrega os botões
        for icon, tab_id, tooltip in buttons_config:
            self._create_button(icon, tab_id)

    def _create_button(self, icon_path, tab_id):
        """Cria um botão para sidebar e atribui uma tab."""

        # Botão
        button = ctk.CTkButton(
            self,
            text='',
            image=get_image_as_tkimage(icon_path, size=20),
            width=30,
            height=30,
            fg_color="transparent",
            hover_color="#3E4D66",
            corner_radius=0,
            font=("Tahoma", 11),
            command=lambda: self._toggle_tab(tab_id)
        )
        button.pack(pady=(2, 0))
        Tooltip(button, tab_id)
        
        self.tab_buttons[tab_id] = button

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
            self.tab_buttons[tab_id].configure(fg_color=self.inactive_fg, hover_color=self.inactive_hover)
            self.active_tab_id = None
            return

        # Atualiza o estado ativo
        self.active_tab_id = tab_id

        # Muda a cor dos botões
        for tid, button in self.tab_buttons.items():
            if tid == tab_id:
                button.configure(fg_color=self.active_fg, hover_color=self.active_hover)
            else:
                button.configure(fg_color=self.inactive_fg, hover_color=self.inactive_hover)

    def show_details(self, item_info: dict):
        """
        Mostra a aba de detalhes atualizada com as informações do item selecionado.
        """

        # Troca para a aba "detalhes"
        if hasattr(self.master, "show_tab"):
            self.master.show_tab("detalhes")

        # Atualiza a aba "detalhes" com as informações do item
        details_tab = self.master.tabs.get("detalhes")
        if details_tab and hasattr(details_tab, "load_details"):
            details_tab.load_details(item_info)
