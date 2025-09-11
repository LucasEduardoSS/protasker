import customtkinter as ctk
from tkinter import PanedWindow

# Functions
from functions.distribution_algorithms import distribute_tasks_fair
from utils.gui import center_window

# Models
from models.person_model import Person
from models.task_model import Task
from models.sector_model import Sector

# Views
from views.components.pro_widgets import ProComboBox, ProCheckBox, ProButton
from views.components.labeled_entry import LabeledEntryView
from views.components.card import Card
from views.components.list_item import ListItem


class DistributionView(ctk.CTkToplevel):
    def __init__(self, tab_info: dict, **kwargs):
        super().__init__(**kwargs)

        # Configurações da janela
        self.configure(fg_color="#2E333C")
        self.iconbitmap("images/protasker_icon.ico")
        self.title('Geração de Distribuição')
        self.minsize(600, 400)

        # Centraliza a janela
        center_window(self, (650, 500))

        # Mantém sobre a janela principal
        self.grab_set()
        self.lift()
        self.focus_force()

        # Informações da tab distribuições
        self.tab_info = tab_info

        # Frame principal
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(padx=5, pady=5, fill="both", expand=True)

        # Título da distribuição
        self.distro_title = LabeledEntryView(self.main_frame, "Título", "Distribuição", fg_color="#2C2E33")
        self.distro_title.pack(side="top", anchor="w", padx=(0, 10), pady=5, fill="x")

        # Área de trabalho
        self.workspace = PanedWindow(
            self.main_frame,
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
        self.people = PeopleView(self.workspace)
        self.tasks = TasksView(self.workspace)

        # Adiciona as sessões na workspace
        self.workspace.add(self.options, width=200, padx=10)
        self.workspace.add(self.people, width=250)
        self.workspace.add(self.tasks, width=250, padx=10)

        # Botão distribuir
        self.generate_button = ProButton(self.main_frame, text="Distribuir", command=self._on_generate)
        self.generate_button.pack(side="top", anchor="e", padx=(0, 10), pady=5)

        self.message = ctk.CTkLabel(self.main_frame, text="Títule a distribuição e selecione as pessoas e tarefas", font=("Tahoma", 11))
        self.message.pack(side="top", anchor="w", padx=5, pady=0)

        # Conectar callbacks que dependem da instância
        self.options.sector_combobox.configure(command=self._on_filters_changed)
        self.options.priority_combobox.configure(command=self._on_filters_changed)
        self.options.company_combobox.configure(command=self._on_filters_changed)
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

    def _on_generate(self):
        """Gera a distribuição de tarefas."""
        if len(self.people.get_selected_people()) == 0 or len(self.tasks.get_selected_tasks()) == 0:
            self.message.configure(text="Selecione pelo menos uma pessoa e uma tarefa para distribuir.")
            return

        if self.distro_title.get() == "":
            self.message.configure(text="Defina um título para distribuição.")
            return

        distro = distribute_tasks_fair(self.people.get_selected_people(), self.tasks.get_selected_tasks())

        distro_info = {
            "title": self.distro_title.get(),
            "total_tasks": len(self.tasks.get_selected_tasks()),
            "finished_tasks": 0,
        }

        item = ListItem(self.tab_info["tab_meta"]["list_container"], distro_info)
        self.tab_info["tab_meta"]["list_container"].add_item(item)

        card = Card(self.tab_info["tab_meta"]["cards_container"], distro_info)
        self.tab_info["tab_meta"]["cards_container"].add_card(card)


class OptionsView(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        # Configurações
        self.configure(
            fg_color="transparent",
            corner_radius=0
        )

        self.pack_propagate(False)

        # Dados
        self.sectors: list[Sector] = [s.name for s in Sector.select(Sector.name).order_by(Sector.name)]
        self.priorities: list[Task] = [t.priority for t in Task.select(Task.priority).order_by(Task.priority)]
        self.companies: list[str] = [p.company for p in Person.select(Person.company).order_by(Person.company)]

        # Filtros
        self.filters_label = ctk.CTkLabel(self, text="Filtros", font=("Tahoma", 11), anchor="w")
        self.filters_label.pack(side="top", anchor="w", pady=2)

        self.sector_label = ctk.CTkLabel(self, text="setor:", font=("Tahoma", 10), anchor="w")
        self.sector_label.pack(side="top", anchor="w", padx=5)

        self.sector_combobox = ProComboBox(self, values=self.sectors)
        self.sector_combobox.pack(side="top", anchor="w", padx=5, pady=2, fill="x")
        self.sector_combobox.set("Nenhum")

        self.priority_label = ctk.CTkLabel(self, text="prioridade:", font=("Tahoma", 10), anchor="w")
        self.priority_label.pack(side="top", anchor="w", padx=5)

        self.priority_combobox = ProComboBox(self, values=self.priorities)
        self.priority_combobox.pack(side="top", anchor="w", padx=5, pady=2, fill="x")
        self.priority_combobox.set("Nenhum")

        self.company_label = ctk.CTkLabel(self, text="empresa:", font=("Tahoma", 10), anchor="w")
        self.company_label.pack(side="top", anchor="w", padx=5)

        self.company_combobox = ProComboBox(self, values=self.companies)
        self.company_combobox.pack(side="top", anchor="w", padx=5, pady=2, fill="x")
        self.company_combobox.set("Nenhum")

        self.clean_button = ProButton(self, text="Limpar filtros", height=15, command=self.clean_filters)
        self.clean_button.pack(side="top", anchor="e", padx=5, pady=(10, 0), fill="x")

    def get_filters(self):
        """Retorna os filtros selecionados."""
        return {
            "sector": self.sector_combobox.get(),
            "priority": self.priority_combobox.get(),
            "company": self.company_combobox.get()
        }

    def clean_filters(self):
        """Limpa os filtros."""
        self.sector_combobox.set("Nenhum")
        self.priority_combobox.set("Nenhum")
        self.company_combobox.set("Nenhum")


class PeopleView(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        # Configurações
        self.configure(
            fg_color="transparent",
            corner_radius=0
        )

        # Pessoas
        self.people_label = ctk.CTkLabel(self, text="Pessoas", font=("Tahoma", 11), anchor="w")
        self.people_label.pack(side="top", anchor="w", pady=2)

        # Lista de pessoas
        self.people_list = Person.select()
        self.people_list_view = ctk.CTkScrollableFrame(self, corner_radius=5, fg_color="#2C2E33", border_width=1, border_color="#777")
        self.people_list_view._scrollbar.grid_configure(padx=5)
        self.people_list_view.pack(side="top", fill="both", expand=True)

        # Carrega sem filtro inicialmente
        self.refresh()

    def refresh(self, filter_by: dict = None):
        # Limpa a lista de pessoas
        for child in self.people_list_view.winfo_children():
            child.destroy()

        self.select_all = ProCheckBox(self.people_list_view, text="Selecionar todos", command=self.select_all_people)
        self.select_all.pack(side="top", anchor="w", padx=5, pady=(5, 0), fill="x")

        # Carrega a lista de pessoas com filtros
        for person in self.people_list:
            if filter_by:
                if filter_by["sector"] != "Nenhum" and filter_by["sector"].lower() != person.sector.name.lower():
                    continue
                if filter_by["company"] != "Nenhum" and filter_by["company"].lower() != person.company.lower():
                    continue
            item = ProCheckBox(self.people_list_view, text=person.name)
            item.pack(side="top", anchor="w", padx=5, pady=(5, 0), fill="x")

    def select_all_people(self):
        for person in self.people_list_view.winfo_children():
            if person.cget("text") == "Selecionar todos":
                continue
            if self.select_all.get() == 0:
                person.deselect()
            else:
                person.select()

    def get_selected_people(self):
        """Retorna uma lista com as pessoas selecionadas."""
        selected_people = []
        for person in self.people_list_view.winfo_children():
            if person.cget("text") == "Selecionar todos":
                continue
            if person.get() == 1:
                selected_people.append(Person.get_by_name(person.cget("text")))

        return selected_people


class TasksView(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        # Configurações
        self.configure(
            fg_color="transparent",
            corner_radius=0
        )

        # Tarefas
        self.tasks_label = ctk.CTkLabel(self, text="Tarefas", font=("Tahoma", 11), anchor="w")
        self.tasks_label.pack(side="top", anchor="w", pady=2)

        # Lista de tarefas
        self.tasks_list = Task.select()
        self.tasks_list_view = ctk.CTkScrollableFrame(self, corner_radius=5, fg_color="#2C2E33", border_width=1, border_color="#777")
        self.tasks_list_view._scrollbar.grid_configure(padx=5)
        self.tasks_list_view.pack(side="top", fill="both", expand=True)

        # Carrega sem filtro inicialmente
        self.refresh()

    def refresh(self, filter_by: dict = None):
        # Limpa a lista de tarefas
        for child in self.tasks_list_view.winfo_children():
            child.destroy()

        self.select_all = ProCheckBox(self.tasks_list_view, text="Selecionar todos", command=self.select_all_tasks)
        self.select_all.pack(side="top", anchor="w", padx=5, pady=(5, 0), fill="x")

        # Carrega a lista de tarefas com filtros
        for task in self.tasks_list:
            if filter_by:
                if filter_by["sector"] != "Nenhum" and filter_by["sector"].lower() != task.sector.name.lower():
                    continue
                if filter_by["priority"] != "Nenhum" and filter_by["priority"] != task.priority:
                    continue
                if filter_by["company"] != "Nenhum" and filter_by["company"].lower() != task.company.lower():
                    continue
            item = ProCheckBox(self.tasks_list_view, text=task.name)
            item.pack(side="top", anchor="w", padx=5, pady=(5, 0), fill="x")

    def select_all_tasks(self):
        for task in self.tasks_list_view.winfo_children():
            if task.cget("text") == "Selecionar todos":
                continue
            if self.select_all.get() == 0:
                task.deselect()
            else:
                task.select()

    def get_selected_tasks(self):
        """Retorna uma lista com as tarefas selecionadas."""
        selected_tasks = []
        for task in self.tasks_list_view.winfo_children():
            if task.cget("text") == "Selecionar todos":
                continue
            if task.get() == 1:
                selected_tasks.append(Task.get_by_name(task.cget("text")))

        return selected_tasks
