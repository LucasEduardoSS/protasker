from customtkinter import CTkFrame, CTkLabel, CTkButton
from peewee import IntegrityError

from services.data_facade import DataFacade

from views.windows.edit_view import EditView
from views.components.tooltip import Tooltip
from views.windows.alert_view import AlertView

from utils.widgets_utils import format_card_info
from utils.widgets_utils import propagate_hover_bind
from utils.image_utils import get_image_as_tkimage


class ListItem(CTkFrame):
    """ Define um item de lista de registros. """

    def __init__(self, master, model_info: dict, **kwargs):
        super().__init__(master, **kwargs)

        self.model = master.model
        self.model_info = model_info
        self._item_info_frame = None
        self.buttons = {}

        # Configuração do card
        self._normal_fg = "#3E4D66"
        self._hover_fg = "#465773"
        self.configure(fg_color="#3E4D66", border_color="#777", height=30)

        self.buttons_info = [
            {"tooltip": "Deletar", "command": None, "icon": get_image_as_tkimage("delete-icon.png", 20)},
            {"tooltip": "Detalhes", "command": None, "icon": get_image_as_tkimage("list-icon.png", 20)},
            {"tooltip": "Editar", "command": self._edit_record, "icon": get_image_as_tkimage("edit-icon.png", 20)}

        ]

        # Constrói os botões do card
        for button in self.buttons_info:
            button_widget = ListItemButton(self, icon=button["icon"], command=button["command"])
            Tooltip(button_widget, button["tooltip"])

            if not "total_tasks" in model_info or button["tooltip"] != "Editar":
                button_widget.pack(side="right", padx=0, pady=0)

            self.buttons[button["tooltip"]] = button_widget

        # Carrega os campos
        if model_info is not None or model_info == {}:
            self.load_fields(model_info)
        else:
            raise ValueError("model_info cannot be None")

    def load_fields(self, fields: dict):
        """Carrega os campos do card com os dados do registro."""

        # Limpa conteúdo anterior, se existir
        if self._item_info_frame is not None:
            self._item_info_frame.destroy()

        # Formata os dados do registro
        fields = format_card_info(fields)

        # Cria frame para os campos
        item_info_frame = CTkFrame(self)
        item_info_frame.pack(side="left", fill="x", expand=True)
        item_info_frame.configure(fg_color="transparent")
        self._item_info_frame = item_info_frame

        for field in fields.items():
            # Ignora campos vazios
            if field[1] is None:
                continue

            # Nome do campo
            name_lb = CTkLabel(
                self._item_info_frame,
                text=field[0]+":",
                fg_color="transparent",
                font=("Tahoma", 11, "bold"),
                height=20,
            )
            name_lb.pack(side="left", ipadx=10)

            # Valor do campo
            value_label = CTkLabel(
                self._item_info_frame,
                text=field[1],
                fg_color="transparent",
                font=("Tahoma", 11)
            )
            value_label.pack(side="left", padx=(0, 10))

        # Propaga o hover bind para todos os widgets do item
        propagate_hover_bind(self, self._hover_fg, self._normal_fg)

    def _edit_record(self):
        """Abre uma janela de edição do registro."""
        EditView(
            title="Editar registro",
            model_cls=self.model,
            model_info=self.model_info,
            on_save=self._apply_update
        )

    def _apply_update(self, updated_row: dict):
        """Chamado pela janela de edição após um save sucedido."""
        self.model_info = updated_row
        self.load_fields(updated_row)


class ListItemButton(CTkButton):
    def __init__(self, master, icon, command,  **kwargs):
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
