import customtkinter as ctk


class CardContainer(ctk.CTkScrollableFrame):
    def __init__(self, master, card_w=160, card_h=250, pad_x=4, pad_y=4, **kwargs):
        super().__init__(master, **kwargs)

        self.card_w = card_w
        self.card_h = card_h
        self.pad_x = pad_x
        self.pad_y = pad_y

        # Guarda os cards do container
        self.cards = []

        # Recalcula layout sempre que o container muda de largura
        self.bind("<Configure>", lambda e: self.relayout())

    def add_card(self, card: ctk.CTkFrame):
        """ Adiciona um novo card ao container """
        self.cards.append(card)

    def relayout(self):
        """ Recalcula layout do container de cards """
        container_width = self.winfo_width()

        # calcula quantas colunas cabem
        max_cols = max(1, (container_width // (self.card_w + self.pad_x)) -1)

        for idx, card in enumerate(self.cards):
            row = idx // max_cols
            col = idx % max_cols
            card.grid(row=row, column=col,
                      padx=self.pad_x, pady=self.pad_y,
                      sticky="nw")
