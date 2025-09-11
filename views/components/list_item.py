from customtkinter import CTkFrame, CTkLabel

from views.components.edit_button import EditButton
from utils.format_card_info import format_card_info


class ListItem(CTkFrame):
    def __init__(self, master, model_info: dict, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="#3E4D66", border_color="#777", height=30)

        # Botão de editar registro
        edit_button = EditButton(self, text="Editar")
        edit_button.pack(side="right", padx=(0, 5))

        self.load_fields(format_card_info(model_info))

    def load_fields(self, fields: dict):
        """Carrega os campos do card com os dados do registro."""
        for field in fields.items():
            # Ignora campos vazios
            if field[1] is None:
                continue

            # Nome do campo
            name_lb = CTkLabel(
                self,
                text=field[0]+":",
                fg_color="transparent",
                font=("Tahoma", 11, "bold"),
                height=20,
            )
            name_lb.pack(side="left", ipadx=10)

            # Valor do campo
            value_label = CTkLabel(self, text=field[1], fg_color="transparent", font=("Tahoma", 11))
            value_label.pack(side="left", padx=(0, 10))

    def edit_record(self):
        pass

    def toggle_filter_tab(self):
        pass
