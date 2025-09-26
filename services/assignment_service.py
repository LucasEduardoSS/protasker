from models.assignment_model import Assignment


class AssignmentService:
    """Lida com operações relacionadas a pessoas."""

    @staticmethod
    def get_all_assignments():
        return Assignment.select(Assignment)

    @staticmethod
    def get_assignment_by_id(assignment_id: int):
        return Assignment.get(Assignment.id == assignment_id)

    @staticmethod
    def get_assignment_by_distro(distro_id: int):
        return Assignment.select().where(Assignment.distro == distro_id)

    @staticmethod
    def get_assignment_by_person(person_id: int):
        return Assignment.select().where(Assignment.person == person_id)

    @staticmethod
    def get_assignment_by_task(task_id: int):
        return Assignment.select().where(Assignment.task == task_id)

    @staticmethod
    def create_assignment(data: dict) -> Assignment:
        assignment = Assignment(**data)
        assignment.save()
        return assignment

    @staticmethod
    def update_assignment(assignment_id: int, new_data: dict):
        query = Assignment.update(**new_data).where(Assignment.id == assignment_id)
        query.execute()

    @staticmethod
    def delete_assignment(assignment_id: int):
        query = Assignment.delete().where(Assignment.id == assignment_id)
        query.execute()
