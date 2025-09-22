from models.distribution_model import Distribution


class DistributionService:
    """Lida com operações relacionadas a distribuições."""

    @staticmethod
    def get_all_distributions():
        return Distribution.select().dicts()

    @staticmethod
    def get_distribution_by_id(distro_id: int):
        return Distribution.get(Distribution.id == distro_id)

    @staticmethod
    def create_distribution(data: dict) -> Distribution:
        distro = Distribution(**data)
        distro.save()
        return distro

    @staticmethod
    def update_distribution(distro_id: int, new_data: dict):
        query = Distribution.update(**new_data).where(Distribution.id == distro_id)
        query.execute()

    @staticmethod
    def delete_distribution(distro_id: int):
        query = Distribution.delete().where(Distribution.id == distro_id)
        query.execute()
