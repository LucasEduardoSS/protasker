import customtkinter as ctk
from PIL import Image

IMAGES_PATH = "C:/Users/luedu/Documents/Projetos/Pycharm/ProTasker/images/"


class ToolbarBaseButtonView(ctk.CTkButton):
    """ Padroniza a criação de botões para toolbar_left """
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

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
            command=None
        )
        self.pack(side="left", padx=2, pady=2, ipadx=2)


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
            command=None
        )
        self.pack(side="left", padx=2, pady=2, ipadx=2)


class ViewModeSwitch(ctk.CTkSegmentedButton):
    """ Muda a visualização atual da aba."""
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Ícones
        cards_icon = ctk.CTkImage(light_image=Image.open(IMAGES_PATH + "cards-icon.png"),
                                  dark_image=Image.open(IMAGES_PATH + "cards-icon.png"), size=(25, 25))
        list_icon = ctk.CTkImage(light_image=Image.open(IMAGES_PATH + "list-icon.png"),
                                 dark_image=Image.open(IMAGES_PATH + "list-icon.png"), size=(25, 25))

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
            command = None,
        )

        # Adiciona os ícones após configuração inicial para evitar fundo branco
        self._buttons_dict["Cards"].configure(image=cards_icon, fg_color="transparent")
        self._buttons_dict["Lista"].configure(image=list_icon, fg_color="transparent")

        self.pack(side="right", padx=2, pady=2, ipadx=20)
