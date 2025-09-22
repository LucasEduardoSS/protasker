from customtkinter import CTkFrame, CTkLabel

from views.components.edit_button import EditButton
from views.windows.edit_view import EditView

from utils.widgets_utils import format_card_info
from utils.widgets_utils import propagate_hover_bind


class Record(CTkFrame):
    """
    Widget para exibir um registro.
    Pode ser configurado como card ou item.
    """

    def __init__(self, master, model, model_info: dict, mode: str, **kwargs):
        super().__init__(master, **kwargs)

        # Atributos
        self.mode = mode
        self.model = model
        self.model_info = model_info

        # Widgets
        self.field_labels = []
        self.field_values = []

        # Configuração comum
        self.configure(fg_color="#3E4D66")

        # Carrega os campos, se fornecido
        if model_info is not None or model_info == {}:
            self.build_fields(model_info)
        else:
            raise ValueError("model_info cannot be None")

        # Cores
        self._normal_fg = "#3E4D66"
        self._hover_fg = "#465773"

        # Propaga o hover bind para todos os widgets do item
        propagate_hover_bind(self, self._hover_fg, self._normal_fg)

    def build_fields(self, fields: dict):
        """Carrega os campos do card com os dados do registro."""

        # Formata os dados do registro
        fields = format_card_info(fields)

        for key, value in fields.items():
            # Ignora campos vazios
            if value is None:
                continue

            # Nome do campo
            self.field_labels.append(CTkLabel(
                self,
                text=key+":",
                fg_color="transparent",
                font=("Tahoma", 11, "bold"),
                height=20,
            ))

            # Valor do campo
            self.field_values.append(CTkLabel(
                self,
                text=value,
                fg_color="transparent",
                font=("Tahoma", 11)
            ))

    def edit_record(self):
        """Abre uma janela de edição do registro."""
        EditView(
            model_cls=self.model,
            model_info=self.model_info,
            on_save=self._apply_update
        )

    @staticmethod
    def _apply_update(record, updated_row: dict):
        """Chamado pela janela de edição após um save sucedido."""
        record.model_info = updated_row
        record.load_fields(updated_row)


class Card(Record):
    """ Define um card de registro. """

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Configuração do card
        self.configure(height=250, width=175)

        # Configuração do Grid Layout
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=0, minsize=30)

        # Impede que os widgets redimensionem o card
        self.grid_propagate(False)

        # Botão de editar registro
        edit_button = EditButton(self, text="", command=self.edit_record)
        edit_button.grid(row=0, column=1, padx=5, pady=5, sticky="n")

    def load_fields(self):
        """Carrega os campos do card com os dados de um registro."""

        for i in range(len(self.field_labels)):
            self.field_labels[i].pack(side="top", anchor="w", padx=5, pady=(5, 0), fill="x", expand=True)
            self.field_values[i].pack(side="top", anchor="w", padx=5, pady=4, fill="x", expand=True)


class ListItem(Record):
    """ Define um item de lista de registros. """

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(height=30)

        # Botão de editar registro
        edit_button = EditButton(self, text="Editar", command=self.edit_record)
        edit_button.pack(side="right", padx=(0, 5))

    def load_fields(self):
        """Carrega os campos do registro."""

        for i in range(len(self.field_labels)):
            self.field_labels[i].pack(side="left", ipadx=10)
            self.field_values[i].pack(side="left", ipadx=(0, 10))
