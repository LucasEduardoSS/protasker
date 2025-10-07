from services.sector_service import SectorService
from services.person_service import PersonService
from services.task_service import TaskService
from services.distribution_service import DistributionService
from services.assignment_service import AssignmentService


class DataFacade:
    """Centraliza chamadas relacionadas a dados."""

    @staticmethod
    def get_all_data(entity: str) -> list[dict]:
        """Obtém todos os registros de uma entidade."""
        if entity == "sector":
            return SectorService.get_all_sectors()
        elif entity == "person":
            return PersonService.get_all_people()
        elif entity == "task":
            return TaskService.get_tasks()
        elif entity == "distro":
            return DistributionService.get_all_distributions()
        elif entity == "assignment":
            return AssignmentService.get_all_assignments()
        else:
            raise ValueError(f"Entidade '{entity}' não suportada.")

    @staticmethod
    def get_record(entity: str, record_id: int):
        """Obtém um único registro por entidade e ID."""
        if entity == "sector":
            return SectorService.get_sector_by_id(record_id)
        elif entity == "person":
            return PersonService.get_person_by_id(record_id)
        elif entity == "task":
            return TaskService.get_task_by_id(record_id)
        elif entity == "distro":
            return DistributionService.get_distribution_by_id(record_id)
        elif entity == "assignment":
            return AssignmentService.get_assignment_by_id(record_id)
        else:
            raise ValueError(f"Entidade '{entity}' não suportada.")

    @staticmethod
    def create_record(entity: str, data: dict):
        """Cria um novo registro por entidade."""
        if entity == "sector":
            return SectorService.create_sector(data)
        elif entity == "person":
            return PersonService.create_person(data)
        elif entity == "task":
            return TaskService.create_task(data)
        elif entity == "distro":
            return DistributionService.create_distribution(data)
        elif entity == "assignment":
            return AssignmentService.create_assignment(data)
        return None

    @staticmethod
    def update_record(entity: str, record_id: int, new_data: dict):
        """Atualiza um registro por entidade e ID."""
        if entity == "sector":
            SectorService.update_sector(record_id, new_data)
        elif entity == "person":
            PersonService.update_person(record_id, new_data)
        elif entity == "task":
            TaskService.update_task(record_id, new_data)
        return None

    @staticmethod
    def delete_record(entity: str, record_id: int):
        """Remove um registro por entidade e ID."""
        if entity == "sector":
            SectorService.delete_sector(record_id)
        elif entity == "person":
            PersonService.delete_person(record_id)
        elif entity == "task":
            TaskService.delete_task(record_id)
        elif entity == "distro":
            DistributionService.delete_distribution(record_id)
        return None

    @staticmethod
    def get_fields(entity: str):
        match entity:
            case "sector":
                return SectorService.get_fields()
            case "person":
                return PersonService.get_fields()
            case "task":
                return TaskService.get_fields()
        return None
