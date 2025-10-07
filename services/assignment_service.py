from models.assignment_model import Assignment


class AssignmentService:
    """Lida com operações relacionadas a pessoas."""

    # Operações básicas

    @staticmethod
    def get_all_assignments():
        return Assignment.select(Assignment)

    @staticmethod
    def get_assignment_by_id(assignment_id: int):
        return Assignment.get(Assignment.id == assignment_id)

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

    # Operações especiais

    @classmethod
    def apply_filter(
            cls,
            query,
            sector_id: int = None,
            distro_id: int = None,
            person_id: int = None,
            person_ids: list[int] = None
        ):
        # Aplica filtros
        if sector_id:
            query = query.where(Assignment.sector == sector_id)
        if distro_id:
            query = query.where(Assignment.distro_id == distro_id)
        if person_id:
            query = query.where(Assignment.person == person_id)
        if person_ids:
            query = query.where(Assignment.person.in_(person_ids))
        return query

    @staticmethod
    def get_assignments(
            sector_id: int = None,
            distro_id: int = None,
            person_id: int = None,
            person_ids: list = None
    ) -> list[dict]:
        """
        Busca atribuições com base em um conjunto flexível de filtros.
        """

        query = Assignment.select()
        query = AssignmentService.apply_filter(query, sector_id, distro_id, person_id, person_ids)
        return list(query.dicts())

    @staticmethod
    def delete_assignments(
            sector_id: int = None,
            distro_id: int = None,
            person_id: int = None,
            person_ids: list = None
    ):
        """
        Busca atribuições com base em um conjunto flexível de filtros.
        """

        query = Assignment.delete()
        query = AssignmentService.apply_filter(query, sector_id, distro_id, person_id, person_ids)
        query.execute()

    @staticmethod
    def get_fields():
        """Retorna os campos de Assignment."""
        return Assignment._meta.sorted_field_names
