from customtkinter import CTkLabel, CTkToplevel

from views.sidebar.tabs.sidebar_base_tab_view import SidebarBaseTabView
from views.components.tooltip import Tooltip
from services.data_facade import DataFacade
from services.task_service import TaskService


class ControlTabView(SidebarBaseTabView):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.label.configure(text="Controle")
        self.refresh_btn.configure(command=self.load_data)

        self.bind("<Visibility>", self.load_data)

    def load_data(self, event=None):
        """Carrega as informações de controle."""

        # Limpa as informações anteriores
        for child in self.winfo_children():
            if child == self.tab_top_bar:
                continue
            child.destroy()

        sectors = DataFacade.get_all_data("sectors")  # Todos os setores
        tasks = DataFacade.get_all_data("tasks")      # Todas as tarefas
        distros = DataFacade.get_all_data("distros")  # Todas as distribuições

        # Distribuições
        self.title("Distribuições")

        if len(distros) == 0:
            self.item("Nenhum registro encontrado.")
        else:
            for distro in distros:
                completed_tasks = TaskService.get_completed_tasks_by_distro(distro["id"])
                porcentagem = (len(completed_tasks) / distro["total_tasks"]) * 100
                self.item(f"{distro["title"]}: {int(porcentagem)}%", related_tasks=completed_tasks)

        # Setores
        self.title("Setores")

        if len(sectors) == 0:
            self.item("Nenhum registro encontrado.")
        else:
            for sector in sectors:
                completed_tasks = TaskService.get_completed_tasks_by_sector(sector["id"])
                porcentagem = (len(completed_tasks) /
                               len(TaskService.get_tasks_by_sector(sector["id"]))) * 100
                self.item(f"{sector["name"]}: {int(porcentagem)}%", related_tasks=completed_tasks)

        # Tarefas
        self.title("Tarefas")

        completed_tasks = [task for task in tasks if task["status"] == "Concluída"]
        self.item(f"Total concluídas: {len(completed_tasks)}", related_tasks=completed_tasks)

        assigned_tasks = TaskService.get_assigned_tasks()
        self.item(f"Total distribuídas: {len(assigned_tasks)}", related_tasks=assigned_tasks)


    def title(self, text: str):
        """Adiciona um título a lista"""
        title_label = CTkLabel(self, text=text, font=("Tahoma", 11, "bold"), anchor="w")
        title_label.pack(side="top", anchor="w", pady=(10, 0), padx=(20, 10), fill="x")

    def item(self, item_info: str, related_tasks: list = None):
        """Adiciona um novo item à lista."""
        item_label = CTkLabel(self, text=item_info, font=("Tahoma", 11), anchor="w")
        item_label.pack(side="top", anchor="w", padx=(30, 10))

        # Cria um tooltip com as tarefas relevantes ao item
        if related_tasks:
            task_list = "\n".join(f"- {task['name']}" for task in related_tasks)
            Tooltip(item_label, f"Tarefas concluídas:\n{task_list}")
