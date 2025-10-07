from models.assignment_model import Assignment
from models.task_model import Task


class TaskService:
    """
    Lida com operações relacionadas a tarefas.
    Os métodos retornam apenas objetos Task model.
    """

    @staticmethod
    def get_all_tasks():
        return Task.select().dicts()

    @staticmethod
    def get_task_by_id(task_id: int):
        return Task.get(Task.id == task_id)

    @staticmethod
    def get_task_by_name(name: str):
        return Task.get_or_none(Task.name == name)

    @staticmethod
    def create_task(data: dict):
        task = Task(**data)
        task.save()
        return task

    @staticmethod
    def update_task(task_id: int, new_data: dict):
        query = Task.update(**new_data).where(Task.id == task_id)
        query.execute()

    @staticmethod
    def delete_task(task_id: int):
        query = Task.delete().where(Task.id == task_id)
        query.execute()


    @staticmethod
    def get_tasks_by_distro(distro_id: int) -> list[dict]:
        from peewee import JOIN

        # Junção entre Assignment e Task, filtrando pela distribuição especificada
        completed_tasks = (
            Task.select()
            .join(Assignment, JOIN.INNER, on=(Assignment.task == Task.id))
            .where(Assignment.distro_id == distro_id)
        )
        return list(completed_tasks.dicts())

    @staticmethod
    def get_completed_tasks_by_distro(distro_id: int) -> list[dict]:
        from peewee import JOIN

        # Junção entre Assignment e Task, filtrando pela distribuição especificada e status de tarefa "Concluído"
        completed_tasks = (
            Task.select()
            .join(Assignment, JOIN.INNER, on=(Assignment.task == Task.id))
            .where((Assignment.distro_id == distro_id) & (Task.status == "Concluída"))
        )
        return list(completed_tasks.dicts())

    @staticmethod
    def get_completed_tasks_by_person(person_id: int) -> list[dict]:
        from peewee import JOIN

        completed_tasks = (
            Task.select()
            .join(Assignment, JOIN.INNER, on=(Assignment.task == Task.id))
            .where((Assignment.person == person_id) & (Task.status == "Concluída"))
        )
        return list(completed_tasks.dicts())

    @staticmethod
    def get_tasks_by_person(person_id: int) -> list[dict]:
        from peewee import JOIN

        tasks = (
            Task.select()
            .join(Assignment, JOIN.INNER, on=(Assignment.task == Task.id))
            .where(Assignment.person == person_id)
        )
        return list(tasks.dicts())

    @staticmethod
    def get_completed_tasks_by_sector(sector_id: int):
        return list(Task.select().where((Task.sector == sector_id) & (Task.status == "Concluída")).dicts())

    @staticmethod
    def get_tasks_by_sector(sector_id: int):
        return list(Task.select().where(Task.sector == sector_id).dicts())

    @staticmethod
    def get_assigned_tasks():
        from models.assignment_model import Assignment
        from peewee import JOIN

        # Retorna todas as tarefas atribuídas a pelo menos uma pessoa como uma lista de dicionários
        assigned_tasks = (
            Task.select(Task.id, Task.name, Task.status)
                .join(Assignment, JOIN.INNER, on=(Assignment.task == Task.id))
                .where(Assignment.id.is_null(False))
                .dicts()  # Retorna os resultados como dicionários
        )
        return list(assigned_tasks)

    @staticmethod
    def get_unassigned_tasks():
        from models.assignment_model import Assignment
        from peewee import JOIN

        # Retorna todas as tarefas não atribuídas como uma lista de dicionários
        assigned_tasks = (
            Task.select(Task.id, Task.name, Task.status)
                .join(Assignment, JOIN.LEFT_OUTER, on=(Assignment.task == Task.id))
                .where(Assignment.id.is_null(True))
                .dicts()
        )
        return list(assigned_tasks)

    @staticmethod
    def get_assigned_tasks_by_sector(sector_id: int):
        from models.assignment_model import Assignment
        from peewee import JOIN

        assigned_tasks = (
            Task.select(Task.id, Task.name, Task.status)
                .join(Assignment, JOIN.INNER, on=(Assignment.task == Task.id))
                .where(Assignment.id.is_null(False) & (Task.sector == sector_id))
                .dicts()
        )
        return list(assigned_tasks)

    @staticmethod
    def get_tasks(
        sector_id: int = None,
        distro_id: int = None,
        person_id: int = None,
        status: str = None,
        assigned: bool = None
    ) -> list[dict]:
        """
        Busca tarefas com base em um conjunto flexível de filtros.
        """
        from models.assignment_model import Assignment
        from peewee import JOIN

        query = Task.select()

        # Adiciona JOINs apenas quando necessário
        if distro_id or person_id or assigned is not None:
            # Se 'assigned' for False, precisamos de um LEFT JOIN para encontrar tarefas sem atribuição
            join_type = JOIN.LEFT_OUTER if assigned is False else JOIN.INNER
            query = query.join(Assignment, join_type, on=(Assignment.task == Task.id))

        # Aplica filtros
        if sector_id:
            query = query.where(Task.sector == sector_id)
        if distro_id:
            query = query.where(Assignment.distro_id == distro_id)
        if person_id:
            query = query.where(Assignment.person == person_id)
        if status:
            query = query.where(Task.status == status)
        
        # Filtro booleano para tarefas atribuídas/não atribuídas
        # if assigned is True:
        #     query = query.where(Assignment.id.is_null(False))
        # elif assigned is False:
        #     query = query.where(Assignment.id.is_null(True))
        #query = query.where(Assignment.id.is_null(not assigned))

        # Filtro booleano para tarefas atribuídas/não atribuídas
        if assigned is not None:
            query = query.where(Assignment.id.is_null(not assigned))

        return list(query.dicts())

    @staticmethod
    def get_fields():
        """Retorna os campos de Task."""
        return Task._meta.fields.items()
