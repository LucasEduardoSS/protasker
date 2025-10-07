import customtkinter as ctk
from peewee import IntegrityError

from services.data_facade import DataFacade

from views.windows.edit_view import EditView
from views.windows.alert_view import AlertView
from views.components.tooltip import Tooltip

from utils.widgets_utils import format_card_info
from utils.widgets_utils import propagate_hover_bind
from utils.image_utils import get_image_as_tkimage


class Card(ctk.CTkFrame):
    """ Define um card de registro. """

    def __init__(self, master, model_info: dict | None = None, **kwargs):
        super().__init__(master, **kwargs)

        # Informações do card
        self.model_info = model_info
        self.buttons = {}

        # Configuração do card
        self._normal_fg = "#3E4D66"
        self._hover_fg = "#465773"
        self.configure(
            fg_color="#3E4D66",
            border_color="#777",
            border_width=0,
            corner_radius=5,
            height=250,
            width=175
        )

        # Configuração do Grid Layout
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=0, minsize=30)
        self.grid_propagate(False)

        buttons_frame = ctk.CTkFrame(self, height=250, width=30, fg_color="transparent")
        buttons_frame.grid(row=0, column=1, padx=2, pady=4, sticky="nsew")

        self.buttons_info = [
            {"tooltip": "Editar", "command": self._edit_record, "icon": get_image_as_tkimage("edit-icon.png", 20)},
            {"tooltip": "Detalhes", "command": None, "icon": get_image_as_tkimage("list-icon.png", 20)},
            {"tooltip": "Deletar", "command": None, "icon": get_image_as_tkimage("delete-icon.png", 20)}
        ]

        # Constrói os botões do card
        for button in self.buttons_info:
            button_widget = CardButton(buttons_frame, icon=button["icon"], command=button["command"])
            Tooltip(button_widget, button["tooltip"])

            if not "total_tasks" in model_info or button["tooltip"] != "Editar":
                button_widget.pack(side="top", padx=0, pady=2)

            self.buttons[button["tooltip"]] = button_widget

        # Frame que conterá os campos (reutilizado)
        self._card_info_frame = None

        # Carrega os campos
        if model_info is not None or model_info == {}:
            self.load_fields(model_info)
        else:
            raise ValueError("model_info cannot be None")

    def load_fields(self, fields: dict):
        """Carrega os campos do card com os dados de um registro."""

        # Limpa conteúdo anterior, se existir
        if self._card_info_frame is not None:
            self._card_info_frame.destroy()

        # Formata os dados do registro
        fields = format_card_info(fields)

        # Cria frame para os campos
        card_info_frame = ctk.CTkFrame(self, height=self.cget("height") - 15)
        card_info_frame.grid(row=0, column=0, padx=5, pady=5, ipadx=2, ipady=2, sticky="nsew")
        card_info_frame.configure(fg_color="transparent")
        card_info_frame.pack_propagate(False)
        self._card_info_frame = card_info_frame

        for index, (key, value) in enumerate(fields.items()):
            # Ignora campos com valores vazios
            if value is None or value == "":
                continue

            # Ignora o ID
            if key == "id":
                continue

            # Nome do campo
            lb = ctk.CTkLabel(
                self._card_info_frame,
                text=str(key) + ":",
                fg_color="transparent",
                font=("Tahoma", 11, "bold"),
                height=10,
                anchor="w",
                justify="left",
            )
            lb.pack(side="top", anchor="w", padx=5, pady=(5, 0), fill="x")

            # Valor do campo
            lb = ctk.CTkLabel(
                self._card_info_frame,
                text=str(value),
                fg_color="transparent",
                font=("Tahoma", 11),
                height=10,
                anchor="w",
                justify="left",
            )
            lb.pack(side="top", anchor="w", padx=5, pady=4, fill="x")

        # Propaga o hover bind para todos os widgets do item
        propagate_hover_bind(self, self._hover_fg, self._normal_fg)

    def _edit_record(self):
        """Abre uma janela de edição do registro."""

        EditView (
            title="Editar registro",
            model_cls=self.master.model,
            model_info=self.model_info,
            on_save=self._apply_update
        )

    def _apply_update(self, updated_row: dict):
        """Chamado pela janela de edição após um save sucedido."""
        self.model_info = updated_row
        self.load_fields(updated_row)


class CardButton(ctk.CTkButton):
    def __init__(self, master, icon, command, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(
            text="",
            width=30,
            height=20,
            font=("Tahoma", 11),
            image=icon,
            fg_color="transparent",
            hover_color="#3E4D66",
            command=command
        )
