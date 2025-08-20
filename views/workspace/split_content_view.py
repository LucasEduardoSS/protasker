import tkinter as ttk
from views.workspace.workspace_tab_view import WorkspaceTabView
from views.sidebar.sidebar_tab_view import SidebarTabView


class SplitContentView(ttk.PanedWindow):
    def __init__(self, master):
        super().__init__(master)

        self.configure(
            orient="horizontal",
            borderwidth=4,
            sashwidth=2,
            sashpad=2,
            bg="#3F3F3F",
            showhandle=False,
            opaqueresize=False
        )
        self.pack(fill="both", expand=True)

        # Controle se há aba visível
        self.sidebar_tabs_visible = False

        # Tabs da sidebar (inicialmente oculto)
        self.sidebar_tabs = SidebarTabView(self)

        # Workspace
        self.workspace = WorkspaceTabView(self)
        self.add(self.workspace)

        # Criando as abas principais
        self.workspace.add("Tarefas")
        self.workspace.add("Pessoas")
        self.workspace.add("Setores")
        self.workspace.add("Distribuições")

        # Ajustes finos do Workspace
        self.workspace.configure(corner_radius=0)
        self.workspace.grid_rowconfigure(2, minsize=0)
        self.workspace._segmented_button.grid(row=0, column=0, sticky="w", ipadx=20)

    def toggle_sidebar_tabs(self, tab_id):
        """ Método para gerenciar a exibição das tabs da sidebar. Adiciona
        as tabs antes do workspace. """

        if not self.sidebar_tabs_visible:
            # Remove temporariamente o workspace
            self.forget(self.workspace)

            # Adiciona as tabs
            self.add(self.sidebar_tabs, minsize=100, width=300)

            # Readiciona o workspace
            self.add(self.workspace)
            self.sidebar_tabs_visible = True
            self.sidebar_tabs.show_tab(tab_id)
        else:
            if self.sidebar_tabs.current_tab == tab_id:
                # Remove as tabs
                self.forget(self.sidebar_tabs)
                self.sidebar_tabs_visible = False
            else:
                # Apenas muda a aba
                self.sidebar_tabs.show_tab(tab_id)
