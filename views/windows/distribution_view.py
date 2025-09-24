import customtkinter as ctk
from tkinter import PanedWindow
from peewee import IntegrityError

from functions.distribution_algorithms import distribute_tasks_fair
from utils.gui_utils import center_window

from services.assignment_service import AssignmentService
from services.task_service import TaskService
from services.sector_service import SectorService
from services.person_service import PersonService
from services.distribution_service import DistributionService

from views.components.pro_widgets import ProComboBox, ProCheckBox, ProButton
from views.components.pro_labeled_widgets import LabeledEntryView


class DistributionView(ctk.CTkToplevel):
    """Define uma janela para inserir ou atualizar uma distribuição de tarefas."""

    def __init__(self, model_info: dict = None, on_save=None, **kwargs):
        super().__init__(**kwargs)

        # Quando for uma atualização, receberá a função card._apply_update
        # Quando for uma inserção, receberá a função workspace_tab_view.load_record
        self.on_save = on_save if on_save else lambda x: None

        # Só receberá model_info em atualização
        self.model_info = model_info

        # Configurações da janela
        self.configure(fg_color="#2E333C")
        self.iconbitmap("images/protasker_icon.ico")
        self.title('Geração de Distribuição')
        self.minsize(700, 500)

        # Centraliza a janela
        center_window(self, (700, 500))

        # Mantém sobre a janela principal
        self.grab_set()
        self.lift()
        self.focus_force()

        # Título da distribuição
        self.distro_title = LabeledEntryView(self, "Título", fg_color="#2C2E33")
        self.distro_title.entry.insert(0, model_info["title"] if model_info else "Distribuição")
        self.distro_title.pack(side="top", anchor="w", padx=10, pady=10, fill="x")

        # Área de trabalho
        self.workspace = PanedWindow(
            self,
            orient="horizontal",
            borderwidth=4,
            sashwidth=2,
            sashpad=2,
            bg="#2E333C",
            showhandle=False,
            opaqueresize=False
        )
        self.workspace.pack(side="top", fill="both", expand=True)

        # Sessões da área de trabalho
        self.options = OptionsView(self.workspace)
        self.people = ListView(
            master=self.workspace,
            title="Pessoas",
            itens=PersonService.get_all_people(),
            model="person",
            supported_filters=["sector", "company"]
        )
        self.tasks = ListView(
            master=self.workspace,
            title="Tarefas",
            itens=TaskService.get_all_tasks(),
            model="task",
            supported_filters=["sector", "priority"]
        )

        # Adiciona as sessões na workspace
        self.workspace.add(self.options, width=225, padx=10)
        self.workspace.add(self.people, width=270)
        self.workspace.add(self.tasks, width=250, padx=10)

        # Botão distribuir
        self.generate_button = ProButton(self, text="Distribuir", command=self.generate)
        self.generate_button.pack(side="top", anchor="e", padx=(0, 10), pady=5)

        self.message = ctk.CTkLabel(self, text="Títule a distribuição e selecione as pessoas e tarefas", font=("Tahoma", 11))
        self.message.pack(side="top", anchor="w", padx=5, pady=0)

        # Conectar callbacks que dependem da instância
        self.options.filters["setor"].configure(command=self._on_filters_changed)
        self.options.filters["prioridade"].configure(command=self._on_filters_changed)
        self.options.filters["empresa"].configure(command=self._on_filters_changed)
        self.options.clean_button.configure(command=self._on_filter_clear)

    def _on_filters_changed(self, _value=None):
        """Recoleta os filtros atuais e atualiza a lista de pessoas e tarefas."""
        self.people.refresh(self.options.get_filters())
        self.tasks.refresh(self.options.get_filters())

    def _on_filter_clear(self):
        """Limpa os filtros e atualiza as listas de pessoas e tarefas."""
        self.options.clean_filters()
        self.people.refresh()
        self.tasks.refresh()

    def generate(self):
        """Gera a distribuição de tarefas."""

        selected_people = self.people.get_selected()
        selected_tasks = self.tasks.get_selected()

        # Interrompe a distribuição caso nenhum registro seja selecionado
        if  not selected_people or not selected_tasks:
            self.message.configure(text="Selecione pelo menos uma pessoa e uma tarefa para distribuir.")
            return

        # Interrompe a distribuição caso nenhum nome tenha sido informado
        if self.distro_title.get() == "":
            self.message.configure(text="Defina um título para distribuição.")
            return

        # Guarda ou atualiza as informações do modelo
        if self.model_info:
            self.model_info.update({
                "title": self.distro_title.get().strip(),
                "total_tasks": len(selected_tasks),
                "finished_tasks": 0
            })
        else:
            self.model_info = {
                "title": self.distro_title.get().strip(),
                "total_tasks": len(selected_tasks),
                "finished_tasks": 0
            }

        # Cria ou atualiza a distribuição
        if "id" in self.model_info:
            distro = DistributionService.get_distribution_by_id(self.model_info["id"])
            assignments = AssignmentService.get_assignment_by_distro(distro)
            for assignment in assignments:
                if assignment.person not in selected_people:
                    AssignmentService.delete_assignment(assignment)
        else:
            distro = DistributionService.create_distribution(self.model_info)

        try:
            buckets = distribute_tasks_fair(distro, selected_people, selected_tasks)
        except IntegrityError as e:
            self.message.configure(text=f"Erro ao distribuir tarefas: {e}")
            return

        # Persiste os dados
        self.on_save(self.model_info)


class OptionsView(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.configure(fg_color="#3E4D66", corner_radius=5, border_width=1)
        self.pack_propagate(False)
        self.filters = {}

        # Dados
        self.sectors: list = [sector["name"] for sector in SectorService.get_all_sectors()]
        self.priorities: list = list(set([task["priority"] for task in TaskService.get_all_tasks()]))
        self.companies: list = list(set([person["company"] for person in PersonService.get_all_people()]))

        # Filtros
        self.filters_label = ctk.CTkLabel(self, text="Filtros", font=("Tahoma", 11), anchor="w")
        self.filters_label.pack(side="top", anchor="w", pady=2, padx=(10, 0))

        self.filter("setor", self.sectors)
        self.filter("prioridade", self.priorities)
        self.filter("empresa", self.companies)

        self.clean_button = ProButton(self, text="Limpar filtros", height=25, corner_radius=5, command=self.clean_filters)
        self.clean_button.pack(side="bottom", padx=10, pady=10, fill="x")

    def filter(self, label, values):
        """Adiciona um filtro."""
        filter_label = ctk.CTkLabel(self, text=f"{label}:", font=("Tahoma", 10), anchor="w")
        filter_label.pack(side="top", anchor="w", padx=10)

        self.filters[label] = ProComboBox(self, height=30, values=values, corner_radius=5)
        self.filters[label].pack(side="top", anchor="w", padx=10, pady=2, fill="x")
        self.filters[label].set("Nenhum")

    def get_filters(self):
        """Retorna os filtros selecionados."""
        return {
            "sector": self.filters["setor"].get(),
            "priority": self.filters["prioridade"].get(),
            "company": self.filters["empresa"].get()
        }

    def clean_filters(self):
        """Limpa os filtros."""
        for field_filter in self.filters.values():
            field_filter.set("Nenhum")


class ListView(ctk.CTkFrame):

    def __init__(self,
                 title: str,
                 itens: list,
                 model: str,
                 supported_filters: list=None,
                 **kwargs):

        super().__init__(**kwargs)

        self._itens = itens
        self._model = model
        self._supported_filters = supported_filters
        self.configure(fg_color="#3E4D66", corner_radius=5, border_width=1)
        self.pack_propagate(False)

        # Título
        self.tasks_label = ctk.CTkLabel(self, text=title, font=("Tahoma", 11), anchor="w")
        self.tasks_label.pack(side="top", anchor="w", pady=2, padx=(10, 0))

        # Frame movimentável
        self.itens_frame = ctk.CTkScrollableFrame(self, corner_radius=5, fg_color="transparent", border_width=0)  #3E4D66
        self.itens_frame._scrollbar.grid_configure(padx=5)
        self.itens_frame.configure(scrollbar_fg_color="transparent", scrollbar_button_color="#2E333C")
        self.itens_frame.pack(side="top", padx=0, pady=5, fill="both", expand=True)

        # Selecionar todos
        self.select_all = ProCheckBox(self.itens_frame, text="Selecionar todos", command=self.select_all)
        self.select_all.pack(side="top", anchor="w", padx=5, pady=(5, 0), fill="x")

        # Carrega inicialmente sem filtros
        self.refresh()

    def refresh(self, filter_by: dict = None):

        # Evita duplicidade de itens
        for child in self.itens_frame.winfo_children():
            if child == self.select_all:
                continue
            child.destroy()

        # Faz a filtragem dos itens com filtros
        for item in self._itens:
            if filter_by:

                if "sector" in item:
                    if filter_by["sector"] != "Nenhum" and filter_by["sector"].lower() != SectorService.get_sector_by_id(item["sector"]).name.lower():
                        continue

                if "priority" in item:
                    if filter_by["priority"] != "Nenhum" and filter_by["priority"] != item["priority"]:
                        continue

                if "company" in item:
                    if filter_by["company"] != "Nenhum" and filter_by["company"].lower() != item["company"].lower():
                        continue

                # Tentativa de automatizar a filtragem dos itens
                # for filter_ in self._supported_filters:
                #     if filter_ == "sector" and filter_by[filter_] != "Nenhum":
                #         if filter_by[filter_].lower() != SectorService.get_sector_by_id(item["sector"]):
                #             continue
                #     if filter_by[filter_] != "Nenhum" and filter_by[filter_].lower() != item[filter_].lower():
                #         continue

            item = ProCheckBox(self.itens_frame, text=item["name"])
            item.pack(side="top", anchor="w", padx=5, pady=(5, 0), fill="x")

    def select_all(self):
        for item in self.itens_frame.winfo_children():
            if item.cget("text") == "Selecionar todos":
                continue
            if self.select_all.get() == 0:
                item.deselect()
            else:
                item.select()

    def get_selected(self):
        """Retorna uma lista com os itens selecionados."""
        children = self.itens_frame.winfo_children()

        if self._model == "person":
            return [PersonService.get_person_by_name(item.cget("text")) for item in children if item.cget("text") != "Selecionar todos"]

        elif self._model == "task":
            return [TaskService.get_task_by_name(item.cget("text")) for item in children if item.cget("text") != "Selecionar todos"]

        return None
