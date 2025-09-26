import customtkinter as ctk

from views.components.card import Card


class CardContainer(ctk.CTkScrollableFrame):
    def __init__(self, master, model, card_w=160, card_h=250, pad_x=4, pad_y=4, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(fg_color="transparent")
        self.cards = []     # Guarda os cards do container
        self.model = model  # Modelo

        self.card_w = card_w
        self.card_h = card_h
        self.pad_x = pad_x
        self.pad_y = pad_y

        # Recalcula layout sempre que o container muda de largura
        self._relayout_after_id = None
        self.bind("<Configure>", self._on_resize, add="+")

    def refresh_cards(self, data: list):
        """ Atualiza os campos dos cards do container. """
        for index, card in enumerate(self.cards):
            card.load_fields(data[index])
            card.model_info = data[index]

    def add_card(self, card_info: dict):
        """ Adiciona um novo card ao container. """
        card = Card(self, card_info)
        card.details_button.configure(command=lambda: self.master.master.master.master.show_item_details(self.model, card_info))
        card.delete_button.configure(command=lambda: card.remove_record(self.model))
        self.cards.append(card)
        self.relayout()

    def remove_card(self, card):
        self.cards.remove(card)
        self.relayout()

    def _on_resize(self, event):
        # Debounce: Reorganiza apenas após parar de mover por ~60ms
        if self._relayout_after_id:
            self.after_cancel(self._relayout_after_id)
        self._relayout_after_id = self.after(60, self.relayout)

    def relayout(self):
        """ Recalcula layout do container de cards. """
        self._relayout_after_id = None
        container_width = self.winfo_width()

        # calcula quantas colunas cabem
        max_cols = max(1, (container_width // (self.card_w + self.pad_x)) -1)

        for idx, card in enumerate(self.cards):
            row = idx // max_cols
            col = idx % max_cols
            card.grid(row=row, column=col,
                      padx=self.pad_x, pady=self.pad_y,
                      sticky="nw")
