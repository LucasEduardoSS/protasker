from customtkinter import CTkScrollableFrame


class ListContainer(CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Lista de itens
        self.list_items = []

    def add_item(self, item):
        """ Adiciona um novo item ao container """
        self.list_items.append(item)
        self.relayout()

    def relayout(self):
        """ Recalcula layout do container de itens """
        # 1) Limpa todos os itens
        for widget in self.winfo_children():
            widget.pack_forget()

        # 2) Reposiciona todos os itens em ordem
        for item in self.list_items:
            item.pack(anchor="nw", side="top", fill="x", padx=(0, 10), pady=5)
