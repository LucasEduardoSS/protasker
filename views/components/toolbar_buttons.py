import customtkinter as ctk
from PIL import Image

from views.windows.register_base_view import RegisterPersonView, RegisterTaskView, RegisterSectorView
from views.windows.distribution_view import DistributionView

IMAGES_PATH = "C:/Users/luedu/Documents/Projetos/Pycharm/ProTasker/images/"


class ToolbarBaseButtonView(ctk.CTkButton):
    """ Padroniza a criação de botões para toolbar_left """
    def __init__(self, master, tab_info: dict, **kwargs):
        super().__init__(master, **kwargs)

        # Dados da tab
        self.tab_info = tab_info

        # Configuração
        self.configure(
            width=25,
            height=25,
            font=("Tahoma", 11),
            corner_radius=0,
            hover_color="#3E4D66"
        )


class AddButton(ToolbarBaseButtonView):
    """ Adiciona um novo registro na aba atual. """
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        add_icon = ctk.CTkImage(
            light_image=Image.open(IMAGES_PATH + "add-icon.png"),
            dark_image=Image.open(IMAGES_PATH + "add-icon.png"),
            size=(20, 20)
        )

        self.configure(
            fg_color="transparent",
            text="",
            image=add_icon,
            command=self.add
        )
        self.pack(side="left", padx=2, pady=2, ipadx=2)

    def add(self):
        match self.tab_info["tab_name"]:
            case "Pessoas":
                RegisterPersonView(self.tab_info)
            case "Tarefas":
                RegisterTaskView(self.tab_info)
            case "Setores":
                RegisterSectorView(self.tab_info)
            case "Distribuições":
                DistributionView(self.tab_info)


class FilterButton(ToolbarBaseButtonView):
    """ Filtra os registros da aba atual. """
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        filter_icon = ctk.CTkImage(
            light_image=Image.open(IMAGES_PATH + "filter-icon.png"),
            dark_image=Image.open(IMAGES_PATH + "filter-icon.png"),
            size=(25, 25)
        )

        self.configure(
            fg_color="transparent",
            text="",
            image=filter_icon,
            command=self.filter
        )
        self.pack(side="left", padx=2, pady=2, ipadx=2)

    def filter(self):
        pass


class ViewModeSwitch(ctk.CTkSegmentedButton):
    """ Muda a visualização atual da aba."""
    def __init__(self, master, tab_info: dict, **kwargs):
        super().__init__(master, **kwargs)

        # Dados da tab
        self.tab_info = tab_info

        # Configuração
        self.configure(
            values=["Cards", "Lista"],
            font=("Tahoma", 11),
            border_width=0,
            corner_radius=0,
            selected_color="#2E333C",
            unselected_color="#2C2E33",
            selected_hover_color="#3E4D66",
            unselected_hover_color="#393E4A",
            fg_color="#2C2E33",
            command = self.on_mode_change,
        )

        # Ícones
        cards_icon = ctk.CTkImage(light_image=Image.open(IMAGES_PATH + "cards-icon.png"),
            dark_image=Image.open(IMAGES_PATH + "cards-icon.png"), size=(25, 25))
        list_icon = ctk.CTkImage(light_image=Image.open(IMAGES_PATH + "list-icon.png"),
            dark_image=Image.open(IMAGES_PATH + "list-icon.png"), size=(25, 25))

        self._buttons_dict["Cards"].configure(image=cards_icon, fg_color="transparent")
        self._buttons_dict["Lista"].configure(image=list_icon, fg_color="transparent")

        self.pack(side="right", padx=2, pady=2, ipadx=20)

        # Seta o switch no padrão configurado na tab
        self.set(self.tab_info["tab_meta"]["view_mode"])

    def on_mode_change(self, value: str):
        if value == "Cards":
            self.tab_info["tab_meta"]["list_container"].pack_forget()
            self.tab_info["tab_meta"]["cards_container"].pack(fill="both", expand=True)
            self.tab_info["tab_meta"]["view_mode"] = "Cards"
        else:
            self.tab_info["tab_meta"]["cards_container"].pack_forget()
            self.tab_info["tab_meta"]["list_container"].pack(fill="both", expand=True)
            self.tab_info["tab_meta"]["view_mode"] = "Lista"
