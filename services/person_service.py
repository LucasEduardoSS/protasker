from models.person_model import Person


class PersonService:
    """Lida com operações relacionadas a pessoas."""

    @staticmethod
    def get_all_people() -> list[dict]:
        return Person.select().dicts()

    @staticmethod
    def get_person_by_id(person_id: int):
        return Person.get(Person.id == person_id)

    @staticmethod
    def get_person_by_name(name: str):
        return Person.get_or_none(Person.name == name)

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
