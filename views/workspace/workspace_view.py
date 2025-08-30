import tkinter as ttk
from views.workspace.workspace_tab_view import WorkspaceTabView
from views.sidebar.sidebar_tab_view import SidebarTabView


class WorkspaceView(ttk.PanedWindow):
    """Painel que divide as tabs da sidebar e do workspace."""
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
        self.sidebar_tabs_visible = True

        # Tabs da sidebar
        self.sidebar_tabs = SidebarTabView(self)
        self.sidebar_tabs.setup_tabs()

        # Mostra os primeiros-passos na inicialização
        self.add(self.sidebar_tabs, minsize=100, width=300)
        self.sidebar_tabs.show_tab('primeiros-passos')

        # Workspace tabs
        self.workspace_tabs = WorkspaceTabView(self)
        self.add(self.workspace_tabs)

        # Criando as abas principais
        self.workspace_tabs.add("Distribuições")
        self.workspace_tabs.add("Tarefas")
        self.workspace_tabs.add("Pessoas")
        self.workspace_tabs.add("Setores")

        self.workspace_tabs.load_data("Distribuições")
        self.workspace_tabs.load_data("Tarefas")
        self.workspace_tabs.load_data("Pessoas")
        self.workspace_tabs.load_data("Setores")

        # Ajustes finos do Workspace
        self.workspace_tabs.configure(corner_radius=0)
        self.workspace_tabs.grid_rowconfigure(2, minsize=0)
        self.workspace_tabs._segmented_button.grid(row=0, column=0, sticky="w", ipadx=20)

        # Conteúdo
        self.content_meta = {
            "sidebar_tabs": self.sidebar_tabs,
            "workspace": self.workspace_tabs
        }

    def toggle_sidebar_tabs(self, tab_id):
        """ Metodo para gerenciar a exibição das tabs da sidebar. Adiciona
        as tabs antes do workspace. """

        if not self.sidebar_tabs_visible:
            # Remove temporariamente o workspace
            self.forget(self.workspace_tabs)

            # Adiciona as tabs
            self.add(self.sidebar_tabs, minsize=100, width=300)

            # Readiciona o workspace
            self.add(self.workspace_tabs)
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
