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
    def get_completed_tasks_by_distro(distro_id: int):
        from peewee import JOIN

        # Junção entre Assignment e Task, filtrando pela distribuição especificada e status de tarefa "Concluído"
        completed_tasks = (
            Task.select()
            .join(Assignment, JOIN.INNER, on=(Assignment.task == Task.id))
            .where((Assignment.distro_id == distro_id) & (Task.status == "Concluída"))
        )
        return list(completed_tasks.dicts())

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
