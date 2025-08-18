import customtkinter as ctk
from time import sleep


# CardContainer Horizontal
"""class CardContainer(ctk.CTkScrollableFrame):
    def __init__(self, master,
                 card_w=150, card_h=250,
                 pad_x=4, pad_y=4, **kwargs):
        super().__init__(master, **kwargs)

        self.card_w = card_w  # card width
        self.card_h = card_h  # card height
        self.pad_x = pad_x
        self.pad_y = pad_y

        # guarda os cards do container
        self.cards = []

        # não deixa o frame encolher para caber os filhos
        self._parent_frame.grid_propagate(False)

        # sempre que mudar de tamanho, relayout
        self.bind("<Configure>", lambda e: self._relayout())

    def add_card(self, card: ctk.CTkFrame):
        # assume que o card já foi criado com master=self
        self.cards.append(card)
        self._relayout()

    def _relayout(self):
        h = self.winfo_height()

        # quantos cards cabem verticalmente
        max_rows = max(1, (h + self.pad_y) // (self.card_h + self.pad_y))

        # posiciona os cards
        for idx, card in enumerate(self.cards):
            row = idx % max_rows
            col = idx // max_rows            
            card.grid(row=row, column=col,
                      padx=self.pad_x, pady=self.pad_y,
                      sticky="nw") """

# Card Container vertical
class CardContainer(ctk.CTkScrollableFrame):
    def __init__(self, master,
                 card_w=160, card_h=250,
                 pad_x=4, pad_y=4,
                 **kwargs):
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
        # card deve ter master=self e não chamar pack() internamente
        self.cards.append(card)

    def relayout(self):
        container_width = self.winfo_width()

        # calcula quantas colunas cabem
        max_cols = max(1, (container_width // (self.card_w + self.pad_x)) -1)
        print(container_width, max_cols)

        for idx, card in enumerate(self.cards):
            row = idx // max_cols
            col = idx % max_cols
            print(idx, row, col)
            card.grid(row=row, column=col,
                      padx=self.pad_x, pady=self.pad_y,
                      sticky="nw")
