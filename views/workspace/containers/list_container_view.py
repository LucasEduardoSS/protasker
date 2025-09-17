from customtkinter import CTkScrollableFrame

from views.components.list_item import ListItem


class ListContainer(CTkScrollableFrame):
    """
    Define um container de itens de lista.
    Recebe um modelo/tabela de dados.
    """

    def __init__(self, master, model, **kwargs):
        super().__init__(master, **kwargs)

        self.model = model
        self.configure(fg_color="transparent")

        # Lista de itens
        self.list_items = []

    def load_items(self, model: list):
        """ Carrega itens ao container """
        for item in model:
            self.list_items.append(ListItem(self, item))
        self.relayout()

    def refresh_items(self, data: list):
        """ Atualiza os campos dos itens do container. """
        for index, item in enumerate(self.list_items):
            item.load_fields(data[index])
            item.model_info = data[index]

    def add_item(self, item_info: dict):
        """ Adiciona um novo item ao container """
        item = ListItem(self, item_info)
        item.pack(anchor="nw", side="top", fill="x", padx=(0, 10), pady=5)
        self.list_items.append(item)
        #self.relayout()

    def relayout(self):
        """ Recalcula layout do container de itens """

        # Limpa todos os itens
        for widget in self.winfo_children():
            widget.pack_forget()

        # Reposiciona todos os itens em ordem
        for item in self.list_items:
            item.pack(anchor="nw", side="top", fill="x", padx=(0, 10), pady=5)
