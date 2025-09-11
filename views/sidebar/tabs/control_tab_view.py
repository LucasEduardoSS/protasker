from views.sidebar.tabs.sidebar_base_tab_view import SidebarBaseTabView


class ControlTabView(SidebarBaseTabView):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.label.configure(text="Controle")
