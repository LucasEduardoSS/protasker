import customtkinter as ctk

from views.sidebar.tabs.first_steps_tab_view import FirstStepsTabView
from views.sidebar.tabs.control_tab_view import ControlTabView
from views.sidebar.tabs.details_tab_view import DetailsTabView


class SidebarTabView(ctk.CTkFrame):
    """ Define a tab base para as tabs da sidebar. """

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(width=100, fg_color="#2E333C", border_width=0)
        self.current_tab = None

        self.tabs = {
            "controle": ControlTabView(self),
            "detalhes": DetailsTabView(self),
            "primeiros-passos": FirstStepsTabView(self, show_refresh_btn=False)
        }

    def show_tab(self, tab_id):
        """ Carrega a aba selecionada. """

        # Esconde a aba atual se existir
        if self.current_tab:
            self.tabs[self.current_tab].pack_forget()

        # Mostra a nova aba
        self.current_tab = tab_id
        self.tabs[tab_id].pack(fill="both", expand=True)
