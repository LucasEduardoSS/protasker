import customtkinter as ctk
from peewee import IntegrityError

from functions.distribution_algorithms import allocate_tasks
from utils.gui_utils import center_window

from services.task_service import TaskService
from services.sector_service import SectorService
from services.person_service import PersonService
from services.distribution_service import DistributionService

from views.components.pro_widgets import ProComboBox, ProCheckBox, ProButton
from views.components.pro_labeled_widgets import LabeledEntryView


class DistributionView(ctk.CTkToplevel):
    """Define uma janela para inserir ou atualizar uma distribuição de tarefas."""

    def __init__(self, on_save=None, **kwargs):
        super().__init__(**kwargs)

        self.on_save = on_save if on_save else lambda x: None
        self.model_info = None

        # Configurações da janela
        self.configure(fg_color="#2E333C")
        self.iconbitmap("images/protasker_icon.ico")
        self.title('Geração de Distribuição')
        self.minsize(690, 510)

        # Centraliza a janela
        center_window(self, (690, 510))

        # Mantém sobre a janela principal
        self.grab_set()
        self.lift()
        self.focus_force()

        # Título da distribuição
        self.distro_title = LabeledEntryView(self, "Título", fg_color="#2C2E33")
        self.distro_title.entry.configure(placeholder_text="Distribuição")
        self.distro_title.grid(row=0, column=0, columnspan=3, padx=(5, 15), pady=(15, 5), sticky="new")

        # Área de trabalho
        self.workspace = ctk.CTkFrame(self, fg_color="#3E4D66")
        self.workspace.grid(row=1, column=0, columnspan=3, padx=15, pady=10, sticky="nsew")
        self.workspace.grid_rowconfigure(0, weight=1)
        self.workspace.grid_columnconfigure(0, weight=2, minsize=225)
        self.workspace.grid_columnconfigure(2, weight=3, minsize=270)
        self.workspace.grid_columnconfigure(4, weight=3, minsize=270)

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
            itens=TaskService.get_unassigned_tasks(),
            model="task",
            supported_filters=["sector", "priority"]
        )

        # Adiciona as sessões na workspace
        separator1 = ctk.CTkFrame(self.workspace, width=2, fg_color="#2E333C")
        separator2 = ctk.CTkFrame(self.workspace, width=2, fg_color="#2E333C")

        self.options.grid(row=0, column=0, sticky="nsew")
        separator1.grid(row=0, column=1, sticky="ns", padx=2)
        self.people.grid(row=0, column=2, sticky="nsew")
        separator2.grid(row=0, column=3, sticky="ns", padx=2)
        self.tasks.grid(row=0, column=4, sticky="nsew")

        # Botão distribuir
        self.submit_button = ProButton(self, text="Distribuir", command=self.submit)
        self.submit_button.grid(row=2, column=2, padx=10, pady=5, sticky="e")

        self.message = ctk.CTkLabel(self, text="Títule a distribuição e selecione as pessoas e tarefas", font=("Tahoma", 11))
        self.message.grid(row=2, column=0, columnspan=2, padx=(20, 5), pady=(0, 5), sticky="w")

        # Conectar callbacks que dependem da instância
        self.options.filters["setor"].configure(command=self._on_filters_changed)
        self.options.filters["prioridade"].configure(command=self._on_filters_changed)
        self.options.filters["empresa"].configure(command=self._on_filters_changed)
        self.options.clean_button.configure(command=self._on_filter_clear, border_color="#2C2E33", border_width=2)

    def _on_filters_changed(self, _value=None):
        """Recoleta os filtros atuais e atualiza a lista de pessoas e tarefas."""
        self.people.refresh(self.options.get_filters())
        self.tasks.refresh(self.options.get_filters())

    def _on_filter_clear(self):
        """Limpa os filtros e atualiza as listas de pessoas e tarefas."""
        self.options.clean_filters()
        self.people.refresh()
        self.tasks.refresh()

    def submit(self):
        """Gera ou atualiza uma distribuição."""

        selected_people = self.people.get_selected()
        selected_tasks = self.tasks.get_selected()

        # Interrompe a distribuição caso nenhum registro seja selecionado
        if  not selected_people or not selected_tasks:
            self.message.configure(text="Selecione pelo menos uma pessoa e uma tarefa para distribuir.", text_color="#EB4436")
            return

        # Impede que uma pessoa fique sem tarefas
        if len(selected_people) < len(selected_tasks):
            self.message.configure(text="Selecione pelo menos um tarefa para cada pessoa.", text_color="#EB4436")
            return

        # Interrompe a distribuição caso nenhum nome tenha sido informado
        if self.distro_title.get() == "":
            self.message.configure(text="Defina um título para distribuição.", text_color="#EB4436")
            return

        # Dados da distribuição
        self.model_info = {
            "name": self.distro_title.get().strip(),
            "total_tasks": len(selected_tasks),
            "finished_tasks": 0
        }

        # Cria uma nova instância de distribuição
        distro = DistributionService.create_distribution(self.model_info)

        try:
            if allocate_tasks(distro, selected_people, selected_tasks):
                self.on_save(distro.__data__)  # Persiste os dados
            else:
                self.message.configure(text="Selecione pelo menos uma tarefa para cada setor de pessoa.")
                return
        except IntegrityError as e:
            self.message.configure(text=f"Erro ao distribuir tarefas: {e}")

            # Impede criar uma distribuição sem tarefas
            DistributionService.delete_distribution(distro)

            # Evita retornar dados vazios
            return
        finally:
            self.model_info = None
            self.message.configure(text="Distribuição gerada com sucesso!", text_color="white")


class OptionsView(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.configure(fg_color="transparent", corner_radius=0, border_width=0)  #3E4D66
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
        self.configure(fg_color="transparent", corner_radius=0, border_width=0, height=400)
        self.pack_propagate(False)

        # Título
        self.tasks_label = ctk.CTkLabel(self, text=title, font=("Tahoma", 11), anchor="w")
        self.tasks_label.pack(side="top", anchor="w", pady=2, padx=(10, 0))

        # Frame movimentável
        self.itens_frame = ctk.CTkScrollableFrame(self, corner_radius=5, fg_color="transparent", border_width=0)
        self.itens_frame._scrollbar.grid_configure(padx=5)
        self.itens_frame.configure(scrollbar_fg_color="transparent", scrollbar_button_color="#2E333C")
        self.itens_frame.pack(side="top", padx=0, pady=5, fill="both", expand=True)

        if self._itens.__len__() == 0:
            self.empty_label = ctk.CTkLabel(self.itens_frame, text="Nenhum item disponível.", font=("Tahoma", 11), anchor="w")
            self.empty_label.grid(row=0, column=0, padx=5, pady=5)
            return

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

        if len(children) == 1:
            return None

        if self._model == "person":
            return [PersonService.get_person_by_name(item.cget("text")) for item in children if item.cget("text") != "Selecionar todos" and item.get() == 1]

        elif self._model == "task":
            return [TaskService.get_task_by_name(item.cget("text")) for item in children if item.cget("text") != "Selecionar todos" and item.get() == 1]

        return None
