from customtkinter import CTkFrame, CTkLabel

from views.components.pro_widgets import ProButton
from utils.image_utils import get_image_as_tkimage


class SidebarBaseTabView(CTkFrame):
    """ Define uma base para as tabs da sidebar no workspace. """

    def __init__(self, master, show_refresh_btn: bool = True, **kwargs):
        super().__init__(master, **kwargs)

        # Configuração da base
        self.configure(fg_color="transparent", corner_radius=0)

        self.tab_top_bar = CTkFrame(
            self,
            fg_color = "#2C2E33",
            height = 25,
            corner_radius = 0,
            border_width = 0
        )
        self.tab_top_bar.pack(side="top", fill="x", pady=(0, 10))
        self.tab_top_bar.pack_propagate(False)

        # Título da tab
        self.label = CTkLabel(self.tab_top_bar, text="title", font=("Tahoma", 11))
        self.label.pack(side="left", padx=(10, 0))

        # Botão de refresh
        self.refresh_btn = ProButton(
            self.tab_top_bar,
            text="",
            height=15,
            width=15,
            image=get_image_as_tkimage("refresh-icon.png", 20)
        )
        if show_refresh_btn:
            self.refresh_btn.pack(side="right", padx=(10, 0))
