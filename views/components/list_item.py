from customtkinter import CTkFrame, CTkLabel

from views.components.edit_button import EditButton
from views.windows.edit_view import EditView

from utils.widgets_utils import format_card_info
from utils.widgets_utils import propagate_hover_bind


class ListItem(CTkFrame):
    """ Define um item de lista de registros. """

    def __init__(self, master, model_info: dict, **kwargs):
        super().__init__(master, **kwargs)

        self.model = master.model
        self.model_info = model_info
        self._item_info_frame = None

        # Configuração do card
        self._normal_fg = "#3E4D66"
        self._hover_fg = "#465773"
        self.configure(fg_color="#3E4D66", border_color="#777", height=30)

        # Botão de editar registro
        edit_button = EditButton(self, text="Editar", command=self.edit_record)
        edit_button.pack(side="right", padx=(0, 5))

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

    def edit_record(self):
        """Abre uma janela de edição do registro."""
        EditView(
            model_cls=self.model,
            model_info=self.model_info,
            on_save=self.apply_update
        )

    def apply_update(self, updated_row: dict):
        """Chamado pela janela de edição após um save sucedido."""
        self.model_info = updated_row
        self.load_fields(updated_row)

    def toggle_filter_tab(self):
        pass
