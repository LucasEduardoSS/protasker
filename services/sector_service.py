from models.sector_model import Sector


class SectorService:
    """Lida com operações relacionadas a setores."""

    @staticmethod
    def get_all_sectors():
        """Obtém todos os setores no banco de dados."""
        return Sector.select().dicts()

    @staticmethod
    def get_sector_by_id(sector_id: int):
        """Obtém um setor pelo ID."""
        return Sector.get(Sector.id == sector_id)

    @staticmethod
    def create_sector(data: dict = None):
        """Cria um novo setor."""
        sector = Sector(**data)
        sector.save()
        return sector

    @staticmethod
    def update_sector(sector_id: int, new_data: dict):
        """Atualiza os dados de um setor."""
        query = Sector.update(**new_data).where(Sector.id == sector_id)
        query.execute()

    @staticmethod
    def delete_sector(sector_id: int):
        """Exclui um setor pelo ID."""
        query = Sector.delete().where(Sector.id == sector_id)
        query.execute()


    @staticmethod
    def get_fields():
        """Obtém os nomes dos campos do modelo Sector."""
        return Sector._meta.fields.items()
