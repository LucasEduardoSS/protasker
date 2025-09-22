from services.sector_service import SectorService
from services.person_service import PersonService
from services.task_service import TaskService
from services.distribution_service import DistributionService
from services.assignment_service import AssignmentService


class DataFacade:
    """Centraliza chamadas relacionadas a dados."""

    @staticmethod
    def get_all_data(entity: str):
        """Obtém todos os registros de uma entidade."""
        if entity == "sectors":
            return SectorService.get_all_sectors()
        elif entity == "people":
            return PersonService.get_all_people()
        elif entity == "tasks":
            return TaskService.get_all_tasks()
        elif entity == "distros":
            return DistributionService.get_all_distributions()
        elif entity == "assignments":
            return AssignmentService.get_all_assignments()
        else:
            raise ValueError(f"Entidade '{entity}' não suportada.")

    @staticmethod
    def get_record(entity: str, record_id: int):
        """Obtém um único registro por entidade e ID."""
        if entity == "sectors":
            return SectorService.get_sector_by_id(record_id)
        elif entity == "people":
            return PersonService.get_person_by_id(record_id)
        elif entity == "tasks":
            return TaskService.get_task_by_id(record_id)
        elif entity == "distros":
            return DistributionService.get_distribution_by_id(record_id)
        elif entity == "assignments":
            return AssignmentService.get_assignment_by_id(record_id)
        else:
            raise ValueError(f"Entidade '{entity}' não suportada.")