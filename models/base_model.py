from peewee import Model

# Supondo que 'database' seja a instância do seu banco de dados importada de 'database.db'
from database.db import database


class BaseModel(Model):
    """
    Modelo base para todos os outros modelos do projeto.

    Responsabilidades:
    - Conectar todos os modelos à mesma instância do banco de dados.
    - Fornecer representações de string padrão (__str__, __repr__) para depuração.

    Esta classe intencionalmente NÃO contém métodos de acesso a dados
    (como get_by_id, get_all), pois essa responsabilidade é delegada
    às classes de Serviço (Service Layer).
    """
    class Meta:
        database = database

    def __str__(self):
        # Retorna o nome da classe, ex: "Task"
        return self.__class__.__name__

    def __repr__(self):
        # Retorna uma representação útil para debug, ex: "<Task: 1>"
        # O 'getattr' é usado para evitar erro se o objeto ainda não tiver um id.
        return f"<{self.__class__.__name__}: {getattr(self, 'id', 'unsaved')}>"
