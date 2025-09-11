import customtkinter as ctk
from views.sidebar.tabs.first_steps_tab_view import FirstStepsTabView
from views.sidebar.tabs.control_tab_view import ControlTabView
from views.sidebar.tabs.details_tab_view import DetailsTabView

class SidebarTabView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(width=100, fg_color="#2E333C", border_width=0)
        self.current_tab: str = 'primeiros-passos'
        self.tabs = {}

    def setup_tabs(self):
        # Criar os frames para cada aba
        self.tabs = {
            "controle": ControlTabView(self),
            "detalhes": DetailsTabView(self),
            "primeiros-passos": FirstStepsTabView(self)
        }

    def show_tab(self, tab_id):
        """ Mostra a aba selecionada. Funciona como uma extensão
        da funçao toggle_sidebar_tabs neste escopo. """

        # Esconde a aba atual se existir
        if self.current_tab:
            self.tabs[self.current_tab].pack_forget()

        # Mostra a nova aba
        self.current_tab = tab_id
        self.tabs[tab_id].pack(fill="both", expand=True)
