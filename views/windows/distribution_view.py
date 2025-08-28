import customtkinter as ctk
from tkinter import PanedWindow
from utils.gui import center_window
from models.person_model import Person
from models.task_model import Task
from models.sector_model import Sector
from views.components.pro_widgets import ProComboBox, ProCheckBox, ProRadioButton, ProButton


class DistributionView(ctk.CTkToplevel):
    def __init__(self, tab_info: dict, **kwargs):
        super().__init__(**kwargs)

        # Configurações da janela
        self.configure(fg_color="#2E333C")
        self.iconbitmap("images/protasker_icon.ico")
        self.title('Geração de Distribuição')
        self.minsize(600, 300)

        # Centraliza a janela
        center_window(self, (700, 400))

        # Mantém sobre a janela principal
        self.grab_set()
        self.lift()
        self.focus_force()

        # Informações da tab distribuições
        self.tab_info = tab_info

        # Frame principal
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(padx=5, pady=5, fill="both", expand=True)

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
        self.workspace.add(self.options, width=200)
        self.workspace.add(self.people, width=300)
        self.workspace.add(self.tasks, width=300)

        # Botão distribuir
        self.generate_button = ProButton(self.main_frame, text="Distribuir", command=None)
        self.generate_button.pack(side="top", anchor="e", pady=5)

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


class OptionsView(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        # Configurações
        self.configure(fg_color="transparent", corner_radius=0)
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

        # Distribuições
        self.distru_types = ctk.CTkLabel(self, text="Distribuição", font=("Tahoma", 11), anchor="w")
        self.distru_types.pack(side="top", anchor="w", pady=(10, 2))
        self.distru_type = ctk.StringVar(value="simple")

        self.simple = ProRadioButton(self, text="Simples", variable=self.distru_type, value="simple", command=None)
        self.simple.pack(side="top", anchor="w", padx=(10, 0), pady=4)

        self.complex = ProRadioButton(self, text="Complexa", variable=self.distru_type, value="complex", command=None)
        self.complex.pack(side="top", anchor="w", padx=(10, 0), pady=4)

    def get_filters(self):
        return {
            "sector": self.sector_combobox.get(),
            "priority": self.priority_combobox.get(),
            "company": self.company_combobox.get()
        }

    def clean_filters(self):
        self.sector_combobox.set("Nenhum")
        self.priority_combobox.set("Nenhum")
        self.company_combobox.set("Nenhum")


class PeopleView(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        # Configurações
        self.configure(fg_color="transparent", corner_radius=0)

        # Pessoas
        self.people_label = ctk.CTkLabel(self, text="Pessoas", font=("Tahoma", 11), anchor="w")
        self.people_label.pack(side="top", anchor="w", pady=2)

        # Lista de pessoas
        self.people_list = Person.select()
        self.people_list_view = ctk.CTkScrollableFrame(self, corner_radius=0, fg_color="#2C2E33")
        self.people_list_view.pack(side="top", fill="both", expand=True)

        # Carrega sem filtro inicialmente
        self.refresh()

    def refresh(self, filter_by: dict = None):
        # Limpa a lista de pessoas
        for child in self.people_list_view.winfo_children():
            child.destroy()

        # Carrega a lista de pessoas com filtros
        for person in self.people_list:
            if filter_by:
                if filter_by["sector"] != "Nenhum" and filter_by["sector"].lower() != person.sector.name.lower():
                    continue
                if filter_by["company"] != "Nenhum" and filter_by["company"].lower() != person.company.lower():
                    continue
            item = ProCheckBox(self.people_list_view, text=person.name)
            item.pack(side="top", anchor="w", padx=10, pady=(10, 0), fill="x")


class TasksView(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        # Configurações
        self.configure(fg_color="transparent", corner_radius=0)

        # Tarefas
        self.tasks_label = ctk.CTkLabel(self, text="Tarefas", font=("Tahoma", 11), anchor="w")
        self.tasks_label.pack(side="top", anchor="w", pady=2)

        # Lista de tarefas
        self.tasks_list = Task.select()
        self.tasks_list_view = ctk.CTkScrollableFrame(self, corner_radius=0, fg_color="#2C2E33")
        self.tasks_list_view.pack(side="top", fill="both", expand=True)

        # Carrega sem filtro inicialmente
        self.refresh()

    def refresh(self, filter_by: dict = None):
        # Limpa a lista de tarefas
        for child in self.tasks_list_view.winfo_children():
            child.destroy()

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
            item.pack(side="top", anchor="w", padx=10, pady=(10, 0), fill="x")
