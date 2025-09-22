import customtkinter as ctk

from utils.image_utils import get_image_as_tkimage


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
    """ Define um botão de adicionar um registro. """

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(
            fg_color="transparent",
            text="",
            image=get_image_as_tkimage("add-icon.png", 20),
            command=None
        )
        self.pack(side="left", padx=2, pady=2, ipadx=2)


class FilterButton(ToolbarBaseButtonView):
    """ Define um botão de filtrar registros. """

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(
            fg_color="transparent",
            text="",
            image=get_image_as_tkimage("filter-icon.png", 20),
            command=None
        )
        self.pack(side="left", padx=2, pady=2, ipadx=2)


class ViewModeSwitch(ctk.CTkSegmentedButton):
    """ Define o botão de mudança de visualização dos registros."""

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

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
        self._buttons_dict["Cards"].configure(image=get_image_as_tkimage("cards-icon.png", 25), fg_color="transparent")
        self._buttons_dict["Lista"].configure(image=get_image_as_tkimage("list-icon.png", 25), fg_color="transparent")

        self.pack(side="right", padx=2, pady=2, ipadx=20)
