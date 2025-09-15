import customtkinter as ctk

from views.components.edit_button import EditButton
from views.windows.edit_view import EditBaseWindowView
from utils.format_card_info import format_card_info


class Card(ctk.CTkFrame):
    def __init__(self, master, model_info: dict | None = None, **kwargs):
        super().__init__(master, **kwargs)

        # Informações do card
        self.model_info = model_info
        self.model = master.model

        # Configuração do card
        self._normal_fg = "#3E4D66"
        self._hover_fg = "#465773"
        self.configure(
            fg_color="#3E4D66",
            border_color="#777",
            border_width=1,
            corner_radius=0,
            height=250,
            width=175
        )

        # Configuração do Grid Layout
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=0, minsize=30)

        # Impede que os widgets redimensionem o card
        self.grid_propagate(False)

        # Botão de editar registro
        edit_button = EditButton(self, text="", command=self.edit_card)
        edit_button.grid(row=0, column=1, padx=5, pady=5, sticky="n")

        # Hover leve (evita mudança contínua em <Motion>)
        self.bind("<Enter>", lambda e: self.configure(fg_color=self._hover_fg))
        self.bind("<Leave>", lambda e: self.configure(fg_color=self._normal_fg))

        # Frame que conterá os campos (reutilizado)
        self._card_info_frame = None

        # Carrega os campos, se fornecido
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

        card_info_frame = ctk.CTkFrame(self)
        card_info_frame.grid(row=0, column=0, padx=5, pady=5, ipadx=2, ipady=2, sticky="nsew")
        card_info_frame.configure(fg_color="transparent")
        self._card_info_frame = card_info_frame

        for key, value in fields.items():
            # Ignora campos com valores vazios
            if value is None or value == "":
                continue

            # Ignora o ID
            if key == "id":
                continue

            # Nome do campo
            lb = ctk.CTkLabel(
                card_info_frame,
                text=str(key) + ":",
                fg_color="transparent",
                font=("Tahoma", 11, "bold"),
                height=10,
                anchor="w",
                justify="left",
            )
            lb.pack(side="top", anchor="w", padx=5, pady=(5, 0), fill="x", expand=True)

            # Valor do campo
            lb = ctk.CTkLabel(
                card_info_frame,
                text=str(value),
                fg_color="transparent",
                font=("Tahoma", 11),
                height=10,
                anchor="w",
                justify="left",
            )
            lb.pack(side="top", anchor="w", padx=5, pady=4, fill="x", expand=True)

    def edit_card(self):
        """Abre uma janela de edição do registro."""
        EditBaseWindowView(
            model_cls=self.model,
            model_info=self.model_info,
            on_save=self._apply_update
        )

    def _apply_update(self, updated_row: dict):
        """Called by the edit window after a successful save."""
        self.model_info = updated_row
        self.load_fields(updated_row)
