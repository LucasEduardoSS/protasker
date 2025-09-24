import customtkinter as ctk

from views.sidebar.tabs.sidebar_base_tab_view import SidebarBaseTabView


class DetailsTabView(SidebarBaseTabView):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.label.configure(text="Detalhes")

    def load_details(self, item_info: dict):
        """ Atualiza a visualização dos detalhes com as informações do item selecionado. """

        # Limpa todos os itens
        for widget in self.winfo_children():
            if widget == self.tab_top_bar:
                continue
            widget.destroy()

        # Exibe as informações do item
        for key, value in item_info.items():
            if value is not None and value != "":
                label = ctk.CTkLabel(self, text=f"{key}: {value}", anchor="w", font=("Tahoma", 11))
                label.pack(fill="x", padx=10, pady=5)
