import customtkinter as ctk

from views.workspace.workspace_toolbar_view import WorkspaceToolbarView
from views.workspace.containers.card_container_view import CardContainer
from views.workspace.containers.list_container_view import ListContainer


class WorkspaceTabView(ctk.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(
            fg_color="#2E333C",
            bg_color="#2C2E33",
            border_width=5,
            border_color="#2E333C",
            segmented_button_fg_color="#2C2E33",
            segmented_button_selected_color="#2E333C",
            segmented_button_unselected_color="#2C2E33",
            anchor="w"
        )

        # Configura a fonte e o estilo dos botões
        self._segmented_button.configure(
            font=("Tahoma", 11),
            border_width=0,
            dynamic_resizing=True,
            selected_hover_color="#3E4D66",
            unselected_hover_color="#393E4A"
        )

        # Metadados por tab
        self.tabs_meta = {}  # name -> dict

    def add(self, name, **kwargs):
        # Cria a tab padrão do CTkTabview
        super().add(name)
        tab = self.tab(name)  # Pessoas, Tarefas, Setores e Distribuições

        # Guarda metadados da tab
        self.tabs_meta[name] = {
            "tab": tab,
            "toolbar": None,
            "toolbar_left": None,
            "toolbar_right": None,
            "content": None,
            "cards_container": None,
            "list_container": None,
            "view_switch": None,
            "view_mode": "Lista"
        }

        # Toolbar (topo da tab)
        toolbar = WorkspaceToolbarView(tab, name, fg_color=self.cget("bg_color"))

        # Área de conteúdo (abaixo da toolbar)
        content = ctk.CTkFrame(tab, fg_color="transparent")
        content.pack(side="top", pady=(10, 0), fill="both", expand=True)

        # Containers para modos de visualização
        cards_container = CardContainer(content, fg_color="transparent")
        list_container = ListContainer(content, fg_color="transparent")

        # Guarda metadados da tab
        self.tabs_meta[name].update({
            "toolbar": toolbar,
            "toolbar_left": toolbar.toolbar_left,
            "toolbar_right": toolbar.toolbar_right,
            "content": content,
            "cards_container": cards_container,
            "list_container": list_container,
            "view_switch": toolbar.view_mode_switch
        })

        # Constrói o container padrão
        toolbar.view_mode_switch.on_mode_change(self.tabs_meta[name]["view_mode"])
