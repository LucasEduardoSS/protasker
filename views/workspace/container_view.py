from customtkinter import CTkScrollableFrame

from views.components.record_view import Record

""" Classes criadas pensando na unificação dos containers e
    no uso da classe Record. """


class Container(CTkScrollableFrame):
    """
    Define um container de registros.
    Recebe um modelo/tabela de dados.
    Pode ser configurado para cards ou itens.
    """

    def __init__(self, master, model, mode: str, **kwargs):
        super().__init__(master, **kwargs)

        self.mode = mode
        self.model = model
        self.configure(fg_color="transparent")

        # Lista de itens
        self.records = []

    def load_records(self, records_info: list):
        """ Carrega registros no container """
        for info in records_info:
            self.records.append(Record(self, self.model, info, self.mode))
        self.relayout()

    def refresh_records(self, data: list):
        """ Atualiza os campos dos registros do container. """
        for index, record in enumerate(self.records):
            record.load_fields(data[index])
            record.model_info = data[index]

    def add_record(self, record_info: dict):
        """ Adiciona um novo registro ao container """
        self.records.append(Record(self, self.model, record_info, self.mode))
        self.relayout()

    def relayout(self):
        pass


class CardContainer(Container):
    def __init__(self, master, model, card_w=160, card_h=250, pad_x=4, pad_y=4, **kwargs):
        super().__init__(master, **kwargs)

        self.model = model

        self.card_w = card_w
        self.card_h = card_h
        self.pad_x = pad_x
        self.pad_y = pad_y

        # Recalcula layout sempre que o container muda de largura
        self._relayout_after_id = None
        self.bind("<Configure>", self._on_resize, add="+")

    def _on_resize(self, event):
        # Debounce: Reorganiza apenas após parar de mover por ~60ms
        if self._relayout_after_id:
            self.after_cancel(self._relayout_after_id)
        self._relayout_after_id = self.after(60, self.relayout)

    def relayout(self):
        """ Recalcula layout do container de cards """
        self._relayout_after_id = None
        container_width = self.winfo_width()

        # calcula quantas colunas cabem
        max_cols = max(1, (container_width // (self.card_w + self.pad_x)) -1)

        for idx, card in enumerate(self.records):
            row = idx // max_cols
            col = idx % max_cols
            card.grid(row=row, column=col,
                      padx=self.pad_x, pady=self.pad_y,
                      sticky="nw")


class ListContainer(Container):
    """
    Define um container de itens de lista.
    Recebe um modelo/tabela de dados.
    """

    def __init__(self, master, model, **kwargs):
        super().__init__(master, **kwargs)

        self.model = model

    def relayout(self):
        """ Recalcula layout do container de itens """

        # Limpa todos os itens
        for widget in self.winfo_children():
            widget.pack_forget()

        # Reposiciona todos os itens em ordem
        for item in self.list_items:
            item.pack(anchor="nw", side="top", fill="x", padx=(0, 10), pady=5)
