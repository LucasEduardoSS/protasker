import customtkinter as ctk

from views.sidebar.tabs.sidebar_base_tab_view import SidebarBaseTabView

from services.data_facade import DataFacade
from services.task_service import TaskService
from services.person_service import PersonService
from services.assignment_service import AssignmentService


class DetailsTabView(SidebarBaseTabView):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.label.configure(text="Detalhes")
        self.model = None
        self.item_info = None
        self.refresh_btn.configure(command=self.refresh)

    def refresh(self):
        if self.item_info:
            model_info = self.model.get_by_id(self.item_info["id"])
            if model_info:
                self.load_details(self.model, dict(model_info.__data__))

    def load_details(self, model, item_info: dict):
        """ Atualiza a visualização dos detalhes com as informações do item selecionado. """

        self.model = model
        self.item_info = item_info

        # Certifica que existe dados
        if not item_info or not model:
            return

        # Limpa todos os itens
        for widget in self.winfo_children():
            if widget == self.tab_top_bar:
                continue
            widget.destroy()

        if model == "person":
            template = TemplatePerson(self)

            template.name_label.configure(text=item_info["name"])
            template.company_sector_role_label.configure(text=f"{item_info["company"]} | {DataFacade.get_record("sector", item_info["sector"])} | {item_info["role"]}")
            template.total_assigned_tasks.configure(text=f"Total: {AssignmentService.get_assignments(person_id=item_info["id"]).__len__()}")
            template.total_completed_tasks.configure(text=f"Concluídas: {TaskService.get_completed_tasks_by_person(item_info['id']).__len__()}")

            template.load_tasks(TaskService.get_tasks_by_person(item_info["id"]))

        elif model == "task":
            template = TemplateTask(self)

            template.name_label.configure(text=item_info["name"])
            template.company_sector_label.configure(text=f"{item_info['company']} | {DataFacade.get_record("sector", item_info["sector"])}")
            template.description_label.configure(text=item_info["description"])
            template.status_label.configure(text=f"Status: {item_info["status"]}")
            template.weight_label.configure(text=f"Peso: {item_info['weight']}")
            template.priority_label.configure(text=f"Prioridade: {item_info['priority']}")
            template.creation_data_label.configure(text=f"Data de criação: {item_info['creation_date'].date()}")
            if item_info["deadline"]:
                template.deadline_label.configure(text=f"Prazo: {item_info['deadline'].date()}")
            else:
                template.deadline_label.destroy()
            if item_info["closure_date"]:
                template.closure_date_label.configure(text=f"Conclusão: {item_info['closure_date'].date()}")
            else:
                template.closure_date_label.destroy()

            template.load_people(PersonService.get_people_by_task(item_info["id"]))

        elif model == "sector":
            template = TemplateSector(self)

            template.name_label.configure(text=item_info["name"])
            template.total_people_label.configure(text=f"{PersonService.get_people_by_sector(item_info["id"]).__len__()} pessoas")
            template.total_tasks_label.configure(text=f"{TaskService.get_tasks_by_sector(item_info["id"]).__len__()} tarefas")

            template.load_people(PersonService.get_people_by_sector(item_info["id"]), after=template.people_label)
            template.load_people(TaskService.get_tasks_by_sector(item_info["id"]))

        elif model == "distro":
            template = TemplateDistro(self)

            template.name_label.configure(text=item_info["name"])
            template.total_people_label.configure(
                text=f"{PersonService.get_people_by_distro(item_info["id"]).__len__()} pessoas")
            template.total_tasks_label.configure(
                text=f"{TaskService.get_tasks_by_distro(item_info["id"]).__len__()} tarefas")
            template.total_completed_tasks_label.configure(
                text=f"{TaskService.get_completed_tasks_by_distro(item_info["id"]).__len__()} tarefas concluídas")

            template.load_people(PersonService.get_people_by_distro(item_info["id"]), after=template.people_label)
            template.load_tasks(TaskService.get_tasks_by_distro(item_info["id"]))
        else:
            print("Erro.")


# Experimental
def style_config() -> dict:
    return {
        "font": ("Tahoma", 11)
    }


class TemplateBase(ctk.CTkFrame):
    """ Classe base para os modelos de detalhes. """

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(width=300, height=100)
        self.pack(fill="both", expand=True, padx=10, pady=5)
        self.pack_propagate(False)

        self.configure(fg_color="#2E333C", corner_radius=0)
        self.style = style_config()

        self.model_label = ctk.CTkLabel(self, text="", anchor="w", font=("Tahoma", 11))
        self.model_label.pack(fill="x", padx=10, pady=0)

    def line(self, padding: tuple=None):
        line = ctk.CTkFrame(self, height=2, fg_color="#3E4D66", corner_radius=0)
        line.pack(fill="x", padx=padding[0] if padding else 10, pady=(padding[1] if padding else 5))

    def load_records(self, records: list, after=None):
        """ Carrega os registros de um modelo. Precisa receber uma lista de strings. """
        for record in records:
            record_label = ctk.CTkLabel(self, text=record, anchor="w", font=self.style["font"], height=15)
            record_label.pack(fill="x", padx=10, pady=0, after=after)

    def load_people(self, people: list, after=None):
        self.load_records([f"- {person['name']}" for person in people], after=after)

    def load_tasks(self, tasks: list, after=None):
        self.load_records([f"- {task['name']}: {task["status"]}" for task in tasks], after=after)


class TemplatePerson(TemplateBase):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.model_label.configure(text="Pessoa")

        self.name_label = ctk.CTkLabel(self, text="Nome", anchor="w", font=("Tahoma", 14, "bold"))
        self.name_label.pack(fill="x", padx=10, pady=0)

        self.company_sector_role_label = ctk.CTkLabel(self, text="", anchor="w", font=self.style["font"], height=15)
        self.company_sector_role_label.pack(fill="x", padx=10, pady=(0, 10))

        self.tasks_label = ctk.CTkLabel(self, text="Tarefas:", anchor="w", font=("Tahoma", 12, "bold"))
        self.tasks_label.pack(fill="x", padx=10, pady=0)

        self.total_assigned_tasks = ctk.CTkLabel(self, text="", anchor="w", font=self.style["font"], height=15)
        self.total_assigned_tasks.pack(fill="x", padx=10, pady=0)

        self.total_completed_tasks = ctk.CTkLabel(self, text="", anchor="w", font=self.style["font"])
        self.total_completed_tasks.pack(fill="x", padx=10, pady=0)

        self.line()


class TemplateTask(TemplateBase):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.model_label.configure(text="Tarefa")

        self.name_label = ctk.CTkLabel(self, text="", anchor="w", font=("Tahoma", 14, "bold"))
        self.name_label.pack(fill="x", padx=10, pady=0)

        self.company_sector_label = ctk.CTkLabel(self, text="", anchor="w", font=self.style["font"], height=15)
        self.company_sector_label.pack(fill="x", padx=10, pady=0)

        self.description_label = ctk.CTkLabel(self, text="", anchor="w", font=self.style["font"], height=15)
        self.description_label.pack(fill="x", padx=10, pady=10)
        self.description_label.after(100, lambda: self.description_label.configure(wraplength=self.winfo_width() - 20))

        self.status_label = ctk.CTkLabel(self, text="", anchor="w", font=self.style["font"], height=15)
        self.status_label.pack(fill="x", padx=10, pady=0)

        self.weight_label = ctk.CTkLabel(self, text="", anchor="w", font=self.style["font"], height=15)
        self.weight_label.pack(fill="x", padx=10, pady=0)

        self.priority_label = ctk.CTkLabel(self, text="", anchor="w", font=self.style["font"], height=15)
        self.priority_label.pack(fill="x", padx=10, pady=0)

        self.creation_data_label = ctk.CTkLabel(self, text="", anchor="w", font=self.style["font"], height=15)
        self.creation_data_label.pack(fill="x", padx=10, pady=0)

        self.deadline_label = ctk.CTkLabel(self, text="não informada", anchor="w", font=self.style["font"], height=15)
        self.deadline_label.pack(fill="x", padx=10, pady=0)

        self.closure_date_label = ctk.CTkLabel(self, text="não informada", anchor="w", font=self.style["font"], height=15)
        self.closure_date_label.pack(fill="x", padx=10, pady=0)

        self.line()

        self.people_label = ctk.CTkLabel(self, text="Encarregados:", anchor="w", font=("Tahoma", 12, "bold"))
        self.people_label.pack(fill="x", padx=10, pady=0)


class TemplateSector(TemplateBase):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.model_label.configure(text="Setor")

        self.name_label = ctk.CTkLabel(self, text="", anchor="w", font=("Tahoma", 14, "bold"))
        self.name_label.pack(fill="x", padx=10, pady=0)

        self.total_people_label = ctk.CTkLabel(self, text="", anchor="w", font=self.style["font"], height=15)
        self.total_people_label.pack(fill="x", padx=10, pady=(5, 0))

        self.total_tasks_label = ctk.CTkLabel(self, text="", anchor="w", font=self.style["font"], height=15)
        self.total_tasks_label.pack(fill="x", padx=10, pady=5)

        self.line()

        self.people_label = ctk.CTkLabel(self, text="Pessoas:", anchor="w", font=("Tahoma", 12, "bold"))
        self.people_label.pack(fill="x", padx=10, pady=0)

        self.line()

        self.tasks_label = ctk.CTkLabel(self, text="Tarefas:", anchor="w", font=("Tahoma", 12, "bold"))
        self.tasks_label.pack(fill="x", padx=10, pady=0)


class TemplateDistro(TemplateBase):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.model_label.configure(text="Distribuição")

        self.name_label = ctk.CTkLabel(self, text="", anchor="w", font=("Tahoma", 14, "bold"))
        self.name_label.pack(fill="x", padx=10, pady=0)

        self.total_people_label = ctk.CTkLabel(self, text="", anchor="w", font=self.style["font"], height=15)
        self.total_people_label.pack(fill="x", padx=10, pady=(5, 0))

        self.total_tasks_label = ctk.CTkLabel(self, text="", anchor="w", font=self.style["font"], height=15)
        self.total_tasks_label.pack(fill="x", padx=10, pady=5)

        self.total_completed_tasks_label = ctk.CTkLabel(self, text="", anchor="w", font=self.style["font"], height=15)
        self.total_completed_tasks_label.pack(fill="x", padx=10, pady=0)

        self.line()

        self.people_label = ctk.CTkLabel(self, text="Pessoas:", anchor="w", font=("Tahoma", 12, "bold"))
        self.people_label.pack(fill="x", padx=10, pady=0)

        self.line()

        self.tasks_label = ctk.CTkLabel(self, text="Tarefas:", anchor="w", font=("Tahoma", 12, "bold"))
        self.tasks_label.pack(fill="x", padx=10, pady=0)
