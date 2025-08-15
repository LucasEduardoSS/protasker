import customtkinter as ctk
from PIL import Image

from views.windows.base_window_view import BaseWindowView

# Project Config
GENERAL_FONT = ("Tahoma", 11)
IMAGES_PATH = "C:/Users/luedu/Documents/Projetos/Pycharm/ProTasker/images/"


class WorkspaceToolbarView(ctk.CTkFrame):
    """
    Cria a barra de ferramentas para as tabs do workspace onde podem ser
    adicionados botões e outros elementos. Nela há duas barras laterais: uma
    para os manipular os dados, e outra para manipular a visualização dos dados.
    Para cada tab existe uma Toolbar.
    """

    def __init__(self, master, tab_name, **kwargs):
        super().__init__(master, **kwargs)

        self.tab_info = {
            "tab_name": tab_name,
            "tab_master": master.master,  # WorkspaceTabView
            "tab_meta": master.master.tabs_meta[tab_name]
        }

        self.configure(
            #width=35,
            height=35,
            corner_radius=5,
            border_width=1,
            border_color="#555"
        )

        self.pack(side="top", fill="x", padx=5, pady=4)
        self.pack_propagate(False)

        # Lado esquerda da toolbar
        self.toolbar_left = ctk.CTkFrame(self, fg_color="transparent")
        self.toolbar_left.pack(side="left", padx=2, pady=2, anchor="w")

        # Espaçamento central
        self.spacer = ctk.CTkFrame(self, fg_color="transparent")
        self.spacer.pack(side="left", padx=2, pady=2, fill="x", expand=True)

        # Lado direito da toolbar
        self.toolbar_right = ctk.CTkFrame(self, fg_color="transparent")
        self.toolbar_right.pack(side="right", padx=2, pady=2, anchor="w")

        self.create_button("add-icon.png", 20, self.add)
        self.create_button("filter-filled-icon.png", 25, lambda: self.tab_info["tab_master"].toggle_filter_tab)
        self.view_mode_switch = self.create_view_mode_switch()

    def create_button(self, image: str, image_size: int, command):  # (Rascunho)
        """ Padroniza a criação de botões para toolbar_left """
        icon_image = ctk.CTkImage(
            light_image=Image.open(IMAGES_PATH + image),
            dark_image=Image.open(IMAGES_PATH + image),
            size=(image_size, image_size)
        )

        btn = ctk.CTkButton(
            master=self.toolbar_left,
            text="",
            image=icon_image,
            width=30,
            height=30,
            font=GENERAL_FONT,
            corner_radius=0,
            fg_color="#2C2E33",
            hover_color="#3E4D66",
            command=command
        )
        btn.pack(
            side="left",
            padx=2,
            pady=2
        )

        return btn

    def create_view_mode_switch(self):
        view_switch = ctk.CTkSegmentedButton(
            master=self.toolbar_right,
            values=["Cards", "Lista"],
            font=GENERAL_FONT,
            border_width=0,
            corner_radius=0,
            selected_hover_color="#5A5E68",
            unselected_hover_color="#393E4A",
            fg_color="#2C2E33",
            command = self._on_mode_change,
        )

        cards_icon = ctk.CTkImage(light_image=Image.open(IMAGES_PATH + "cards-icon.png"),
            dark_image=Image.open(IMAGES_PATH + "cards-icon.png"), size=(25, 25))
        list_icon = ctk.CTkImage(light_image=Image.open(IMAGES_PATH + "list-icon.png"),
            dark_image=Image.open(IMAGES_PATH + "list-icon.png"), size=(25, 25))

        view_switch._buttons_dict["Cards"].configure(image=cards_icon, fg_color="transparent")
        view_switch._buttons_dict["Lista"].configure(image=list_icon, fg_color="transparent")

        view_switch.pack(
            side="right",
            padx=2,
            pady=2,
            ipadx=20
        )
        return view_switch

    def _on_mode_change(self, value: str):
        if value == "Cards":
            self.tab_info["tab_meta"]["list_container"].pack_forget()
            self.tab_info["tab_meta"]["cards_container"].pack(fill="both", expand=True)
            self.tab_info["tab_meta"]["view_mode"] = "Cards"
        else:
            self.tab_info["tab_meta"]["cards_container"].pack_forget()
            self.tab_info["tab_meta"]["list_container"].pack(fill="both", expand=True)
            self.tab_info["tab_meta"]["view_mode"] = "Lista"

    def add(self):

        match self.tab_info["tab_name"]:
            case "Pessoas":
                BaseWindowView(self.tab_info, "Cadastrar Pessoa")
            case "Tarefas":
                BaseWindowView(self.tab_info, "Cadastrar Tarefa")
            case "Setores":
                BaseWindowView(self.tab_info, "Cadastrar Setor")
            case "Distribuições":
                pass
