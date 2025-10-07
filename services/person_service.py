from models.person_model import Person
from models.assignment_model import Assignment


class PersonService:
    """Lida com operações relacionadas a pessoas."""

    # Operações básicas

    @staticmethod
    def get_all_people() -> list[dict]:
        return Person.select().dicts()

    @staticmethod
    def get_person_by_id(person_id: int):
        return Person.get(Person.id == person_id)

    @staticmethod
    def create_person(data: dict):
        person = Person(**data)
        person.save()
        return person

    @staticmethod
    def update_person(person_id: int, new_data: dict):
        query = Person.update(**new_data).where(Person.id == person_id)
        query.execute()

    @staticmethod
    def delete_person(person_id: int):
        query = Person.delete().where(Person.id == person_id)
        query.execute()

    # Operações especiais

    @staticmethod
    def get_person_by_name(name: str):
        return Person.get_or_none(Person.name == name)

    @staticmethod
    def get_people_by_sector(sector_name: str):
        return list(Person.select().where(Person.sector == sector_name).dicts())

    @staticmethod
    def get_people_by_task(task_id: int):
        from peewee import JOIN

        people = (
            Person.select()
            .join(Assignment, JOIN.INNER, on=(Assignment.person == Person.id))
            .where(Assignment.task == task_id)
        )
        return list(people.dicts())

    @staticmethod
    def get_people_by_distro(distro_id: int):
        from peewee import JOIN

        people = (
            Person.select()
            .join(Assignment, JOIN.INNER, on=(Assignment.person == Person.id))
            .where(Assignment.distro == distro_id)
        )
        return list(people.dicts())

    @staticmethod
    def get_fields():
        """Retorna os campos de Person."""
        return Person._meta.fields.items()
