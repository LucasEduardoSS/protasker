import customtkinter as ctk

from views.sidebar.tabs.sidebar_base_tab_view import SidebarBaseTabView
from models.person_model import Person
from models.task_model import Task
from models.sector_model import Sector
from services.task_service import TaskService
from services.person_service import PersonService
from services.assignment_service import AssignmentService


class DetailsTabView(SidebarBaseTabView):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.label.configure(text="Detalhes")

    def load_details(self, model, item_info: dict):
        """ Atualiza a visualização dos detalhes com as informações do item selecionado. """

        # Certifica que existe dados
        if not item_info or not model:
            return

        # Limpa todos os itens
        for widget in self.winfo_children():
            if widget == self.tab_top_bar:
                continue
            widget.destroy()


        if model == Person:
            template = TemplatePerson(self, width=300, height=100)
            template.pack(fill="both", expand=True, padx=10, pady=5)
            template.pack_propagate(False)

            template.name_label.configure(text=item_info["name"])
            template.sector_label.configure(text=f"{Sector.get_by_id(item_info["sector"]).name} | ")
            template.role_label.configure(text=item_info["role"])
            template.total_assigned_tasks.configure(text=f"Total: {AssignmentService.get_assignment_by_person(item_info["id"]).__len__()}")
            template.total_completed_tasks.configure(text=f"Concluídas: {TaskService.get_completed_tasks_by_person(item_info['id']).__len__()}")

            template.load_tasks(TaskService.get_tasks_by_person(item_info["id"]))

        elif model == Task:
            template = TemplateTask(self, width=300, height=100)
            template.pack(fill="both", expand=True, padx=10, pady=5)
            template.pack_propagate(False)

            template.name_label.configure(text=item_info["name"])
            template.company_sector_label.configure(text=f"{item_info['company']} | {Sector.get_by_id(item_info['sector']).name}")
            template.description_label.configure(text=item_info["description"])
            template.status_label.configure(text=f"Status: {item_info["status"]}")

            template.load_people(PersonService.get_people_by_task(item_info["id"]))

        elif model == Sector:
            template = TemplateSector(self, width=300, height=100)
            template.pack(fill="both", expand=True, padx=10, pady=5)
            template.pack_propagate(False)

            template.name_label.configure(text=item_info["name"])
            template.total_people_label.configure(text=f"{PersonService.get_people_by_sector(item_info["id"]).__len__()} pessoas")
            template.total_tasks_label.configure(text=f"{TaskService.get_tasks_by_sector(item_info["id"]).__len__()} tarefas")

            template.load_people(PersonService.get_people_by_sector(item_info["id"]))
            template.load_tasks(TaskService.get_tasks_by_sector(item_info["id"]))
        else:
            print("Erro.")


# Experimental
def style_config() -> dict:
    return {
        "font": ("Tahoma", 11)
    }


class TemplatePerson(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(fg_color="#2E333C", corner_radius=0)
        self.style = style_config()

        self.name_label = ctk.CTkLabel(self, text="Nome", anchor="w", font=("Tahoma", 14, "bold"))
        self.name_label.pack(fill="x", padx=10, pady=0)

        self.sector_role_frame = ctk.CTkFrame(self, fg_color="#2E333C", corner_radius=0, height=15)
        self.sector_role_frame.pack(fill="x", padx=10, pady=(0, 10))

        self.sector_label = ctk.CTkLabel(self.sector_role_frame, text="Setor", anchor="w", font=self.style["font"], height=15)
        self.sector_label.pack(side="left")

        self.role_label = ctk.CTkLabel(self.sector_role_frame, text="Cargo", anchor="w", font=self.style["font"], height=15)
        self.role_label.pack(side="left", padx=(0, 10))

        self.tasks_label = ctk.CTkLabel(self, text="Tarefas:", anchor="w", font=("Tahoma", 12, "bold"))
        self.tasks_label.pack(fill="x", padx=10, pady=0)

        self.total_assigned_tasks = ctk.CTkLabel(self, text="", anchor="w", font=self.style["font"], height=15)
        self.total_assigned_tasks.pack(fill="x", padx=10, pady=0)

        self.total_completed_tasks = ctk.CTkLabel(self, text="", anchor="w", font=self.style["font"])
        self.total_completed_tasks.pack(fill="x", padx=10, pady=0)

        self.line = ctk.CTkFrame(self, height=2, fg_color="#3E4D66", corner_radius=0)
        self.line.pack(fill="x", padx=10, pady=5)

    def load_tasks(self, tasks):
        for task in tasks:
            task_label = ctk.CTkLabel(self, text=f"- {task["name"]}: {task["status"]}", anchor="w", font=self.style["font"])
            task_label.pack(fill="x", padx=10, pady=0)


class TemplateTask(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(fg_color="#2E333C", corner_radius=0)
        self.style = style_config()

        self.name_label = ctk.CTkLabel(self, text="", anchor="w", font=("Tahoma", 14, "bold"))
        self.name_label.pack(fill="x", padx=10, pady=0)

        self.company_sector_label = ctk.CTkLabel(self, text="", anchor="w", font=self.style["font"], height=15)
        self.company_sector_label.pack(fill="x", padx=10, pady=0)

        self.description_label = ctk.CTkLabel(self, text="", anchor="w", font=self.style["font"])
        self.description_label.pack(fill="x", padx=10, pady=5)

        self.status_label = ctk.CTkLabel(self, text="", anchor="w", font=self.style["font"])
        self.status_label.pack(fill="x", padx=10, pady=0)

        self.line = ctk.CTkFrame(self, height=2, fg_color="#3E4D66", corner_radius=0)
        self.line.pack(fill="x", padx=10, pady=5)

        self.people_label = ctk.CTkLabel(self, text="Encarregados:", anchor="w", font=("Tahoma", 12, "bold"))
        self.people_label.pack(fill="x", padx=10, pady=0)

    def load_people(self, people: list):
        for person in people:
            person_label = ctk.CTkLabel(self, text=f"- {person['name']}", anchor="w", font=self.style["font"])
            person_label.pack(fill="x", padx=10, pady=0)


class TemplateSector(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(fg_color="#2E333C", corner_radius=0)
        self.style = style_config()

        self.name_label = ctk.CTkLabel(self, text="", anchor="w", font=("Tahoma", 14, "bold"))
        self.name_label.pack(fill="x", padx=10, pady=0)

        self.total_people_label = ctk.CTkLabel(self, text="", anchor="w", font=self.style["font"], height=15)
        self.total_people_label.pack(fill="x", padx=10, pady=(5, 0))

        self.total_tasks_label = ctk.CTkLabel(self, text="", anchor="w", font=self.style["font"], height=15)
        self.total_tasks_label.pack(fill="x", padx=10, pady=5)

        self.line = ctk.CTkFrame(self, height=2, fg_color="#3E4D66", corner_radius=0)
        self.line.pack(fill="x", padx=10, pady=5)

        self.people_label = ctk.CTkLabel(self, text="Pessoas:", anchor="w", font=("Tahoma", 12, "bold"))
        self.people_label.pack(fill="x", padx=10, pady=0)

        self.line = ctk.CTkFrame(self, height=2, fg_color="#3E4D66", corner_radius=0)
        self.line.pack(fill="x", padx=10, pady=5)

        self.tasks_label = ctk.CTkLabel(self, text="Tarefas:", anchor="w", font=("Tahoma", 12, "bold"))
        self.tasks_label.pack(fill="x", padx=10, pady=0)

    def load_people(self, people: list):
        for person in people:
            person_label = ctk.CTkLabel(self, text=f"- {person['name']}", anchor="w", font=self.style["font"])
            person_label.pack(fill="x", padx=10, pady=0, after=self.people_label)

    def load_tasks(self, tasks: list):
        for task in tasks:
            task_label = ctk.CTkLabel(self, text=f"- {task['name']}: {task["status"]}", anchor="w", font=self.style["font"])
            task_label.pack(fill="x", padx=10, pady=0, after=self.tasks_label)


class TemplateDistro(ctk.CTkFrame):
    pass
