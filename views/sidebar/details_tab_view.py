from customtkinter import CTkFrame, CTkLabel
from views.sidebar.sidebar_base_tab_view import SidebarBaseTabView


class DetailsTabView(SidebarBaseTabView):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.label.configure(text="Detalhes")
