from customtkinter import CTkFrame, CTkButton, CTkToplevel

from views.components.card import Card
from views.components.list_item import ListItem


class EditBaseWindowView(CTkToplevel):
    def __init__(self, tab_info: dict, **kwargs):
        super().__init__(**kwargs)
        self.configure(fg_color="#2E333C")
        self.iconbitmap("images/protasker_icon.ico")

        # Mantém sobre a janela principal
        self.grab_set()
        self.lift()
        self.focus_force()

        # Frame principal
        self.main_frame = CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(padx=5, pady=5, fill="both", expand=True)

        self.tab_info = tab_info
        self.entries = {}
        self.data = None
        self.model = self.tab_info["tab_meta"]["model"]

    def _build(self, entries: dict):
        # Posiciona os campos
        for widget in entries.values():
            widget.pack(side="top", anchor="nw", fill="x", padx=10, pady=5)

        # Botão de salvar
        btn = CTkButton(self, height=30, text="Salvar", font=("Tahoma", 11), command=self._on_save)
        btn.pack(side="top", anchor="s", padx=10, pady=10, fill="x", expand=True)

    def get_data(self) -> dict:
        """Retorna um dict com os valores atuais do formulário."""
        data = {}
        for name, widget in self.entries.items():
           data[name] = widget.get()
        return data

    def _on_save(self):
        self.data = self.get_data()

        # Cria um card
        card = Card(self.tab_info["tab_meta"]["cards_container"], self.data)
        self.tab_info["tab_meta"]["cards_container"].add_card(card)

        # Cria um item na lista
        list_item = ListItem(self.tab_info["tab_meta"]["list_container"], self.data)
        self.tab_info["tab_meta"]["list_container"].add_item(list_item)

        # Registra no banco de dados (somente se houver model válido)
        if self.model is not None:
            self.model.create(**self.data)
        else:
            # Caso o model não tenha sido injetado, evita crash e informa no console
            print("Aviso: nenhum 'model' foi fornecido em tab_info; dados não foram persistidos.")

        # fecha a janela ou limpa campos
        self.destroy()
