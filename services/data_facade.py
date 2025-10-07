from services.sector_service import SectorService
from services.person_service import PersonService
from services.task_service import TaskService
from services.distribution_service import DistributionService
from services.assignment_service import AssignmentService


class DataFacade:
    """ Centraliza chamadas relacionadas a dados. """

    @staticmethod
    def get_all_data(entity: str) -> list[dict]:
        """ Obtém todos os registros de uma entidade. """
        match entity.lower():
            case "sector":
                return SectorService.get_all_sectors()
            case "person":
                return PersonService.get_all_people()
            case "task":
                return TaskService.get_tasks()
            case "distro":
                return DistributionService.get_all_distributions()
            case "assignment":
                return AssignmentService.get_all_assignments()
            case _:
                raise ValueError(f"Entidade '{entity.lower()}' não suportada.")

    @staticmethod
    def get_record(entity: str, record_id: int):
        """ Obtém um único registro por entidade e ID. """
        match entity.lower():
            case "sector":
                return SectorService.get_sector_by_id(record_id)
            case "person":
                return PersonService.get_person_by_id(record_id)
            case "task":
                return TaskService.get_task_by_id(record_id)
            case "distro":
                return DistributionService.get_distribution_by_id(record_id)
            case "assignment":
                return AssignmentService.get_assignment_by_id(record_id)
            case _:
                raise ValueError(f"Entidade '{entity.lower()}' não suportada.")

    @staticmethod
    def create_record(entity: str, data: dict):
        """ Cria um novo registro por entidade. """
        match entity.lower():
            case "sector":
                return SectorService.create_sector(data)
            case "person":
                return PersonService.create_person(data)
            case "task":
                return TaskService.create_task(data)
            case "distro":
                return DistributionService.create_distribution(data)
            case "assignment":
                return AssignmentService.create_assignment(data)
            case _:
                raise ValueError(f"Entidade '{entity.lower()}' não suportada.")

    @staticmethod
    def update_record(entity: str, record_id: int, new_data: dict):
        """ Atualiza um registro por entidade e ID. """
        match entity.lower():
            case "sector":
                return SectorService.update_sector(record_id, new_data)
            case "person":
                return PersonService.update_person(record_id, new_data)
            case "task":
                return TaskService.update_task(record_id, new_data)
            case _:
                raise ValueError(f"Entidade '{entity.lower()}' não suportada.")

    @staticmethod
    def delete_record(entity: str, record_id: int):
        """ Remove um registro por entidade e ID. """
        match entity.lower():
            case "sector":
                return SectorService.delete_sector(record_id)
            case "person":
                return PersonService.delete_person(record_id)
            case "task":
                return TaskService.delete_task(record_id)
            case "distro":
                return DistributionService.delete_distribution(record_id)
            case _:
                raise ValueError(f"Entidade '{entity.lower()}' não suportada.")

    @staticmethod
    def get_fields(entity: str):
        """ Retorna os campos de uma entidade. """
        match entity.lower():
            case "sector":
                return SectorService.get_fields()
            case "person":
                return PersonService.get_fields()
            case "task":
                return TaskService.get_fields()
            case _:
                raise ValueError(f"Entidade '{entity.lower()}' não suportada.")
