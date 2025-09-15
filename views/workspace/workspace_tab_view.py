import customtkinter as ctk

from views.workspace.workspace_toolbar_view import WorkspaceToolbarView
from views.workspace.containers.card_container_view import CardContainer
from views.workspace.containers.list_container_view import ListContainer

from views.windows.distribution_view import DistributionView
from views.windows.edit_view import EditBaseWindowView


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

    def add(self, name, model=None, **kwargs):
        """Adiciona uma nova tab ao CTkTabview."""

        # Cria a tab padrão do CTkTabview
        super().add(name)

        tab = self.tab(name)

        # Guarda metadados da tab
        self.tabs_meta[name] = {
            "tab": tab,
            "model": model,
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
        cards_container = CardContainer(content, model, fg_color="transparent")
        list_container = ListContainer(content, fg_color="transparent")

        # Guarda metadados da tab
        self.tabs_meta[name].update({
            "toolbar": toolbar,
            "toolbar_left": toolbar.toolbar_left,
            "toolbar_right": toolbar.toolbar_right,
            "content": content,
            "cards_container": cards_container,
            "list_container": list_container,
            "view_switch": toolbar.view_mode_switch_btn
        })

        # Configura os botões da toolbar
        toolbar.view_mode_switch_btn.configure(command=lambda value: self.on_mode_change(name, value))
        if name == "Distribuições":
            toolbar.add_btn.configure(command=self.add_distribution)
        else:
            toolbar.add_btn.configure(command=lambda: self.add_record(name))

        # Configura e carrega a visualização inicial dos dados
        toolbar.view_mode_switch_btn.set(self.tabs_meta[name]["view_mode"])
        self.on_mode_change(name, self.tabs_meta[name]["view_mode"])

        # Carrega os dados de cada tab
        data: list[dict] = self.tabs_meta[name]["model"].get_all_dicts()
        for item in data:
            self.load_record(name, item)

    def on_mode_change(self, tab_name, value: str):
        """Muda a visualização dos dados."""
        if value == "Cards":
            self.tabs_meta[tab_name]["list_container"].pack_forget()
            self.tabs_meta[tab_name]["cards_container"].pack(fill="both", expand=True)
            self.tabs_meta[tab_name]["view_mode"] = "Cards"
        else:
            self.tabs_meta[tab_name]["cards_container"].pack_forget()
            self.tabs_meta[tab_name]["list_container"].pack(fill="both", expand=True)
            self.tabs_meta[tab_name]["view_mode"] = "Lista"

    def load_record(self, name: str, record_info: dict):
        """Insere um novo registro na tab."""
        self.tabs_meta[name]["list_container"].add_item(record_info)
        self.tabs_meta[name]["cards_container"].add_card(record_info)

    def add_record(self, name: str):
        """Abre uma janela de inserção de registro."""
        EditBaseWindowView(
            tab_name=name,
            model_cls=self.tabs_meta[name]["model"],
            on_save=self.load_record
        )

    def add_distribution(self):
        """Abre uma janela de distribuição de tarefas."""
        DistributionView(on_save=lambda info: self.load_record("Distribuições", info))
